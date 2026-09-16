## Remaining

- Change 1 of `plans/check-skills-locations/outline.md`: remove `attribution` across the checker, tests, design doc (FR-4, a new decision, the check count), changelog and README, then verify with a whole-tree grep.
- Change 2: line numbers plus per-occurrence `private-reference`, test-first; fix the `SOURCE_FACTS` comment.
- Change 3: delete L-1, renumber the remaining limitations, re-derive NFR-3's test count.
- Once the plan lands, record in `docs/design.md` Now/Next what dogfooding `plan-contracts` and `removing-cleanly` showed.
- Dogfood `craft:directive-writing` against real agent-facing output — a hook's additionalContext, a deny reason, an instructing error message.
