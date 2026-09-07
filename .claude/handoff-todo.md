## Open decisions

- The two briefs in `inbox/` are unread: `brief-decisions-index-is-the-hubs-last-seam.md` (arrived 2026-09-07) and `brief-fr-nfr-not-tabular.md` (2026-09-07), both proposing changes to `skills/design-doc-writing/`. A brief's recommendation is input, not a decision — read each, verify its stated constraints against the shipped skill rather than against the brief's own framing, and get a ruling before editing.
- `.claude-plugin/plugin.json` still carries the stub `description` from the manifest stub commit. It ships verbatim to the marketplace row, so it needs writing before any release; the seed plan explicitly left it uncovered.
- Whether `inbox/` is versioned in this repo or stays local scratch. It was deliberately left out of the seed commit as briefs for other work.

## Remaining

- Dogfood the five skills on real work. Nothing has invoked them since they were written, so no trigger phrasing or reference-node split has been tested against a live task.
- `just release` plus the `ddaanet/claude-plugins` marketplace entry, which the seed plan put out of scope as a separate later step.
