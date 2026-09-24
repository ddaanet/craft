## Brief: three mutations the ordinary red misses

For `skills/test-discipline`. Evidence from claude-plugin-dev's
deliverable-review fix pass (`plans/2026-09-18-deliverable-review-fixes/`),
where each case was found in a gate that had passed its own red step.

### A refusal's prose is a behaviour

A guard has two outputs: its decision (exit status, deny/allow) and the message
it prints. A red that mutates only the decision leaves the wording unpinned, so
a deny reason naming a recipe it must not name, or a `hint:` block carrying the
wrong value, stays green. The red for a refusal mutates the message too — change
the wording the test means to pin and confirm a `contains` assertion on the
literal goes red. Found twice in the same pass (version-guard's initial-release
branch, release.sh's drift refusal).

### An equality assertion is not gated by another equal value

`assert_eq "$got" "$want"` is only proven by a mutation that changes what the
subject emits. Swapping a fixture value for another the subject reproduces
verbatim keeps the test green. Mutate the subject's transformation — drop a
field, reorder, alter the format — not the input it copies through.

### A `set -o` line masks the property it enforces

When `set -euo pipefail` is what makes a `cmd | cut` capture fail closed, no
test of the script as it stands can show the capture itself fails closed: the
option covers it, and a lost `set` line is exactly the regression to guard. Run
the scenario against a copy with the line rewritten, and prove the rewrite
landed, or a renamed `set` line silently turns the scenario into a second run of
the unmodified script:

```sh
sed '/^set -euo pipefail$/s//set -eu/' "$script" > "$nopipefail"
grep -qx 'set -eu' "$nopipefail" || fail "the set line was not rewritten"
```

`tests/release-test.sh` in claude-plugin-dev does this for its `ls-remote | cut`
probes.

### Constraints

- Input, not a decision: the skill already says one mutation per behaviour;
  these are candidates for the list of behaviours it names, and may fit as one
  node rather than three.
- One repository's evidence, over shell scripts behind an assertion-harness
  suite.
