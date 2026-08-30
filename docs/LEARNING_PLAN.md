# DSA Learning Plan — 12 weeks, ~11 h/week

**Goal:** recognise the right pattern within 90 seconds, and implement it cleanly
without looking anything up. Not "solve 300 problems".

**Target volume:** ~85 problems, each seen 3–5 times, spread out over time.
That beats 300 problems seen once — the research below is unanimous on this.

---

## 1. The principle everything else follows from

You are not learning problems. You are learning **triggers**: the feature of a
problem statement that tells you which tool to reach for.

> "sorted array + find a pair" → two pointers
> "longest/shortest contiguous ___" → sliding window
> "minimum number of steps in an unweighted graph" → BFS

There are roughly 15 of these. They cover the large majority of Easy/Medium
interview questions. Everything in this plan — the ordering, the spaced review,
the `Trigger` section in every solution file — exists to build that trigger list
in your head.

The single most common failure mode, per every guide I read: grinding hundreds
of problems with no pattern framework, then failing on a variant you haven't
seen. Volume without a framework doesn't transfer.

---

## 2. Weekly rhythm (~11 hours)

| When | Length | What |
|---|---|---|
| Session 1 (e.g. Mon) | 1.5 h | **Learn the pattern.** Read/watch the topic, then implement the data structure or template from scratch in a scratch file, no reference. |
| Sessions 2–5 (Tue–Fri) | 1.5 h each | **Solve.** 1–2 new problems using the session protocol below. Start each session with any due reviews. |
| Session 6 (weekend) | 1.5 h | **Review.** Clear the review queue, then go back over this week's solution files and sharpen the `Trigger` line in each one. |
| Session 7 (weekend) | 1 h | **Check the numbers.** `uv run track.py stats`: is the cold-solve rate moving, and what's at the bottom of the weakest-patterns list? From week 6: replace with a timed mock instead. |

Five days a week beats two long days. The spaced-repetition schedule assumes
you show up most days; if you disappear for a week the review queue piles up and
you'll be tempted to skip it. Don't — reviews come before new problems, always.

**If you fall behind:** cut new problems, never reviews. A week where you solved
2 new problems and cleared all reviews is a good week. A week where you solved 8
new problems and skipped reviews is wasted work.

---

## 3. The session protocol (per problem)

This is the part that matters most. Follow it literally.

1. **Read + restate (3 min).** Write the problem statement into the file
   docstring, trimmed. Say the input, output and constraints out loud. Constraints
   are a hint: `n ≤ 10^5` rules out O(n²); `n ≤ 20` suggests exponential/backtracking.
2. **Guess the pattern (90 s).** Before any thinking, write down which pattern
   you think it is and why. Wrong guesses are fine and *informative* — that's the
   skill you're training. Time yourself.
3. **Brute force first (5 min).** State the dumb solution and its complexity, in
   words, in the docstring. Interviewers want to hear this; it also gives you a
   correctness reference.
4. **Optimise on paper (10 min).** What is the brute force redundantly
   recomputing? Which structure removes that redundancy? Write the invariant.
5. **Only now, code (15 min).** Approach section written first, then the function.
6. **The 45-minute rule.** Total time box: 45 minutes for a Medium, 25 for an
   Easy. At the limit, stop. Take a **hint** only (the pattern name, not the
   solution) and give it 10 more minutes. Then read the solution.
   - Struggle is where the learning happens; frustration past ~45 min is not.
7. **After solving — the step people skip.** Close everything and **re-implement
   from a blank file**. Then fill in the `Trigger` section of the docstring:
   *what should have told me this was pattern X?* This one sentence is the actual
   artefact you're producing. The code is a by-product.
8. **Log it:** `uv run track.py log <n> solved -m 30 -n "missed the sort step"`.

Honest logging is what makes the stats useful. `hint` and `read` are not failures
— they're how the tracker knows what to bring back sooner.

---

## 4. How the tracker works

```bash
uv run track.py today          # what to do right now: due reviews, then new problems
uv run track.py new 1          # scaffold problems/1-two-sum.py from the template
uv run track.py log 1 solved -m 25 -n "hash map on complement"
uv run track.py due            # just the review queue
uv run track.py stats          # summary + weakest patterns
uv run track.py sync           # regenerate PROGRESS.md
```

