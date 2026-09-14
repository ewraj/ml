# ml-from-scratch

Phase 1 of a year-long ML plan (14 Sep – 22 Nov 2026, 60 sessions): foundations,
numpy only, one rule — **implement before you import.**

## The quarantine rule (read this first, every session)

You have called `.fit()` before. For the next ten weeks, treat everything you
know from that layer as vocabulary you happen to have, not knowledge you can
lean on. When a session covers something whose *name* you recognize, that's
the signal to slow down, not skip.

The failure mode to watch for: "logistic regression, I've done that." You
haven't. You've called it. The gap between those is the entire point of
Phase 1.

What **not** to discard: your C/C++/Java. Memory layout, pointers, OOP design
— those are a real advantage here and most people arriving at ML don't have
them. The Friday session on why numpy is fast is a C mental model. Week 5's
library API design is an OOP problem.

One trap that comes with that background: don't write Python like C. Index
loops and manual bookkeeping will fight you all week. **This session's
exercise is the cure.**

## Setup

```
python -m venv .venv
.venv/Scripts/activate        # .venv/bin/activate on macOS/Linux
pip install -e ".[dev]"
```

## W1 — numpy from the metal

`exercises/loops.py` has ten functions, each written index-by-index the way
a C/Java brain writes them. They're correct — that was never the problem.

`exercises/vectorized.py` has the same ten functions as stubs. Rewrite each
one using broadcasting, reductions, and `einsum`. **No `for`/`while` over the
data** — `tests/test_vectorized.py` checks this by parsing the file, not by
trusting you.

```
pytest              # correctness + the no-loop rule, per function
ruff check .         # style
```

A function is done when its test goes green. All ten green is the session.
Delete the hint comments in `vectorized.py` as you stop needing them.

## This week — 14-20 Sep 2026

Session plans, one file per day, in `days/`. Each has the calendar block, what
to cover, a gist of the ideas, a done-when checklist, and blank space to fill
in as you go.

| Day | ML block | Other blocks | Hrs |
|---|---|---|---|
| [Mon 14](days/2026-09-14-mon.md) | numpy from the metal — the ten functions | DSA A1 | 5 |
| [Tue 15](days/2026-09-15-tue.md) | Essence of Linear Algebra + pure-Python matmul/inverse | DSA A1 · Apply | 6 |
| [Wed 16](days/2026-09-16-wed.md) | Reps — rebuild cold; det/rank/inv without `np.linalg` | DSA A1 | 5 |
| [Thu 17](days/2026-09-17-thu.md) | MML Ch.2, exercises 2.1-2.8 | DSA A1 | 5 |
| [Fri 18](days/2026-09-18-fri.md) | Depth — why numpy is fast; benchmark + write-up | DSA A1 · Ship | 6 |
| [Sat 19](days/2026-09-19-sat.md) | — | DSA contest + upsolve | 4 |
| [Sun 20](days/2026-09-20-sun.md) | k-NN from scratch, MNIST subset | DSA re-solve · Trading T1.1 | 11 |

**42 hours.** The week's arc: vectorize it (Mon) -> understand it (Tue, Thu) ->
rebuild it cold (Wed) -> understand why it's fast (Fri) -> build something real
with it (Sun).

## Also here

- [`git-github.md`](git-github.md) — git and GitHub reference: the mental model,
  the daily loop, the undo table, and how to make a repo readable to someone
  hiring you.
