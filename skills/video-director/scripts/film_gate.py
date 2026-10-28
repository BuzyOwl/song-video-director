"""Objective gates on a rendered video, so quality is measured before it is claimed.

Usage: python -I film_gate.py <video> [--feel feel.json] [--song song_facts.json] [--style STYLE.md] [--loop] [--json out.json]
Exit 0 = all HARD checks pass, 1 = a HARD check failed, 2 = the video could not be read.

HARD
  dead_gap       longest run with no visible change vs 0.5 s earlier > 1.0 s   (feel "still": [[t0,t1],...] spans are exempt)
  flicker        two luminance flashes (jump > 25/255 and back) < 0.17 s apart
  slideshow      duration-weighted share of shots with in-shot motion < 0.6 (still spans excluded)
  loop           --loop only: first vs last frame mean abs diff > 2/255
SOFT (INFO, never fails)
  short_shots   shots under 0.3 s (feel "flash" spans exempt). SOFT: finished films use 1-frame impact cuts on purpose
  sections   cuts/min, stillness ratio (0.5 s window: on-twos and slow drift count as moving), mean motion per section. Spans: feel "sections" [{t0,t1,cpm:[lo,hi],
             still:[lo,hi]}] (then in/out of band is reported), else song_facts "sections"/"hits", else whole film.
  feel_sync  Pearson r, motion vs audio energy at phrase scale (8 s smoothing; frame-level r was ~0 on every finished film)
  palette    k-means k=6 in CIE Lab, weighted mean dE76 to the nearest STYLE.md #RRGGBB; saturated accent hue count
  beat_hits  share of cuts within +-1 frame of a song_facts beat, and share landing 1-2 frames before one
Frame difference = mean abs diff in 0..255, max of gray (160 px wide) and RGB thumbnail (32x18, catches isoluminant cuts).
"""
import argparse, collections, json, re, subprocess, sys
import numpy as np

DEAD = 0.6          # diff below this: no visible change
MOTION = 1.0        # in-shot median diff above this: a moving shot
CUT_FLOOR = 8.0     # a cut clears this absolute diff ...
CUT_X = 4.0         # ... and this many times the rolling median of its neighbours
FLASH = 25.0        # mean-luminance jump that counts as a flash edge
LIMIT = dict(dead_gap=1.0, flicker=0.17, slideshow=0.6, short_shot=0.3, loop=2.0)
r3 = lambda x: None if x is None else round(float(x), 3)


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                          'stream=r_frame_rate,width,height', '-of', 'json', path], capture_output=True, check=True).stdout
    st = json.loads(out)['streams'][0]; num, den = map(int, st['r_frame_rate'].split('/'))
    return st['r_frame_rate'], num / den, st['width'], st['height']


def frames(path, rate, scale, pix, size):
    """Raw frames resampled to constant native fps (safe for VFR files)."""
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'fps={rate},scale={scale}:flags=area',
                          '-pix_fmt', pix, '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    while len(b := p.stdout.read(size)) == size:
        yield np.frombuffer(b, np.uint8).astype(np.int16)
    p.stdout.close(); p.wait()


def decode(path):
    rate, fps, w, h = probe(path)
    gh = max(2, round(80 * h / w) * 2)
    k = max(1, round(fps / 2)); ring = collections.deque(maxlen=k + 1)
    dg, dw, lum, first, prev = [], [], [], None, None
    for f in frames(path, rate, f'160:{gh}', 'gray', 160 * gh):       # streamed: memory stays flat on long films
        lum.append(f.mean()); ring.append(f)
        if prev is None: first = f
        else: dg.append(np.abs(f - prev).mean()); dw.append(np.abs(f - ring[0]).mean())   # vs 0.5 s ago: slow drift counts
        prev = f
    th = np.array(list(frames(path, rate, '32:18', 'rgb24', 32 * 18 * 3)))
    n = min(len(dg), len(th) - 1)
    if n < 1: raise ValueError('fewer than 2 frames decoded')
    d = np.maximum(np.array(dg[:n]), np.abs(np.diff(th[:n + 1], axis=0)).mean(1))
    return fps, d, np.array(dw[:n]), np.array(lum[:n + 1]), np.abs(first - prev).mean(), th.reshape(-1, 3)


