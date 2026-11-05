# YouTube mode: long-form edit (3–30 min) plus Shorts

Use for explainer, vlog or tutorial footage, or narration, cut into a 16:9 video plus Shorts.
Follow the hub front door and hub rules; they are not repeated here. Engines: `engines/code.md` for
the Remotion comp. Use `engines/ai-clip.md` only for b-roll that cannot be filmed or found.

## 0. Front-door defaults for this mode
- Look shortlist (offer 3): **clean-talk** (face + t2 screenshots + y5 chapter cards), **explainer**
  (t1/y1 animation-led), **documentary** (y2 collage + t3 charts). Grammars are listed in §3.
- 5 questions, with defaults: target length (= the cut, never padded) · 16:9 1920×1080 at source fps, plus 2 Shorts ·
  language en (hi → `--lang hi`) · at most 2 grammars besides the face · thumbnail with face: yes.
- Brief adds: chapter list, captions as CC (burned only on Shorts), mix at about −14 LUFS integrated, true peak
  ≤ −1 dBTP, music bed 15–20 dB under the voice.

## 1. Inputs and the cut
| Input | Do |
|---|---|
| Talking head, vlog, any footage with speech | Cut it with `prep.py` (below). |
| Screen recording + voice | Same cut. The screen is the main picture; the face goes in a PiP or cutaways. |
| Narration audio only | First wrap it: `ffmpeg -f lavfi -i color=black:s=1920x1080:r=30 -i voice.wav -shortest -c:v libx264 -c:a aac narr.mp4`. Then cut it. The face track reports 0 faces; ignore that. |

    python -I $SKILL/talking/scripts/prep.py "<video>" <work> --pause 0.25 [--lang hi] [--drop i,j-k] [--keep i] [--cut a-b]
- `--pause` 0.22–0.3 for long-form (0.12 is reel-punchy). Long footage: run it in the background.
- Read `<work>/cut.txt` exactly as `modes/talking.md` §Cut says. Judge `[soft?]` fillers by meaning.
- Files used here: `cut.mp4`, `words.json` (word times + `emphasis[]`), `cut.txt`, and `track.json`
  (per-frame face box `[cx, cy, w, h]`, normalised, plus `w`, `h`, `fps`).

**16:9 vs the talking pipeline.** `compile.mjs` throws unless the source aspect matches `size` (default 1080×1920).
- Default for long-form: keep the prep cut, then build your own 16:9 Remotion comp (`engines/code.md`) that reads
  `cut.mp4` and `words.json`. Borrow the card ideas, not its lanes.
- Quick pass only: setting `"size": [1920, 1080]` in edit.json passes the check, but the lanes, caption size and face
  bands were tuned on 9:16. That is untested, so preview every card with `--range a:b` first.
- Never crop the main long-form to 9:16. Crop only for Shorts (§5).

## 2. Retention structure
| When | Rule |
|---|---|
| 0–5 s | Hook: open on the payoff (the end result, the strangest frame, or the question). First word ≤ 0.5 s. A visual change by 2 s. No logo, no "welcome back". |
| 5–30 s | The promise and why to trust it. Content starts by 30 s. |
| Every 60–90 s | Re-hook: an open loop ("in a minute I'll show…") or a payoff tease. Place it at a chapter start. |
| Every ≤ 20 s | Something new on screen: b-roll, graphic, angle, or punch-in (1.1–1.2×, alternate long takes, land on sentence breaks). |
| A concrete thing named | Show that thing (literal over abstract). B-roll in on the word ±0.2 s, 2–6 s long, voice keeps running (L-cut). |
| Dead air | `--pause` squeezes it. Also cut tangents that serve no chapter, retakes, and "so that's it / to wrap up". |
| Chapters | Take them from topic shifts in `cut.txt` (new subject, "step 2", "next", "so why"). ≥ 3 chapters, first at 0:00, each ≥ 10 s (YouTube rule); aim for 1–4 min each. Chapter card 1.5–2.5 s (y5). |
| Last 5–20 s | End screen. Give a verbal CTA to one named next video before it starts. Keep the frame clear for 2 video tiles + subscribe: no captions or cards there. The video must be ≥ 25 s. |

## 3. Explainer grammars (adapted from alchaincyf/huashu-art-motion, MIT)
Choose per segment from what the narration is doing. Use one grammar per segment; switch only at a segment boundary.
| Narration is… | Grammar | Signature moves | Ban |
|---|---|---|---|
| A mechanism becoming the next step (network, matrix, gradient); action verbs, formulas | **t1 3b1b** | Black ground holding only the thing being discussed. Transform the last concept into the next (no cut). Colour = concept. 1–3 s move + 1 s hold, smoothstep easing. | Glow, bloom, blue-gradient ground ("tech PPT"). |
| A product, feature, tutorial step or spec (noun + number) | **t2 keynote UI** | One thing per screen. Screenshot full frame, pushed into the part named. A noun or number lands as it is spoken. Spring bounce ≤ 0.15. | Glass card on a flat dark ground; using it for mechanisms or bad news. |
| Revenue, price, share, trend, before/after | **t3 finance chart** | Axes, then data grows, then annotate one thing. About 1 s per step; hold a number ≥ 0.5 s. One colour tells the story, the rest grey. | Truncated bar axis (bars start at 0; a line axis not at 0 says so on screen); bouncy, 3D or spinning charts. |
| Scale, "what's inside", a system; calm science voice | **y1 Kurzgesagt** | The abstract idea becomes one concrete glowing object. The camera travels between scales on a log zoom, redrawing the scene at each scale. Dark ground + 2–3 glow accents; shots 7–9 s. | Everything breathing at once; linear zoom; scaled-up bitmaps; outlines. |
| News, history, a quote, archive evidence | **y2 Vox collage** | Real material on a paper desk. The camera glides; highlighter and red line step at 12 fps. Hard cuts on sentence breaks. Black, paper white, one red. | Fake "archives" when no real source exists; torn-paper bounce-in templates. |
| A reasoning chain, the "why", a step-by-step argument | **y3 whiteboard** | Write as it is said, about 0.5 s behind the phrase. One big board; the camera moves about 0.23 of the frame width. Pull out to the full map at the end. Black + one accent. | Wiping to a blank board at each point; drawing everything before speaking. |
| A first-person story, a fail, a joke | **y4 storytime** | Pose swap in 0.1 s, then truly hold (about 70 % of frames are still). Reaction close-up in silence, ≥ 0.8 s. Jump in 2× or slam on the punchline. Background one step duller than the character. | Everything drifting; using it for data-heavy content. |
| A list, "3 reasons", a quote, a number open, a chapter card | **y5 kinetic type** | The key word slams in on the stress. Main word to sub line ≥ 3:1. One thing enters at a time. Text pins 0.35 s after landing. | More than 30–60 s of type in a row; more than 5 list items; text moving while it is being read. |

