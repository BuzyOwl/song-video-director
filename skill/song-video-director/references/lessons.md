# Lessons from three procedural music videos

Sources:
- **Basement Goldfish (BG):** a 3:31 comedic indie track, about 132.5 BPM. Built with p5.js and p5.brush cut-out puppets in three rounds, plus four vertical Shorts.
- **Toota Naksha (TN):** a 3:53 Hindi ballad, about 63.5 BPM. Built with Remotion and a custom Canvas2D/WebGL2 engine over six versions, using up to five parallel agents.
- **Jod Ke Dekh (JKD):** a 4:12 Hindi rap about generalists, 100 BPM. Built with Remotion and a three.js engine by seven parallel scene agents over eight versions. It ends with a Blender-posed hand signing the lyric sheet, and it was published by the agent with the creator.

Each lesson follows one shape: **problem → first instinct → real cause → fix → thinking move**. The thinking move is what transfers to the next project, and to problems that have nothing to do with video.

## Contents
1. See before you fix
2. Root cause, not symptom
3. Measure, don't guess
4. Constraints spark ideas
5. Borrow the idea, not the energy
6. Split the work into independent parts
7. Iterate on feedback, and know when the bar moved
8. Clean up after yourself
9. Architecture lessons (the quiet ones)
10. The third film: Jod Ke Dekh

---

## 1. See before you fix
The film is the evidence. Opinions about the film are not.

**1a. Timestamped feedback → exact frames (TN, every round).**
- **Problem:** the user writes "1:26–1:33 looks odd".
- **First instinct:** guess which code is responsible and start changing it.
- **What worked:**
  1. Map each timestamp to its scene in the timeline.
  2. Pull the actual frames from the rendered MP4 at those seconds.
  3. Tile them into one contact sheet and look.
- **Result:** the frames showed what words couldn't. One shot of SC15 was a static wide, she was tiny in frame, and nothing moved.
- **Move:** *reproduce the complaint before you touch the code.*

**1b. The review loop as a tool, not a chore (BG).**
- BG's render tool has three views, each answering a different question:
  - **contact sheet:** the shape of the whole piece
  - **strip:** every frame of one moment
  - **crop:** full-res detail of hands, faces, contacts
- TN rebuilt the same idea as `tools/sheet.mjs`.
- **Move:** *build the instrument that lets you see the problem, once, then use it constantly.*

**1c. "Done" means verified in the final artifact.**
- Every TN version was checked by pulling frames out of the encoded MP4, not just previews.
- The previews and the encode can differ (bundling, timing, codec).
- **Move:** *verify the thing you ship, not a proxy for it.*

**1d. The slide that wouldn't open (the masterclass deck itself).**
- **Problem:** 23 slides were hand-written from one repeated template and published without any check. One slide (`m5r`) opened read-only: "div opened at 6:1 was never closed".
- **Real cause:** while editing one copy of the template, a single closing `</div>` was dropped.
- **Fix:**
  - added the missing tag
  - counted opening and closing tags in *every* slide; one shell loop took about 10 seconds
  - only that slide was broken
- **Move:** *when you produce many near-identical files, run one cheap mechanical check across all of them before shipping; repetition is where slips hide.*

---

## 2. Root cause, not symptom
The symptom is where the problem shows up. The cause is where it starts. They are rarely the same place.

**2a. The milky film (TN v5).**
- **Symptom:** every frame looked washed out, as if a peach fog lay over it.
- **First instinct:** "the bloom is too strong", so turn it down.
- **Investigation:** switch the five post-processing passes off one at a time (debug flags `poff1..5`). Bloom alone caused it.
- **Real cause:** a scripted edit had put a `//` comment in the middle of a line. That silently commented out the `drawImage` that fills the bloom buffer. A multiply-tint on the *empty* buffer turned it solid peach, which was then screened over everything.
- **Turning it down would have hidden the bug forever.**
- **Move:** *bisect: turn things off one by one until the symptom disappears, then read that one piece closely.*

