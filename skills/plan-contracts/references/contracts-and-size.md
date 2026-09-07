# Contracts and size

## Contract size predicts implementation size

The 400-line cap on human-reviewed artifacts — plans, PRs — is a **soft**
guideline for reviewability, not a hard gate. Do not block a commit or agonize
over exceeding it in local self-review.

Contract size predicts implementation size: when a single spec or plan task's
**contract** runs past ~400 lines, its implementation almost certainly
overshoots the 400-line PR cap too. Observed at roughly 3.5× — a ~400-line
contract producing a 1385-line implementation.

Catching the overshoot at spec-review time is cheap; discovering it at
PR-slicing time is expensive re-work. So during spec or plan review, treat a
single task's contract approaching 400 lines as the signal to
**split that task**. Weight contract length as a predictor of implementation
length in the update-vs-split decision; do not judge the contract's size in
isolation.

Stating a step as a contract also catches errors that writing it as code hides.
One measured case: a task's test had asserted a fixed surviving line count,
already wrong once. Rewritten as a contract it said
*derive the count from what came back and assert the ceiling*, which is the
load-bearing claim.

## Measure the cap honestly

When an artifact has a line-count cap, the cap is a proxy for *reviewable*.
Hard-wrap prose at the repo's convention first, **then** measure; if it exceeds
the cap, split into multiple focused documents. Never keep the count down by
cramming content onto 150–300-character single lines: long unwrapped lines game
the number while destroying reviewability, the thing the cap protects.

Wrap honestly, measure with `wc -l`, split on a clean seam if over — one corpus
plan split three ways on its local-vs-network seam. Splitting is explicitly
sanctioned by such caps ("anything longer gets split"). Preserve all information
across the split: duplicated front matter (constraints, shared types) is fine;
dropped content is not.

GitHub bodies are the opposite case — they render every newline as a break, so
no hard wrap there.

## The three forms of cramming

**Long lines** are the first, above.

**A run-on paragraph** is the second: conveying a full interface as
semicolon-chained methods or a comma-run type list. One contract per line — the
`test-discipline` skill covers the same rule where it bites hardest, in a stub's
assertions.

**Shaving docstrings on source files** is the third. Fixing one two-population
bug pushed a module from 389 to 406 lines against a 400-line cap, and trimming
the two new docstrings brought it back to exactly 400 — with the real split left
undecided because it sat on the open-decisions list. Trimming *was* the
conservative call there, but it is borrowing against the split, not an
alternative to it: prose is the cheapest thing in the file to cut and the first
thing a later reader needs, and a file parked at exactly its cap has stopped
emitting the signal the cap exists to emit. The next line added anywhere breaks
the build, which reads as a tooling failure rather than as "this module is due
to be split". If trimming is the only way to fit,
**say so out loud and put the split in front of the human as a decision**; never
let the cap be satisfied quietly by prose loss.

## Splitting is not free, so the cap is not absolute

The cap is a *reader-context* budget, and a split imposes its own reader cost —
re-reading several docs, chasing cross-references between them. When that cost
would exceed what the overage saves, accept a bounded overage on one cohesive
doc rather than split reflexively.

Measured instance: one sync plan sat ~40 lines over 400 and was deliberately
kept whole. The content was all validated and the review was not unwieldy, so
splitting would have been *more* human effort, not less.

This is a judgment call, not a licence to cram — the honest-wrap discipline
above still holds. Only the "always split when over" reflex is tempered.
