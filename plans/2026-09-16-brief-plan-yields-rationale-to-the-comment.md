## Brief: a plan yields rationale to the comment it commissions

2026-09-16 — from a session in `ddaanet/claude-plugin-dev`

Concerns `plan-contracts`. That skill owns sizing a plan to its executable work,
contracts rather than code, and the ~400-line split signal. It does not say what
to do when a plan is over its cap and the overage is not padding but duplication
of the code it is about to produce.

### Observed

A design outline for first-release version selection reached 498 lines against a
400-line cap enforced by the repo's docs gate. The obvious moves were to split
it across nodes or to mark it exempt; the gate's own comment reserves the
exemption marker for a plan that already landed, so a split looked like the
answer.

It was not. Roughly a quarter of the document was shell-mechanics rationale — a
no-match `grep` under `set -euo pipefail`, `git ls-remote` exiting 128, a hook
exiting non-zero being a non-blocking error that lets through the call it
refused. Each was argued in the plan, and each was *also* the subject of a code
comment the same plan instructed the implementer to write. The plan was
pre-writing its own comments.

Compression to 376 lines lost no content, changed no decision, and removed the
need to split at all. Splitting would have filed the redundancy in two documents
instead of removing it; the exemption would have preserved it whole.

### Proposal

**Where a plan and the code comment it commissions would both carry a rationale,
the comment keeps it and the plan names the constraint.** A failure mode
recurring across several sections is hoisted into one short list the sections
reference.

This is worth stating because the instinct runs the other way: the plan is the
design artifact, so rationale feels like it belongs there and the comment feels
like a pointer. The durable reason it is backwards — a plan is read once and
discarded after execution, while the comment ships and is read by whoever next
edits that line.

Second, a checklist for an over-cap plan, in descending yield, to run **before**
reaching for a split or an exemption:

1. Recurring mechanics hoisted into one section.
2. A flat list of test scenarios reduced to a bullet each, with a shared
   preamble for the assertions every one of them makes.
3. Rejected alternatives cut to a sentence once the decision is settled.
4. Any "what changes" summary that restates a per-file section.

### Constraints

- Craft ships prose. This is a rule in `plan-contracts`, most likely a section
  in `references/contracts-and-size.md` beside the existing split-signal
  material, not a new skill and not a script.
- Coverage check, for verification rather than trust: grepped `SKILL.md`,
  `references/contracts-and-size.md` and `references/code-in-a-plan.md` for
  `comment|duplicat|redundan|twice|argue|rationale|hoist|compress`. The only
  near hit is "duplicated front matter (constraints, shared types) is fine" in
  `contracts-and-size.md`, which is about what may repeat *across a split* — the
  opposite question. Re-run it against the shipped version before acting.
- The measured instance is one document. The rule generalises on its reasoning,
  not on sample size.

### Rejected approaches

- **A ddaanet memory entry.** Written, then discarded. Subtracting the anecdote
  leaves one sentence, and a tier index line is loaded by every session in every
  mounting repo against an index already over its loader cap. Too thin to buy
  that, and it would sit on `plan-contracts`' own topic.
- **A project memory in the originating repo.** The fact is not
  project-specific, so it would be in the wrong tier in the other direction.
- **Leaving it implicit in the compressed outline.** The compressed document
  demonstrates the rule without stating it, so nothing carries it to the next
  plan.

### Additional context

The cap that surfaced this is the ddaanet 400-line convention, which already
warns against satisfying a cap "quietly" by cramming lines or shaving prose.
Splitting and exempting are the two sanctioned escapes, and both are wrong when
the overage is duplication — that is the gap this brief is about.
