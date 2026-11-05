# Craft: camera (moves, framing, transitions, balance)

Load when keying or reviewing any camera, writing a shot plan, or when a draft reads "bland", "floaty", "game-like".
Story and coverage come first (`craft/story.md`); moves start and land on the timing map (`craft/timing.md`).
Adapted from Imaginative-Prompting/claude-video-skills `shot-design` (MIT), measured on four finished films.
Directions unless tagged **Fact** (measured bug) or **Safety** (hard rule 1); a piece may break a direction with one line
in its STYLE.md.

## The bland first pass (each one was sent back on those films; use one only on purpose)
- **Observer shot:** eye level, 2–4 m, mid lens (35–50° vertical), subject centred, nothing near the lens or far behind.
- **One axis, one speed:** a straight push or pull. Nothing turns, nothing passes the lens.
- **Waypoint-and-stop:** arrive, hold, move, hold.
- **Stick camera:** fixed offset from a moving subject, so it sits centred all shot.
- **Looking down** 35–45° onto a few people. **Same size all section.** **Nudges** under ~0.3 m or ~10°.
- **Creeping zoom** in every hold. Hold the framing with a slight kick shake instead (`craft/timing.md`).
- **Softened words:** creator says "at the edge" and you put it a third in. Use the table below.

## Procedure
1. List the section's beats (sung onsets, drum hits) from the timing map.
2. **One shot card per move.** First line: "From [start frame], [move] so we [reveal / follow / feel] [what], landing on
   [end frame] on [word or beat]." If the only verb is "show", the move has no reason.
3. Spec every waypoint (Framing below), with the creator's words built literally.
4. **Variety pass:** table of waypoints (size, height, side, lens, place in frame). Neighbours differ in 2+ columns.
5. Key the moves (rules below). 6. Probe before rendering (Verify). 7. Frame sheet every 2–4 frames for composition + each
   waypoint as a full still, judged as a photograph. Sheets hide pops: approve motion by stepping every frame (Verify).
   Then watch at speed with the song.

## Moves
- **Something big changes:** shot size ×2+, or 45°+ orbit, or 1 m+ height, or a reveal. Ending near the start = wasted.
- **Two axes, one leading:** push+rise, orbit+push, truck+pan, dolly+tilt. A pure zoom or a pan from a fixed
  spot reads flat in a 3D world; punch-ins on talking footage and log zooms in explainers are their own grammar (modes).
- **Parallax always:** something 0.5–3 m from the lens crosses 20%+ of frame; something far behind.
- **Lens by intention:** wide (60°+ vertical) close for energy; long (≤25°) from far for compression and intimacy.
  Mid lens at mid distance is the bland observer look; use it on purpose (35 storytelling, 50 neutral, `craft/story.md`).
  In 3D, move the camera rather than zoom to enlarge.
- **Height with meaning:** default near level, ≤20–25° down, horizon in frame. Steep top-down is a short beat.
- **Subject travels** through frame: under ~60% of a move in the middle third.
- **Speed is musical:** start and land on beats, speed into accents, slow (never stop) through held notes. One rise, one
  fall per move. Next move eases in under the last; travel direction turns ≤ ~10°/frame.
- **Monotone and decisive:** each parameter changes one way. No swing past and back; slerp look directions, never lerp
  a look-at point.
- **Holds are directed:** default a slow drift or a held framing with beat shake (dead-still 1–2 beats a section on the
  films). A locked-off hold is a choice (awe, a held breath, storytime, landed boards): declare it in feel.json `still`.
- **The shot comes first.** Words on screen are placed into the shot after. Default: no lyric moves, slows or aims the
  camera (every such blanket rule hurt the films and was withdrawn); one move landing on a line on purpose (a push-in
  realisation, `craft/story.md`) is a story choice.

