# Writing style

## Prose over tables

Prose beats a big table for anything with a paragraph's worth of reasoning in a
cell: a rejected-alternatives or decisions table hides the rationale in one long
cell and forces every entry into the same width. Subsections with a bolded
lead-in read the same at a glance and let the argument breathe. Keep tables for
genuinely tabular data — short, uniform, scannable cells, which is what FR/NFR
rows and transformation contracts are.

Each decision carries its rationale and, where one applies, a **Supersedes** or
**Reopen-if** clause — the condition that puts a settled decision back on the
table. That stops re-litigation and flags when a parked call has gone live
again.

## No draft archaeology

When revising a spec or design doc, scrub language of the form "don't do X (like
a previous version of this doc did)" — "was confusingly similar", "the earlier
constraint is dropped", "the smoking gun", "(good) not (bad)" comparisons
against a prior draft. Implementers and future readers do not know and do not
care about previous versions of the document; self-referential history is noise
to them.

State the surviving design positively. **Keep** rejections of real design
alternatives that make sense on their own ("shelling out to `gh api graphql` was
rejected: …", "deny-patterns were rejected") — those are decisions, not draft
archaeology.

Introduce private or opaque references — sibling repos, personal tooling — on
first use instead of assuming the reader knows them.

## Write-time record vs. current truth

Two rules pull in opposite directions and are resolved by *which artifact* is
being written.

- **A dated design-decision or changelog entry is a record.** It captured the
  thinking at the time, with the information available then. Its rationale
  paragraphs — why option A was chosen, what trade-offs were weighed — are the
  audit trail and are preserved, dates and all.
- **A durable note, a code comment, or a doc's standing description of how the
  system behaves is current truth.** Written present-tense, plainly, with no
  "used to be" framing. Leaving these stale does not preserve thinking, it
  actively misleads.

Inside a design doc the same split applies section by section:
**rationale paragraphs** — preserve; **mechanism descriptions** (how the system
behaves now, what happens in edge case X) — update.

Measured instance: at one release, two reviewers split on exactly this over an
`## Activation` chosen-pattern bullet and a `### Missing-extract edge case`
section, both still describing an abandoned `@`-ref load chain. The spec
reviewer wanted them left as history; the code-quality reviewer called them
current-behavior descriptions. The code-quality framing was correct, and they
were rewritten as such.

## Present-tense standing truth

In durable notes, code comments, and docs, state what is true now. Phrasings
like "no longer true", "X does now fire (contrary to before)", "not what it
was", "the earlier note said Y" read as museum-keeping: a fresh reader who never
held the old belief does not need the rebuttal, and the temporal framing dates
and rots. Git history already preserves what changed — the diff *is* the
changelog.

The vantage is the future reader's, not today's. That reader holds none of
today's state: no pending action, no session about to end, no change halfway
applied. So a body that says "needs a fresh session", "still to be applied", or
"the new wording is going in" names nothing they can act on and is false as soon
as the state moves. Write the standing fact and let the transient half go to the
task file, the todo list or the commit message.

Sanctioned exception: inoculating against a *live* wrong belief still in
circulation — and even then one present-tense clause ("a widespread belief holds
the opposite; test before trusting it"), never a narration of the old version.
**A commit message is exempt:** it *is* a changelog, so before→after phrasing
belongs there.

Distinct but adjacent: do not claim a behaviour *changed* from a single
current-state test. A broken prior config or a different environment explains it
equally, so a delta is not visible in one snapshot.

## Compact prose

"Less connective wordage. Same sense." Connective tissue — transitions, framing,
restated context, re-summaries of what was just said — costs reading time
without adding content. State claims and their grounds directly; drop
transitional sentences and hedged framings.

**Compactness is cutting connectives, not dropping content** — completeness of
substance stays. The same instinct applies to text an agent emits for a channel
rather than for a reader; see the `directive-writing` skill.
