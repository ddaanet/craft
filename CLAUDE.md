@memory/ddaanet/shared-claude.md

# craft

A Claude Code plugin of guidance skills. Each skill is a `SKILL.md` hub with
opt-in `references/` nodes; `scripts/check-skills.py` caps the hub at 200 lines
and a node at 400, and runs in `just precommit` behind a rumdl reflow pass.

Prospective content this repo wrote for itself — plans, specs, briefs — goes in
`plans/`. A brief arriving from a session in *another* repository goes in
`inbox/`, never the repo root, where it reads as a tracked project document.
See `inbox/README.md`.
