"""prep.py - talking-head video -> filler-free cut + word times + face track.

    python prep.py <video> <workdir> [--drop 3,8-10] [--keep 5] [--cut 31.9-32.3] [--pause 0.18] [--lang en]
                   [--model auto] [--no-check]

Writes into <workdir>:
    src.mp4          CFR 30 fps copy of the input (rotation applied)
    words.raw.json   faster-whisper words, CTC-aligned times (wav2vec2 for en, MMS-1130 otherwise) on the SOURCE timeline
    cut.mp4          fillers, stutters and dead air removed
    words.json       kept words on the CUT timeline + jump-cut times
    track.json       per-frame face box on cut.mp4 (normalised cx, cy, w, h)
    cut.txt          paper edit: what was cut, the cut transcript, word indexes for --drop/--keep

Re-running is cheap: src.mp4 and words.raw.json are cached, only the cut and track redo.
"""
import argparse, difflib, hashlib, json, os, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I drops the script dir
from aligner import align_words, energy_db, session as aligner_session, voicing
from tracker import track, emphasis, emphasis_loud, TW

FPS = 30
HARD = {"uh", "uhh", "um", "umm", "uhm", "erm", "er", "ah", "ahh", "hmm", "hm", "mm", "mhm", "mmm",
        "hmmm", "aaa", "हम्म", "अं", "आं", "उम"}  # Hindi hesitations as Whisper spells them; "haan" (yes) / "aa" (come) are real words
SOFT = {"like", "basically", "actually", "literally", "so", "okay", "ok", "right", "well", "just",
        "matlab", "woh", "achha", "accha", "toh", "aise", "yaar", "haina", "haan", "मतलब", "वो", "अच्छा", "तो", "हाँ", "ऐसे", "यार", "बस"}
SOFT2 = {("you", "know"), ("i", "mean"), ("sort", "of"), ("kind", "of"), ("mera", "matlab"), ("kya", "bolte"),
         ("मेरा", "मतलब"), ("क्या", "बोलते")}
# Whisper drops disfluencies unless the prompt shows them; this keeps "uh"/"um" in the transcript.
# No "okay"/"so": the prompt biases toward its own words.
PROMPT = {"en": "Umm, uh, like, you know, I mean... uh, hmm.",
          "hi": "Umm, uh, matlab, woh, haan... hmm, achha, toh."}


def run(cmd):
    subprocess.run(cmd, check=True)


def norm(w):
    return re.sub(r"[^\w'ऀ-ॣ०-ॿ]", "", w.lower())


def parse_idx(s):
    out = set()
    for part in filter(None, (s or "").split(",")):
        a, _, b = part.partition("-")
        out.update(range(int(a), int(b or a) + 1))
    return out


_models = {}
_model_lock = threading.Lock()


def auto_model(lang):
    return "large-v3-turbo" if (lang or "en") == "en" else "large-v3"


def load_model(model_name):
    with _model_lock:  # prefetch thread and transcribe() may race
        if model_name not in _models:
            from faster_whisper import WhisperModel
            try:
                _models[model_name] = WhisperModel(model_name, device="cuda", compute_type="int8_float16")
            except Exception as e:  # no CUDA -> CPU still works, just slower
                print("cuda unavailable, using cpu:", e)
                _models[model_name] = WhisperModel(model_name, device="cpu", compute_type="int8")
    return _models[model_name]


def prefetch(model_name, lang, aligned):
    """Load Whisper (and the aligner session) in the background while ffmpeg cuts."""
    def go():
        try:
            load_model(model_name)
            if aligned:
                aligner_session(lang)
        except Exception:
            pass  # the real call reports it
    threading.Thread(target=go, daemon=True).start()


