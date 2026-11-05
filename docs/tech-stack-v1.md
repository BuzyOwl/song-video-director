# Tech stack: what was used, what it's good for, what hurt

## Stack A: Basement Goldfish (painterly cut-out)
| Layer | Tool |
|---|---|
| Drawing | p5.js + p5.brush (ClaudeAnimationBase starter kit): brush strokes, paper texture, 12 fps line boil |
| Frame render | `render.mjs`: puppeteer-core drives local Chrome, writes PNG frames, `--workers=N` |
| Encode | ffmpeg (frames + original MP3) |
| Art ingest | `tools/cutout.py` (Python, PIL/OpenCV): keys generated sprite sheets into transparent layers, aligns swim atlases on the eye |
| Lyrics | `tools/align.py`: Whisper large-v3 word times cross-checked against a second detector |
| Audio | `tools/energy.py`: loudness + onset per frame; beat grid ~132.5 BPM |
| Shorts | `tools/shorts.py`: vertical 1080×1920 cuts with looping start and end poses |

**Pros:**
- A genuinely handmade look.
- Small codebase.
- Deterministic.
- Easy character swaps through a pose table.

**Cons:**
- p5.brush watercolour fills are slow without a GPU: seconds per frame.
- Low-res art sheets give soft close-ups.
- Generated walk cycles repeat similar poses.

## Stack B: Toota Naksha (cinematic + procedural)
| Layer | Tool |
|---|---|
| Host | Remotion 4 (React/TypeScript): composition, parallel frame rendering, audio mux, h264 encode (CRF 17) |
| Engine | A custom framework-neutral ES-module engine; Canvas2D compositor plus one shared WebGL2 context. `renderFilm(ctx, t)` is a pure function of time. |
| GPU effects | textured meshes and homography warps; halftone/misregistration; 3D paper slabs with perspective, lighting and motion blur; GPU particles with bokeh depth of field; multiverse style shaders; a close-up lens pass (glass, rain, rack focus, diffusion) |
| Camera | 2.5D camera projection of still plates (floor-plane depth from the calibration) for real-feeling dolly and crane moves |
| Finishing | camera micro-motion, bloom/halation, anamorphic streaks, edge chromatic aberration, light leaks, grain, all audio-reactive |
| Vision tools | Python + OpenCV: ECC image registration, similarity-transform fitting (SVD), masks, vanishing-point and scale measurement |
| Lyrics | faster-whisper (CUDA int8_float16), multiple passes, confidence tags |
| Audio | numpy: per-frame energy, low-band kick flux, section hits → `data/audio_env.json` |
| Review | `tools/sheet.mjs` (bundle once, render stills, ffmpeg tile into sheets); ffmpeg frame pulls from the final MP4 |
| Team | Claude Code with parallel subagents, each owning specific files |

**Pros:**
- Remotion handles the boring hard parts: parallel rendering, encoding, audio.
- The engine stays portable (no React inside).
- WebGL gives real 3D, depth and light.
- Every frame is reproducible.
- Parallel agents cut wall-clock time about 5×.

**Cons:**
- **Browser GL quirks:** the shared context needs strict state hygiene.
- **Remotion's licence:** free for individuals; companies need a licence.
- **Disk use:** each render leaves temp profiles and bundles (redirect TEMP, clean up).
- **Acting is limited to sprite poses:** no real animation or lip-sync.
- **Identity drift** between generated image sets.
- **Plates upscaled** from about 1672 px.
- Lyric timing needs an ear-check.
- **Full renders take 10–20 min.**