**Spaced repetition.** Every logged attempt schedules the next one:

| Outcome | Effect | Comes back in |
|---|---|---|
| `solved` (unaided, in time box) | streak +1 | 1 → 3 → 7 → 16 → 35 → 90 days |
| `hint` (needed a nudge) | streak held | same interval again |
| `read` (read the solution) | streak reset | tomorrow |

After 5 clean solves a problem is **mastered** and stops coming back. The
intervals are the standard forgetting-curve ladder — the point is to review at
the moment you're about to forget, which is roughly 5 days after first learning
something.

**A review means re-solving from a blank file, not re-reading your solution.**
Re-reading feels productive and teaches you almost nothing. If you can't re-solve
it, that's a `read`, and it comes back tomorrow. That's the system working.

---

## 5. Metrics — what to actually watch

Problems solved is a vanity metric. Track these instead (all in `track.py stats`):

- **Cold-solve rate** — % of problems solved unaided on first sight. This is your
  real skill curve. Expect ~20% in week 2 and ~60% by week 10. It should climb
  even as the problems get harder; if it doesn't, you're going too fast.
- **Weakest patterns** — the tracker ranks patterns by first-attempt success.
  Whatever sits at the bottom in week 8 is what week 12 is for.
- **Pattern latency** — can you name the pattern in under 90 seconds? When you
  can't, say so in the log notes (`-n "took 6 min to see it was a window"`);
  interviewers effectively test this.
- **Day streak** — consistency is the input that drives everything else.
- **Review debt** — `due today` should be near zero most days.

### Phase exit criteria

Don't move to the next phase on the calendar alone — move when you can do this:

| After | You should be able to |
|---|---|
| **Phase 1** (wk 5) | Write a correct binary search and a sliding-window skeleton from memory, first try, no reference. State the complexity of anything you write. |
| **Phase 2** (wk 9) | Write BFS and DFS from memory in under 5 minutes. Solve a new Easy tree problem cold in under 15 minutes. |
| **Phase 3** (wk 12) | Take an unseen Medium, name the pattern in 90 s, and produce working code in 30 min while narrating. Cold-solve rate ≥ 50%. |

---

## 6. The 12 weeks

Full problem lists live in `curriculum.json` and render into `PROGRESS.md`.

### Phase 1 — Linear foundations (weeks 1–5)
Arrays, and the three ways to walk them efficiently. Nearly every hard problem
later reduces to one of these plus recursion.

| Wk | Topic | New | Key idea |
|---|---|---|---|
| 1 | Complexity + Arrays & Hashing | 6 | Trade space for time: remember what you've seen |
| 2 | Two Pointers | 7 | Sortedness makes a pointer move provably safe |
| 3 | Sliding Window | 6 | One expand/contract skeleton, reused everywhere |
| 4 | Stack & Queue | 7 | "Remember until the matching thing arrives"; monotonic stack |
| 5 | Binary Search | 7 | One template, forever. Then: search the *answer*, not the array |

### Phase 2 — Recursive & hierarchical (weeks 6–9)
Recursion as a contract: assume the recursive call is correct, then combine.
Once trees click, graphs are trees plus a `visited` set.

| Wk | Topic | New | Key idea |
|---|---|---|---|
| 6 | Linked List | 7 | Dummy head; fast/slow pointers |
| 7 | Trees & BST | 9 | DFS orders and what each is *for*; BFS when depth matters |
| 8 | Heaps & Backtracking | 8 | "Top k" → heap of size k; choose/explore/un-choose |
| 9 | Graphs | 8 | Grid as implicit graph; BFS = shortest path; topological sort |

### Phase 3 — Optimization (weeks 10–12)
The hardest category, deliberately last: DP is unlearnable until recursion is
automatic.

