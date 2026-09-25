## Current task

Triaging craft's inbox one group at a time, grouped by the skill node each brief targets, so only one topic is open at once. The test-discipline, removing-cleanly and plan-contracts groups have landed; directive-writing is next. Per group: read every brief critically against the shipped node, present per-item rulings with defaults, then edit, run `just precommit`, add a changelog entry, move each spent brief to `plans/<its own dateline>-<name>.md`, and commit. A brief spanning groups moves only when its last section is spent.
