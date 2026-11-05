# Rules inventory: video-director plugin

Every rule, restriction, ban, threshold and default found in the plugin's text files, plus the owner's personal checks.md.
Read-only survey, 2026-11-05. Plugin root: `song-video-director/skills/video-director`. Rule numbers run across the whole document.

## Summary

Total rules: **740**

| Tier | Count |
|---|---|
| Safety | 57 |
| Fact | 105 |
| Process | 249 |
| Direction | 296 |
| Case note | 33 |

### Conflicts

1. R150 vs R688: unspoken caption words at 45 % opacity vs captions at full ink from the first frame.
2. R148 / R160 / R655 / R724 vs R670: captions ≥ 70 px vs ~52 px at 1080p in pitch films.
3. R106 vs R148: music sans type ≥ 60 px vs talking captions ≥ 70 px (and R670 ~52 px).
4. R403 vs R567 / R569 / R676: "keep it dark" vs Pop bright sets, lightness +10 %, cream pitch-film rooms.
5. R37 vs R679: never crossfade bodies (universal) vs fades fine for real-person cutouts in pitch films.
6. R426 vs R201: every entrance animates 6–12 frames vs storytime pose swap in 0.1 s.
7. R426 vs R677 / R680: 6–12-frame entrances vs wake into video in 5 frames, and hide (not fade in).
8. R234 vs R629 / R394 / R471: "do not argue with the gate" vs fix a gate that fails good work, a disagreeing number is a broken metric, a FAIL can be the instrument.
9. R19 vs R732: nothing still > ~3 s vs HARD fail at 1.0 s of no change.
10. R19 vs R43 / R201 / R377 / R492 / R619: 3 s still cap vs quiet sections stay still, ~70 % still frames, dead-still beats, 4–8 s verse holds.
11. R20 / R715 vs R291 / R424 / R96 / R585: nothing moves after landing vs constant camera drift, breathing idle, keep one thing alive, 2 looping motifs.
12. R715 vs R732 / R734: a landed board that must not move fails both HARD gates after 1 s.
13. R734 vs R201 / R567: ≥ 60 % moving shots vs storytime ~70 % still and lo-fi stillness 0.50–0.80.
14. R26 vs R589 / R599: fix until 80+ (no cap) vs at most 2 repair rounds, then report under 80.
15. R73 / R126 vs R181 / R227: 9:16 by re-layout, never crop vs Shorts cropped on the face.
16. R53 / R123 vs R222: always tick AI disclosure vs only for realistic AI, not for 2D animation.
17. R17 vs R601: read lessons.md before building vs read it when stuck.
18. R61 / R167 vs R602 / R653: lessons go only in ~/.video-director/checks.md vs add a line to plugin files.
19. R54 / R635 vs R537: delete render temp after a verified render vs never delete without the creator's OK on the exact list.
20. R35 vs R41 / R409: no halftone on emotional close-ups vs no global style ban and halftone as comic structure.
21. R170 vs R8: offer 3 named looks vs never pick a look off a shelf.
22. R186 vs R18 / R427: b-roll on the word ±0.2 s vs never before the word.
23. R370 vs R142 / R722 / R185 / R197: never a pure zoom vs auto punch zoom, punch-ins, log zoom.
24. R378 vs R481: nothing about a lyric may aim the camera vs push-in lands on the lyric.
25. R372 vs R479: avoid mid lens at mid distance vs 35 mm storytelling / 50 mm neutral.
26. R291 vs R212 / R481 / R377: always drift (dead-still = slideshow) vs move only when the eye must go somewhere, locked-off awe, dead-still beats allowed.
27. R592 vs R735: nothing on screen under 0.3 s vs 1-frame impact cuts used on purpose.
28. R664 vs R209: one accent per clip vs ≤ 3–4 meaning colours.
29. R322 vs R318: never project the reference into the scene vs project the photo onto the blockout.
30. R571 vs R96: EDM drop silent and still for one bar vs a fully frozen frame reads as a bug.
31. R713 vs R18 / R660: structure on screen from frame 0 vs everything appears on the word that names it.
32. R125 vs R225: Shorts 15–45 s vs 20–45 s.
33. R124 vs R190: skip end cards over the final shot vs end screen in the last 5–20 s.
34. R386 vs R591 vs R217: one-glance test at 360 px vs 160 px vs 168×94.
35. R368 vs R393 / R435: frame sheet every 2–4 frames vs step every frame; sheets hide pops.
36. R427 vs R88 / R295: never before the cue vs cut 1–2 frames before the beat.
37. R56 vs R468: SKILL pulls frames with -ss vs -ss isn't frame-exact.

Duplicates (the same rule stated in more than one file) are marked "Dup of R#" in the Note column.

## SKILL.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R1 | If a better-result stack or repo (like HyperFrames) appears, switch to it or at least try it. | 6 | Process | Sits loose above the title, outside any section. |
| R2 | Each piece gets its own work folder; never build inside the skill folder. | 11 | Process | |
| R3 | Prove quality from frames, never from code. | 10-11 | Process | |
| R4 | Load this file, one mode, at most two engines, one or two craft files at a time. | 14-15 | Process | |
| R5 | Read `references/*` only when the current step names it. | 15 | Process | Partly at odds with R17, which always reads lessons.md before building. |
| R6 | Run `doctor.py` once at setup. | 36 | Process | |
| R7 | Put heavy temp files and models on a big drive (`VD_TMP`, `VD_MODELS`). | 36 | Fact | Workaround for C: filling up (7.8 GB). Dup of R281, R608. |
| R8 | Invent the look for each piece; never pick one off a shelf; never restrict style or method. | 37 | Direction | CONFLICT with R170 (offer 3 named looks). |
| R9 | Every song gets a new look, written as a new STYLE.md via style-protocol. | 38 | Direction | Dup of R739, R577. |
| R10 | Talking/YouTube: user picks brand kit or fresh look; save as `brand/STYLE.md` for reuse. | 39 | Process | |
| R11 | Measure each loved reference with `film_gate.py --json` (cuts/min, stillness, palette). | 41 | Process | |
| R12 | Gallery and `styles/` are inspiration only; never copy a look unchanged. | 42 | Direction | |
| R13 | `taste.jsonl` records rejections so they aren't repeated; never pushes toward a past look. | 43 | Process | |
| R14 | Ask five questions in one message, each with a default; "go" accepts all. | 44 | Process | |
| R15 | Print one routing line per scene: engine, why, cost (render minutes, tokens, credits). | 45 | Process | |
| R16 | Pick the lightest engine that passes a frame-first test; step up one if it misses; never start heavy. | 45 | Direction | |
| R17 | Before building, read lessons.md (talking: also talking/checks.md) and the user's checks.md; user's file wins. | 46 | Process | CONFLICT with R601 ("read this when you're stuck"). |
| R18 | Anything a word names appears at word start + 0.05 s, never before, at most 2 s after. | 47 | Direction | Board-sync rule made universal for every mode. Dup of R711, R660. CONFLICT with R186 (±0.2 s) and R713 (structure on screen from frame 0). |
| R19 | Nothing stays still for more than about 3 s. | 47 | Direction | Board rule made universal. CONFLICT with R732 (1.0 s is stricter), R43, R201 (~70 % of frames still), R377, R492 (verses hold 4–8 s), R619. Dup of R662, R714. |
| R20 | Nothing moves after it lands. | 47 | Direction | Board rule made universal. CONFLICT with R291, R424, R96, R585, and with gates R732 / R734 (a landed, unmoving frame fails them). Dup of R663, R715. |
| R21 | BRIEF.md in numbers: size, fps, palette hex, fonts with links, easing, feel card. | 48 | Process | |
| R22 | If any credits will be spent, stop for an explicit "yes" on the plan and its cost. | 49 | Safety | Dup of R49, R241, R312. |
| R23 | Render the signature moment in two contrasting treatments, one still each; user picks. | 51 | Process | |
| R24 | Then 3 stills at the hardest moments (signature, busiest transition, densest text), never the prettiest. | 52 | Process | |
| R25 | Self-check only facts: signature checklist and vetoes. | 53 | Process | |
| R26 | Fresh reviewer subagent scores stills on the rubric; fix until 80+, then show with the score. | 54 | Process | CONFLICT with R589 / R599 (at most 2 repair rounds, then report under 80). |
| R27 | Render draft picture muted, then mux the master WAV. | 55 | Fact | Dup of R284, R458. |
| R28 | Frame-exact joins and BT.709 tags on every render. | 55 | Fact | Dup of R454, R456. |
| R29 | Post each draft with known issues on top (review page), then fix. | 55 | Process | Dup of R521, R523, R72. |
| R30 | Run `film_gate.py`; HARD failures block delivery; SOFT numbers go to the reviewer. | 56 | Process | |
| R31 | Fresh subagent that never saw the code scores 12 muted frames + gate report; lower score counts. | 57 | Process | Dup of R594, R597. |
| R32 | Hand-off lists path, specs, gate results, both scores, one "next try" idea. | 58 | Process | |
| R33 | Append one line per job to `taste.jsonl`; never repeat an approved look. | 59 | Process | |
| R34 | Faces: similarity transforms only. | 63 | Fact | Workaround for shear (squeezed faces, TN). Dup of R159, R609. |
| R35 | No comic or halftone filters on emotional close-ups. | 64 | Direction | CONFLICT with R41 (no global style ban; no rule may cap a look); tension with R409 (halftone as a comic structure). |
| R36 | Text and graphics never cover a face. | 65 | Direction | Dup of R109, R261, R654, R490. |
| R37 | Never crossfade bodies or limbs; step drawings, or rotate about the joint and swap at the midpoint. | 67 | Direction | Stated universally. CONFLICT with R679 (fades fine for real-person cutouts in pitch films). Dup of R610. |
| R38 | Scale figures by a rigid feature in cm, never by bounding box. | 68 | Fact | Dup of R103, R611. |
| R39 | Feet sit on the floor. | 69 | Direction | |
| R40 | One coherent look per piece, invented for it; may evolve by section; STYLE.md sets its rules. | 70 | Direction | |
| R41 | No global style ban list; no engine or rule may cap a look; step up an engine, never water it down. | 70 | Direction | CONFLICT with R35; tension with mode-level bans (R193 … R202) and R403. |
| R42 | Every effect must name its meaning in one line, or be cut. | 71 | Direction | Dup of R624. |
| R43 | Quiet sections stay still so the peaks land. | 71 | Direction | CONFLICT with R19 and R732. |
| R44 | Repeats grow: keep the motif, restage it. | 71 | Direction | Dup of R93, R491, R623. |
| R45 | Borrow the mechanism, not the energy; re-derive motion from this song's tempo and emotion. | 72 | Direction | Dup of R618. |
| R46 | Every frame is f(t): no Math.random, Date.now or timers. | 73 | Fact | Renderers draw frames out of order. Dup of R270, R416. |
| R47 | Tempo, timing, scale and palette come from data, not guesses. | 74 | Process | |
| R48 | Label machine-aligned lyrics "not ear-checked". | 74 | Safety | Dup of R615. |
| R49 | Never spend credits without a "yes" on the plan and its cost. | 76 | Safety | Dup of R22. |
| R50 | Never print, log or commit an API key. | 77 | Safety | |
| R51 | Log every external asset in CREDITS.md with its licence. | 79 | Safety | Dup of R636, R324. |
| R52 | No NC-licensed assets in monetised work. | 80 | Safety | |
| R53 | Credit who did what (human vs which AI); tick the AI-disclosure box. | 81 | Safety | Unconditional. CONFLICT with R222 (disclosure only for realistic AI; not needed for 2D). |
| R54 | After a verified render, delete bundles, check frames, render temp; keep source and deliverables. | 82 | Safety | CONFLICT with R537 (never delete without the creator's OK on the exact list); partial overlap with R635. |
| R55 | Map each timestamp (incl. WIP notes and drawings) to its scene; open the marked frame first. | 85 | Process | |
| R56 | Pull frames from the latest render (`ffmpeg -ss`), or a strip around the moment. | 86 | Process | Uses `-ss`; R468 says `-ss` isn't frame-exact. |
| R57 | Name the real cause (camera, scale, crossfade, style, tempo, meaningless effect). | 87 | Process | |
| R58 | Fix at the cause; a bug in several scenes means fix the shared system. | 88 | Process | |
| R59 | Answer with frames; one decision at a time, recommended default pre-picked, plain question at end. | 89 | Process | |
| R60 | After each round, ask whether the bar moved from "correct" to "wow". | 90 | Process | Dup of R621. |
| R61 | Every complaint becomes a DO/DON'T line in `~/.video-director/checks.md` (never in the plugin) or a gate check. | 91 | Process | CONFLICT with R602 (adds to lessons.md) and R653 (adds to plugin's talking/checks.md). Dup of R167. |
| R62 | Offer to upstream general lessons to the plugin repo. | 91 | Process | |
| R63 | Suggest a better-fitting tool when it fits (hookline.cc, claude-video-2, huashu-art-motion, ae-builder). | 94-97 | Process | |

