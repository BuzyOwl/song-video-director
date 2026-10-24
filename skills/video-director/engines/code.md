# Engine: code (HyperFrames · Remotion · three.js · p5)

## Pick the lightest one that passes the frame-first test
| Engine | Use for | Cost | Avoid when |
|---|---|---|---|
| **HyperFrames** (HTML + CSS + GSAP → MP4) | lyric videos, kinetic type, graphic looks, any 2D design | low; fastest to iterate | you need real 3D light and depth |
| **Remotion + Canvas2D/WebGL** | 2.5D story films from art plates, a mix of footage and graphics, the talking pipeline | med | the whole world is procedural 3D |
| **three.js inside Remotion** | a world that is itself the story (lyrics on objects, real camera, light, depth) | high: 20–25 min full renders | 2D would carry it; then it's a waste |
| **p5.js + p5.brush** | hand-painted cut-out with line boil | med; slow without a GPU | high-res close-ups |

Install the official agent skills next to this one:
- `npx skills add heygen-com/hyperframes` (it includes `/music-to-video`)
- `npx skills add remotion-dev/skills`

Their API rules beat any memory of them. This file only adds what our films taught.

## Contract (all engines)
- **Every frame is `render(t)`:**
  - no state between frames
  - no Math.random (use a seeded RNG)
  - no Date.now, timers or rAF loops
  - guard every search loop: a t-dependent infinite loop hangs Remotion at "waiting for the page"
- **The song is the only clock.** The scene table is data: `[from, to, sceneId, 'cut'|'wipe'|...]`. Each scene exports `build(ctx)` and `update(t, ctx)`.
- **Fonts:**
  - free fonts only, loaded by `<link>` (HyperFrames) or `@remotion/google-fonts`
  - in HyperFrames, if you link any font, link every font
  - never copy paid font files
- **Media** lives in the project's `media/` or `public/`. Never touch the user's originals.

## HyperFrames specifics
- **Structure:**
  - one root `<div id="root" data-composition-id="main" data-duration=.. data-width=.. data-height=..>`
  - one paused GSAP timeline at `window.__timelines["main"]`
  - timed media gets `class="clip"` plus `data-start` and `data-duration`
- **Commands:**
  - lint: `npx hyperframes lint <dir>`
  - stills: `npx hyperframes snapshot <dir> --at 3,9,15 -o stills/`
  - render: `npx hyperframes render <dir> -o out.mp4 -q draft|high`, adding `--gpu` when NVENC is available
- **Text** that changes over time changes inside the timeline (onUpdate), never through `gsap.set` on innerHTML.

## Remotion specifics
- Keep the engine framework-neutral: plain ES modules with `renderFilm(ctx, t)`. Remotion only hosts it, which handles parallel frames, audio mux and h264 at CRF 17.
- **One shared WebGL2 context:** reset its state after every pass (blend, framebuffer, viewport). Most "random" glitches are leaked GL state.
- **Temp files on the big drive:** `TEMP`/`TMP` = `VD_TMP` in `remotion.config.ts` and the render env. Every run leaves Chrome profiles behind; one project filled C: with 7.8 GB.
- **Commands:**
  - stills for review: `npx remotion still <Comp> --frame N` (bundle once with `--bundle`, reuse it)
  - render: `npx remotion render <Comp> out.mp4 --concurrency=4`
- **Tail render for small changes:** render only `--frames a-b`, then join:
  `ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4`. Cut at a keyframe, or re-encode the joint second.

## three.js specifics
- One renderer. Transitions composite two scenes in linear HDR **before** bloom, so wipe lines glow.
- **Post:**
  - subframe motion blur: average n renders with `autoClear = false`, otherwise it comes out dark
  - bloom
  - one finish shader: vignette, grain, fade
- Lyrics go on canvas textures inside the world (TextPlane with maxWidth auto-fit). Mirrored floors reflect text: use render layers.
- Pin the three.js version. The API churns; 0.186 removed `PCFSoftShadowMap`.
- **Hero bodies:** primitives can't carry anatomy. Use a rigged mesh, posed by FK, or by Blender headless (`blender -b -P pose.py` exports GLB plus a fit JSON). Judge poses from 3 angles, with the real props.

## Finishing that reads as "film", not "code"
- **Camera micro-motion:** a slow drift of 0.3–0.8% of frame width per second, plus a 2–4 frame settle after every move. A dead-still camera reads as a slideshow.
- **Light carries emotion:** one key, one rim, and warm/cool contrast between sections.
- **Lens pass** only on close-ups: rack focus, diffusion, a little halation. Grain at 2–4% on everything, so code-perfect gradients stop banding.
- **Audio-reactive ≠ everything pulses.** One element listens to the kick (a light, a thread, the particles). The rest follows the section's arousal.
- **Cut on motion:** start the next shot while something is still moving. Land hits on the beat; cut 1–2 frames early.

## Parallel agents (big rounds)
1. **Before dispatching:**
   - split by file ownership
   - create stub modules and wire their hooks into the frame pipeline first
   - give each agent its own project copy (junctions to `node_modules` and `public`)
2. **Each brief carries:**
   - the song facts
   - the feel card
   - the STYLE.md
   - `anchors/` (the approved stills)
   - the universal rules
   - its files
   - its verification commands
   - the shared-file rule: read right before each edit, small anchored edits, never rewrite a whole file
3. **Steer mid-flight** with short notes.
4. **The coordinator owns the scene table, transitions and bookends,** and checks every seam where two agents' layers share a timestamp or a frame region. Thin one layer when two land on the same hit.

## Tool sharp edges (Windows)
- Inline heredocs and `sed` eat quotes and backslashes. Write patch scripts to files, or use an exact-match edit.
- A CLI that splits arguments on `=` mangles `--debug=front=0.1`; use `front:0.1`.
- Read errors literally. ENOSPC means find where the disk went.