## Transitions (STYLE.md picks: one continuous camera, or coverage cutting from `craft/story.md`)
**Continuous camera** is an optional style (the reference author's one-take habit on their films), not a default:
- A list of views is one move between them. A "shot change" is a fast whip/arc/pull-out with blur. A following camera
  never drops to zero speed between moves.
- **World change = push into a shape** (window, moon, a letter's counter); the next world fades in inside it and grows
  past the edges while the push continues. A plain dissolve reads as a shortcut.
- **Through an object:** travel through real geometry; show the new place the moment the camera is inside. No white flash.
- **Cut** only when asked, or behind a full-frame push. At that cut nothing changes: pose, facing, gaze match both sides.
  Cut before a whip starts, never inside it.

## Framing (one line each per waypoint)
Beat served · subject + size · place (third, side) · angle · lens · fg / mid / bg · edges.
- **Sizes:** ECU detail ≥60% width · CU head ⅓–½ height · MCU chest up · MS waist up · WS whole body ⅓–½ height ·
  EWS subject <10% height. Neighbours differ by one size or 45°+.
- Eyes on the upper third; subject on a vertical third facing the bigger space (lead room ≥ ⅓). Centre only for symmetry.
- 2+ of 3 layers; soft, edge-cropped foreground. Lines lead to the subject. Nothing important within 5% of an edge;
  crop people between joints. Subject separates from background by value or colour. Roll 0 unless banking.
- **One-glance story:** at the size it's seen small (a phone feed ~360 px wide; a thumbnail, `modes/youtube.md`) the
  frame says the idea with no words.

| Creator says | Build |
|---|---|
| "at the edge" | subject at ≥0.9 of frame width |
| "close-up" | head ⅓–½ of frame height |
| "ECU" | detail ≥60% of width, never just "closer" |
| "framed by A and B" | subject in the screen-space notch between A and B (measure the gaps) |
| "wide angle" | ~60°+ vertical, close to the action |
| "in frame" | 50%+ of the subject reached by rays from the lens, not just its centre |

## Balance (measured on three finished films; a reference, not a target)
| | Films | Rejected draft A | Rejected draft B |
|---|---|---|---|
| Still (picture speed < 0.04 frame-widths/s) | 30–40% | 18% | 17% |
| Median picture speed | 0.06–0.11 fw/s | 0.19 | 0.15 |
| Moves per 10 s | 4.9–6.9 | 6.2 | 8.0 |
| Moves that land and hold ≥10 frames | 18–35% | 8% | 14% |
A never settled (glided all the time, no close-ups, 63% high). B, told "too slow", tripled the whips and still never held.
Shared shape: quiet verses (still ~half the section, 3–7 s holds), energy saved for pre-chorus/chorus, a long still
stretch near the end. Time spread across every shot size; mostly level to slightly high.

| Share of film time (3 films) | |
|---|---|
| Size | ECU 1–12% · CU 3–7% · MCU 4–9% · MS 4–11% · MWS 5–15% · WS 13–14% · very wide 12–20% · EWS 5–11% · no figure 16–31% |
| Height | eye level 24–33% · high or slightly high 41–47% · Dutch 1–7% |

## Verify (whole scene, every round)
- From the camera function per frame: turn ≤90°/s, turn change ≤250°/s², speed change ≤12 m/s² (4 for slow moves),
  travel direction ≤300°/s, no reversal. Faster only on a designed whip with blur. At large scales measure pace
  (speed ÷ view depth): ≤4/s, changing ≤12/s².
- Image speed: points at subject distance projected into the next frame, < ~120 px/frame at 1080p except whips.
- Subject size + place at each waypoint vs spec; seen ≥50% every frame; no pass nearer than ~0.3 m unless designed.
```ts
// turn-rate probe over a pure camera function (30 fps)
for (let f = a; f < b; f++) {
  const dps = THREE.MathUtils.radToDeg(cameraAt(f).quaternion.angleTo(cameraAt(f + 1).quaternion)) * 30;
  if (dps > 90) console.log(`f${f}: ${dps.toFixed(0)}°/s`);
}
```

## Failure modes
- **Fact:** approving camera from 3–8-frame sheets
  (passed a mid-air stop, a snap, a 687°/s whip). Step every frame of the shot.
- Answering the creator's eye with a metric. A number that disagrees with what they see is a broken metric.
- Re-staging approved shots while fixing one. A camera round touches only the frames the note names; diff the rest.
- **Fact:** sparse keys on an orbit stall where a coordinate turns; key a computed path or interpolate in angle.
- **Fact:** a spline key edit leaks into its neighbours' timing. Pin the neighbours' rates; diff the old path vs the new.
