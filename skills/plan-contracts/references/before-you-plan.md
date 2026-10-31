# Before you plan

Before planning a subproject that builds on an existing pipeline,
**run that pipeline against real data first.** Fixtures are written by the same
hand as the code, so they encode the same assumptions and cannot disprove them.

Measured instance: one corpus tool had 187 green tests and had never fetched a
byte from the service it indexed. One live run produced nine findings, and the
classes they fall into are the ones fixtures structurally cannot reach.

- **Environment the fixture always provides.** Every test used a `tmp_path`,
  which exists; nothing in the system created `corpus/`, so a fresh checkout
  tracebacked on every read command.
- **Scale.** No index on any foreign key is free at 20 fixture rows, and its
  absence made the `heat` command take over 10 minutes at 3875 items — 12
  seconds once indexed.
- **Distribution.** Heat weights set by intuition about importance were inverted
  in practice, because metric scales differ 40× and weight ≠ influence. Sparsity
  too: most items score zero on most metrics.
- **Boundaries real history crosses and fixtures do not.** The service's nested
  connections truncate at their first page, clipping the highest-weighted metric
  precisely on the most-connected items.
- **Unreachable code paths.** A whole designed mechanism — solo-item diff
  fitting — turned out to have no trigger in real data.

## How to run it

**Do the read half first; it is reversible.** Sync, rebuild, then run every read
command over the whole corpus, not one sampled item.

**Sweep for errors *and* warnings across all items.** That is what closed a
property left "hypothesized, not observed" for weeks.

**Hold back anything that writes a non-regenerable ledger** until the read half
is proven.

**Measure distributions, not just "it ran"** — the p50, p90 and max of every
quantity a downstream constant is supposed to bound.

A green suite is evidence about the code's behaviour under the assumptions the
fixtures encode, never about the world; the `test-discipline` skill covers what
a green run does and does not prove.

## Load the skill that governs what the plan edits

A plan that edits an artifact with its own maintenance rules — a living design
doc, a skill — restates those rules as steps, and restates them from recall
unless the governing skill is loaded while the plan is written. The executor
follows the plan, because the plan is more specific, and the skill's rule
arrives only if something invokes it later, after the edit has landed.

Measured instance: an outline told its executor to delete a limitation from a
design doc and renumber the rest. The `design-doc-writing` skill says to retire
an id and leave the gap, because commits, plans and reports cite limitations by
number. The outline was written without loading that skill; the renumber passed
the gate, was committed, and was reversed a commit later, when the skill loaded
for the next edit to the same doc.

**Before writing a step that edits such an artifact, load its skill and check
the step against it.** A step that contradicts the governing skill is a finding
against the plan, not a deviation for the executor to make.