## modes/film.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R64 | Five questions with defaults: 60–90 s 16:9, your VO, code 3D, direct shot by shot. | 6-14 | Process | |
| R65 | Beat sheet and emotional spine first, then the shot list. | 17 | Process | Dup of R474. |
| R66 | Sound is the clock: record/generate VO or score first; build the timing map on it. | 18-19 | Process | |
| R67 | STYLE.md declares continuous camera or coverage cutting, at the top. | 20-21 | Process | |
| R68 | Block the whole piece with stand-ins on the real sound before any detail. | 24 | Process | |
| R69 | Shot by shot: question first, build their words literally, one shot per round. | 25 | Process | Dup of R351, R353. |
| R70 | Sign-off writes a scene spec and freezes the scene's data. | 27 | Process | Dup of R355. |
| R71 | Each scene builds from its spec and imports paths read-only. | 30 | Process | Dup of R356. |
| R72 | Post every draft to the review page with known issues on top. | 36-37 | Process | Dup of R29. |
| R73 | 9:16 cut-down re-lays out, never crops. | 40 | Direction | CONFLICT with R181 / R227 (Shorts are cropped). Dup of R126. |
| R74 | Deliver beat sheet + shot list in `docs/`, honest credits, AI disclosure, CREDITS.md. | 40-41 | Safety | |

## modes/music.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R75 | The mode is distilled from three films (Basement Goldfish, Toota Naksha, Jod Ke Dekh). | 3-6 | Case note | Frames the whole file as three films' practice. |
| R76 | Five questions word for word; defaults 16:9 + 2 Shorts, pure code, lyrics in-world/lanes, ~20 min render, 0 credits. | 8-15 | Process | |
| R77 | Run `song_facts.py --whisper` before planning. | 18-19 | Process | |
| R78 | Sanity-check the BPM against the felt tempo. | 27 | Process | |
| R79 | Tag every lyric word M / A2 (two sources within 0.3 s) / A1 / E. | 28-32 | Process | Dup of R547, R615. |
| R80 | Mixed scripts: two passes or creator's start list; sandwich unmatched words; ties by voice onset. | 33 | Case note | From JKD. Dup of R616. |
| R81 | Full mix: separate vocals first (Mel-Band RoFormer), then align the stem. | 34 | Process | |
| R82 | Suno songs: ask before spending credits on Suno's stems. | 34-35 | Safety | Dup of R538. |
| R83 | Whisper gives which word, not when: 0.5–0.8 s early on sung vocals. | 36 | Fact | Dup of R544. |
| R84 | Words a visual lands on get onsets snapped on the vocal-stem spectrogram, tagged M. | 37 | Process | Dup of R546. |
| R85 | Beats from drum-stem audio onsets, not drum MIDI. | 38 | Fact | Dup of R551. |
| R86 | Read sections off the energy curve; breakdowns = low energy, no kicks. | 39 | Process | |
| R87 | Tempo table: <75 breathe/phrase cuts/bloom; 75–110 beat/bar/pop; >110 punches/beat/slam. | 41-46 | Direction | |
| R88 | Above 110 BPM cut 1–2 frames before the beat; it reads on time. | 46 | Direction | Dup of R295. Tension with R427 (never before the cue). |
| R89 | Write feel.json + scene-plan rows; show it and get a yes. | 49-51 | Process | |
| R90 | Something striking in the first 1.5 s; title lands on the first measured hit. | 54 | Direction | |
| R91 | One signature moment: the frame people screenshot. | 55 | Direction | Dup of R151, R496. |
| R92 | A verse-1 motif returns transformed; ending echoes the opening. | 56 | Direction | Dup of R474, R151. |
| R93 | Chorus 2 keeps chorus 1's motif with new staging; never replay it. | 57 | Direction | Dup of R44. |
| R94 | Credits happen inside the story; no reusable credit card. | 58 | Case note | From JKD (R625). |
| R95 | Stillness is declared in feel.json `still` spans with a reason, never accidental. | 60 | Direction | |
| R96 | In any hold keep one thing alive (mist, grain, breath); a fully frozen frame reads as a bug. | 60 | Direction | CONFLICT with R20 / R715 and R571 (EDM drop "silent and still"). |
| R97 | Mark each timing as measured or estimated. | 62 | Process | |
| R98 | Animatic first: whole song at 480p, grey boxes + lyrics + cuts, with audio. | 65 | Process | |
| R99 | Run `film_gate.py` on the animatic (pacing, beat hits). | 66 | Process | |
| R100 | User approves the rhythm before any art is built. | 67 | Process | |
| R101 | Scene table is data `[from, to, scene, transition]`; every scene a pure function of t. | 72 | Process | Dup of R272. |
| R102 | Each plate gets horizon + vanishing points; px/cm = a·(y − horizon). | 74 | Case note | BG/TN plate method. Dup of R613. |
| R103 | Figures carry their own cm-per-px from a rigid feature. | 75 | Fact | Dup of R38. |
| R104 | Seated figures anchor on a seat point. | 76 | Case note | Dup of R613. |
| R105 | Two or three type voices in fixed lanes. | 78 | Direction | |
| R106 | Thin serif ≥ 74 px at 1080p, sans ≥ 60 px. | 79 | Direction | CONFLICT with R148 / R160 (≥ 70 px) and R670 (~52 px). |
| R107 | Soft scrim behind type. | 80 | Direction | |
| R108 | One key word per line in the accent colour. | 81 | Direction | |
| R109 | Type never over a face. | 82 | Direction | Dup of R36. |
| R110 | Lyrics inside the world on canvas textures with maxWidth auto-fit. | 83 | Direction | Dup of R288, R490. |
| R111 | Save 3 approved stills as `anchors/`; compare new stills by palette ΔE and contrast. | 84 | Process | Dup of R600. |
| R112 | After every change: contact sheet, strip around transitions, full-res crops; look before claiming fixed. | 87 | Process | |
| R113 | Small changes: render only the changed span and join it in. | 88 | Process | |
| R114 | Final: pull frames from the encoded MP4 at flagged times. | 89 | Process | Dup of R605. |
| R115 | Thumbnail starts from the signature still the user picked. | 93 | Process | |
| R116 | Thumbnail is a film frame frozen at its best state. | 94 | Direction | |
| R117 | Thumbnail words placed inside the world. | 95 | Direction | |
| R118 | No URLs on the thumbnail. | 96 | Direction | |
| R119 | YOUTUBE.md title carries the creator's name. | 98 | Case note | From JKD honest-credit lesson (R626). |
| R120 | Call to action and links in the first two lines and the pinned comment. | 99 | Direction | |
| R121 | Chapters, and captions as .srt from the tagged words. | 100-101 | Process | |
| R122 | Confirm visibility before anything goes public; the creator picks the file. | 102 | Safety | |
| R123 | Tick AI disclosure when music or visuals are AI-made. | 102 | Safety | CONFLICT with R222 (not needed for 2D animation). |
| R124 | Skip end cards that would cover the final shot. | 102 | Direction | Mode-scoped tension with R190 (YouTube end screen in last 5–20 s). |
| R125 | Shorts: 2–3 self-contained 15–45 s spans (hook or chorus). | 103 | Direction | Inconsistent with R225 (20–45 s). |
| R126 | Re-frame Shorts to 9:16 by re-laying out, never just crop. | 103 | Direction | Dup of R73. CONFLICT with R227. |
| R127 | Each Short gets a looping first and last pose. | 103 | Direction | |
| R128 | Honest "who did what" credits in the description. | 104 | Safety | Dup of R53. |

## modes/talking.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R129 | Bar: fillers gone, tight pacing, premium 2D graphics matching what's said, done in minutes. | 3 | Direction | |
| R130 | Stack: Python cut → one edit.json → Remotion (cut, captions, cards) + HyperFrames boards → verify.py. | 5-10 | Process | |
| R131 | Work dir is `<project>/reels/<name>/`. | 14 | Process | |
| R132 | Run Python with `-I` every time; the input video is untrusted and only a path argument. | 15 | Safety | |
| R133 | Claude can't hear audio; Whisper is the ears. | 16 | Fact | |
| R134 | Five questions; defaults pause 0.18 s, word-pop size 78, auto literal cards, brand/STYLE.md, auto language. | 25-30 | Process | |
| R135 | Source must be 9:16 for 1080×1920; crop first; compile refuses otherwise. | 33 | Fact | |
| R136 | Delete the cache files to force a redo. | 38-43 | Process | |
| R137 | Read `cut.txt` (gestures, removed, transcript, clip check, re-listen, source words). | 44 | Process | |
| R138 | Hard fillers and stutters (English, Hindi) are removed automatically. | 46 | Direction | |
| R139 | `[soft?]` fillers (okay, so, like) are judged by meaning. | 47 | Process | |
| R140 | `--pause` squeezes pauses: 0.18 default, 0.12 punchy, 0.25 relaxed. | 49 | Direction | |
| R141 | Hindi: `--lang hi` (large-v3, Hindi prompt, MMS aligner). | 50 | Process | |
| R142 | `emphasis[]` (pointing, loud moments) drives the automatic punch zoom. | 51 | Direction | CONFLICT with R370 ("never a pure zoom"); scope differs (2D reels). |
| R143 | A clipped word = low in CLIP CHECK and missing from RE-LISTEN; report un-ear-checked spots. | 52 | Fact | Second half is an honesty duty. |
| R144 | Literal over abstract: when the speaker names a thing, show it. | 55 | Direction | Dup of R657, R186. |
| R145 | HF board: start from `hf-board/`, read boards.md, run `hyperframes check --json` first. | 69 | Process | |
| R146 | Whisper mishears go in `fix`. | 71 | Process | |
| R147 | Captions: word-pop, 1–3 words. | 74 | Direction | |
| R148 | Caption size defaults to 78, never below 70. | 75 | Direction | CONFLICT with R670 (~52 px at 1080p in pitch films). Dup of R160, R655, R724. |
| R149 | Accent on key words and numbers. | 76 | Direction | |
| R150 | Unspoken words in a chunk shown at 45 % opacity. | 77 | Direction | CONFLICT with R688 (captions at full ink from their first frame). |
| R151 | Shape: hook on first content word, one signature moment, end echoes open, stillness between. | 80-83 | Direction | "Stillness between" is in tension with R19 / R732. |
| R152 | Show the plan in a few lines; ask only when a cue is ambiguous. | 85 | Process | |
| R153 | URL capture isn't automated: fetch the image or ask for it. | 85 | Fact | |
| R154 | `--concurrency 4` is the sweet spot. | 93 | Fact | |
| R155 | After a full render, open `sheet.jpg` before claiming anything. | 94 | Process | |
| R156 | FACE/CARD OVERLAP warnings: change the card's `y` or `until`, or shorten its neighbour. | 95 | Process | |
| R157 | Keep listed source/output files; delete preview.mp4. | 96-97 | Safety | Pre-listed deletion. |
| R158 | Cuts land in silence; never widen a snap window past ~50 ms. | 101 | Direction | |
| R159 | Faces: uniform scale and shift only; compile enforces the lanes. | 102 | Fact | Dup of R34. |
| R160 | One caption lane, one card lane, accents from the look, ≥ 70 px at 1080 wide. | 103 | Direction | Dup of R148. CONFLICT with R670. |
| R161 | Small graphic = new Remotion card; slide-sized = HyperFrames board. | 104 | Process | |
| R162 | After touching cut logic, run `test_prep.py`. | 105 | Process | |
| R163 | Honest limits: aligner edges ±30–50 ms, not ear-checked; gesture emphasis is a guess. | 107-108 | Fact | |
| R164 | Feedback: take the timestamp, run `--range a:b --preview`. | 111 | Process | |
| R165 | Name the cause: word ref, lane, face box or zoom. | 112 | Process | |
| R166 | Recurring → fix compile.mjs; one moment → fix edit.json. | 113 | Process | |
| R167 | Add the lesson to `~/.video-director/checks.md`, never inside `$SKILL`. | 114 | Process | Dup of R61. CONFLICT with R653. |