Picking rules:
- The face is the default grammar. Keep it for opinion and story; animate only where a picture explains better.
- Real screenshot: use t2 (tutorial, clean) or y2 (argument, evidence). Show it full frame, scaled uniformly, never cropping key UI.
- Only one number: no chart. Use a big count (t2 or y5) that lands as the number is spoken.
- 2–5 cues per 3–8 s segment. The first cue is a visual event, not a title. At most half the cues are text. On-screen
  text ≤ 6 words; the voice carries the rest. t1, t3, y3 and y5 put text on screen: move or drop burned captions there.

Cross-grammar rules:
- One focus per frame: one thing enters, the rest hold still. Background one step lower in saturation and contrast.
- Structure, then data, then annotation. Annotate one thing per shot. Colour = concept; ≤ 3–4 meaning colours.
- Land on the word. Count start = the time the number is spoken − count length. The reveal frame sits on the word, not
  at the start of the transition.
- In 0.3–0.4 s, out about 0.18 s. Hold ≥ 0.5 s after a number and ≥ 0.9 s after a punchline.
- Move the camera only when the eye must go somewhere new: 0.6–1.5 s eased glides. Use a fast push (0.28 s, +18–32 %)
  or a slam (0.17 s) only for a reveal, a twist or a key number. The same move on every shot reads as a slide deck.
  Put transitions at breaths and topic shifts, never mid-sentence.
- Real material goes full frame and unaltered. Data stays honest: units, source, bars from 0. Label made-up data
  "illustrative" on every shot. Check the wording against the picture: "8.7× as much" is not "up 8.7×".

## 4. Thumbnail and upload pack
- Thumbnail: 1280×720 JPG/PNG, ≤ 2 MB, built from a real film frame picked from a contact sheet. A face with clear
  emotion, ≤ 3 words that do not repeat the title, the look's accent. It must read at 168×94: check it at that size.
- Title: ≤ 60 characters visible (100 max). It promises what the hook pays off; no bait the video does not deliver.
- Description: the first 2 lines are the promise + the key link. Then chapters (0:00 first), then credits from
  CREDITS.md and the music licence.
- Pinned comment: one question that invites a reply, or a link to the next video.
- Captions: upload an SRT built from `words.json` (after the `fix` corrections) as CC.
- AI disclosure: tick "altered or synthetic content" when realistic AI people, places, events or cloned voices appear.
  It is not needed for 2D animation, captions, cuts or colour. Name the AI parts in the description. Never pass AI
  shots off as real footage.
- Write it all to `<work>/upload.md`: 3 title options, description, chapters, pinned comment, thumbnail path.

## 5. Shorts cut-downs
- Pick 2–3 moments, each 20–45 s, that stand alone: one claim + its payoff, a joke, or a result reveal. Start on the
  strongest line, never on a setup word.
- Write a new hook line, since the long-form setup is gone: a card ≤ 6 words, on screen from 0 to 2 s.
- Reframe to 9:16 on the face. From `track.json`, take the median `cx` of the boxes in the span. Then cw = H·9/16
  (round to even) and x = clamp(cx·W − cw/2, 0, W − cw):
  `ffmpeg -ss a -to b -i cut.mp4 -vf "crop=cw:H:x:0" short_N.mp4`
- Re-run `prep.py` on each crop to get 9:16 words and a 9:16 track. Then follow `modes/talking.md` §Plan and §Render
  (`compile.mjs`, word-pop captions on). Screen moments use a `screenshot` or `board` card.
- No end screen. Loop the end into the start if it is natural. On upload, link the long video as the related video.

## 6. Gates (never claim a pass without running them)
- `python -I $SKILL/scripts/film_gate.py <work>/final.mp4 --json <work>/gate.json`; exit 1 means fix and re-run.
  Run it on every Short too. HARD checks:
  - `dead_gap`: no visible change for more than 1.0 s.
  - `flicker`: two luma spikes less than 0.17 s apart.
  - `slideshow`: under 60 % of shots have in-shot motion.
- A held screen recording or chart that fails `dead_gap`: zoom to the part being named, or cut to the face. Do not
  argue with the gate.
- Retention self-check, from the timeline:
  - List the time of every new visual or new piece of info (cut, b-roll, card, zoom, chapter card, new on-screen
    fact) and sort them. **Any gap over 20 s is a flag**: fix it at the next concrete noun.
  - Also check: a visual change by 2 s; content by 30 s; a re-hook every ≤ 90 s; chapters valid; end-screen zone clear;
    numbers on screen match the voice.
- In the hand-off, list the flags left unfixed and the spots no one checked by ear.
