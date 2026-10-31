# Contracts and size

## Contract size predicts implementation size

The size cap is 20000 bytes for a file and 10000 for a `SKILL.md`, bytes as
`wc -c` counts them, whitespace included: about 10k and 5k tokens as a reader
takes the file in. It is **hard** for design docs and implementation — source
files, skill hubs and nodes — and **soft** for plans and PRs. It exists for
context management, and a file that reaches it usually holds cohesive content to
spin off, so split on that seam rather than arguing the overage. On a plan or a
PR, do not block a commit or agonize over exceeding it in local self-review.

Contract size predicts implementation size: a single spec or plan task's
implementation runs several times the size of its **contract**. Measured
instance, in lines: roughly 3.5×, a ~400-line contract producing a 1385-line
implementation.

Catching the overshoot at spec-review time is cheap; discovering it at
PR-slicing time is expensive re-work. So during spec or plan review, treat a
single task whose contract, scaled by that ratio, would overshoot the PR's size
cap as the signal to **split that task**. Weight contract length as a predictor
of implementation length in the update-vs-split decision; do not judge the
contract's size in isolation.

Stating a step as a contract also catches errors that writing it as code hides.
One measured case: a task's test had asserted a fixed surviving line count,
already wrong once. Rewritten as a contract it said
*derive the count from what came back and assert the ceiling*, which is the
load-bearing claim.

The same holds for a dispatch. One specified `line.strip()` before an emptiness
test on markdown lines, and the subagent implemented it exactly. Stripping
re-opened the defect one indent along: four leading spaces open a code block, so
an indented `# run the migration first` is content, and the strip-first rule
read it as a heading. Reviewing the returned diff found nothing, correctly. The
contract form — under four spaces a heading, four or more content — states the
inputs the rule must handle, which gives the implementer a case set to test
against and the dispatcher one to check the returned rule by.

## Measure the cap honestly

The cap is a proxy for *reviewable*. `check-size` counts bytes, which long lines
and merged paragraphs do not change, so nothing has to run before the count. If
a file exceeds the cap, split it into multiple focused documents on a clean seam
— one corpus plan split three ways on its local-vs-network seam. Splitting is
explicitly sanctioned by such caps ("anything longer gets split"). Preserve all
information across the split: duplicated front matter (constraints, shared
types) is fine; dropped content is not.

GitHub bodies are the opposite case — they render every newline as a break, so
no hard wrap there.

## Before splitting, cut what the plan duplicates

An over-cap plan has two sanctioned escapes under its soft cap, a split and a
bounded overage, and both are wrong when the overage is duplication: a split
files the redundancy in two documents, an overage keeps it whole. Under root
`plans/` a `size.exempt` entry is not one of them: `check-size` skips that
directory and refuses an entry there. The duplication that hides best is the
plan pre-writing the code comments it commissions.

**Where a plan and the comment it commissions would both carry a rationale, the
comment keeps it and the plan names the constraint.** The instinct runs the
other way, because the plan feels like the design artifact. But a plan is read
once and discarded after execution, while the comment ships and is read by
whoever next edits that line.

Measured instance: a design outline at 498 lines against a 400-line cap, roughly
a quarter of it shell-mechanics rationale — a no-match `grep` under
`set -euo pipefail`, `git ls-remote` exiting 128 — each argued in the plan and
each also the subject of a comment the plan told the implementer to write.
Compressed to 376 lines, it lost no content, changed no decision, and no longer
needed a split.

Run this before reaching for a split or an overage, in descending yield:

1. Hoist a failure mode recurring across sections into one short list the
   sections reference.
2. Reduce a flat list of test scenarios to a bullet each, with a shared preamble
   for the assertions every one of them makes.
3. Cut rejected alternatives to a sentence once the decision is settled.
4. Drop any "what changes" summary that restates a per-file section.

This is not the prose loss the next section forbids. Shaving loses what a later
reader needs; cutting duplication loses nothing, because every removed sentence
survives in the place that ships. If a cut would leave a rationale nowhere, it
is shaving — keep it.

## Shaving content is how the cap is gamed

Bytes ignore layout, so only removing content lowers the count. A 300-character
line or a run-on paragraph — a full interface as semicolon-chained methods or a
comma-run type list — is still unreviewable, but that is a readability rule, not
a counting one. One contract per line; the `test-discipline` skill covers the
same rule where it bites hardest, in a stub's assertions.

**Shaving docstrings on source files** is the form that games a byte cap.
Measured instance, in lines: fixing one two-population bug pushed a module from
389 to 406 lines against a 400-line cap, and trimming the two new docstrings
brought it back to exactly 400 — with the real split left undecided because it
sat on the open-decisions list. Trimming *was* the conservative call there, but
it is borrowing against the split, not an alternative to it: prose is the
cheapest thing in the file to cut and the first thing a later reader needs, and
a file parked at exactly its cap has stopped emitting the signal the cap exists
to emit. The next line added anywhere breaks the build, which reads as a tooling
failure rather than as "this module is due to be split". If trimming is the only
way to fit,
**say so out loud and put the split in front of the human as a decision**; never
let the cap be satisfied quietly by prose loss.

## Splitting is not free, so a soft cap is not absolute

The cap is a *reader-context* budget, and a split imposes its own reader cost —
re-reading several docs, chasing cross-references between them. For a plan or a
PR, where the cap is soft, accept a bounded overage on one cohesive doc when
that cost would exceed what the overage saves, rather than split reflexively.

Measured instance, in lines: one sync plan sat ~40 lines over a 400-line cap and
was deliberately kept whole. The content was all validated and the review was
not unwieldy, so splitting would have been *more* human effort, not less.

This is a judgment call, not a licence to shave — the discipline above still
holds. Only the "always split when over" reflex is tempered.
