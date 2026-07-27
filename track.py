#!/usr/bin/env python3
"""Study tracker for the 12-week DSA plan (see docs/LEARNING_PLAN.md).

The curriculum lives in curriculum.json (static). Your state lives in
progress.json (append-only history of attempts). PROGRESS.md is generated
from both and should never be edited by hand.

Usage:
    uv run track.py today                     # what to do right now
    uv run track.py new 1                     # scaffold problems/1-two-sum.py
    uv run track.py log 1 solved -m 25        # record an attempt
    uv run track.py log 1 hint -m 40 -n "forgot to sort first"
    uv run track.py due                       # reviews due today
    uv run track.py stats                     # summary
    uv run track.py sync                      # regenerate PROGRESS.md

Outcomes:
    solved  - got it unaided, within the time box
    hint    - needed a nudge (a hint, a pattern name, a peek at a comment)
    read    - could not solve it; read the solution
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent
CURRICULUM_FILE = ROOT / "curriculum.json"
PROGRESS_FILE = ROOT / "progress.json"
PROGRESS_MD = ROOT / "PROGRESS.md"
PROBLEMS_DIR = ROOT / "problems"

# Spaced-repetition ladder. Index = number of consecutive clean solves.
INTERVALS = [1, 3, 7, 16, 35, 90]
MASTERED_AT = 5  # clean solves needed before a problem stops coming back
OUTCOMES = ("solved", "hint", "read")

TEMPLATE = '''"""{number}. {title}  [{difficulty}]

https://leetcode.com/problems/{slug}/

Pattern: {pattern}

--- Problem statement ---
TODO: paste the statement here (trim the fluff, keep the constraints).

--- Approach ---
TODO: write this BEFORE you write any code.
  1. What is the brute force, and what does it cost?
  2. What does the optimal approach do differently, in one sentence?
  3. What is the invariant that makes it correct?

Complexity: time O(?), space O(?)

