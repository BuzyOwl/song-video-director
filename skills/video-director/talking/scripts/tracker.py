"""tracker.py - per-frame face box + hand gestures for a talking clip.

MediaPipe Tasks (face detector + gesture recognizer) when importable, OpenCV YuNet otherwise.
Boxes are interpolated across misses and One-Euro smoothed inside each shot (a jump cut is a real jump).
"""
import contextlib, math, os, subprocess, sys
from pathlib import Path

import numpy as np

MODELS = Path(os.environ.get("VD_MODELS", Path.home() / ".video-director" / "models"))
GESTURES = {"Pointing_Up": "point", "Open_Palm": "palm", "Thumb_Up": "thumb", "Victory": "victory"}
TW = 320  # detection width; faces are big in a selfie clip


@contextlib.contextmanager
def _quiet_stderr():
    """MediaPipe's C++ layer logs straight to fd 2; point it at devnull for the duration."""
    sys.stderr.flush()
    saved, null = os.dup(2), os.open(os.devnull, os.O_WRONLY)
    os.dup2(null, 2)
    try:
        yield
    finally:
        os.dup2(saved, 2)
        os.close(saved)
        os.close(null)


class OneEuro:
    """Casiez et al. 2012: low lag on real moves, strong smoothing on jitter."""

    def __init__(self, freq, min_cutoff=1.0, beta=0.02, d_cutoff=1.0):
        self.freq, self.mc, self.beta, self.dc = freq, min_cutoff, beta, d_cutoff
        self.x = self.dx = None
        self.t = None

    @staticmethod
    def _a(cutoff, dt):
        tau = 1 / (2 * math.pi * cutoff)
        return 1 / (1 + tau / dt)

    def filter(self, x, t):
        if self.x is None:
            self.x, self.dx, self.t = x, 0.0, t
            return x
        dt = max(t - self.t, 1e-3)
        self.t = t
        dx = (x - self.x) / dt
        self.dx = self.dx + self._a(self.dc, dt) * (dx - self.dx)
        cutoff = self.mc + self.beta * abs(self.dx)
        self.x = self.x + self._a(cutoff, dt) * (x - self.x)
        return self.x


def _frames(video, tw):
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", str(video)], capture_output=True, text=True, check=True)
    sw, sh = map(int, p.stdout.strip().split(","))
    th = int(round(sh * tw / sw / 2) * 2)
    proc = subprocess.Popen(["ffmpeg", "-v", "quiet", "-i", str(video), "-vf", f"scale={tw}:{th}", "-f", "rawvideo",
                             "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    try:
        while True:
            buf = proc.stdout.read(tw * th * 3)
            if len(buf) < tw * th * 3:
                break
            yield np.frombuffer(buf, np.uint8).reshape(th, tw, 3)
    finally:
        proc.stdout.close()
        proc.kill()  # no-op once ffmpeg has exited; frees it if the consumer stops early
        proc.wait()
    return sw, sh


def _mediapipe():
    """(name, face(rgb, i, fps) -> box|None, new_gesture() -> gesture(rgb, i, fps) -> name|None).
    Each new_gesture() is its own recognizer, so track() can run one per shot-aligned chunk in parallel."""
    import mediapipe as mp
    from mediapipe.tasks.python import BaseOptions
    from mediapipe.tasks.python import vision as v
    with _quiet_stderr():
        face = v.FaceDetector.create_from_options(v.FaceDetectorOptions(
            base_options=BaseOptions(model_asset_path=str(MODELS / "mediapipe" / "blaze_face_short_range.tflite")),
            running_mode=v.RunningMode.VIDEO, min_detection_confidence=0.5))
    warm = []

    def image(rgb):
        return mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))

    def detect_face(rgb, i, fps):
        if not warm:  # the first detect loads the inference delegate and logs: keep it quiet
            warm.append(1)
            with _quiet_stderr():
                return detect_face(rgb, i, fps)
        th, tw = rgb.shape[:2]
        r = face.detect_for_video(image(rgb), int(i * 1000 / fps))
        if not r.detections:
            return None
        d = max(r.detections, key=lambda d: d.bounding_box.width * d.bounding_box.height).bounding_box
        return [(d.origin_x + d.width / 2) / tw, (d.origin_y + d.height / 2) / th, d.width / tw, d.height / th]

    def new_gesture():
        with _quiet_stderr():
            gest = v.GestureRecognizer.create_from_options(v.GestureRecognizerOptions(
                base_options=BaseOptions(model_asset_path=str(MODELS / "mediapipe" / "gesture_recognizer.task")),
                running_mode=v.RunningMode.VIDEO, num_hands=2))
        quiet = []

        def detect_gesture(rgb, i, fps):
            if not quiet:
                quiet.append(1)
                with _quiet_stderr():
                    return detect_gesture(rgb, i, fps)
            g = gest.recognize_for_video(image(rgb), int(i * 1000 / fps))
            cats = [h[0].category_name for h in g.gestures if h]
            return next((GESTURES[c] for c in cats if c in GESTURES), None)
        return detect_gesture
    return "mediapipe", detect_face, new_gesture


def _yunet():
    import cv2
    det = cv2.FaceDetectorYN.create(str(MODELS / "yunet" / "face_detection_yunet_2023mar.onnx"), "", (TW, TW))

    sized = []

    def detect(rgb, i, fps):
        th, tw = rgb.shape[:2]
        if not sized:  # frame size is constant per video
            det.setInputSize((tw, th))
            sized.append(1)
        _, faces = det.detect(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
        if faces is None or len(faces) == 0:
            return None
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])[:4]
        return [(x + w / 2) / tw, (y + h / 2) / th, w / tw, h / th]
    return "yunet", detect, None