def transcribe(wav, lang, model_name="auto", align=True):
    """Whisper decides WHAT was said; the CTC aligner (aligner.py) then decides exactly WHEN (Whisper's own word edges
    drift 50-150 ms and stretch over pauses, which clips syllables or leaks fillers at the cut)."""
    if model_name == "auto":
        model_name = auto_model(lang)
    model = load_model(model_name)
    audio = np.fromfile(wav, np.int16).astype(np.float32) / 32768  # array in: skips PyAV decoding
    segs, info = model.transcribe(
        audio, language=lang, word_timestamps=True, initial_prompt=PROMPT["hi"] if lang == "hi" else PROMPT["en"],
        condition_on_previous_text=False, beam_size=5,
        vad_filter=True,  # Silero v6 (bundled): no words invented over silence
        vad_parameters=dict(min_silence_duration_ms=400, speech_pad_ms=250, threshold=0.4))
    words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)}
             for s in segs for w in (s.words or []) if w.word.strip()]
    aligned = False
    if words and align:
        try:
            words, aligned = align_words(words, audio, info.language), True
        except Exception as e:  # aligner missing/offline: Whisper times still work, just looser
            print("aligner unavailable, using Whisper word times:", e)
    return {"lang": info.language, "model": model_name, "aligned": aligned, "words": words}


def flag_words(words):
    flags = [""] * len(words)
    ns = [norm(w["w"]) for w in words]
    for i, n in enumerate(ns):
        if n in HARD:
            flags[i] = "filler"
        elif i + 1 < len(ns) and n and n == ns[i + 1]:
            flags[i] = "repeat"  # stutter: drop the first copy
        elif n in SOFT:
            flags[i] = "soft?"
        elif i + 1 < len(ns) and (n, ns[i + 1]) in SOFT2:
            flags[i] = flags[i + 1] = "soft?"
    return flags


def silences(med, thr, min_len=0.18):
    quiet = np.concatenate([[False], med < thr, [False]])
    edges = np.flatnonzero(np.diff(quiet.astype(np.int8)))
    return [(a / 100, b / 100) for a, b in zip(edges[::2], edges[1::2]) if (b - a) / 100 >= min_len]


def valley(t, db, lo=0.05, hi=0.05):
    """Nudge a cut onto the quietest 10 ms frame in [t-lo, t+hi]. Keep it small; a wide one jumps words."""
    i0, i1 = max(0, int(round((t - lo) * 100))), min(len(db), int(round((t + hi) * 100)) + 1)
    return (i0 + int(np.argmin(db[i0:i1]))) / 100 if i1 > i0 else t


def spans_from(words, cut_idx, db, med, thr, dur, pause, aligned, cuts=()):
    """Kept speech = runs of consecutive kept words (a removed word splits a run), padded a little but never past
    the midpoint to a removed neighbour; then every pause inside is squeezed to `pause` seconds."""
    kept = [w for w in words if w["i"] not in cut_idx]
    spans = []
    for w in kept:
        i = w["i"]
        lo, hi = max(0.0, w["s"] - 0.04), w["e"] + 0.06
        if i > 0 and i - 1 in cut_idx:
            lo = max(lo, (words[i - 1]["e"] + w["s"]) / 2)
        if i + 1 < len(words) and i + 1 in cut_idx:
            hi = min(hi, (w["e"] + words[i + 1]["s"]) / 2)
        if spans and spans[-1][2] == i - 1:
            spans[-1][1:] = [max(spans[-1][1], hi), i]
        else:
            spans.append([lo, hi, i])
    spans = [[a, b] for a, b, _ in spans]
    if not aligned:  # Whisper edges wobble ~50 ms: nudge onto the quietest nearby frame
        spans = [[valley(a, db), valley(b, db)] for a, b in spans]
    ends = [w["e"] for w in kept if w["w"][-1:] in ".?!"]
    holes = [(a + (0.22 if any(abs(e - a) < 0.3 for e in ends) else pause / 2), b - pause / 2)
             for a, b in silences(med, thr)] + list(cuts)  # breathe a little longer at sentence ends
    for ca, cb in holes:
        if cb - ca < 0.03:
            continue
        out = []
        for a, b in spans:
            if cb <= a or ca >= b:
                out.append([a, b])
                continue
            if ca > a:
                out.append([a, ca])
            if cb < b:
                out.append([cb, b])
        spans = out
    frames = []
    for a, b in sorted(spans):
        f0, f1 = round(a * FPS), round(min(b, dur) * FPS)
        if frames and f0 <= frames[-1][1]:
            frames[-1] = (frames[-1][0], max(frames[-1][1], f1))
        elif f1 - f0 >= 3:  # under 0.1 s is a noise sliver, not speech
            frames.append((f0, f1))
    return frames


