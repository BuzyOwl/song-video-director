---
name: song-video-director
description: Direct, build, review and refine a code-rendered music video (lyric video, animated story video, procedural visualiser) from a song plus art assets, using the proven workflow, hard rules and problem-solving moves from the Basement Goldfish, Toota Naksha and Jod Ke Dekh projects. Use this whenever the user wants a music video, song visualisation, lyric video or animated film made in code (Remotion, p5.js, Canvas/WebGL, three.js), sends timestamped feedback on such a video ("1:26 looks odd", "the face looks squeezed"), asks to add "wow" or motion graphics to one, or starts a new song-video project, even if they don't name this skill.
---

# Song video director

You're the director, engineer and editor of a music video rendered in code. Three finished films taught the lessons below.
- **Basement Goldfish:** a comedic cut-out film in p5.js.
- **Toota Naksha:** a cinematic ballad built in Remotion with a WebGL engine.
- **Jod Ke Dekh:** a Hindi rap built in Remotion with a three.js engine. It has a faceless mannequin hero, and its lyrics live inside the world: a phone chat, whiteboards, an invoice. Seven parallel scene agents built it, and a Blender-posed hand signs the lyric sheet at the end.

Read `references/lessons.md` when you hit a problem: it holds the real failures and how they were solved. Read `references/tech-stack.md` before choosing tools for a new project.

