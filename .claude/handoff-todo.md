## Open decisions

- Whether the first release waits on a test suite for `scripts/check-skills.py` (recorded as L-1 in `docs/design.md`, and the top item in its Now/Next). The checker gates every functional requirement but has no tests of its own, so nothing shows a check would fail if it regressed. Releasing first is defensible — the gate runs on the real tree every commit — but the doc currently promises the suite as the next thing.
- Whether the four skills not yet exercised (`plan-contracts`, `test-discipline`, `directive-writing`, `removing-cleanly`) get a dogfooding pass before the release. Only `design-doc-writing` has been run against live work; trigger phrasing and the reference-node splits of the other four are untested against a real task.

- Whether `craft:design-doc-writing`'s `references/state-layer.md` should widen its `Done` rung. The legend reads "`Done` — implemented and pinned by a test", which is what invited the `Done (gated)` detour: craft's own requirements are pinned by `just precommit` rather than by a suite. The ruling stands that a gate is a pin; open is whether the shipped wording should say so, on the strength of one instance. A memory fact for this was drafted and discarded at the commit gate — the skill owns the claim, so the store is the wrong home for it.

## Remaining

- Write the test suite for `scripts/check-skills.py` (L-1).
- Dogfood the four unexercised skills.
- Cut the first release: `just release` plus the `ddaanet/claude-plugins` marketplace entry, which the seed plan put out of scope as a separate step.
