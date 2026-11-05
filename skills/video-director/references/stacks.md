# Stacks and looks: what to use where (a guide, never a limit)

Any stack is allowed if it serves the video's tone, mood and the user's ask. This file says where each one has
worked best, its pros and cons, the combinations that held up, and when Blender earns its place.
A newer tool that renders better, faster or is easier for an agent to write reliably is worth a trial: measure it on
one shot against the current pick, and switch on a measured win. Versions move fast; check the current release before
quoting a flag.

## 1. Looks: a menu to start from, never a fence
Offer the user three kinds of start in one message, and let them mix:
1. **Their own style.** Brand kit, reference films, mood board, a painter, a frame they love, or plain words.
   Build it with `references/style-protocol.md`. Their style always wins over anything below.
2. **A ready-made look** (proven in finished films, in `styles/`; clips in `gallery/index.html`):
   | Look | Proven in | Suits | Stack |
   |---|---|---|---|
   | Cinematic plate | Toota Naksha | ballads, longing, one protagonist with a face | Remotion + Canvas2D/WebGL 2.5D plates |
   | Clay world | Jod Ke Dekh | rap, spoken word, wordplay and metaphor | three.js in Remotion |
   | Mist silhouette | Himalayan Vow | slow romantic, devotional, travel, ambient | three.js in Remotion, fully procedural |
   | Painterly cut-out | Basement Goldfish | comic or warm indie/folk story songs | p5.js + p5.brush |
   | Pop era collage | My Teacher Used To Say | nostalgia, then-vs-now, life journeys | Canvas2D engine + Blender-baked 3D clips |
   For talking and YouTube: the explainer grammars in `modes/youtube.md` §3 (3b1b, keynote UI, finance chart,
   Kurzgesagt, Vox collage, whiteboard, storytime, kinetic type) are the same kind of menu.
3. **A fresh look invented for this piece**, from what the song or script believes, its tempo and its world.

A ready-made look is a starting point: change its palette, medium, camera or engine freely. Two pieces in a row in
the same look is fine when the user asks for it; Claude never pushes a past look, and never avoids one either.

