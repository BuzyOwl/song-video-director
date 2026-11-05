# Cinematic Plate
id: cinematic-plate
Proven in: Toota Naksha (Remotion + Canvas2D/WebGL 2.5D plates, 3:53)
Best for: ballads, longing/heartbreak, narrative songs with one protagonist who needs a face; 55–90 BPM
Mood: A night-train film still that breathes: warm amber memory against a cold blue present.
Engine: Remotion+Canvas/WebGL · cost high · render time not logged (24 fps, 5,592 frames, full post stack every frame)
Gallery sample: gallery/samples/cinematic-plate.mp4
## Feel
- Genres: Hindi/Urdu ballads, acoustic, singer-songwriter, cinematic pop. Proven at 63.5 BPM (beat .945 s, bar 3.78 s).
- valence −0.6..0.3, arousal 0.1..0.55
- Cuts/min 4.9 hard cuts measured; ~9 scene changes/min authored (35 scenes / 233 s, many as dissolves or panel inserts)
- Stillness ratio 0.4..0.6 (measured 0.52): never truly locked (sub-px camera life) but long holds
## Palette (hex)
Sourced from `src/engine/core.js` PAL, `type.js`, `post.js`:
- night #0B0F18 (base under camera moves), ink #10151F
- railway blue #293D4B, teal #526B6B (present, cold)
- lavender #8D859B (bridge, "you"), rose #C98B8B
- ivory #D1C7B1, paper #E8DCC2 (map world)
- amber #C3945D (lamp light, memory grade)
- **ACCENT amberHot #F2B66D** (one key word per line, Devanagari accents, kintsugi seam)
- type: verse #EFE6D2, chorus #F1E8D6, bridge #CFC5E0
- post tints: bloom multiply #FFD2A0; light leak #FFC48A → #E57B5A
## Type
- Verse: Cormorant Garamond 600, 74 px (x-height ~.40 em, so never smaller), track 1, scrim .4 — https://fonts.google.com/specimen/Cormorant+Garamond
- Chorus: Noto Sans Devanagari 700 (Latin glyphs), 64 px CAPS, track 6, scrim .34; stamped hooks 88–92 px — https://fonts.google.com/noto/specimen/Noto+Sans+Devanagari
- Bridge: Cormorant 500, 72 px, lavender #CFC5E0
- Accent (≤4 per film): Amita 700, 130 px, #F2B66D — https://fonts.google.com/specimen/Amita ; title also Noto Serif Devanagari
- Hook word: Noto Sans 800, 300 px outline (3 px stroke), behind the subject, fitted inside margins
- Lines romanised (Hindi in Roman letters); ≤2 lines on screen; margins 96 px H / 72 px V; scrim = soft local darkening, no box
- Lanes: home lower-centre x 960–1100, y 950–990 (default, 9:16-friendly); right lane x ≈1440 (short stacked lines in close-ups); left lane x 450–490 (subject faces right)
- Modes: rise (default), fog, stamp, echo, shard, fold, caption box, words, seam (amber kintsugi line), dust; karaoke sweep on the active word; text drawn between plate and figure
## Easing (numbers)
- ease smoothstep; easeOut/easeIn cubic; easeInOut cubic; soft = 1−(1−x)⁴ for type ("ink soaking in")
- Type in 0.35 s (fog 0.45 s); out 0.45 s, rising 0.22·size with blur to 5 px; letters track in from word centre, no bounce on verses
- Chorus lines turn in about Y (flip .75); one slow light glint only if the hold is >1.15 s
- Key word: amber bloom over 0.6 s, then decays 55 % over 1.4 s
- Downbeat breath (chorus kicks >0.7, ≥3.3 s apart): scale +1.4 % over 0.25 s, exhale exp(−d/0.5) (~1.4 s)
- Light leak 0.9 s per measured section hit; graphics on twos (12 fps), camera on ones (24 fps)
## Motion rules
1. Frame = renderFilm(t), pure; no state between frames.
2. Camera zoom ≤1.12 (plates are 1672×941, upscaled ×1.148); organic wiggle ±1.8 px, roll ±0.0007 rad, 0.8 % overscan.
3. Parallax only between truly separate layers (window stack: hills / town / trees behind glass; woman + carriage locked to camera).
4. Figures at true scale for their plate depth, anchored by the feet with contact shadows; scale from a head landmark, never the bbox.
5. Close-ups use a rig: blink, one-step view turn, nod, breath. No puppet stretching.
6. Section intensity drives post: chorus 1.0, verse/intro .6, breakdowns .25; breakdowns are held almost still.
7. Transitions are metaphors: push into map paper → creases glow → paper-grain threshold dissolve; halftone dot-dissolve; tears on section hits.
## Signature (must / bonus / taboo)
- must: painted 2.5D plates with one consistent heroine, window/reflection layers with real parallax
- must: finishing stack: halation/bloom (quarter-res, threshold ~.55, warm), anamorphic horizontal streaks, 2 px edge chromatic aberration ring, light leaks on hits, grain + vignette
- must: serif verses vs tracked-caps chorus, one amber key word per line
- bonus: paper-map metaphor world (ink lines, crease nets, Ben-Day halftone, misregistration as defocus); blueprint wireframe → real plate reveal
- taboo: halftone or graphic FX on present-tense faces (memory faces ≤20 % warm halftone only)
## Medium
Film plates + lens pass. Painted keyframe plates cover-fit to 1920×1080 → masked layers (window panes, crowd masks) → cut-out figures and face rig → fx (motes far/mid/near, steam, light bands, god rays) → lyric layer → post (camera life → bloom → streaks → edge CA → light leaks) → grain + vignette. Memory scenes: amber grade, 25 % halftone in shadows, print misregistration. Map world: paper grain, ink linework, halftone.
## Composition
- Subject on a third, facing into frame; type in the space she looks into, or the home lane.
- Close-ups: face 45–55 % of frame height on a defocused cabin with halftone bokeh.
- Wides: platform, carriage, viaduct diagonals leading into depth.
- One focal effect per frame; ≤2 lines of type.
## With media
- User photos as plates: grade to night/amber, add window glass + reflection pass, split into 2–4 masked depth layers for parallax.
- Portraits: present = clean + rim light; memory = warm grade + ≤20 % halftone + misregistration inside photo cards or a shard.
- Footage/AI clips: seen through a window, phone screen or reflection, never raw full-frame; run the same post stack so it matches.
## Ban list
- Teal-orange LUT, generic glow gradients, zoom >1.12, type on faces/hands/bright props, >2 lines, Devanagari karaoke (accents only), camera shake.
## Known limits
- Opening 0–6 s is weak: black, then a static empty platform; title only at ~6 s.
- Long holds: same bag-top plate ~16 s (17.7–33.7), one face 11.3 s (136–148), outro ~8 s near-static.
- A near-black dip at 106.6–107.1 reads as a dropout.
- Type on steep world planes shrinks (one line ~20 px, a map label ~35 px).
- 9:16 needs its own layout pass (subjects off-centre, many lines at x 1400–1560).
- Depends on many generated plates/sprites sharing one face: identity drift risk.
