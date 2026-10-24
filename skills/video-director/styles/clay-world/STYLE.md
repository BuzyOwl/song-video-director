# Clay World
id: clay-world
Proven in: Jod Ke Dekh (three.js inside Remotion, 4:12)
Best for: rap/hip-hop, spoken word, motivational or satirical songs built on wordplay and metaphors rather than a story; 85–110 BPM
Mood: A dark gallery of glowing metaphors where a faceless clay figure stitches ideas together with light.
Engine: three.js · cost med (no image assets; motion blur costs n renders per frame) · render time not logged (30 fps)
Gallery sample: gallery/samples/clay-world.mp4
## Feel
- Genres: Hindi/English rap, spoken word, motivational pop, workplace satire, explainer songs. Proven at 100 BPM (beat .6 s, bar 2.4 s).
- valence −0.3..0.6, arousal 0.45..0.85
- Cuts/min 10..15 (measured 12.4 hard cuts/min) plus 0.5 s line-wipes between 9 scenes
- Stillness ratio 0.2..0.4 (measured 0.30); three dropouts held still
- Tempo grammar: a new idea every bar in verses, every beat in double time, every 2 bars in the half-time bridge
## Palette (hex)
Sourced from `src/engine/kit.js` COL/mats and `type.js`:
- night #070A12 (void/sky), haze #0B1020, gloss floor #0C0F16, walls #23242A, wood #2A2018, core #141821
- clay #BFB6AA (mannequin, props), clay dark #5A5650
- glass tint #9FB8D8 (silos), cool fill light #8FB0FF
- type ivory #F3EEE6
- **ACCENT haldi/turmeric #F2C14E**: the thread and exactly one key word per line
- warning red #E5484D (blame/warnings only), metallic gold #F5C15A (crowns)
- dusk set: lavender → peach sky ≈ #B7A2C4 → #E6B79E (sampled)
## Type
- Lyrics: Anek Latin + Anek Devanagari, variable weight and width, one family so English (Roman) and Hindi (Devanagari) read as one voice — https://fonts.google.com/specimen/Anek+Latin , https://fonts.google.com/specimen/Anek+Devanagari
- Spoken/ironic voice: Instrument Serif italic + Tiro Devanagari Hindi italic — https://fonts.google.com/specimen/Instrument+Serif , https://fonts.google.com/specimen/Tiro+Devanagari+Hindi
- Handwriting (lyric sheet, pen): Kalam — https://fonts.google.com/specimen/Kalam
- ≥72 px on screen at 1080p; key word turmeric, heavier and wider; sentence case; auto-fit to the surface, never overflow
- Lane = a surface in the world (phone chat, whiteboard, wall, silo, sign, receipt, floor). Fallback: low-centre, bottom 96 px, in scene light, soft shadow, no box
- Words appear one by one on the sung onset (fade + rise)
## Easing (numbers)
- smooth = smoothstep; easeIO = cubic in-out (default for keyframed camera tracks); easeOut/easeIn cubic
- Scene join: turmeric line-wipe, 0.5 s centred on the boundary, smoothstep, slightly tilted line sweeping left→right, composited in linear HDR before bloom
- Bloom: UnrealBloom strength 0.55, radius 0.45, threshold 0.82; ACES filmic tone map, exposure 1.0
- Finish shader: vignette 0.32 (smoothstep .35→1.15 from centre), grain 0.035
## Motion rules
1. Camera always moving but slow (dolly, truck, flythrough between objects, one crane-dive in the bridge); cuts/pops on kicks only in hooks.
2. No shake (one hammer hit in the whole film), no glitch.
3. Never crossfade bodies; the mannequin moves only by joint rotation.
4. One focal thing per frame, lots of empty dark space.
5. Motion blur by 10–12 subframes, only on whips and fast flights.
6. Each scene must look right from start −0.5 s to end +0.5 s (wipe overlap); no own fades unless a dropout to black.
7. Frame = f(t): hash() noise, keyframe tracks, no accumulation.
8. The story loops back to its first set (bookend).
## Signature (must / bonus / taboo)
- must: faceless warm-grey clay mannequin (~1.75 m, roughness .78) as the only character
- must: turmeric thread, a glowing tube that joins things and doubles as the scene wipe
- must: lyrics living on world surfaces, one turmeric key word per line
- bonus: Devanagari shirorekha pun: the thread lands as the headline bar joining letters; the final pull-up shows the set spells the title
- taboo: subtitle bar, or boxes/pills behind lyric type
## Medium
Clay + glass + bloom in a black box. MeshStandard clay (roughness .8), MeshPhysical frosted glass (roughness .12), dark gloss floor (roughness .32) reflecting emissive type, one motivated key light per scene (screen, lamp, window, dawn) + light haze, PCF shadows, ACES, UnrealBloom, vignette + grain pass. Text = 2D canvas textures on planes, emissive where lit from within.
## Composition
- Figure small (10–25 % of frame height) against large dark negative space; the type surface is the hero.
- Low three-quarter camera, wide lens in rooms; corridors as a dollhouse cross-section trucked sideways.
- Objects in rows receding to a vanishing point; the thread draws the leading line.
## With media
- Photos/footage as textures on in-world screens, posters, phone UIs, whiteboards or framed on walls, lit by scene light, under bloom.
- AI clips: on a monitor or projected onto a wall in the dark set; never full-frame.
- Logos: on signage planes, desaturated, never turmeric.
## Ban list
- Teal-orange grade, default "AI orange", glitch, shake, neon grids, a face on the mannequin, crossfaded limbs, boxes behind lyrics, red for anything but blame/warning.
## Known limits
- Dark-heavy: ~31 % of seconds have mean luma <22/255 (measured); murky on phones and at 480p.
- Several frames are a lyric alone in the void: weak as images.
- Faceless mannequin limits emotion to posture; mid-shot acting reads stiff (sampled).
- Wipes + motion blur give smeared frames (sampled ~1:58).
- Lyric timing machine-aligned, not ear-checked.