## modes/youtube.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R168 | Follow the hub front door and rules (not repeated here). | 4 | Process | |
| R169 | Use AI clips only for b-roll that can't be filmed or found. | 5 | Direction | |
| R170 | Offer a shortlist of 3 looks: clean-talk, explainer, documentary. | 8-9 | Direction | CONFLICT with R8 ("never pick it off a shelf") and R10. |
| R171 | Target length = the cut, never padded. | 10 | Direction | |
| R172 | 16:9 1920×1080 at source fps, plus 2 Shorts. | 10 | Direction | |
| R173 | At most 2 grammars besides the face. | 11 | Direction | |
| R174 | Thumbnail with face: yes (default). | 11 | Direction | |
| R175 | Captions as CC; burned in only on Shorts. | 12 | Direction | |
| R176 | Mix ≈ −14 LUFS integrated, true peak ≤ −1 dBTP, music bed 15–20 dB under voice. | 12-13 | Direction | |
| R177 | Narration-only: wrap in a black video first, then cut; ignore "0 faces". | 20 | Process | |
| R178 | `--pause` 0.22–0.3 for long-form; run long footage in the background. | 23 | Direction | |
| R179 | compile.mjs throws on aspect mismatch; long-form builds its own 16:9 Remotion comp. | 28-30 | Process | |
| R180 | `"size": [1920,1080]` passes but lanes were tuned on 9:16: untested, preview every card. | 31-32 | Fact | |
| R181 | Never crop the main long-form to 9:16; crop only for Shorts. | 33 | Direction | CONFLICT with R73 / R126 (never crop). |
| R182 | 0–5 s: open on the payoff; first word ≤ 0.5 s; visual change by 2 s; no logo, no "welcome back". | 38 | Direction | |
| R183 | 5–30 s: the promise and why to trust it; content starts by 30 s. | 39 | Direction | |
| R184 | Re-hook every 60–90 s at a chapter start. | 40 | Direction | |
| R185 | Something new on screen every ≤ 20 s; punch-in 1.1–1.2× on sentence breaks. | 41 | Direction | CONFLICT with R370 (never a pure zoom). |
| R186 | Named thing → b-roll on the word ±0.2 s, 2–6 s long, L-cut. | 42 | Direction | CONFLICT with R18 / R427 (never before the word). |
| R187 | Cut tangents, retakes and "so that's it / to wrap up". | 43 | Direction | |
| R188 | Chapters: ≥ 3, first at 0:00, each ≥ 10 s (YouTube rule). | 44 | Fact | |
| R189 | Chapters aim 1–4 min each; chapter card 1.5–2.5 s. | 44 | Direction | |
| R190 | Last 5–20 s: verbal CTA to one named video; frame clear for end screen; no captions/cards. | 45 | Direction | Mode tension with R124. |
| R191 | The video must be ≥ 25 s for an end screen. | 45 | Fact | |
| R192 | One grammar per segment; switch only at a segment boundary. | 48 | Direction | |
| R193 | t1 3b1b: black ground, transform concept to concept, 1–3 s move + 1 s hold; ban glow, bloom, blue gradient. | 51 | Direction | Tension with R41. |
| R194 | t2 keynote: one thing per screen, push into the named part, spring ≤ 0.15; ban glass card on dark. | 52 | Direction | |
| R195 | t3 chart: axes → data → annotate one; ~1 s per step; hold number ≥ 0.5 s; one story colour; no 3D/bouncy charts. | 53 | Direction | |
| R196 | Bars start at 0; a line axis not at 0 says so on screen. | 53 | Safety | Honest data. Dup of R214. |
| R197 | y1 Kurzgesagt: one concrete glowing object, log zoom, dark ground + 2–3 glows, 7–9 s shots; ban breathing-everything, linear zoom. | 54 | Direction | |
| R198 | y2 Vox: real material on a paper desk, 12 fps highlighter, hard cuts, black/paper/one red. | 55 | Direction | |
| R199 | No fake "archives" when no real source exists. | 55 | Safety | |
| R200 | y3 whiteboard: write ~0.5 s behind the phrase; camera ~0.23 frame width; pull out at end; no wipe per point. | 56 | Direction | |
| R201 | y4 storytime: pose swap in 0.1 s, then hold (~70 % of frames still); reaction CU ≥ 0.8 s; 2× jump or slam. | 57 | Direction | CONFLICT with R426 (6–12 frame entrances), R19, R377, R732, R734. |
| R202 | y5 kinetic type: key word slams on stress, ratio ≥ 3:1, one thing at a time, text pins 0.35 s after landing; ≤ 5 items. | 58 | Direction | |
| R203 | The face is the default grammar; animate only where a picture explains better. | 61 | Direction | |
| R204 | Real screenshots full frame, scaled uniformly, never cropping key UI. | 62 | Direction | |
| R205 | Only one number → no chart; a big count landing as it's spoken. | 63 | Direction | |
| R206 | 2–5 cues per 3–8 s segment; first cue visual; ≤ half text; on-screen text ≤ 6 words. | 64-65 | Direction | |
| R207 | In text grammars (t1, t3, y3, y5) move or drop burned captions. | 65 | Direction | |
| R208 | One focus per frame; background one step lower in saturation and contrast. | 68 | Direction | |
| R209 | Structure → data → annotation; colour = concept; ≤ 3–4 meaning colours. | 69 | Direction | CONFLICT with R664 (one accent per clip). |
| R210 | Count start = spoken time − count length; reveal frame sits on the word. | 70-71 | Direction | |
| R211 | In 0.3–0.4 s, out ~0.18 s; hold ≥ 0.5 s after a number, ≥ 0.9 s after a punchline. | 72 | Direction | |
| R212 | Move camera only when the eye must go somewhere new: 0.6–1.5 s glides; push 0.28 s / slam 0.17 s for reveals. | 73-75 | Direction | CONFLICT with R291 (always drifting). |
| R213 | Real material goes full frame and unaltered. | 76 | Safety | |
| R214 | Data honest (units, source, bars from 0); label made-up data "illustrative" on every shot. | 76-77 | Safety | |
| R215 | Check wording against the picture ("8.7× as much" ≠ "up 8.7×"). | 77 | Safety | |
| R216 | Thumbnail 1280×720 JPG/PNG, ≤ 2 MB. | 80 | Fact | |
| R217 | Thumbnail from a real frame: emotional face, ≤ 3 words not repeating title, accent, reads at 168×94. | 80-81 | Direction | Test size differs from R386 (360 px) and R591 (160 px). |
| R218 | Title ≤ 60 chars visible (100 max); promises what the hook pays; no bait. | 82 | Direction | "No bait" is an honesty point. |
| R219 | Description: first 2 lines promise + key link; then chapters, credits, music licence. | 83-84 | Direction | |
| R220 | Pinned comment: one question or a link to the next video. | 85 | Direction | |
| R221 | Upload an SRT from `words.json` (after `fix`) as CC. | 86 | Process | |
| R222 | Tick "altered or synthetic" only for realistic AI people/places/events/voices; not for 2D, captions, cuts, colour. | 87-88 | Safety | CONFLICT with R53 and R123 (tick whenever AI-made). |
| R223 | Name the AI parts in the description; never pass AI shots off as real footage. | 88-89 | Safety | |
| R224 | Write `upload.md`: 3 titles, description, chapters, pinned comment, thumbnail path. | 90 | Process | |
| R225 | Shorts: 2–3 standalone moments, 20–45 s; start on the strongest line. | 93-94 | Direction | Inconsistent with R125 (15–45 s). |
| R226 | New hook card ≤ 6 words, on screen 0–2 s. | 95 | Direction | |
| R227 | Reframe Shorts to 9:16 by cropping on the median face cx (formula given). | 96-98 | Process | CONFLICT with R73 / R126. |
| R228 | Re-run prep.py on each crop; then talking-mode plan and render. | 99-100 | Process | |
| R229 | Shorts: no end screen; loop end into start if natural; link the long video. | 101 | Direction | |
| R230 | Never claim a pass without running gates; run on every Short; exit 1 = fix and re-run. | 103-105 | Process | |
| R231 | HARD dead_gap: no visible change for > 1.0 s. | 106 | Direction | Dup of R732. |
| R232 | HARD flicker: two luma spikes < 0.17 s apart. | 107 | Direction | Dup of R733. |
| R233 | HARD slideshow: under 60 % of shots with in-shot motion. | 108 | Direction | Dup of R734. |
| R234 | A held screen or chart failing dead_gap: zoom or cut to the face. Do not argue with the gate. | 109-110 | Process | CONFLICT with R629 ("a gate that fails good work gets fixed, not obeyed"), R394, R471. |
| R235 | Retention self-check: list every new visual/info time; any gap > 20 s is a flag. | 112-113 | Direction | |
| R236 | Also check: visual by 2 s, content by 30 s, re-hook ≤ 90 s, chapters, end zone, numbers match voice. | 114-115 | Process | |
| R237 | Hand-off lists unfixed flags and spots no one checked by ear. | 116 | Safety | |

## engines/ai-clip.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R238 | AI clips for a few shots only, where they earn it (skin, cloth, water, crowds, performance); rest in code. | 3 | Direction | |
| R239 | Pick the model by the shot's hardest need; read the MCP's current model list, not memory. | 11 | Process | |
| R240 | Write `shots.json`, one row per AI shot with est_credits. | 19 | Process | |
| R241 | Show the table with the total, then STOP for an explicit "yes". | 20 | Safety | Dup of R22. |
| R242 | Generate one shot at a time; inspect each before the next. | 21 | Process | |
| R243 | Log seed, model, prompt file, credits spent, verdict for each generation. | 22 | Process | |
| R244 | Prompt order: format + event, reference roles, cast/props, camera rule, timed paragraphs, ending backwards, continuity. | 25-35 | Process | |
| R245 | Pick keyframe mode in the tool; prose doesn't replace it. | 27 | Fact | |
| R246 | Few exclusions, only for failures actually seen; spend words on positive mechanisms. | 35 | Direction | |
| R247 | Keep a private state ledger per beat; entrances use declared routes. | 37 | Process | |
| R248 | Always state the sound; music videos usually want the clip silent. | 39 | Direction | |
| R249 | Add a sentence only if it removes an ambiguity; count pasted characters against the limit. | 41 | Process | |
| R250 | Inspect 3 frames minimum, then step the risky moments. | 43-45 | Process | |
| R251 | Write what actually happens; never report the planned action as seen. | 46 | Safety | |
| R252 | Classify the failure, revise the earliest broken event, one change per retry. | 47-55 | Process | |
| R253 | After 3 failed retries on one mechanism, simplify it or cut to a code shot. | 57 | Direction | |
| R254 | Chain shots: last frame of clip N is the first frame of N+1. | 60 | Process | |
| R255 | Reuse one character sheet as identity reference; never re-describe the face in prose. | 61 | Direction | |
| R256 | Fix bad endings in the cut (2-frame trim, cut on motion). | 63 | Direction | |
| R257 | Match fps and size; grade AI shots to the STYLE palette. | 66 | Process | |
| R258 | One finish pass (grain, vignette, halation) over AI and code shots alike. | 67 | Direction | |
| R259 | Lyrics and type always rendered in code over the clip; never ask the model for text. | 68 | Direction | |
| R260 | Cut on the beat grid; speed-ramp at most ±15 %. | 69 | Direction | |
| R261 | Check every face frame for drift; no text over faces. | 70 | Direction | Dup of R36. |
| R262 | Log model and prompt in CREDITS.md; tick AI disclosure. | 71 | Safety | Dup of R53. |
| R263 | Draft tier first (3–5 s); hero model only once the mechanism works. | 74 | Process | |
| R264 | Generate the hardest shot first. | 75 | Process | |

