# Brief: the size cap counts all bytes (supersedes the non-whitespace brief)

2026-10-31, from a claude-plugin-dev session. A proposal, not a decision: what
changes in craft is craft's call, after a ruling from my human partner.

This supersedes `2026-10-31-brief-size-cap-in-nonws-bytes.md`, whose metric was
reversed before release. That file can be deleted when this one is triaged.

## What shipped

The claude-plugin-dev toolkit v0.13.0 ships `toolkit/check-size.sh`, wired by
consumers as `precommit: check-refs check-size`.

- **Metric:** a file's size is its bytes as `wc -c` counts them, whitespace
  included.
- **Caps:** 20000, and 10000 for a `SKILL.md` at any depth. Unchanged from the
  earlier brief: about 10k and 5k tokens as the Read tool presents a file.
- **Scope and report:** root `plans/` is skipped; a root `size.exempt` lists
  files kept over on purpose, each with a reason. The report is
  `oversized-file: <path>: <n> bytes > <cap>`.
- **No reflow needed:** a re-wrap barely moves a byte count, so no formatter has
  to run ahead of it.

## Why the metric moved from non-whitespace bytes to all bytes

Bytes fit tokens as presented better than non-whitespace bytes do: 7.2% against
9.5% median error, with bytes winning 96% of bootstrap resamples. They also
charge for the newlines and indentation the agent pays for when it reads a file.
The earlier worry, that bytes move with every re-wrap, proved small in practice.

The argument is the design node, "The metric: all bytes":
<https://github.com/ddaanet/claude-plugin-dev/blob/v0.13.0/docs/references/size-check.md>
The consumer manual chapter:
<https://github.com/ddaanet/claude-plugin-dev/blob/v0.13.0/toolkit/manual/size-check.md>

## The shared ddaanet rule is reworded

The bullet in `memory/ddaanet/shared-claude.md`, under Code, now reads:

> - **20000 bytes caps any artifact a reader takes in at one go** — source
>   files, `references/` nodes, plans, design docs and PRs — and
>   **10000 a `SKILL.md` hub**, which is paid on every invocation while a node
>   is opt-in. Bytes as `wc -c` counts them, whitespace included: about 10k and
>   5k tokens as the Read tool presents a file. For design docs and
>   implementation the cap is *hard*; for plans it is soft. It exists for
>   context management, and a file that reaches it usually holds cohesive
>   content to spin off — find that seam rather than arguing the overage. Never
>   satisfy it quietly by shaving docstrings and prose — that is borrowing
>   against the split, and a file parked at exactly its cap has stopped emitting
>   the signal. A byte count barely moves on a re-wrap, so no formatter has to
>   run ahead of it. The plugin-dev toolkit ships the checker as `check-size`,
>   wired `precommit: check-refs check-size`, reporting
>   `oversized-file: <path>: <n> bytes > <cap>`; a root `size.exempt` names a
>   file kept over on purpose, with its reason. The full argument ships in
>   `craft:plan-contracts`.

`craft:plan-contracts`, which that bullet points at, still carries the
line-count wording. What to change there is craft's call. The places listed in
the superseded brief (the skill hub, `contracts-and-size.md`,
`code-in-a-plan.md`, `scripts/check-skills.py`, and the docs restating the rule)
apply as written, with "non-whitespace bytes" read as "bytes" and the report
format as above.

## Separate note: `design-doc-writing`

In claude-plugin-dev, cutting the design hub's decisions down to a floor was
rejected as a false gain. My human partner had the hub keep each decision's
one-line conclusion and move the rationale into `docs/references/` nodes
instead. See
<https://github.com/ddaanet/claude-plugin-dev/blob/v0.13.0/docs/design.md>.
Craft's `design-doc-writing` skill may want to say so where it discusses
splitting or trimming a hub.
