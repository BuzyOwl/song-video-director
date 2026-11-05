# Craft: team and review (several sessions on one video, overnight runs, the review page)

Load when a piece is split across several sessions or subagents, for an unattended overnight run, or to set up the
review page. Adapted from Imaginative-Prompting/claude-video-skills `directing-sessions` + `review-page` (MIT).
(`engines/code.md` "Parallel agents" covers file ownership and stubs; this file covers direction and review.)

## The director session
Makes nothing in the workers' files. Briefs and reviews every worker against the creator's notes, owns the GPU queue
order and the schedule, writes for the creator. **The creator's notes always outrank the director's.**

### Day zero
1. **Director's log**, in order: header (who, from when) · **FOR THE CREATOR** (to watch / to decide / done; rewritten
   each morning and handoff) · **STATE** (read first on resume) · the creator's words verbatim with times · **the bar**
   (approved parts as a checklist) · GPU protocol + plan table (each worker's own promised times) · advice log.
2. **One brief per worker:** scope, the creator's words that concern it (verbatim, oldest first), routing facts (files,
   frame ranges, queue command). No paraphrase, no step list of your own.
3. **A recurring tick:** `/loop` or a scheduled task, every 30 min by day, 15 overnight (prompt below).
4. **Checked saves for shared code:** typecheck, import every module, build the real bundle, revert all if any step
   fails. Never land a multi-file change file by file (half-saved changes broke every render five times in two days).

## Relaying the creator's notes (the rule that matters most)
- A relay = their **exact words** + routing facts. No summary, no "this means", no numbers they didn't give.
- Unclear or conflicting notes: ask them in one line instead of choosing.
- Review against their sentences, never your derived spec (paraphrased step lists were what got built and passed, and the
  same shots kept coming back wrong; sending their words alongside the list didn't help, the list won).
- "My only issue is X" + another sentence: the second sentence is the fix for X. "At least X" is a floor. "Have one be X"
  adds or swaps; it never deletes what they didn't name.

## Note checklist (per section)
Their note verbatim → the frame that shows it met → the render it was checked on. A shot isn't approved until every row
is met on a named frame. Any change to camera, staging, set or timing unchecks every row.

## Running workers
At most three working besides the director, as a queue. Fresh worker per new task, briefed with the creator's words;
finished workers write their state and stand down. One consolidated message per worker per tick (their notes verbatim,
then, marked as the director's, only verified technical findings with frames: a flicker at f1520, a word 3 frames late).
No message when nothing is new. Ask for times, not effort; on a 30+ min slip ask for a new true time and scope order,
never a quality cut. Only the creator's notes are to-dos; flaws found on approved work go to the director as a list.
Sessions talk via the app's session messaging, or an inbox file each reads at the start of every turn plus a STATE file.

### Tick prompt (fill the <…>, rewrite at every phase change)
```
DIRECTOR TICK (video: <name>; phase: <phase + the creator's latest plan in their words>).
Read the log first (FOR THE CREATOR, STATE, plan table, bar, latest entry). Run `date` before writing any time.
1 USAGE: read the real meter, never an estimate. Unattended only: at 95% pause (each worker queues renders, writes state).
2 GPU: queue status; anything rendering outside it gets one message. Order: unblock deps, then what the creator waits on.
3 KEEP WORKING: ≤3 workers, none idle with work left.
4 SCHEDULE: each worker vs its own promised times; 30+ min slip → new true time + scope order; risks → FOR THE CREATOR.
5 REVIEW each new render vs the previous draft the creator saw; re-read their notes; watch at speed; step fast moves;
  words on time; camera decisive; no flicker / blank / clipping; note checklist row by row.
6 ADVICE: one message per worker with new work: their notes verbatim + routing; below, marked mine, verified findings only.
7 LOG the tick. 8 SANITY: disk, temp files, keep-awake, stale browsers (report, never kill).
```

### Overnight
15-min tick. Never wait on the creator: anything pending their answer gets a noted default and work moves to improving
what's agreed. Review and splice each render as it lands. Handoff before they wake. Keep the machine awake.
Before a master, sweep the whole film on today's code against the cut.

## The review page (every draft goes here, never a bare file path)
- **One entry per pass**, newest first: title, time added, **known issues at the top** (plain words, frame numbers),
  what changed and what to look at, media, link to the previous pass. Never revise an old entry in place.
- Render → blank scan → post at once with known issues → then fix. Review adds notes; it never holds a draft back.
- Marks: "waiting review" (director checked it) → "reviewed" (their one-line note + time). Reviewed ≠ approved.
- Clips carry their own audio; a clip against the full song gives its start offset in seconds, not frames.
- **New file name for every version** (players cache by URL; never overwrite a delivered file).
- Looping previews: 10-bit AVIF, not lossy WebP (it blocked dark gradients):
  `ffmpeg -i in.mp4 -c:v libsvtav1 -crf 23 -preset 6 -pix_fmt yuv420p10le -f avif out.avif`.
- Read the stored entry back after writing. Third-party reference footage stays off the page.
- Minimal page: a folder of one JSON per entry + a static page listing them newest first. A private Artifact page works
  too (it can be shared with collaborators).
```json
{"id": "chorus-1-draft-4", "title": "Chorus 1, draft 4", "createdAt": "2026-10-12T14:05:00+04:00",
 "subject": "chorus-1", "knownIssues": ["f1520–1524: sign letters flicker (coplanar faces); fix in draft 5"],
 "body": "What changed since draft 3, what to look at.",
 "media": [{"type": "video", "src": "renders/chorus-1-d4.mp4"}], "previous": "chorus-1-draft-3",
 "review": {"state": "waiting"}}
```

## Safety
Never kill a process you didn't start. Never delete without the creator's OK on the exact list. `date` before any time.
