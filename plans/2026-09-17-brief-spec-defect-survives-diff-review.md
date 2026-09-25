## Brief: the defect can be in the spec, which no diff review reaches

2026-09-17

Touches two skills: `plan-contracts` (the `Interfaces:` block) and
`directive-writing` (what a dispatching agent reviews on the way back). Arrived
from the `handoff` plugin repo, from two incidents in one job.

### The shared mechanism

Every artifact downstream of a contract is a faithful transformation of it. The
implementer writes the docstring from the `Interfaces:` line; the subagent
implements the semantics the directive states. Faithfulness is what makes
dispatch work — and it is exactly what stops the defect being caught, because
each diff conforms to its input and the input was wrong.

So a review of the returned diff confirms only what was never in doubt. The spec
has to be read **as a claim**, against the inputs it was written to handle, by
someone who has the full case set.

### Incident 1 — the contract reaches the docstring verbatim

`plan-contracts` says to write the `Interfaces:` block verbatim, and that is
right. What it does not say is that the block's lines are *source text*: the
implementer copies a contract sentence into the docstring, close to verbatim,
because that is the most faithful thing to do with a contract someone else
settled.

A self-contradicting contract line therefore ships as a self-contradicting
docstring, having changed medium without anyone re-examining it. It then
survives code review for a structural reason: a reviewer reads the code
*against* its docstring — the docstring is the statement of intent the code is
checked for conformance to. Nothing in that stance points at the docstring.

Observed: a review tabulated, case by case, the exception that falsified the
contract sentence three lines above its own table, and closed clean. Each case
conformed to the code, the code conformed to the sentence, and the sentence was
wrong about the set of cases.

Suggested for `plan-contracts`: one line saying a contract must be readable as a
standalone proposition and checked for a counterexample before it is written,
and one for the implementing side — do not copy a contract into a docstring
without first checking it against the cases you are about to write. The
one-contract-per-line rule already makes this possible; it just does not ask for
it.

### Incident 2 — reviewing the agent's diff instead of your own spec

A dispatch specified `line.strip()` before an emptiness test on markdown lines.
The subagent implemented it exactly. The spec was wrong: stripping closes both
filed defect routes and re-opens the second one indent along, because four
leading spaces open a markdown code block, so

```
    # run the migration first
```

is content, and a strip-first rule reads it as a heading and removes the file.
Reviewing the returned diff found nothing, correctly.

Suggested for `directive-writing`: write the failure class into the brief in
terms of **inputs**, not in terms of the rule that handles them. The agent can
then test the rule against the class rather than only implementing it, and the
dispatcher has something to check the returned rule against.

### The general form, worth more than either instance

**Tightening a predicate along one axis can re-open the same defect one step
further along that axis.** A guard that was too loose gets narrowed, and the
narrowing is expressed as a normalization — strip, lowercase, canonicalize,
resolve — that erases the distinction the original defect turned on. The new
predicate is correct on every input that motivated it and wrong just past them.

Two practices follow:

- Run a returned rule against inputs one step beyond the filed cases: one more
  indent, one more nesting level, one character past the boundary.
- Pin the boundary from **both** sides in the suite. A row saying "three spaces
  is a heading" does not stop a later strip-first rewrite; the row saying "four
  spaces is content" does.

This has no obvious skill home — it is a code lesson rather than a planning or
dispatch one. Offered for wherever it fits, including nowhere.

### Additional context

Both incidents came from one job in the `handoff` plugin; the fix and its
reasoning are recorded there in
`docs/changelog/2026-09-14-a-heading-is-not-a-leading-hash.md`. No change is
proposed to that repo.
