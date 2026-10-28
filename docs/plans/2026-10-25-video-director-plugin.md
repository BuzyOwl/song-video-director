# video-director plugin: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: use superpowers:subagent-driven-development or superpowers:executing-plans to work through this plan task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the `song-video-director` repo into the `video-director` plugin. It covers music videos first, plus talking-head reels and YouTube edits. It gets a front door, a router, taste evals, gates, a gallery made from real films, and a verified sources guide.

**Architecture:** A plugin root containing one skill, `skills/video-director/`. The hub `SKILL.md` loads lazily: one mode file, then at most two engine files. Code is reused wherever it already works: the talking-head pipeline is copied whole, and `song_facts.py` is kept. There is one new script, `film_gate.py`, with tests. The gallery is a static HTML page of 6–8 s clips cut from the user's own finished films.

**Tech stack:** Markdown skills, Python 3.11+ (numpy plus ffmpeg/ffprobe on PATH), Node 22+ / Remotion (talking pipeline, unchanged), plain HTML.

**Spec:** `docs/specs/2026-10-25-video-director-plugin-design.md`. Source verification: `docs/specs/sources-verified-2026-10-25.md`.

## Global constraints
- Hub `SKILL.md` ≤ 90 lines. Every mode or engine file ≤ 120 lines. A typical load (hub + 1 mode + 2 engines) ≤ 330 lines.
- Python scripts run with `-I`. Inputs are untrusted paths, and nothing is ever executed from an input folder.
- No API keys in files. Credit spend needs an explicit "yes" from the user.
- Gallery clips: ≤ 1.5 MB each, 480p, no audio (silent loops).
- Every external asset goes in `CREDITS.md` with its license. Nothing NC goes into monetised output.
- Work on the `v2-video-director` branch. **Do not push** without the user's OK.

## File map
```
.claude-plugin/plugin.json, .claude-plugin/marketplace.json
skills/video-director/SKILL.md                      hub
skills/video-director/modes/{music,talking,youtube}.md
skills/video-director/engines/{code,ai-clip,guide-3d,recreate}.md
skills/video-director/references/{feel,style-protocol,lessons,sources}.md
skills/video-director/styles/<id>/STYLE.md          looks (proven + companion)
skills/video-director/scripts/{song_facts.py,film_gate.py,make_samples.py,test_film_gate.py}
skills/video-director/talking/                      copied talking-head pipeline (scripts/, remotion/, references/)
gallery/index.html, gallery/samples/*.mp4
evals/evals.json, evals/taste-ab.md
docs/specs/*, docs/plans/*, README.md, CHANGELOG.md, CREDITS.md
```
Removed: `skill/song-video-director/`. Its content moves into the files above, and git history keeps the old version.

---