def relisten(work, src, frames, key, expected, lang, model_name, aligned):
    """Second pass: re-transcribe the cut, diff against the words we meant to keep. Returns (report, fillers
    heard in the cut that the first pass missed). Whisper mishears too: a diff is a place to look, not proof.
    Heard words are cached by `key` (hash of the cut spans), so an identical cut is never re-transcribed or even
    re-encoded. The CTC aligner only runs when a filler was heard (its times place the pass-2 cut)."""
    cf = work / "relisten.json"
    cache = json.loads(cf.read_text()) if cf.exists() else {}
    now = time.time()
    # word-level timestamps are kept 30 days from creation; after that an entry goes once unused for 7 days
    cache = {k: v for k, v in cache.items() if now - v.get("made", now) < 30 * 86400 or now - v.get("used", now) < 7 * 86400}
    hit = cache.get(key)
    pcm_file = work / "cut.pcm"

    def pcm():
        data = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ensure_cut(src, frames, key, work)), "-ac", "1", "-ar", "16000",
                               "-f", "s16le", "-"], capture_output=True, check=True).stdout
        pcm_file.write_bytes(data)
        return pcm_file

    if hit is None:
        hit = {"aligned": False, "words": transcribe(pcm(), lang, model_name, align=False)["words"]}
    exp = [norm(w["w"]) for w in expected]

    def diff(heard):
        got = [norm(w["w"]) for w in heard]
        report, missed = [], []
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, exp, got, autojunk=False).get_opcodes():
            if op == "equal":
                continue
            t = heard[j1]["s"] if j1 < len(heard) else expected[i1]["s"]
            report.append(f"  @{t:.2f}s cut: expected {' '.join(exp[i1:i2]) or '-'} | heard {' '.join(got[j1:j2]) or '-'}")
            missed += [h for h in heard[j1:j2] if norm(h["w"]) in HARD]
        return report, missed

    report, missed = diff(hit["words"])
    if missed and aligned and not hit["aligned"] and hit["words"]:
        try:
            audio = np.fromfile(pcm(), np.int16).astype(np.float32) / 32768
            hit = {"aligned": True, "words": align_words(hit["words"], audio, lang)}
            report, missed = diff(hit["words"])
        except Exception as e:
            print("aligner unavailable, using Whisper word times:", e)
    cache[key] = dict(hit, made=hit.get("made", now), used=now)
    cf.write_text(json.dumps(cache))
    pcm_file.unlink(missing_ok=True)
    return report, missed


def peek_cached(work, key):
    cf = work / "relisten.json"
    return cf.exists() and key in json.loads(cf.read_text())


def ensure_cut(src, frames, key, work):
    """Path of the cut for `key`, encoded at most once. Each key gets its own file (cut.<key>.mp4) so a speculative
    track on pass 1's cut can't read a file pass 2 is rewriting; main() promotes the final one to cut.mp4."""
    kf, final = work / "cut.key", work / "cut.mp4"
    if kf.exists() and kf.read_text() == key and final.exists():
        return final
    path = work / f"cut.{key}.mp4"
    if not path.exists():
        part = work / f"cut.{key}.part.mp4"  # atomic: a killed run must not leave a half-written cut behind
        cut_video(src, frames, part, work)
        os.replace(part, path)
    return path


