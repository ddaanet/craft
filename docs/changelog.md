# Changelog

Design-significant changes only: decisions reversed, subsystems built or torn
down, requirements added or dropped, a rationale that turned out false. Git
history is already the full changelog and needs no duplicate here. An entry
earns its place by answering a question a future reader would otherwise ask of
[the design](design.md) and find no answer to.

## 2026-09-08 — dogfooding `test-discipline` fed a gap back into it

Writing the checker's suite was the skill's first run against live work, and it
found the skill covering only half its own subject. `genuine-red` prescribed
stub-then-assert, which presumes the code does not exist yet, and noted in
passing that a suite validated against a finished implementation "has to
manufacture the absence the ordering would have given" — without saying how.
Everything the suite actually needed was in that unwritten half: one mutation
per behaviour, the whole suite run against each, and the three distinct things a
surviving or misdirected red tells you.

Added there rather than to the hub, and phrased to lean on the existing
mutate-in-place rule instead of restating it. The exactness requirement travels
with it: a test asserting only that the run failed survives the mutation of its
own check whenever the fixture trips a second one, which is why the suite
asserts complete output.

## 2026-09-07 — the checker gets a suite, and the gate stops being sub-second

L-1 was the last thing the design doc named as unpinned: eleven checks gating
every requirement, and nothing showing that any of them would fail if it
regressed. The suite closes it with one test per check, each spoiling an
otherwise-clean tree in exactly one way and asserting the *complete* output
rather than the exit code — a test that only asserted "something failed" would
pass just as well when a different check fired on an accidental second defect.

Thirty tests, all green the first time they ran, which is no evidence at all
that they discriminate. A mutation pass supplied the missing red: each check was
neutered in turn in a copy of the checker, and every one of the thirteen
mutations turned the test named for it red. No mutation survived.

The suite runs in `precommit`, which takes the gate from well under a second to
around six. NFR-3 was rewritten rather than quietly left standing: the property
that lets the gate be unconditional is that it has no cache and no sentinel, and
a sub-second figure was never what bought that. The cost is thirty subprocess
spawns, which is the price of running the checker the way `precommit` runs it
instead of importing its functions.

L-1 is now a different limitation. `blank_code` substitutes spaces for code
rather than deleting it, so that a failure message would name the right line —
but no check reports a line number, and the one line-derived figure counts the
raw text. Nothing can tell the implementation apart from one that deletes. The
behaviour stays; what is missing is the seam that would let a test see it.

## 2026-09-07 — the living design doc, and the gate widened to cover it

Craft shipped `design-doc-writing` and had no `docs/design.md`. Writing one from
the skill was the first real dogfooding pass, and it found two gaps in the
plugin's own tooling: `just format-docs` wrapped `skills` and `plans` but not
`docs`, and `scripts/check-skills.py` capped skill bodies but nothing else. A
design doc that is neither wrapped nor capped cannot obey the rule its own skill
states, so both were widened (D-9).

Every requirement is pinned by `just precommit` rather than by a unit test, and
that is what a pin is for: the gate re-checks the claim on every commit, which
is the property that makes a `Done` more than an assertion. What stays unpinned
is the checker itself, which has no test suite, so nothing shows a check would
fail if it regressed (L-1).

## 2026-09-07 — two inbound briefs applied to `design-doc-writing`

FR and NFR rows were named as an example of genuinely tabular data. They are
not: a requirement stated as a sentence is neither short nor uniform, which is
the test the section already gave. The error had two carriers — the
prose-over-tables rule and the state layer's `Where · pinned by` item, which
prescribed a *column* — and fixing one alone left the skill contradicting
itself. The requirement sections in this design doc are the corrected form.

The same pass added the decisions index to the levers available at a hub's
floor: the `## Design Decisions` heading is a need-time seam, so the conclusions
can move whole into a `docs/decisions.md` while the hub keeps its six sections
as pointer stubs. Recorded as a lever rather than a default shape, because it
does not pay the way other splits do — nobody skips a decisions index, so the
saving is in *when* it is read, not whether.

`inbox/` became a tracked directory in the same commit, and
`brief-craft-seed.md` moved off the repo root where it read as a tracked project
document (D-8).

## 2026-09-07 — five skills seeded, twenty memory facts retired

The plugin's reason to exist: guidance that a private memory store already
encoded but structurally could not deliver. A memory fact is retrieved by
matching an index line against a symptom, which never fires on a *moment* — "you
are about to write a design doc" routes to nothing. A skill description names
the moment.

Twenty source facts were rewritten into five skills and deleted from the store
in the same pass, so there is no second copy to drift. Their names survive in
`SOURCE_FACTS` in the checker, where a surviving mention in a shipped body is
now a dangling private reference rather than a citation (D-4).

`scripts/check-skills.py` and the rumdl reflow pass were built alongside, for a
failure mode that is leakage rather than breakage: a wikilink or a `memory/`
path does not stop a skill loading, so nothing but a gate reports it.

## 2026-09-02 — plugin stubbed and the release toolkit vendored

`.claude-plugin/plugin.json`, the justfile, and `plugin-dev/` pulled in as a git
subtree from a pinned `dist-` tag. Vendoring rather than depending: the release
recipe has to work in a repo that has never been released, which a runtime
dependency resolved from a marketplace cannot guarantee.