### Task 1: Plugin scaffold, plus moving the existing skill
**Files:**
- Create `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.
- `git mv skill/song-video-director/scripts/song_facts.py skills/video-director/scripts/song_facts.py`.
- Delete the rest of `skill/` once its content has been ported (Tasks 6 and 8).
- Copy the specs into `docs/specs/`.

- [ ] Write `plugin.json`: `{"name":"video-director","version":"2.0.0","description":"...","author":{"name":"BuzyOwl"},"license":"MIT"}`.
- [ ] Write `marketplace.json` listing the one plugin, with `"source": "./"`.
- [ ] Run `python -I skills/video-director/scripts/song_facts.py --selftest`. Expected: it prints a pass.
- [ ] Commit: `chore: scaffold video-director plugin`.

### Task 2: Absorb the talking-head pipeline
**Files:** copy `~/.claude/skills/talking-head-director/{scripts,remotion,references,CHANGELOG.md}` to `skills/video-director/talking/`. Leave out `.git` and `node_modules`. Create `modes/talking.md`.

- [ ] Copy the tree, then `grep -rn "talking-head-director\|skills/talking" skills/video-director/talking`. Fix any absolute paths; the scripts use paths relative to their own folder, so none are expected.
- [ ] Write `modes/talking.md`. It is the old SKILL.md body, with the cut, plan, render and feedback sections kept verbatim. The commands are rewritten to use `$SKILL/talking/scripts/...`. The hard rules already in the hub are dropped.
- [ ] Run `python -I skills/video-director/talking/scripts/test_prep.py`. Expected: PASS, or a skip naming the missing optional dependency.
- [ ] Commit: `feat: absorb talking-head-director as talking mode`.

### Task 3: `film_gate.py` (TDD)
**Interface:** `python -I film_gate.py <video> [--feel feel.json] [--song song_facts.json] [--style STYLE.md] [--loop] [--json out.json]`. It exits 1 if any HARD check fails.
- **HARD checks:**
  - `dead_gap`: no visible change for more than 1.0 s.
  - `flicker`: two luminance spikes less than 0.17 s apart.
  - `slideshow`: the share of shots with in-shot motion is below 0.6.
  - `loop`: first frame ≠ last frame, when `--loop` is passed.
- **SOFT checks** (reported to the reviewer, never a fail):
  - cut rate and stillness per section against the feel card
  - `feel_sync`: correlation between motion energy and audio energy
  - palette ΔE against the STYLE.md hex values
  - `beat_hits`: share of cuts within ±1 frame of the beat grid

**Method:** decode with ffmpeg at 160 px wide grayscale plus a 32×18 RGB thumbnail stream. Then compute:
- per-frame mean absolute difference
- cuts: a difference spike more than 4× the rolling median
- in-shot motion: median difference inside each shot
- luminance spikes
- palette: k-means (k=6, numpy only) on RGB samples, converted to Lab, nearest-hex ΔE

**Tests** (`test_film_gate.py`, plain asserts, clips generated with ffmpeg lavfi into a temp dir):
- [ ] A 4 s `testsrc2` clip passes: no dead gap, no slideshow.
- [ ] A clip made of three 2 s solid colours fails `slideshow` and `dead_gap`.
- [ ] A clip with two white frames 0.1 s apart over black fails `flicker`.
- [ ] A loop check on `testsrc2` with `--loop` fails, because the first and last frames differ.
- [ ] Run `python -I test_film_gate.py`, watch it fail, implement, then rerun until it passes.
- [ ] Commit: `feat: film_gate hard/soft checks with tests`.

### Task 4: Gallery from the user's real films
**Files:** `scripts/make_samples.py`, `gallery/index.html`, `gallery/samples/*.mp4`.

- [ ] `make_samples.py` reads `gallery/samples.json` (`[{id, src, start, dur, title, look, engine, cost}]`). For each entry it runs `ffmpeg -ss S -t D -i SRC -an -vf scale=-2:480,fps=24 -c:v libx264 -crf 30 -preset slow -movflags +faststart`. It asserts the output is ≤ 1.5 MB, and if not, re-encodes at CRF+3.
- [ ] Pick 1–2 signature moments per film from a 12-frame contact sheet of each source:
  - toota-naksha-v6
  - jod-ke-dekh-v8
  - basement-goldfish-final
  - teacher_journey_v9
  - himalayan-vow-v1
- [ ] `index.html` is one file: a tile grid of looping `<video muted autoplay loop playsinline>`. Each tile shows the look name, engine, cost and a "Use this look" button that copies the id. It must work from `file://`, with no server needed.
- [ ] Commit: `feat: gallery of proven looks from finished films`.

### Task 5: Style cards
**Files:** `styles/<id>/STYLE.md`. Five proven looks come from the films, each read from its project source and frames:
- `painterly-cutout` (Basement Goldfish)
- `cinematic-plate` (Toota Naksha)
- `clay-world` (Jod Ke Dekh)
- `teacher-journey`
- `himalayan-vow`

Plus pointers to companion looks: claude-video-2 for motion graphics, huashu for art styles.

- [ ] Use the claude-video-2 STYLE.md format, extended with `## Feel` (genre fit, valence/arousal range, cut-rate band) and `## Signature (must / bonus / taboo)`.
- [ ] Check: `grep -c "^## " styles/*/STYLE.md`. Each card should have 9 or more sections.
- [ ] Commit.

### Task 6: Hub and modes
- [ ] `SKILL.md` (≤ 90 lines):
  - frontmatter description, triggering on music, talking-head and YouTube edit requests
  - front door (10 steps)
  - router table
  - load rule
  - universal rules
  - feedback protocol
  - gate summary
- [ ] `modes/music.md`: song_facts, lyric tagging (M/A2/A1/E), section hits, scene plan fields, lyric lanes, "repeats grow", endings in the film's world, the upload pack.
- [ ] `modes/youtube.md`: the hook in 0–5 s, chapters, b-roll, retention pacing, 8 explainer grammar cards (condensed from huashu 09 and its grammar files; credited), and the thumbnail.
- [ ] Check line counts with `wc -l`.
- [ ] Commit.

### Task 7: Engines
Each file is ≤ 120 lines:
- [ ] `code.md`:
  - HyperFrames, Remotion and three.js rules
  - determinism
  - temp files on the big drive
  - tail-render plus concat
  - the parallel-agent playbook
  - the official skills to install (`remotion-dev/skills`, `heygen-com/hyperframes`)
- [ ] `ai-clip.md`:
  - prompt as a production plan (Seedance guide distilled: causal timeline, state ledger, end frame written backward, contact evidence)
  - the credit gate
  - inspect 3 frames per clip
  - Higgsfield and Runway MCP calls
- [ ] `guide-3d.md`:
  - Blender blockout with mcp-for-blender: grey clay, the camera path, first/last frames, a depth pass
  - feeding those to AI video gen
  - dance reference through FreeMoCap or Rokoko to a rig, or `hf_mult_motion_control`
- [ ] `recreate.md`:
  - REFERENCE.md breakdown
  - blockout
  - detail passes
  - matched-time side-by-side
  - at most 3 repair passes
  - Blender by default, with Unreal 5.8 MCP as the optional branch
- [ ] Commit.

### Task 8: References
- [ ] `feel.md`: a genre×mood table (8 genres × valence/arousal) giving cuts per minute, motion energy, stillness, palette band and easing family; plus how to read valence and arousal.
- [ ] `style-protocol.md`: anchor → signatures → compose → shape + medium → frame first → motion logic → 100-point rubric with vetoes → independent reviewer.
- [ ] `lessons.md`: one line per lesson in rule-and-fix form. Target ≤ 110 lines, down from 332.
- [ ] `sources.md`: the verified tables plus "last verified 2026-10-25".
- [ ] Commit.

### Task 9: Evals
- [ ] `evals/evals.json` in skill-creator format: 24 genre×mood prompts plus 4 near-misses, each with expectations covering mode, engine, feel band and vetoes.
- [ ] `evals/taste-ab.md`: the 4 fixed briefs and the blind A/B procedure.
- [ ] Commit.

### Task 10: README, CHANGELOG and CREDITS; local verify
- [ ] README: the gallery wall (GIFs made from the samples), what it does, one-line install (`/plugin marketplace add BuzyOwl/song-video-director`, then `/plugin install video-director`), and credits.
- [ ] Verify:
  - `wc -l` budgets
  - `grep -rn "TODO\|TBD"` returns nothing
  - `python -I scripts/test_film_gate.py` passes
  - the gallery opens
- [ ] Commit.

### Task 11: Improvement pass (user request)
Review everything above for anything that harms output quality, and drop or rework it. Add outside-the-box tricks. Update the spec to match, rerun Task 10's verification, and commit.
