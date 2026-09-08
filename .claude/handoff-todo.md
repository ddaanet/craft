## Open decisions

- Whether to open a seam in `scripts/check-skills.py` that makes `blank_code`'s line preservation observable. It substitutes spaces for code rather than deleting, so a failure message would name the right line — but no check reports a line number, and the one line-derived figure (`oversized-file`) counts the raw text, so no test can tell it from an implementation that deletes. Carried as L-1 in `docs/design.md`. The forks are: give some check a line number so a test can see it, or leave the behaviour unpinned and keep saying so.

## Remaining

- Dogfood `craft:plan-contracts` against a real plan or spec.
- Dogfood `craft:directive-writing` against real agent-facing output — a hook's additionalContext, a deny reason, an instructing error message.
- Dogfood `craft:removing-cleanly` against a real removal.
