# Craft: motion (anything that moves: characters, props, type, effects)

Load when animating or reviewing motion, or when a note says "pops in", "stiff", "floaty", "fake", "dead".
Camera has its own rules (`craft/camera.md`). Adapted from Imaginative-Prompting/claude-video-skills
`animation-principles` (MIT). Characters with their own movement style (a cartoon, a liquid, a realistic person) get
their own motion file in the piece's folder, on top of this one.
Directions unless tagged **Fact** (measured bug) or **Safety** (hard rule 1); a piece may break a direction with one line
in its STYLE.md.

## 1. Every frame is a pure function of time (hard rule 7)
Renderers draw frames out of order and in parallel chunks.
- **Physical state is re-simulated, not remembered:** springs and lag re-run from t=0 on a fixed step (1/120 s), or
  baked once into a track and sampled.
- Seeded noise only. One timeline owns timing (never a shader's hidden clock).
- **Speed is a parameter:** each action takes one `speed` that scales all its phases, so it retimes without a rebuild.
```ts
function springAt(t, target, k = 120, c = 14, dt = 1 / 120) {   // follow-through, still f(t)
  let x = target(0), v = 0;
  const step = (s, h) => { v += (k * (target(s) - x) - c * v) * h; x += v * h; };
  const n = Math.floor(t / dt);
  for (let i = 0; i < n; i++) step(i * dt, dt);
  step(n * dt, t - n * dt);
  return x;
}
```

## 2. Grammar of a move: hold → anticipation → action → overshoot → settle
| Phase | Cartoon / elastic | Realistic person |
|---|---|---|
| Hold | 6–8+ frames on a key pose | 10–15+ frames |
| Anticipation | ~0.2 s, opposite way, ease-out | 0.25–0.5 s, often a breath in |
| Action | ~0.15 s sharp ease-out (snap) | 0.25–0.6 s, minimum-jerk reaches |
| Overshoot | a few cm, ~30% squash | ≤5%, in rotation not position |
| Settle | ~0.45 s damped spring | 0.5–0.9 s, heavier damping |
- Default: nothing alive moves linearly (it reads mechanical).
  Pushed = ease-out; falling or giving up = ease-in; impacts are never eased to a stop.
- Settles start with zero slope: `settle = u => 1 - Math.exp(-k*u) * (Math.cos(w*u) + (k/w)*Math.sin(w*u))` (k≈6, w≈14).

## 3. Arcs, overlap, follow-through
Moves travel on arcs. A body is a chain (root → spine → head/limbs, a few frames apart). Loose parts (hair, cloth,
strings, fingers) lag on springs. Velocity is continuous across path segments unless the stop is the point.

## 4. Every action moves the material it acts on
- Cause → propagation → consequence. A local hit doesn't make every part react at once.
- Travel changes the body: acceleration trails loose material, turns throw it out, braking lets it overtake and recoil.
- Carry displaced state forward; don't reset after every hit.
- **Idle wobble isn't a reaction.** Change the stimulus and the deformation must change with it.
- Music-driven things land their accent **on** the beat, not a slow move that starts on it and peaks late.

## 5. Alive by default
Breathing (~4–5 s at rest; held in anticipation, released after), per-limb idle noise 1–2° out of phase, weight shifts
every few seconds, attention always aimed at something. Check a 6 s rest loop, never one still.
A truly still figure is a choice (a storytime hold, a frozen beat), declared, never accidental.

## 6. Weight, gravity, impacts
Gravity accelerates (ease-in or real ballistic arc). An impact has a contact frame at peak speed, then compression,
damped rebound, settle. First part to land stops first. Heavy starts slow and stops hard; light reacts fast and floats.
What it touches reacts (a chair rolls back, a cushion gives, a car dips its nose).

## 7. Nothing pops in
- Default entrance animates over 6–12 frames; type letter by letter where it fits. Faster on purpose is fine (a
  storytime pose swap ~0.1 s, a wake into video in 5 frames, a slam, a hard cut); an accidental pop is not.
- **Starts on its cue by default** (a word's measured onset, `craft/timing.md`); an unplanned wind-up that reads before
  the cue looks early. Running ahead as foreshadowing or a lead-in is a choice the brief names (hard rule 5).
- Hidden ≠ absent: an edge-on card flipping in its last half frame is still a pop.
- **Grow out, never through:** draw things rising from a surface only once their face clears it (~3 cm close, ~0.4 m at
  city scale). Scaling depth up from 0 z-fights.
- Exits leave the frame or animate out.

## 8. Smears and blur
Cartoon shapes smear along their real path over the last ~0.07 s, gated by speed. Realistic people get motion blur,
not smears. Camera and fast objects get shutter-sample blur in finals (`craft/render.md`).

## 9. Contacts
Every moving part's sweep is clear of the props round it on every frame (probe it). Hands land on what they work;
planted feet don't slide; nothing passes through a body or desk unless designed; placed things stay fixed to their surface.

## Verify
Typecheck → probe framing/image speed → draft render → frame-difference spike scan (`craft/render.md`) → step
consecutive frames round every spike, contact, entrance, impact → 100% crops of hands, eyes, type → watch at 1× as a loop.
For a reaction, compare with the stimulus off: the difference must be the response, not idle motion.
**Fact:** every-Nth-frame sheets hide strobing and one-frame pops.
Don't relay "no pops" from someone else without stepping the frames yourself (hard rule 3).
A rework adds to the existing beats; it never drops the point the shot already made.
