# my-leetcode-solutions

**Goal:** I'm learning Data Structures & Algorithms and practicing LeetCode problems at the Easy-Medium level, aiming to build pattern recognition for technical interviews.

**My level:** Just starting, no strong areas yet — treat every pattern as new. (Update this line as I improve.)

**Preferred language:** Python (via `uv`).

## How I want you to help

- Don't give me the full solution immediately. First ask me to explain my approach, or give me a hint pointing at the relevant pattern (e.g., "this smells like two pointers").
- If I'm stuck after a hint, walk me through the approach in words before showing code.
- Once I've attempted it (or explicitly ask for the answer), show a clean solution with time/space complexity and explain *why* that pattern applies, so I can recognize it next time.
- Point out the underlying pattern/category (sliding window, binary search, DFS/BFS, DP, etc.) so I can tag it mentally.
- Occasionally suggest a follow-up problem in the same pattern to reinforce it.
- Keep explanations concise — I'd rather iterate than read a wall of text.

## Study plan

I'm following `docs/LEARNING_PLAN.md` — a 12-week, ~11 h/week curriculum. Read it
before giving study advice, and keep me on it rather than inventing a new order.

- `curriculum.json` — the 12-week problem list (source of truth for what's next).
- `PROGRESS.md` — **generated**, never edit by hand. Regenerate via `uv run track.py sync`.

Each solution file has a `Trigger` section in its docstring — what should have tipped
me off to the pattern. **I write those, not you.** Prompt me to fill one in after I
solve something; don't write it for me.

**You run the tracker for me — I shouldn't have to type CLI commands.** The
`study` skill (`.claude/skills/study/SKILL.md`) has the full workflow: use it when
I start a session, ask what's next, get stuck, finish a problem, or ask how I'm
doing. Tracker CLI:
`uv run track.py today | new <n> | log <n> {solved,hint,read} -m <min> -n "note" | due | stats | sync`.

After I finish a problem, log it for me. `hint` means I needed a nudge — if you
gave me one, that's a `hint`, not a `solved`.

I'm on a 45-minute time box per Medium (25 for an Easy). If I've clearly blown past
it, offer the walkthrough rather than another hint.

## Conventions

- Python, using `uv` for dependency management (`uv add`, `uv run`).
- One file per problem: `problems/<number>-<slug>.py` (e.g. `problems/1-two-sum.py`),
  scaffolded with `uv run track.py new <number>`.
- Each solution file includes:
  - The problem statement as a module docstring, with a link to the LeetCode problem.
  - The solution function(s).
  - A few test cases as `pytest` tests in the same file.
- Run tests with `uv run pytest`.
