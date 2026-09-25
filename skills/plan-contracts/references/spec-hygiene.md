# Spec hygiene

When a design hand-enumerates the sites a change must touch ("eight files carry
this paragraph"), **re-derive that list mechanically at review time**, before
checking conformance.

Conformance and completeness are different questions, and a hand-written
enumeration answers only the first. Measured instance: a rewire whose spec
listed 8 call sites passed conformance exactly — every listed file changed,
nothing outside touched — while a grep at review found 15. The 7 unlisted sites
kept both the duplication the change existed to remove and the dependency it
existed to drop. Every review layer above the grep was blind to this: the
implementer matched the spec, and the spec was the thing that was wrong.

**Grep for the pattern the change replaces, not for the files the spec names.**
Do it before reading any of them, so the spec's list cannot anchor the search.

A count that disagrees with the spec is a finding **against the spec**, filed as
completeness rather than conformance — the delivered work is not at fault, and
re-reviewing it will not surface the gap.

The same split applies to a phrase that is quietly a claim about the corpus:
"the only place X appears", "these are the N consumers". Treat each as a query
to run, not a fact to carry forward.

A claim that two passages are the same is one of these, and the query is `diff`.
A dedup is the one edit whose premise is that reading one copy tells you what
the other says, which is exactly when nobody reads the other.
**Diff the passages before treating them as copies, and state what came back**,
even when it is "byte identical". Classify each difference as wording or
substance: a substantive one becomes a declared decision with a rationale, never
a side effect of which copy survived. Then scope the replacement to the
duplicated **block** by its line range, and name what in the enclosing section
stays. Measured instance: an outline proposing to collapse two copies of a
routing block asserted they "state the same decision" and scoped the change as
"the section, replaced by a pointer". The copies routed the same input
differently, and the enclosing section also decided whether an outline sufficed
— a question the pointer would have deleted. A reviewer who diffed found both;
the author, who had read each copy for plausibility, found neither.

## A contract line is source text

The same blindness runs one step further down. The implementer copies a contract
sentence into the docstring, close to verbatim, because that is the most
faithful thing to do with a contract someone else settled. Code review then
reads the code *against* that docstring, so a wrong sentence changes medium
without anyone re-examining it, and nothing in the reviewer's stance points at
it.

**Whoever enumerates the cases checks the sentence against them** — the
implementer before copying it, the reviewer before signing off on a case table.
Measured instance: a review tabulated, case by case, the exception that
falsified the docstring sentence three lines above its own table, and closed
clean. Each case conformed to the code, the code conformed to the sentence, and
the sentence was wrong about the set of cases.
