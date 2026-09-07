# Classification — craft-seed

Source: `brief-craft-seed.md` (2026-09-02)

## Requirements clarity

- **Requirements source:** brief-craft-seed.md
- **Completeness:** Each FR has concrete mechanism: Y (five named skills,
  enumerated source facts, `SKILL.md` + `references/` shape, description form,
  link-resolution list). Each NFR has measurable criterion: partial — "keep
  descriptions tight" has no stated byte budget; every other constraint is
  checkable.
- **Routing:** Proceed to triage.

## Multi-item decomposition

Implicit bundling: the brief enumerates five skills. Enumerated, with a per-item
behavioral code check:

| item | behavioral code? | destination |
| ---- | ---------------- | ----------- |
| design-doc writing | No — markdown only | agentic-prose |
| plan and spec writing | No | agentic-prose |
| test discipline | No | agentic-prose |
| directive writing | No | agentic-prose |
| tooling-change hygiene | No | agentic-prose |

No item adds a function, a logic path or a conditional branch; no item elevates.
Homogeneous in kind, destination and complexity, so they batch into one routing.

## Classification

- **Classification:** Moderate
- **Implementation certainty:** High for structure — the plugin shape is settled
  (`skills/<name>/SKILL.md` auto-discovery, hub + `references/` progressive
  disclosure, prior art in `shell-scripting:shell-gotchas`), and the release
  path is already vendored at `plugin-dev/`. Moderate for content — routing 20
  facts and ~74.8KB of body into five hubs is judgment per fact, not per
  architecture.
- **Requirement stability:** High — scope is closed at 20 named source files,
  and the brief states its exclusions (no source-fact edits, no cross-repo
  writes).
- **Behavioral code check:** No. Markdown skill bodies only; no hooks, no
  scripts, no manifest logic.
- **Work type:** Production — the plugin delivers capability to every session
  that enables it.
- **Artifact destination:** agentic-prose (`skills/`) — quality obligations are
  wording quality and behavioral verification, not tests and lint.
- **Evidence:** Sizes verified against the store rather than taken from the
  brief (`design-doc-writing` 18,635 B, `green-is-not-evidence` 15,190 B,
  `directive-states-acts` 6,099 B, `hook-output-channels` 17,646 B with a real
  §7 "Wording"; the five clusters total 28.1 / 12.6 / 23.7 / 6.1+§7 / 4.3 KB,
  matching the brief). Triage recall returned `skill-description-purpose-first`
  (description form and the per-session cost of its length),
  `directive-states-acts` (distributed text never cites a memory file — both a
  source fact and a constraint on every body written here),
  `imperative-form-scope` (classify each `you` hit before rewriting),
  `stale-plugin-code` (a skill body is snapshotted at session start;
  `/reload-plugins` before believing any in-session verification),
  `gitlore-tier-index-budget` (the cutoff the brief's secondary motive rests on,
  and gitlore-specific, so it cannot ship verbatim in a distributed body).

## Author-corrector coupling

Author change: none — no edify author skill or artifact format is modified.
Coupled corrector: n/a. Update needed: no.
