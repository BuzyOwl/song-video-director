# Engine: 3D guide (Blender blockout or dance reference drives the AI clip)

**Why:** AI video drifts on camera paths, choreography and geometry. A 3D blockout fixes all three in a minute of CPU time:
- the exact lens and path
- beat-locked timing
- real scale and occlusion

The AI only has to "paint" the result. Use this whenever a shot needs a precise camera move, a choreography, or several angles of one space.

## Tools
- **mcp-for-blender** (`uvx mcp-for-blender`, formerly blender-mcp):
  - `get_scene_info`, `execute_blender_code`, `look`
  - CC0 assets: `search_assets` / `import_asset` (Poly Haven, Sketchfab, Poly Pizza)
  - `generate_3d` for one prop
  - Start with `get_addon_status`.
- **Alternative: Blender Lab's official MCP** (Blender 5.1+). It uses the same port (9876), so run **only one** of the two.
- **Without an MCP:** run headless with `blender -b -P script.py`. Keep scripts in `blender/` so every shot can be regenerated.
- **Scripting rules for someone else's Blender:**
  - find shader nodes by `type`, never by name
  - read enum identifiers, never hardcode them
  - put colours on node inputs
  - size imported models from `world_bounding_box` and set them on the ground

## Blockout to guides
1. **Blockout at real scale** (metres): primitives plus CC0 imports, grey clay material, one key light matching the planned light direction. Set the scene fps to the film's fps.
2. **Camera on the beat:** convert the beats from `song_facts.json` to frame numbers. Put camera keys on the downbeats, using Bezier with ease-in-out, plus a 2–4 frame settle. Set a real lens (24/35/50/85 mm) to match the look.
3. **Clay animatic:** render with Workbench or EEVEE at 480p, mux the song in, and show it. **The user approves the camera and timing here,** before any credit is spent.
4. **Export guides** per shot, each with one job:
   - `first.png` / `last.png`: clay frames. Turn them into styled keyframes with image generation (the same identity references), or with depth→image so composition stays exact.
   - `depth.mp4` (mist or Z pass, normalised) and `lines.mp4` (Freestyle or edge): structure guides for models that take a video or structure reference.
   - `clay.mp4`: the motion reference.
5. **Generate** through `engines/ai-clip.md`. Mode depends on the model:
   - keyframe (first + last)
   - video-to-video with the structure reference
   - motion reference

   The credit gate applies.
6. **Coverage for free:** render the *same* blockout from a second camera. AI shots made from both angles cut together because the geometry is identical.

## Dance and performance reference
**Rights first:** use only footage the user filmed, owns, or has permission for. No celebrity likeness, and no copying of a named choreographer's routine as the selling point.

| Goal | Route |
|---|---|
| One character mimics a dance clip | Higgsfield `hf_mult_motion_control`: the motion video plus a character image. Fastest. |
| Exact choreography, custom camera, several angles | Video → mocap: **FreeMoCap** (open source) or **Rokoko Vision** free tier (30 s/month). Then BVH/FBX → retarget onto a rigged character (Mixamo auto-rig, or the project mesh) in Blender → clay render with the beat-locked camera → motion reference for AI, or the final render itself in a 3D look. |
| Stylised dance in code (three.js) | Load the retargeted GLB and drive its animation mixer with `t`. Deterministic, no credits. |

**Choreo on the beat:**
- Snap the key poses (hits, freezes) to beats by retiming the action in Blender's NLA. Clean mocap is not on beat on its own.
- On the clay render, check foot contacts (no sliding) and hand-face intersections before any generation.

## Real footage → 3D → animate (the "recreate then move" trick)
When the user has a real location clip or photo and wants impossible camera moves through it:
- **A few photos:** blockout from the photo (match the horizon and vanishing points, fSpy-style), project the photo onto the blockout as a texture (camera projection), and move the camera within about 15° of the original view.
- **A walkthrough clip:** go to `engines/recreate.md` to rebuild it properly, then animate.
- **A gaussian splat or photogrammetry** of the location, when available: import it, and use it as the blockout and depth source.

## Checks
- Show the clay animatic with the song before any credits.
- After generation, compare the AI clip with the clay frame at 3 matched times. Composition and camera must match within a few percent of the frame. Drift there means the guide wasn't used, so change the mode, not the prose.
- Feed the gates in `engines/ai-clip.md` (inspection) and the hub (`film_gate.py`).
