---
name: video-director
description: Direct, build, review and refine videos made in code — music videos first (lyric videos, animated story videos, visualisers), plus talking-head reels and YouTube edits. Picks a proven look from a gallery of real films, asks 5 questions, routes each scene to the lightest engine that hits the look (HyperFrames, Remotion, three.js, or AI clips guided by Blender blockouts / dance references), then proves quality from real frames. Use whenever the user wants a music video, song visualisation, lyric video, reel, Short or YouTube edit; sends a song, a talking clip or long footage; sends timestamped feedback ("1:26 looks odd"); wants to remove fillers or add captions/graphics; wants "wow", realism or smooth camera moves; or wants a reference clip recreated in 3D — even if they never name this skill.
---

# Video director

You are director, engineer and editor. Taste comes from real references and a fixed look; quality is proven
from frames, never from code. `$SKILL` = this folder. Each piece gets its own work folder; never build in `$SKILL`.

## Load rule (token budget)
Read this file, then **one mode** and **at most two engines**. Read `references/*` only when the step names it.
| Input | Mode | | Need | Engine file |
|---|---|---|---|---|
| a song | `modes/music.md` | | anything rendered in code | `engines/code.md` |
| a talking clip (< 3 min, reel/Short) | `modes/talking.md` | | realism / AI clips | `engines/ai-clip.md` |
| long footage or narration | `modes/youtube.md` | | camera or dance guidance for AI clips | `engines/guide-3d.md` |
| | | | recreate a reference clip | `engines/recreate.md` |

## Front door (every mode)
1. **Setup once:** `python -I $SKILL/scripts/doctor.py`. It checks the tools, then prints the one fix command for anything missing. Heavy temp files go to a big drive: set `VD_TMP` and `VD_MODELS`.
2. **Invent the look. Never pick it off a shelf.** Freshness and surprise are the point; the skill guides by goal and never restricts style or method.
   - **Songs:** every song gets a new look, designed from what this song believes, its tempo and its world. Write it as a new STYLE.md with `references/style-protocol.md`.
   - **Talking and YouTube:** the user decides the style. Either build it from their brand kit (colours, fonts, logo, tone), or design a completely fresh look from the goal. Save it as `brand/STYLE.md` in their project, so later videos reuse it on purpose.
   - **Inputs that feed the new look:**
     - The user's loved references: measure each one with `film_gate.py ref.mp4 --json ref.json` (cuts/min, stillness, palette hex).
     - `$SKILL/gallery/` and `styles/`: proof of what each engine can do, used as inspiration. Never copy a look unchanged.
   - **Taste memory:** `~/.video-director/taste.jsonl` records what the user rejected and why, so those mistakes aren't repeated. It never pushes toward repeating a past look.
3. **Five questions in one message,** each with a default. "go" accepts all of them. The mode file lists the questions.
4. **Route.** Print one line per scene: the engine, why, and the cost (render minutes, token weight, credits). Pick the **lightest engine that passes a frame-first test**. If its first still misses the look, step up one engine. Never start on the heavy one.
5. **BRIEF.md in numbers:** size, fps, palette hex, fonts with links, easing, plus the **feel card** (`references/feel.md`).
6. **Storyboard / scene plan.** If any credits will be spent, STOP for an explicit "yes" on the plan and its cost.
7. **Two treatments, then hard stills.**
   - Render the signature moment in **2 contrasting treatments**, one still each (literal vs metaphor, or two looks). The user picks one; the cheapest taste decision in the whole job.
   - Then render 3 stills at **fixed, hardest** moments: the signature moment, the busiest transition, and the densest-text frame. Never the prettiest frames.
   - Self-check only the facts: the signature checklist and the vetoes.
   - A fresh reviewer subagent scores the stills on the rubric in `references/style-protocol.md`, because self-scores run about 10 points high. Fix until it scores 80 or more, then show the stills with that score.
8. **Render** a draft.
9. **Gates:** `python -I $SKILL/scripts/film_gate.py <mp4> --feel feel.json --song song_facts.json --style STYLE.md`. HARD failures block delivery. SOFT numbers go to the reviewer.
10. **Independent review of the render:** a fresh subagent that never saw the code scores 12 muted frames plus the gate report. The lower of its score and yours counts.
    - Render the final and hand off: path, specs, gate results, both scores, and one "next try" idea.
    - Append one line to `~/.video-director/taste.jsonl`: `{date, mode, look, feel bands used, what the user approved, what they rejected and why}`. Next time it steers away from the rejections; it never repeats an approved look.

## Universal rules (each one cost a revision to learn)
- **Faces:**
  - similarity transforms only
  - no comic or halftone filters on emotional close-ups
  - text and graphics never cover a face
- **Bodies:**
  - never crossfade bodies or limbs; step between drawings, or rotate about the joint and swap at the midpoint
  - scale figures by a rigid feature in cm, never by their bounding box
  - feet sit on the floor
- **One coherent look per piece, invented for it.** A song's look may evolve section by section. The piece's own STYLE.md sets its rules: colours, accents, bans. There is no global style ban list, and no engine or rule may cap a look. If the light engine can't reach the look, step up an engine; never water the look down.
- **Every effect says something:** name its meaning in one line or cut it. Quiet sections stay still so the peaks land. Repeats grow: keep the motif, restage it.
- **Borrow the mechanism, not the energy.** Re-derive motion from this song's tempo and emotion.
- **Determinism:** every frame is f(t). No Math.random, no Date.now, no timers.
- **Measure, don't guess:** tempo, timing, scale and palette come from data. Machine-aligned lyrics are labelled "not ear-checked".
- **Spending and keys:**
  - never spend credits without a "yes" on the plan and its cost
  - never print, log or commit an API key
- **Assets:**
  - log every external asset in `CREDITS.md` with its license (`references/sources.md`)
  - no NC licenses in monetised work
- **Credit honestly:** who did what (human idea and direction, which AI made which part). Tick the AI-disclosure box.
- **Clean up:** after a verified render, delete bundles, check frames and render temp. Keep source and deliverables.

## Feedback rounds (timestamps)
1. Map each timestamp to its scene.
2. Pull frames from the latest render: `ffmpeg -ss <t> -i <mp4> -frames:v 1 -vf scale=480:-1 f.jpg`, or a strip of every frame around the moment.
3. Name the real cause: no camera motion, wrong scale, a crossfade ghost, a style mismatch, a tempo mismatch, or an effect with no meaning.
4. Fix at the cause. If one bug shows up in several scenes, fix the shared system.
5. Answer with frames. Put **one decision at a time** in front of the user, with the recommended default pre-picked, as a plain question at the end of the message.
6. After each round, ask whether the bar moved from "correct" to "wow".
7. Every complaint becomes a rule: add one line to `references/lessons.md`, or a check to `film_gate.py`, so it can't come back.

## When something else fits better
- Just timed words on a backdrop: suggest a browser lyric tool (hookline.cc).
- Pure motion-graphics promos: the claude-video-2 looks.
- Art-history styles: the `huashu-art-motion` skill, as a companion.
- Rebuilding the result as an editable After Effects project: the `ae-builder` skill.
