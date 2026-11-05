# Craft: story and coverage (beats, shot list, editing grammar)

Load when planning what each shot is *for*: turning a song or script into beats and a shot list, or when a piece has
a nice world but no point of view. Measured camera rules live in `craft/camera.md`; light in `craft/light.md`.
From the user's own film-cinematographer skill. Engine is irrelevant: Unreal, Blender, three.js, Remotion, AI clips.

Every shot needs a subject, an intention and a reason to end. The common failure is a camera wandering a nice world.

## 1. Story first
1. **Map the structure** (song sections with times + energy curve, or the script's acts). It is the film's structure.
2. **Emotional spine in one sentence** ("a couple relives the best trip of their life, knowing it won't come back").
3. **Mood vs picture:** the picture can be sunlit while the direction carries the ache (memory haze, lingering on small
   gestures, ending shots a beat late, callbacks, a final image mirroring the opening).
4. **Each section has a dramatic job:** verse = discovery, observational · pre-chorus = anticipation · chorus = release,
   scale reveal · bridge = the turn, quiet · final chorus = montage of memories · outro = echo of the opening.
5. **Beat sheet:** one line per scene: who wants what, what changes, what we feel. Nothing changes → cut it or add a turn.

## 2. Shot grammar (what each tool means)
- **Sizes:** EWS place, scale, freedom · WS people in the world · MS action, relationship · CU emotion · insert the
  detail that matters (hands meeting, a cup passed).
- **Lens (full-frame mm):** 14–24 space, play up close · 35 storytelling · 50 neutral · 85–135 intimacy, longing,
  compression (long lens makes peaks tower).
- **Height:** eye level neutral · low heroic or the world huge · high small, vulnerable · child height wonder.
- **Moves have motives:** push-in realisation (land on the lyric) · pull-out release, goodbye, context · track alongside
  companionship · crane up transcendence · crane down arriving · slow arc bonding, fast arc joy · subtle handheld
  (~1% frame) memory, intimacy · locked-off awe, a held breath · whip energy, time jump.
- **Composition:** thirds and lead room; foreground / mid / background; frame through doorways, branches, flags; leading
  lines; faces out of the lyric area and off the edges.

## 3. Coverage and blocking (when STYLE.md picks cutting over one continuous camera)
- Per scene: establishing → medium two-shot → singles / close-ups → inserts; cut between them on action or the beat.
- **180° rule:** characters keep their sides across cuts; cross only on screen or on purpose.
- **Screen direction:** the journey moves left → right; returns right → left; consistent all film.
- Block people before placing the camera; motivate movement (walk to, reach for, turn toward a sound).
- Physical believability is directing: planted feet, real seats with no interpenetration, stride-matched walk speed,
  hands really holding props, heads turning with the eyes, weight shift before a step (`craft/motion.md`).

## 4. Transitions with meaning
Plain cut is the default and strongest (on action, beat or a look). Match cut ties places (steam → clouds). Foreground
wipe continues a journey. Dissolve / light leak = time or memory, sparingly. Push through glass or cloud = entering a
memory. Whip = energy. Never without a reason; never the same fancy transition twice in a row.
(Continuous-camera pieces use `craft/camera.md` Transitions instead.)

## 5. Words inside the world
Put a key line where someone in that world could write or see it: chalk, a finger on fogged glass, a stick in snow,
a stall sign. Reveal on the vocal onset (`craft/timing.md`), phone-readable, never over faces. Subtitle lane only when
no believable surface exists. Repeated hooks get new staging each time.

## 6. Rhythm
Verses hold 4–8 s, choruses cut on bars, final montage every bar, bridge holds long. A quiet hold before each emotional
peak. End shots **late on emotion**, **early on action** (cut while motion continues; a walk never stops dead pre-cut).

## 7. Deliverables
1. Beat sheet: section · time · beat · emotion.
2. Shot list, one row per shot:
   `# | time | section/lyric | story beat | size | lens | height | move | subject + blocking | light | transition in | words staging`
3. Continuity notes: screen direction, wardrobe, props, time of day.
4. Engine mapping: **Unreal** Level Sequence per scene, CineCameraActor with lens mm, focus tracking, real aperture
   (f/2.8 intimate, f/8 landscape), Rail/Crane rigs, Movie Render Queue with AA samples · **Blender** camera rigs with
   Track To, DOF, a marker per shot · **three.js** keyed camera table (`craft/blocking.md`).

## 8. Self-review (watch like a viewer)
Can you title each shot in five words? Anything game-like: constant-speed orbit, unmotivated floating camera, sliding or
clipping characters, flat light, empty midground, a walk freezing before a cut? Does the ending echo the opening? Is
there one signature image? Is the arc visible with the sound off?
