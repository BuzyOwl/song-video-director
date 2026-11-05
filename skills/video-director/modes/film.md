# Film mode (animated short, cinematic sequence, cutscene, narrated story, product film)

For story pieces driven by a script, voiceover or score rather than a finished song. A song-led story goes to
`modes/music.md`; it can still borrow this file's blocking flow.
Directions unless tagged **Fact** (measured bug) or **Safety** (hard rule 1); a piece may break a direction with one line
in its STYLE.md.

## The five questions (one message; skip any already answered)
1. In one line: whose story, what changes, what should a viewer feel at the end? [I'll draft it from the script]
2. Length and format? 16:9 / 9:16 / both. [60–90 s, 16:9]
3. Sound? Your voiceover / a score or song / AI voice (costs credits) / silent with SFX. [your VO]
4. Picture source? Code 3D (three.js) / 2.5D from your art (Remotion) / AI clips guided by blockouts / Unreal or Blender. [code 3D]
5. How do you want to direct? Shot by shot with me (blocking first, slower, you decide every shot) / I plan it all, you
   review stills. [shot by shot]

Reply with the numbers you want to change, or "go".

## 1. Script → beats → shot list
- Beat sheet and spine first (`craft/story.md`). Then the shot list table from that file.
- **Sound is the clock.** Record or generate the VO / score first and build the timing map on it (`craft/timing.md`
  section 2 works for spoken onsets too; a VO word lands visuals the same way a sung word does).
- STYLE.md decides **continuous camera** (one-take, push-into-shape transitions) or **coverage cutting** (180°, match
  cuts). Write which at the top.

## 2. Blocking first (`craft/blocking.md`)
- Whole piece blocked with stand-ins on the real sound, as data, before any detail.
- Shot by shot with the creator when they chose it: question first, build their words literally, one shot per round.
- Camera rules and the variety pass: `craft/camera.md`. Motion: `craft/motion.md`.
- Sign-off writes a scene spec and freezes the scene's data.

## 3. Build the look on locked paths
- Each scene (or a subagent / worker session per scene) builds from its spec and imports paths read-only.
- Light and materials: `craft/light.md`. Engines: `engines/code.md`, `engines/ai-clip.md` + `engines/guide-3d.md`.
- More than one worker: `craft/team.md` (verbatim relays, note checklist, review page).

## 4. Render, check, review
- `craft/render.md` for drafts vs finals, muted render + WAV mux, BT.709, frame-exact joins.
- Front-door gates and the independent review apply as for every mode. Post every draft to the review page with known
  issues on top.

## 5. Deliver
Final + a 9:16 cut-down if asked (re-lay out by default; crop on the subject only when the frame survives it), the beat
sheet and shot list in `docs/`. **Safety:** honest credits, AI parts credited and the platform's AI box ticked per its
rule, `CREDITS.md` for every external asset.
