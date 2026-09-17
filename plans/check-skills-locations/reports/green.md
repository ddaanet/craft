# GREEN — change 2: line numbers on locatable checks

Slice: item 2 (line-number contract), GREEN dispatch. `uv run pytest` could not
acquire its lock in the sandbox; ran with `python3 -m pytest` instead, per the
fallback the RED report already used.

## What changed (`scripts/check-skills.py`)

- Added `line_of(text: str, index: int) -> int`, placed right after
  `blank_code`: `1 + text.count("\n", 0, index)`. Docstring states the
  dependency — `blank_code` substitutes rather than deletes, so an index into
  the blanked prose is an index into the raw text.
- `check_body`'s `wikilink`, `private-reference` and `broken-link` now emit
  `f"{path}:{line}: {check}: {token}"`, one failure per occurrence, each found
  by `finditer` over the blanked prose (`WIKILINK.finditer`, `re.finditer` over
  `re.escape(pattern)` for the two literal patterns and each `{slug}.md`,
  `LINK.finditer`). Check order unchanged: wikilink, then `memory/`,
  `MEMORY.md`, source facts sorted, then links. Existing skip rules for links
  (`://`, `#`-anchors) unchanged.
- Added a comment above the literal private-reference patterns recording that
  none contains a space, so a formatter reflow cannot split one across lines.
- Fixed the `SOURCE_FACTS` comment: replaced the false "Every one is gone from
  the store" with a statement that a body naming one of these files is private
  to a reader who lacks the store, without resting on their absence
  (`hook-output-channels` is still indexed there).
- Module docstring: unchanged. It does not describe the per-check output format
  (that's implicit in each check's own `f"{path}: ..."` string), so nothing in
  it misdescribes the new `path:line:` format.

No test file touched.

## Tests made to pass, one at a time

Ran each of the 9 red tests individually (`pytest -k <name>`) after each
implementation step, in this order, confirming each passes before moving to the
next:

1. `test_wikilink` — after adding `line_of` and switching `wikilink` to
   `finditer` + `line_of`.
2. `test_private_reference_to_the_store`
3. `test_private_reference_to_the_index`
4. `test_private_reference_to_a_retired_source_fact` — 2-4 after switching the
   two literal patterns and the `SOURCE_FACTS` loop to `re.finditer` +
   `line_of`.
5. `test_private_reference_reports_every_occurrence` — same change; confirms
   per-occurrence reporting (was per-pattern-`in`-check before).
6. `test_broken_link` — after switching the link loop to `LINK.finditer` +
   `line_of`.
7. `test_blanking_code_does_not_hide_prose_on_the_same_line`
8. `test_blanking_a_fence_keeps_lines_below_it_at_their_raw_line` — the L-1
   seam: confirms `line_of` reads the blanked prose's offsets as raw-text line
   numbers (fence substituted, not deleted).
9. `test_every_failure_is_reported_not_just_the_first` — confirms
   `name-mismatch` (frontmatter) keeps `{path}: {check}: …` while `wikilink`
   (body) gains `:8:`.

## Full suite

`cd /Users/david/code/craft && python3 -m pytest tests/test_check_skills.py -q`

```
31 passed in 2.52s
```

All 22 previously-passing tests remain green, including
`test_the_real_tree_passes`; all 9 previously-red tests now pass.

## `just precommit`

No `just lint` recipe exists in this repo (`just --list` confirmed); ran
`just precommit` directly, exit code 0.

Closing lines:

```
check-skills: 18 files, all checks passed
...............................                                          [100%]
31 passed in 2.42s
jq: plugin.json parses
shellcheck: .bin/claude clean
```

`just precommit`'s `format-docs`/rumdl pass reflowed
`plans/check-skills-locations/reports/red.md` (a pre-existing report, not
touched by this dispatch's implementation work) on its first run; a second run
still reports 9 MD013 line-length issues in that file as informational findings,
without affecting the exit code (0 both times). Not acted on here — out of scope
for this dispatch (report content, not `scripts/`, `tests/test_check_skills.py`,
or `docs/`).

## No regressions, no warnings needing report

Precommit's other gates (`check-skills`, pytest, `jq`, `shellcheck`) all passed
clean on the first pass with no complexity/line-limit warnings against
`scripts/check-skills.py` to carry forward to review.

## Not committed

Per the dispatch prompt, no commit made — the orchestrating session commits this
slice together with a doc change. `git status --porcelain` at the end of this
dispatch:

```
 M docs/design.md
 M scripts/check-skills.py
 M tests/test_check_skills.py
?? plans/check-skills-locations/reports/
```

`docs/design.md`'s modification (closing L-1, change 3 of the outline) was
already present before this dispatch started and was not touched by it — this
dispatch edited only `scripts/check-skills.py`.
