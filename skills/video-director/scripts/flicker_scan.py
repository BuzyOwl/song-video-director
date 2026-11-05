"""Local flicker scan: find things that change for 1-3 frames and change back (z-fighting, crawling shadow maps,
glinting thin edges, decals a millimetre off their surface, shader thresholds tipping), even under a moving camera.

Method from Imaginative-Prompting/claude-video-skills `render-checks` (MIT), implemented here:
1. Align each frame's neighbours (up to 3 frames away) onto it with dense optical flow (Farneback), with a
   forward-backward check; where one direction fails and the other passes, the passing one reversed stands in.
2. A pixel scores when every frame of a 1-3 frame run differs from both the frame before and the frame after the run
   while those two agree:  score = min over run of min(d(f, before), d(f, after)) - d(before, after).
   Changes that stay (a word appears, a cut), ramps (fades) and uncoverings score ~0.
3. d() is tolerant, in CIELAB: how far a pixel lies outside the colour range of the 3x3 neighbourhood in the other frame.
4. Motion is quieted: score * 1 / (1 + (speed / 8 px)^2), speed in px/frame at 720 lines.
5. Events: seed > 12 dE, grow > 6 dE, specks dropped, grouped across frames with gaps <= 2. Strength = summed score per
   thousandth of the frame, so it reads the same at any resolution.
Outputs in --out: report.json (events ranked), mask.mp4 (white = flickering), sheets/event_NN.jpg (the region over 5
frames round its peak; bottom row = peak frame with flagged pixels in red). Judge every event on its sheet: designed
blinks, strobes and sparkles get flagged too.

Usage: python -I flicker_scan.py <video> [--start s] [--end s] [--out dir] [--height 720] [--top 20]
Calibrate --seed/--grow on a span with a known flicker and a known-clean span before trusting a new project.
"""
import argparse, collections, json, os, subprocess, sys
import numpy as np
import cv2

K3 = np.ones((3, 3), np.uint8)


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                          'stream=r_frame_rate,width,height', '-of', 'json', path], capture_output=True, check=True).stdout
    st = json.loads(out)['streams'][0]; num, den = map(int, st['r_frame_rate'].split('/'))
    return num / den, st['width'], st['height']


def frames(path, start, end, w, h):
    args = ['ffmpeg', '-v', 'error', '-ss', str(start), '-i', path]
    if end is not None: args += ['-t', str(end - start)]
    p = subprocess.Popen(args + ['-vf', f'scale={w}:{h}:flags=area', '-pix_fmt', 'bgr24', '-f', 'rawvideo', '-'],
                         stdout=subprocess.PIPE)
    size = w * h * 3
    while len(b := p.stdout.read(size)) == size:
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.stdout.close(); p.wait()


