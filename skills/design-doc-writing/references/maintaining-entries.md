# Maintaining entries

## Superseding a decision

When a decision is superseded, the old section is deleted and the commit that
deletes it says why; every *mechanism* description elsewhere gets updated to the
new truth. An old approach worth keeping as ruled out becomes a
rejected-alternative entry carrying its reason. A stale architecture section
outlives its decision otherwise: on one project a branch model was rewritten by
a decision in July, and the Architecture "Branch Model" section, two earlier
decisions and four rejected-alternative rows still described the abandoned named
per-worktree branches ten days later.

A past decision whose rationale looks thin on re-reading gets
**re-examined, not treated as settled**; new context or fresh eyes can invert
it. One measured inversion: a "no SessionStart hook, use an `@`-ref instead"
decision had given "no hook overhead" and "no race conditions" as its arguments,
both negligible in practice, while the cost of the chosen path — a whole
user-facing setup skill, an entire silent-failure mode — was structural. The
inversion produced a cleaner architecture.

- When citing a past decision, check whether the *reasons* it gave still hold.
  Do not just relay the conclusion.
- When someone challenges a documented decision, default to honest
  re-examination over defending the doc.
- Be willing to write a new spec that inverts an old one. Spec history in git is
  the audit trail; the latest doc is the current answer.

The new entry leads with the reason it stands — the constraint the incident
exposed, in the present tense — then the positive design and its reasoning. The
incident itself goes in the commit body. Cut the museum narrative: deletion
inventories ("extract.py loses functions A, B, C…"), "it no longer does what it
used to" framing, and inversion-bookkeeping ("this supersedes decision X and
Y"). "Retained as a record of what was cut" is not a justification.

## Rewiring a dead component

When a component a living design doc references is removed,
**rewire the document** in the same sweep as the code. Neither of the two easy
moves is right: leaving the stale reference standing, or deleting the decision
along with the thing it named.

These documents carry institutional memory, and a decision pointing at something
that no longer exists degrades into noise a future session can neither act on
nor trust. But the decision usually outlives its mechanism — deleting it invites
re-litigating a question already settled for good reason, which is the
rejected-alternatives section's whole job. The audit trail lives in git history;
the document is current truth.

Four rewires, by what survived:

- **A successor exists** → substitute it. This is the mechanism-vs-rationale
  split applied to a name.
- **The mechanism died, the principle survived** → generalize the prose rather
  than delete the decision. "`edify _recall resolve` is the canonical gate
  anchor" becomes "the recall pass is the canonical gate anchor" — same
  decision, one abstraction level up, no dangling name.
- **The decision is *about* the dead component** → keep the name, because naming
  it is the point. Evidence that a precommit gate broke for nine days on a
  non-existent `edify validate` command is worthless with the command redacted.
- **Nothing replaced it** → say so inline. A sentence stating the script was not
  restored is a fact a reader can act on; a path that silently resolves to
  nothing is not.

The failure this prevents is asymmetric. A stale pointer is usually caught by
the next reader who follows it; a dropped decision is silent, and its cost
arrives later as someone re-deriving an answer the project already had.

## Retiring an entry

An entry that exists only to report a measurement of mutable state gets retired
rather than corrected — its content was always a task. Delete the figure, keep
the mechanism and the pass that acts on it.

**Retire, don't renumber.** FR/D/L ids are cited from commits, plans, reports
and other durable notes, so removing one leaves a gap in the sequence. Leave the
gap: renumbering silently repoints every existing citation past it at the wrong
entry.
