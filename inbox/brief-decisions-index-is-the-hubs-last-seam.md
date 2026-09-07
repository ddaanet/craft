## Brief: the decisions index is a design hub's last need-time seam — add it to `design-doc-writing`

2026-09-07

The `design-doc-writing` guidance says a hub at its line cap has a floor —
six sections, a component map, one conclusion line per decision, one
*Rejected* line per group — and that the lever at the floor is to move the
largest hub-only detail into a node. gitlore reached that floor with a new
decision waiting to be concluded and found one more seam the guidance does
not name: the `## Design Decisions` heading itself. The cut was taken, and the
result belongs in the skill rather than in a memory fact, since the moment it
fires at is "writing a design doc", which no index literal routes to.

### Decisions

- **The seam is need-time and falls on a section boundary.** Everything above
  `## Design Decisions` says what the system is and how it is built, read while
  building or debugging a component. Everything below it — the decision groups
  and their *Rejected* lines — is the argument index, read whole when weighing
  or adding a decision. Cut there.
- **The conclusions move whole into `docs/decisions.md`.** One conclusion line
  per decision and every rejected alternative by name, grouped by the node that
  argues them, verbatim from the hub. This preserves the rule the guidance
  already states: a reader weighing a new decision needs every conclusion and
  rejected name in front of them, in one place.
- **The hub keeps its six sections.** §Design Decisions and §Rejected
  Alternatives become pointer stubs to `decisions.md`, the shape §Changelog
  already has toward `changelog.md`. The hub's opening names the index and says
  to read it whole before weighing a decision; the repo's `CLAUDE.md` says the
  same.
- **The checker follows the conclusions, not the hub.** Every conclusion line
  and every delegation (`(D29–D31) in [name](references/x.md)`) is read from
  `decisions.md`; a missing index is an error like a missing hub; citations in
  the hub are still checked against what the index and the nodes define. No
  check needs a conclusion in both files, so there is no two-file hub — one
  constant moved.
- **Collapse restatements before cutting.** The tell for a hub past its floor
  is a section that restates a node instead of summarizing it. gitlore's Hook
  Manager Support and Remote Repository sections both restated
  `installation.md`; they became one Install-time surfaces paragraph. This is
  noise reduction and stands on its own; the split is the structural move.

### Constraints

- The cap stays uniform. A separate, higher cap for the hub — argued as "the
  hub is read whole, so a node's budget does not apply" — was the runbook's
  default and was rejected: the split preserves exactly that property at a
  third of the size, and the cap's own docstring prefers a split.
- Measured on gitlore: hub 400 → 279 lines, index 133 lines at creation, one
  constant retargeted in `scripts/check-docs-links.py`, three new checker tests
  (missing index is an error; a conclusion bullet left in the hub concludes
  nothing; a hub citation is checked against the index).
- Every argument that leaves still leaves its one-line conclusion behind — now
  in the index rather than the hub. The invariant the checker enforces is
  unchanged: a conclusion is reachable before its argument.

### Rejected approaches

- `HUB_MAX_LINES = 440` beside `MAX_LINES = 400`, selected by path. Rejected
  for the reason above, and because the checker's `check_size` docstring
  ("split along a need-time seam rather than raising the cap") would have
  argued against the code beneath it.
- Compressing four lines out of §Architecture. Rewording against a
  hard-wrapping formatter returns almost nothing, as the guidance already
  records.
- Demoting conclusion lines into each node's opening summary. Not a lever:
  it scatters what a decision-weigher needs in one view.

### Additional context

- Where this lands in the skill: the paragraph that begins "The hub has a
  floor, and it is reached before you expect." The decisions-index cut is the
  move after "fold the rejected-alternative names under the decision group" and
  before "move the largest hub-only detail into a node" — it is larger and
  cleaner than the latter, because it moves a whole section along an existing
  heading.
- The split ships with its loading instructions, per the guidance's existing
  rule: the hub's opening and `CLAUDE.md` both name `docs/decisions.md` as the
  file to read whole before weighing a new decision.
- Reference implementation: gitlore, changelog entry
  `docs/changelog/2026-09-07-the-decisions-index-leaves-the-hub.md`, checker
  `scripts/check-docs-links.py` (constant `DECISIONS`), tests
  `tests/check_docs_links.bats`.
- The ddaanet memory fact `design-doc-writing` still describes the hub as the
  home of conclusions. It is being cut into the skill; this brief is the
  correction to carry, not a request to edit the fact.
