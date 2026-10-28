# Painterly Cut-out
id: painterly-cutout
Proven in: Basement Goldfish (p5.js + p5.brush, 3:31)
Best for: comedic or warm indie/folk, story songs with one person + one small hero creature/prop, 100–140 BPM
Mood: A handmade puppet show in a damp, lamp-lit room: grounded, wry, tender.
Engine: p5.js · cost high · render time not logged; guide budget ≤1.5 s/frame → 5,074 frames ≈ ≤32 min on 4 workers (estimate); p5.brush watercolour fills take seconds/frame without a GPU
Gallery sample: gallery/samples/painterly-cutout.mp4
## Feel
- Genres: comedic indie, quirky folk-pop, story ballads, adult-witted kids' songs. Proven on ~132.5 BPM (machine beat grid).
- valence 0.1..0.8, arousal 0.3..0.7
- Cuts/min 4.5 hard cuts measured; 9.7 authored shots/min (34 shots / 211 s; most joins are brush-wipes)
- Stillness ratio 0.6..0.8 (measured 0.74 = frames with mean luma change <1.2/255 at 12 fps): sets hold, puppets act
## Palette (hex)
Sourced from `src/gf/fish.js` (GF) and `src/core.js` (PAL):
- ink #263F45 (outlines; type shadow rgba(25,45,56,.55)), black #192D38
- deep teal #334F56, teal #799D99 (cold alley/basement walls)
- paper #EFE2C8, cream #F6EACF (caption fill, BASEMENT title)
- **ACCENT orange #ED793F** (current-word underline, GOLDFISH, emphasis words); fish body #F66222 is the same family
- shadow #C95836, red #DC603D, peach #F4B780 (backing-vocal lane), mustard #D6AD59 (crown, collage blobs)
- skin #B9774E, glass #CFE0DA, water #9CC3C0
- lamp/home light #FFD68A, #F2A65A (window beams, warm-basement grade)
- chorus collage ground #F3EBDC with peach/mustard blobs (sampled)
## Type
- Lyrics: Patrick Hand https://fonts.google.com/specimen/Patrick+Hand — verse 60 px, hook 96 px (left, x 110, y 210+112·i), payoff 64, bridge 52 (cream, slow reveal), backing 44 italic peach (x 1390, y 810)
- Chorus block: Permanent Marker https://fonts.google.com/specimen/Permanent+Marker — 158 px, BASEMENT cream / GOLDFISH orange, ink stroke, stacked left
- Lanes, chosen per shot so text never sits on the creature or a face: bottom-centre y 940 (1 line) or 872 + 72·i (2 lines); top y 130; left x 110; right x 1810; top-right
- Future words wait as faint ghosts; current word pops 1 + 0.07·e^(−9a) and gets the orange underline (wipes in 4 frames)
- 4 emphasis words grow once to 1.75× (backOut, 0.3 s) + one tiny idea each (sparkle, clock wobble, crown, glow)
## Easing (numbers)
- ease = smoothstep x²(3−2x); easeOut = 1−(1−x)³; easeIn = x³; backOut overshoot s = 1.9
- Verse line in: from 0.12 s before onset to 0.06 s after; hook 0.2 s; bridge 0.2 s + 8 frames
- Brush-wipe: 0.6 s across the cut (0.3 s each side); fat strokes cover p 0→0.5, drag off 0.5→1, rotated −0.1 rad
- Cut flash: 3 frames (0.12 s), alpha 0.3 cream, chorus beat cuts only
- Chorus title: each word stamps in on its sung onset with overshoot + tilt that settles, then pulses on the beat
## Motion rules
1. Linework boils at 12 fps (BOIL = 12): the seed changes per boil frame; anything not moving redraws identically until the next boil.
2. Characters are cut-out puppets from painted art, drawings held on twos; acting small and weighted (slow nods, a laugh that builds and settles).
3. One real-world scale per set (px/cm measured from the plate: alley 2.6, basement 3.9); man 178 cm, jar 26 cm, fish 11 cm wherever they stand.
4. Small actions get a cut-in insert at true scale; never an oversized prop in a wide. Exaggeration only in imagined chorus collages.
5. Each shot starts 0.25 s before its lyric cue; moving a cue moves its shot.
6. Choruses cut on 4-beat phrases with a gentle camera push per beat; the bridge has no beat effects at all.
7. Atmosphere (drizzle, dust motes, lantern glow, collage blob size) breathes with measured loudness/onset per frame.
8. Deterministic: frame = f(t), renderable in any order.
## Signature (must / bonus / taboo)
- must: 12 fps line boil + paper grain multiplied over the whole frame
- must: painted cut-out puppets; the hero creature has a code-drawn eye (lid, pupil, brow) so it can look, squint, blink
- must: hand-lettered lyrics with the orange current-word underline, lane picked per shot
- bonus: choruses jump to a flat paper collage (cream ground, soft blobs, giant stamped title, prop cards)
- taboo: smooth vector tweens, glossy gradients, 3D camera orbits
## Medium
Cut paper + brush on a paper table. Stack: paper fill #F3EBDC → painted set plate (1920×1080, graded per shot) → cut-out PNG layers (57 keyed from painted sheets: cycles, poses, props, FX) → code-drawn glass vessel (back glass, water, creature, front glass) → p5.brush ink (weights 5 / 2.6, grain 40, scatter .25) + dry brush (weight 14) → static grain (55 % of pixels darkened ≤34/255) + radial vignette rgba(120,95,70,.35), multiplied. Boil 12 fps; timeline 24 fps.
## Composition
- Wides: full set plate, figure on the measured floor line with contact shadow; hero vessel on a third, caption lane opposite.
- Close-ups: face or hands fill 50–60 % of frame; plate behind darkened.
- Chorus collage: title block left ~40 %, subject right ~40 %, flat ground, no perspective.
## With media
- User photos of people: key out, place as a puppet at true scale on a painted set; add ink outline + boil; grade to the shot.
- Photos of things: prop cards in the chorus collage (like the 3 prop panels at ~0:50) or framed prints on the set wall.
- Footage/AI clips: only inside an in-world screen or window, posterised + paper-grain multiply; never full-frame live action.
## Ban list
- Photoreal faces full frame, 3D renders, neon, lens flares, kinetic-type templates, a subtitle bar, oversized props in wides, beat effects in the bridge.
## Known limits
- Source art sheets were low-res: set close-ups go soft (native 1920×1080 plates only fixed the wides).
- Generated walk cycles repeat similar leg poses.
- Verse captions (60 px Patrick Hand) read small at phone/480p size (sampled).
- Lyric times and the 132.5 BPM grid are machine estimates, not ear-checked.
- Needs a painted asset pack (sets, puppet poses, props) before any code: high upfront cost.
