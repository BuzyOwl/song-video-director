# Craft: blocking first (previs with stand-ins, shot by shot, scene handoff)

Load when starting a 3D or camera-heavy piece, when shots keep getting rebuilt, or when the creator wants to direct
shots one at a time. Adapted from Imaginative-Prompting/claude-video-skills `blocking-first` (MIT).
Directions unless tagged **Fact** (measured bug) or **Safety** (hard rule 1); a piece may break a direction with one line
in its STYLE.md.
Simple shapes iterate in minutes; detail built on locked paths never moves the camera again.
(The music-mode grey-box animatic is the 2D cousin of this. For AI clips, `engines/guide-3d.md` blocks in Blender.)

## Blocking is data
1. One data file per scene (song sections by default) + a cast list (what each stand-in really is). Times in film
   frames on the song clock; fractional frames fine.
2. **Channels:** camera = position, look (point, anchor or rotation), fov, focus. Objects = position, rotation, scale,
   `show` 0–1, plus own channels (head look, transform progress). A key may name a **parent** (rides an object or an
   anchor like `subject.head`); on a parent change, hand over in world space with speed and acceleration matched.
3. **Interpolation:** passes through keys exactly, C2 between them (momentum never breaks), monotone (no swing past a
   key), per-key options `stop`, `hold`, `gravity` (ballistic to next key).
4. Scenes tile the song with no gaps. The boundary frame belongs to both and its key is identical in both files. Each
   object has one track across all files.
5. **Pure readers are the only access:** `cameraAt(f)`, `objectAt(id, f)`, `anchorAt('subject.head', f)`. **Fact:** every
   lookup **refuses an unknown id** (a fall-through once turned every text card into cloth).
6. Stand-ins flat: shapes, flat colours, no materials/fog/shadows/post. Nothing near the hero shares the hero's colour.
   Text placeholders get one translucent colour.
7. Slow motion = one world-clock setting per scene; camera and song stay on the song clock.
8. Blocking clips render in seconds: muted 720p, song muxed from the WAV at the same offset, each shot playable alone.

## Directing shot by shot with the creator
- **Every shot starts with a question:** give the stretch's lyric and story, quote their earlier notes on it, ask them to
  describe the shot. Build nothing ahead of the answer.
- Build their words literally (word-to-number table in `craft/camera.md`).
- **One shot per round;** change nothing else.
- Fast means no polish, never no checks: smoothness over the whole scene, step every frame of the changed shot, follow
  every moving object out of frame (nothing stops mid-air), hero seen ≥50% with nothing over their head, and check the
  move a note produced as well as the note.
- On sign-off, write the scene spec (below) and freeze its data.

## Handoff to a scene session (or subagent)
A fresh session builds the real look from the spec alone. It imports the paths **read-only** (`cameraAt` for every
shutter sample, models hung on `objectAt`), never copies a path into its own code, and asks the blocking owner for any
missing path. If the blocking moves later, the scene follows by itself.

### Scene spec template (`specs/NN-name.md`)
```
# Scene NN name (start–end s, frames a–b)
## Creator's words (verbatim, oldest first, with when)
## Beats (frame | time | word / hit / action)
## Camera: one shot card per move (craft/camera.md); keys live in the blocking data, never copied here
## Everything in it (blocking id | stand-in | what it really is | scale, materials, behaviour)
## References, lighting, details the creator described
## Reusable from earlier work
## Still open (ask before building around it)
## Note checklist (their note verbatim | frame that shows it met | render checked on)
   Any change to camera, staging, set or timing unchecks every row.
```

## Verify
Data check flags gaps between scenes, mismatched boundary keys and unknown ids. Smoothness, seen and waypoint-size
probes every round. Once built: blocking still vs real still at the same frames, camera identical.
