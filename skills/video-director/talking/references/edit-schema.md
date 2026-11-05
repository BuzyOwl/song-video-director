# edit.json schema (read this before writing `<work>/edit.json`)

`node scripts/compile.mjs <work>/edit.json [--preview] [--range a:b] [--no-render]`
writes `<work>/props.json` and renders `<work>/final.mp4` (`--preview` = half-size `preview.mp4`; `--range a:b` = seconds, implies preview).
Read `<work>/cut.txt` first: every word ref must exist in that transcript.

```json
{"out": "final.mp4", "size": [1080, 1920], "tail": 1.2, "punch": 1.12, "zoom": "auto", "sfx": true,
 "captions": {"font": "Montserrat-ExtraBold", "words": 3, "y": 0.84, "size": 78, "accent": "#FFD23F", "keys": ["fire", "idea"]},
 "cards": [
  {"type": "title", "at": "test", "until": "one.e+0.3", "text": "TEST 01", "y": 0.1, "size": 120},
  {"type": "stat", "at": "100", "until": "up.e+0.2", "tokens": [["100","100"],["−","minus"],["25","25"],["=","equals"],["75","75"]], "y": 0.12},
  {"type": "list", "at": "three", "until": "end", "items": [["Fast","fast"],["Cheap","cheap"],["Good","good"]]},
  {"type": "cutout", "at": "fire", "until": "smoke.e", "src": "assets/strip.png", "motion": "drift", "frame": "torn"},
  {"type": "screenshot", "at": "site", "until": "that.e", "src": "assets/site.png", "pan": "down"},
  {"type": "quote", "at": "said", "until": "said.e+2", "text": "…", "by": "…"},
  {"type": "arrow", "at": "this", "until": "this.e+1", "target": "face", "shape": "circle"},
  {"type": "lowerthird", "at": "start", "until": "start+3", "text": "Dr. R", "sub": "MIC Class"},
  {"type": "pip", "at": "see", "until": "see.e+2", "src": "assets/x.png", "corner": "tr"}]}
```

## Top level
- `size` output px (default 1080x1920). `tail` seconds of held last frame after the speech (1.2). `punch` zoom on alternate long shots (1.12).
- `zoom`: `"auto"` punches in on the gesture/emphasis events from `words.json`; `"off"` disables.
- `sfx`: `false` mutes the synthesized effects (the clip's own audio is always kept).
- `fix`: `{"misheard": "right"}` rewrites transcript words (trailing punctuation kept) before refs and captions, e.g. `{"coruscant": "carousel", "-shot": "shot"}`; refs then use the new word.
- `captions`: `null` = none. `words` per chunk (3), `y` baseline (0.84, pushed below the chin automatically, max 0.9), `size` px at 1080 wide (78, never rendered below 70), `accent` the one accent colour, `keys` words drawn in the accent (numbers always are).

## Cards (all optional; `until` defaults to `at` + 2 s)
- `title` big text, `size` optional. `lowerthird` name + `sub`. `quote` `text` + `by`.
- `stat` `tokens` = `[text, wordRef]` pairs; each pops in at its word. Use for numbers/equations.
- `list` `items` = `[text, wordRef]` pairs; each ticks in at its word.
- `cutout` `src` image; `motion` drift|drop|none; `frame` torn|strip|news. `screenshot` `src`, `pan` down|up|none. `pip` `src`, `corner` tl|tr|bl|br.
- `board` full-screen slide; while it is up the speaker shrinks into a face-centred PiP bubble (top-right) and grows back after. Fields: `n` (big accent number, e.g. "01"), `kicker`, `title`, `sub`, `prompt` (`[text, ref]` pairs typed into a chat box; an entry that extends the previous one continues typing), `rows` (`[label, text, ref]`), `label` + `chips` (`[text, ref]` pops on the word; bare strings cascade in from the board start). Boards < 0.6 s apart keep the bubble (chain them `until` = next `at`). Takes no lane; captions keep `y` over a board. Keep other cards off board spans.
  HyperFrames board instead of the built-in layout: `html` (HF project dir, relative to the work dir) + `sync` (`{"#elementId": wordRef}`); the other fields are ignored. See `boards.md`.
- `arrow` `shape` arrow|circle|underline; `target: "face"` (circle/underline around the face box) or explicit `from`/`to` as normalised `[x, y]`.
- `src` paths are relative to the work dir (`assets/...`); they are copied for the render.
- `y` (normalised 0-1, optional): default lanes title 0.10, stat 0.12, lowerthird 0.20, quote/list/cutout/screenshot 0.24, arrow 0.30. Each card is modelled as centre `y` ± h/2 with h (frame fraction): title 0.09, stat 0.11, lowerthird 0.11, quote 0.16, list 0.06+0.05×items (max 0.3), cutout 0.30, screenshot 0.42; `arrow` and `pip` are exempt from lanes. A card must sit ≥0.02 above the face band or below it (above the caption zone, bottom ≤0.78): author `y` if it clears, else moved above the face (top ≥0.04), else below; if nothing fits compile prints `FACE OVERLAP <id>`. Simultaneous cards are placed directly below/above each other (0.02 gap) and must also clear the face; if no clear lane exists compile prints `CARD OVERLAP <id> <type> with <id>`. To control placement yourself, give them different `y`.

## Word refs (`at`, `until`, token/item refs, same grammar as `render.py`)
`"fire"` first occurrence start | `"fire#2"` second occurrence | `"fire.e"` end of the word | `"fire+0.3"` / `"fire.e-0.2"` offset seconds | `"start"` 0 | `"end"` end of speech | `"end-1"` | a plain number = seconds. Matching ignores case and punctuation. A ref not in the transcript is an error.