**2b. The render that died (TN v5).**
- **Symptom:** `ENOSPC: no space left on device` at frame 0.
- **First instinct:** "Remotion is broken", so retry.
- **Real cause:** C: had 0.58 GB free. 222 leftover Chrome profiles (7.8 GB) from earlier preview renders were piling up in the temp folder.
- **Fix:** redirect temp to D: in the project config, then delete the leftovers.
- **Move:** *read the error literally. "No space" means no space; ask where the space went.*

**2c. Squeezed faces (TN).**
- **Symptom:** in some close-ups her face looked slightly squeezed or stretched.
- **Real cause:** each head image was aligned to the next with an *affine* fit (which allows shear and non-uniform scale). Chaining nine of them let small distortions add up.
- **Fix:** project every transform to a *similarity* (rotation + uniform scale + shift only).
- **Move:** *ask which freedom in your tool allowed the bad result, and remove that freedom.*

**2d. Ghost arms (TN).**
- **Symptom:** a reaching arm showed two semi-transparent arms mid-move.
- **Real cause:** crossfading between two arm drawings. Any blend of two poses is a double exposure.
- **Fix:**
  - rotate the arm about the shoulder socket between neighbouring drawings
  - swap drawings at the midpoint
  - never blend limbs
- **Move:** *if the technique itself produces the artifact, tuning won't fix it; change the technique.*

**2e. The miniaturised girl (TN) and the tiny plumber (BG).**
- **Symptom:** characters at the wrong size next to furniture and sets.
- **Real cause:** figures were scaled by their image bounding box, which carries no physical meaning.
- **Fix:** a scale engine (see §3a).
- **Move:** *when the same bug keeps coming back in different scenes, the cause is in the system, not the scene.*

**2f. Floating feet (BG).**
- **Symptom:** the plumber floated slightly above the basement floor.
- **Real cause:** the background plate was drawn at 1.18× overscan, but the floor line was measured on the unscaled image.
- **Move:** *when two numbers should match and don't, check what each one is measured against.*

---

## 3. Measure, don't guess

**3a. Real-world scale.**
- **BG:** measured each set from known objects:
  - an alley doorway → about 2.6 px/cm
  - the basement doorway → about 3.9 px/cm
  - an 18 cm stair riser

  Then every object got a real height: man 178 cm, chair 92, crate 60, jar 26, fish 11.
  - Result: he can never be smaller than the jar.
  - Cartoon exaggeration is allowed only in the imagined chorus collages.
- **TN generalised it:**
  - every plate has a horizon and vanishing points, so `pxcm(y) = a·(y − horizon)`
  - figures carry their own cm-per-px, measured from a rigid feature like the ear, never from the bounding box
  - seated figures anchor on a seat landmark
- **Move:** *convert taste problems into measurement problems wherever you can.*

**3b. Audio is data.**
- **BG:** measured loudness and onsets per frame, and detected a beat grid of about 132.5 BPM.
- **TN:** measured per-frame energy and low-band kick, and found the section hits (2.5, 48.5, 80.0, 124.3, 155.4, 183.0, 216.0 s).
  - The "breakdowns" were confirmed by measurement: energy about 0.55, zero kicks.
- Every effect that pulses, swells or cuts reads from this data, so motion follows the actual song.
- **Move:** *don't invent timing; extract it from the source.*

**3c. Say what you don't know.**
- Lyric timing was machine-aligned (Whisper large-v3, two independent passes) and tagged by confidence:
  - **M:** measured
  - **A2:** two passes agree ≤ 0.3 s
  - **A1:** single source
  - **E:** estimate
- BG reported "282 words agree within 0.35 s, 10 words have no time".
- Every deliverable said "machine-aligned, not checked by ear".
- **Move:** *confidence labels are part of the answer; a confident wrong answer costs more than an honest maybe.*

---