## engines/code.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R265 | HyperFrames is the default for new 2D work. | 6 | Direction | |
| R266 | On the next 3D film, trial three.js inside HyperFrames; switch if frames match. | 6 | Process | |
| R267 | three.js only when the world is the story; full renders take 20–25 min. | 8 | Direction | |
| R268 | p5.js: avoid for high-res close-ups; slow without a GPU. | 9 | Fact | |
| R269 | Install the official HyperFrames and Remotion agent skills; their API rules beat memory. | 11-15 | Process | |
| R270 | Every frame is render(t): no state between frames, seeded RNG, no Date.now/timers/rAF. | 18-21 | Fact | Dup of R46. |
| R271 | Guard every search loop; a t-dependent infinite loop hangs Remotion. | 22 | Fact | Dup of R633. |
| R272 | The song is the only clock; scene table is data; scenes export build/update. | 23 | Process | |
| R273 | Free fonts only, via `<link>` or `@remotion/google-fonts`; never copy paid font files. | 25-27 | Safety | |
| R274 | In HyperFrames, if you link any font, link every font. | 26 | Fact | |
| R275 | Media lives in project `media/` or `public/`; never touch the user's originals. | 28 | Safety | |
| R276 | HF structure: one root div with data attrs, one paused GSAP timeline, `class="clip"` media. | 31-34 | Fact | |
| R277 | HF lint / snapshot / render commands; `--gpu` when NVENC is available. | 35-38 | Process | |
| R278 | Time-varying text changes inside the timeline (onUpdate), never `gsap.set` on innerHTML. | 39 | Fact | |
| R279 | Engine is plain ES modules `renderFilm(ctx, t)`; Remotion only hosts it (h264 CRF 17). | 42 | Direction | |
| R280 | One shared WebGL2 context; reset its state after every pass. | 43 | Fact | |
| R281 | TEMP/TMP = VD_TMP; Chrome profiles once filled C: with 7.8 GB. | 44 | Fact | Dup of R7. |
| R282 | Remotion stills (bundle once) and render `--concurrency=4`. | 46-47 | Process | |
| R283 | Tail render with ~12-frame pre-roll; join by decode+encode, never `concat -c copy` (21 ms late). | 48-50 | Fact | Dup of R454. |
| R284 | Render picture muted; mux master WAV from 0 (Remotion AAC 42.7 ms late). | 51 | Fact | Dup of R27. |
| R285 | One renderer; transitions composite in linear HDR before bloom. | 54 | Direction | |
| R286 | Subframe blur: average n renders with `autoClear = false`, else it comes out dark. | 56 | Fact | Dup of R632. |
| R287 | Post: bloom + one finish shader (vignette, grain, fade). | 57-58 | Direction | |
| R288 | Lyrics on canvas textures in the world; mirrored floors need render layers. | 59 | Direction | Dup of R110. |
| R289 | Pin the three.js version (0.186 removed PCFSoftShadowMap). | 60 | Fact | Dup of R438. |
| R290 | Hero bodies: rigged mesh posed by FK or Blender; judge poses from 3 angles with real props. | 61 | Case note | From JKD's hand (R628). |
| R291 | Camera micro-drift 0.3–0.8 % frame width/s + 2–4 frame settle; a dead-still camera reads as slideshow. | 64 | Direction | CONFLICT with R715, R212, R377 (dead-still allowed 1–2 beats), R567 (lo-fi "static"). |
| R292 | One key, one rim, warm/cool contrast between sections. | 65 | Direction | |
| R293 | Lens pass only on close-ups; grain 2–4 % on everything. | 66 | Direction | |
| R294 | One element listens to the kick; the rest follows section arousal. | 67 | Direction | |
| R295 | Cut on motion; land hits on the beat; cut 1–2 frames early. | 68 | Direction | Dup of R88. |
| R296 | Parallel agents: split by file ownership, wire stubs first, separate project copies. | 71-74 | Process | Dup of R627. |
| R297 | Each agent brief carries song facts, feel card, STYLE, anchors, rules, files, verification. | 75-82 | Process | |
| R298 | Shared files: read before each edit, small anchored edits, never rewrite a whole file. | 83 | Process | |
| R299 | Steer mid-flight with short notes. | 84 | Process | |
| R300 | Coordinator owns scene table, transitions, bookends and seams; thins one layer on a shared hit. | 85 | Process | |
| R301 | Windows: heredocs and sed eat quotes; write patch scripts to files. | 88 | Fact | Dup of R631. |
| R302 | CLIs that split on `=` mangle args; use `front:0.1`. | 89 | Fact | Dup of R631. |
| R303 | Read errors literally; ENOSPC means find where the disk went. | 90 | Process | Dup of R608. |

## engines/guide-3d.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R304 | Use a 3D guide whenever a shot needs a precise camera, choreography, or several angles. | 8 | Direction | |
| R305 | Run only one Blender MCP (both use port 9876). | 16 | Fact | Dup of R649. |
| R306 | No MCP: headless Blender; keep scripts in `blender/` so every shot regenerates. | 17 | Process | |
| R307 | Scripting: shader nodes by type, read enums, colours on node inputs, size from world_bounding_box. | 18-22 | Fact | |
| R308 | Blockout at real scale, grey clay, one key light, scene fps = film fps. | 25 | Process | |
| R309 | Camera keys on downbeats, Bezier ease-in-out, 2–4 frame settle, real lens (24/35/50/85). | 26 | Direction | |
| R310 | 480p clay animatic with the song; user approves camera and timing before any credit. | 27 | Process | Dup of R319. |
| R311 | Export guides per shot, one job each (first/last, depth, lines, clay). | 28-31 | Process | |
| R312 | The credit gate applies to generation. | 37 | Safety | Dup of R22. |
| R313 | Coverage for free: render the same blockout from a second camera. | 38 | Direction | |
| R314 | Dance reference: only footage the user filmed/owns/has permission for; no celebrity likeness; no copied routine as selling point. | 41 | Safety | |
| R315 | Rokoko free tier is 30 s/month. | 46 | Fact | |
| R316 | Snap key poses to beats in the NLA; clean mocap isn't on beat by itself. | 50 | Direction | |
| R317 | On the clay render check foot sliding and hand-face intersections before generating. | 51 | Process | |
| R318 | Photo blockout: project the photo onto the blockout; move camera within ~15° of the original view. | 55 | Direction | CONFLICT with R322 (never project the reference into the scene). |
| R319 | Show the clay animatic with the song before any credits. | 60 | Process | |
| R320 | Compare AI clip vs clay at 3 matched times, within a few % of frame; drift → change mode, not prose. | 61 | Process | |

## engines/recreate.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R321 | Blender is the default; Unreal 5.8 optional (took 3–4× the time). | 5-6 | Direction | |
| R322 | Never alter or project the reference into the scene; never put its frames inside. | 11 | Safety | CONFLICT with R318. |
| R323 | Anything the clip never shows can be inferred, but is logged as inferred. | 11 | Safety | |
| R324 | Procedural or CC0 assets only; log every import in CREDITS.md. | 13-14 | Safety | Dup of R51. |
| R325 | No paid assets, APIs or cloud jobs without a "yes". | 15 | Safety | |
| R326 | New project folder per recreation; save a working state before every big push. | 16 | Process | |
| R327 | Generator scripts in `blender/gen_*.py`; every mesh regenerable. | 17 | Process | |
| R328 | Write REFERENCE.md and keep going; no approval stop. | 19 | Process | |
| R329 | Extract frames every 0.5 s (finer on fast motion); view them upscaled. | 20 | Process | |
| R330 | Inventory every object > ~2 % of frame, sized against a ruler (door 2.0 m, desk 0.75 m). | 23 | Process | |
| R331 | Blockout target: running and saved in 30–60 min. | 29 | Direction | |
| R332 | Composition and camera locked before any detail work. | 32 | Process | |
| R333 | Detail passes in the order the eye reads (silhouette → secondary → surface → light → motion). | 34-39 | Process | |
| R334 | Repeated items from one seeded generator; never hand-place copies. | 41 | Direction | |
| R335 | Compare at least start, ¼, ½, ¾ and end of the reference. | 44 | Process | |
| R336 | Colour check per region, plus judge layout and silhouettes by eye. | 46 | Process | |
| R337 | Each pass: 5 biggest differences, fix, re-render; at most 3 passes, then reassess. | 47 | Direction | |
| R338 | At least one off-axis angle and one lighting change. | 51 | Direction | |
| R339 | Unreal branch: playable mode with `Play.bat` and `Open_Editor.bat`. | 56 | Direction | |
| R340 | BUILD_LOG.md with milestone times, compare passes, measured times, defects. | 59 | Process | |
| R341 | Final report: matched vs inferred, 3 biggest mismatches, performance, file list. | 60-64 | Process | |
| R342 | Never invent token counts or costs. | 66 | Safety | |

## craft/blocking.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R343 | One data file per scene + a cast list; times in film frames on the song clock. | 9-10 | Process | |
| R344 | Parent change hands over in world space with speed and acceleration matched. | 11-13 | Direction | |
| R345 | Interpolation passes through keys, C2, monotone; per-key stop/hold/gravity. | 14-15 | Direction | |
| R346 | Scenes tile the song with no gaps; boundary key identical in both; one track per object. | 16-17 | Process | |
| R347 | Pure readers only; every lookup refuses an unknown id. | 18-19 | Fact | A fall-through turned every text card into cloth. |
| R348 | Stand-ins flat (no materials/fog/shadows/post); nothing near the hero in the hero's colour. | 20-21 | Direction | |
| R349 | Slow motion = one world-clock per scene; camera and song stay on the song clock. | 22 | Direction | |
| R350 | Blocking clips: muted 720p, song muxed from WAV, each shot playable alone. | 23 | Process | |
| R351 | Every shot starts with a question; build nothing ahead of the answer. | 26-27 | Process | Dup of R69. |
| R352 | Build the creator's words literally (word-to-number table). | 28 | Process | Dup of R365. |
| R353 | One shot per round; change nothing else. | 29 | Process | Dup of R395. |
| R354 | Fast ≠ no checks: smoothness, every frame, objects out of frame, hero seen ≥ 50 %, nothing over head. | 30-32 | Process | |
| R355 | On sign-off, write the scene spec and freeze its data. | 33 | Process | Dup of R70. |
| R356 | Scene sessions import paths read-only, never copy them; ask the blocking owner. | 36-38 | Process | |
| R357 | Any change to camera, staging, set or timing unchecks every note row. | 51 | Process | Dup of R507. |
| R358 | Data check flags gaps, mismatched keys, unknown ids; probes every round; camera identical once built. | 55-56 | Process | |

