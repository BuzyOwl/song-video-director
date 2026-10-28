# video-director plugin: design

Date: 2026-10-25. Status: approved in brainstorm, awaiting spec review.

## Goal
One lean, token-cheap Claude Code plugin that directs music videos first, and also YouTube edits and talking-head reels. It replaces `song-video-director` and absorbs `talking-head-director`. Taste comes from a style gallery with real sample videos, and quality from gates that check frames. Cost comes down because a router picks the lightest engine that hits the look.

## Inputs studied
- `BuzyOwl/song-video-director`: craft (song_facts, measure the world, feedback protocol, parallel agents, three stacks). The local copy and the repo are byte-identical.
- `ItsssssJack/claude-video-2`: productised UX (a gallery of looks as real videos, 5 questions in one message, a brief in numbers, 3 stills scored, pacing and loop checks, STYLE.md format, credit gate).
- `ae-builder` (attached): verify, don't trust (curve fit ≤2%, strict mock), and a postmortem → rule pipeline. Not ported; its discipline goes into the gates.
- `alchaincyf/huashu-art-motion` (MIT): 36 art-style recipe cards, 9 explainer grammars, style demo protocol with 100-pt rubric + vetoes, measured self-score inflation (~10 pts) → independent reviewer, `film_gate` anti-slideshow, breakdown (transitions, beat grid, motion heatmap). Adopted: protocol, rubric, grammars, gate. Its 36 art styles are offered as an optional companion install (`npx skills add alchaincyf/huashu-art-motion`), not copied; 6 most music-relevant (ink, ukiyo/woodblock, impressionism, vaporwave, Shinkai, 8-bit) are condensed into English STYLE.md cards with credit.
- `mattvideoproductions/MVP-Prompts`: the video-to-unreal method (REFERENCE.md breakdown, blockout, detail passes, matched-time compare, ≤3 repair passes) and the Seedance guide (prompt = production plan, causal timeline, end frame written backward, contact evidence).

## Problems fixed
1. No front door: the user isn't guided, has no samples, and gets no style choice.
2. No stack router: Claude picked heavy stacks that gave worse results and cost more tokens.
3. No objective gates.
4. No realism path: AI clips guided by Blender camera blockouts or dance references.
5. No asset or reference help.

## Layout
```
video-director/
  .claude-plugin/plugin.json
  skills/video-director/
    SKILL.md              hub ≤90 lines: front door, router, universal rules, feedback protocol
    modes/music.md        song_facts → scene plan → lyric lanes; repeats grow; endings in-world
    modes/talking.md      filler cut (EN/HI), captions, cards, punch zooms (from talking-head-director)
    modes/youtube.md      long-form: hook 0–5 s, chapters, b-roll, retention pacing, thumbnail, upload pack
    engines/code.md       HyperFrames / Remotion / three.js rules, determinism, temp on big drive
    engines/ai-clip.md    prompt as production plan, state ledger, credit gate, 3-frame inspection
    engines/guide-3d.md   Blender blockout → camera path / depth / first-last frames → AI gen; dance ref → motion transfer
    engines/recreate.md   reference clip → REFERENCE.md → rebuild (Blender/three.js/UE) → matched-time compare
    styles/<id>/STYLE.md  ~8 music-video looks (+ sample.mp4, short and low bitrate)
    references/sources.md free assets, reference sites, MCPs (license-tagged)
    references/feel.md    genre×mood → target numbers table; valence/arousal how-to
    references/style-protocol.md  anchor → signatures → medium → frame-first → score (from huashu 16)
    evals/                skill eval prompts + assertions + taste A/B briefs
    references/lessons.md trimmed: rules and the fix for each; war stories cut
    scripts/              song_facts.py, stills.sh, pacing_check.py (+ beat-sync), gallery.py
  README.md               gallery GIF wall, 3 finished films, one-line install
```

**Load rule:** hub + 1 mode + at most 2 engines, about 300 lines in a typical run. `sources.md` and `lessons.md` are read only on demand.

## Front door (all modes)
1. Detect the mode from the input: a song gives music, a talking clip gives talking, long footage gives youtube. Ask only if it's ambiguous.
2. Choose a look. Music opens the gallery. Talking and YouTube get a 3-style shortlist.
3. Ask 5 questions in one message, each with a default; "go" accepts them all.
4. The router prints the engine for each scene, why, and its cost (render time, token weight, credits).
5. Write BRIEF.md in numbers (size, fps, palette hex, fonts, easing, ban list).
6. Storyboard. Stop for a "yes" if any credits will be spent.
7. Render 3 stills and self-score them 1–10 on composition, motion, type, colour and idea. Fix until every score is ≥8, then show them.
8. Render.
9. Run the gates.
10. Hand-off: path, specs, gate results, one "next try" idea.

## Router
| Need | Engine | Cost |
|---|---|---|
| lyric / graphic / kinetic type | HyperFrames (HTML+GSAP) | low |
| 2.5D story from art plates | Remotion + Canvas/WebGL | med |
| procedural 3D world | three.js in Remotion | high: only when the world is the story |
| realism, smooth complex camera | AI clip, guided by a Blender blockout | credits |
| dance / performance | AI clip + motion transfer from a reference clip | credits |
| recreate a reference shot in 3D | recreate engine (Blender default, UE optional) | high |
| talking / YouTube edit | Python cut + Remotion | low |

