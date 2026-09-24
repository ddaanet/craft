---
name: test-discipline
description: "Make a test evidence rather than decoration: name the state of the world that fails it, get a genuine red from a failed assertion, and check that the suite is reached and the code invoked as production invokes it. Use when writing, reviewing or dispatching tests, when a red step is being planned, or when inherited or subagent-authored tests came back green. Complements test-driven-development rather than replacing it."
---

# Test discipline

A test is evidence only when
**there is a state of the world in which it fails**. A test that stays green
with the code it names deleted asserts something true of the *fixture* rather
than of the code. The fix is always the same move: make the fixture carry the
discrimination, so the assertion has something to be wrong about.

Green is not the bar; green *for the stated reason* is.

**A TDD "watch it fail" step must fail on a failed assertion, never because the
module or command does not exist yet.** "Run both, verify they fail (module
missing)" is not a behavioral test — an ImportError proves nothing about whether
the test asserts anything. Stub the subject importable but inert, run, confirm
each test fails on its assertion, then implement to green.

An assertion that was green the first time it ran is not evidence either. It has
never demonstrated that it discriminates, and no reviewer reading the finished
test can recover that history from the artifact. Where the code already exists
and the ordering cannot supply a red, one mutation per behaviour supplies it
instead.

## The nodes

- [Vacuous green](references/vacuous-green.md) — the catalogue of shapes that
  pass whatever the code does, each with the rebuild that fixes it.
- [Non-vacuous negatives](references/non-vacuous-negatives.md) — how to
  structure a test asserting something does *not* happen so that it cannot go
  vacuous later.
- [Genuine red](references/genuine-red.md) — stub-then-assert, the inert-stub
  batch run and what it does not prove, one mutation per behaviour for a suite
  written after the code, one contract per line, mutating the subject in place
  rather than relocating the test, restoring it by inverting the edit rather
  than from a backup copy, and proving a mutation landed before reading what
  survives it.
- [Coverage shape](references/coverage-shape.md) — outside-in when the
  architecture is settled; assert that the suite is *reached* and that the code
  is *invoked as production invokes it*.

## Dispatch discipline

Apply this hardest to green nobody watched go red — inherited or
subagent-authored work, where nothing shows the red that never happened. In
subagent-driven development a wrong-reason test is not an occasional risk.
Measured instance: across the five tasks of one dispatch, **every single task**
shipped at least one test that passed for the wrong reason, and reading the
tests found none of them. Every assertion on the page was correct; the wrong
cause lived in the fixture, which is the part review skims.

- **Budget one wrong-reason test per task** and let a reviewer hunt for it.
- **Put that reviewer a rung above the implementer.**
- **Dispatch the red phase separately from the green one**, or nobody ever saw
  the test fail. The red-phase review is what proves the test fails against
  unchanged code; "they share a commit" is a packaging detail, not a reason to
  bundle them.

The brief that dispatched the work misdescribes the code in the same way a
hand-listed enumeration does — conformance passes clean against it. The
`plan-contracts` skill covers re-deriving those enumerations by grep.

## For each test guarding non-trivial logic

Name a state of the world in which it fails, and name what else could produce
the observable it checks. Where anything else can, rebuild the fixture until
nothing else can.

Where a behaviour has no such state because it has no entry point of its own,
that is a **missing seam in the code**: open the seam rather than accepting the
test, and until it exists, rename the test to what it actually proves. Never
leave a test whose *name* claims coverage it does not have.

A validation ritual performed once by hand is a test run by hand — behaviour
worth checking belongs in the suite, never in a throwaway fixture — and it stops
being true the moment the code changes. That is what makes the structural
answers in these nodes the answer: they cost no separate pass and keep working
as the code moves.

For the bats mechanisms that make these failure modes concrete —
`run missing_function` exiting 127 before the code exists, `run` being a
subshell so out-params never reach the test — see
`shell-scripting:shell-gotchas`.