## craft/camera.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R359 | Don't ship the observer shot (eye level, 2–4 m, mid lens, centred, no fg/bg). | 8 | Direction | |
| R360 | Don't ship one axis, one speed (a straight push or pull). | 9 | Direction | |
| R361 | Don't ship waypoint-and-stop (arrive, hold, move, hold). | 10 | Direction | |
| R362 | Don't ship a stick camera at fixed offset from the subject. | 11 | Direction | |
| R363 | Don't ship 35–45° look-downs, same size all section, or nudges under ~0.3 m / ~10°. | 12 | Direction | |
| R364 | No creeping zoom in holds; hold the framing with slight kick shake. | 13 | Direction | |
| R365 | Never soften the creator's words; use the word-to-number table. | 14 | Process | |
| R366 | One shot card per move: "From …, move so we reveal/follow/feel …, landing on …"; "show" alone = no reason. | 17-19 | Process | |
| R367 | Variety pass: neighbouring waypoints differ in 2+ columns. | 21 | Direction | |
| R368 | Frame sheet every 2–4 frames + each waypoint still; then watch at speed with the song. | 22-23 | Process | Tension with R393 and R435 (sheets hide pops). |
| R369 | Each move changes something big (size ×2, 45° orbit, 1 m height, reveal). | 26 | Direction | |
| R370 | Two axes, one leading; never a pure zoom or a pan from a fixed spot. | 27 | Direction | CONFLICT with R142 / R722 (auto punch zoom), R185 (punch-ins), R197 (log zoom). |
| R371 | Parallax always: something 0.5–3 m from the lens crosses 20 %+ of frame. | 28 | Direction | |
| R372 | Wide close or long far; avoid mid lens at mid distance; never zoom to enlarge. | 29-30 | Direction | Tension with R479 (35 mm storytelling, 50 mm neutral). |
| R373 | Height near level, ≤ 20–25° down, horizon in frame; steep top-down only a short beat. | 31 | Direction | |
| R374 | Subject travels through frame: under ~60 % of a move in the middle third. | 32 | Direction | |
| R375 | Moves start/land on beats; slow (never stop) through held notes; turn ≤ ~10°/frame. | 33-34 | Direction | |
| R376 | Each parameter changes one way; slerp look directions, never lerp a look-at point. | 35-36 | Direction | |
| R377 | Never dead: a hold is slow drift or beat shake; dead-still only 1–2 beats a section. | 37 | Direction | CONFLICT with R201, R715, R481 ("locked-off awe"). |
| R378 | The shot comes first; nothing about a lyric may move, slow or aim the camera. | 38-39 | Direction | CONFLICT with R481 ("push-in … land on the lyric"); tension with R549. |
| R379 | Continuous camera: a shot change is a fast whip/arc/pull-out with blur. | 42 | Direction | |
| R380 | World change = push into a shape; a plain dissolve reads as a shortcut. | 43-44 | Direction | Scoped tension with R489 (dissolve for time/memory). |
| R381 | Through an object: travel through real geometry; no white flash. | 45 | Direction | |
| R382 | Cut only when asked or behind a full-frame push; pose/facing/gaze match both sides. | 46 | Direction | Scoped tension with R488 ("plain cut is the default and strongest"); STYLE.md picks which applies. |
| R383 | Shot-size definitions (ECU ≥ 60 % width … EWS < 10 % height); neighbours differ by one size or 45°+. | 50-51 | Direction | |
| R384 | Eyes on upper third; lead room ≥ ⅓; centre only for symmetry. | 52 | Direction | Tension with R670 (seat early speakers in the middle). |
| R385 | 2+ of 3 layers; nothing important within 5 % of an edge; crop between joints; roll 0. | 53-54 | Direction | |
| R386 | One-glance story: at 360 px wide the frame says the idea. | 55 | Direction | Test size differs from R591 (160 px) and R217 (168×94). |
| R387 | Creator-word table ("at the edge" ≥ 0.9 width, "close-up" head ⅓–½, …). | 57-64 | Direction | |
| R388 | Balance table from three finished films (still 30–40 %, 4.9–6.9 moves/10 s…), reference not target. | 66-73 | Case note | |
| R389 | Shared shape: quiet verses (3–7 s holds), energy saved for chorus, long still stretch near the end. | 74-75 | Case note | Tension with R19. |
| R390 | Probes: turn ≤ 90°/s, ≤ 250°/s², speed change ≤ 12 m/s² (4 slow), travel ≤ 300°/s, no reversal. | 78-79 | Direction | |
| R391 | Image speed < ~120 px/frame at 1080p except whips. | 80 | Direction | |
| R392 | Subject seen ≥ 50 % every frame; no pass nearer than ~0.3 m unless designed. | 81 | Direction | |
| R393 | Never approve camera from 3–8-frame sheets; step every frame of the shot. | 91 | Process | |
| R394 | Never answer the creator's eye with a metric; a disagreeing number is a broken metric. | 92 | Process | CONFLICT with R234. |
| R395 | A camera round touches only frames the note names; diff the rest. | 93 | Process | |
| R396 | Sparse orbit keys stall; key a computed path or interpolate in angle. | 94 | Fact | |

## craft/light.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R397 | STYLE.md may overrule any of this on purpose; a flat graphic look is a choice. | 5-6 | Direction | Softens R403 etc. |
| R398 | Time of day per beat (dawn hope, golden hour love, blue hour reflection, night warm pools). | 9 | Direction | |
| R399 | Motivate every light; key + rim + eye light in close-ups; flat even light is the biggest "game" tell. | 10-11 | Direction | |
| R400 | Palette arc across the film; 2–3 hues a scene. | 12 | Direction | |
| R401 | Haze and depth fog for scale and memory. | 13 | Direction | |
| R402 | Real PBR textures on every surface (Poly Haven CC0), texel density for closest framing, logged. | 16-17 | Direction | |
| R403 | Keep it dark: sets and crowds muted, lit only by real sources. | 18 | Direction | CONFLICT with R567 (Pop: bright sets), R569 (lightness +10 %), and light pitch-film rooms (R676: cream backgrounds). Scoped to 3D; R397 applies. |
| R404 | Only real light sources glow; all else emissive 0; emissive < ~0.4 usually fakes light. | 19-20 | Direction | Tension with R197 (glowing object, glow accents) in 2D. |
| R405 | three.js: decay 2 + distance; RectAreaLight has no range or shadow; no camera-side fill. | 21-23 | Fact | "No camera-side fill" is a taste default. |
| R406 | A dark space, not a void: floor/haze lit by the scene's sources. | 24 | Direction | |
| R407 | Judge colour in the film's light; sample the rendered pixel. | 25-26 | Process | |
| R408 | Stylised form, real colours from photos; never fit a sculpt to photos. | 27-28 | Direction | |
| R409 | A style needs structure, not a filter (comic: ink outlines, screen-fixed halftone, one accent per character). | 29-30 | Direction | Tension with R35. |
| R410 | Separation: one focal value, warm vs cool, palette per place, colourblind-safe. | 31 | Direction | |
| R411 | Solo each light and measure what it adds; don't name causes from a list. | 34 | Process | |
| R412 | Look at leaked mask pixels before reporting an audit. | 35 | Process | |
| R413 | Big white surfaces (LED wall) cause a bloom veil. | 36 | Fact | |
| R414 | List every emissive and light before a lighting pass; zero fakes; zoom dark areas for banding. | 39-40 | Process | |

## craft/motion.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R415 | Physical state re-simulated from t=0 on a fixed 1/120 s step, or baked. | 9-10 | Fact | |
| R416 | Seeded noise only; one timeline owns timing, never a shader's hidden clock. | 11 | Fact | Dup of R46. |
| R417 | Each action takes one `speed` scaling all its phases. | 12 | Direction | |
| R418 | Move grammar table: hold / anticipation / action / overshoot / settle (cartoon vs realistic timings). | 24-31 | Direction | Anticipation before action is in tension with R427. |
| R419 | Nothing alive moves linearly; pushed = ease-out, falling = ease-in; impacts never eased to a stop. | 32 | Direction | |
| R420 | Settles start with zero slope (formula, k≈6, w≈14). | 33 | Direction | |
| R421 | Moves on arcs; body as a chain; loose parts lag on springs; continuous velocity. | 36-37 | Direction | |
| R422 | Action moves the material it acts on; carry displaced state; idle wobble isn't a reaction. | 40-43 | Direction | |
| R423 | Music-driven accents land on the beat, not peak late. | 44 | Direction | |
| R424 | Alive is never static: breathing 4–5 s, idle noise 1–2°, weight shifts; check a 6 s rest loop. | 47-48 | Direction | CONFLICT with R20 (if applied to figures) and R201 ("truly hold"). |
| R425 | Gravity accelerates; impacts: contact frame at peak speed, compression, rebound; touched things react. | 51-53 | Direction | |
| R426 | Every entrance animates over 6–12 frames; type letter by letter where it fits. | 56 | Direction | CONFLICT with R201 (pose swap 0.1 s), R677 (wake in 5 frames), R680 (hide, not fade), R202 (slam). |
| R427 | Starts on its cue, never before; no readable wind-up before the cue. | 57 | Direction | Dup of R18. Tension with R88 and R418. |
| R428 | Hidden ≠ absent: an edge-on card flipping in its last half frame is still a pop. | 58 | Fact | |
| R429 | Grow out, never through; scaling depth up from 0 z-fights. | 59-60 | Fact | |
| R430 | Exits leave the frame or animate out. | 61 | Direction | |
| R431 | Cartoon shapes smear over the last ~0.07 s; realistic people get motion blur instead. | 64-65 | Direction | |
| R432 | Contacts: sweeps clear props, hands land, feet don't slide, nothing passes through. | 68-69 | Direction | |
| R433 | Verify chain: typecheck → probe → draft → spike scan → step frames → 100 % crops → watch as loop. | 72-73 | Process | |
| R434 | Compare a reaction with the stimulus off. | 74 | Process | |
| R435 | Every-Nth-frame sheets hide strobing and one-frame pops. | 75 | Fact | Tension with R368. |

