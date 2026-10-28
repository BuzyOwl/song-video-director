# HyperFrames boards (full-screen slides synced to the voice)

Why HyperFrames here: a board is a page of HTML + GSAP. HyperFrames seeks that timeline frame by frame (deterministic),
lints it (`check`), and ships ~450 blocks (`/hyperframes-registry`: charts, kinetic type, transitions). The 74 boards of
github.com/sirioberati/YouTube-AI-Motion-Graphics (MIT, local clone
`D:\03_Projects\Video Caption Project MIC Class\YouTube-AI-Motion-Graphics`) are the same kind of file. In Remotion each
would need a React port. Remotion still composites the result: cut video, PiP bubble, captions.

## Make one
1. Pick the board from what is said: `YouTube-AI-Motion-Graphics/skills/explainer-board-system/references/board-catalog.md`
   (each board has "say it when" tags in spoken words), then the registry (`npx hyperframes catalog`). Borrow the motion
   and layout; the boards there are 1920x1080 with a bottom-right camera box, ours are 1080x1920.
2. Copy `assets/hf-board/` (tested template: index.html + local gsap.min.js) to `<work>/boards/<name>/`. Root
   `data-width="1080" data-height="1920"`, `data-duration` = the board span (compile prints `HF DURATION` if not).
3. edit.json: `{"type": "board", "at": ..., "until": ..., "html": "boards/<name>", "sync": {"#row1": "email#6", ...}}`.
   compile writes `sync.js` (`window.__sync["#row1"]` = seconds from the board start, word start + 0.05 s) and the
   timeline places each tween at `__sync[sel]`.
4. `npx hyperframes check --json` in the board dir (after one `compile.mjs --no-render` so sync.js exists): fix errors,
   weigh warnings (`dead_stretch` = the nothing-still rule below).
5. `compile.mjs` renders `board.mp4` with HyperFrames (~34 s for a 12 s board, GPU) only when the board's sources
   change (`board.key`), then Remotion plays it under the bubble. Look at frames before saying it works.

## Safe zones (1080x1920)
- PiP bubble: x 632-1021, y 150-539. Nothing readable there.
- Caption band: from `captions.y` (default 0.84 h) +-0.08 h. Nothing readable there unless `captions` is null.
- 60 px padding on every side; every readable word >= 40 px (phone).

## Sync rules (from board-sync, proven on real reviews)
- Land on the word that names it: never before the word, never more than 2 s after.
- A part never lands before its container; an arrow never before both of its ends.
- Structure first: headline and boxes/rails/axes are on screen from frame 0. No board opens empty.
- Nothing still for more than ~3 s while the speaker talks: fill with the speaker's own words (a 2-4 word note),
  never invented copy.
- Nothing moves after it lands: no pulses, loops, zooms or camera pushes inside a board. Emphasis = size.
- Money/percent pop only on a number said as money/percent; a count never gets a price sticker.
- Copy that contradicts what is said is flagged to the user, never silently changed. Never invent numbers, logos,
  quotes or footage: a missing asset is a dashed "pending" card.
- QA: each element is absent 0.1 s before its word and present 0.5 s after (pull those two frames).
