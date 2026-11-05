# Pop Era Collage
id: pop-era-collage
Proven in: My Teacher Used To Say (Canvas2D engine + Blender-baked 3D clips, 4:21)
Best for: nostalgia and time-passage songs, then-vs-now commentary, life-journey ballads with a message; 60–100 BPM
Mood: A Spider-Verse-style journey through 40 years where every era is a different painter, tied together by comic print.
Engine: Canvas/WebGL (huashu Canvas2D engine, Playwright render, 24 fps, 6,269 frames; budget <150 ms/frame ≈ 16 min) + three.js clips of Blender sets with Cycles-baked light · cost high
Gallery sample: gallery/samples/pop-era-collage.mp4
## Feel
- Genres: message ballads, generational pop, coming-of-age, diaspora stories (village → Gulf → city). Proven at 72 BPM (bar 3.33 s).
- valence −0.3..0.7, arousal 0.35..0.75 (visual energy runs above the music)
- Cuts/min 10..16 (measured 12.9 hard changes/min incl. panel slams); segments 9–39 s joined by camera moves
- Stillness ratio 0.05..0.2 (measured 0.14): camera never stops, no locked frame >2 s
## Palette (hex)
Most-used values in `scenes/j_*.js` + `lib_teacher.js`:
- comic red #E0262C / #D8232A
- **ACCENT pop yellow #FFD23F** (caption boxes, "DIAMONDS", impact stars)
- royal blue #2A4A9A, navy #1C2458
- newsprint cream #F4EFE2, paper #FBF8EE, ink #111018 / #0D0B0A
- night/office violet-greys #2A2833, #5A5478, #C9C4D6
- hero rim gold #FFCC66; Klimt gold #E0B24A / #E8C870
- Dalí sand-browns #3A2410, #8A5A34 (with year stamp #2A2018)
- magenta #FF45C8 (misregistration ghost, neon only)
- Each world keeps its painter's palette, limited to ≤5 colours + ink
## Type
- Comic captions/slogans: Bangers (most used) https://fonts.google.com/specimen/Bangers ; poster heads Anton https://fonts.google.com/specimen/Anton ; Archivo Black https://fonts.google.com/specimen/Archivo+Black ; world-specific Lilita One, Alfa Slab One
- The mentor's voice: Kalam 700 as chalk — https://fonts.google.com/specimen/Kalam (the refrain line is always chalked onto a surface)
- Year stamp: Marcellus 400, 54 px, top-right (x 1860, y 92), rolls over 2.0 s at an era change — https://fonts.google.com/specimen/Marcellus
- Engraved/pencil notes: Cormorant Garamond italic, Caveat
- Key words ≥80 px; one accent word per line bigger or coloured
- No fixed lane: words sit in world space as the world's material (chalk, hay, cloth, neon, speech bubbles, slogans, dots, drone lights, tape, gold) and move with the camera; keep x >1450, y <200 free for the year
## Easing (numbers)
- ease = cubic in-out; outBack c1 = 1.70158 (pop-ins); twos(t) = floor(t·12)/12
- World animation on twos (12 fps), camera on ones (24 fps); accents snap on beats and sung words
- coalDive transition 0.9–1.0 s: push into the hero object at (960,540), ~110 px; next world pulls out from it
- lightBloom transition 0.9–1.4 s: through bright light, segment ends bright
- Year counter roll 2.0 s
## Motion rules
1. Each segment is ONE continuous camera move through 4+ depth layers (far/mid/near/foreground), layers cached 1.4× oversize.
2. No locked-off frame >2 s: dolly, crane, orbit, push past foreground, whip on a beat.
3. The hero object (coal → diamond at 186.8 s) is almost always on screen and doing something (rolls, carried by a crow, bounces, rides); camera follows it.
4. Lyrics appear word by word on sung time in world space and leave by the camera passing or the material blowing away, never blinking off.
5. Verses calm, choruses bolder, finale biggest (grid slam, gathering of 9 panels, bloom to white).
6. Comic devices: split panels, caption boxes, speech bubbles, speed lines, impact frames, Ben-Day dots, misregistration on accents.
7. No people or faces: traces only (bag, cup, bicycle, clothes on a line); animals allowed (crow).
## Signature (must / bonus / taboo)
- must: one hero object drawn in the same bold inked comic style in every world
- must: per-era art-movement skins (Monet → Van Gogh fields, Ghibli courtyard, pop-art night city, Dalí desert, Shinkai sky, Hopper office, Klimt gold) unified by print language
- must: year stamp top-right rolling forward through time
- bonus: agit-prop poster panels (red/black/cream, diagonal wedges, Anton slogans) for then-vs-now lines
- taboo: generic glow gradients, default neon grids, symmetrical stock skylines, decorative lens flares
## Medium
Comic print over painted worlds + baked 3D rooms. Per-world Canvas2D painters (brush/paint libs, cached static layers) → ink outlines → Ben-Day halftone dot fields → cyan/magenta misregistration ghosts (0.35 on the hero) → year stamp. Real rooms (village classroom, school) are Blender sets with Cycles-baked lighting rendered in three.js as clips, comic sprites composited in. Finale = panels of every world taped onto cream paper.
## Composition
- Hero object at screen centre (960,540, ~110 px) at every boundary; elsewhere on thirds at 50–110 px.
- Strong silhouettes, clear value structure, flat colour fields; diagonals for poster panels.
- In painterly worlds keep y >860 calm when text sits there; top-right reserved for the year.
## With media
- User photos: taped polaroids/panels on paper (finale grid) or screens inside a world (phone, TV niche, smart board), halftoned with an inked edge.
- Footage/AI clips: inside panels or screens with halftone + misregistration so they read as print, or as a "3D world" segment between painted ones.
- A user's own object can replace the hero if drawn in one consistent inked style.
## Ban list
- Slideshow wipes between static tableaux, people/faces, logos/brands, AI-slop clichés, more than one hero, text over busy paint without a material/scrim.
## Known limits
- Hardest look to build: ~10 bespoke world painters (scene files 40–115 KB each) + Blender sets; 9 versions to land.
- Style-hopping reads as a "PPT slideshow" (first-cut verdict) unless every segment is one continuous camera move.
- Generic painterly worlds look like AI slop (first night city); the Dalí world took 3 rebuilds.
- 3D set bugs (chairs facing backwards: glTF quaternion rotation) cost days.
- Low stillness (0.14) tires the eye on a slow ballad; lyrics compete with the art in busy worlds.
