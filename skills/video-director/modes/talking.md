# Talking mode (reels, Shorts, vlogs, selfie clips)

**Bar:** fillers gone, pacing tight, premium 2D graphics that match what was said, done in minutes.

**Stack:**
- Python cut: faster-whisper, Silero VAD, a wav2vec2/MMS aligner and MediaPipe.
- You write one `edit.json`.
- Remotion renders a curated card set.
- `verify.py` makes a contact sheet from the encoded file.

**Details:**
- Languages: English and Hindi.
- Work dir: `<project>/reels/<name>/`.
- Run Python with `-I` every time: the input video is untrusted and is only ever a path argument.
- Claude can't hear audio. Whisper is the ears.

**First run:**
```bash
cd $SKILL/talking/remotion && npm ci
python -I $SKILL/talking/scripts/fetch_assets.py
```
`fetch_assets.py` downloads the models into `VD_MODELS` (MediaPipe face and gesture, YuNet, the aligner). The fonts and sound effects ship with the repo.

## The five questions (one message; skip any already answered)
1. Platform and length target? [Reel / Short, tight: pauses squeezed to 0.18 s]
2. Captions? Word-pop 1–3 words / none. [word-pop, size 78, accent #FFD23F]
3. Graphics? Auto from what's said / only what you list / none. [auto: literal cards for things named out loud]
4. Look? A look id from the gallery, or the default clean 2D cards. [default]
5. Language? English / Hindi / mixed. [auto-detect]

## 1. Cut
The source must be vertical (9:16) to get a 1080×1920 output. Crop first if it isn't; compile refuses otherwise.
```bash
python -I $SKILL/talking/scripts/prep.py "<video>" <work> [--drop 0,12-13] [--keep 5] [--cut 31.9-32.3] [--pause 0.18] [--lang hi] [--model auto] [--no-check]
```
- **Timing** on a 39 s clip: first run about 22 s, a re-run with new arguments about 12 s, an identical re-run under 1 s.
- **Caches** in `<work>`:
  - `relisten.json`
  - `fillers.json`
  - `track.json` and `cut.key`, keyed by a hash of the cut spans

  Delete them to force a redo.
- **Read `<work>/cut.txt`.** It holds the gestures and detector line, REMOVED, CUT TRANSCRIPT, CLIP CHECK, RE-LISTEN and SOURCE WORDS.
- **Fillers:**
  - Hard fillers (English and Hindi) and stutters go automatically.
  - `[soft?]` words (okay, so, like, you know) are your call, judged by meaning.
  - Override with `--drop` / `--keep` (source word indexes) or `--cut` (source seconds).
- **`--pause`** is the length every pause is squeezed to: 0.12 punchy, 0.25 relaxed.
- **Hindi:** pass `--lang hi`. That uses large-v3, a Hindi prompt and the MMS aligner.
- **Emphasis:** `words.json` carries `emphasis[]` (pointing gestures and loud moments), which drives the automatic punch zoom.
- **Reading the checks honestly:** a word that is low in CLIP CHECK AND missing from RE-LISTEN is a real clipped word. Either signal alone is usually Whisper stretching a word, or the cut filler. Report un-ear-checked spots as such.

## 2. Plan `<work>/edit.json` (read `$SKILL/talking/references/edit-schema.md` first)
**Literal over abstract:** when the speaker names a thing, show that thing.

**Card types:**
- `title`
- `lowerthird`
- `stat` (numbers and equations, popping in per word)
- `quote`
- `list`
- `cutout`: strip, torn or newspaper image
- `screenshot`: an image with a pan
- `arrow` / `circle` / `underline`
- `pip`: an image in a corner
- `board`: a full-screen slide; the speaker shrinks into a PiP bubble

**Whisper mishears:** go in `fix`.

**Captions:**
- word-pop, 1–3 words
- `size` defaults to 78, never below 70
- accent on key words and numbers
- unspoken words in a chunk at 45% opacity

**Shape:**
- the hook on the first content word
- one signature moment
- the end echoes the open
- stillness between

**Workflow:** show the plan in a few lines, and ask only when a cue is ambiguous. Assets go in `<work>/assets/`. URL capture isn't automated: fetch the image or ask for it (`references/sources.md` lists free libraries).

## 3. Render + verify
```bash
node $SKILL/talking/scripts/compile.mjs <work>/edit.json --preview        # half-res, ~34 s
node $SKILL/talking/scripts/compile.mjs <work>/edit.json --range 16:20    # one moment
node $SKILL/talking/scripts/compile.mjs <work>/edit.json                  # final 1080x1920, ~67 s for 27 s
```
- **Flags:** `--no-render` (writes props.json only), `--concurrency N` (4 is the sweet spot).
- **After a full render,** `verify.py` runs. Open `sheet.jpg` before claiming anything.
- **Placement warnings:** `FACE OVERLAP <id>` or `CARD OVERLAP <id> with <id>` means no clear lane was found. Change that card's `y` or `until`, or shorten its neighbour.
- **Keep:** src.mp4, cut.mp4, words.raw.json, words.json, track.json, edit.json, props.json, final.mp4.
- **Delete:** preview.mp4.
- **Fallback, captions only:** `python -I $SKILL/talking/scripts/render.py <work>/edit.json`.

## Mode rules
- **Cuts land in silence:** energy decides and VAD gates. Never widen a snap window past about 50 ms.
- **Faces:** uniform scale and shift only. Compile enforces the lanes.
- **Type:** one caption lane, one card lane, one accent, ≥ 70 px at 1080 wide.
- **New graphic:** a new card in `remotion/src/cards`, never per-clip HTML.
- **After touching the cut logic:** `python -I $SKILL/talking/scripts/test_prep.py`.
- **Honest limits:**
  - aligner edges are ±30–50 ms and not ear-checked
  - gesture emphasis is a MediaPipe guess

## Feedback
1. Take the timestamp and run `--range a:b --preview`.
2. Name the cause: a word ref, a lane, the face box or the zoom.
3. If it can recur, fix it in compile.mjs. If it's one moment, fix it in edit.json.
