# Vacuous green

Shapes that pass whatever the code does. Each asserts something true of the
*fixture* rather than of the code, so it stays green with the behaviour it names
removed.

- **Satisfied by birth state.** `topic.dirty is True` after a re-route holds
  with the whole dirtying branch gone, because the topic was created dirty and
  nothing clears it. Assert a transition, or start from the state the code must
  change.

- **Algebraic tautology.** `routed + no_signal + pending + dispatched == total`
  cannot fail when `routed + no_signal` *is* `triaged` by construction and
  `pending` is defined as `total - triaged - dispatched`. It holds at
  `pending = -2`. Pin the components against independently known numbers.

- **Two derived states compared.** "Doing it live equals replaying it" is
  `() == ()` when both sides are empty in the scenario, which is vacuously true
  whether or not the reducer agrees with itself. Any `derived_a == derived_b`
  needs a separate non-emptiness guard, or it proves only that both paths did
  nothing.

- **Parallel values all equal.** Two counts both asserted as `1` cannot detect
  their predicates being exchanged. Where a test pins several parallel numbers,
  make them mutually distinct.

- **Deterministic twins meant to be strangers.** Two "unrelated" fixture git
  repos each seeded with an empty commit under the same test identity and
  message are the *same object* whenever setup lands both in one clock second —
  commits have no randomness. Any surface that needs the two sides to differ (a
  consumer's submodule at the same path as a foreign gitlink, so the fetch must
  fail to resolve one against the other) silently vanishes: the "missing" commit
  is already present, and the test passes vacuously on fast runs and exercises
  the collision only when setup straddled a second boundary. Seed distinct
  content or messages so the twins can never coincide.

- **An isolation fixture with nothing to leak.** To prove A does not see B's
  rows, B must *have* rows. A cross-join or a dropped `.correlate()` is
  invisible when only one entity carries the data the leak would pull in.

- **Idempotence standing in for teardown.** "Rebuild twice, get the same rows"
  stays green with the schema drop deleted, because every write is an upsert.
  Only a row that must *vanish* — inserted out of band, then rebuilt away —
  proves the teardown runs.

- **A substring another line satisfies.** `"topic-a" in output` passes with the
  entire dirty-set line deleted, because a different line also names it. The
  same defect appears in a channel several producers append to — a log, a status
  line, a notification payload: `assert_output --partial "$path"` passes with
  the new message deleted, because some other notice names that path too. Assert
  the line, not the token, and match a phrase unique to the message under test,
  never an identifier the channel carries for other reasons.

- **A downstream effect standing in for the write.** A `record_verdict` test
  called `serve_next` afterwards and asserted the next item was served, which
  "proved" the verdict was recorded — but the queue advances on the `Dispatch`
  row `serve_next` itself wrote. Deleting the entire `record_routing_event` call
  left all ten tests green: the write was **completely unobserved**. Where a
  test observes a downstream effect, assert the actual write directly.

- **End state standing in for the moment.** A test for "X happens too late" or
  "in the wrong step" that asserts only the end state is green for any
  implementation reaching that state later — a retry, a second push, a repair
  pass — including the ones that leave the window open. The end state is the
  cheapest thing to assert and the fixture already exposes it, which is why it
  gets picked. Make the moment observable and assert on it: a stub or hook
  recording what each step offered, an append-only log, a fixture in which the
  late route is impossible.

- **The right exception from the wrong guard.** Two note-validation tests raised
  the right `TriageSessionError`, from the dispatch-ownership guard firing first
  rather than the note check they were named for. When a test pins an exception,
  check nothing upstream raises the same type.

- **A seam that substitutes for the expression under test.** An override read as
  `src="${SEAM:-/proc/$pid/cmdline}"` replaces the *whole* expression, so the
  `$pid` inside it is never evaluated by any test that sets the seam. When every
  test of the function sets it, the selection has no coverage at all while the
  green rows read as covering the function. The tell is a seam whose value spans
  more than the one thing being faked: a single file standing in for a *lookup*,
  one canned response for a *route*, a stub that also swallows its own argument
  computation. Put the seam **beneath** the choice — fake the process tree, not
  the resolved path — so the choice still runs.

- **A bare negative assertion.** A test asserting something does not happen
  passes before the feature exists, and keeps passing if the guard it protects
  is later deleted. It contributes to the green count while proving nothing.

- **A negative against a fall-through gate.** This one cannot pass at all:
  asserting a guarded action did not happen, when the gate guarding it waits and
  then proceeds anyway. Given enough wall clock the action always happens — that
  is what the fall-through is for, since never acting is worse than acting late.
  It fails immediately and reads as a bug in working code, so the reflex is to
  "fix" the implementation, or to weaken the test until it passes and thereby
  stop testing the gate.

Related smell: a read path tested against hand-authored fixtures the write path
cannot produce. Check that fixtures are reachable from the real pipeline, not
merely well-formed.

## Why reading the tests does not find these

A test that sets up state and asserts an outcome is satisfied by **any** cause
producing that outcome, and in a system with several coupled writes — a ledger,
a mirror, a queue that filters on a different row — there is usually more than
one. Writing a negative case first and seeing it green feels like red-green, but
the red never happened; the suite then reports coverage of a branch no test can
distinguish from its absence.
