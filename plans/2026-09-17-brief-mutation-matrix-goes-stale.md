## Brief: a mutation matrix describes the bytes it ran against

2026-09-17

Proposed increment to `skills/test-discipline/references/genuine-red.md`.
Arrived from the `handoff` plugin repo, after inheriting a delegated
mutation-check report whose evidence no longer described the shipped file.

### What the skill already covers, and why this is not that

`genuine-red.md` is comprehensive on the mutation itself: "A suite written after
the code gets its red from mutation" gives the one-mutation-per-behaviour bar
and the three readings of a run; "Mutate the subject in place, never relocate
the test" and "Restore by inverting the edit, never from a copy" cover applying
and undoing it. Nothing here proposes changing any of that — in particular the
invert-the-edit rule was checked against a competing backup-file protocol and is
right, for the reason it gives.

The gap is about the **record**, not the mutation: how long a mutation run stays
true after it is made.

### The increment

A mutation matrix is evidence about one exact version of the subject. Any later
edit invalidates it, and nothing re-runs to notice:

- a docstring rewrap to satisfy a formatter
- a lint fix (an unused import, a renamed loop variable)
- a rename, a comment, a reordering

None of those change behaviour, which is exactly why they feel safe to make
after the mutation work is done — and why the invalidation is silent. A report
whose "mutation evidence" section precedes its "green evidence" section is
describing a file that no longer exists by the time anyone reads it.

Two rules follow:

1. **Run the mutations last**, against the final bytes, or re-run them after the
   final edit. Ordering the report's sections does not fix it; ordering the
   *work* does.
2. **Re-run an inherited matrix before believing it.** A matrix produced by a
   delegated agent, or by an earlier session, is a claim about a file that has
   since been through review. Cheap to redo, and the failure mode of trusting it
   is a suite that looks mutation-checked and is not.

### The instance

A delegated `is_empty_body` fix returned a report with a clean three-mutation
matrix and a checksum recorded either side of each restore. The agent then took
a formatter pass over the same file to satisfy `docformatter` and `ruff`
line-length, and noted in passing that the matrix predated it. Re-running all
three mutations against the final file was necessary and reproduced the same
reds — but that was not knowable from the report, and the report as written
would have been believed.

### Suggested shape

A short section after "Restore by inverting the edit", or a paragraph inside it
— the restore rule and this one are both about the mutation run's boundaries in
time, so they read well adjacent.

### Additional context

The same session confirmed the `$TMPDIR` premise the restore section already
rests on: a path written to `$TMPDIR` in one Claude Code Bash call was
unresolvable in the next, in a session whose earlier calls had a working
`$TMPDIR`. That is the failure the section cites, re-observed; no change needed.

Two smaller observations, offered without a recommendation:

- A mutation's red must land on an **assertion**, not an exception. A mutation
  that makes a file absent reds the row at a `FileNotFoundError` during setup,
  which proves the file is missing and nothing about the assertion below it.
  Asserting the artifact exists ahead of every content comparison makes the
  distinction visible. This may already be implied by the skill's "red is a
  failed assertion" thesis.
- A mutation check is a prediction that a change reds a named row, and the
  prediction can fail because the row's *fixture* cannot express the difference
  — not because the code is unpinned. The skill's "a test that goes red under no
  mutation at all asserts something true of the fixture" is the same observation
  from the other side.
