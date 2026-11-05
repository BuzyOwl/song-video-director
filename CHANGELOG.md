# Changelog

## 2.2.0 (2026-11-05)
- Rules model: 9 hard rules in SKILL.md (honesty/money/legal, the creator's vision first, look before claiming, no broken finals, deliberate measured placement, faces, determinism, approved stays approved, originals safe). Everything else is a direction a piece may break with one line in its STYLE.md; measured bugs are tagged **Fact**, hard-rule-1 lines **Safety**. Every mode, engine, craft and reference file carries the note.
- Looks are a menu, never a fence: the creator's own style, ready looks, or a fresh one (`references/stacks.md` §1). New stack guide: pros/cons, combinations that held, when Blender earns its place and how it hands off.
- `film_gate.py`: HARD = broken render only (global flicker, blank, delivery, loop). Pacing (dead gap, slideshow) is judged against the feel card and fails only when feel.json sets `"gate"`. New HARD blank check (black/white/magenta runs, `blank` spans exempt) and delivery made HARD (CFR, A/V offset within a frame).
- New `scripts/flicker_scan.py`: local flicker under a moving camera (flow-aligned neighbours, 1-3-frame change-and-back runs, CIELAB tolerance, motion quieting), with mask video, ranked events and contact sheets; method from Imaginative-Prompting/claude-video-skills render-checks (MIT). Chroma compared at 4:2:0 resolution (saturated edges under a pan otherwise read as flicker). Tested on planted flicker, a clean pan and a hard cut.
- Conflicts from the rules inventory (`docs/rules-inventory.md`) resolved: lesson location, deletion, AI disclosure, fix rounds, Shorts length, thumbnails, 9:16 crop vs re-layout, b-roll timing, entrances, dark vs bright looks, camera drift, caption ink and sizes, reviewer vetoes as advice.
- Added from the reference repo: camera pace at large scale, spline edits leaking into neighbours, shot size and height balance shares, optional continuous-camera style; rework keeps the point; scope lock; patch pre-roll and gated-span diffs.
- talking/checks.md keeps only bugs and safety; pitch-film look choices are options.

## 2.1.0 (2026-11-05)
- New `craft/` layer, loaded one file at a time: story, camera, motion, timing, blocking, light, render, team. Camera, motion, timing, blocking, light, render and team are adapted from Imaginative-Prompting/claude-video-skills (MIT); story comes from the author's film-cinematographer skill.
- New film mode for animated shorts, cutscenes and narrated story films (script or VO as the clock, blocking first, shot by shot).
- Fixes from measured evidence: no `concat -c copy` joins (21 ms drift, dropped frames); render muted and mux the WAV (Remotion AAC ~43 ms late); Whisper word times are for which word, not when (0.5-0.8 s early on sung vocals).
- talking/checks.md absorbs the group and pitch film lessons from the standalone skill; new lessons go to `~/.video-director/checks.md`, which survives plugin updates.
- Review page: WIP (Imaginative-Prompting/wip) recommended, with its CLI and entry format; its frame references and drawings feed feedback rounds.
- `film_gate.py` reports delivery facts (BT.709 tags, constant frame rate, A/V start offset), with a test.

## 2.0.0 (2026-10-25)
- Renamed to the `video-director` plugin. One hub skill, lazy modes (music, talking, youtube) and engines (code, ai-clip, guide-3d, recreate).
- Front door: gallery of real film clips, five questions in one message, router with cost per scene, animatic before art.
- Absorbed talking-head-director as the talking mode. Hardcoded drive paths replaced by `VD_TMP`, `VD_MODELS`, `VD_TEST_REEL`.
- New `film_gate.py` with tests. Calibrated on five finished films: a 0.5 s window diff so slow drift and on-twos animation count as motion; wipes merged into one cut; single blooms are not flicker; sub-0.3 s shots and feel-sync are reported, never failed.
- Feel card (genre and mood bands, one deliberate break), style protocol with 100 point rubric and independent reviewer, taste anchors.
- AI clip engine (prompt as production plan, credit gate), Blender-guided generation and dance reference, recreate-in-3D engine.
- Verified free sources and MCPs (2026-10-25).
- Evals: 29 routing and feel cases, blind taste A/B for releases.

## 1.0.0
- song-video-director skill: workflow, hard rules, lessons from three films, song_facts.py.
