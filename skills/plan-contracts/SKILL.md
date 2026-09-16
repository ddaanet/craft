---
name: plan-contracts
description: "Size a plan or spec to the executable work it carries and state each task as a contract rather than full code, so the document stays reviewable and its enumerations stay true. Use when writing, sizing, splitting or reviewing an implementation plan, spec or design task, when another plan-writing skill asks for complete code in every step, or when a line-count cap on a plan, PR or source file is in play. Not for the design doc itself, which is a living doc rather than a frozen plan."
---

# Plan contracts

A plan doc's length tracks the **executable work**, not the topic. When the work
is concrete — "edit N files, run M commands" — the plan should be that small.
Padding with architecture diagrams, lessons-learned openers, multi-tier dogfood
narratives and self-review checklists feels productive but adds review burden
without changing the work.

Exposition does not help an agent execute — it already has the context — and it
defeats review, because nobody eyeballs 700 lines. Measured instance: a
packaging plan that reduced to 7 executable steps (edit two manifests, validate,
push twice, dogfood twice) ran to 700 lines under a spec template inherited from
the design-bearing plans before it.

**Before writing a plan doc, list the actual executable steps.** Under ~10
commands with no genuine design decisions, skip the spec-style template — a
checklist of steps, open decisions and scope notes, 30 lines or under, is
plenty. Reserve full spec docs for plans carrying design decisions worth
recording across sessions. The template fitting an earlier plan in the same
series is not evidence it fits this one.

## The task's unit is a contract

A plan task states a **contract**: the precondition, the postcondition and the
invariant that the implementation must satisfy — not the function body. Contract
size is the lever the rest of this skill turns on: it predicts implementation
size, it is what a line cap actually measures, and it is what a split cuts.

Two acts follow when the plan-writing skill in play demands complete code
instead. Write the `Interfaces:` block verbatim and the steps as contracts, and
**say in the plan that it deviates** — otherwise the implementer hunts for code
nobody wrote. And never patch the offending skill in the plugin cache to make
the override stick; the next upgrade overwrites it without a word.

- [How much code a plan carries](references/code-in-a-plan.md) — what stays
  verbatim, why full bodies cost more than they save, and the size difference to
  budget for.
- [Contracts and size](references/contracts-and-size.md) — the ~400-line
  contract as the split signal, how to measure a line cap honestly instead of
  gaming it, and cutting duplicated rationale before splitting an over-cap plan.
- [Spec hygiene](references/spec-hygiene.md) — a spec that enumerates its own
  call sites is answering conformance, not completeness; re-derive the list by
  grep before checking anything against it.
- [Before you plan](references/before-you-plan.md) — run the existing pipeline
  against real data first. Fixtures are written by the same hand as the code, so
  they encode the same assumptions and cannot disprove them.

Large docs defeat eyeball review, which is the other half of why a plan is sized
to its work; the `design-doc-writing` skill covers how to present one for review
when it is unavoidably long.
