# Changelog

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