## craft/render.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R436 | Prove it renders cheaply first: typecheck, load modules, bundle, render one real frame. | 8-9 | Process | |
| R437 | Render long jobs from a frozen copy (a queued render uses code as it is at start). | 10 | Fact | |
| R438 | Pin `remotion` and every `@remotion/*` to one exact version; pin three.js. | 11 | Fact | |
| R439 | Fonts: static instances via one loader that holds the frame until ready. | 12 | Fact | |
| R440 | Bake heavy meshes (30 s load timeout); exact integer output sizes. | 13 | Fact | |
| R441 | One GPU job at a time through a queue (two Chrome renders lost WebGL). | 16-17 | Fact | |
| R442 | Stills jump ahead of renders; tickets ~15 min renders, ~5 min stills. | 17-18 | Process | |
| R443 | Log full output to a file; never pipe through `tail -1`. | 18 | Process | |
| R444 | To cancel, kill the whole process tree, then confirm the queue is free. | 18-19 | Process | |
| R445 | Never kill a process you didn't start. | 19 | Safety | Dup of R536. |
| R446 | Draft 720p, ~8 shutter samples; final full res, full samples. | 22 | Direction | |
| R447 | Trust a draft shortcut only after a draft still matches a full still. | 23-24 | Fact | |
| R448 | Before a 4K master, compare downscaled 4K stills; pixel quantities scale by height ÷ 1080. | 25-26 | Fact | |
| R449 | 180° shutter; log real sample times; ~4 px movement per sample keeps lettering sharp. | 29-30 | Direction | |
| R450 | Prove the blur mixer with a frame-number test. | 31 | Process | |
| R451 | R3F in Remotion: render once after the last canvas draw; never skip it (white canvases). | 32-33 | Fact | |
| R452 | Pre-roll every chunk ~12 frames; compare frames across each boundary. | 36-37 | Fact | |
| R453 | 4K chunks as ProRes 422 HQ. | 38 | Direction | |
| R454 | Never join by `concat -c copy` (21 ms late, irregular packets); decode in order, encode once. | 39-42 | Fact | Dup of R283, R28. |
| R455 | Splice: additions out of frame at the splice; prove the seam on neighbouring frames. | 43-44 | Process | |
| R456 | BT.709 everywhere; ffmpeg 8 keeps frame tags, so stamp with `setparams`. | 47-48 | Fact | |
| R457 | PNG → mp4 needs `out_color_matrix=bt709` (else green shift); tag raw piped input. | 49-50 | Fact | |
| R458 | Render muted, mux the master WAV from 0 (Remotion AAC 42.7 ms late). | 53-54 | Fact | Dup of R27. |
| R459 | No `-shortest` under a copied picture; pad/trim audio, count frames. | 55 | Fact | |
| R460 | Run `film_gate.py` after every render. | 58 | Process | |
| R461 | Blank scan: black/white/frozen/magenta/missing frames; frame count vs expected. | 59-60 | Process | |
| R462 | Pop scan: look at every frame-diff spike; anything vanishing between frames is a pop. | 61-62 | Process | |
| R463 | Hard-cut scan by colour-histogram jump per frame pair. | 63-64 | Process | |
| R464 | Local flicker test (1–3-frame runs, formula); flow-align with a moving camera. | 65-69 | Process | |
| R465 | Jitter: 1 s window, no step > 12 px, path ≥ 14 px, net < 35 % = wander. | 70-71 | Direction | |
| R466 | Clipping audit before render; camera is a solid; 100 % stills of every cluster. | 72-73 | Process | |
| R467 | Step consecutive frames round every flag, contact, entrance, transition; watch at speed. | 74 | Process | |
| R468 | `-ss` isn't frame-exact; use `select=eq(n,K)` and assert the count. | 75 | Fact | Tension with R56 (uses `-ss`). |
| R469 | Checks must be able to fail: plant a known-bad case. | 78 | Process | |
| R470 | A perfect score is a prompt to check the instrument; count compared vs expected. | 78-79 | Process | |
| R471 | A FAIL can be the instrument too; check inputs; run new detectors on a clean render first. | 80 | Process | CONFLICT with R234. |

## craft/story.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R472 | Every shot needs a subject, an intention and a reason to end. | 7 | Direction | |
| R473 | Map the structure (sections + energy, or acts) first. | 10 | Process | |
| R474 | Emotional spine in one sentence. | 11 | Process | |
| R475 | Mood vs picture: direction can carry an ache in a sunlit picture. | 12-13 | Direction | |
| R476 | Section jobs: verse discovery, pre-chorus anticipation, chorus release, bridge turn, outro echo. | 14-15 | Direction | |
| R477 | Beat sheet; a scene where nothing changes is cut or gets a turn. | 16 | Process | |
| R478 | Shot-size meanings (EWS place, WS people in world, CU emotion, insert detail). | 19-20 | Direction | |
| R479 | Lens meanings: 14–24 space, 35 storytelling, 50 neutral, 85–135 intimacy. | 21-22 | Direction | Tension with R372. |
| R480 | Height meanings (eye neutral, low heroic, high vulnerable, child wonder). | 23 | Direction | |
| R481 | Moves have motives: push-in realisation (land on the lyric), locked-off awe, ~1 % handheld memory… | 24-26 | Direction | CONFLICT with R378 and R377 / R291 (locked-off). |
| R482 | Composition: thirds, layers, frame-through, leading lines; faces out of the lyric area and off edges. | 27-28 | Direction | |
| R483 | Coverage: establishing → two-shot → singles → inserts; cut on action or beat. | 31 | Direction | |
| R484 | 180° rule. | 32 | Direction | |
| R485 | Screen direction: journey left→right, return right→left, consistent all film. | 33 | Direction | |
| R486 | Block people before placing the camera; motivate every movement. | 34 | Direction | |
| R487 | Physical believability: planted feet, real seats, stride-matched walks, hands really hold props. | 35-36 | Direction | |
| R488 | Plain cut is the default and strongest transition. | 39 | Direction | Scoped tension with R382. |
| R489 | Match cut, wipe, dissolve (sparingly), push-through, whip — each with a reason; never the same fancy one twice in a row. | 39-41 | Direction | |
| R490 | Words inside the world, on the vocal onset, phone-readable, never over faces; subtitle lane only if no surface. | 45-47 | Direction | Dup of R110, R36. Mode tension with R76 default (lyric video: lanes). |
| R491 | Repeated hooks get new staging each time. | 47 | Direction | Dup of R44. |
| R492 | Verses hold 4–8 s, choruses cut on bars, final montage every bar, bridge holds long. | 50 | Direction | Tension with R19. |
| R493 | A quiet hold before each emotional peak. | 50-51 | Direction | |
| R494 | End shots late on emotion, early on action; a walk never stops dead before a cut. | 51 | Direction | |
| R495 | Deliverables: beat sheet, shot list (columns), continuity notes, engine mapping (f/2.8, f/8…). | 54-60 | Process | |
| R496 | Self-review: title each shot in 5 words; game-like tells; ending echo; one signature image; arc with sound off. | 63-65 | Process | |

## craft/team.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R497 | The director session makes nothing in workers' files; owns GPU queue and schedule. | 8-9 | Process | |
| R498 | The creator's notes always outrank the director's. | 9 | Process | |
| R499 | Director's log structure (FOR THE CREATOR, STATE, verbatim words, bar, GPU plan, advice). | 12-14 | Process | |
| R500 | One brief per worker: scope, creator's verbatim words, routing; no paraphrase or own step list. | 15-16 | Process | |
| R501 | Recurring tick every 30 min by day, 15 min overnight. | 17 | Process | |
| R502 | Checked saves for shared code; revert all on failure; never land multi-file changes file by file. | 18-19 | Process | |
| R503 | A relay is the creator's exact words + routing; no summary, no numbers they didn't give. | 22 | Process | |
| R504 | Unclear or conflicting notes: ask in one line instead of choosing. | 23 | Process | |
| R505 | Review against the creator's sentences, never a derived spec. | 24-25 | Process | |
| R506 | Phrase reading: "my only issue is X" + next sentence = fix; "at least X" = floor; "have one be X" adds/swaps. | 26-27 | Process | |
| R507 | Note checklist; approved only when every row is met on a named frame; changes uncheck all. | 30-31 | Process | Dup of R357. |
| R508 | At most three workers besides the director, as a queue. | 34 | Direction | |
| R509 | Fresh worker per new task; finished workers write state and stand down. | 34-35 | Process | |
| R510 | One consolidated message per worker per tick; director's own findings only if verified with frames. | 35-37 | Process | |
| R511 | No message when nothing is new. | 37 | Process | |
| R512 | Ask for times not effort; 30+ min slip → new true time and scope order, never a quality cut. | 37-38 | Process | |
| R513 | Only the creator's notes are to-dos; flaws on approved work go to the director as a list. | 38 | Process | |
| R514 | Sessions talk via session messaging, or an inbox file + STATE file. | 39 | Process | |
| R515 | Run `date` before writing any time. | 44, 97 | Process | |
| R516 | Read the real usage meter, never estimate; unattended runs pause at 95 %. | 45 | Process | |
| R517 | Sanity: disk, temp, keep-awake, stale browsers (report, never kill). | 52 | Process | |
| R518 | Overnight: never wait on the creator; noted defaults; improve what's agreed. | 56-57 | Process | |
| R519 | Review and splice each render as it lands; handoff before they wake; keep the machine awake. | 57 | Process | |
| R520 | Before a master, sweep the whole film on today's code. | 58 | Process | |
| R521 | Every draft goes on the review page, never as a bare file path. | 60 | Process | Dup of R29. |
| R522 | One entry per pass, newest first, known issues on top; never revise an old entry. | 61-62 | Process | |
| R523 | Render → blank scan → post with known issues → fix; review never holds a draft back. | 63 | Process | |
| R524 | Marks "waiting review" → "reviewed"; reviewed ≠ approved. | 64 | Process | |
| R525 | Clips carry their own audio; offsets in seconds, not frames. | 65 | Process | |
| R526 | New file name for every version; never overwrite a delivered file (players cache by URL). | 66 | Fact | |
| R527 | Looping previews as 10-bit AVIF, not lossy WebP (banded dark gradients). | 67-68 | Fact | |
| R528 | Read the stored entry back after writing. | 69 | Process | |
| R529 | Third-party reference footage stays off the review page. | 69 | Safety | |
| R530 | Recommended review page: WIP (setup and serve steps). | 70-74 | Process | |
| R531 | Update = read, then write with the revision read; never bypass a revision conflict. | 76-77 | Process | |
| R532 | `wip validate` after every write. | 83 | Process | |
| R533 | Frame refs and drawings from the page count as timestamped notes. | 84-85 | Process | Dup of R55. |
| R534 | Static export only with an explicit allowlist and when the creator asks; drafts stay local. | 86 | Safety | |
| R535 | No WIP: a JSON-per-entry folder + static page, or a private Artifact page. | 87 | Process | |
| R536 | Never kill a process you didn't start. | 97 | Safety | Dup of R445. |
| R537 | Never delete without the creator's OK on the exact list. | 97 | Safety | CONFLICT with R54 (auto clean-up) and R635 (delete what you regenerate without asking). |

## craft/timing.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R538 | Suno songs: use Suno's own stems; it spends the user's credits, so ask first. | 8-9 | Safety | Dup of R82. |
| R539 | No tool stems: use a splitter and label the map "separated stems". | 10-11 | Process | |
| R540 | Summed stems vs master cross-correlate at lag 0; check each instrument's stem. | 12 | Process | |
| R541 | Edit the mix by layering a stem phrase on the master; summed stems sound different. | 13 | Fact | |
| R542 | Onset = first audible energy of the word's first sound; never the breath or previous tail. | 16-17 | Direction | |
| R543 | Nothing keyed to a word is readable before its onset. | 18 | Direction | Dup of R18. |
| R544 | Lyric times, aligners, Whisper (0.5–0.8 s early), stem MIDI (~6.5 frames ahead) give which, not when. | 20-23 | Fact | Dup of R83. |
| R545 | Traps: held tails, melisma, merged MIDI, s/f hiss 5–8 frames early, doubled backing, repeats differ. | 25-27 | Fact | |
| R546 | Candidate → spectrogram snap → measured twice within ~25 ms → mean. | 30-32 | Process | |
| R547 | One words file: onset, end, confidence tag, reason; every scene keys to it. | 33 | Process | |
| R548 | A perceptual call → render a short A/B clip with waveform; don't argue in words. | 34 | Process | |
| R549 | Re-timing a word moves it in the shot: re-check the camera at the new time. | 35 | Process | Tension with R378. |
| R550 | Tempo can drift; keep a list of beat times, not one period. | 38 | Fact | |
| R551 | Fit the grid to drum-stem audio onsets; mean distance < ~0.1 beat. | 39-40 | Direction | Dup of R85, R559. |
| R552 | Hit bands (kick 30–110 Hz, snare 1.2–5 kHz…); thresholds from this song; check as 16-step. | 41-43 | Fact | |
| R553 | Map events: drum stops, fills, risers, drops, silences, prominent notes. | 44 | Process | |
| R554 | Moves start and land on beats; not every hit needs a move. | 47 | Direction | |
| R555 | Kick shake: small push + roll nudge dying in ~0.2 s over a slow sway; softer when framing must read. | 48-49 | Direction | |
| R556 | Accent: anticipation before, impact on the beat, follow-through after. | 58 | Direction | Dup of R418. |
| R557 | Pace follows the song: slow song, slow eased moves. | 59 | Direction | |
| R558 | Word-timing clip with onsets on the waveform; entrance starts on that frame. | 62-63 | Process | |
| R559 | Verify grid vs drum stem < ~0.1 beat. | 64 | Process | Dup of R551. |
| R560 | `ffprobe`: start_time 0 on both streams; frame 0 = song time 0. | 65 | Fact | |

