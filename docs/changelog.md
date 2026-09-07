# Changelog

Design-significant changes only: decisions reversed, subsystems built or torn
down, requirements added or dropped, a rationale that turned out false. Git
history is already the full changelog and needs no duplicate here. An entry
earns its place by answering a question a future reader would otherwise ask of
[the design](design.md) and find no answer to.

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