def cut_video(src, frames, out, work):
    parts, labels = [], []
    for i, (f0, f1) in enumerate(frames):
        d = (f1 - f0) / FPS
        parts.append(f"[0:v]trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS[v{i}];"
                     f"[0:a]atrim=start={f0 / FPS:.6f}:end={f1 / FPS:.6f},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d=0.008,afade=t=out:st={max(0, d - 0.008):.6f}:d=0.008[a{i}];")
        labels.append(f"[v{i}][a{i}]")
    graph = "".join(parts) + "".join(labels) + f"concat=n={len(frames)}:v=1:a=1[v][a]"
    gfile = work / "cut.filter"
    gfile.write_text(graph)
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-/filter_complex", str(gfile), "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "ultrafast", "-crf", "16", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", str(out)])
    gfile.unlink()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("work")
    ap.add_argument("--drop", default="", help="extra source word indexes to cut, e.g. 0,8-10")
    ap.add_argument("--keep", default="", help="word indexes to keep even if auto-flagged")
    ap.add_argument("--lang", default=None, help="whisper language code; pass hi for Hindi (picks large-v3 + Hindi prompt)")
    ap.add_argument("--cut", default="", help="extra SOURCE time ranges to remove, e.g. 31.9-32.3,40-41.5")
    ap.add_argument("--pause", type=float, default=0.18, help="every pause is squeezed to this many seconds")
    ap.add_argument("--no-check", action="store_true", help="skip the re-listen check (saves ~10 s)")
    ap.add_argument("--model", default="auto", help="auto = large-v3-turbo for en, large-v3 otherwise")
    a = ap.parse_args()
    if a.model == "auto":
        a.model = auto_model(a.lang)
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    src, wav, raw = work / "src.mp4", work / "src.wav", work / "words.raw.json"

    if not src.exists():
        run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-vf", f"fps={FPS}", "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(src)])
    if not wav.exists():
        run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-ac", "1", "-ar", "16000", "-f", "s16le", str(wav)])
    cached = json.loads(raw.read_text()) if raw.exists() else {}
    if cached.get("model", "large-v3") != a.model or "aligned" not in cached:
        cached = transcribe(wav, a.lang, a.model)
        raw.write_text(json.dumps(cached, indent=1))
    words, aligned = cached["words"], cached["aligned"]
    db = energy_db(np.fromfile(wav, np.int16).astype(np.float32) / 32768)
    dur = len(db) / 100
    med, thr = voicing(db)
    cuts = [tuple(map(float, r.split("-"))) for r in filter(None, a.cut.split(","))]

    flags = flag_words(words)
    drop, keep = parse_idx(a.drop), parse_idx(a.keep)
    kept, removed = [], []
    for i, w in enumerate(words):
        w["i"] = i
        cut = (flags[i] in ("filler", "repeat") or i in drop) and i not in keep
        (removed if cut else kept).append(w)
    lang = a.lang or json.loads(raw.read_text())["lang"]

    tf = work / "track.json"
    track_data = json.loads(tf.read_text()) if tf.exists() else {}
    pool, tfut, stop = ThreadPoolExecutor(1), None, threading.Event()
    ff = work / "fillers.json"  # fillers pass 2 found before, in SOURCE time: apply them up front so a re-cut with
    sig = hashlib.sha1(raw.read_bytes()).hexdigest()  # new args needs one pass, not two (valid while words.raw.json is)
    memo = json.loads(ff.read_text()) if ff.exists() else {}
    memo = memo["extras"] if memo.get("sig") == sig else []
    for w, s0, e0 in memo:
        cuts.append((s0, e0))
        removed.append({"w": w + " (pass 2)", "s": s0, "i": "-"})
    for attempt in range(2):  # pass 2 only if the re-listen hears fillers the first transcript missed
        cut_idx = {w["i"] for w in removed if w["i"] != "-"}
        frames = spans_from(words, cut_idx, db, med, thr, dur, a.pause, aligned, cuts)
        key = hashlib.sha1(json.dumps([frames, a.model, lang, TW]).encode()).hexdigest()[:16]
        out_start = np.cumsum([0] + [f1 - f0 for f0, f1 in frames]).tolist()
        total_f = out_start.pop()

        def to_cut(t):
            f = t * FPS
            for (f0, f1), o in zip(frames, out_start):
                if f < f1:
                    return round((o + max(f - f0, 0)) / FPS, 3)
            return round(total_f / FPS, 3)

        def to_src(t):
            f = t * FPS
            k = max(j for j, o in enumerate(out_start) if o <= f)
            return (frames[k][0] + f - out_start[k]) / FPS

        cut_words = [{"w": w["w"], "s": to_cut(w["s"]), "e": to_cut(w["e"]), "i": w["i"]} for w in kept]
        cut_words = [w for w in cut_words if w["e"] > w["s"]]  # a word that fell wholly inside a cut pause
        if not a.no_check and attempt == 0 and not peek_cached(work, key):
            prefetch(a.model, lang, aligned)  # model loads while ffmpeg cuts
        if tfut:  # pass 2 changed the cut: the speculative track is for a cut we are discarding
            stop.set()
        tfut, stop = None, threading.Event()
        if track_data.get("key") != key:  # face track of this cut runs alongside the re-listen (CPU vs GPU)
            tfut = pool.submit(track, ensure_cut(src, frames, key, work), out_start[1:], FPS, stop)
        if a.no_check:
            report = []
            break
        report, missed = relisten(work, src, frames, key, cut_words, lang, a.model, aligned)
        if not missed or attempt:
            break
        extra = [(to_src(m["s"]) - 0.02, to_src(m["e"]) + 0.02) if aligned else
                 (valley(to_src(m["s"]), db), valley(to_src(m["e"]), db)) for m in missed]
        print("pass 2: cutting fillers heard in the cut:", ", ".join(f"{m['w']}@src {s:.2f}-{e:.2f}"
                                                                     for m, (s, e) in zip(missed, extra)))
        cuts += extra
        removed += [{"w": m["w"] + " (pass 2)", "s": s, "i": "-"} for m, (s, _) in zip(missed, extra)]
        memo += [[m["w"], s, e] for m, (s, e) in zip(missed, extra)]
        ff.write_text(json.dumps({"sig": sig, "extras": memo}))

    # Whisper-free clip check: every voiced 10 ms frame of a kept word should survive the cut
    keep_mask = np.zeros(len(med), bool)
    for f0, f1 in frames:
        keep_mask[int(f0 / FPS * 100):int(f1 / FPS * 100)] = True
    clipped = []
    for w in kept:
        i0, i1 = int(w["s"] * 100), int(w["e"] * 100)
        voiced = med[i0:i1] > thr
        if voiced.sum() >= 3 and (keep_mask[i0:i1] & voiced).sum() / voiced.sum() < 0.85:
            clipped.append(f"{w['w']}@{to_cut(w['s']):.2f}s ({(keep_mask[i0:i1] & voiced).sum() / voiced.sum():.0%} kept)")

    cut_frames = out_start[1:]
    total = total_f / FPS
    if tfut:  # same spans -> same cut -> same face track, so an identical re-run skips all of this
        track_data = dict(tfut.result(), key=key)
        tf.write_text(json.dumps(track_data))
    path = ensure_cut(src, frames, key, work)
    if path.name != "cut.mp4":
        os.replace(path, work / "cut.mp4")
    (work / "cut.key").write_text(key)
    for old in [*work.glob("cut.*.mp4"), *work.glob("cut.*.part.mp4")]:  # superseded pass-1 cut
        old.unlink(missing_ok=True)
    emph = emphasis([dict(e, t=to_cut(e["t"])) for e in emphasis_loud(db, thr)], track_data["gestures"])
    (work / "words.json").write_text(json.dumps(
        {"fps": FPS, "dur": round(total, 3), "cuts": [round(f / FPS, 3) for f in cut_frames], "spans": frames,
         "words": cut_words, "emphasis": emph}, indent=1))

    lines = [f"CUT {dur:.1f}s -> {total:.1f}s  ({len(frames) - 1} jump cuts, {len(removed)} removed, "
             f"face found in {track_data['detected']}/{len(track_data['boxes'])} frames, "
             f"gestures {len(track_data['gestures'])}, detector {track_data['detector']})", "", "REMOVED:"]
    lines += [f"  #{w['i']} {w['w']!r} @{w['s']:.2f}s ({flags[w['i']] if w['i'] != '-' else 'relisten'})"
              for w in removed] or ["  (none)"]
    lines += ["", "CUT TRANSCRIPT (cut-timeline seconds):"]
    row = []
    for k, w in enumerate(cut_words):
        row.append(w)
        if w["w"][-1:] in ".?!" or len(row) == 10 or k == len(cut_words) - 1:
            lines.append(f"  [{row[0]['s']:6.2f}] " + " ".join(x["w"] for x in row))
            row = []
    lines += ["", "CLIP CHECK (voiced frames of kept words that the cut removed):"]
    lines += ["  " + c for c in clipped] or ["  none clipped"]
    if not a.no_check:
        lines += ["", "RE-LISTEN (Whisper on cut.mp4 vs intended words; it mishears too, so look before re-cutting):"]
        lines += report or ["  all heard"]
    lines += ["", "SOURCE WORDS (index word @source_s flag) - use with --drop / --keep:"]
    lines += ["  " + "  ".join(f"{w['i']}:{w['w']}@{w['s']:.2f}{'[' + flags[w['i']] + ']' if flags[w['i']] else ''}"
                               for w in words[j:j + 8]) for j in range(0, len(words), 8)]
    report = "\n".join(lines)
    (work / "cut.txt").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    sys.exit(main())