| Wk | Topic | New | Key idea |
|---|---|---|---|
| 10 | 1-D Dynamic Programming | 8 | Memo first, table second. Name the state in English |
| 11 | Greedy, Intervals & 2-D DP | 8 | What makes a local choice provably safe; sort by start vs end |
| 12 | Consolidation & mocks | 4 bonus | No new patterns. Clear the queue, two timed mocks, and list every pattern with its trigger from memory |

**Week 12 is not a buffer week — it's the most valuable week.** Protect it. If
you slip, drop problems from weeks 10–11, not from 12.

---

## 7. Resources

**Pick one primary, use the rest as backup.** Switching resources mid-stream is
a procrastination pattern.

- **[NeetCode roadmap / NeetCode 150](https://neetcode.io/roadmap)** — *your primary.*
  Problems grouped by pattern in dependency order, free video walkthrough for
  each. The curriculum here is deliberately a subset of it in the same order, so
  when you're stuck you can watch that problem's video. Best fit if you learn
  from someone reasoning out loud.
- **[Tech Interview Handbook](https://www.techinterviewhandbook.org/coding-interview-study-plan/) / [Grind 75](https://www.techinterviewhandbook.org/grind75)** —
  by the author of Blind 75. Generates a plan for your timeline; the 3-month /
  ~11 h-per-week track is the one this plan is calibrated against.
- **[Blind 75](https://www.techinterviewhandbook.org/best-practice-questions/)** —
  the original minimal high-signal list. Use as a final-week checklist, not as
  your curriculum (no ordering, no explanations).
- **[Striver's A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)** —
  450+ problems, 4–6 months, written explanations. Where to go *after* this plan
  if you want real depth rather than interview coverage.
- **Python specifics:** the [`collections`](https://docs.python.org/3/library/collections.html)
  and [`heapq`](https://docs.python.org/3/library/heapq.html) docs, plus the
  [time complexity table](https://wiki.python.org/moin/TimeComplexity) for every
  built-in operation. Knowing `deque`, `Counter`, `defaultdict` and `heapq` cold
  removes a lot of friction.

---

## 8. Where to read the theory

This is what Session 1 of each week is for. **Read one source per topic, not
four.** Reading about algorithms feels like progress and isn't — cap theory at
~1.5 h/week and spend the rest solving.

### Your three defaults

| Source | Use it for |
|---|---|
| **[AlgoMaster DSA course](https://algomaster.io/learn/dsa/course-roadmap)** | *Start here every week.* One page per topic at `/learn/dsa/<topic>-introduction`: the idea, when it applies, the template, the complexity. 15-20 min each. |
| **[AlgoMaster pattern list](https://algomaster.io/practice/dsa-patterns)** | Problems grouped by pattern. Use it for extra reps of the pattern you just learned, off-plan. |
| **[AlgoMaster animations](https://algomaster.io/animations/dsa)** | Watch the structure *move*. Non-negotiable for heaps, BSTs and graph traversal - the topics where a static explanation fails and an animation works. |

For framing rather than detail:
[20 DSA patterns](https://blog.algomaster.io/p/20-dsa-patterns) ·
[15 LeetCode patterns](https://blog.algomaster.io/p/15-leetcode-patterns)

### Per week

Verified links are direct. Where a row says *course roadmap*, the exact page
gets looked up and pinned when that week comes up - better an honest pointer
than a guessed URL.

| Wk | Topic | Read |
|---|---|---|
| 1 | Complexity, Arrays & Hashing | [arrays](https://algomaster.io/learn/dsa/arrays-introduction) · [Python time complexity](https://wiki.python.org/moin/TimeComplexity) |
| 2 | Two Pointers | [two pointers](https://algomaster.io/learn/dsa/two-pointers-introduction) |
| 3 | Sliding Window | [sliding window](https://algomaster.io/learn/dsa/sliding-window-introduction) |
| 4 | Stack & Queue | course roadmap - stacks & queues · [`deque` docs](https://docs.python.org/3/library/collections.html#collections.deque) |
| 5 | Binary Search | [binary search](https://algomaster.io/learn/dsa/binary-search-introduction) - pick one template and stop reading |
| 6 | Linked List | [fast & slow pointers](https://algomaster.io/learn/dsa/fast-slow-pointers-introduction) |
| 7 | Trees & BST | course roadmap - trees & BST · [Python Tutor](https://pythontutor.com/) to *watch* your recursion run |
| 8 | Heaps & Backtracking | course roadmap - heaps, backtracking · [`heapq` docs](https://docs.python.org/3/library/heapq.html) |
| 9 | Graphs | course roadmap - graphs, BFS & DFS |
| 10 | 1-D DP | course roadmap - dynamic programming · [freeCodeCamp DP course](https://www.youtube.com/watch?v=oBt53YbR9Kk) (Alvin Zablan, ~5 h) as the long-form backup |
| 11 | Greedy, Intervals, 2-D DP | course roadmap - greedy, intervals, DP |
| 12 | Consolidation | Nothing new. Re-read only your own notes and `Trigger` lines |

### When you want the real thing

Not required for this plan — for when you want to know *why* something works
rather than how to use it:

- **[MIT 6.006 Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/)** —
  full lecture videos, notes and problem sets, free. The proper CS treatment.
- **[William Fiset's data structures course](https://www.youtube.com/watch?v=RBSGKlAvoiM)** —
  8 hours, implementation-level, genuinely excellent on heaps and graphs.
- **[USACO Guide](https://usaco.guide/)** — free, rigorous, competitive-programming
  angle. Its DP and graph sections are better than most paid courses.
- **[CP-Algorithms](https://cp-algorithms.com/)** — reference for algorithms
  beyond interview scope. Bookmark, don't read cover to cover.
- ***Grokking Algorithms*** (Bhargava) — illustrated, ~250 pages, the friendliest
  book if you want one on paper. ***The Algorithm Design Manual*** (Skiena) as the
  reference you keep for years.

### How to read theory so it sticks

Reading a pattern explanation and nodding is worth almost nothing. After each
theory session, **close the tab and implement the structure or template from
scratch in a scratch file** — heap, BST insert, BFS, the binary search template.
If you can't, you didn't learn it; reread the one part you got stuck on, not the
whole page.

---

## 9. Things that will go wrong (and the fix)

| Symptom | Fix |
|---|---|
| "I understood the solution but couldn't reproduce it" | You re-read instead of re-solving. Reviews must start from a blank file. |
| "I solve it, then forget it a week later" | Normal — that's the forgetting curve. Trust the review queue; don't skip it. |
| Tempted to look at the solution at minute 10 | Set a literal timer. The struggle *is* the mechanism. |
| Stuck on Hards, feeling behind | Ignore Hards entirely for 12 weeks. Easy/Medium fluency is what gets offers. |
| Copying a solution to "keep the streak" | A `read` logged honestly is worth more than a dishonest `solved`. The tracker is for you. |
| Solved it but can't explain it | Feynman test: explain it to someone who doesn't code. If you fall back on jargon, you don't have it yet. |

---

## 10. What to do right now

```bash
uv run track.py today      # → Week 1, Arrays & Hashing
uv run track.py new 1      # → problems/1-two-sum.py
```

Then open the file, fill in the statement, and write the Approach section
*before* you write a line of code. Ask me for a hint whenever you hit the
45-minute wall — hints only, unless you ask for the full solution.

---

*Sources consulted:*
[Tech Interview Handbook study plan](https://www.techinterviewhandbook.org/coding-interview-study-plan/) ·
[NeetCode](https://neetcode.io/roadmap) ·
[Blind 75 vs NeetCode 150 vs Striver](https://interviewpilot.dev/blog/neetcode-150-vs-striver-sde-vs-blind-75) ·
[Best DSA sheet for beginners](https://spacecomplexity.ai/blog/best-dsa-sheet-for-beginners) ·
[DSA interview prep patterns & strategy](https://www.calibreos.com/blog/dsa-interview-prep-guide-2026) ·
[Spaced repetition for LeetCode retention](https://medium.com/@therubeprotocol/stop-forgetting-your-leetcode-solutions-a-retention-system-that-works-26acc13e83e0) ·
[Step-by-step guidance to master DSA](https://www.enjoyalgorithms.com/blog/step-by-step-guidance-to-master-data-structure-and-algorithms-for-coding-interview/)
