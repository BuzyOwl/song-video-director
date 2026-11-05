"""make_sfx.py - write the six synthesized one-shots used by the Remotion renderer (deterministic)."""
import sys, wave
from pathlib import Path
import numpy as np

SR = 48000
OUT = Path(__file__).resolve().parent.parent / "remotion" / "public" / "sfx"


def tt(d):
    return np.arange(int(d * SR)) / SR


def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, "same")


def sounds():
    rng = np.random.default_rng(3)
    pop = np.sin(2 * np.pi * np.cumsum(900 * np.exp(-tt(0.09) * 25) + 250) / SR) * np.exp(-tt(0.09) * 45)
    f = 110 * np.exp(-tt(0.6) * 8) + 45
    hit = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt(0.6) * 7) + rng.standard_normal(len(f)) * np.exp(-tt(0.6) * 120) * 0.4
    wn = rng.standard_normal(int(0.5 * SR))
    whoosh = (lowpass(wn, 24) - lowpass(wn, 220)) * np.sin(np.pi * np.linspace(0, 1, len(wn))) ** 2 * 3
    tick = rng.standard_normal(int(0.02 * SR)) * np.exp(-tt(0.02) * 300)
    riser = lowpass(rng.standard_normal(int(0.8 * SR)), 12) * np.linspace(0, 1, int(0.8 * SR)) ** 2 * 2
    ding = sum(a * np.sin(2 * np.pi * fr * tt(1.4)) * np.exp(-tt(1.4) * d) for fr, a, d in
               [(1318.5, 1.0, 3), (2637, 0.45, 5), (3955, 0.2, 8)])
    return {"pop": pop, "hit": hit, "whoosh": whoosh, "tick": tick, "riser": riser, "ding": ding}


def write(path, x, peak_db=-18.0):
    x = x / (np.abs(x).max() + 1e-9) * 10 ** (peak_db / 20)
    pcm = (np.repeat(x[:, None], 2, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, x in sounds().items():
        write(OUT / f"{name}.wav", x)
        print("wrote", name)


if __name__ == "__main__":
    sys.exit(main())
