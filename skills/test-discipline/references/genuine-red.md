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

A red is evidence for the one assertion it landed on. Under errexit the test
dies there, so every assertion below it ran for the first time in the green that
followed: born green, inside a test that passed its red step. Measured: a
refusal's exit status redded and the wording assertion under it never did, and
the wording was wrong, twice in one pass.

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

## A suite written after the code gets its red from mutation

Tests written against an implementation that already works are green on their
first run, so the ordering never supplies a red. Manufacturing the absence per
test is the general remedy; the systematic form is
**one mutation per behaviour the suite claims to pin**.

Take each check, branch or rule the code implements, neuter exactly that one in
the subject where it lives, run the whole suite, and record which tests go red.
Three things come out of the run that reading the tests cannot give you:

- **A mutation nothing catches** names an unpinned behaviour. The suite looked
  complete and was not.
- **A red that is not the test named for the mutated behaviour** means the test
  that failed is coupled to something it does not claim, while the one that
  should have failed is passing for another reason.
- **A test that goes red under no mutation at all** asserts something true of
  the fixture rather than of the code.

The bar is that every mutation is caught, and caught by its own test. Measured:
thirty tests over a gate's eleven checks, thirteen mutations, each turning red
the test named for it and none surviving — which is exactly the evidence the
first green run could not give.

This only works if the assertions are exact. A test asserting merely that the
run failed passes whenever *any* check fires, so it survives the mutation of its
own check whenever the fixture happens to trip a second one. Assert the complete
output and a mutation has nowhere to hide.

The red a mutation owes is the red the ordering owes: a failed assertion. A
mutation that removes a file reds the test at a setup exception, which proves
the file is missing and nothing about the assertion below it.

Mutate in place and restore after, per the next section — a suite copied
somewhere else to be mutated fails for reasons unrelated to the mutation.

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

Mutate the script where it lives, then restore it per the next section. A
red-check recipe handed over in a plan or a skill is where relocation arrives;
check it against the suite's own root resolution before following it.

## Restore by inverting the edit, never from a copy

Mutating, running the suite and restoring are separate tool calls, so any
restore that depends on state surviving between calls is the hazard. Measured: a
backup written to `$TMPDIR` succeeded, the suite redded as intended, and the
restore one call later read an empty `$TMPDIR` — `cp` failed, and the mutation
stayed live in a tree holding uncommitted work. The `&&` that chained the backup
proved it was written, never that it could be found again.

Apply the mutation as an exact string replacement, and restore by applying it
again with the two strings swapped. No backup file, no scratch directory, and
the string pair is itself the record of what was changed.

- **The mutated string must be unique in the file.** Inverting `return []` in a
  file that already holds another `return []` restores the wrong line. Choose a
  mutation text that occurs nowhere else, or confirm its count before applying.
- **Prove the mutation landed.** A replacement whose old string matches nothing
  exits 0 and changes nothing, so the suite stays green and the run reads as a
  mutation nothing catches — a false finding of an unpinned behaviour. Grep for
  the mutated text before running the suite. Measured: a `sed` dropping
  `pipefail` from a `set` line, where a renamed line turns the scenario into a
  second run of the unmodified script. The same false reading arrives when a
  recorded mutation is re-applied after the subject changed: the recipe names
  bytes and the proof names a behaviour, so the recipe having missed is the
  first reading to check, ahead of the two that `non-vacuous-negatives` gives a
  survived mutation.
- **Prove the restore.** Grep for the mutation text and expect no hit, then run
  the full suite and expect green. The replacement exiting 0 is not the
  evidence.

Rejected, each for a reason worth keeping: `${TMPDIR:-/tmp}` keeps the
cross-call assumption and only covers an unset variable;
`git checkout -- <file>` and `git stash` discard the uncommitted fixes of the
very session that is mutation-checking a test it just wrote.

## Interface contracts, one per line

In a contract-style plan, conveying a full interface as a run-on paragraph —
semicolon-chained methods, comma-run dataclass lists — is cramming that a byte
count does not catch. Give each method, dataclass and exception its own bullet
with its full signature and return type.

Un-cramming also surfaces elided return types: three missing `list[...]`
annotations were caught this way on one plan.

**In every plan, phrase red steps as stub-then-assert, and lay out every
`Produces` interface one contract per line.**
