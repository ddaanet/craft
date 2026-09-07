---
name: design-doc-writing
description: "Write and maintain a living design doc — the six sections, the state layer, and the splitting, superseding and style rules that keep it current truth rather than an archive. Use when creating, updating, reviewing, splitting or auditing a design doc, spec, or architecture reference, or when a decision, requirement or rejected alternative needs recording. Not for plans and runbooks, which are frozen and date-stamped."
---

# Design doc writing

A design doc is a **living doc**, not a one-off spec. Six sections: functional
requirements, non-functional requirements, architecture, design decisions (with
rationale), rejected alternatives, changelog — and the changelog is a
**separate file** the doc points at. Past a certain size that file is only the
index and each change gets its own dated file beside it,
`docs/changelog/<date>-<title>.md`, one line per entry in the index.

Plans and specs go in a root `plans/`. The design doc is a
**single living doc for the project** — `docs/design.md`. The rule is one living
doc, not one filename: check where the project actually keeps it before creating
a second. Its filename is stable and undated, which is what signals it is
living; frozen specs and plans are date-stamped.

The point is to capture the *why* alongside the *what*, so future sessions do
not re-litigate settled decisions. The rejected-alternatives section matters
most — it prevents revisiting approaches already ruled out for good reason.

When updating, add to the changelog and update the relevant section. Do not
flatten or summarize decisions; preserve the rationale. Asked for a "live" or
"living" design doc, do not reach for brainstorming or ask about scope and
format: the format is settled, and it is this one.

## Two documents, two jobs

The living design answers **what, how and why**, in the present tense: what the
system does, how it is built, why it is built that way. The changelog answers
**how we got here**.

**The changelog is scoped to design-significant changes only.** Git history is
already the full changelog and needs no duplicate. What belongs in the file is
what explains why the project is the way it is — decisions reversed, subsystems
built or torn down, requirements added or dropped, a rationale that turned out
false — never a line-by-line account of every edit. An entry earns its place by
answering a question a future reader would otherwise ask of the design doc and
find no answer to.

That split decides where text goes when a doc is cleaned up. Implementation
status ("slice 3-ii done 2026-07-21, 37 cases in …"), `(implemented 2026-07-15)`
tags stamped on a mechanism paragraph, and "this retired the two earlier
point-fixes" narratives are all changelog material: in the design they are
noise, and they rot. Dates that *ground a claim* stay wherever the claim is —
"verified against CC 2.1.150", "measured over 76 bullets", "eval over 528
transcripts" — because deleting them turns evidence into assertion.

## No measurement of mutable state

A **measurement of mutable state** is neither what the system is nor why: a byte
count of a file that changes on every write, a "this is currently over the
limit" claim, a queue depth, a count of open findings. These read like the
grounded figures above, but they describe a moment rather than supporting a
claim, and they go stale between the commit that records them and the next one.
Refreshing the figure does not fix the category error — it schedules the same
correction again.

Measured instance: one project's `docs/design.md` recorded its memory index at
"~28.9 KB against a 24.4 KB limit"; the store was 31.7 KB three weeks later, and
the fix was queued as a review finding as though the figure were the defect.

- **Delete the figure, keep the mechanism and the pass.** "The index budget is a
  real loader cutoff rather than a soft limit, so retiring entries is a periodic
  pass" survives every future measurement; "the index is 31.7 KB and truncated"
  does not.
- **State that has to live somewhere lives where state lives** — the doc's
  status stamp, a task frame, a report. Those are read as of-a-moment by
  construction; the design record is not.
- **An entry existing only to report that a mutable quantity is out of bounds
  gets retired, not corrected.** Its content was always a task, and the task
  belongs to whatever pass owns it.

## The nodes

- [The state layer](references/state-layer.md) — the six sections say what the
  system is and why, never what is true right now or how much to trust it. Five
  additions carry that, and a cold reader has nothing without them.
- [Splitting an oversized doc](references/splitting-an-oversized-doc.md) —
  trimming has a hard ceiling, so past it the fix is a cut, and which cut
  depends on a measurement taken first.
- [Maintaining entries](references/maintaining-entries.md) — superseding a
  decision, rewiring a citation to a component that no longer exists, and
  retiring an id without renumbering.
- [Writing style](references/writing-style.md) — prose over tables, compact
  prose, present-tense standing truth, and the
  write-time-record-vs-current-truth split that decides which of two opposed
  rules applies.
- [General vs repo-scoped](references/general-vs-repo-scoped.md) — split a
  durable guideline from a point-in-time audit *before* delegating the research,
  or repo-specific commentary leaks into the doc meant to outlast the repo.

## Numbering

Numbering makes requirements, decisions and limitations individually
referenceable (FR-3, D-12, L-5) so other artifacts — and other sections — can
cite them.

**Retire, don't renumber.** Those ids are cited from changelog entries, plans,
reports and other durable notes, so removing one leaves a gap in the sequence.
Renumbering silently repoints every existing citation past the gap at the wrong
entry.

## Reviewing a large doc

Never ask for an eyeball pass over a large doc: volume defeats review. Flag the
high-risk sections explicitly instead — see
[Splitting an oversized doc](references/splitting-an-oversized-doc.md).
