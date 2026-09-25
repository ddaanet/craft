## Brief: test-discipline and directive-writing increments from a gitlore run

2026-09-18

Arrived from the `gitlore` plugin repo, after a seven-phase orchestrated TDD run
(`tier-arrival-review-minors`) and its audit. A memory-writing pass there
declined to save these as memories because these skills are the owners that
state them at the moment they matter. Each item names the section it extends and
states only the increment. This note ends gitlore's involvement; nothing is
tracked there.

### 1. `test-discipline`, `references/genuine-red.md` — pin the moment

A RED for a defect of the form "X happens too late" or "in the wrong step" that
asserts only the **end state** is green for any lookalike that gets there later
— a retry, a second push, a repair pass — including ones that leave the window
open. End state is the cheapest thing to assert and the fixture already exposes
it, which is why it gets picked.

Make the moment observable and assert on it: a stub `git` or a `pre-receive`
hook recording what each push offered, an append-only step log, a fixture in
which the late route is impossible. Before accepting a GREEN, name one wrong
implementation reaching the same end state and check the test reds it.

Instance: three tier-publication ordering slices in gitlore each asserted the
remote's end state, and review, not the test, found the gap.

### 2. `test-discipline`, `references/genuine-red.md` — a mutation proof goes stale

Overlaps `inbox/brief-mutation-matrix-goes-stale.md` (2026-09-17, from the
`handoff` repo), which covers a matrix invalidated by *behaviour-neutral* edits
and rules "run mutations last" and "re-run an inherited matrix". The increment
here is the behaviour-changing case and who owns the repair:

- The mutation a born-green test's comment names is a measurement of one
  implementation. When the subject changes again — a review fix, a refactor —
  that mutation may **fail for an unrelated reason**, and the case passes under
  it with the defect present while the comment still claims the proof. A re-run
  that merely reds is not enough: confirm the *same line* reds.
- If it no longer does, find the mutation expressing the same wrong
  implementation against the new code, or the test is vacuous.
- **A reviewer who weakens a proof fixes it in the same pass.** Flagging it as a
  residual gives a vacuous test a paper trail and leaves it vacuous.

Instance: a born-green case's proof rotted inside its own slice, between GREEN
and code review, and was filed as a residual.

### 3. `test-discipline`, `references/non-vacuous-negatives.md`, "Ordering under errexit"

One sentence of increment. The section covers negatives sitting behind a
positive. The same mechanism applies to a whole RED run: the first failing line
is the death point, and every assertion **and cleanup line** below it has never
run against any code. A test review lists what sits below the death point and
says which run proves it.

### 4. `test-discipline` — a step from "Path staleness"

A case whose meaning depends on a fixture property asserts that property itself
(`run ! git merge-base --is-ancestor …`, `case "$p" in *\ *)`) rather than
trusting a helper's name, so a repointed helper reds instead of going vacuous.
"A pairing is a property of the fixture, not of the comment above it" is the
neighbouring section; this may already be implied there.

### 5. `directive-writing`, "Distributed text never cites private files" and "Code comments take the same cut"

The same cut covers runbook item and slice ids (`Item 1.3`, `the GREEN report`)
and `file:NNN` line numbers. Subagent-written comments carry these by default,
because the dispatch prompt is the agent's vocabulary for *why*. A sweep that
finds them:

```sh
grep -nE 'plans/|memory/[a-z]|Item [0-9]|slice|GREEN|\.bats:[0-9]|runbook'
```

### Constraints

- Section names were checked against this repo's tree on 2026-09-18.
- Items 3 and 4 are small and may be judged already implied; say so and drop
  them rather than padding the reference.
- A brief's recommendation is input, not a decision — placement and wording are
  this repo's call.
