"""Song facts for a code-rendered music video: per-frame energy and onset, tempo + beat grid,
and (optionally) Whisper word timestamps. One JSON file that every scene, effect and lyric reads from.

Usage:
  python song_facts.py --audio song.mp3 --out data/song_facts.json [--fps 24] [--bpm-range 60,180]
                       [--whisper] [--language en] [--prompt "first lyric lines"] [--limit SECONDS]
  python song_facts.py --selftest          # synthetic 120 BPM click track must come back as ~120 BPM

Output JSON:
  fps, duration        frames per second used for the arrays; song length in seconds
  rms[], on[]          per-frame loudness and onset strength, 0..1 (smoothed, 98th-percentile normalised)
  bpm, beat_conf       machine tempo estimate; on-beat / off-beat onset ratio (>1.3 is a confident grid)
  beats[]              DP beat tracker grid in seconds (follows local timing, so it cannot drift)
  words[]              only with --whisper: {w, s, e, p} = word, start ms, end ms, confidence 0..1

Everything here is measured or machine-estimated. The beat grid can land on half or double the
felt tempo (both alternatives are printed), and word times are a proposal, never ear-verified:
say "machine-aligned, not checked by ear" in every deliverable that uses them.

Lineage: energy.py + tempo.py + align.py transcribe() from Basement Goldfish, parametrised so a
new song needs no code changes. The fuzzy match of Whisper words onto canonical lyric lines stays
project-specific (lyric line/lane structure differs per film); see references/lessons.md §3c.
"""
import argparse, json, subprocess, sys
import numpy as np


def decode(audio, sr, limit=None):
    """Mono float32 PCM via ffmpeg (handles mp3/wav/m4a/mp4 alike)."""
    cmd = ['ffmpeg', '-v', 'error', '-i', audio]
    if limit: cmd += ['-t', str(limit)]
    cmd += ['-map', '0:a', '-ac', '1', '-ar', str(sr), '-f', 's16le', '-']
    pcm = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768


def energy(x, sr, fps):
    """Per-frame smoothed loudness and low/mid onset strength, each normalised to 0..1."""
    # frame i starts at the exact sample round(i*sr/fps): an integer hop (sr//fps) drifts ~0.2 s over a 3-4 min song
    n = int(np.ceil(len(x) * fps / sr)); starts = np.round(np.arange(n) * sr / fps).astype(int)
    x = np.pad(x, (0, starts[-1] + 2048 - len(x) + 1))
    win = np.hanning(2048); frames = np.stack([x[s:s + 2048] * win for s in starts])
    spec = np.abs(np.fft.rfft(frames, axis=1))
    rms = np.sqrt((frames ** 2).mean(1)); rms = np.convolve(rms, np.ones(9) / 9, 'same')
    flux = np.maximum(0, np.diff(np.log1p(spec[:, 1:120]), axis=0, prepend=0)).sum(1)
    flux = flux - np.convolve(flux, np.ones(fps) / fps, 'same'); flux = np.maximum(flux, 0)
    norm = lambda v: np.clip(v / (np.percentile(v, 98) + 1e-9), 0, 1)
    return norm(rms), norm(flux)


def tempo(x, sr, bpm_lo, bpm_hi):
    """Onset autocorrelation -> fine BPM/phase search -> Ellis-style DP beat tracker."""
    hop = 256; n = (len(x) - 1024) // hop; win = np.hanning(1024)
    S = np.abs(np.fft.rfft(np.stack([x[i * hop:i * hop + 1024] * win for i in range(n)]), axis=1))
    on = np.maximum(0, np.diff(np.log1p(S[:, :200]), axis=0, prepend=0)).sum(1)
    on = on - np.convolve(on, np.ones(32) / 32, 'same'); on = np.maximum(on, 0)
    fr = sr / hop
    ac = np.correlate(on, on, 'full')[len(on) - 1:]
    lags = np.arange(len(ac)) / fr; bpm_axis = 60 / np.maximum(lags, 1e-9)
    m = (bpm_axis > bpm_lo) & (bpm_axis < bpm_hi)
    w = np.exp(-.5 * (np.log2(bpm_axis / 110) / .9) ** 2)      # gentle prior around 110 BPM
    k = np.argmax(ac * m * w); bpm = 60 / (k / fr)
    best = (0, bpm, 0)                                           # refine: fine BPM + phase search
    for b in np.arange(bpm - 2, bpm + 2, .02):
        per = 60 / b * fr
        for ph in np.arange(0, per, .5):
            idx = (ph + per * np.arange(int((n - ph) / per))).astype(int)
            sc = on[idx].sum()
            if sc > best[0]: best = (sc, b, ph)
    _, bpm, ph = best
    per = 60 / bpm
    P = per * fr; onn = on / (on.std() + 1e-9); score = onn.copy(); back = -np.ones(n, int)
    lo, hi = int(P * .8), int(P * 1.25)
    for i in range(hi, n):
        prev = np.arange(i - hi, i - lo)
        pen = -400 * (np.log((i - prev) / P)) ** 2
        j = np.argmax(score[prev] + pen); score[i] = onn[i] + score[prev][j] + pen[j]; back[i] = prev[j]
    i = int(np.argmax(score[-hi:])) + n - hi; path = []
    while i >= 0: path.append(i); i = back[i]
    beats = [round(k / fr, 4) for k in reversed(path)]
    idx = lambda off: np.array([int((b + off * per) * fr) for b in beats if (b + off * per) * fr < n - 1])
    conf = on[idx(0)].mean() / (on[idx(.5)].mean() + 1e-9)
    return round(float(bpm), 3), round(float(conf), 2), beats


