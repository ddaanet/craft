# Coverage shape

## Outside-in when the architecture is settled

When the architecture is already settled — decided in a design doc, say — start
TDD from a **red end-to-end test that names the user-facing contract**, then let
its failure modes drive what to build next. Do not default to bottom-up unit
tests first.

Bottom-up unit tests can pass while the integration contract is still broken:
they verify internal consistency, not the behavior the user cares about.
Outside-in red-first tests are black-box by construction — they assert through
the boundary — so:

- the test survives refactors of the internals;
- the next failure names the next file to write, with no speculative helpers;
- integration risk (fixtures, stubs, env setup) gets exercised on day 1 instead
  of being deferred.

Measured instance: one plan had its end-to-end test added last, so its passing
only confirmed unit-test self-consistency, not the contract.

**Default to outside-in when a design doc exists**: e2e (red) → fill in by
following failures → backfill unit tests at the seams the e2e does not reach.
Fall back to bottom-up only when the architecture itself is still being
discovered.

Constrain at the artifact boundary rather than mid-stream — the same principle
one level up; the `directive-writing` skill covers it.

## Assert the invocation contract

A test harness usually invokes code the most convenient way, not the way the
runtime does. **Every difference between those two is an untested contract** —
and mode bits, shebangs, `$PATH` resolution and CWD are invisible to a green
suite.

Measured instance: a hook script shipped through 16 green tests, three task
reviews and a lint pass while committed **mode 100644**. Its manifest invokes
hooks *by path*, so in production it would have failed `Permission denied`
(rc=126) on every `Write` and `Edit` in every installed project. Every test
invoked it as `bash "$SCRIPT"`, which bypasses the executable bit entirely. The
suite was green precisely because it tested a different invocation path than the
real one. Only the final whole-branch review caught it.

When code is invoked by something other than the test — a hook manifest, cron,
systemd, a shell exec —
**assert the invocation contract itself, not just the behavior.** Concretely:
`[ -x path ]` per hook script.

**Corollary:** use `git ls-files -s` (recorded mode), not `ls -l` (local
filesystem mode). A fresh clone reproduces git's mode, and a local `chmod` can
mask the bug.

The pattern had already been added elsewhere in the same repo for this exact
reason. The lesson had been learned once and not generalized.

A guard is invoked by the system it contains, so its ALLOW case is a command
that system really issues, copied from a recorded invocation rather than
composed from memory of its shape, and not a synthetic probe. An allowlist hook
signed off on blocked probes alone admitted no space or quote, while the
subcommand it contained takes a quoted, multi-word note on every call. So it
blocked the one operation the contained agent existed to perform. After moving
or editing a live guard, re-provoke it and read two things off the denial: the
script path the harness attributes it to, which proves which copy fired rather
than a stale one, and a phrase only the new text contains, which proves the edit
is what runs. Pair the provocation with a must-ALLOW command in the same check,
because a guard broken closed blocks the provocation too and looks like success
from the deny alone.

## A suite that is not run cannot fail

Same family, one layer up. A hand-listed `make test` had five `.bats` suites (21
tests) drift off the list — including the cover for a load-bearing memory-gate
invariant. That invariant sat with zero regression cover and nothing reported
it: **an unlisted suite is indistinguishable from a passing one.** The fix is
globbing (`wildcard` / `filter-out`) so discovery cannot drift.

**Green means nothing without knowing what ran.** Check the count and plan
lines, not just the exit status. Two contracts are worth asserting rather than
assuming: the suite is *reached* (discovery), and the code is
*invoked as production invokes it* (mode, shebang, PATH).

## Corollary on measuring

A pipe (`make test | tail`) reports the *last* stage's exit status, so a failing
suite reads as exit 0. Two concurrent runs redirected to the same log interleave
into a garbage count. Both landed at once on one measurement, producing a bogus
"393 green".

Redirect to distinct files, echo `$?` before any pipe, count `^ok` and
`^not ok`, and sanity-check the delta: a number that moves the wrong way is a
broken measurement, not a surprise.

This is the same failure family as dogfooding the real target — fixtures and
tests miss what the real target hits.