## references/feel.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R561 | Write a feel card (BRIEF section + feel.json) before any build. | 3 | Process | |
| R562 | Arousal = normalised section energy, nudged ±0.1 for > 120 / < 75 BPM. | 6 | Direction | |
| R563 | Valence from the lyrics' stance, not single words; confirm with Q1. | 7 | Direction | |
| R564 | The emotion arc must read with the sound off, from 12 muted frames. | 8 | Direction | |
| R565 | Genre bands are uncalibrated estimates; only gate thresholds were calibrated (five films). | 11 | Fact | |
| R566 | A measured loved reference beats the table; two beat one; measurement wins. | 13 | Process | |
| R567 | Genre band table: cuts/min, stillness, motion, camera, palette, easing, type per genre. | 15-24 | Direction | Lo-fi stillness 0.50–0.80 / "static" camera conflicts with R734 and R291; Pop "bright sets" conflicts with R403. |
| R568 | Valence < −0.3: lightness −10 %, saturation −15 %, colder shadows, easing ×1.3, more space. | 27-31 | Direction | |
| R569 | Valence > +0.3: lightness +10 %, warmer highlights, overshoot, tighter framing. | 32-36 | Direction | Tension with R403. |
| R570 | Cuts/min scale with arousal; stillness inversely. | 37 | Direction | |
| R571 | Break one genre convention on purpose, in one place, for a reason; write it in the card. | 40-45 | Direction | Its example "EDM drop silent and still for one bar" conflicts with R96 and, unless declared, R732. |
| R572 | Section `still` is a stillness-ratio band. | 60 | Process | |
| R573 | Top-level `still` spans are exempt from dead_gap. | 61 | Fact | |
| R574 | SOFT measures: cuts/min and stillness per section vs bands; feel-sync. | 64 | Process | |
| R575 | Veto: mood contradicts the section (strobe in a grief verse). | 66 | Direction | Dup of R593. |

## references/style-protocol.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R576 | Self-scores run ~10 (up to 17) points above independent review. | 3 | Fact | Measured by the huashu-art-motion makers. |
| R577 | Use this protocol for every look; every song new; each brand look built once. | 5 | Process | |
| R578 | Anchor in ≥ 3 different real works, never memory; film stills for study only. | 8 | Process | |
| R579 | Save refs in `refs/`, one contact sheet, k-means palette hex. | 9 | Process | |
| R580 | Write 5 signature traits (must-have / bonus / taboo), palette, physical medium. | 11-13 | Process | |
| R581 | Write "this style composes by …"; never reuse another piece's layout. | 23 | Direction | |
| R582 | Shape layer, then a medium pass; noise on flat vectors is not a style. | 26-34 | Direction | |
| R583 | A missing medium pass becomes a reusable function, never hard-coded in one scene. | 36 | Process | |
| R584 | One still before any animation, side by side with refs; recognisability judged only from it. | 39-42 | Process | |
| R585 | One main action plus 2 looping motifs. | 45 | Direction | CONFLICT with R20 / R715 (no loops after landing). |
| R586 | Move by the style's own motion logic (e.g. cut paper at 12 fps with boil). | 46 | Direction | |
| R587 | No generic fade-in on every element. | 47 | Direction | |
| R588 | 100-point rubric with fixed item weights. | 49-59 | Direction | |
| R589 | Threshold 80, at most 2 repair rounds. | 49 | Direction | CONFLICT with R26 ("fix until 80+", no round cap). |
| R590 | Feel-sync is never scored (read ~0 on every finished film). | 54 | Fact | |
| R591 | Thumbnail-size test at 160 px wide still reads. | 56 | Direction | Differs from R386 (360 px), R217 (168×94). |
| R592 | Nothing on screen under 0.3 s. | 57 | Direction | CONFLICT with R735 (1-frame impact cuts used on purpose; SOFT only). |
| R593 | Vetoes: signature < 15, childish/sticker hero, mood contradicts section, any gate HARD failure. | 61-65 | Direction | |
| R594 | Independent review is mandatory: fresh subagent that hasn't seen the code or conversation. | 68 | Process | Dup of R31. |
| R595 | Give it refs sheet, side-by-side, 12 muted frames, gate report, STYLE.md, feel card, rubric. | 69 | Process | |
| R596 | It returns item scores, signature checklist, vetoes, 3 biggest fixes. | 70 | Process | |
| R597 | The lower score counts; report both. | 71 | Process | Dup of R31. |
| R598 | Taste is flagged for the human; the AI never writes "taste approved". | 72 | Safety | |
| R599 | Under 80 after 2 rounds: say so plainly, name what's stuck, don't call it done. | 73 | Safety | CONFLICT with R26. |
| R600 | Approved stills go to `anchors/`; later stills checked by ΔE, contrast, grain; drift fixed before integration. | 76-79 | Process | Dup of R111. |

## references/lessons.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R601 | Read this file when you're stuck. | 9 | Process | CONFLICT with R17 (read before building). |
| R602 | Every new user complaint adds one line here (lessons.md) or one gate check. | 11 | Process | CONFLICT with R61 (never write lessons in the plugin). |
| R603 | "1:26 looks odd" (TN): reproduce the complaint as frames before touching code. | 14-17 | Case note | |
| R604 | Build review instruments once (contact sheet, strip, crop) and use them constantly. | 18-23 | Process | |
| R605 | Previews and the encode can differ; verify the shipped MP4. | 24 | Fact | |
| R606 | Run one cheap mechanical check across every near-identical file (a missing `</div>`). | 25 | Process | |
| R607 | Milky film (TN): bisect post passes; read the guilty piece closely. | 28-32 | Case note | |
| R608 | ENOSPC (TN): TEMP to the big drive, clean up each render; read errors literally. | 33 | Fact | Dup of R7. |
| R609 | Squeezed faces (TN): project every transform to a similarity. | 34 | Fact | Dup of R34. |
| R610 | Ghost arms (TN): rotate the arm about its joint, swap drawings at the midpoint. | 35 | Case note | Dup of R37. |
| R611 | Tiny figures (TN, BG): a px/cm scale engine; a recurring bug lives in the system. | 36 | Case note | Dup of R38. |
| R612 | Floating feet (BG): check what each of two matching numbers is measured against. | 37 | Case note | |
| R613 | Scale (BG/TN): door 2.6 px/cm, 18 cm riser, pxcm(y) formula, ear as rigid feature, seat point. | 40-46 | Case note | |
| R614 | Audio is data: energy, kicks and hits drive every pulse and cut. | 47 | Process | |
| R615 | M/A2/A1/E on every lyric word; "machine-aligned, not ear-checked" on every deliverable. | 48 | Safety | Dup of R48. |
| R616 | Two scripts (JKD): sandwich method gave 535 of 596 words within 0.3 s. | 49 | Case note | Dup of R80. |
| R617 | Constraints spark ideas (TN no new assets, unseen tea-giver, BG one plate two moods). | 52-55 | Case note | |
| R618 | LGTM study (TN): keep the mechanism, re-derive energy; 49 punches → ~15 pushes. | 58-60 | Case note | Dup of R45. |
| R619 | Stillness (BG): the bridge had zero beat effects, so the last chorus landed. | 61 | Case note | Tension with R19. |
| R620 | The crown (JKD): stage what the song believes. | 62 | Case note | |
| R621 | TN v1–v4 correctness, v5–v6 "wow": ask what the bar is after each round. | 65 | Case note | Dup of R60. |
| R622 | The hook decides everything (BG fish face; TN point of light, title on the 2.5 s hit). | 66-68 | Case note | |
| R623 | "Same same" (JKD): keep the motif, restage chorus 2. | 69 | Case note | Dup of R44. |
| R624 | Effect must mean something (JKD clay→skin became wireframe spreading from fingertips). | 70 | Case note | Dup of R42. |
| R625 | Credits (JKD): a hand inking credits on the lyric sheet; endings belong to the song. | 71 | Case note | Dup of R94. |
| R626 | Honest credit (JKD): who-did-what, creator's name in title, links, AI disclosure ticked. | 72 | Safety | Stated through one film. |
| R627 | Parallel work (TN 5+4 agents, JKD 7): ownership, stubs, copies, notes, coordinator owns seams. | 75-83 | Case note | Dup of R296, R300. |
| R628 | The hand (JKD): read what you rewarded; show reviewers the real thing from 3 angles. | 86-89 | Case note | |
| R629 | Gate calibration: diff vs 0.5 s earlier, merge spikes in 0.25 s; a gate that fails good work gets fixed, not obeyed. | 92-97 | Process | CONFLICT with R234. |
| R630 | The gate still caught a 7 s frozen tableau (BG) and a 10 s mist freeze; films prove the pipeline, not the taste ceiling. | 98-102 | Case note | |
| R631 | Windows: heredocs/sed eat quotes; `=`-splitting CLIs mangle args. | 105 | Fact | Dup of R301, R302. |
| R632 | three.js 0.186: PCFSoftShadowMap gone; blur average needs `autoClear = false`. | 106-108 | Fact | Dup of R289, R286. |
| R633 | Remotion: t-dependent infinite loop hangs; guard every search loop. | 109 | Fact | Dup of R271. |
| R634 | Blender 5.2 glTF has no loose-edge export; send wireframes as JSON segments. | 110 | Fact | |
| R635 | Cleanup is policy (TN 8.6 → 1.95 GB); delete only what you regenerate, else get the owner's OK. | 111 | Safety | Partly conflicts with R537 (OK on every deletion). |

## references/sources.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R636 | Licences change: re-check at download time; log every asset in CREDITS.md. | 4 | Safety | Dup of R51. |
| R637 | Default to CC0, no-account sources (Poly Haven, ambientCG, Kenney). | 6 | Safety | |
| R638 | Quaternius is not CC0 (commercial OK, no redistribution). | 9, 20 | Fact | |
| R639 | Coverr and Sonniss forbid AI training. | 10 | Fact | |
| R640 | Pixabay music carries Content ID claim risk. | 11 | Fact | |
| R641 | Freesound includes NC sounds; filter by licence. | 12, 53 | Safety | |
| R642 | Megascans and ShotDeck are no longer free. | 13 | Fact | |
| R643 | Sketchfab licence is per model; needs an account/API key. | 21 | Fact | |
| R644 | CMU Mocap: use http (TLS certificate error). | 34 | Fact | |
| R645 | DeepMotion (free tier non-commercial) and Move One are dropped. | 38-39 | Fact | |
| R646 | YouTube Audio Library licence covers YouTube only. | 55 | Fact | |
| R647 | Fontshare: use their CDN; don't redistribute the font files. | 60 | Safety | |
| R648 | Reference/taste sites are reference only; never reuse frames. | 68 | Safety | |
| R649 | Blender Lab MCP port 9876 clashes with mcp-for-blender; run only one. | 87, 98 | Fact | Dup of R305. |
| R650 | Ranked MCP shortlist (mcp-for-blender first … Unreal last). | 93-101 | Direction | |
| R651 | Several terms are UNVERIFIED (Rokoko, FreeMoCap AGPL, Eyecannndy, Poly Pizza, Mixamo, LottieFiles). | 35-36, 103-108 | Fact | |

