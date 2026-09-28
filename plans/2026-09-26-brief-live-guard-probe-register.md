# Brief: `test-discipline` covers the fixture register of pairing, not the live one

From a gitlore session, 2026-09-26, reviewing the `ddaanet` memory store. No
change is proposed to gitlore; this is a gap in `craft:test-discipline` that a
retiring memory fact can fill.

## The claim `non-vacuous-negatives.md` already makes

`references/non-vacuous-negatives.md` owns the pairing rule in its test-suite
register, under **path staleness**: "Pair each negative with a positive over the
**same fixture**, differing only in the guard's trigger input. Positive red
means the path or the wording drifted; negative red means the guard was deleted
or widened."

That is the same argument as the one below, and the skill states it only for
assertions inside a suite.

## The register it does not cover

A guard verified by a **live probe** rather than a fixture — a permission hook,
a sandbox rule, an agent's frontmatter `hooks:`, anything whose containment is
demonstrated by running something and watching it be refused. Three additions:

- **The deny alone proves nothing, for the same reason path staleness does.** A
  guard broken *closed* refuses the provocation too, and from the deny alone
  that is indistinguishable from the guard working. Pair the must-block probe
  with a command that must be **allowed**, in the same run.
- **Read the probe's tool result, not the agent's report of it.** Where the
  probe runs inside a subagent, the agent is not a witness to its own
  containment: it has no way to observe a hook that was never attached, so it
  reasons from the definition it was given and answers that it was contained. A
  gitlore check on 2026-07-24 was recorded as proving containment live; the
  transcript shows the probe command executing and printing its output. The
  agent said contained, the tool result said executed, and the agent was
  believed for weeks.
- **The probe must be harmless if the guard is dead.** An `echo` and a throwaway
  file, never real data — the whole point is that it may well run.

A fourth, weaker note, if it fits: a uniform history corroborates nothing. Every
dispatch in a project can share the shape under inspection while the one field
that differs is the one that decides the outcome.

## Provenance

These lines are being cut from the `ddaanet` fact
`frontmatter-hooks-two-silent-gates`, which is over the 4096-byte recall cap and
splitting into a hub plus one file per gate. The harness-specific halves (an
exact-key trust lookup, a dispatch `name` overwriting `agentType`) stay in the
memory store, keyed to their symptoms; the register above is general and belongs
with the skill that owns evidence quality. Nothing in the store will assert it
after the split, so if it is not wanted here it is lost — which is a fine
outcome if the judgement is that `non-vacuous-negatives.md` generalizes to live
probes as written.