def whisper_words(audio, language, prompt, limit=None):
    """faster-whisper large-v3 word timestamps with confidence. GPU if available, else CPU int8."""
    from faster_whisper import WhisperModel
    x = decode(audio, 16000, limit)
    try:
        m = WhisperModel('large-v3', device='cuda', compute_type='int8_float16')
    except Exception as e:
        print(f'GPU unavailable ({e.__class__.__name__}); using CPU', file=sys.stderr)
        m = WhisperModel('large-v3', device='cpu', compute_type='int8')
    segs, _ = m.transcribe(x, language=language, word_timestamps=True, initial_prompt=prompt or None,
                           vad_filter=False, condition_on_previous_text=False, beam_size=5)
    words = []
    for s in segs:
        for w in s.words:
            words.append({'w': w.word.strip(), 's': round(w.start * 1000), 'e': round(w.end * 1000), 'p': round(w.probability, 3)})
        print(f'{s.start:7.2f} {s.text}', flush=True)
    return words


def selftest():
    sr = 22050; t = np.arange(20 * sr) / sr
    clicks = np.zeros_like(t)
    for b in np.arange(0, 20, 0.5): clicks[int(b * sr):int(b * sr) + 300] = np.hanning(300) * np.sin(2 * np.pi * 1000 * t[:300])
    bpm, conf, beats = tempo(clicks.astype(np.float32), sr, 60, 180)
    assert abs(bpm - 120) < 1, f'expected ~120 BPM, got {bpm}'
    assert conf > 1.3 and len(beats) > 30, f'weak grid: conf={conf} beats={len(beats)}'
    rms, on = energy(clicks.astype(np.float32), sr, 24)
    assert len(rms) == len(on) == 480, len(rms)            # 20 s * 24 fps exactly: no hop drift
    k = int(10.5 * 24)                                    # a click at 10.5 s: peak within one frame (causal 93 ms window), silence midway
    assert on[k - 1:k + 2].max() > 0.5 and on[k + 5:k + 8].max() < 0.2, f'onset must sit on the click: {on[k-1:k+8].round(2)}'
    print(f'selftest ok: {bpm} BPM, conf {conf}, {len(beats)} beats, {len(rms)} frames')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--audio'); ap.add_argument('--out'); ap.add_argument('--fps', type=int, default=24)
    ap.add_argument('--bpm-range', default='60,180'); ap.add_argument('--limit', type=float, help='analyse only the first N seconds (quick checks)')
    ap.add_argument('--whisper', action='store_true'); ap.add_argument('--language', default='en'); ap.add_argument('--prompt', default='', help='first lyric lines; steers spelling')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest: return selftest()
    if not (a.audio and a.out): ap.error('--audio and --out are required')
    sr = 22050; x = decode(a.audio, sr, a.limit)
    rms, on = energy(x, sr, a.fps)
    lo, hi = map(float, a.bpm_range.split(','))
    bpm, conf, beats = tempo(x, sr, lo, hi)
    out = {'audio': a.audio, 'fps': a.fps, 'duration': round(len(x) / sr, 3),
           'rms': [round(float(v), 3) for v in rms], 'on': [round(float(v), 3) for v in on],
           'bpm': bpm, 'beat_conf': conf, 'beats': beats,
           'note': 'machine-measured; bpm may be half/double the felt tempo; word times (if any) are not ear-verified'}
    if a.whisper: out['words'] = whisper_words(a.audio, a.language, a.prompt, a.limit)
    json.dump(out, open(a.out, 'w'), separators=(',', ':'))
    print(f'{a.out}: {len(rms)} frames @ {a.fps} fps, {out["duration"]} s | bpm {bpm} (half {bpm/2:.1f}, double {bpm*2:.1f}) '
          f'conf {conf} beats {len(beats)} | bar at 4/4 = {240/bpm:.3f} s' + (f' | {len(out["words"])} words' if a.whisper else ''))


if __name__ == '__main__':
    main()
