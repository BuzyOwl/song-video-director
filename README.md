# song-video-director

A Claude Code skill that directs, builds and reviews **code-rendered music videos** (lyric videos, animated story videos, procedural visualisers) from a song plus art assets. Distilled from three finished films: Basement Goldfish (p5.js), Toota Naksha (Remotion + WebGL) and Jod Ke Dekh (Remotion + three.js).

Watch the result: [Jod Ke Dekh](https://www.youtube.com/watch?v=19mDcggGr7I) · [Basement Goldfish](https://www.youtube.com/watch?v=vVhuyxakG-k)

## Install

```bash
git clone https://github.com/BuzyOwl/song-video-director.git
cp -r song-video-director/skill/song-video-director ~/.claude/skills/
```

Windows PowerShell:

```powershell
git clone https://github.com/BuzyOwl/song-video-director.git
Copy-Item -Recurse song-video-director\skill\song-video-director $HOME\.claude\skills\
```

Then in Claude Code say: *"Make a music video for this song"* or send timestamped feedback like *"1:26 looks odd"*. The skill triggers on its own.

## What is inside

| Path | What |
|---|---|
| `skill/song-video-director/SKILL.md` | workflow, hard rules, feedback loop |
| `skill/song-video-director/references/lessons.md` | real failures and fixes |
| `skill/song-video-director/references/tech-stack.md` | three stacks, pros and cons |
| `skill/song-video-director/scripts/song_facts.py` | BPM, beat grid, energy, Whisper word times |
| `docs/GLOSSARY.md` | technical words cheat sheet |
| `docs/TECHNIQUES.md` | sprites vs CGI vs layers vs Motion Canvas vs code, and how to combine them |
| `docs/video-techniques.xlsx` | same sheets as a spreadsheet |
| `docs/LINKS.md` | tools, docs, tutorials |

Needs for `song_facts.py`: Python 3, `numpy`, and optionally `faster-whisper` for lyric times.

## Need a simple lyric video?

Use [hookline.cc](https://hookline.cc). Use this skill when the video needs a story, a world and a director.

If it helped, please star the repo.

MIT licensed.
