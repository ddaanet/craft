# Brief: the size cap moves from lines to non-whitespace bytes

2026-10-31, from a claude-plugin-dev session. A proposal, not a decision: what
changes in craft is craft's call, after a ruling from my human partner.

## What changed in the toolkit, and why

The [claude-plugin-dev toolkit](https://github.com/ddaanet/claude-plugin-dev) is
shipping a size check to every consumer, `toolkit/check-size.sh`, wrapped by a
`check-size` recipe in `release.just`. Consumers wire it as
`precommit: check-refs check-size`. The design is
`plans/2026-10-31-line-cap-gate/design.md` in that repo, with its three evidence
reports in `reports/` beside it. Both are uncommitted at the time of writing, so
the path is given rather than a link.

My human partner decided:

- **Metric:** a file's byte count after deleting `[ \t\n\r\f\v]`, under
  `LC_ALL=C`. On 131 files from 14 repos (tokens counted with
  `edify tokens --model opus`), the median error of a proportional fit to tokens
  is 13.3% for lines and 8.7% for this metric. Plain bytes fit slightly better,
  but they charge for indentation and move with every re-wrap. Non-whitespace
  bytes move by at most 1–2 characters per wrapped line, so
  **the count no longer needs a reflow formatter run ahead of it**.
- **Caps:** 20000 for every counted file, 10000 for any `SKILL.md`. That is
  about 400 and 200 wrapped lines of prose (400 × ~51 non-whitespace bytes per
  line, rounded down), and about 10k and 5k tokens. Neither is configurable.
- **Scope:** every file git does not ignore, minus symlinks, non-regular files,
  unreadable files, binaries, `plugin-dev/`, root `plans/`, `uv.lock` and
  `package-lock.json`, and a root `size.exempt` whose entries carry a mandatory
  reason and are refused once stale. `docs/changelog/` counts.
- **Report:** `oversized-file: <path>: <n> non-whitespace bytes > <cap>`, with a
  hint to split along a seam and never to shave prose.

craft passes both caps today: no file over 20000, and its largest hub is about
7.5k. Adopting the check costs craft no split and no exemption, and its
`uv.lock` is skipped by default.

The shared ddaanet rule ("400 lines caps any artifact…") is reworded when the
gate ships, not before. Its proposed text keeps hard for design docs and
implementation, soft for plans, the ban on shaving prose, and the pointer to
`craft:plan-contracts`, and replaces the line counts and the "wire a
hard-wrapping formatter ahead of the checker" sentence.

## How this relates to brief-400-line-cap-hard-vs-soft.md

That brief, still in this inbox, asks for the hard/soft split to be stated: soft
for plans, hard for design docs and implementation. This brief leaves that
ruling as it is and changes only the unit and the way it is measured. The
toolkit's root `plans/` skip is how "soft for plans" shows up mechanically.

Two points of contact:

- Its last paragraph says `tests/line-cap-test.sh` enforces the cap after a
  rumdl reflow. That becomes false when the gate ships: the suite retires, and
  the count needs no reflow.
- Both briefs rewrite the opening of `contracts-and-size.md` (lines 5–16).
  Triaging them together avoids rewriting it twice. Its open question about PRs,
  and the "do not block a commit" sentence (5–7), are left where that brief left
  them.

## Places in craft that would need rewording

`skills/plan-contracts/`:

- `SKILL.md`, the `description` ("a line-count cap on a plan, PR or source
  file") and line 32 ("it is what a line cap actually measures"): "size cap".
  The hub's bullet for `contracts-and-size.md` says "how to measure a line cap
  honestly"; it becomes "how to measure a size cap".
- `references/contracts-and-size.md`:
  - 5–16, "Contract size predicts implementation size": restate the cap as a
    size, not a line count. The 3.5× contract-to-implementation ratio was
    measured in lines, so it stays a line figure, labelled as one, or is
    measured again.
  - 36–62, "Measure the cap honestly": wrapping first stops being a counting
    step, since a reflow does not move the count; `check-size` replaces `wc -l`.
    The normalize-mode paragraph (44–53) stops bearing on the cap. It survives
    only as advice on rumdl, if craft wants it here at all. Splitting on a seam
    and preserving information across the split stand as written.
  - 77, the measured instance "498 lines against a 400 cap": a dated line
    measurement, accurate as stated. Keep it labelled in lines.
  - 98–118, "The three forms of cramming": long lines no longer game the count,
    so the first form turns from a counting rule into a reading rule (a
    300-character line is still unreviewable). Run-on paragraphs and shaving
    docstrings still apply. The 389→406→400 instance (106–118) is a line
    measurement and stays one.
  - 127, "~40 lines over 400": dated, keep in lines.
- `references/code-in-a-plan.md:53`, "the ~400-line contract intact as the split
  signal": either keep it as a line heuristic for contracts, or restate it as "a
  contract near the size cap".

`scripts/check-skills.py`:

- The module docstring (lines 10–14) and the comment at 48–51 say both caps
  count lines after `just format-docs` has wrapped, and that "an unwrapped file
  games any cap". Under the new metric neither holds.
- `MAX_HUB_LINES = 200` and `MAX_NODE_LINES = 400` (52–53), with the counts at
  181–183 and 212–214, which report `<path>: oversized-file: <n> lines > <cap>`.
  Either convert them to 10000 and 20000 non-whitespace bytes, in the toolkit's
  report format, or retire this half of the script and let `check-size` cover
  `skills/`, `scripts/`, `tests/` and `docs/` (it scans all of them). The
  toolkit's migration note will list `check-skills.py` among the checkers that
  can drop their size half. `MAX_DESCRIPTION_BYTES` is a different cap and is
  not affected.

Elsewhere, restating the same rule:

- `docs/design.md` FR-5 (line 45, "line caps are enforced against wrapped
  prose", pinned by `format-docs` running first), and lines 3 and 144 (the "do
  not re-litigate the 200/400 line caps" note and D-1): the hub-to-node ratio of
  one half survives, the unit does not.
- `CLAUDE.md` 6–7 and `README.md` 71–73 ("caps the hub at 200 lines and a node
  at 400").
- `skills/design-doc-writing/references/splitting-an-oversized-doc.md:128`: "a
  formatter that hard-wraps the prose so a line count means something".

gitlore's D55 makes the parallel argument ("lines are exact, free and
reproducible"), which holds equally for non-whitespace bytes; it reaches gitlore
through the toolkit's migration note, not through craft.
