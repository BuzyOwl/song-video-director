"""python -I test_prep.py  - fast checks for the cut logic (no models, no video)."""
import json, os, sys, tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prep
import aligner

EN = {c: i for i, c in enumerate("|ETAONIHSRDLUMWCFGYPBVKJXQZ'")}  # wav2vec2 style (upper)

# numbers are spelled for the English aligner
assert aligner.letters("75", EN, "en") == "SEVENTYFIVE" and aligner.letters("100,", EN, "en") == "ONEHUNDRED" and aligner.letters("it's", EN, "en") == "IT'S"

# CTC Viterbi: letters spiking at known frames come back at those frames, repeats need a blank between
V, blank = 5, 0
lp = np.full((12, V), -9.0, np.float32)
lp[:, blank] = -0.1
for frame, tok in [(2, 1), (5, 2), (7, 2), (10, 3)]:
    lp[frame, tok], lp[frame, blank] = -0.1, -9.0
assert aligner.ctc_path(lp, [1, 2, 2, 3], blank) == [(2, 2), (5, 5), (7, 7), (10, 10)], aligner.ctc_path(lp, [1, 2, 2, 3], blank)

# spans: a removed filler splits the run and the cut stops at the midpoint between the words
words = [{"w": "so", "s": 0.0, "e": 0.4, "i": 0}, {"w": "uh", "s": 0.6, "e": 0.9, "i": 1},
         {"w": "yes.", "s": 1.0, "e": 1.4, "i": 2}]
db = np.full(200, -20.0)
frames = prep.spans_from(words, {1}, db, db, -40.0, 2.0, 0.18, aligned=True)
assert frames == [(0, 14), (29, 44)], frames  # pad stops at 0.46s; restarts at midpoint (0.9+1.0)/2=0.95s

# Devanagari fillers: norm keeps matras/virama, Hindi lists match
assert prep.norm("मतलब,") == "मतलब" and prep.norm("क्या") == "क्या"
assert prep.flag_words([{"w": x} for x in ["मतलब,", "हम्म", "ठीक", "ठीक", "है"]]) == ["soft?", "filler", "repeat", "", ""]

# Silero VAD gate: speech + 6 s of silence -> Whisper must not hallucinate words after the speech ends
REEL = Path(os.environ.get("VD_TEST_REEL", "D:/03_Projects/Video Caption Project MIC Class/reels/test-01"))
if not (REEL / "src.wav").exists():
    print("pure checks ok; SKIP fixture checks (set VD_TEST_REEL to a prepped reel)"); sys.exit(0)
src = REEL / "src.wav"
a = np.fromfile(src, np.int16)[: 16000 * 8]  # first 8 s of real speech
with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "t.pcm"
    np.concatenate([a, np.zeros(16000 * 6, np.int16)]).tofile(p)
    r = prep.transcribe(p, "en", "large-v3-turbo")
late = [w for w in r["words"] if w["s"] > 8.6]
assert not late, f"hallucinated words in silence: {late}"
assert len(r["words"]) > 10
# letters(): English upper-case vocab vs MMS lower-case vocab, Devanagari romanised by uroman
assert aligner.letters("75%", EN, "en") == "SEVENTYFIVEPERCENT"
mms_vocab = {c: i for i, c in enumerate("abcdefghijklmnopqrstuvwxyz'")}  # MMS style (lower)
assert aligner.letters("Fire", mms_vocab, "hi") == "fire"
r = aligner.letters("नमस्ते", mms_vocab, "hi")
assert r and r.isalpha() and r.islower(), r  # romanised by uroman, e.g. 'namaste'

# MMS aligner on the English benchmark must agree with the wav2vec2-aligned times (raw 's') within 0.25 s on >85%
# of words (measured 70/78; misses are 'uh' fillers and 1-letter words). Vs raw Whisper times even wav2vec2 only reaches 66/78.
raw = json.loads((REEL / "words.raw.json").read_text())
audio = np.fromfile(REEL / "src.wav", np.int16).astype(np.float32) / 32768
words = [{"w": w["w"], "s": w.get("ws", w["s"]), "e": w.get("we", w["e"]), "p": w["p"]} for w in raw["words"]]
out = aligner.align_words(words, audio, "hi")  # force the MMS model on English audio
close = sum(abs(o["s"] - r["s"]) < 0.25 for o, r in zip(out, raw["words"]))
assert close / len(words) > 0.85, f"{close}/{len(words)} within 0.25 s"

# tracker: One-Euro damps jitter but follows a real move
import tracker
f = tracker.OneEuro(30, min_cutoff=1.0, beta=0.02)
rng = np.random.default_rng(0)
still = [f.filter(0.5 + rng.normal(0, 0.01), i / 30) for i in range(60)]
assert np.std(still[30:]) < 0.004, np.std(still[30:])          # jitter damped
moved = [f.filter(0.8, (60 + i) / 30) for i in range(15)]
assert abs(moved[-1] - 0.8) < 0.03, moved[-1]                  # a real move is followed within 0.5 s

# tracker on the benchmark cut: steady face box, he points at ~25 s (cut timeline)
t = tracker.track(REEL / "cut.mp4", [], 30)
assert t["detector"] in ("mediapipe", "yunet")
assert t["detected"] / len(t["boxes"]) > 0.95, t["detected"]
cx = np.array([b[0] for b in t["boxes"]])
assert np.abs(np.diff(cx)).max() < 0.08, "box jumps between frames"
assert any(g["name"] == "point" for g in t["gestures"]) or t["detector"] == "yunet"  # he points at ~25 s (cut timeline)

# emphasis: a 200 ms shout over a voiced floor becomes one loud event
db = np.full(1000, -30.0); db[500:520] = -15.0   # 200 ms shout at 5.0 s
ev = tracker.emphasis(tracker.emphasis_loud(db, -40), [])
assert len(ev) == 1 and abs(ev[0]["t"] - 5.0) < 0.1 and ev[0]["kind"] == "loud", ev
# a louder onset right after a pause is not emphasis
db = np.concatenate([np.full(300, -30.0), np.full(150, -60.0), np.full(300, -22.0)])
assert tracker.emphasis_loud(db, -40) == []
# collision keeps the larger z
assert tracker.emphasis([{"t": 5.0, "kind": "loud", "z": 1.10}], [{"t": 6.0, "name": "point"}]) == \
    [{"t": 6.0, "kind": "gesture", "z": 1.14}]

print("prep checks ok")
