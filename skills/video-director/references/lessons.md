# Lessons: what went wrong, the real cause, the fix

These come from:
- **BG:** Basement Goldfish, p5.js
- **TN:** Toota Naksha, Remotion + WebGL
- **JKD:** Jod Ke Dekh, three.js
- the talking-head reels

Read this when you're stuck. Each lesson's last line is the transferable move.

**Every new user complaint adds one line here, or one check to `film_gate.py`.**

## See before you fix
- **"1:26 looks odd" (TN).**
  - Cause: a static wide shot, with the hero tiny in frame.
  - Found by mapping the timestamp to its scene, pulling the frames and tiling them.
  - *Reproduce the complaint as frames before touching code.*
- **Review instruments (BG/TN), each answering one question:**
  - the contact sheet: the shape of the whole piece
  - the strip: every frame of one moment
  - the crop: hands, faces, contacts

  *Build the instrument once, then use it constantly.*
- **Previews and the encode can differ** in bundling, timing and codec. *Verify the shipped MP4.*
- **One of 23 slides didn't open:** a closing `</div>` was missing. *Run one cheap mechanical check across every near-identical file you produce.*

## Root cause, not symptom
- **The milky film (TN).**
  - First instinct: turn the bloom down.
  - Real cause: a stray `//` commented out the `drawImage` that fills the bloom buffer, so an empty buffer was tinted peach and screened over every frame.
  - Found by switching the post passes off one by one.
  - *Bisect; read the one guilty piece closely.*
- **ENOSPC at frame 0 (TN).** 222 leftover Chrome profiles (7.8 GB) were sitting in C:\ temp. Fix: point TEMP at the big drive and clean up after each render. *Read errors literally.*
- **Squeezed faces (TN).** Chained affine fits allowed shear. Fix: project every transform to a similarity. *Remove the freedom that allowed the bad result.*
- **Ghost arms (TN).** A crossfade between two poses is a double exposure. Fix: rotate the arm about its joint and swap drawings at the midpoint. *If the technique makes the artifact, change the technique.*
- **Tiny figures (TN, BG).** Characters were scaled by their bounding box. Fix: a px/cm scale engine. *A bug that recurs across scenes lives in the system.*
- **Floating feet (BG).** The floor line was measured on the un-overscanned plate. *When two numbers should match, check what each is measured against.*

## Measure, don't guess
- **Scale (BG/TN):**
  - Measure each set from known objects (door 2.6 px/cm, an 18 cm riser).
  - Then `pxcm(y) = a·(y − horizon)`.
  - Figures carry their own cm/px, taken from a rigid feature like the ear.
  - Seated figures anchor on a seat point.

  *Turn taste problems into measurement problems.*
- **Audio is data.** Energy, kicks and section hits (TN: 2.5, 48.5, 80.0 … s) drive every pulse and cut. Breakdowns are confirmed by low energy and zero kicks.
- **Confidence labels:** M / A2 / A1 / E on every lyric word, and "machine-aligned, not ear-checked" on every deliverable. *An honest maybe beats a confident wrong answer.*
- **Two scripts (JKD).** Merge Whisper with the creator's start list, place unmatched words between their neighbours (sandwich), and break ties with the voice onset. Result: 535 of 596 words within 0.3 s. *Two measurements reconciled by a third signal.*

## Constraints spark ideas
- **"No new generated assets" (TN)** pushed the film's best ideas: crease nets, kintsugi seams, paper shards cut from the frame itself, shader "universes".
- **"The tea-giver stays unseen"** became just a hand and steam: mystery as strength.
- **One plate, two moods (BG):** the same plate through a colour map, so the geometry never shifts between moods.
- *Ask "given we can't X, what's the most interesting Y?"*

## Borrow the idea, not the energy
- **LGTM study (TN).** We kept the mechanism (a visual metaphor per line, word sync, a key-word accent) and re-derived the energy for 63.5 BPM:
  - motion breathes on the bar
  - 49 punches became about 15 pushes
- **Stillness (BG).** The bridge had zero beat effects, so the last chorus landed.
- **The crown (JKD).** The scene illustrated the words, but the song's stance was refusal. He takes the crown and walks on. *Stage what the song believes.*

## Iterate, and notice when the bar moves
- **TN v1–v4** fixed correctness. **v5–v6** answered "make it wow". *After each round, ask what the bar is now.*
- **The hook decides everything:**
  - BG opens on the painted fish face
  - TN: from 0–1 s of black and a title at 6 s, to one point of light with the title on the 2.5 s hit
- **"Same same" (JKD).** Chorus 2 replayed chorus 1. Fix: keep the motif and restage it (new cameras, a twist, a reveal). *Repeats grow.*
- **The effect has to mean something (JKD).** Clay → skin read as "mannequin". The intent was "machine model becoming human", so: a viewport-grey wireframe, with skin spreading from the fingertips. *Name the meaning before building the look.*
- **Credits (JKD).** A glowing reusable card became a hand inking the credits on the lyric sheet, with the beat looping. *Endings belong to the song.*
- **Honest credit (JKD).** "100% AI" was wrong. The fix: a who-did-what list, the creator's name in the title, the link in the description and pinned comment, AI disclosure ticked.

## Parallel work
- **TN:** 5 agents, then 4 more. About 1 hour per round instead of 5. **JKD:** 7 scene agents built 22 scenes.
- **What made it work:**
  - file ownership
  - stubs wired in first
  - separate build copies
  - short steering notes
  - the coordinator owns the seams

  Two agents' effects both fired on the 183 s drop, so the coordinator thinned one. *Isolate the builds; own the seams.*

## Bodies and props
- **The hand (JKD).**
  - Primitives couldn't carry anatomy.
  - The pose search rewarded fingers touching paper, so it picked dangling straight fingers. *Read what you rewarded.*
  - Previews used a placeholder pen, so the reviewer judged the placeholder. *Show reviewers the real thing, from 3 angles.*

## Calibrating the gates (v2)
- **First film_gate run** failed all five finished films:
  - wipes counted as 1-frame shots
  - slow drift and 12 fps animation counted as "frozen"
  - one title bloom counted as flicker

  Fix: diff against the frame 0.5 s earlier, merge spikes within 0.25 s, and count a flash by its onset. *A gate that fails good work gets fixed, not obeyed.*
- **What the gate still caught** after the fix:
  - a 7 s fully frozen tableau (BG, around 201 s)
  - a 10 s time-freeze where even the mist stopped (Himalayan Vow, around 53 s)

  *Our own films are proof the pipelines work, not the taste ceiling.*

## Tools
- **Windows:** heredocs and sed eat quotes and backslashes, so write patch scripts to files. A CLI that splits on `=` mangles `front=0.1`.
- **three.js 0.186:**
  - `PCFSoftShadowMap` is gone
  - a motion-blur average needs `autoClear = false`
- **Remotion:** a t-dependent infinite loop hangs "waiting for the page". Guard every search loop.
- **Blender 5.2 glTF** has no loose-edge export, so wireframes go out as a JSON list of segments.
- **Cleanup:** TN's `out/` went from 8.6 GB to 1.95 GB once cleanup became policy. Delete only what you regenerate; anything else needs the owner's OK.
