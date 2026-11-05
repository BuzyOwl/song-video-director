# Craft: render and render checks (drafts, finals, joins, mux, colour, QA)

Load for every render past the first still, every join or mux, and whenever someone reports flicker, a pop, a blank
frame, colour shift or A/V lag. `scripts/film_gate.py` covers the automatic part; this file covers the rest.
Adapted from Imaginative-Prompting/claude-video-skills `rendering` + `render-checks` (MIT).

## Before you queue
- **Prove it renders cheaply first:** typecheck, load every module, bundle the whole project, render one real frame.
  (A scene with no component behind it threw at frame 1 after two hours in a queue.)
- **Render from a frozen copy** for anything long; a queued render uses the code as it is when it starts (macOS: an
  APFS clone, `cp -c -R`, costs no extra disk).
- Pin `remotion` and every `@remotion/*` to one exact version. Pin three.js.
- Fonts: static instances through one loader that holds the frame until ready.
- Bake heavy meshes ahead (scene build > load timeout, 30 s default, fails). Exact integer output sizes.

## One GPU job at a time
Two headless Chrome renders at once lost WebGL contexts and blanked frames. All renders, still batches and in-browser
probes go through one queue (a lock file is enough). Stills jump ahead of renders; keep tickets ~15 min (renders) and
~5 min (stills). Log full output to a file; never pipe through `tail -1`. To cancel, kill the whole process tree
(npm, node, Chrome), then confirm the queue is free. Never kill a process you didn't start.

## Drafts vs finals
- Draft: 720p, shutter capped (~8 samples). Final: full res, full samples.
- **Trust a draft shortcut only after a draft still matches a full still of the same frame** (lower pixel ratio darkened
  an AO pass and showed as a pop at a join).
- Before a 4K master: 4K stills of every world/effect, downscaled to 1080p, vs 1080p stills. Anything in output pixels
  (grain, line width, bloom radius, canvas text) scales by frame height ÷ 1080.

## Motion blur
- Average sub-frame shutter samples across 180° (half the frame interval); know whether samples centre on or trail the
  frame and log the real sample times. Sharp lettering stays sharp at ~4 px movement per sample, not 12.
- **Fact:** movies and stills can sample different times (in one film no movie sample fell on a whole frame; a still
  was exactly the frame). A bug seen only in the movie lives at sub-frame times: render single samples as stills.
- **Prove the mixer:** a test where each frame shows its own number; frame k's mix must show only k.
- R3F in Remotion: don't `advance()` after every canvas-texture draw (4–5 renders a frame); render once after the last
  draw in the frame's commit, and never skip that last render (cleared canvases came out pure white).

## Chunks and joins
- **Pre-roll every chunk** ~12 frames and drop the run-in (first frames come out cold). Compare the first frame after
  each boundary with the one before it, colour as well as brightness.
- 4K chunks as ProRes 422 HQ: `-c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le` (intra-frame, seamless joins).
- **Never join by stream copy** (`concat -c copy`): it started a part 21 ms late and gave irregular packet durations that
  players turned into dropped and repeated frames. Decode in order, encode once:
  `ffmpeg -f concat -safe 0 -i list.txt -vf "setpts=N/(30*TB),setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709" -fps_mode cfr -r 30 -c:v libx264 -crf 17 -pix_fmt yuv420p out.mp4`
  (your fps in place of 30).
- Splicing a partial re-render: everything the change adds is out of frame at the splice; prove the seam by comparing
  old vs new frames just outside the kept span.
- **Fact:** diff a patch's pre-roll frames against the cut before handing it over (missing props once drew an old
  version of a section, and it passed its checks: the wrong scene rendered).
- **Fact:** a mount or speed gate changed the picture on every frame it covered. Render one frame inside the gated span
  before and after the gate, and diff it.

## Colour
- BT.709 everywhere. ffmpeg 8 keeps frames' own tags over output flags, so stamp them in the filter chain:
  `setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709`.
- PNG → mp4 needs `scale=out_color_matrix=bt709` (else BT.601, a green shift). Raw frames piped in: tag the input
  (`-colorspace bt709 -color_range tv` before `-i -`).

## Audio
- **Render the picture muted, then mux the master WAV from time 0** (Remotion's own AAC came out 42.7 ms late):
  `ffmpeg -i picture.mp4 -i song.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k out.mp4`.
- No `-shortest` under a copied picture: pad or trim the audio, then count output frames.

## Checks (after every render, before anyone sees it)
1. `film_gate.py`: HARD = global flicker, blank, delivery (tags, CFR, A/V offset), loop; dead gap and slideshow are
   reported against the feel card and only fail when feel.json sets `"gate"`.
2. **Blank scan:** black, white, frozen, magenta or missing frames; frame count vs expected. (A draft with 55 of 101
   frames blank once passed its QC.)
3. **Pop scan:** spikes in frame-to-frame difference. Each is a designed snap or a bug; look at every one. Anything that
   vanishes between two frames is a pop until you've shown it leaving the edge.
4. **Hard-cut scan:** colour-histogram jump per frame pair (16 bins/channel at 160×90, half L1). Catches one-frame world
   switches inside fast motion where pixel diff can't.
5. **Local flicker** (z-fighting, decals 1 mm off a surface, shader thresholds tipping, shadow crawl, thin-face glints,
   grow-from-zero-depth, window and frame edges in 3D sets): film_gate only sees global luminance flashes. Run
   `python -I $SKILL/scripts/flicker_scan.py film.mp4 --start s --end s --out flicker/` on every 3D or shader span.
   It aligns neighbours with optical flow, scores 1–3-frame runs that change and change back, quiets fast motion, and
   writes `report.json` (ranked events: time, source frame, box), `mask.mp4` and `sheets/event_NN.jpg` (5 frames round
   the peak; bottom row = flagged pixels in red). Judge each event on its sheet: designed blinks, sparkles, strobes and
   per-frame noise or grain (a dither, a noise texture) score too. Calibrate `--seed/--grow` on one known flicker and one
   known-clean span per project. **Fact:** compare chroma at 4:2:0 resolution, or saturated edges under a pan read as
   flicker (the scanner does this). Method: Imaginative-Prompting/claude-video-skills `render-checks` (MIT).
6. **Jitter:** phase-correlate consecutive frames; a 1 s window with no step >12 px whose path is ≥14 px but net travel
   <35% of path = the camera wandered and came back.
7. **Clipping:** audit oriented boxes + swept circles before render; triangle tests for thin parts; measure depth before
   calling a fault (1 mm fingertips on keys); the camera is a solid too. Then 100% stills of every cluster.
8. **Step consecutive frames** round everything flagged, every contact, entrance and transition. Watch at speed with song.
- Frame-exact extraction: `-ss` isn't exact. Use `-vf select=eq(n\,K) -fps_mode passthrough` and assert the count.

## Checks must be able to fail
Plant a known-bad case and see the check fail ("nothing to plant on" is a failed check). A perfect score is a prompt to
check the instrument (a mis-parsed flag compared a frame with itself: "diff 0.000"). Count what was compared vs expected.
A FAIL can be the instrument too: check its inputs before reporting. Run any new detector on a clean render first.
