# Style protocol: from "inspired by" to "recognisably this look"

Adapted from huashu-art-motion protocol 16 (alchaincyf, MIT). Its finding: a style built from a text description alone came out as the same flat modern illustration with a new palette and noise. And its makers' self-scores ran about 10 points (up to 17) higher than independent review.

Use this protocol for every look: every song gets a new one, and every brand look is built with it once.

## 1. Anchor in real works (never from memory)
- Gather at least 3 **different** references: the user's links or images, public-domain works (Met Open Access, Wikimedia Commons), or film stills for study only (FILMGRAB).
- Save them in `refs/`, build one contact sheet, and extract the palette (k-means over the pixels gives hex values).
- **Look at the sheet,** then write:
  - **5 signature traits,** each tagged must-have / bonus / taboo. Example, for Ma Yuan ink: must-have one-corner composition, large empty space, axe-cut texture strokes; bonus willow, a tiny figure gazing out; taboo full-frame fill, bright colour.
  - **Palette:** the extracted hex values, plus which way the lights and the shadows lean.
  - **How it is physically made** (brush, cut paper, woodblock, film stock, cel, clay). That physical process is the renderer's spec.

## 2. Compose by the style's own logic
Every style organises the frame in its own way:
- Ma Yuan: one corner plus emptiness.
- Persian miniature: the ground tipped up, every surface filled.
- Gauguin: foreground crops and diagonal splits.
- Shinkai: half the frame sky, lens flare from practical lights.
- Wes Anderson-like: centred symmetry and planimetric staging.

Write one sentence, "this style composes by …", and lay out the new subject by it. Never reuse another piece's layout.

## 3. Shape layer, then medium pass
Noise on top of flat vectors is not a style. Build two layers:
- **Shape layer:** clean forms, figures and space.
- **Medium pass:** the forms run through the real medium:
  - broken directional strokes (impressionism)
  - pigment sunk into plaster (fresco)
  - silk weave plus dry-brush (ink)
  - thick uneven outlines with in-fill strokes (cloisonné, Gauguin)
  - hatching (woodcut, etching)
  - halation plus gate weave (film)

If the library has no pass for the medium, write one as a reusable function; never hard-code it into one scene.

## 4. One frame first, side by side
Render one still before any animation, then place it next to the references:
`ffmpeg -i refs/a.jpg -i still.png -filter_complex "[0]scale=-1:720[a];[1]scale=-1:720[b];[a][b]hstack" cmp.jpg`.

"Is it recognisably this look?" is answered only from that image.

## 5. Move by the style's own motion logic
- One main action plus 2 looping motifs.
- Use the style's own way of moving: ink drifts with the wind, strokes breathe, reflections shatter, frescoes barely move while gazes and handoffs do, cut paper steps at 12 fps with boil.
- No generic fade-in on every element.

## 6. Score: 100 points, threshold 80, at most 2 repair rounds
| Item | Points | How it is judged |
|---|---|---|
| Signature hit | 25 | tick off the must-haves; −5 for each one missing; −5 for each taboo present |
| Mood and emotion match | 20 | each section reads as its valence/arousal point; the arc reads in 12 muted frames; the deliberate break lands |
| Feel targets | 15 | the `film_gate.py` cuts/min and stillness per section, against the feel card bands. Feel-sync is never scored: it read about 0 on every finished film. |
| Medium credibility | 10 | at a 1:1 crop: a real medium, or vector plus noise? |
| Composition and story | 10 | the style's own layout logic; the event reads at a glance; thumbnail-size test (160 px wide) still reads |
| Motion and music sync | 10 | hits on the grid; motion follows the energy; nothing on screen under 0.3 s |
| Type and faces | 5 | lanes, phone-readable size, accent discipline, nothing over a face |
| Technical | 5 | deterministic, no flicker, a clean encode |

**Vetoes** (any one is a fail, whatever the total):
- signature hit below 15
- the hero or main subject looks childish or like a sticker
- the mood contradicts the section
- a `film_gate.py` HARD failure

## 7. Independent review (mandatory before delivery)
- Spawn a **fresh subagent** that has not seen the code or the conversation.
- **Give it:** the refs contact sheet, the side-by-side, 12 frames across the film (muted), the gate report, STYLE.md, the feel card and this rubric.
- **It returns:** item scores, the signature checklist, vetoes, and the 3 biggest fixes.
- **The lower score counts.** Report both.
- **Taste** (is it beautiful?) is flagged for the human. The AI never writes "taste approved".
- If the score is still under 80 after 2 rounds, say so plainly. Name what's stuck, and don't call it done.

## 8. Taste anchors (consistency across scenes and agents)
- After the 3 stills are approved, copy them to `anchors/`.
- Every later scene still is checked against the anchors: palette ΔE, contrast histogram, grain level (`film_gate.py --style STYLE.md` reads the hex values).
- Parallel agents get `anchors/` in their brief.
- Drift beyond the anchors gets fixed before integration, not after.
