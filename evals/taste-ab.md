# Taste A/B: does a skill change make the films better?

Trigger and routing evals (`evals.json`) check that the skill *does the right steps*. This check asks the harder question: did a change make the **output look better**? Run it before every release that touches `SKILL.md`, a mode, an engine, `feel.md` or `style-protocol.md`.

## The 4 fixed briefs (never edit these; comparability is the point)
1. **Ballad, despair → acceptance.** 63 BPM Hindi ballad, a 40 s verse into the first chorus. Pure code, look `cinematic-plate`.
2. **Rap, defiant.** 100 BPM, a 30 s hook. Lyrics inside the world, look `clay-world`.
3. **Lo-fi, warm loop.** 72 BPM, a 12 s seamless loop, 9:16. Pick the look yourself.
4. **Talking reel.** A 35 s English clip about one idea with two numbers in it. Talking mode, default cards.

The source songs and clips live in a private folder outside the repo (`VD_EVAL_MEDIA`). Each brief names its files there.

## Procedure
1. Check out the **old** skill version (A) and the **new** one (B).
2. For each brief and each version, run a fresh session with the same prompt: the plan, the 3 stills, the gate report. That's 8 runs. Stills and plans are enough; full renders aren't needed, which keeps this cheap.
3. Put each pair side by side **with labels hidden and order randomised**: left/right decided by coin flip, recorded in `ab-key.txt`.
4. A fresh judge subagent scores each side on the `style-protocol.md` rubric, then picks a winner per brief. It has seen neither the code nor the conversation; it gets only the brief, the stills, the gate reports and the rubric.
5. A human looks at the same pairs and picks a winner per brief. Taste is the human's call.
6. **Ship B only if it wins or ties at least 3 of 4 briefs with the human, and loses none on a veto.** Record the result in `CHANGELOG.md`: the date, the wins, the judge's scores and the human's picks.

## Why it is built this way
- **Blind and randomised:** a judge who knows which side is "new" favours it.
- **Fixed briefs:** a rule that helps one genre often quietly hurts another. The four briefs cover slow/fast, code/3D, loop and talking.
- **The human decides taste.** Self-scores ran about 10 points higher than independent review in huashu-art-motion's measurements, so the AI's numbers rank the options and the human picks.
