# How much code a plan carries

Verbatim code belongs in a plan only where a mismatch across a task boundary
would be a real defect. Everything else is stated as a contract, and the
implementer writes the code.

- **Verbatim, always:** signatures, types, names, and literal strings that cross
  a task or process boundary — a `Literal[...]` union's members, a header prefix
  an agent parses, a terminal message. A reviewer reading one task in isolation
  cannot catch a mismatch here.
- **Contract, never code:** function bodies. State the precondition, the
  postcondition and the invariant.
- **Arguably verbatim:** tests, since a test is the contract made executable —
  but only when the implementation is *not* also handed over, or the red phase
  becomes theatre.

## Overriding a plan-writing skill that demands full code

`superpowers:writing-plans` requires the opposite, and says so twice ("code
blocks required for code steps", "Complete code in every step"). Its stated
assumption is that the engineer has "questionable taste" and "doesn't know good
test design". That assumption does not hold for a mid-tier implementer with a
stronger reviewer behind it, and the cost of writing to it is concrete:

- The plan's copy of the code is the one thing in the change that was never run,
  type-checked or linted.
- It goes stale against the tasks written after it.
- An implementer handed the implementation cannot write a genuinely failing
  test, which manufactures a green nobody ever watched fail — see the
  `test-discipline` skill.
- The reviewer ends up reviewing the planner's judgement laundered through the
  implementer, instead of independent work.

Verification belongs in the gate — the linter, the type checker, the test run —
not in an unverified markdown code block.

**So when that skill asks for full code:** write the `Interfaces:` block
verbatim, write the steps as contracts, and
**say in the plan that it deviates**. The implementer needs telling there is no
code to copy, or they will spend the task hunting for it.

**Never edit an installed skill in the plugin cache to make this stick.** The
next upgrade overwrites the edit, silently, and the plan written after it is
back to full code with nobody aware the override was lost.

## Budget the size difference

Contracts are shorter than code, but not by as much as first guessed. Measured
on one plan: 874 lines of code-carrying steps became 537 lines of contracts,
about 1.6×, and its largest task went from ~430 lines to ~190. Budget for 1.6×,
not the 2.5× that seems intuitive.

That leaves a contract near the size cap intact as the split signal — see
[Contracts and size](contracts-and-size.md), which also covers the way stating a
step as a contract catches errors that writing it as code hides.
