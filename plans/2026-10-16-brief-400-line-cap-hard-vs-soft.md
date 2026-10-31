# Brief: state where the 400-line cap is hard and where it is soft

2026-10-16, from a claude-plugin-dev session.

`skills/plan-contracts/references/contracts-and-size.md` opens by calling the
400-line cap on "plans, PRs" a **soft** guideline, not a hard gate. My human
partner's ruling: the cap is
**soft for plans, hard for design docs and implementation**.

The shared ddaanet conventions (`memory/ddaanet/shared-claude.md`, "400 lines
caps any artifact…") now say the same and point at `craft:plan-contracts` for
the full argument, so the skill should agree with them.

What needs deciding in craft:

- Plans: already soft here; matches.
- Design docs and source files: not named by the opening paragraph; state the
  hard cap and why (context management — a file reaching it holds content to
  spin off; split along that seam, never cram or shave prose).
- PRs: this file calls them soft. If a PR counts as implementation, it is hard
  under the ruling. Confirm with my human partner before changing it.

claude-plugin-dev enforces the hard cap mechanically: `tests/line-cap-test.sh`
fails the gate on any tracked file over 400 lines once rumdl has reflowed the
markdown to 80 columns.
