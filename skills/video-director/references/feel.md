# Feel: turning genre, mood and emotion into numbers

Words like "sad", "hype" or "dreamy" can't be checked; numbers can. Before any build, write a **feel card**: a feel section in BRIEF.md plus `feel.json`. `film_gate.py` reads that file.

## 1. Place each section on the mood grid
- **Arousal** (calm 0 → intense 1): the section's mean `energy` from `song_facts.json`, normalised over the song, then nudged by tempo (+0.1 above 120 BPM, −0.1 below 75 BPM).
- **Valence** (despair −1 → joy +1): from the lyrics' stance, not their single words. "I'm fine" sung over a minor drone is negative. Confirm with the user's answer to Q1.
- **Emotion arc:** one line per section, e.g. "numb → cracking → release → quiet acceptance". The arc must read **with the sound off**. If a stranger can't tell the arc from 12 muted frames, the visuals aren't carrying it.

## 2. Start from the genre band
These are starting bands, not law. A reference video the user loves beats this table: measure it with `film_gate.py ref.mp4` and use its numbers.

| Genre | Cuts/min | Stillness | Motion | Camera | Palette tendency | Easing | Type |
|---|---|---|---|---|---|---|---|
| Ballad | 4–12 | 0.30–0.55 | low | slow push, breathe on the bar | warm low-sat, deep shadows | sine / power2 in-out, long | blooms, serif, few words |
| Hip-hop / rap | 18–40 | 0.05–0.15 | high on the snare | punch-ins, whips, locked lows | high contrast, one hot accent | expo out, hard cuts | slams per syllable, heavy sans |
| EDM / dance | build 10–20, drop 30–60 | build 0.2, drop <0.05 | ramps with the riser | orbit, strobe-free flashes on the drop | saturated neon or stark mono | expo / back out | sparse, huge |
| Lo-fi / chill | 1–6 | 0.50–0.80 | ambient loop drift | static or slow pan, loopable | muted pastels, film grain | sine, very long | small, handwritten |
| Rock / indie | 15–35 | 0.05–0.20 | handheld energy | handheld, push on chorus | desaturated, crushed blacks | power3 out, abrupt | distressed, cut-out |
| Devotional / folk | 4–10 | 0.30–0.50 | gentle, cyclical | rising crane, wide landscapes | earth tones, gold light | sine, symmetric | calligraphic, native script |
| Pop | 14–30 | 0.10–0.25 | bouncy on the beat | dolly moves, bright sets | bright, clean, 2–3 hues | back out (≤4% overshoot) | bold, playful, karaoke |
| Cinematic / score | 6–14 | 0.20–0.40 | builds with the swell | long takes, motivated moves | graded teal-amber or one-colour world | power2 in-out | rare, title cards |

**Mood modifiers** (apply after the genre band):
- **Valence < −0.3:**
  - lightness −10%, saturation −15%
  - colder shadows
  - slower easing (×1.3 duration)
  - more negative space
- **Valence > +0.3:**
  - lightness +10%
  - warmer highlights
  - allow overshoot
  - tighter framing on faces and hands
- **Arousal swing:** cuts per minute scale about linearly with arousal within the band. Stillness scales inversely.

## 3. The deliberate break (what makes it memorable instead of generic)
Pick **one** convention of the genre and break it on purpose, in one place, for a reason the song gives you. The band then makes the break land. Examples:
- a rap verse held in one unbroken locked shot
- a ballad's bridge that cuts on every word
- an EDM drop that goes silent and still for one bar

Write the break into the feel card with its reason.

## 4. feel.json (read by film_gate.py)
```json
{
  "genre": "ballad", "bpm": 63.5,
  "sections": [
    {"name": "verse1", "t0": 2.5, "t1": 48.5, "valence": -0.5, "arousal": 0.2, "cpm": [4, 8],  "still": [0.35, 0.6]},
    {"name": "chorus1", "t0": 48.5, "t1": 80.0, "valence": -0.1, "arousal": 0.6, "cpm": [8, 14], "still": [0.15, 0.35]}
  ],
  "still": [[124.3, 131.0]],
  "break": {"at": 155.4, "what": "bridge cuts on every word", "why": "the narrator's composure breaks"},
  "arc": "numb -> cracking -> release -> quiet acceptance"
}
```
- **Section `still`** is a band, for the stillness ratio.
- **Top-level `still`** lists intentional static spans, which are exempt from `dead_gap`.

## 5. Where it gets judged
- **Measured** (SOFT numbers, by `film_gate.py`): cuts per minute and stillness per section, against the bands; feel-sync, the correlation of motion with audio energy.
- **Judged** (rubric item "Mood and emotion match", `style-protocol.md`): does each section *feel* like its grid point; does the muted arc read; does the break land.
- **Veto:** the mood contradicts the section (a strobe in a grief verse, a giddy bounce under a eulogy).
