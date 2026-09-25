## Brief: `removing-cleanly` has no check on the premise of a dedup

2026-09-17

Arrived from the `edify` repo, after an outline proposing to collapse a
duplicated block in a skill got two things wrong that a reviewer caught.

This is a proposal, not a decision. The recommendation below is one agent's
reading of where the fact belongs; the placement question is genuinely open.

### The gap

`removing-cleanly` covers the **completeness** of a removal — cut the helpers,
fixtures, absence-guards, docs, inbound links and derived figures in the same
pass. It says nothing about a removal whose premise is
*"these two passages are the same, so one can go"*.

A dedup, a collapse, an extract-shared-node refactor: each cuts one of two
copies and redirects references to the survivor. Same moment the skill already
fires at, and two failure modes it does not name.

**1. The copies have drifted, and the collapse picks a winner silently.** Two
passages maintained separately disagree. The collapse resolves the disagreement
whichever text survives — so the resolution is a decision that should be
declared with a rationale, not a side effect of which paragraph got kept.

**2. The section containing the duplicate also decides something else.** Scoping
the replacement to the enclosing section destroys whatever else that section
owned.

### Evidence

In `edify`, one skill carried its execution-routing block in two reference
files. An outline proposing to merge them asserted the copies "state the same
decision", and scoped the change as "the section, replaced by a pointer".

Both claims were false. The two copies' criteria lists were headed "non-prose
paths only — prose path bypasses these" and "all must hold for
prose/investigation/exploration paths" respectively — they routed differently on
the same input. And the enclosing section separately decided whether an outline
sufficed or a full design was needed, a question the other copy had no
counterpart for; the pointer as scoped would have deleted it.

A reviewer that diffed the passages found both. The author, who had read each
copy for plausibility, had found neither. That asymmetry is the point: a dedup
is the one edit whose whole premise is that reading one copy tells you what the
other says, which is exactly when nobody reads the other.

### Proposed addition

A section in `removing-cleanly`, in the shape its existing "grep for its whole
machinery" paragraph uses — rule, then the measured instance:

- `diff` the passages before treating them as copies, and state what came back,
  even when it is "byte identical".
- Where they differ, classify each difference as wording or substance. A
  substantive one becomes a declared decision with a rationale, never an
  inherited default.
- Scope the replacement to the duplicated **block**, naming its line range, and
  say what in the enclosing section stays.

This brackets the skill's existing claim rather than repeating it: "cut all of
it in one pass" guards against cutting too little, this guards against cutting
past the block.

### Constraint

The skill's `description` currently triggers on "removing a feature, retiring a
file, deleting a module, or handling a version transition in your own tooling".
None of those is how an agent about to merge two copies describes its task, so
the description needs `dedup` / `collapse` / `extract a shared node` or the
addition never fires at the moment it is for.

### Rejected approach

Keeping this as a `ddaanet` memory fact. It was written as one and then
withdrawn: a memory whose body reduces to "when doing X, do Y" is owned by
whatever names X, and pays index bytes in every mounting repo to state it worse
than the owner would. If the addition lands here, the memory should not also
exist.
