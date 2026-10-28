# Engine: AI clips (realism, performance, physical events code can't fake)

Use AI clips for a few shots only, and only where they earn it: real skin, cloth, water, crowds, a human performance, or a camera move through a real-looking space. Everything else stays in code, where it is exact and free.

## Tools (MCP first; see `references/sources.md`)
- **Higgsfield MCP** (`generate_video`, `generate_image`, `media_upload`):
  - motion transfer: `hf_mult_motion_control`
  - object swap: `hf_mult_replace_object`
  - for multi-step jobs, call its `get_workflow_instructions` first
- **Runway hosted MCP** (`https://mcp.runwayml.com/mcp`, OAuth): Gen-4.5, Kling 3.0, Veo 3.1 and Seedance through one login.
- Pick the model by the shot's hardest need, and read the MCP's current model list rather than memory:
  - identity lock
  - camera control
  - first-and-last-frame (keyframe) mode
  - length
  - motion reference

## Credit gate (hard)
1. Write `shots.json`. One row per AI shot: `id, range, purpose, model, mode, refs, duration, est_credits`.
2. Show the table with the total, then STOP. Wait for an explicit "yes".
3. Generate **one shot at a time.** After each one, inspect it (below) before generating the next. A broken shot 1 usually means the prompt pattern is wrong for every shot.
4. Log each generation in `shots.json`: seed, model, prompt file, credits spent, verdict.

## Prompt = a small production plan (distilled from the Seedance 2.5 guide, MVP-Prompts)
Write prompts in this order:
1. **Format + one-sentence event:** "8 s, 16:9, one continuous shot: …".
2. **Reference roles:** bind each image to exactly one job (first frame / identity / prop design / last frame / location). Pick the mode in the UI or tool (keyframe mode); prose doesn't replace that.
3. **Persistent cast and props:**
   - one identity each, a few stable identifiers
   - exact counts ("one chair, two gloves")
   - scale written as relations ("a finger thicker than his forearm")
4. **Camera rule for the shot:** locked, tracking or one motivated approach. "One continuous shot" means no cuts, no dissolves and no snap to the last frame.
5. **Timed paragraphs** (`0.0–2.0 s …`). For each event: origin → path → mechanism → **contact** → resulting state → what persists. Contact makes the impossible look photographed: compression, wrinkles, shadows, rebound, settling.
6. **Write the ending backwards:** decide the final frame (pose, gaze, prop positions, camera), then design the motion that physically arrives there. Arrival, then settle, then hold.
7. **Continuity notes:** a few targeted exclusions for failures actually seen ("no extra person, no chair replacement, no final dissolve"). Spend words on positive mechanisms, not negatives.

**State ledger** (private, while drafting): for each beat, record where each actor and prop is, what supports it, whether it is visible, and how it gets to the next beat. Entrances use declared routes.

**Sound:** say diegetic-only, score, or in-world music. Never leave it to the model. Music videos usually want the clip silent, because the song is the audio.

**Length:** add a sentence only when it removes an ambiguity (route, contact, identity, timing, final state). If the model has a limit, count the characters that will actually be pasted.

## Inspect before use (3 frames minimum, then the decisive moments)
- Watch at full speed for story and rhythm.
- Then step through the risky moments slowly: entries and exits, contacts, occlusions, the transformation's end, the final alignment, and the frames just before and after anything disappears.
- Write down what actually happens; never report the planned action as if it were seen.
- **Classify the failure, then revise the earliest broken event.** Keep what works and change one thing per retry:

| Failure | Fix |
|---|---|
| skipped action | more time or fewer competing events |
| teleport | a supported path and a visible boundary crossing |
| identity drift | tighter reference binding, fewer transformations |
| physics break | name the contact and the support |
| last-frame snap | write the arrival backwards from the end |

- After 3 failed retries on one mechanism, simplify the mechanism or cut to a code shot.

## Continuity tricks that save credits
- **Chain shots:** take the last frame of clip N (`ffmpeg -sseof -0.04 -i n.mp4 -frames:v 1 last.png`) as the first frame of clip N+1. The cut becomes invisible.
- **One character sheet, reused** as the identity reference in every shot (Higgsfield's character-sheet workflow, on explicit request). Never re-describe the face in prose.
- **Guide the camera with a 3D blockout** instead of words: `engines/guide-3d.md`.
- **Fix it in the cut instead:** a 2-frame trim or a cut on motion hides a bad final second for free.

## Conform AI clips into the film
- **Technical match:** match fps (`-r`) and size. Grade to the STYLE palette (`ffmpeg -vf lut3d=look.cube`, or eq/colorbalance) so AI shots and code shots share black level, warmth and saturation.
- **One finish pass over everything:** the same grain, vignette and halation applied to AI and code shots alike. This is the single biggest "it all belongs to one film" trick.
- **Text:** lyrics and type are always rendered in code *over* the clip. Never ask the model for text.
- **Timing:** cut on the beat grid. Speed-ramp at most ±15%; more than that looks synthetic.
- **Faces:** check every face frame for drift. No text over faces.
- **Credits:** log the model and the prompt in `CREDITS.md`, and tick AI disclosure.

## Spend credits like a director, not a gambler
- **Draft tier first:** if the MCP offers a cheaper or shorter mode, prove the prompt there (3–5 s). Re-run on the hero model only once the draft shows the mechanism working.
- **Generate the hardest shot first.** If it can't be done, the plan changes before the easy shots are paid for.
