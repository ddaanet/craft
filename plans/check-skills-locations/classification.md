# Classification — check-skills-locations

Two items, classified individually.

## Item A — line numbers on locatable checks

- **Classification:** Moderate
- **Implementation certainty:** High — `finditer` plus a line-offset helper
- **Requirement stability:** High — per-occurrence reporting decided in the
  outline
- **Behavioral code check:** Yes — new helper, three changed logic paths
- **Work type:** Production
- **Artifact destination:** production (`scripts/`, `tests/`)

## Item B — remove the `attribution` check

- **Classification:** Simple — a removal with enumerated call sites
- **Implementation certainty:** High — every reference found by whole-tree grep
- **Requirement stability:** High — my human partner ruled on 2026-09-16 that
  "my human partner" is house policy; the check enforced the opposite
- **Behavioral code check:** Yes — a check stops firing
- **Work type:** Production
- **Artifact destination:** production (`scripts/`, `tests/`) and docs
- **History:** first classified as a Defect (a reflow split disarms the
  substring match). Superseded by the policy ruling: the check is removed rather
  than hardened.
