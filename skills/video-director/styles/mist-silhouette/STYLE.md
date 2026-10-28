# Mist Silhouette
id: mist-silhouette
Proven in: Himalayan Vow / ले चल मुझे पहाड़ों में (three.js inside Remotion, 6:44)
Best for: slow romantic, devotional, travel, sufi/folk or ambient songs about a place; long songs; 60–85 BPM
Mood: A song you breathe, not watch: tiny figures inside vast layered mountains and moving mist.
Engine: three.js · cost low (fully procedural, no image assets) · render time not logged (30 fps, 12,133 frames)
Gallery sample: gallery/samples/mist-silhouette.mp4
## Feel
- Genres: romantic ballads, travel songs, devotional/sufi, folk, ambient. Proven at 78 BPM (bar 3.07 s), D minor with a D drone.
- valence 0.0..0.7, arousal 0.05..0.45
- Cuts/min 1..5 (measured 1.3 hard cuts/min; 31 shots / 404 s = 4.6 shots/min incl. 1.6 s mist dissolves); one image per phrase held 6–12 s, up to 28 s
- Stillness ratio 0.7..0.9 (measured 0.80)
- Effects only where the song turns (~8 moments in 6.5 min)
## Palette (hex)
One colour world per section, from `src/engine/world.js` PAL (sky top / horizon / near ridge / snow / mist):
- night #0B1430 / #2A3A62 / #121A2E / #C4D2EE / #5A6C9C
- first light #2F3D5E / rose #E2B0A2 / #253244 / #F2DFDF / #CDBCC6
- morning #86A3BA / #ECDCCB / jade #40604F / #F6F5F0 / #E6E9E2
- day lapis #3A6AA6 / #BED4E6 / Kangra green #4A6A3C / #FFFFFF / #F2F6F8
- above clouds #2B5994 / #CFE0F0 / cloud floor #EEF3FA
- dusk indigo #2E3B66 / saffron #E3964C / #271F30 / #F6C398
- moon #070D26 / #1C2548 / #0C1224 / #B4C3EA
- gold sunrise #4A6FA4 / #F0B866 / #3B2F3E / #FFD9B8 / #EFC9A2
- blue hour #212C44 / #6A778F (near-monochrome bridge)
- type ivory #F6EFE2; **ACCENT Kangra gold #E8B54D** (one sung key word)
- prayer flags blue/white/red/green/yellow (sampled): the only saturated colour, used sparingly
## Type
- Sung key phrase: Tiro Devanagari Hindi 400, 80 px (≥76), ivory, one gold word, low-centre at bottom 92 px, line-height 1.32, on a radial mist scrim rgba(8,12,20,.55) ~1500 px wide, no box — https://fonts.google.com/specimen/Tiro+Devanagari+Hindi
- Handwritten: Kalam 400/700, finger-written into window fog (drawn into the fog mask) and credits — https://fonts.google.com/specimen/Kalam
- Lyrics shown only for the opening line, each chorus hook, ~1 phrase per verse, the bridge question. Never karaoke; a few phrases written into the world (fog, starlight, light on a ridge).
## Easing (numbers)
- smooth = smoothstep; easeIO = cubic in-out; easeOut cubic
- Camera breath: breath(t) = 0.5 − 0.5·cos(2π·(t − beat0) / (2 bars)) → 6.14 s cycle; drift speed and mist density swell with it
- Word bloom 0.45 s: opacity 0→1, rise 10 px, blur 6→0 px; cue in over 0.5 s (from 0.35 s before), out over the last 1.2 s
- Mist dissolve 1.6 s centred on the boundary; hard cuts only on silences
- Freeze ("time stops"): world time halts, in 0.4 s / out 0.25 s, desaturating grade; camera time keeps running
- Bloom: UnrealBloom (0.3, radius 0.6, threshold 0.93), strength = shot bloom (default 0.5) × 0.6
## Motion rules
1. The camera drifts, never punches; its speed swells and settles on the 2-bar breath.
2. Two clocks: song time t (camera, light) and world time tw (mist, flags, water, particles); tw can freeze.
3. Mist, clouds and the moon do the acting; people are small (≤15 % of frame height), from behind, as silhouettes with rim light.
4. Silences are staging cues: hold, cut or freeze on them.
5. Onset-driven micro-events (flag gusts, mist pulses on the kick, snaps) only in choruses.
6. Atmospheric perspective: each ridge paler and bluer toward the horizon.
## Signature (must / bonus / taboo)
- must: layered procedural ridges (fbm / ridged-noise shader planes) with volumetric mist planes between them
- must: two small back-facing silhouettes with a rim-light mask (light from the left; UV-mirrored for the right)
- must: mist dissolves between shots; one colour world per section
- bonus: a ridge finger-drawn on a fogged bus window that becomes the real range; the moon coming down to sit beside them; a time-freeze before the last chorus
- taboo: faces, close-ups of people, karaoke lyrics, neon, gloss
## Medium
Gouache ridges + volumetric mist + soft bloom. Sky gradient (top → horizon) → 4–6 ridge planes (ShaderMaterial, per-layer haze lerp) → instanced deodars, slate-roof temple, prayer flags, river ribbon, cloud sea, stars/moon → drifting mist planes on world time → code-drawn silhouette sprites (R = body mask, G = rim mask) → bloom → warm-lift grade → fine grain + gentle vignette. Painterly, not photoreal; borrows the Pahari/Kangra miniature idea (layered hills, jewel colour, tiny lovers in vast nature).
## Composition
- Horizon on the low or high third; huge sky or cloud sea; figures tiny, off-centre, often on the horizon line.
- Lyric scrim low-centre; keep figures out of the lower 25 %.
- Leading lines: river, road/thread ribbon on a ridge face, flags strung across the top third.
## With media
- Photos: as a distant far layer (posterised, palette-matched, 2+ mist planes over it) or as a print left at a place; never a sharp face.
- Footage/AI clips: through the fogged window, or as the far layer behind mist; match the section's colour world.
- User text: Kalam written in window fog.
## Ban list
- Faces, close-ups, beat-punch zooms, glitch, shake, fast verse cuts, a lyric line for every sung line, more than one accent colour per frame (flags excepted), photoreal textures.
## Known limits
- Peaks read as flat low-poly triangles and the cloud-sea texture repeats at 480p (sampled): "screensaver" risk.
- Long holds (up to 28 s) need strong mist motion or they feel static; there is little story.
- Lyric scrim text is small/low-contrast over bright cloud seas (sampled ~2:44, ~5:41).
- Scale jump when a silhouette is near camera: a giant dark head fills a third of frame (sampled ~1:28).
- Lyric timing is Whisper-aligned, not ear-checked; the song's real ending (hard full-band hit) differs from its lyric sheet.