Rules:
- Pick the lightest engine that hits the look. A heavier pick needs a one-line reason shown to the user.
- Engines can mix per scene, on one clock: the song.

## Gates (never claim a pass without running it)
- Stills scored ≥8.
- `pacing_check.py`: no dead gap over 1 s, nothing on screen under 0.3 s, and in music mode the hits land within ±1 frame of the beat grid.
- Loop check if the piece loops.
- Pull frames from the final MP4 at the flagged times.
- AI clips: inspect 3 frames per clip before using it.
- Recreate: side-by-side at matched times, at most 3 repair passes.
- Lyric timing is labelled "not ear-checked" unless the user has confirmed it.

## Taste evals: style, genre, mood, emotion, feel
Two layers: **in-run evals** judge each video; **skill evals** regression-test the skill itself.

### A. Feel card (written before any build, part of BRIEF.md)
Translate the words into targets that can be checked:
- **Genre** sets the conventions to honour or break on purpose. Examples: hip-hop cuts on the snare and uses hard type; a ballad holds long and moves the camera slowly; EDM builds and drops; lo-fi loops and drifts.
- **Mood** is valence (sad↔joyful) × arousal (calm↔intense). Each song section gets a point on that grid. Arousal comes from song_facts energy; valence comes from the lyrics plus the user's answer.
- **Emotion arc** is one line per section ("numb → cracking → release → quiet acceptance"), plus the one signature moment.
- **Measurable targets per section:**
  - cuts per minute
  - motion energy (mean optical-flow magnitude)
  - palette lightness and saturation band
  - contrast
  - easing family
  - stillness ratio

  Defaults come from a genre×mood table in `references/feel.md`. The user's answers and the reference override them.

### B. Style fidelity (adapted from huashu-art-motion protocol 16, MIT, credited)
1. **Anchor:** gather at least 3 real references, either public-domain works fetched to the project or the user's own links. Build a contact sheet and extract the palette. Never work from memory.
2. **Signature list:** 5 traits, each marked must-have, bonus or taboo, plus how the medium is physically made (brush, cut paper, film grain, cel). That physical process is the renderer's spec.
3. **Compose by the style's own logic,** not a reused layout.
4. **Shape layer, then medium pass:** noise over flat vectors is not a style.
5. **Frame first:** render one still and put it side by side with the references before animating.
6. **Move by the style's own motion logic:** no generic fades everywhere.

### C. Scoring (100 points; the threshold is 80; at most 2 repair rounds)
| Item | Points | How it's judged |
|---|---|---|
| Signature hit | 25 | tick off each must-have from the signature list; −5 for each one missing |
| Mood and emotion match | 20 | each section sits on its valence/arousal point; the arc is readable with the sound off |
| Feel targets | 15 | measured values against the feel card, from `film_gate.py` |
| Medium credibility | 10 | at 1:1 crop, is it real medium or vector plus noise? |
| Composition and story | 10 | the style's own layout logic; the event reads at a glance |
| Motion and music sync | 10 | hits on the grid; motion follows the energy curve |
| Type and faces | 5 | lanes, phone-readable size, nothing over a face |
| Technical | 5 | determinism, no flicker, render clean |

**Vetoes (instant fail):**
- signature hit below 15
- the hero looks childish or like a sticker
- the mood contradicts the section (for example a strobe in a grief verse)
- the slideshow gate fails

**Independent review:** a fresh subagent that did not build the film scores it from stills plus the side-by-side, never from the code. The lower of the self-score and the independent score counts. Taste items (beauty) are flagged for the human, and the AI never writes "taste approved".

### D. Automated gates (`scripts/film_gate.py`, one script)
- **Anti-slideshow:** share of shots with real in-shot motion is at least the target. Adapted from huashu `film_gate`.
- **Feel-sync:** correlation between the motion-energy curve and the audio-energy curve is at least 0.4 in music mode.
- **Cut rate and stillness per section:** within ±25% of the feel card.
- **Palette:** mean ΔE from the STYLE.md hex set is at most the threshold; at most one accent hue present.
- **Flicker:** two flashes under 0.17 s apart is a fail.
- Plus the existing pacing and beat-grid checks, folded into this one script.

### E. Skill evals (`evals/`, skill-creator format)
- **Prompt matrix:** about 24 cases. 8 genres (ballad, rap, EDM, lo-fi, rock, devotional/folk, pop, cinematic score) × 3 moods. Each asserts:
  - the router picked the right engine
  - the feel card's numbers fall inside the genre×mood band
  - the style pick fits, or the user's choice was honoured
  - no veto rule was broken in the plan
- **Near-misses:** a talking clip with background music must route to talking, not music. "Make a lyric video quick" must route to the light engine or hookline.
- **Taste A/B:** 4 fixed briefs, with the plan and 3 stills generated before and after any skill change. A blind reviewer agent picks the winner; the change ships only if it wins or ties at least 3 of 4.
- Run `evals/run.md` before each release, and record the results in CHANGELOG.