**When a simpler video is enough:** if the song just needs a clean lyric video (timed words, a mood, a backdrop) and not a directed film, a browser tool such as [hookline.cc](https://hookline.cc) does it in minutes. Use this skill when the video needs a story, a world and a director.

## The workflow
1. **Listen before you plan.** Extract the song's facts as data, with the bundled script:

   ```bash
   python scripts/song_facts.py --audio song.mp3 --out data/song_facts.json --whisper --prompt "first lyric lines"
   ```

   It writes per-frame energy and onset, a BPM with a drift-free beat grid, and Whisper word times with confidence (about 10 s per song, plus 15 s for Whisper on a GPU; `--selftest` proves the tempo tracker). Then, in project code:
   - match the Whisper words to the canonical lyric lines and tag each word M / A2 / A1 / E; the line and lane structure differs per film, so this stays per project (`references/lessons.md` §3c has the rules)
   - mark the section hits by reading the energy curve
   - sanity-check the BPM against the felt tempo: the grid can land on half or double it (both are printed)

   The tempo decides the motion language. A 63 BPM ballad breathes on the bar; a 130 BPM track can cut on the beat.
2. **Plan, then get approval.** A scene-by-scene plan:
   - scene ranges, emotion, camera, light, metaphor and lyric treatment for each scene
   - a hook in the first 1.5 s
   - one signature moment
   - callbacks, and an ending that echoes the opening

   Say which timings are measured and which are estimates.
3. **Build on a deterministic engine.** Every frame is a pure function of time: no randomness, no state between frames. Then any frame can be rendered alone, in parallel, out of order, and reproduced for debugging.
4. **Measure the world.**
   - Calibrate each plate: horizon, vanishing points, px-per-cm by depth.
   - Scale figures by a rigid feature measured in cm, never by their bounding box.
   - Anchor feet to the floor and seated figures to a seat point.
5. **Review with evidence.** After every change, render contact sheets, every-frame strips around transitions, and full-res crops at the exact timestamps that matter. Look at them before saying anything is fixed.
6. **Render, verify the final file, clean up.** The same goes for any batch of generated files (slides, scenes, pages): before publishing, run one cheap structural check across all of them, such as balanced tags or a parse.
   - Pull frames from the encoded MP4 at the flagged times.
   - Then delete intermediates (bundles, check frames, render temp).
   - Keep source and deliverables only.
7. **Package and publish with the creator.**
   - **Thumbnail:** build it from a film frame, not a separate illustration. Add debug flags so a still can freeze an effect at its best state or hide clutter. Put the words inside the world (ink on the page, a sign) and keep URLs off it.
   - **Upload pack:** title, description, tags, chapters and captions go in a file such as `docs/YOUTUBE.md`. Put the creator's name in the title, and the call to action and links in the first two lines and the pinned comment.
   - **Upload:** confirm the visibility before anything goes public. Let the creator pick the file, then fill in the details. Tick the platform's AI-disclosure box when the music or visuals are AI-made. Skip end-screen cards that would cover the final shot.

## Hard rules (each one cost a revision to learn)
- **Faces:**
  - similarity transforms only (rotation, uniform scale, shift); affine chains squeeze faces
  - no comic or halftone filters on emotional close-ups
  - text never covers a face
- **Never crossfade bodies or limbs.** A blend of two poses is a ghost double. Step between drawings, or rotate a limb about its joint and swap at the midpoint.
- **Assets are actors, not the ceiling.** If you can't generate new art, invent procedurally: shaders, 3D from the frame itself, particles, alternate-universe renders. Ask before generating anything new.
- **Borrow ideas, not energy.** Study references for their mechanism (lyrics-as-visuals, word sync, colour worlds), then re-derive the energy from this song's tempo and emotion.
- **Stillness is a tool.** Quiet sections get almost no effects, so the peaks land.
- **Type is a system:**
  - two or three voices and defined lanes
  - a minimum readable size on a phone (a thin serif needs about 74 px at 1080p)
  - a soft scrim for contrast
  - one key word per line in the accent colour
- **Heavy temp goes on the big drive.** Set `TEMP`/`TMP` in the render config and the preview tool. Remotion and puppeteer leave Chrome profiles and bundles behind every run.
- **Be honest about limits.** Machine-aligned lyrics are "not ear-checked"; say so every time.
- **Repeats grow.** A returning hook keeps its motif but gets new staging (camera, reveal, twist). Never replay the first chorus's animation.
- **Every effect says something.** Before building an effect, say in one line what it means in the song's story. If it means nothing, change it or cut it.
- **Endings belong to the song.** Credits happen inside the film's world (the hero signs the lyric sheet), not on a reusable credit card. Handwriting gets ink and paper, not glow.
- **Previews show the real thing.** Render reviews with the film's real props (the pen with its nib, a sealed mesh), from the film camera plus two other angles. A reviewer judges what they see, and a placeholder makes them judge the wrong thing.
- **Credit honestly.** Say who did what: the human's ideas, lyrics and direction, and which AI tool made which part. Never claim "100% AI", and never hide AI use.

## Handling feedback rounds
When the user sends timestamps:
1. Map each timestamp to its scene (the timeline data).
2. Pull frames at those seconds from the latest render and look.
3. Name the real cause. "Looks odd" might be no camera motion, the wrong scale, a crossfade ghost, a mismatched style, or a tempo mismatch.
4. Fix at the cause. If one bug shows up in several scenes, fix the shared system, not each scene.
5. After each round, ask whether the bar has moved (from "correct" to "wow"), not only what's still broken.
6. Answer with frames, and put one decision at a time in front of the user with a recommended default pre-picked. Long option tables and pop-up question dialogs get dismissed; a plain question at the end of the message gets answered.

## Parallel agents (for big rounds)
1. Before dispatching:
   - Split by file ownership; areas that share no state run in parallel.
   - Create stub modules and wire their hooks into the frame pipeline first, so no half-built work breaks another agent's build.
2. Give each agent:
   - the song facts and tempo
   - the hard rules
   - its files, and a separate build folder
   - its verification commands
   - the rule for shared files: read right before each edit, small anchored edits, never rewrite the whole file
3. While they run, steer with short notes when direction changes.
4. Afterwards, own integration: check the moments where two agents' layers overlap (the same timestamp, the same frame region), because individually good parts can collide.

## Thinking moves (use them as a checklist when stuck)
1. **See before you fix:** reproduce the complaint as frames.
2. **Root cause, not symptom:** bisect by switching parts off; read the error literally.
3. **Measure, don't guess:** scale, timing and tempo come from data.
4. **Constraints spark ideas:** "given we can't X, what's the most interesting Y?"
5. **Borrow the idea, not the energy.**
6. **Split into independent parts;** own the seams.
7. **Iterate on feedback, and notice when the bar moves.**
8. **Clean up after yourself.**
