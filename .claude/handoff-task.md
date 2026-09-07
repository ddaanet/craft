## Current task

Moving craft toward its first release. The living design doc and changelog now exist at `docs/`, the formatter and `scripts/check-skills.py` were widened to cover them, and the three inbound briefs have been ruled on, applied and archived into `plans/` under their own datelines.

What is left before a release is readiness rather than authoring. `just release` and the `ddaanet/claude-plugins` marketplace entry have never been run from this repo; `plugin-dev/release.just` needs `MARKETPLACE_DIR` set and skips its version check non-fatally without it. `ddaa:preflight` aborts on a dirty memory submodule, which is the resting state here — ` M memory` is not a finding, other dirty paths still are.
