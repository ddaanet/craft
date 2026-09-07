## Brief: FR/NFR rows are not the tabular case — correct it as `design-doc-writing` becomes a skill

2026-09-04

The `design-doc-writing` fact in the shared `ddaanet` tier names FR and NFR rows
as an example of genuinely tabular data. That is wrong, my human partner
corrected it, and the correction has to reach the skill being cut from that
fact — not just the fact. Two sentences carry the error, in two different
sections, and a pass that fixes only the obvious one leaves the doc
contradicting itself.

### Decisions

- **The rule is: no tables, except for small amounts of content.** My human
  partner's words. Default to prose; reach for a table only where the cells
  really are small.
- **A transformation contract stays the tabular example. FR and NFR rows do
  not.** A requirement stated as a sentence is neither short nor uniform, which
  is the test the section already gives — it just drew the wrong conclusion
  from it.
- **Requirement sections take the same bolded lead-in prose as decisions.** Each
  entry carries its id, the statement, the status and the `Where · pinned by`
  pin inline. Numbering survives the move, so `FR-7` stays citable from a plan,
  a commit message or another section.
- **The state layer's fourth item changes with it.** It called `Where · pinned
  by` a *column on the FR and NFR tables*. With no tables it is a clause on each
  entry. This is the sentence a fix aimed only at the *Prose over tables*
  section will miss, and leaving it turns the skill into an instruction to build
  a table that the same skill forbids two sections later.

### Constraints

- **The tier fact is deliberately left uncorrected — this brief is the only
  carrier.** `design-doc-writing` is being retired into the skill, so editing it
  would record a residual in a file that is going away, and a skill cut from it
  afterwards would still need this correction applied by hand. Take the wording
  below as the intended text; the tier's own copy still reads the old way and
  should not be trusted or patched.
- **The skill text must not cite the memory store.** No wikilink, no `memory/`
  path, no bare fact filename — consumers do not have the store, so any of those
  dangles for all of them. Inline the criteria instead.

The corrected *Prose over tables* wording now reads:

> Keep tables for genuinely tabular data — short, uniform, scannable cells,
> which is what a transformation contract is. **FR and NFR rows usually are
> not**: a requirement stated as a sentence is neither short nor uniform, so
> those sections take the same bolded lead-in prose as decisions, each carrying
> its id, the statement, the status and the `Where · pinned by` pin inline.
> Numbering survives the move, so `FR-7` stays citable. Default to prose and
> reach for a table only where the cells really are small.

And the state-layer item now opens `**A `Where · pinned by` clause** on every FR
and NFR entry, mapping each requirement to its code symbol and the test that
proves it` — clause, every entry, no table.

### Rejected approaches

- **Fixing only the *Prose over tables* section.** It leaves the state layer
  prescribing a column on a table the reader was just told not to build. The two
  sentences are one correction.
- **Dropping the `Where · pinned by` pin along with the column.** The pin is
  what makes a `Done` status re-checkable rather than a bare claim; it survives
  the format change and moves inline.
- **Treating this as a formatting preference.** The failure it prevents is
  concrete: a doc written from the uncorrected fact produced two tables whose
  every cell held a full sentence, which is exactly what the section's own
  opening paragraph argues against.

### Additional context

The correction came out of writing `docs/design.md` for the `plugin-craft`
plugin. That doc followed the fact as written, produced FR and NFR tables with
sentence-length cells, and was corrected on sight. Its current state is the
worked example of the prose form, if one is wanted — nine FR entries and four
NFR entries as bolded lead-in subsections, each ending in an italicised status
and its pin, at `~/code/plugin-craft/docs/design.md`.

Worth knowing while extracting: this same tier fact is what `plugin-craft` cut
its four skills from, and that pass found two classes of dangling identifier a
wikilink check cannot see — internal requirement, decision and plan ids
(`FR5a`, `(D14)`, `Plan 04 Step 6`) and file paths in another repository. Both
appear in the tier's design-doc material. `my human partner` phrasing is *not*
in that set and ships fine in a skill body, on the `superpowers` precedent.
