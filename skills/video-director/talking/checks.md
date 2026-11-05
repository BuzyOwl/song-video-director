# checks.md

Read before every plan and every board; check the frames against it before calling a render done. Every correction
the user makes becomes one line here. Format: `- DO / DON'T: the rule (the clip that taught it)`. Newest at the bottom.
Starter rules come from the user's past feedback and sirioberati/YouTube-AI-Motion-Graphics checks.md.

## Canvas
- DON'T: put cards or text over the face; on boards, keep the PiP bubble zone empty. (every clip)
- DO: every readable word >= 70 px for captions, >= 40 px on boards. If it does not fit, cut words, never shrink. (v2)
- DO: keep footage and screenshots at their real aspect ratio. Never crop to fill a box.

## Content
- DO: literal over abstract: the speaker names it, you show that thing. (v2)
- DON'T: put a paragraph on a board. One claim per board, written as its title.
- DON'T: invent numbers, logos, quotes or footage. A missing asset is a dashed "pending" card.

## Motion
- DO: everything appears on the word that names it. (sirioberati board-sync)
- DON'T: open a board empty.
- DON'T: let a board sit still more than ~3 s while the speaker talks.
- DON'T: zoom or pulse elements after they land; on boards emphasis is size, not motion.

## Colour
- DO: one accent per clip; numbers and key words in it.
- DON'T: dark text on a dark panel.

## Group and pitch films (several speakers as cutouts in one room)
Learned on the ViseMe and Drishyam pitch films (Nov 2026).
### Layout
- DO: fixed zones before any shot: meta bar, stage, label zone (name plate, tag), caption lane nothing else enters.
  Prove it with a script sampling every 0.25 s for heads, bodies and text boxes in the zones, not by eye; give it
  per-person head boxes (crown/chin from meta, width from the matte at the eye row) or it false-alarms.
- DO: shot budget = speaker + their one name plate + caption + at most one chip. Swap a panel's content, never add a box.
- DO: name plate directly under the ACTIVE speaker (moves on a cut, stays on a punch-in); dim and slightly blur resting
  neighbours so the speaker is obvious.
- DO: fill the frame: medium = head ~40% of height (crown ~17% from top), table band ~22%, captions ~52 px at 1080p on
  one line. Seat early speakers in the middle, fill centre-out. Many people → rows or a cluster, never one thin line.
- DO: equal head sizes in a group (scale by eye distance + crown-to-chin mixed; eyes on one line); highlight the speaker,
  don't enlarge them. A person who moves their head through a line gets a lower crown line override.
- DON'T: a neighbour's head or shoulder cut by the frame edge in a medium; fit them in the 90% area or leave them out.
  Back tier high enough that a front speaker's medium never shows it.
- DO: `hyperframes check --samples=<duration/0.25> --caption-zone="...;severity=error"` to 0 errors; its layout pass
  ignores parent opacity, so hide finished caption pages with visibility.
- DO: opaque pill behind small labels over footage; re-run contrast after any ink change (60% ink 4.41:1 failed, 70% passed).
- DO: contributors with no footage as clean typography ("Also building with us"), never blank heads or empty seats.
### Cutouts
- DO: check every cutout on dark and on cream over several frames (cream hides white slivers); matte at native res,
  open the mask ~9 px, keep the biggest piece. Feather the side edges of phone-portrait cutouts.
- DO: one motion language for people: enter/leave through the same iris on the eyes, sit as a still of their own first
  frame, wake into video in 5 frames with a 2% lift, rest on their own last frame in 7. Opacity leads the iris.
  Show the cutout's own frame at the in-point before they speak, so still-to-video is one frame-exact step.
- DO: light cutouts into the room (shared key, contact shadow, edge light-wrap). Room light belongs to the card, never
  inside a person's clip (it draws a visible circle). Fades are fine for real-person cutouts in a pitch film; the
  body-crossfade ban is for sprite and music-video storytelling.
- DO: hide (not fade in) a person cut off at a move's start and still off-frame at its end. Grow a grid tile into a
  medium by laying out at medium size and tweening scale + clip-path inset from the tile rect.
- DON'T: hide a live `<video class="clip">` with visibility on a wrapper (the engine sets the clip visible); use opacity.
- DO: rebuild room plates with the exact ingest reader (grab, crop, resize, fps); prove alignment by differencing inside
  solid alpha against a +1-frame-slip control.
### Words, cuts and captions
- DON'T: trust a word's end from a start-only list (it's the next word's start; the last word has none). Measure speech
  end from a 10 ms energy envelope with a lower threshold for END than onset (soft tails sit 20–30 dB under the peak).
  Out-point = real end + 0.15–0.25 s, never into the next word; a cut inside running speech is a hand-placed boundary.
- DON'T: let aligner times decide what a caption shows at a cut (one sat 0.3 s early and printed a cut word); use the
  later of the team and re-listen times. Measure deleted silence from audio, never words.json (1.8 s off on a slow speaker).
- DON'T: trim a "pause" before checking it isn't a drawn-out word. Prove every caption line complete with Whisper on the
  final mix.
- DO: 25 ms fade on a cut inside speech (90 ms ate a syllable); ~150 ms fade into room tone where a cut stops in raw room
  noise (25 ms stepped the floor down 10 dB). Check where a phone take's audio really ends (~50 ms after the last word).
- DO: captions at full ink from their first frame on phones (grey-then-lit reveals read faint). Reading floor ~0.5 s +
  0.2 s a word; one sentence per shot. End captions and plates ≥0.02 s before the next cut; at speaker hand-offs end the
  old plate and caption before the new ones start (J/L cuts otherwise stack two boxes).
- DO: a panel's first content starts with its shot; outgoing content fades over the last 0.2 s. Never an empty panel.
- DO: for a pitch film, check every competitor claim against their own site text before it goes on screen.
- DON'T: play a person's AI-generated voice or present an AI-animated clip as a recording; keep it silent, tag "AI-animated".
### Audio
- DO: one chain on voices from different phones and rooms: denoise, partial EQ-match (a third of the way, ≤3 dB, never
  cut >2 dB above 2 kHz: −6 dB above 4 kHz turned "studio" into "watches"), same LUFS and compression, one shared room
  reverb and tone, J/L overlaps.
- DO: keep music out of the video render: render dialogue + effects, then duck, mix and master the bed in a separate step
  with the video stream copied, so a new track is a remux. Measure true peak on the encoded AAC, not the WAV.
### Engine gotchas (HyperFrames / GSAP / ffmpeg)
- DON'T: GSAP `fromTo` for something hidden until its moment (it renders its start state from frame 0); hide in CSS, `tl.set` on cue.
- DON'T: reuse a generic class name (.who, .name) across layers. DON'T: an absolute line for a strike inside a wrapping
  phrase (use line-through). DON'T: an absolute highlight box inside an inline word without z-index on the text.
- DON'T: a parallax layer that drags a wall sign half-cut into later shots.
- DO: patch a few frames by overlaying fixed snapshots in ffmpeg with the source's colour tags (a cv2 round trip shifts
  every frame ~2/255); diff vs the old render, only patched frames may change. Long render, one fix: patch the seconds,
  splice frame-exactly.
- DON'T: glob `assets/music/*.*` (picks up LICENSE.txt). On Windows, ffmpeg drawtext can segfault in fontconfig: label
  contact sheets with cv2.

## Your fixes
<!-- Add new rules below this line. Newest at the bottom. -->