## talking/checks.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R652 | Read before every plan and board; check frames against it before calling a render done. | 3 | Process | |
| R653 | Every user correction becomes one line here; newest at the bottom. | 3-4 | Process | CONFLICT with R61 / R167 (corrections go to `~/.video-director/checks.md`, never inside the plugin). |
| R654 | No cards or text over the face; on boards keep the PiP bubble zone empty. | 8 | Direction | Dup of R36. |
| R655 | Readable words ≥ 70 px for captions, ≥ 40 px on boards; cut words, never shrink. | 9 | Direction | CONFLICT with R670 (~52 px captions) in the same file. Dup of R148. |
| R656 | Keep footage and screenshots at real aspect; never crop to fill a box. | 10 | Direction | |
| R657 | Literal over abstract. | 13 | Direction | Dup of R144. |
| R658 | No paragraph on a board; one claim per board, as its title. | 14 | Direction | |
| R659 | Never invent numbers, logos, quotes or footage; a missing asset is a dashed "pending" card. | 15 | Safety | Dup of R718. |
| R660 | Everything appears on the word that names it. | 18 | Direction | Dup of R18. |
| R661 | Don't open a board empty. | 19 | Direction | Dup of R713. |
| R662 | Don't let a board sit still more than ~3 s while the speaker talks. | 20 | Direction | Dup of R19 (here scoped to boards). |
| R663 | Don't zoom or pulse elements after they land; board emphasis is size. | 21 | Direction | Dup of R20. |
| R664 | One accent per clip; numbers and key words in it. | 24 | Direction | CONFLICT with R209 (≤ 3–4 meaning colours). |
| R665 | No dark text on a dark panel. | 25 | Direction | |
| R666 | Group/pitch rules were learned on the ViseMe and Drishyam pitch films (Nov 2026). | 28 | Case note | Header for the rows below. |
| R667 | Fixed zones (meta bar, stage, label, caption lane) before any shot; prove with a 0.25 s sampling script. | 30-32 | Process | |
| R668 | Shot budget: speaker + one name plate + caption + ≤ 1 chip; swap content, never add a box. | 33 | Direction | |
| R669 | Name plate under the active speaker; dim and slightly blur resting neighbours. | 34-35 | Direction | |
| R670 | Fill frame: head ~40 % height, crown ~17 %, table ~22 %, captions ~52 px at 1080p; seat centre-out. | 36-37 | Case note | CONFLICT with R655, R148, R160 (≥ 70 px); tension with R384. |
| R671 | Equal head sizes in a group, eyes on one line; highlight the speaker, don't enlarge. | 38-39 | Direction | |
| R672 | No neighbour cut by the frame edge in a medium; fit in 90 % or leave out. | 40-41 | Direction | |
| R673 | `hyperframes check` with samples + caption zone to 0 errors; layout ignores parent opacity, so hide with visibility. | 42-43 | Fact | Not a conflict with R682 (different elements), but easy to misread. |
| R674 | Opaque pill behind small labels over footage; re-run contrast after ink changes (60 % failed, 70 % passed). | 44 | Direction | |
| R675 | Contributors without footage as clean typography, never blank heads or empty seats. | 45 | Direction | |
| R676 | Check cutouts on dark and cream; matte at native res, open mask ~9 px, keep biggest piece, feather sides. | 47-48 | Case note | Cream backgrounds imply a light look; see R403. |
| R677 | People: iris on the eyes, still first frame, wake into video in 5 frames with 2 % lift, rest in 7. | 49-51 | Case note | CONFLICT with R426 (6–12 frames). |
| R678 | Light cutouts into the room (shared key, contact shadow, light-wrap); room light on the card, not the clip. | 52-53 | Direction | |
| R679 | Fades are fine for real-person cutouts in a pitch film; the body-crossfade ban is for sprite/music-video work. | 53-54 | Direction | CONFLICT with R37 (stated universally). |
| R680 | Hide (don't fade in) a person cut off at a move's start and still off-frame at its end. | 55 | Direction | Tension with R426. |
| R681 | Grow a grid tile into a medium by laying out at medium and tweening scale + clip-path inset. | 55-56 | Direction | |
| R682 | Don't hide a live `<video class="clip">` with visibility on a wrapper; use opacity. | 57 | Fact | |
| R683 | Rebuild room plates with the exact ingest reader; prove alignment against a +1-frame-slip control. | 58-59 | Process | |
| R684 | Word end ≠ next start; measure from a 10 ms energy envelope; out-point = end + 0.15–0.25 s. | 61-63 | Fact | |
| R685 | Don't let aligner times decide a caption at a cut; use later of team/re-listen; measure deleted silence from audio. | 64-65 | Fact | |
| R686 | Check a "pause" isn't a drawn-out word before trimming; prove captions complete with Whisper on the final mix. | 66-67 | Process | |
| R687 | 25 ms fade on a cut inside speech; ~150 ms into room tone; phone audio ends ~50 ms after the last word. | 68-69 | Fact | |
| R688 | Captions at full ink from their first frame on phones (grey-then-lit reads faint). | 70 | Direction | CONFLICT with R150 (unspoken words at 45 %). |
| R689 | Reading floor ~0.5 s + 0.2 s a word; one sentence per shot. | 70-71 | Direction | |
| R690 | End captions/plates ≥ 0.02 s before the next cut; at hand-offs end the old before the new starts. | 71-72 | Direction | |
| R691 | A panel's first content starts with its shot; outgoing fades over the last 0.2 s; never an empty panel. | 73 | Direction | Tension with R18 (content keyed to shot start, not to a word). |
| R692 | Pitch film: check every competitor claim against their own site text. | 74 | Safety | |
| R693 | Never play a person's AI voice or present an AI-animated clip as a recording; keep silent, tag "AI-animated". | 75 | Safety | |
| R694 | One voice chain: denoise, partial EQ-match (≤ 3 dB, never cut > 2 dB above 2 kHz), same LUFS, shared reverb. | 77-79 | Direction | |
| R695 | Keep music out of the video render; mix the bed separately; true peak measured on the encoded AAC. | 80-81 | Process | |
| R696 | GSAP `fromTo` shows its start state from frame 0; hide in CSS and `tl.set` on cue. | 83 | Fact | |
| R697 | Don't reuse generic class names across layers. | 84 | Fact | |
| R698 | Strikes use line-through; highlight boxes need z-index on the text. | 84-85 | Fact | |
| R699 | No parallax layer dragging a wall sign half-cut into later shots. | 86 | Case note | |
| R700 | Patch frames by overlaying snapshots in ffmpeg with source colour tags (cv2 shifts ~2/255); splice frame-exactly. | 87-89 | Fact | |
| R701 | Don't glob `assets/music/*.*` (picks up LICENSE.txt). | 90 | Fact | |
| R702 | Windows ffmpeg drawtext can segfault; label contact sheets with cv2. | 90-91 | Fact | |

## talking/references/boards.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R703 | Pick the board from the catalog by "say it when" tags; borrow motion and layout. | 10-12 | Process | |
| R704 | Copy `hf-board/`; root 1080×1920; data-duration = board span. | 13-14 | Process | |
| R705 | `sync.js` places each element at word start + 0.05 s. | 16-17 | Fact | |
| R706 | Run `hyperframes check --json` after `compile --no-render`; fix errors, weigh warnings. | 18-19 | Process | |
| R707 | Look at frames before saying a board works. | 21 | Process | |
| R708 | PiP bubble x 632–1021, y 150–539: nothing readable there. | 24 | Direction | |
| R709 | Caption band captions.y (0.84 h) ± 0.08 h: nothing readable unless captions are off. | 25 | Direction | |
| R710 | 60 px padding on every side; readable words ≥ 40 px. | 26 | Direction | Dup of R655 (boards part). |
| R711 | Land on the word: never before it, never more than 2 s after. | 29 | Direction | Dup of R18. |
| R712 | A part never lands before its container; an arrow never before both ends. | 30 | Direction | |
| R713 | Structure first: headline and boxes/axes on screen from frame 0; no board opens empty. | 31 | Direction | Tension with R18 / R660 ("everything appears on the word that names it"). |
| R714 | Nothing still > ~3 s while the speaker talks; fill with the speaker's own words, never invented copy. | 32-33 | Direction | Dup of R19. |
| R715 | Nothing moves after it lands: no pulses, loops, zooms or camera pushes; emphasis = size. | 34 | Direction | CONFLICT with R732 / R734 (a landed static board fails both gates), R291, R585. |
| R716 | Money/percent pop only on numbers said as money/percent; a count never gets a price sticker. | 35 | Safety | |
| R717 | Copy that contradicts what's said is flagged to the user, never silently changed. | 36 | Safety | |
| R718 | Never invent numbers, logos, quotes or footage; missing asset = dashed "pending" card. | 36-37 | Safety | Dup of R659. |
| R719 | QA: element absent 0.1 s before its word and present 0.5 s after. | 38 | Direction | |

## talking/references/edit-schema.md

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R720 | Read cut.txt first; every word ref must exist in the transcript (else error). | 5, 41 | Fact | |
| R721 | `tail` holds the last frame 1.2 s after speech. | 23 | Direction | |
| R722 | `punch` 1.12 zoom on alternate long shots; `zoom: auto` punches on gesture/emphasis. | 23-24 | Direction | CONFLICT with R370. Dup of R142. |
| R723 | The clip's own audio is always kept; `sfx` only mutes synthesized effects. | 25 | Fact | |
| R724 | Captions: 3 words a chunk, y 0.84 (below chin, max 0.9), size 78 never < 70, one accent, numbers in accent. | 27 | Direction | Dup of R148. |
| R725 | A card's `until` defaults to `at` + 2 s. | 29 | Direction | |
| R726 | Boards < 0.6 s apart keep the bubble; boards take no lane; keep other cards off board spans. | 34 | Direction | |
| R727 | Default lanes/heights; cards clear the face band by ≥ 0.02, bottom ≤ 0.78, top ≥ 0.04, 0.02 gaps. | 38 | Direction | |

## scripts/film_gate.py (LIMIT constants and HARD checks)

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R728 | Frame diff below 0.6/255 counts as "no visible change". | 24 | Direction | |
| R729 | In-shot median diff above 1.0 counts as a moving shot. | 25 | Direction | |
| R730 | A cut = diff > 8.0 and > 4× the rolling median of neighbours. | 26-27 | Direction | |
| R731 | A mean-luminance jump > 25/255 is a flash edge. | 28 | Direction | |
| R732 | HARD dead_gap: no visible change (vs 0.5 s earlier) for > 1.0 s fails; feel `still` spans exempt. | 7, 29, 161-163 | Direction | CONFLICT with R19 (~3 s), R201, R377, R715, R96/R571; dup R231. |
| R733 | HARD flicker: two same-sign flashes < 0.17 s apart fails. | 8, 29, 165-175 | Direction | Dup of R232. |
| R734 | HARD slideshow: duration-weighted share of moving shots < 0.6 fails (still spans excluded). | 9, 29, 177-190 | Direction | CONFLICT with R201 (~70 % still), R715, R567 (lo-fi). Dup of R233. |
| R735 | SOFT short_shots: shots < 0.3 s reported only, never fail (1-frame impact cuts are used on purpose). | 11, 29, 192-194 | Direction | CONFLICT with R592. |
| R736 | HARD loop (`--loop` only): first vs last frame diff > 2/255 fails. | 10, 29, 195-196 | Direction | |

## C:\Users\Dr. Rajesh Pareek\.video-director\checks.md (owner's personal rules)

| # | Rule | Line | Tier | Note |
|---|---|---|---|---|
| R737 | These rules belong to the owner and override the plugin's. | 3 | Process | Dup of R17. |
| R738 | Make it feel like an animated film (Pixar camera, light, acting), never like a game. | 7 | Direction | Learned on Pocket Hills; written as universal. |
| R739 | Every song gets a fresh look; past films prove the pipeline, not the style ceiling. | 8 | Direction | Dup of R9, R630. |
| R740 | Never use real hill-station names (Shimla, Manali, Atal tunnel, Solan); keep hill work nameless. | 11 | Direction | Owner's content rule. |

## styles/*/STYLE.md

The five files (cinematic-plate, clay-world, mist-silhouette, painterly-cutout, pop-era-collage) are example looks. Their rules apply only when that look is chosen, so they are not listed here.
