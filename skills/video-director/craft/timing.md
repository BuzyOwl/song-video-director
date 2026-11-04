# Craft: timing (stems, word onsets, beat grid, keying to the music)

Load at the start of any music video (build the audio map before keying anything), whenever something keys to a word
or hit, and whenever a draft looks early or late. Talking mode uses section 2 for caption onsets.
Adapted from Imaginative-Prompting/claude-video-skills `song-timing` (MIT); `scripts/song_facts.py` gives candidates.

## 1. Stems from the music tool itself
- **Suno songs: use Suno's own stems** (song menu → Edit → Get Stems / MIDI → Auto split, WAV + MIDI; as of Oct 2026).
  ~10 stems plus one MIDI per stem. **It spends credits on the user's account: ask first.**
- No tool stems? Fall back to a splitter (audio-separator, Mel-Band RoFormer). A general splitter buried a piano in
  "other" on one film; label the map "separated stems".
- Check: summed stems vs master cross-correlate at lag 0. Check each instrument really sits in its stem.
- To edit the mix, add a stem's phrase on top of the master, level-matched; rebuilding from summed stems sounds different.

## 2. Every word's onset, measured on the vocal audio
**Onset = first audible energy of the word's first sound:** a fricative's noise rise, a stop's release burst, the first
change into a vowel. Never the breath before a phrase, the previous word's tail, or a pitch ornament.
Nothing keyed to a word is readable before its onset.

Use these for *which* words, never *when*:
- lyric-sheet times; automatic aligners (within 2 frames only ~half the time; held notes dragged words 1–1.7 s);
- **speech-transcription (Whisper) word times: measured 0.5–0.8 s early on sung vocals;**
- stem MIDI alone (Suno vocal MIDI ran ~6.5 frames ahead of its own audio; no blanket offset fixes it).

Traps: a held note's tail labelled as the next word · melisma notes aren't words · same-pitch syllables merged into one
MIDI note · sung s/f hiss 5–8 frames before the vowel (pick a rule, be consistent) · a doubled backing phrase before the
lead · repeated lines aren't copies (measure each, then cross-check choruses).

Method:
1. Candidate time per syllable from MIDI or the aligner (`song_facts.py --whisper`).
2. Snap it to its acoustic event on the vocal stem with a spectrogram crop.
3. Do it twice independently; agree within ~25 ms → mean, else re-measure.
4. One words file: onset, end, confidence tag (M / A2 / A1 / E), reason. Every scene keys to it.
5. A perceptual call → render a short A/B clip with the waveform; don't argue it in words.
6. Re-timing a word moves it in the shot: re-check the camera at the new time.

## 3. Beats and hits from the drum stem's audio
- Tempo can drift (one song went 123.5 → 127.7 BPM and back): keep a list of beat times, not one period.
- Fit the grid to drum-stem audio onsets, not drum MIDI. Mean distance to onsets < ~0.1 beat (half a beat off lands
  every snap on the "and").
- Hits by spectral flux, classified by band: kick 30–110 Hz rise · snare/clap 1.2–5 kHz noise with 25–110 ms tail ·
  hats 7–16 kHz burst · crash 5–16 kHz held 150–500 ms. Thresholds from this song's levels; strength 0–1; check bar by
  bar as a 16-step pattern.
- Map events too: drum stops and re-entries, fills, risers, drops, silences, prominent instrument notes.

## 4. Drive camera and animation from the map
- Moves start and land on beats; not every hit needs a move.
- **Kick shake:** a small push toward the subject plus a quick roll-nudge dying in ~0.2 s, over a slow sway. Softer on a
  framing that must be read.
```ts
function kickJolt(t, kicks) {                       // kicks: sorted seconds
  const last = kicks.findLast(k => k <= t);
  if (last === undefined || t - last > 0.5) return 0;
  const s = t - last;
  return Math.exp(-11 * s) * Math.sin(52 * s);       // two wiggles, gone in ~0.2 s
}  // offset camera by a few thousandths of subject distance on right/up, roll a few mrad, × kickJolt
```
- Accent lands on the beat: anticipation before, impact at, follow-through after. Prominent notes get an accent too.
- Pace follows the song: slow song, slow eased moves.

## Verify
- Word-timing clip: the section with each onset marked on the vocal waveform. Step frames at each onset: the entrance
  starts on that frame and nothing reads before.
- Grid vs drum stem: mean distance < ~0.1 beat.
- `ffprobe`: `start_time` 0 on both streams; frame 0 is song time 0 (or the excerpt's own start).
