# Non-vacuous negatives

Where ordering can buy a genuine red for free, take it: write the check before
the thing it checks. Where it cannot — a test pinning behaviour that already
works — the answer is **structural**, not a separate validation pass. Build the
assertion so that it cannot pass while the thing it watches is absent.

## The three stalenesses

- **String staleness** — the negative asserts the absence of wording production
  no longer emits. Hold every trigger string in a global defined in the test
  helper, and assert it from a positive test as well as the negative. A rename
  in production turns the positive red, the global is corrected once, and the
  negative moves with it. Define the literal test-side: sourcing it from the
  production lib moves both sides together and the positive stops pinning the
  wording.

- **Path staleness** — the negative passes because its fixture never reaches the
  guard at all. Pair each negative with a positive over the **same fixture**,
  differing only in the guard's trigger input. Positive red means the path or
  the wording drifted; negative red means the guard was deleted or widened.

- **Proxy staleness** — the observable the negative watches is not one the
  positive path actually produces. A "nothing happened" proxy that is equally
  true on the success path pins nothing at all: a hook asserted not to write a
  settings file that its own design forbids writing in either branch, a marker
  no branch creates. The proxy never discriminated, so no change anywhere can
  fail it. Pick the observable from what the feature emits when it *does* fire —
  the config keys it sets, the files it installs, the bytes on its output
  channel — and assert their absence.

## A fall-through gate is tested by latency

The gate buys **latency**, so latency is the assertion: with the condition held
false, the action must be delayed by roughly the timeout, and removing the gate
collapses that gap to zero.

Read what the gate does when its condition never becomes true before writing the
test. Falls through ⟹ assert the delay. Aborts or records a failure ⟹ assert
*that*. Only a gate that blocks forever is tested by absence, and one of those
is usually a bug.

## Ordering under errexit

Few grouped positives license many negatives: one positive over a fixture pins
the strings and proves the path, and each negative flips a single condition
against it. That licenses the *coverage*, not the evidence.

A test body runs under errexit, so the grouped positive aborts the test the
moment it fails and every negative after it is never reached: a negative sitting
behind a positive runs only in the case where the positive already held.
**Give each negative its own test body, or place it ahead of the positive**, so
its result is its own.

## Where the absent string is a variant of the present one, assert the block

A prefixed twin of an unprefixed line, or the superseded wording of a line whose
new wording is asserted: no single fault produces both, so the negative restates
the positive and nothing can fail it alone.

An **exact-block equality** — the file's whole bullet region, in order — has no
absent string to go stale, and a dropped line, a stray duplicate, a reorder and
a wording drift each fail it.

Same move for "this file was not written at all": byte-compare against a copy
taken before the pass, rather than grepping for the mark a write would have
left. A write that reordered without leaving the mark is just as much a write.

## Put the decoy first

Where a fallback can supply the same answer as the rule, order the fixture so it
cannot. A preference implemented as "use the matching entry, else the first one"
is not pinned by input whose first entry is the matching one: deleting the
preference leaves the test green. Put the decoy first.

Same shape as the pairing rule below, one level in: the fixture has to make the
two implementations disagree, not merely exercise both.

## A pairing is a property of the fixture, not of the comment above it

A negative whose fixture differs from its positive in more than the guard's
trigger input is unpaired however confidently the comment claims otherwise: it
can bail out earlier, on a condition neither test names, and pass with the guard
deleted.

The tell is a fixture assembled for convenience — reusing the positive's setup
and moving the *subject* rather than the trigger. Building one that reaches the
guard often means constructing the odd layout the guard actually defends
against, which is also the fastest way to find out whether the guard is
load-bearing at all, or what its real justification is.

Where a feature writes to two channels, pin each independently: dropping one
must fail its own assertion and leave the other's green, or the two are not
separately pinned.

## A mutation the test survives has two readings

The reflex is to rebuild the test, but
**the code's reading is the one to check first**. A guard whose deletion changes
nothing observable is a guard doing nothing — usually because a broader one
beside it already covers the case, the way a bounded walk's depth limit covers a
self-parent check. Delete the guard and pin the guarantee that is actually
load-bearing. Its comment goes with it: a comment claiming the reason the line
did not serve survives the line unless the same pass cuts both.

Both readings assume the mutation landed. A recipe recorded against an earlier
version of the subject can miss the behaviour it once neutered, and a survived
mutation then says nothing about the code or the test; `genuine-red` has the
check.

## Delete an untestable negative whole

Where a negative genuinely cannot fail — it refutes wording no producer emits at
all, so the property is untestable by design — delete the whole test rather than
trimming it back to its testable residue. A title stating an untestable claim is
the thing to cut; keeping the assertions that survive leaves a test whose name
no longer describes it.

A negative refuting a **third-party** tool's message (git's "embedded git
repository" advice, a compiler warning) still pairs: run that tool's producing
path directly over the same fixture, so one assertion proves the message is
still live in this version and reaches this store, while the other proves the
local code avoids it.
