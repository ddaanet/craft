---
name: removing-cleanly
description: "Cut a capability in one pass — helpers, constants, fixtures, absence-guards, docs and inbound references — and fix forward instead of branching for a transition in tooling you also control. Use when removing a feature, retiring a file, deleting a module, or handling a version transition in your own tooling. Not for migrations at a boundary with users you do not control, which need real migration handling."
---

# Removing cleanly

When cutting a capability, **cut all of it in the same pass**. Do not leave
behind:

- tests that assert the *absence* of the removed behavior ("test that it's not
  what it used to be");
- fixtures or sentinel data that stood for the removed inputs;
- a now-trivial script preserved as its own file or subprocess. A module
  collapsed to a few lines gets inlined into its single caller, not kept as a
  hollow shell.

Half-removals force the reader to reconstruct what is live and what is
vestigial, and absence-guards grow stale defending behavior nobody will re-add —
pure noise. If a design "proved harmful", the cleanup is total, not a museum of
guards against its return.

**How to apply:** after removing a feature, grep for its whole machinery —
helpers, constants, fixtures, tests, docs, recipes, and inbound references — and
cut each. Convert any absence-guard into the positive contract of what remains.

**A grep for the name misses every figure derived from it.** "Eleven checks",
"thirty tests", a file total: none contains the removed thing's name, so each
survives the sweep and goes stale on the commit that lands. Grep for the number
words and numerals the removal changes, and re-derive each from its source —
collect the suite, count the list — rather than decrementing, since a removal
rewrites some dependents and deletes others. Measured: removing one check from a
checker came back clean on a grep for its name while a design doc still claimed
the suite's old test count.

Retiring a durable note is the same pass: `rm` leaves every surviving link to it
pointing at content nobody will write, so sweep the corpus for inbound links
too. **Where the link carried meaning, restate the rule inline rather than
dropping the sentence** — measured: retiring 24 files cost 40 such rewrites
across 30 survivors.

This shares the spirit of refusing compatibility shims, and the
`design-doc-writing` skill covers the docs analogue — rewiring an entry whose
component no longer exists rather than deleting the decision with it.

## No transition special cases

Do not add a branch, fallback, or diagnostic narrative that exists only to cover
a transition between versions of tooling you **also control** — a plugin update
that has not re-pinned its config key, an old on-disk layout, a half-migrated
path. Fix forward instead.

With a user base of one, the transition window is a single restart. The branch
outlives the case it covers, and its explanatory prose is wrong the moment the
transition ends. Same instinct as refusing compat aliases: carrying the old
state costs more than patching through.

When a message or code path starts enumerating causes — "installed before this
session / updated since / the pinned path moved" —
**collapse it to one fact plus one recovery act.**

Reserve real migration handling for boundaries with users you do not control.
Read-only *liveness* detection of a foreign tool's state is a different thing
and still applies: probing whether that tool is currently running, and acting on
the answer, is not a transition branch.