def longest(mask):
    best = cur = at = 0
    for i, m in enumerate(mask):
        cur = cur + 1 if m else 0
        if cur > best: best, at = cur, i - cur + 1
    return best, at


def in_spans(t, spans):
    return np.array([any(a <= x <= b for a, b in spans) for x in t], bool)


def sections(feel, song, dur):
    """[(t0, t1, band)] from feel sections, else song_facts sections/hits (numbers, [t0,t1] or dicts), else whole film."""
    if feel.get('sections'):
        return [(float(s['t0']), float(s['t1']), s) for s in feel['sections']]
    items = []
    for x in song.get('sections') or song.get('hits') or []:
        if isinstance(x, (int, float)): t0, t1 = x, None
        elif isinstance(x, (list, tuple)) and x: t0, t1 = x[0], (x[1] if len(x) > 1 else None)
        elif isinstance(x, dict): t0, t1 = x.get('t0', x.get('start')), x.get('t1', x.get('end'))
        else: continue
        if t0 is not None: items.append([float(t0), t1, {}])
    items.sort(key=lambda s: s[0])
    if not items or items[0][0] > 0: items.insert(0, [0.0, None, {}])
    for i, s in enumerate(items):          # open-ended section runs to the next start (or the end)
        if s[1] is None: s[1] = items[i + 1][0] if i + 1 < len(items) else dur
    return [(a, min(float(b), dur), band) for a, b, band in items if min(float(b), dur) > a]


def lab(rgb):
    c = rgb / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    xyz = c @ np.array([[.4124, .3576, .1805], [.2126, .7152, .0722], [.0193, .1192, .9505]]).T / [.95047, 1, 1.08883]
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    return np.stack([116 * f[:, 1] - 16, 500 * (f[:, 0] - f[:, 1]), 200 * (f[:, 1] - f[:, 2])], 1)


def palette(px, style, k=6):
    rng = np.random.default_rng(0)
    px = px[rng.choice(len(px), min(len(px), 20000), replace=False)].astype(float)
    L = lab(px); C = L[rng.choice(len(L), k)]
    for _ in range(15):                    # ponytail: random-init Lloyd's, k-means++ if clusters look unstable
        lbl = ((L[:, None] - C[None]) ** 2).sum(2).argmin(1)
        C = np.array([L[lbl == j].mean(0) if (lbl == j).any() else C[j] for j in range(k)])
    w = np.bincount(lbl, minlength=k) / len(lbl)
    hexes = sorted(set(h.upper() for h in re.findall(r'#([0-9A-Fa-f]{6})\b', style)))
    ref = lab(np.array([[int(h[i:i + 2], 16) for i in (0, 2, 4)] for h in hexes], float)) if hexes else None
    cl = []
    for j in np.argsort(-w):
        if w[j] == 0: continue
        e = np.linalg.norm(ref - C[j], axis=1) if ref is not None else None
        cl.append({'hex': '#%02X%02X%02X' % tuple(px[lbl == j].mean(0).round().astype(int)), 'w': r3(w[j]),
                   'nearest': '#' + hexes[e.argmin()] if e is not None else None, 'dE': r3(e.min()) if e is not None else None})
    hues = sorted(np.degrees(np.arctan2(C[j, 2], C[j, 1])) % 360 for j in range(k) if w[j] >= .02 and np.hypot(*C[j, 1:]) > 40)
    acc = sum(1 for i, h in enumerate(hues) if i == 0 or h - hues[i - 1] > 30)
    if acc > 1 and hues[0] + 360 - hues[-1] <= 30: acc -= 1
    mean_de = sum(c['w'] * c['dE'] for c in cl) / sum(c['w'] for c in cl) if ref is not None else None
    return {'mean_dE': r3(mean_de), 'accents': acc, 'style_hexes': len(hexes), 'clusters': cl}


