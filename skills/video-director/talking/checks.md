# checks.md (talking, YouTube boards, pitch films)

Read before every plan and every board; check the frames against it before calling a render done.
Lines tagged **Fact** are measured bugs and workarounds. **Safety** lines are hard rule 1. Everything else is a
direction: the default that worked, which a piece may break with one line in its STYLE.md.
New lessons go to `~/.video-director/checks.md`, not here (this folder is replaced on update).
Starter directions come from the user's past feedback and sirioberati/YouTube-AI-Motion-Graphics checks.md.

## Directions (defaults)
- Cards and text off the face; on boards keep the PiP bubble zone empty (hard rule 6 unless the creator asks).
- Readable sizes for the target screen (captions were ~70 px on 9:16 reels, ~52 px at 1080p in a pitch room; boards
  ≥ 40 px). If it doesn't fit, cut words before shrinking.
- Footage and screenshots at their real aspect ratio; don't crop to fill a box.
- Literal over abstract: the speaker names it, show that thing.
- One claim per board, written as its title; no paragraphs.
- Boards: elements land on the word that names it (board-sync); a board doesn't open empty or sit unchanged > ~3 s
  while the speaker talks; emphasis is size, not motion after landing.
- Caption reveal is a look choice: word-pop with unspoken words dimmed, or the whole line at full ink from its first
  frame (dimmed words read faint on phones in one pitch film).
- Accent colours per the piece's STYLE.md (one accent worked on reels); never dark text on a dark panel.

## Safety
- Never invent numbers, logos, quotes or footage; a missing asset is a dashed "pending" card.
- Check every competitor claim against the competitor's own site text before it goes on screen.
- Never play a person's AI-generated voice or present an AI-animated clip as a recording; keep it silent, tag it.

## Facts: words, cuts and captions (ViseMe / Drishyam pitch films)
- A start-only timestamp list has no word ends (an "end" is the next word's start; the last word has none). Measure
  speech end from a 10 ms energy envelope, with a lower threshold for END than onset (soft tails sit 20–30 dB under the
  peak). Out-point = real end + 0.15–0.25 s, never into the next word; a cut inside running speech is hand-placed.
- Aligner times can sit 0.3 s early at a cut and print a word the audio no longer has: use the later of team and
  re-listen times. Measure deleted silence from the audio, not words.json (1.8 s off on a slow speaker).
- A "pause" can be a drawn-out word: check before trimming (splitting a long "with" became "watch history").
- Prove every caption line complete with Whisper on the final mix.
- Fade lengths: 25 ms on a cut inside speech (90 ms ate a syllable); ~150 ms into room tone where a cut stops in raw room
  noise (25 ms stepped the floor down 10 dB). A phone take can end ~50 ms after the last word: read the source to its end.
- A caption or plate fade that crosses a camera cut leaves ghost text in the next shot: end them ≥ 0.02 s before it.
  Abutting J/L segments stack two text boxes in one zone unless the old one ends first.

## Facts: audio
- EQ-matching voices with big high cuts kills consonants (−6 dB above 4 kHz turned "studio" into "watches"): move about
  a third of the way to the shared curve, ≤ 3 dB, never cut > 2 dB above 2 kHz.
- Render dialogue + effects without music, then mix the bed in a separate step with video stream-copied: a new track
  becomes a remux, not a re-render. Measure true peak on the encoded AAC, not the WAV.

## Facts: cutouts and compositing
- Cream backgrounds hide white matte slivers: check every cutout on dark and on light over several frames. Matte at
  native resolution, open the mask ~9 px, keep the biggest piece.
- Light or vignette inside a person's clip/iris draws a visible circle on the card; put room light on the card.
- Show a cutout's own frame at the in-point before it plays, or the still-to-video swap pops.
- Rebuild room plates with the exact ingest reader (grab, crop, resize, fps); prove alignment by differencing inside
  solid alpha against a +1-frame-slip control.
- Growing a grid tile into a medium: lay out at the medium size and tween scale + clip-path inset from the tile rect, so
  the picture never upsamples from a small box.

## Facts: HyperFrames / GSAP / ffmpeg
- `hyperframes check --samples=<duration/0.25> --caption-zone="...;severity=error"` is a working collision gate; its
  layout pass ignores a parent's opacity, so hide finished caption pages with visibility. Give it per-person head boxes
  or generic boxes false-alarm.
- Hiding a live `<video class="clip">` with visibility on a wrapper fails (the engine sets the clip visible): use opacity.
- GSAP `fromTo` renders its start state from frame 0: hide in CSS and `tl.set` on cue for anything hidden until its moment.
- A generic class name (.who, .name) reused across layers collided and printed over captions.
- An absolutely positioned strike line inside a wrapping phrase collapses to a dot (use `text-decoration: line-through`);
  an absolute highlight box inside an inline word paints over the text without z-index on the text.
- After an ink change re-run contrast (60% ink measured 4.41:1, failed; 70% passed).
- Patching a few frames: overlay fixed snapshots in ffmpeg with the source's colour tags (a cv2 decode/re-encode shifts
  every frame ~2/255); diff against the old render, only patched frames may change.
- `assets/music/*.*` also matches LICENSE.txt: pass the file. On Windows, ffmpeg drawtext can segfault in fontconfig:
  label contact sheets with cv2.
