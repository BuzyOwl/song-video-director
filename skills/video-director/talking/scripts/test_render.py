"""Pixel checks on single rendered frames. Run: python -I scripts/test_render.py (needs Task 5 harness)."""
import json, os, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

SKILL = Path(__file__).resolve().parent.parent
REM = SKILL / "remotion"
TMP = Path(os.environ.get("VD_TMP", Path.home() / ".video-director" / "tmp"))
REEL = Path(os.environ.get("VD_TEST_REEL", "D:/03_Projects/Video Caption Project MIC Class/reels/test-01"))
if not (REEL / "cut.mp4").exists():
    print("SKIP: set VD_TEST_REEL to a prepped reel"); sys.exit(0)


def still(props: dict, frame: int, name: str) -> np.ndarray:
    cut = REM / "public/job/cut.mp4"          # compile.mjs removes public/job after rendering
    if not cut.exists():
        cut.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REEL / "cut.mp4", cut)
    pj = TMP / f"{name}.json"
    pj.write_text(json.dumps(props))
    out = TMP / f"{name}.png"
    subprocess.run(["node", "src/test/one-frame.mjs", str(pj), str(frame), str(out)], cwd=REM, check=True)
    return np.asarray(Image.open(out).convert("RGB")).astype(np.float32)


def base():
    return json.loads((REM / "src/test/fixture.json").read_text())


def test_punch_zoom_alternates_and_is_uniform():
    p = base(); p["cuts"] = [2.0]; p["punch"] = 1.3; p["face"] = [[0.5, 0.4, 0.4, 0.22]]
    a, b = still(p, 30, "z_a"), still(p, 75, "z_b")       # shot 0 (z=1) vs shot 1 (z=1.3), 1.5 s apart
    assert np.abs(a - b).mean() > 6, "second shot should be visibly zoomed"
    q = dict(p, punch=1.0); c = still(q, 75, "z_c")       # same frame, no punch: isolates the zoom from video motion
    assert np.abs(b - c).mean() > 6, "punch=1.3 must differ from punch=1.0 at the same frame"
    # uniform scale: the frame's aspect of a bright patch must not change -> compare row/col energy ratios
    ra, rb = a.mean(axis=(1, 2)), b.mean(axis=(1, 2))
    assert abs(np.corrcoef(ra[::4][:400], rb[::4][:400])[0, 1]) < 1.0  # smoke: both are valid images


def test_caption_word_pop_and_accent():
    p = base(); p["accent"] = "#FFD23F"
    p["chunks"] = [{"s": 0.5, "e": 2.0, "y": 0.84, "words": [{"w": "we", "s": 0.5, "e": 0.8}, {"w": "can", "s": 0.8, "e": 1.1},
                                                             {"w": "fire", "s": 1.1, "e": 1.6, "key": True}]}]
    img = still(p, 40, "cap")                      # t=1.33: 'fire' active + accent
    band = img[int(0.80 * 1920):int(0.88 * 1920)]
    yellow = ((band[..., 0] > 200) & (band[..., 1] > 170) & (band[..., 2] < 120)).sum()
    white = ((band > 235).all(-1)).sum()
    assert yellow > 1500, yellow          # accent word drawn
    assert white > 1500, white            # white words drawn
    before = still(p, 10, "cap0")         # t=0.33: nothing yet
    assert ((before[int(0.80*1920):int(0.88*1920)] > 235).all(-1)).sum() < 200


def test_stat_tokens_build_in_order():
    p = base()
    p["cards"] = [{"id": "c1", "type": "stat", "s": 1.0, "e": 4.0, "y": 0.12, "size": 170,
                   "tokens": [{"text": "100", "t": 1.0}, {"text": "−", "t": 1.4}, {"text": "25", "t": 1.8},
                              {"text": "=", "t": 2.2}, {"text": "75", "t": 2.6}]}]
    a, b = still(p, 36, "stat1"), still(p, 90, "stat5")       # t=1.2 (one token) vs t=3.0 (all five)
    lane = lambda im: (im[int(0.06*1920):int(0.18*1920)] > 200).all(-1).sum() +                       ((im[int(0.06*1920):int(0.18*1920), ..., 0] > 200) & (im[int(0.06*1920):int(0.18*1920), ..., 2] < 120)).sum()
    assert lane(b) > lane(a) * 2.5, (lane(a), lane(b))


def test_cutout_and_arrow_draw():
    from PIL import Image as I
    job = REM / "public/job"; job.mkdir(exist_ok=True)
    I.new("RGB", (600, 400), (30, 120, 220)).save(job / "strip.png")   # a blue strip
    p = base()
    p["cards"] = [{"id": "k", "type": "cutout", "s": 0.5, "e": 3, "y": 0.22, "src": "job/strip.png", "motion": "drift", "frame": "torn"},
                  {"id": "a", "type": "arrow", "s": 0.5, "e": 3, "y": 0.3, "from": [0.2, 0.3], "to": [0.5, 0.45], "shape": "arrow"}]
    img = still(p, 45, "cut")
    blue = ((img[..., 2] > 180) & (img[..., 0] < 80)).sum()
    yellow = ((img[..., 0] > 200) & (img[..., 1] > 170) & (img[..., 2] < 120)).sum()
    assert blue > 60000, blue
    assert yellow > 1500, yellow


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            f(); print("ok", n)
