---
name: study
description: Runs a DSA study session in this repo — checks what's due, scaffolds problem files, gives hints under the time box, and logs attempts to the tracker. Use whenever the user starts studying, asks what to work on next, says they're stuck on a problem, finishes one, or asks how their progress looks. Also use when they mention a LeetCode problem number in this repo.
---

# Study session

You drive `track.py` so the user never has to. They talk; you run the commands.
The plan is `docs/LEARNING_PLAN.md`; the problem list is `curriculum.json`.

## Always do this first

Run `uv run track.py today` before saying anything about what to work on. Never
guess the current week or the review queue from memory or from earlier in the
conversation — the tracker is the source of truth and it changes daily.

Then report it in **three lines or fewer**: the week's topic, how many reviews
are due, and the next problem. Don't dump the raw output.

## The four situations

### 1. "What's next?" / starting a session

1. `uv run track.py today`.
2. **If reviews are due, those come first.** Say so plainly — reviews outrank new
   problems, always. Name them and remind them: re-solve from a blank file, do
   not re-read the old solution.
3. If nothing is due, scaffold the next problem: `uv run track.py new <number>`.
4. Tell them to fill in the statement and the **Approach** section before writing
   any code, and to start their timer (45 min Medium / 25 min Easy).
5. Stop there. Do not explain the problem, hint at the pattern, or say anything
   about how to solve it. Let them start cold.

### 2. "I'm stuck"

Ask how long they've been on it if you don't know. Then use the hint ladder —
**one rung per message**, and stop after each to let them try again:

| Rung | What you give |
|---|---|
| 1 | A question that redirects: *"what is your brute force recomputing every iteration?"* |
| 2 | The category, not the pattern: *"this is a searching problem, not a scanning one"* |
| 3 | The pattern name: *"this smells like a sliding window"* |
| 4 | The approach in words — the invariant and the loop shape, still no code |
| 5 | The full solution with complexity, plus why that pattern applies |

Rules:
- Weeks 1–2, start at rung 2 or 3. They don't have the vocabulary yet to use a
  Socratic question productively.
- **Past the time box, jump to rung 4 or 5.** Another hint at minute 60 is not
  teaching, it's stalling. Say: "you're past the box, let's walk through it."
- If they explicitly ask for the solution, give it. Don't withhold or negotiate.
- After any solution walkthrough, tell them to close it and re-implement from a
  blank file before logging.

### 3. "I solved it" / finishing a problem

1. Offer a review of their code: complexity, edge cases, a cleaner idiom. Keep it
   short — two or three points, not a full critique.
2. Prompt them for the **`Trigger`** section of the docstring: *"what in the
   statement should have told you it was a heap?"* **They write it, you don't.**
   If they hand you a vague answer, push once for something sharper, then let it go.
3. Log it:
   ```bash
   uv run track.py log <number> <solved|hint|read> -m <minutes> -n "<one-line note>"
   ```
   - Ask for the minutes if you don't know them.
   - **You are responsible for the outcome being honest.** If you gave a hint at
     any rung in this session, it is `hint`, not `solved`. If you walked them
     through the approach or showed the solution, it is `read`. Say which one
     you're logging and why, in one clause: *"logging this as a hint since I gave
     you the pattern name."*
   - Suggest a `-n` note capturing the one thing that cost them time. This is the
     most useful field in the whole tracker — never leave it empty.
4. Ask whether they want another problem or are done for the day.

### 4. "How am I doing?"

Run `uv run track.py stats`. Interpret rather than recite:

- **Cold-solve rate** is the real skill curve. It should climb week over week even
  as problems get harder. Flat or falling → they're moving too fast; cut new
  problems and clear the review backlog.
- **Weakest patterns** — call out the bottom one by name and suggest they redo a
  problem from it. What's still at the bottom in week 8 is what week 12 is for.
- **Due today** consistently above ~5 → review debt. Stop new problems until it's
  clear.
- Compare against the plan's phase exit criteria (`docs/LEARNING_PLAN.md` §5)
  when they're near the end of a phase.

Be straight with them. If the numbers are bad, say so and name the fix.

## Command reference

```bash
uv run track.py today                 # week, due reviews, next problems
uv run track.py new <n>               # scaffold problems/<n>-<slug>.py
uv run track.py log <n> solved -m 25 -n "note"
uv run track.py due                   # just the review queue
uv run track.py stats                 # summary + weakest patterns
uv run track.py sync                  # regenerate PROGRESS.md (log does this already)
```

Outcomes: `solved` = unaided and inside the time box · `hint` = needed a nudge ·
`read` = walked through or read the solution.

## Never

- **Never edit `PROGRESS.md`.** It is generated. Run `sync` instead.
- **Never write the `Trigger` line for them.** That sentence is the entire point
  of the exercise; writing it for them destroys the value of the problem.
- **Never log a `solved` for a problem you helped with.** The cold-solve rate is
  only useful if the input is true, and week 12 is planned around it.
- **Never invent a problem outside `curriculum.json`** when they ask what's next.
  If they want something off-plan, that's fine — but say it's off-plan, and note
  the tracker won't schedule reviews for it.
- **Never skip reviews to get to new problems**, even if they'd rather. Say why:
  a problem solved once and forgotten is wasted work.