## Stack C: Jod Ke Dekh (full 3D world, lyrics inside it)
| Layer | Tool |
|---|---|
| Host | Remotion 4.0.53x: composition, audio mux, parallel render, h264 (CRF 17) |
| Engine | three.js 0.186: one WebGL renderer and a scene table on the song clock (`[from, to, scene, 'wipe' or 'cut']`). Each scene exports `build(ctx)` and `update(t, ctx)`, and `update` is a pure function of `t`. |
| Transitions | a custom ScenePass (extends RenderPass) composites two scenes in linear HDR with a turmeric line-wipe, before bloom, so the line glows like the film's thread |
| Post | subframe motion blur (n renders averaged, `autoClear` off), UnrealBloom, OutputPass, a finish shader (vignette, grain, fade) |
| Type | lyrics drawn on canvas textures inside the world (TextPlane), with `maxWidth` auto-fit. The शिरोरेखा technique erases the headline band so a 3D thread can land on it. Fonts: Anek Devanagari/Latin, Instrument Serif, Tiro Devanagari, Kalam for handwriting. |
| Hero | a faceless clay mannequin from primitives, posed by forward kinematics |
| Props | Blender 5.2 headless (`blender -b -P tools/hand_grip.py`): a rigged hand from a downloaded mesh, a pose search, export to GLB plus a fit JSON (wrist and forearm points) and a wireframe JSON |
| Lyrics | faster-whisper merged with the creator's own word-start list (`tools/align_lyrics.py`), tags A2/A1/E, Roman/Devanagari display map |
| Team | 7 scene agents in isolated project copies (`tools/make_agents.py`, junctions to `node_modules`/`public`); one coordinator owns `film.js` and the bookend |
| Thumbnail | a Remotion still composition over a film frame rendered with debug flags (`front:0.085,clean`) |

**Pros:**
- Real 3D cameras, light and depth with no painted plates, so there is no identity drift between generated images.
- Lyrics inside the world read as story, not subtitles.
- Seven agents built 22 scenes in parallel.
- Blender scripts make the hand pose reproducible and tunable.

**Cons:**
- three.js API churn between versions (removed shadow types).
- A full 4:12 render takes about 25 min. For small changes, render only the changed tail and join it to the previous full render with ffmpeg.
- Posing a hand by script takes rounds of feedback. Judge it from several angles, not only the film camera.
- Blender MCP needs Blender running when Claude starts. The headless script path worked without it.

## Alternatives weighed
| Option | Verdict |
|---|---|
| three.js / Motion Canvas | Great for fully procedural 3D worlds. TN got its depth effects from WebGL2 inside its own engine, without a second framework. JKD then used three.js for a fully generated world (Stack C): pick it when there is no painted art and the world itself is the story. |
| makevoid "motion-graphics-music-video" plugin | Fal-generated video (real character acting and lip-sync), p5 graphics, Swift Core Image VFX. Strong for character performance, but it needs Ruby, macOS for Swift, and paid API credits. |
| After Effects | The industry standard for this look. Code wins on repeatability, exact sync to measured audio, and agent-driven iteration. AE wins on hands-on art direction. |

## Commands that worked (TN)
```bash
node tools/sheet.mjs --times=86,88,90 --cols=4 --w=480 --bundle=out/bundle-x --out=out/check/x.jpg
node tools/sheet.mjs --strip=33.2:34.2 ...                      # every frame of a moment
npx remotion render <CompositionId> out/film-vN.mp4 --concurrency=4
ffmpeg -ss <t> -i out/film-vN.mp4 -frames:v 1 -vf scale=480:-1 out/check/f.jpg
```

## 2026-10 renderer options (talking-head v2 decision)
| Option | Verdict |
|---|---|
| Remotion 4.0.53x | Chosen for talking-head v2: installed, TN lessons apply, `@remotion/fonts`, `--public-dir`, temp redirect to D:. Free for individuals. Headless-Chrome frame capture is the bottleneck (~67 s per 27 s 1080x1920). |
| HyperFrames 0.8.x (HeyGen, Apache-2.0) | HTML/CSS/GSAP -> MP4, agent skills (`/music-to-video`, `/talking-head-recut`, `/embedded-captions`), block catalog, `--gpu` NVENC. Same Chrome capture model. Worth a trial for the next song video; `/remotion-to-hyperframes` exists. |
| Song facts | Gate Whisper with Silero VAD (`vad_filter=True`); for lyric timing on a full mix, separate vocals first (Mel-Band RoFormer via audio-separator, needs torch) and align the stem with `aligner.py` (MMS, any language). |