## Explainer grammars (youtube mode)
Adopt huashu's 8 animation grammars as one-paragraph cards in `modes/youtube.md`: 3b1b, keynote UI, finance chart, Kurzgesagt, Vox collage, whiteboard, storytime, kinetic type. Each card has when-to-use, signature moves and one ban. Per segment, the grammar is chosen from the narration.

## Universal rules (hub)
- Faces get similarity transforms only. Text never covers a face. Never crossfade bodies.
- One style per piece and one accent colour. The ban list applies.
- Every effect means something; quiet sections stay still; repeats grow.
- Determinism: no Math.random or Date.now.
- Never spend credits or print API keys without a clear "yes".
- Log every external asset in CREDITS.md with its license. No NC licenses in monetised videos.
- Credit honestly and tick the AI-disclosure box.

## sources.md
Filled from live verification (Oct 2026). One table per category (3D, textures/HDRI, mocap, footage, audio, fonts, motion, reference/taste) with these columns: name, URL, what is free, license, account needed, MCP. It also holds an MCP shortlist.

Verified seed: `sources-verified-2026-10-25.md` (same folder). Key points it carries:
- **Defaults that need no account and are CC0:** Poly Haven, ambientCG, Kenney.
- **Realism-path MCPs:**
  - mcp-for-blender (32k★; Poly Haven, Sketchfab and Poly Pizza import plus text-to-3D)
  - Higgsfield (motion transfer)
  - Runway hosted MCP (Kling and Veo in one OAuth)
- **Dance reference → rig:** FreeMoCap (open source) or Rokoko's free tier, then Mixamo for retargeting.
- **License traps:**
  - Quaternius is not CC0.
  - Coverr and Sonniss forbid AI training.
  - Pixabay music carries Content ID claim risk.
  - Freesound includes NC sounds.
  - Megascans and ShotDeck are no longer free.
- **Changes to follow:** blender-mcp → mcp-for-blender; Blendkit renamed; Sketchfab now owned by KitBash; godly → recent.design. The Blender Lab MCP clashes on port 9876 with mcp-for-blender, so run only one.
- `sources.md` gets a "last verified" date. A `doctor` step re-checks the URLs' HTTP status before each release.

## Migration
- Repo `BuzyOwl/song-video-director` becomes the plugin. Its name stays for the stars, and the README is retitled.
- The old skill folder and `talking-head-director` are retired after the plugin installs. Content is folded in, not deleted, until the plugin has been verified on one real project.

## Out of scope (YAGNI)
- AE export. ae-builder stays a separate skill.
- Unreal as the default. It is an optional branch in recreate.md only.
- Paid APIs other than the user's own Higgsfield/Runway credits, which are always gated.

## Testing
- Trigger evals (skill-creator): about 10 prompts across the 3 modes, plus near-misses.
- A dry run of each mode on a sample input, to confirm the load rule (count the lines read).
- `song_facts.py --selftest`, and `pacing_check.py` on a known clip.

## Improvement pass (2026-10-25, after build)
Dropped or changed because they harmed quality:
- **In-loop self-scoring.** Self-scores run about 10 points high, so iterating on them optimises the wrong number. The scoring now comes from a fresh reviewer subagent at the stills stage and again on the render. The self-check is limited to facts: the signature checklist and the vetoes.
- **Agent-picked stills.** Stills are now taken at fixed, hardest moments: the signature moment, the busiest transition, the densest-text frame. The agent can no longer pick its prettiest frames.
- **Feel-sync as a target.** It read about 0 on all five finished films, so it is reported but never scored or gated.
- **`min_on_screen` as a HARD gate.** It failed every finished film because of 1-frame impact cuts and wipes. It is now SOFT.
- **Frame-to-frame motion measure.** It called slow drift and 12 fps animation "frozen". The gate now diffs against the frame 0.5 s earlier, merges spikes within 0.25 s, and counts a flash by its onset.
- **Gallery as the taste baseline.** The user's own films are proof that the pipelines work, not the taste ceiling. References the user loves come first and are measured, and the gallery is the fallback.
- **Feel bands presented as calibrated.** They are now labelled uncalibrated estimates. A measured reference wins.
- **Universal ban list and the 6-word cap** (from claude-video-2). They broke lyric videos and cinematic finishes, so each style's own ban list rules instead.

Added:
- reference teardown via `film_gate.py ref.mp4`, which seeds the feel card and palette
- two contrasting treatments of the signature moment, the user picks (the cheapest taste decision)
- a taste memory in `~/.video-director/taste.jsonl` (approvals and rejections) that pre-picks defaults
- declared stillness: holds and freezes must be listed in `feel.json` with a reason and keep one thing alive
- the thumbnail starts from the picked signature still
- AI clips: the draft tier first, and the hardest shot first
- talking pipeline paths made portable (`VD_TMP`, `VD_MODELS`, `VD_TEST_REEL`)