def audio_energy(song, path, fps, n):
    key = next((k for k in ('energy', 'rms') if song.get(k)), None)
    if key:
        e = np.array(song[key], float)
        return np.interp((np.arange(n) + 1) / fps, np.arange(len(e)) / float(song.get('fps') or fps), e), 'song.' + key
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-map', '0:a:0', '-ac', '1', '-ar', '16000',
                          '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(float)
    if not len(x): return None, 'none'
    idx = np.minimum((np.arange(len(x)) * fps / 16000).astype(int), n)    # audio sample -> video frame 0..n
    e = np.sqrt(np.bincount(idx, x * x, n + 1) / np.maximum(np.bincount(idx, minlength=n + 1), 1))
    return e[1:], 'audio'


def gate(path, feel, song, style, loop):
    fps, d, dw, lum, loop_diff, px = decode(path)
    n = len(d); dur = (n + 1) / fps; t = (np.arange(n) + 1) / fps          # diff i = frame i -> i+1, at time (i+1)/fps
    still = in_spans(t, feel.get('still') or [])
    flash = feel.get('flash') or []
    hard, soft = {}, {}

    run, at = longest((dw < DEAD) & ~still)
    gap = (run + 1) / fps if run else 0.0
    hard['dead_gap'] = {'pass': gap <= LIMIT['dead_gap'], 'longest_s': r3(gap), 'at_s': r3(at / fps), 'limit_s': LIMIT['dead_gap']}

    j = np.diff(lum); k = max(1, round(LIMIT['flicker'] * fps))
    spikes = [i for i in range(len(j)) if abs(j[i]) > FLASH and
              any(j[i] * j[m] < 0 and abs(j[m]) > FLASH for m in range(i + 1, min(len(j), i + 1 + k)))]
    # one flash = a run of same-sign edges (a bloom ramps over 2-3 frames); its onset is the run's first edge
    onsets = [x for n_, x in enumerate(spikes) if n_ == 0 or np.sign(j[x]) != np.sign(j[spikes[n_ - 1]])]
    same = {sg: [x for x in onsets if np.sign(j[x]) == sg] for sg in (1, -1)}          # bright-bright, dark-dark
    gaps = np.concatenate([np.diff(v) / fps for v in same.values()])
    min_gap = gaps.min() if len(gaps) else None
    bad = [v[i] for v in same.values() for i in range(len(v) - 1) if (v[i + 1] - v[i]) / fps < LIMIT['flicker']]
    hard['flicker'] = {'pass': min_gap is None or min_gap >= LIMIT['flicker'], 'spikes': len(spikes),
                       'min_gap_s': r3(min_gap), 'at_s': r3(bad[0] / fps) if bad else None, 'limit_s': LIMIT['flicker']}

    hw = max(3, round(fps / 4)); cut = np.zeros(n, bool)
    for i in range(n):
        nb = np.r_[d[max(0, i - hw):i], d[i + 1:i + 1 + hw]]
        cut[i] = d[i] > CUT_FLOOR and d[i] > CUT_X * (np.median(nb) if len(nb) else 0)
    for i in np.where(cut)[0]:             # a wipe or flash spans several spike frames: one transition, keep the first
        if cut[i]: cut[i + 1:i + 1 + hw] = False
    starts = [0] + [int(i) + 1 for i in np.where(cut)[0]]
    shots = list(zip(starts, starts[1:] + [n + 1]))                       # frame ranges [a, b)
    stillf = np.r_[still[:1], still]                                       # per-frame still mask
    wts = np.array([(~stillf[a:b]).sum() for a, b in shots], float)
    mov = np.array([b - a > 1 and np.median(dw[a:b - 1]) > MOTION for a, b in shots])
    share = (wts * mov).sum() / wts.sum() if wts.sum() else 1.0
    hard['slideshow'] = {'pass': share >= LIMIT['slideshow'], 'moving_share': r3(share), 'shots': len(shots),
                         'cuts': int(cut.sum()), 'limit': LIMIT['slideshow']}

    lens = [((b - a) / fps, a / fps) for a, b in shots if not any(a / fps <= f1 and b / fps >= f0 for f0, f1 in flash)]
    short, sat = min(lens) if lens else (None, None)
    soft['short_shots'] = {'count': sum(1 for x, _ in lens if x < LIMIT['short_shot']), 'shortest_s': r3(short), 'at_s': r3(sat)}
    if loop:
        hard['loop'] = {'pass': loop_diff <= LIMIT['loop'], 'diff': r3(loop_diff), 'limit': LIMIT['loop']}

    rows = []
    for t0, t1, band in sections(feel, song, dur):
        sel = (t >= t0) & (t < t1)
        cpm = cut[sel].sum() / ((t1 - t0) / 60); st = (dw[sel] < DEAD).mean() if sel.any() else 0.0
        row = {'t0': r3(t0), 't1': r3(t1), 'cpm': r3(cpm), 'still': r3(st), 'motion': r3(d[sel & ~cut].mean() if (sel & ~cut).any() else 0)}
        for key, v in (('cpm', cpm), ('still', st)):
            if band.get(key): row[key + '_ok'] = bool(band[key][0] <= v <= band[key][1])
        rows.append(row)
    soft['sections'] = {'sections': rows}

    box = lambda v: np.convolve(v, np.ones(max(1, round(8 * fps))) / max(1, round(8 * fps)), 'same')
    aud, src = audio_energy(song, path, fps, n)
    mot = box(np.minimum(dw, CUT_FLOOR))     # ponytail: cuts clipped to the cut floor so one cut can't dwarf the curve
    r = None
    if aud is not None and n > 2:
        aud = box(aud)
        if mot.std() > 1e-9 and aud.std() > 1e-9: r = np.corrcoef(mot, aud)[0, 1]
    soft['feel_sync'] = {'r': r3(r), 'source': src}
    soft['palette'] = palette(px, style)

    beats = np.array(song.get('beats') or [], float)
    if len(beats):
        tc = t[cut]; on = early = None
        if len(tc):
            g = beats[np.abs(beats[None] - tc[:, None]).argmin(1)] - tc          # nearest beat minus cut time
            on = (np.abs(g) <= 1 / fps + 1e-6).mean(); early = ((g > 1e-6) & (g <= 2 / fps + 1e-6)).mean()
        soft['beat_hits'] = {'on_beat': r3(on), 'early_1_2f': r3(early), 'cuts': len(tc), 'beats': len(beats)}
    return {'video': path, 'fps': r3(fps), 'duration_s': r3(dur), 'hard': hard, 'soft': soft,
            'pass': all(v['pass'] for v in hard.values())}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video'); ap.add_argument('--feel'); ap.add_argument('--song'); ap.add_argument('--style')
    ap.add_argument('--loop', action='store_true'); ap.add_argument('--json')
    a = ap.parse_args()
    load = lambda p: json.load(open(p, encoding='utf-8')) if p else {}
    try:
        res = gate(a.video, load(a.feel), load(a.song), open(a.style, encoding='utf-8').read() if a.style else '', a.loop)
    except (subprocess.CalledProcessError, ValueError, KeyError, IndexError) as e:
        sys.exit(print(f'film_gate: cannot read {a.video}: {e}', file=sys.stderr) or 2)
    flat = lambda v: ' '.join(f'{k}={x}' for k, x in v.items() if k != 'pass' and not isinstance(x, list))
    print(f"{a.video}  {res['duration_s']} s @ {res['fps']} fps")
    for name, v in res['hard'].items(): print(f"{'PASS' if v['pass'] else 'FAIL'} {name:14s} {flat(v)}")
    for name, v in res['soft'].items():
        print(f'INFO {name:14s} {flat(v)}')
        for row in v.get('sections', []) + v.get('clusters', []): print(f'       {flat(row)}')
    print('PASS overall' if res['pass'] else 'FAIL overall')
    if a.json: open(a.json, 'w', encoding='utf-8').write(json.dumps(res, indent=1, default=lambda o: o.item()))
    sys.exit(0 if res['pass'] else 1)


if __name__ == '__main__':
    main()