## 4. Constraints spark ideas
- **"No new generated assets"** (TN brief). Everything new had to be procedural, and that pushed the film's best ideas:
  - the crease net that cracks the map
  - kintsugi amber seams
  - 3D paper shards cut from the frame itself
  - GPU particle depth
  - "alternate universe" shaders (a mosaic of the lyric's own letters, a living map, a comic print)
- **"The tea-giver stays unseen."** So: only a hand and steam enter the frame. The mystery became a strength.
- **"Reflections are composited, never flipped."** So the outside-looking-in shot was skipped rather than faking a mirrored figure.
- **BG: one basement image, two moods.**
  - The warm basement is the *same* cold plate through a colour map, so cracks and windows never move between moods.
  - The code-drawn eye replaced a blink sheet, so the eye shape stayed consistent.
- **The user's reframe (TN):** "these are assets, that does not mean you can't create alternative-universe styles." The assets are actors; they are not the ceiling.
- **Move:** *treat each constraint as a design prompt: "given that we can't X, what's the most interesting way to Y?"*

---

## 5. Borrow the idea, not the energy
**The LGTM study (TN).** The user's benchmark was a viral AI music video, a comedy track at about 120 BPM. We studied it frame by frame. What made it work:
- lyrics *are* the visuals (each line is a visual pun)
- word-by-word sync
- a new idea every 2–4 s
- one colour world per section
- callbacks
- in-world credits

**Then the user's correction:** "be mindful of our song tempo… strike an emotional chord."
- TN is a 63.5 BPM ballad: beat 0.945 s, bar 3.78 s.
- So we kept the *ideas*: a visual metaphor per line, word sync, an amber key word.
- And translated the *energy*:
  - motion breathes on the bar
  - words bloom through held vowels
  - slow-motion hero moments
  - 49 EDM-style camera punches became about 15 gentle pushes
  - beat flips became rare and story-driven
- **BG had already proved the inverse.** "The bridge has no beat effects at all. That stillness makes the final chorus land."
- **Move:** *separate what a reference does (the mechanism) from how it feels (the energy); copy the first, re-derive the second from your own material.*

---

## 6. Split the work into independent parts
- **Five parallel agents (TN v5, v6).** One each for:
  - 3D shards
  - particles
  - shader universes
  - typography
  - lyric metaphors

  Later, four more for the opening, the reach, the portal and the close-ups. It finished in about one hour per round instead of five.
- **What made it work:**
  - **File ownership:** each agent owned specific files; shared files had a rule: read right before every edit, small anchored edits, never rewrite the whole file.
  - **Stubs and hooks first:** the coordinator created empty modules and wired them into the frame pipeline *before* dispatching, so no agent's half-built work broke another's build.
  - **Separate build folders** per agent.
  - **Steering mid-flight:** when the tempo insight arrived, short direction notes went to all running agents.
  - **Integration is the coordinator's job:** individually good parts can collide. The particle "warp" and the 3D shards both fired at the 183 s drop; together they were cluttered, so the coordinator thinned one.
- **Move:** *divide along boundaries where parts don't share state, make the seams explicit before work starts, and own the integration yourself.*

---

## 7. Iterate on feedback, and know when the bar moved
- **Six TN versions:**
  - **v1–v4** fixed correctness: scale, seams, ghosting, squeezed faces, transitions.
  - **v5–v6** answered a *different* question, "make it wow". A clean film was no longer the bar.
- **Recognising the shift mattered more than any single fix.** The user benchmarked against pure-code three.js videos and said "you have so many things yet feel inferior".
- **The hook decides everything.**
  - BG round 2: the first frame became the painted fish face.
  - TN's review flagged "0–1 s black, title at 6 s".
  - v6 opens on a single point of light on a map crease, and the title lands on the 2.5 s hit.
- **Callbacks and loops make a piece feel designed:**
  - BG: the scrap the fish rejected twice becomes its crown, and the film ends on the same eye it opened with.
  - TN: SC17's window portal exits through the train window it entered from.
- **Make feedback cheap for the person giving it.** Accept timestamps, answer with frames, one decision at a time with a recommended default.
- **Move:** *after each round, ask "what is the bar now?", not just "what is still broken?"*

---

## 8. Clean up after yourself
- **The cost of not cleaning:** a full system drive and a failed render (§2b).
- **The fix became policy:**
  - heavy temp lives on the big drive (`TEMP` set in the project config)
  - each verified render deletes its intermediates (build bundles, check frames, render temp)
  - only deliverables and source are kept
  - anything that isn't our own regenerable output needs the owner's OK before it goes
- TN's `out/` folder went from 8.6 GB to 1.95 GB after v6.
- **Move:** *leave the workspace better than you found it; resources you don't own are borrowed.*

---

## 9. Architecture lessons (the quiet ones)
- **Every frame is a pure function of time** (both projects).
  - Same `t` → same pixels; no randomness, no state between frames.
  - Frames can render in parallel, out of order, and any single frame can be reproduced for debugging.
  - BG: "the order is derived from song time, so jumping into the middle never brings eaten food back."
- **Data drives the film.**
  - Shots start 0.25 s before their lyric cue, so moving a cue moves its shot.
  - Swapping a character means editing one pose table and re-running the cut-out tool; the scene code doesn't change.
- **Type is a system, not decoration** (TN director review). The first cut had:
  - text in six lanes
  - chorus text smaller than the verse
  - a 48 px serif that turned to mush on phones

  The fix was three voices, defined lanes, a 74 px minimum for the serif, and a soft scrim for contrast.
- **Faces are sacred:**
  - similarity transforms only
  - no comic filters on close-ups (they drop the emotion)
  - no crossfaded heads
  - text never covers a face

---

## 10. The third film: Jod Ke Dekh
Each lesson names the thinking move it belongs to.

**10a. Lyrics in two scripts (move 3: measure, don't guess).**
- **Problem:** a Hindi rap full of English words. Whisper writes some English words in Devanagari and some Hindi words in Roman script. The user also sent their own list of word start times.
- **First instinct:** trust Whisper, or trust the list.
- **Real cause:** words written in different scripts never string-match. Whisper also snaps a word too early when it comes right after a pause.
- **Fix:**
  1. Merge the two sources.
  2. For a word that won't match, use the "sandwich" rule: place it between its matched neighbours.
  3. When the two sources disagree, break the tie with the voice onset in the audio.
  4. For display, show English words in Roman script and Hindi in Devanagari, using a small map.
- **Result:** 535 of 596 words agreed within 0.3 s.
- **Move:** *two independent measurements, reconciled by a third signal, beat one source you trust blindly.*

**10b. "Same same but different" (move 7: notice when the bar moves).**
- **Problem:** the creator wrote: "1:20–1:37 animations are the same as 3:23–3:37."
- **First instinct:** reusing the scene for the second hook is efficient.
- **Real cause:** in music, a repeat is a promise of growth. When the picture repeats exactly, the viewer reads it as lazy.
- **Fix:** keep the motif (the thread, the hook words) and restage it. The second hook got new cameras and a twist on the beat, and it ends on a reveal: the campus itself spells the word.
- **Move:** *a repeat should grow; keep the idea, change the staging.*

**10c. The metaphor beat (move 5: borrow the idea, not the energy).**
- **Problem:** the crown scene showed the hero winning a crown. The creator asked: "what if he got the crown but left it?"
- **Real cause:** the scene illustrated the words, not the song's stance. A generalist refuses the single title.
- **Fix:** stage a choice. He reaches the crown, looks at it, and walks on.
- **Move:** *ask what the song believes, then stage that belief as an action.*

**10d. The credit card (move 4: constraints spark ideas).**
- **Problem:** the credits were a glowing type card. Feedback came in three rounds: "glow is too much", then "make it a paper sketch", then "the outro will be different for every song: make it the generalist signing the song sheet".
- **First instinct:** build one reusable credits template.
- **Real cause:** credits are the last scene of the story. A template stands outside it.
- **Fix:** the camera tilts down to the lyric sheet on the desk. A hand writes the credits glyph by glyph with an ink pen, strikes through the old alias, and inks a small ∞ for the channel. The song's beat loops underneath.
- **Move:** *the ending belongs to this song; echo the film's own world.*

**10e. The hand that wouldn't look right (moves 1 and 2).**
- **Problem:** a hand built from primitives and metaballs looked weak. The real rigged mesh then had fingers "falling down". Then "the 3rd shot is not working: the 3 fingers on the right look odd".
- **First instincts:**
  - tweak the joint angles by eye
  - judge only from the film camera
- **Real causes:**
  1. Primitives can't carry anatomy.
  2. The pose search was rewarding fingers that touch the paper, so it chose straight fingers dangling like legs. The objective function was the bug.
  3. The previews used a plain cylinder for the pen and showed the mesh's open forearm. The reviewer reacted to those ("pen is missing the nib", "hollowness"), not to the pose.
- **Fix:**
  1. Use the creator's rigged hand mesh and a headless Blender script (`blender -b -P`). It rigs the mesh, poses a tripod grip and fits the pen through the three finger pads.
  2. Search wrist angle, roll and curl against anatomy: index on top, thumb opposite, ring and little fingers folded into the palm, the hand hovering on its pinky edge, the nib visible from the film camera.
  3. Render previews in the film's own frame, with the real pen silhouette and the arm, from three angles. Seal the mesh's open end.
- **Move:** *when an optimiser picks something ugly, read what you rewarded; and show the reviewer the real thing.*

**10f. An effect has to mean something (move 5).**
- **Problem:** the creator wanted "the skin texture revealed slowly as he writes". The first build went from clay to skin. The creator replied: "clay is not needed, it's skin taking over the model."
- **Real cause:** clay meant the mannequin, which is a different story. The meaning wanted here is a 3D model (made by the machine) becoming human, which is human + AI.
- **Fix:** a viewport-grey model with its quad wireframe showing. Real skin spreads over it from the fingertips to the arm. The same half-model, half-skin frame became the thumbnail.
- **Move:** *name what the effect says before you build how it looks.*

**10g. Honest credit and a findable creator (move 7).**
- **Problem:** the first thumbnails said "100% AI-made" and "No camera. Only code." The creator answered: not 100% AI; made in part with AI, using my AI knowledge. They want people to find them and ask them to teach.
- **Fix:**
  - The description has a "who did what" list: the creator's concept, lyrics and direction, Suno for the song, the coding agent for the frames.
  - The creator's name goes in the title.
  - The thumbnail is a film still, frozen half model and half skin with debug flags, and only the name on a clean sheet. "ME + AI" and the title are inked on the page.
  - The creator's platform link goes in the description and the pinned comment, never on the thumbnail.
  - The AI disclosure is ticked, because the music is AI-made.
- **Move:** *the audience and the creator's goal are part of the brief; credit honestly.*

**10h. Seven agents, one film (move 6: split into independent parts).**
- Each scene agent worked in its own copy of the project. The copies were made by a script, with junctions to `node_modules` and `public` so nothing was duplicated, and each agent owned one scene file. The coordinator owned the scene table and transitions, and the bookend.
- Integration still found the seams:
  - lyric text mirrored in a reflective floor (fixed with render layers)
  - a wall line clipped in one shot
- **Move:** *isolate the builds, then own the seams.*

**10i. Small tools, sharp edges (move 2: read the error literally).**
- The still renderer split its arguments on `=`, so `--debug=front=0.1` arrived as `front`. Use a different separator (`front:0.1`).
- Inline heredocs and `sed` on Windows ate quotes and regex backslashes. Write patch scripts to files, or use an exact-match edit tool.
- Blender 5.2's glTF exporter has no loose-edges option. Export wireframe lines as a small JSON of segments instead.
- three.js 0.186 removed `PCFSoftShadowMap`. A motion-blur average comes out dark unless the averaging pass renders with `autoClear = false`.
- A `t`-dependent infinite loop (a maze path with a dead end) hangs Remotion at "waiting for the page to render". Guard every search loop.
- **Move:** *when output is mysteriously wrong, check what actually reached the code.*