GESTURE_EVERY = 3  # gestures every 3rd frame: cheap and a gesture lasts far longer than 100 ms


def track(video, cut_frames, fps=30, stop=None, workers=3):
    try:
        name, face, new_gesture = _mediapipe()
    except Exception as e:  # mediapipe missing or model absent: YuNet still gives a steady box
        print("mediapipe unavailable, using YuNet:", e)
        name, face, new_gesture = _yunet()
    n_total = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-count_packets", "-show_entries",
                                  "stream=nb_read_packets", "-of", "csv=p=0", str(video)], capture_output=True,
                                 text=True, check=True).stdout.strip().rstrip(","))
    # Gesture recognition is ~3/4 of the cost. Split it into shot-aligned chunks (a jump cut resets tracking anyway),
    # one recognizer per chunk, consumed by worker threads while this thread runs the face detector.
    k = workers if new_gesture and n_total > 150 else 1
    edges = [0]
    for j in range(1, k):
        edges.append(min(cut_frames + [n_total], key=lambda c: abs(c - j * n_total / k)) if cut_frames else j * n_total // k)
    edges = sorted(set(edges)) + [n_total]
    import queue, threading
    queues = [queue.Queue(maxsize=64) for _ in range(len(edges) - 1)]
    found = [dict() for _ in queues]
    errors = []

    def work(q, out, gest):
        try:
            while True:
                item = q.get()
                if item is None:
                    return
                i, rgb = item
                out[i] = gest(rgb, i, fps)
        except Exception as e:
            errors.append(e)
            while q.get() is not None:  # keep draining so the producer never blocks
                pass
    threads = []
    if new_gesture:
        for q, out in zip(queues, found):
            th = threading.Thread(target=work, args=(q, out, new_gesture()), daemon=True)  # built here: init is not thread-safe
            th.start()
            threads.append(th)
    gen = _frames(video, TW)
    boxes = []
    i = 0
    try:
        while True:
            try:
                rgb = next(gen)
            except StopIteration as stop_:
                sw, sh = stop_.value
                break
            if stop is not None and stop.is_set():
                raise InterruptedError
            boxes.append(face(rgb, i, fps))
            if new_gesture and i % GESTURE_EVERY == 0:
                queues[max(j for j, e in enumerate(edges[:-1]) if e <= i)].put((i, rgb))
            i += 1
    finally:
        for q in queues:
            q.put(None)
        for th in threads:
            th.join()
    if errors:
        raise errors[0]
    gestures, last_seen = [], {}
    for i, g in sorted(kv for out in found for kv in out.items()):
        if g:  # sampled every 3rd frame: only a gap > 0.5 s starts a new event
            if i - last_seen.get(g, -10**9) > 0.5 * fps:
                gestures.append({"t": round(i / fps, 3), "name": g})
            last_seen[g] = i
    n = len(boxes)
    have = [k for k, b in enumerate(boxes) if b]
    if not have:
        return {"fps": fps, "w": sw, "h": sh, "boxes": [[0.5, 0.4, 0.4, 0.22]] * n, "detected": 0,
                "gestures": gestures, "detector": name}
    arr = np.array([b if b else [np.nan] * 4 for b in boxes], np.float32)
    starts = [0] + list(cut_frames) + [n]
    for a, b in zip(starts[:-1], starts[1:]):  # fill misses and smooth inside each shot only
        seg = arr[a:b]
        idx = np.arange(len(seg))
        for k in range(4):
            ok = ~np.isnan(seg[:, k])
            seg[:, k] = np.interp(idx, idx[ok], seg[ok, k]) if ok.any() else np.interp(a + idx, have, arr[have, k])
            f = OneEuro(fps, min_cutoff=0.8 if k < 2 else 0.4, beta=8.0 if k < 2 else 4.0)
            seg[:, k] = [f.filter(float(v), j / fps) for j, v in enumerate(seg[:, k])]
        arr[a:b] = seg
    return {"fps": fps, "w": sw, "h": sh, "boxes": np.round(arr, 4).tolist(), "detected": len(have),
            "gestures": gestures, "detector": name}


def emphasis_loud(db, thr):
    """Loudness peaks on the SOURCE timeline: >= 6 dB over the median of the voiced frames in the trailing 1 s
    (window itself >= 60 % voiced, so a post-pause onset never counts), in the clip's top 15 % of voiced
    frames, held 150 ms, not before 0.3 s."""
    voiced = db > thr
    if voiced.sum() < 100:
        return []
    p85 = np.percentile(db[voiced], 85)
    ev, run = [], 0
    for i in range(30, len(db)):
        w, vw = db[max(0, i - 100):i], voiced[max(0, i - 100):i]
        run = run + 1 if (vw.mean() >= 0.6 and db[i] >= p85 and db[i] - np.median(w[vw]) >= 6) else 0
        if run == 15:
            ev.append({"t": round((i - 14) / 100, 2), "kind": "loud", "z": 1.10})
    return ev


def emphasis(loud, gestures, min_gap=2.5):
    """Merge loud events with gestures (both on the CUT timeline); on a collision within `min_gap` keep the larger z."""
    ev = sorted(loud + [{"t": g["t"], "kind": "gesture", "z": 1.14 if g["name"] == "point" else 1.08}
                        for g in gestures], key=lambda e: e["t"])
    out = []
    for e in ev:
        if out and e["t"] - out[-1]["t"] < min_gap:
            if e["z"] > out[-1]["z"]:
                out[-1] = e
        else:
            out.append(e)
    return out
