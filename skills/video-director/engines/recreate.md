# Engine: recreate a reference clip in 3D, then animate it

The reference video is the spec. Rebuild it as a real, controllable 3D scene, match its camera and light, then do what the original couldn't: new angles, new light, the song's camera, a playable space.

- **Blender is the default.** It's free, scriptable, and controlled through mcp-for-blender.
- **Unreal 5.8 is optional,** through Epic's experimental MCP plugin: use it when lighting and surface detail matter more than speed. The Unreal round took about 3–4× the time.

Method adapted from gokaygokay's video-to-shader and MattVidPro's video-to-unreal (MVP-Prompts).

## Rules
- **Never alter or project the reference into the scene,** and never put reference frames inside it. Anything the clip never shows can be inferred, but log it as inferred.
- **Assets:**
  - procedural or CC0 assets only (`references/sources.md`)
  - log every import in `CREDITS.md`
  - no paid assets, APIs or cloud jobs without a "yes"
- **Isolation:** a new project folder per recreation. Save a working state before every big push.
- **Editable source:** generator scripts live in `blender/gen_*.py`. Every mesh can be regenerated, and the scripts are the editable source.

## 1. Breakdown: `REFERENCE.md` (write it and keep going, no approval stop)
Extract frames every 0.5 s, and finer around fast motion: `ffmpeg -i ref.mp4 -vf fps=2 f_%03d.png`. Look at them upscaled. Record:
- **Clip facts:** duration, resolution, fps, cuts, loop.
- **Shot timeline:** time, beat, what's in frame, where the camera is.
- **Object inventory:** every object bigger than about 2% of the frame, with its parts, shape language, size relative to a ruler (door 2.0 m, desk 0.75 m, the hero), and position. Measure across several frames.
- **Materials:** base colour sampled as sRGB means from crops, roughness, metal, wear, grain direction, pattern scale.
- **Camera log:** path, height, FOV estimate, speed, easing and tilt per beat, solved into numbers you can key.
- **Light and palette:** every source (type, colour, rough intensity, flicker), key and fill direction, shadow softness, fog, bloom, grade.
- **Unreproducible:** what can't be matched, and the substitute for each.

## 2. Blockout (target: a running, saved blockout in 30–60 min)
- Real scale, simple primitives, the camera on the reference path, rough light.
- Render matched frames and compare composition.
- **Composition and camera are locked before any detail work.**

## 3. Detail passes, in the order the eye reads
1. Silhouettes and big forms.
2. Secondary forms: trims, panels, frames, bevels, book rows.
3. Surface: procedural materials, edge wear, dirt in crevices, emissives.
4. Light and atmosphere: GI, practicals with flicker, volumetrics, the grade matched to the reference.
5. Motion: anything that moves in the clip (flames, water, cloth, particles).

Repeated items (books, planks, rivets, bottles) come from one parameterised generator with seeded variation. Never hand-place copies.

## 4. Compare at matched times, then repair
- Render at the reference's timeline rows: at least the start, ¼, ½, ¾ and the end.
- Build side-by-sides at the reference resolution: `ffmpeg -i ref.png -i ours.png -filter_complex hstack cmp.png`.
- **Colour check** per key region: mean RGB and spread, reference against render. Colour alone can pass a flat painted frame, so also judge layout and silhouettes by eye.
- **Each pass:** write the 5 biggest visible differences, fix them, re-render. **At most 3 passes** on the match, then reassess honestly.

## 5. Then animate (the reason to recreate)
- The song's camera: keys on beats (as in `engines/guide-3d.md`).
- At least one **off-axis angle** that proves depth, and one **lighting change** that proves it's real (dusk, storm, lanterns only).
- **Output:**
  - final 3D renders, or
  - clay and depth guides for AI clips (`engines/ai-clip.md`), or
  - a stylised render matching the piece's STYLE.md (toon or grease-pencil line art over the recreated space)
- **Unreal branch only:** a playable mode (first-person walk, a few interactions, launchers `Play.bat` and `Open_Editor.bat`).

## Deliverables and log
- `BUILD_LOG.md`: timestamps per milestone, every compare pass with its 5 differences, measured render and frame times, remaining defects.
- **Final report:**
  - what matched vs. what was inferred
  - the 3 biggest remaining mismatches
  - performance
  - the file list

  Never invent token counts or costs.
