# RED — change 2: line numbers on locatable checks

Slice: item 2 (line-number contract), RED dispatch. `uv run pytest` could not
acquire its lock in the sandbox (`Read-only file system` writing to
`/Users/david/.cache/uv`); ran with `python3 -m pytest` instead, per the
fallback the dispatch prompt allows.

## Tests touched (expected string updated to `{path}:{line}: {check}: {token}`)

- `test_wikilink`
- `test_private_reference_to_the_store`
- `test_private_reference_to_the_index`
- `test_private_reference_to_a_retired_source_fact`
- `test_broken_link`
- `test_blanking_code_does_not_hide_prose_on_the_same_line`
- `test_every_failure_is_reported_not_just_the_first` — only the `wikilink` line
  gained `:8`; the `name-mismatch` line is unchanged (frontmatter checks keep
  `{path}: {check}: …`).

All line numbers are `8`, `hub()`'s single-line body position (frontmatter lines
1-4, blank line 5, `# {name}` line 6, blank line 7, body starts line 8), except
the new fence-seam test below.

## Tests added

- `test_private_reference_reports_every_occurrence` (beside the
  `private-reference` tests) — a body with `memory/` on two different lines
  (`"See memory/one.\nAlso memory/two."`, lines 8 and 9) expects two
  `private-reference: memory/` failures, each with its own line, in line order.
- `test_blanking_a_fence_keeps_lines_below_it_at_their_raw_line` (in the "code
  is a sample, not prose (FR-6)" section, after
  `test_blanking_code_does_not_hide_prose_on_the_same_line`) — a three-line
  fenced block (```` ``` ````, `code`, ```` ``` ````, lines 8-10) above a line
  holding `[[x]]` (line 11) expects `wikilink` reported at line 11. Docstring
  states a `blank_code` that deleted the fence instead of substituting spaces
  would report the wikilink three lines earlier (line 8).

## Run: `python3 -m pytest tests/test_check_skills.py -q`

9 failed, 22 passed.

Each changed/added test fails on its assertion (a mismatched output list), never
on `ImportError`/`AttributeError`:

- `test_wikilink` —
  `['skills/alpha/SKILL.md: wikilink: [[some-fact]]'] != ['skills/alpha/SKILL.md:8: wikilink: [[some-fact]]']`
- `test_private_reference_to_the_store` —
  `['skills/alpha/SKILL.md: private-reference: memory/'] != ['skills/alpha/SKILL.md:8: private-reference: memory/']`
- `test_private_reference_to_the_index` —
  `['skills/alpha/SKILL.md: private-reference: MEMORY.md'] != ['skills/alpha/SKILL.md:8: private-reference: MEMORY.md']`
- `test_private_reference_to_a_retired_source_fact` —
  `['skills/alpha/ SKILL.md: private-reference: outside-in-tdd.md'] != ['skills/alpha/ SKILL.md:8: private-reference: outside-in-tdd.md']`
- `test_private_reference_reports_every_occurrence` —
  `['skills/alpha/ SKILL.md: private-reference: memory/'] != ['skills/alpha/SKILL.md:8: private-reference: memory/', 'skills/alpha/SKILL.md:9: private-reference: memory/']`
  (today's `pattern in prose` fires once per pattern, not per occurrence)
- `test_broken_link` —
  `['skills/alpha/SKILL.md: broken-link: references/gone.md'] != ['skills/alpha/SKILL.md:8: broken-link: references/gone.md']`
- `test_blanking_code_does_not_hide_prose_on_the_same_line` —
  `['skills/ alpha/SKILL.md: wikilink: [[x]]'] != ['skills/alpha/SKILL.md:8: wikilink: [[x]]']`
- `test_blanking_a_fence_keeps_lines_below_it_at_their_raw_line` —
  `['skills/ alpha/SKILL.md: wikilink: [[x]]'] != ['skills/alpha/SKILL.md:11: wikilink: [[x]]']`
- `test_every_failure_is_reported_not_just_the_first` —
  `["skills/alpha/ SKILL.md: name-mismatch: 'beta' vs directory 'alpha'", 'skills/alpha/ SKILL.md: wikilink: [[x]]'] != ["skills/alpha/SKILL.md: name-mismatch: 'beta' vs directory 'alpha'", 'skills/alpha/SKILL.md:8: wikilink: [[x]]']`

All 22 other tests pass unchanged, including `test_the_real_tree_passes` against
the checked-out tree.

## No implementation touched

`scripts/check-skills.py` is untouched (`git status --porcelain` shows only
`tests/test_check_skills.py` modified). No commit made; the uncommitted tests
are the designed end state of this dispatch.