--- Trigger ---
TODO (fill in AFTER solving): what in the problem statement should have
made you think "{pattern}" within 90 seconds?
"""

import pytest

# Delete this line once you start implementing, to switch the tests on.
pytestmark = pytest.mark.skip(reason="not implemented yet")


def {func}():
    """TODO: fix the signature and implement."""
    raise NotImplementedError


def test_example_1():
    assert {func}() is None


def test_edge_case():
    """The empty / single-element / all-equal case. Pick the one that bites."""
    assert {func}() is None
'''


# --------------------------------------------------------------------------
# storage
# --------------------------------------------------------------------------
def load_curriculum() -> dict:
    return json.loads(CURRICULUM_FILE.read_text())


def load_progress() -> dict:
    if not PROGRESS_FILE.exists():
        return {"started": date.today().isoformat(), "problems": {}}
    return json.loads(PROGRESS_FILE.read_text())


def save_progress(state: dict) -> None:
    PROGRESS_FILE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def index_problems(curriculum: dict) -> dict[str, dict]:
    """number -> problem metadata, with its week folded in."""
    out = {}
    for week in curriculum["weeks"]:
        for problem in week["problems"]:
            out[str(problem["number"])] = {**problem, "week": week["week"], "topic": week["topic"]}
    return out


def record_for(state: dict, number: int | str) -> dict:
    return state["problems"].setdefault(
        str(number), {"attempts": [], "streak": 0, "next_review": None}
    )


def status_of(record: dict) -> str:
    if not record["attempts"]:
        return "todo"
    if record["streak"] >= MASTERED_AT:
        return "mastered"
    return "learning"


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------
def cmd_new(args) -> None:
    meta = index_problems(load_curriculum()).get(str(args.number))
    if meta is None:
        raise SystemExit(f"Problem {args.number} is not in curriculum.json.")

    PROBLEMS_DIR.mkdir(exist_ok=True)
    path = PROBLEMS_DIR / f"{meta['number']}-{meta['slug']}.py"
    if path.exists():
        print(f"Already exists: {path.relative_to(ROOT)}")
        return

    path.write_text(
        TEMPLATE.format(
            number=meta["number"],
            title=meta["title"],
            difficulty=meta["difficulty"],
            slug=meta["slug"],
            pattern=meta["pattern"],
            func=meta["slug"].replace("-", "_"),
        )
    )
    print(f"Created {path.relative_to(ROOT)}")
    print("Write the Approach section before you write any code.")


def cmd_log(args) -> None:
    problems = index_problems(load_curriculum())
    if str(args.number) not in problems:
        raise SystemExit(f"Problem {args.number} is not in curriculum.json.")

    state = load_progress()
    record = record_for(state, args.number)

    if args.outcome == "solved":
        record["streak"] += 1
    elif args.outcome == "hint":
        pass  # stays put: you get another look at it on the same cadence
    else:
        record["streak"] = 0

    gap = INTERVALS[min(max(record["streak"] - 1, 0), len(INTERVALS) - 1)]
    today = date.today()
    record["next_review"] = (today + timedelta(days=gap)).isoformat()
    record["attempts"].append(
        {
            "date": today.isoformat(),
            "outcome": args.outcome,
            "minutes": args.minutes,
            "notes": args.notes or "",
        }
    )

    save_progress(state)
    write_progress_md(state)

    meta = problems[str(args.number)]
    print(f"Logged {args.outcome} on {meta['number']}. {meta['title']} ({args.minutes} min).")
    if status_of(record) == "mastered":
        print("That one is mastered - it will not come back.")
    else:
        print(f"Next review: {record['next_review']} (streak {record['streak']}).")


def due_list(state: dict, problems: dict) -> list[tuple[dict, dict]]:
    today = date.today().isoformat()
    out = []
    for number, record in state["problems"].items():
        if status_of(record) == "mastered" or not record["next_review"]:
            continue
        if record["next_review"] <= today and number in problems:
            out.append((problems[number], record))
    return sorted(out, key=lambda pair: pair[1]["next_review"])


def cmd_due(args) -> None:
    problems = index_problems(load_curriculum())
    rows = due_list(load_progress(), problems)
    if not rows:
        print("Nothing due. Do new problems.")
        return
    print(f"{len(rows)} due for review (re-solve from a blank file, do not re-read):")
    for meta, record in rows:
        last = record["attempts"][-1]["outcome"]
        print(f"  {meta['number']:>4}. {meta['title']}  [{meta['pattern']}]  last: {last}")


def current_week(state: dict, curriculum: dict) -> dict:
    """First week that still has unattempted problems."""
    for week in curriculum["weeks"]:
        if any(str(p["number"]) not in state["problems"] for p in week["problems"]):
            return week
    return curriculum["weeks"][-1]


def cmd_today(args) -> None:
    curriculum = load_curriculum()
    problems = index_problems(curriculum)
    state = load_progress()

    week = current_week(state, curriculum)
    print(f"Week {week['week']} - {week['topic']}  ({week['phase']})")
    print()
    print("Learn:")
    for item in week["learn"]:
        print(f"  - {item}")
    print()

    rows = due_list(state, problems)
    if rows:
        print(f"Review first ({len(rows)} due):")
        for meta, _ in rows[:5]:
            print(f"  {meta['number']:>4}. {meta['title']}  [{meta['pattern']}]")
        if len(rows) > 5:
            print(f"  ... and {len(rows) - 5} more")
        print()

    todo = [p for p in week["problems"] if str(p["number"]) not in state["problems"]]
    if todo:
        print("Then new problems:")
        for meta in todo[:3]:
            print(f"  {meta['number']:>4}. {meta['title']}  [{meta['difficulty']}]")
            print(f"        uv run track.py new {meta['number']}")
    else:
        print("Week complete. Next week unlocks once you run `today` again.")


def cmd_stats(args) -> None:
    curriculum = load_curriculum()
    problems = index_problems(curriculum)
    state = load_progress()
    for line in stats_lines(state, problems, curriculum):
        print(line)


def stats_lines(state: dict, problems: dict, curriculum: dict) -> list[str]:
    total = len(problems)
    attempted = len(state["problems"])
    mastered = sum(1 for r in state["problems"].values() if status_of(r) == "mastered")
    all_attempts = [a for r in state["problems"].values() for a in r["attempts"]]
    minutes = sum(a["minutes"] for a in all_attempts)

    first_outcomes = Counter(r["attempts"][0]["outcome"] for r in state["problems"].values() if r["attempts"])
    cold = first_outcomes["solved"] / attempted * 100 if attempted else 0.0

    days = {a["date"] for a in all_attempts}
    streak = 0
    cursor = date.today()
    if cursor.isoformat() not in days:  # today not done yet: do not break the streak
        cursor -= timedelta(days=1)
    while cursor.isoformat() in days:
        streak += 1
        cursor -= timedelta(days=1)

    lines = [
        f"Problems attempted : {attempted}/{total}",
        f"Mastered           : {mastered}",
        f"Total attempts     : {len(all_attempts)}  ({minutes / 60:.1f} h)",
        f"Cold-solve rate    : {cold:.0f}%  (solved unaided on first sight)",
        f"Day streak         : {streak}",
        f"Due today          : {len(due_list(state, problems))}",
    ]

    by_pattern = defaultdict(Counter)
    for number, record in state["problems"].items():
        if number in problems and record["attempts"]:
            by_pattern[problems[number]["pattern"]][record["attempts"][0]["outcome"]] += 1
    shaky = {p: c for p, c in by_pattern.items() if c["solved"] < sum(c.values())}
    if shaky:
        lines += ["", "Weakest patterns (by first-attempt outcome):"]
        ranked = sorted(shaky.items(), key=lambda kv: kv[1]["solved"] / sum(kv[1].values()))
        for pattern, counts in ranked[:5]:
            n = sum(counts.values())
            lines.append(
                f"  {pattern:<26} {counts['solved']}/{n} cold  "
                f"(hint {counts['hint']}, read {counts['read']})"
            )
    return lines


def write_progress_md(state: dict | None = None) -> None:
    curriculum = load_curriculum()
    problems = index_problems(curriculum)
    state = state if state is not None else load_progress()

    icons = {"todo": "( )", "learning": "(~)", "mastered": "(x)"}
    out = [
        "# Progress",
        "",
        "<!-- GENERATED by `uv run track.py sync` - do not edit by hand. -->",
        f"<!-- Started {state['started']}, last updated {date.today().isoformat()}. -->",
        "",
        "## Summary",
        "",
        "```",
        *stats_lines(state, problems, curriculum),
        "```",
        "",
    ]

    rows = due_list(state, problems)
    if rows:
        out += ["## Due for review", "", "Re-solve from a blank file. Do not re-read your old solution.", ""]
        out += [f"- [ ] {m['number']}. {m['title']}  `{m['pattern']}`" for m, _ in rows]
        out += [""]

    out += ["## Curriculum", "", "`( )` not started  `(~)` in progress  `(x)` mastered", ""]
    for week in curriculum["weeks"]:
        done = sum(
            1
            for p in week["problems"]
            if status_of(record_for_readonly(state, p["number"])) != "todo"
        )
        out += [f"### Week {week['week']} - {week['topic']}  ({done}/{len(week['problems'])})", ""]
        out += ["| | # | Problem | Difficulty | Pattern | Attempts | Next review |",
                "|---|---|---|---|---|---|---|"]
        for problem in week["problems"]:
            record = record_for_readonly(state, problem["number"])
            status = status_of(record)
            attempts = "".join(a["outcome"][0].upper() for a in record["attempts"]) or "-"
            out.append(
                f"| {icons[status]} | {problem['number']} | {problem['title']} "
                f"| {problem['difficulty']} | `{problem['pattern']}` | {attempts} "
                f"| {record['next_review'] or '-'} |"
            )
        out += [""]

    recent = sorted(
        (
            (a["date"], problems[n]["title"], a["outcome"], a["minutes"], a["notes"])
            for n, r in state["problems"].items()
            if n in problems
            for a in r["attempts"]
        ),
        reverse=True,
    )[:15]
    if recent:
        out += ["## Recent activity", "", "| Date | Problem | Outcome | Min | Notes |", "|---|---|---|---|---|"]
        out += [f"| {d} | {t} | {o} | {m} | {notes} |" for d, t, o, m, notes in recent]
        out += [""]

    out += ["Attempt key: `S` solved unaided, `H` needed a hint, `R` read the solution.", ""]
    PROGRESS_MD.write_text("\n".join(out))
    print(f"Wrote {PROGRESS_MD.relative_to(ROOT)}")


def record_for_readonly(state: dict, number: int | str) -> dict:
    return state["problems"].get(str(number), {"attempts": [], "streak": 0, "next_review": None})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("today", help="what to work on right now").set_defaults(func=cmd_today)
    sub.add_parser("due", help="reviews due today").set_defaults(func=cmd_due)
    sub.add_parser("stats", help="progress summary").set_defaults(func=cmd_stats)
    sub.add_parser("sync", help="regenerate PROGRESS.md").set_defaults(func=lambda a: write_progress_md())

    p_new = sub.add_parser("new", help="scaffold a problem file")
    p_new.add_argument("number", type=int)
    p_new.set_defaults(func=cmd_new)

    p_log = sub.add_parser("log", help="record an attempt")
    p_log.add_argument("number", type=int)
    p_log.add_argument("outcome", choices=OUTCOMES)
    p_log.add_argument("-m", "--minutes", type=int, required=True)
    p_log.add_argument("-n", "--notes", default="")
    p_log.set_defaults(func=cmd_log)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
