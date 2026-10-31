# Brief: the design hub keeps every conclusion; a size split moves argument out of the bullets

From a claude-plugin-dev session, 2026-10-31. A correction from my human
partner, with the craft text it contradicts. Not yet applied anywhere.

## The rule

The conclusions — the standing decisions, one line each — are all that has to be
true. Together they *are* the system overview, so they stay in the hub. A split
for size never moves them out, neither wholesale into a decisions file nor one
by one into the head of each node.

What moves instead is argument embedded inside a conclusion bullet: the
mechanism, the bug that motivated it, the "because" clause, the measurement.
That material is read when weighing or changing that one decision, which is a
time-of-need seam; the conclusion is read on every trip, which is why it stays.
Each bullet keeps its conclusion and its invariant and points at the node.

My human partner's words, rejecting a plan that moved the conclusions out:
"splitting decisions.md and reading it every time (it's the core of the design,
right?) works around the intent of the cap", and "The logic was to keep the
conclusions in the design doc, because that's all that has to be true. Moving
the individual conclusions to their decision file replaces the system overview."

## What craft says now

`skills/design-doc-writing/references/splitting-an-oversized-doc.md`, section
"The hub has a floor, and it arrives early":

- Lines 58–64 already reject demoting conclusions into each node's opening
  summary. That half agrees and stays.
- Lines 70–88 then prescribe the opposite at the floor: "the conclusions move
  whole into `docs/decisions.md`", with the hub's two decision sections reduced
  to pointer stubs. The section itself concedes "nobody skips a decisions index
  — they read it whole". A file read whole on the way to any decision is the hub
  under another name; the cut satisfies the cap without reducing what is read.
  That is the move the correction rejects.
- Lines 90–95 retarget the checker to the index; they go with the cut.

## Proposed change

Replace the `docs/decisions.md` cut (lines 70–95) with the lever the correction
names: once every mechanism section has moved, audit the conclusion bullets
themselves and move every clause that argues rather than concludes into the node
that owns the decision, leaving the conclusion, its invariant and the pointer.
The floor is then one line per decision with no argument in it; a hub still over
its cap at that floor has a group that has become a subsystem, which line 170's
rule already handles (one hub entry for the cluster, its sub-decisions
concluding in its node).

The "Collapse restatements" paragraph (66–69) and the "never a reason to leave a
new conclusion out" paragraph (97–100) stand as written.

## Where it arose

claude-plugin-dev's `docs/design.md` is about 2% over its size cap after the cap
moved to non-whitespace bytes (see
`inbox/2026-10-31-brief-size-cap-in-nonws-bytes.md`). Its plan
(`plans/2026-10-31-line-cap-gate/design.md` there, step 1) first proposed a
`decisions.md` per this reference, was corrected, and now does a full pass over
its 67 hub bullets moving the embedded argument into the `docs/references/`
nodes. Whether that pass lands the hub under the cap is the measurement that
would confirm or refute the proposed floor.