## 2. Stack guide
| Stack | Best for | Pros | Cons | Agent-friendliness |
|---|---|---|---|---|
| **HyperFrames** (HTML + CSS + GSAP → MP4, Apache-2.0) | lyric/kinetic type, motion graphics, explainer boards, 2D cut-out or plate films, captions, title cards | plain HTML; `check` lint; ~450 registry blocks; fastest to iterate; seekable; no company licence threshold | no real 3D light; long films get heavy in one DOM; three.js only through its canvas adapter (trial before relying on it) | highest: plain HTML/JSON, lint, snapshots |
| **Remotion** (React → MP4) | compositing footage + graphics, the talking pipeline, hosting Canvas/WebGL/three.js engines, data-driven batches | mature render farm (concurrency, Lambda); good audio/video handling; React component reuse | React boilerplate per effect; company licence over a team-size threshold (check current terms); AAC ~43 ms late (mux WAV) | good, but more code per effect |
| **Canvas2D / WebGL engine** (own renderer, hosted by Remotion or Playwright) | 2.5D painted plates, parallax, custom shaders, many layers | total control; fast per frame; one shared GL context | you build every tool; leaked GL state causes "random" glitches | medium: needs the engine's own rules |
| **three.js** (inside Remotion, or HyperFrames' adapter) | a world that is itself the story: real camera, light, depth, words on objects | real 3D, PBR, post (bloom, blur); GLB import from Blender | 20–25 min renders; API churns (pin it); GPU one job at a time; looks cheap without `craft/light.md` | medium: probes and blocking data keep it honest |
| **p5.js + p5.brush** | hand-painted, line boil, watercolour, playful cut-out | instant handmade feel | slow without a GPU; weak at high-res close-ups | good for small sketches |
| **Blender** (headless `blender -b -P`, or the Blender MCP) | real sets, characters and rigs, poses, baked light, previs for AI clips, 3D printing-grade assets | free; Cycles/EEVEE quality; MPFB humans, Mixamo rigs, CC0 kits (Quaternius, Poly Haven); scriptable | render time; per-frame lyric sync is clumsy inside it; EEVEE world volume blacks out the sky (use a mist box) | good via Python scripts + MCP `look` |
| **Unreal** (Sequencer + Movie Render Queue) | huge realtime worlds, Lumen light, a later game from the same assets | realtime look-dev; MRQ quality | heavy; MCP link can drop; a river slice once came out unusable and the work moved to Blender | lower: more state, less scriptable |
| **AI video clips** (Seedance, Kling, Veo, Runway, Higgsfield; `engines/ai-clip.md`) | realism the code can't reach: real-looking people, nature, physical effects | photoreal in seconds | costs credits; drifts on camera paths, choreography and identity; never exact timing | prompt as a production plan; guide with Blender |
| **Python + ffmpeg cut** (talking pipeline) | removing fillers and pauses, word timing, face tracking | fast, exact, cached | not a renderer | high |
| **After Effects** (via the ae-builder skill, companion) | when the user needs an editable AE project | industry handoff | paid; separate tool | medium |

## 3. Combinations that held up
| Piece | Combination | Why |
|---|---|---|
| Lyric / kinetic type video | HyperFrames alone | lint + blocks + fastest rounds |
| 2D story or cut-out music video | HyperFrames (or p5.js for painted boil) + measured plates | 2D needs no 3D cost |
| 2.5D painted-plate film | Remotion hosting a Canvas2D/WebGL engine | parallax, post stack, plates with scale engine |
| 3D world music video | Blender for sets/characters → GLB → three.js in Remotion, words on canvas textures | Blender builds, three.js times to the song |
| Film-grade 3D lighting | Blender Cycles renders image sequences (with alpha) → composite and type in Remotion or HyperFrames | baked light, sync stays in the compositor |
| Realistic shots in a code film | Blender clay blockout → first/last frames + depth/line passes → AI clip → composite | the camera and scale stay yours, AI adds realism |
| Dance | motion transfer (Higgsfield) for speed, or FreeMoCap/Rokoko → rig in Blender for exact choreography | exactness vs speed |
| Talking reel | Python cut → Remotion (video, bubble, captions, small cards) + HyperFrames full-screen boards | each does what it's best at |
| YouTube explainer | Python cut → Remotion 16:9 comp + HyperFrames boards per grammar | boards are HTML; footage is Remotion |
| Pitch or multi-speaker film | Python cut per take → HyperFrames room comp with cutouts, shared audio chain | layout gate (`hyperframes check`) |
| Animated short / cutscene | blocking data (`craft/blocking.md`) → three.js or Blender → composite | paths locked before detail |
| Recreate a real clip in 3D | Blender (default) or Unreal (`engines/recreate.md`) | editable source scripts |

## 4. Blender: when, and how it hands off
**Use Blender when** the piece needs real 3D form or light that code won't sell: characters with anatomy (MPFB +
Mixamo, heights in cm), sets with real textures, baked GI, a camera blockout to steer AI clips, hero props or hands posed
by FK, or assets reused later (a game, other videos).
**Skip Blender when** the piece is 2D, type-led, or must re-time every frame to words: do it in HyperFrames/Remotion.
**Handoffs:**
- GLB/glTF → three.js (no loose-edge export: wireframes go as a JSON segment list).
- PNG/EXR sequence with alpha → composite in Remotion or HyperFrames; type and sync stay in the compositor.
- Camera export (per-frame JSON) → overlays that track the Blender camera.
- Clay, depth, line passes → AI clip guidance (`engines/guide-3d.md`).
- A pose solve or fit as JSON → a code engine (`blender -b -P pose.py`).
**Check it** with stills from 3 angles with real props before animating; `look` through the Blender MCP; scale from
known objects.

## 5. Choosing (one line per scene in the route step)
Pick by: does it hit the look and mood → cost (render minutes, tokens, credits) → how reliably an agent can write it →
does it fit what's already built. Start on the lightest that passes a one-still test; step up when the still misses the
look; never water the look down to stay on a light stack. Mixing stacks inside one piece is normal.
