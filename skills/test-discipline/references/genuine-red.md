# Genuine red

## Stub-then-assert

A TDD "watch it fail" step must fail on a **failed assertion**, never because
the module or command does not exist yet. "Run both, verify they fail (module or
command missing)" is not a behavioral test — an ImportError proves nothing about
whether the test asserts anything.

The correct step: **stub the subject importable but inert** — no-op, or a
deliberately wrong return — run, confirm each test fails on its assertion (wrong
value, absent raise), then implement to green.

Never accept "missing subject" in place of "failed assertion". A test that only
errors on a missing symbol has not been shown to detect wrong behavior.

An assertion that was green the first time it ran is not evidence either: it has
never demonstrated that it discriminates, and no reviewer reading the finished
test can recover that history from the artifact.

## The inert stub makes a batch cheap to validate

Run N tests against the inert stub once and every test's red is individually
visible in the output; a test that comes back green has identified itself as
vacuous.

This is why the ordering matters. Tests written before there is anything to pass
them get their red for free, whereas tests validated against a finished
implementation have to manufacture the absence the ordering would have given,
per test.

**What an inert stub does *not* prove** is that a test detects wrongness rather
than absence. An assertion can fail against nothing and still pass against both
the correct implementation and the plausible-but-forbidden one it exists to rule
out. That case needs the *wrong* implementation run against the batch — a second
run, not a per-test exercise.

## Mutate the subject in place, never relocate the test

A shell test that resolves its own root —
`repo_root="$(cd "$(dirname "$0")/.." && pwd)"` — rebinds when the test file is
copied to a temp directory and repointed at an old copy of the script. Fixtures,
payload paths and `cwd` values then all name the wrong tree, and cases fail for
reasons unrelated to the change under test. Measured: a `-e`-versus-`-d` probe
run from a relocated copy reported eight failures where mutating the script in
place reported one, and only the one was signal.

This runs the opposite way from a vacuous green — it manufactures *red*, so a
defect that does not exist clears the "watch it fail" bar and gets a fix written
for it.

Save a copy of the script, mutate it where it lives, restore after. A red-check
recipe handed over in a plan or a skill is where this arrives; check it against
the suite's own root resolution before following it.

## Interface contracts, one per line

In a contract-style plan, conveying a full interface as a run-on paragraph —
semicolon-chained methods, comma-run dataclass lists — is a form of cramming,
the second form beyond long-line line-count gaming. Give each method, dataclass
and exception its own bullet with its full signature and return type.

Un-cramming also surfaces elided return types: three missing `list[...]`
annotations were caught this way on one plan.

**In every plan, phrase red steps as stub-then-assert, and lay out every
`Produces` interface one contract per line.**
