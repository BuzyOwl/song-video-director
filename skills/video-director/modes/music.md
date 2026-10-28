# Music mode

Distilled from three finished films:
- **Basement Goldfish:** p5.js cut-out, 132 BPM.
- **Toota Naksha:** Remotion + WebGL, a 63.5 BPM ballad.
- **Jod Ke Dekh:** three.js, 100 BPM Hindi rap; seven parallel agents built it.

## The five questions (send as one message, word for word, skipping any already answered)
1. In one line: what is the song about, and what should a viewer feel at the very end? [I'll draft it from the lyrics]
2. Format? 16:9 film / 9:16 / both, plus 2 Shorts. [16:9 + 2 Shorts]
3. Picture source? Pure code / your art or photos / AI clips (costs credits) / a mix. [pure code]
4. Lyrics on screen? Inside the world (signs, pages, screens) / clean lanes / key words only / none. [story: inside the world · lyric video: lanes]
5. Ceiling: render time per round, credits? [~20 min per full render, 0 credits]

Reply with the numbers you want to change, or "go".

## 1. Listen before you plan
```bash
python -I $SKILL/scripts/song_facts.py --audio song.mp3 --out data/song_facts.json --whisper --prompt "first lyric lines"
```
This writes:
- per-frame energy and onsets
- BPM with a drift-free beat grid; half and double tempo are printed too
- Whisper word times with confidence

Then:
- **Tempo:** sanity-check the BPM against the felt tempo.
- **Lyrics:** match the Whisper words to the canonical lyrics and tag each word:
  - **M** measured
  - **A2** two sources agree within 0.3 s
  - **A1** single source
  - **E** estimate
- **Mixed scripts** (Hindi + English): two passes, or the creator's start list. Place an unmatched word between its matched neighbours (sandwich), and break ties with the voice onset.
- **Full mix:** separate vocals first (audio-separator, Mel-Band RoFormer), then align the stem.
- **Sections:** read them off the energy curve. Breakdowns show low energy and no kicks.

**Tempo sets the motion language:**
| BPM | Camera | Cuts | Words |
|---|---|---|---|
| < 75 | breathes on the bar, slow pushes | on phrases | bloom through held vowels |
| 75–110 | moves on the beat | on the bar | pop per word |
| > 110 | punches allowed | on the beat (cut 1–2 frames *before* the beat; it reads as on-time) | slam per syllable |

## 2. Feel card + scene plan (show it, get a yes)
Write `feel.json` and the feel section of BRIEF.md (`references/feel.md`). Then one row per scene:

`range · section · emotion (valence, arousal) · what the line BELIEVES (not just says) · visual idea · camera · light · lyric treatment · engine · cost`

Also plan:
- **Hook:** something striking in the first 1.5 s. The title lands on the first measured hit.
- **One signature moment:** the frame people screenshot.
- **Callbacks:** an object or motif from verse 1 returns transformed. The ending echoes the opening.
- **Repeats grow:** chorus 2 keeps chorus 1's motif with new staging (camera, reveal, twist). Never replay it.
- **Ending in the film's world:** credits happen inside the story (the hero signs the lyric sheet). No reusable credit card.

- **Stillness is declared, never accidental.** A hold or time-freeze goes into `feel.json` `still` spans, with its reason. Even then, keep one thing alive: mist, grain, breath or a flag. A fully frozen frame reads as a bug. (Calibration on our own films found a 7 s frozen tableau and a 10 s freeze where even the mist stopped.)

Mark each timing as measured or estimated.

## 3. Animatic before art (cheap, catches 80% of problems)
Render the whole song at 480p as grey boxes plus lyric text plus cut points, with the audio. It takes minutes.
- Run `film_gate.py` on it: pacing and beat hits.
- The user approves the rhythm before any art is built.
- Changing a scene's order here costs a line of JSON; after the art is built it costs hours.

## 4. Build
- Engine rules: `engines/code.md` (or `engines/ai-clip.md` / `engines/guide-3d.md`).
- The scene table is data, `[from, to, scene, transition]`, and every scene is a pure function of t.
- **Measure the world** (painted plates and photos):
  - Each plate gets a horizon and vanishing points; px-per-cm by depth is `a·(y − horizon)`.
  - Figures carry their own cm-per-px from a rigid feature.
  - Seated figures anchor on a seat point.
- **Type system:**
  - two or three voices, fixed lanes
  - phone-readable sizes: thin serif ≥ 74 px at 1080p, sans ≥ 60 px
  - a soft scrim behind type
  - one key word per line in the accent colour
  - never over a face
- **Lyrics inside the world:** draw text on canvas textures that live in the scene (whiteboards, chats, invoices, sheets), with maxWidth auto-fit.
- **Taste anchors:** after the 3 stills are approved, save them as `anchors/`. Every new scene's still is compared to the anchors by palette ΔE and contrast (`film_gate.py --style`), so parallel agents can't drift.

## 5. Review with evidence
- **After every change:** render a contact sheet, a strip of every frame around each transition, and full-res crops at the moments that matter. Look before saying anything is fixed.
- **Small changes:** render only the changed span and join it into the last full render with ffmpeg (`engines/code.md`).
- **Final:** pull frames from the *encoded* MP4 at the flagged times.

## 6. Package and publish (with the creator)
- **Thumbnail:**
  - start from the signature still the user picked in the two-treatments step; it was designed to be the screenshot frame
  - a film frame, frozen at its best state with debug flags
  - the words placed inside the world (ink on a page, a sign)
  - no URLs on it
- **`docs/YOUTUBE.md`:**
  - title with the creator's name
  - the call to action and links in the first two lines and the pinned comment
  - chapters
  - captions (.srt from the tagged words)
- **Upload:** confirm the visibility before anything goes public, and let the creator pick the file. Tick AI disclosure when music or visuals are AI-made. Skip end cards that would cover the final shot.
- **Shorts:** pick 2–3 self-contained 15–45 s spans (a hook or a chorus). Re-frame them to 9:16 (re-lay out, never just crop), and give each a looping first and last pose.
- **Credits:** an honest "who did what" list in the description.