class Scan:
    def __init__(self, h, w, seed, grow, min_area):
        self.h, self.w, self.seed, self.grow, self.min_area = h, w, seed, grow, min_area
        self.gx, self.gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
        self.gray, self.lab, self.bgr, self.flow = {}, {}, {}, {}
        self.calm = 8.0 * h / 720                                  # the 8 px quieting speed, at this height

    def add(self, i, bgr):
        self.bgr[i] = bgr
        self.gray[i] = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        lab = cv2.cvtColor(bgr.astype(np.float32) / 255, cv2.COLOR_BGR2Lab)
        # 4:2:0 delivery stores colour at half resolution: compare a*, b* at that scale, or saturated edges under a pan
        # score as flicker when the chroma sampling phase alternates between odd and even pixel shifts
        lab[..., 1:] = cv2.blur(lab[..., 1:], (3, 3))
        self.lab[i] = lab

    def drop_before(self, i):
        for d in (self.gray, self.lab, self.bgr):
            for k in [k for k in d if k < i]: del d[k]
        for k in [k for k in self.flow if min(k) < i - 1]: del self.flow[k]

    def of(self, a, b):                                            # flow a -> b: a(x) ~ b(x + f(x))
        if (a, b) not in self.flow:
            self.flow[(a, b)] = cv2.calcOpticalFlowFarneback(self.gray[a], self.gray[b], None, 0.5, 4, 31, 3, 5, 1.1, 0)
        return self.flow[(a, b)]

    def warp(self, img, f):
        return cv2.remap(img, self.gx + f[..., 0], self.gy + f[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    def fb_ok(self, f, r):                                         # forward-backward consistency of f, in f's frame
        err = np.linalg.norm(f + self.warp(r, f), axis=2)
        x, y = self.gx + f[..., 0], self.gy + f[..., 1]
        inside = (x >= 0) & (x <= self.w - 1) & (y >= 0) & (y <= self.h - 1)
        return inside & (err < 0.5 + 0.05 * np.linalg.norm(f, axis=2))

    def onto(self, i, n):
        """Neighbour n warped onto frame i, plus the mask of pixels where that alignment can be trusted."""
        f, r = self.of(i, n), self.of(n, i)
        ok_f, ok_r = self.fb_ok(f, r), self.fb_ok(r, f)
        # ponytail: the reversed backward flow is read at the same pixel (fine for the small motions where it matters)
        alt = ~ok_f & ok_r
        f = np.where(alt[..., None], -r, f)
        return self.warp(self.lab[n], f), ok_f | alt

    @staticmethod
    def outside(x, nb):                                            # dE of x outside nb's 3x3 colour range
        lo, hi = cv2.erode(nb, K3), cv2.dilate(nb, K3)
        d = np.maximum(0, np.maximum(lo - x, x - hi))
        return np.sqrt((d * d).sum(2))

    def score(self, i, last):
        """Scores for runs starting at frame i, in frame i's coordinates. Returns {frame: score map}."""
        out = {}
        if i - 1 not in self.lab: return out
        B, vb = self.onto(i, i - 1)
        speed = np.linalg.norm(self.of(i, i + 1), axis=2) if i + 1 <= last else np.zeros((self.h, self.w), np.float32)
        quiet = 1 / (1 + (speed / self.calm) ** 2)
        run_frames, valid = [self.lab[i]], vb.copy()
        for run in (1, 2, 3):
            after = i + run
            if after > last: break
            if run > 1:                                            # the run grows: frame i+run-1 joins it
                R, vr = self.onto(i, i + run - 1); run_frames.append(R); valid &= vr
            A, va = self.onto(i, after)
            inside = np.min([np.minimum(self.outside(R, B), self.outside(R, A)) for R in run_frames], axis=0)
            s = (inside - self.outside(B, A)) * quiet
            s[~(valid & va)] = 0
            s = np.maximum(s, 0)
            for j in range(i, after):                              # ponytail: later run frames reuse frame i's coordinates
                out[j] = np.maximum(out[j], s) if j in out else s
        return out

    def regions(self, s):
        n, lbl, st, _ = cv2.connectedComponentsWithStats((s > self.grow).astype(np.uint8), connectivity=8)
        keep = set(np.unique(lbl[s > self.seed]).tolist()) - {0}
        for l in keep:
            x, y, w, h, area = st[l]
            if area < self.min_area or min(w, h) < 2: continue    # specks and one-pixel lines
            yield (int(x), int(y), int(w), int(h)), float(s[lbl == l].sum()), float(s[lbl == l].max())


def strip(scan, f, box, s):
    x, y, w, h = box; pad = max(16, w // 2, h // 2)
    x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(scan.w, x + w + pad), min(scan.h, y + h + pad)
    tiles = [scan.bgr[k][y0:y1, x0:x1] if k in scan.bgr else np.zeros((y1 - y0, x1 - x0, 3), np.uint8)
             for k in range(f - 2, f + 3)]
    peak = scan.bgr[f][y0:y1, x0:x1].copy()
    peak[s[y0:y1, x0:x1] > scan.grow] = (0, 0, 255)
    blank = np.zeros_like(peak)
    rows = [np.hstack(tiles), np.hstack([blank, blank, peak, blank, blank])]
    sheet = np.vstack(rows)
    k = 160 / (y1 - y0)
    return cv2.resize(sheet, None, fx=k, fy=k, interpolation=cv2.INTER_NEAREST if k > 1 else cv2.INTER_AREA)


def scan_video(path, start=0.0, end=None, out='flicker', height=720, seed=12.0, grow=6.0, top=20):
    fps, W, H = probe(path)
    h = min(height, H) // 2 * 2; w = round(W * h / H / 2) * 2
    scan = Scan(h, w, seed, grow, min_area=max(4, round(12 * (h / 720) ** 2)))
    os.makedirs(os.path.join(out, 'sheets'), exist_ok=True)
    mask = cv2.VideoWriter(os.path.join(out, 'mask.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h), False)
    src = frames(path, start, end, w, h)
    loaded, last, pending, events, compared = -1, None, {}, [], 0
    pad = 0.03 * w                                                  # merge regions this close (flow can split a flat patch)

    def load_to(k):
        nonlocal loaded, last
        while last is None and loaded < k:
            b = next(src, None)
            if b is None: last = loaded; break
            loaded += 1; scan.add(loaded, b)

    def finalize(f):
        nonlocal compared
        s = pending.pop(f, None)
        if s is None: s = np.zeros((h, w), np.float32)
        else: compared += 1
        mask.write(np.where(s > grow, 255, 0).astype(np.uint8))
        for box, total, peak in scan.regions(s):
            x, y, bw, bh = box
            hit = next((e for e in events if f - e['f1'] <= 3 and not (x > e['box'][2] + pad or x + bw < e['box'][0] - pad
                        or y > e['box'][3] + pad or y + bh < e['box'][1] - pad)), None)
            if hit is None:
                hit = {'f0': f, 'f1': f, 'box': [x, y, x + bw, y + bh], 'sum': 0.0, 'peak': -1.0}; events.append(hit)
            hit['f1'] = f; hit['sum'] += total
            hit['box'] = [min(hit['box'][0], x), min(hit['box'][1], y), max(hit['box'][2], x + bw), max(hit['box'][3], y + bh)]
            if peak > hit['peak']: hit.update(peak=peak, peak_f=f, sheet=strip(scan, f, box, s))

    i = 1
    load_to(4)
    if last is not None and last < 2: sys.exit(print('flicker_scan: fewer than 3 frames decoded', file=sys.stderr) or 2)
    finalize(0)
    while True:
        load_to(i + 3)
        if last is not None and i > last - 1: break
        for j, s in scan.score(i, last if last is not None else i + 3).items():
            pending[j] = np.maximum(pending[j], s) if j in pending else s
        finalize(i)
        scan.drop_before(i - 2)
        i += 1
    for f in range(i, (last if last is not None else loaded) + 1): finalize(f)
    mask.release()

    area = h * w / 1000
    events.sort(key=lambda e: -e['sum'])
    report = []
    for n, e in enumerate(events[:top] if top else events, 1):
        x0, y0, x1, y1 = e['box']
        cv2.imwrite(os.path.join(out, 'sheets', f'event_{n:02d}.jpg'), e['sheet'])
        report.append({'rank': n, 'strength': round(e['sum'] / area, 2), 'peak_dE': round(e['peak'], 1),
                       'frames': [e['f0'], e['f1']], 'peak_frame': e['peak_f'],
                       'peak_s': round(start + e['peak_f'] / fps, 3), 'source_frame': round(start * fps) + e['peak_f'],
                       'box_norm': [round(x0 / w, 3), round(y0 / h, 3), round(x1 / w, 3), round(y1 / h, 3)],
                       'sheet': f'sheets/event_{n:02d}.jpg'})
    total = (last if last is not None else loaded) + 1
    res = {'video': path, 'start_s': start, 'end_s': end, 'fps': fps, 'analysed_height': h, 'frames_read': total,
           'frames_scored': compared, 'params': {'seed_dE': seed, 'grow_dE': grow, 'calm_px': 8, 'at_lines': 720},
           'events_found': len(events), 'events': report}
    json.dump(res, open(os.path.join(out, 'report.json'), 'w'), indent=1)
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video'); ap.add_argument('--start', type=float, default=0.0); ap.add_argument('--end', type=float)
    ap.add_argument('--out', default='flicker'); ap.add_argument('--height', type=int, default=720)
    ap.add_argument('--seed', type=float, default=12.0); ap.add_argument('--grow', type=float, default=6.0)
    ap.add_argument('--top', type=int, default=20)
    a = ap.parse_args()
    r = scan_video(a.video, a.start, a.end, a.out, a.height, a.seed, a.grow, a.top)
    print(f"{a.video}  {r['frames_read']} frames read, {r['frames_scored']} scored, {r['events_found']} events")
    if r['frames_scored'] < r['frames_read'] - 3:
        print('WARN fewer frames scored than read: check the span', file=sys.stderr)
    for e in r['events']:
        print(f"#{e['rank']:<3} strength {e['strength']:<8} peak {e['peak_dE']:>5} dE  t={e['peak_s']}s "
              f"src f{e['source_frame']}  frames {e['frames']}  box {e['box_norm']}  {e['sheet']}")


if __name__ == '__main__':
    main()
