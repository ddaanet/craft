# Outline — locatable checker failures

Give `scripts/check-skills.py` failure messages a line number, and remove the
`attribution` check, which enforces the opposite of the house policy.

Executed from this outline directly — no runbook (my human partner's call,
2026-09-16). Each change below is stated as a contract, not code.

## Why

**L-1 in `docs/design.md`.** `blank_code` substitutes spaces for code rather
than deleting, so that every line number in a failure message points at the
right line. No check reports a line, and the one line-derived figure
(`oversized-file`) counts the raw text, so nothing distinguishes the current
implementation from one that deletes. The docstring promises a property the
suite cannot see.

**`attribution` is wrong policy, not just a defect.** It fails any body saying
"my human partner". That phrase is the policy: "user" names whoever uses the
software being built, so the collaborator needs a name of its own, and the
phrase ships in skill bodies on purpose. The check was found while grounding
L-1: `rumdl` `normalize` can reflow the phrase across a newline and disarm the
substring match. Hardening it was the original item B; removing it replaces
that.

## Scope

IN: `scripts/check-skills.py`, `tests/test_check_skills.py`, `docs/design.md`,
`docs/changelog.md`, `README.md`.

OUT: the frontmatter checks — the field name already locates them inside a block
under ten lines, and a line would mean plumbing yaml's own offsets. OUT:
`oversized-file`, a whole-file property with no line to name. OUT: reordering
the module to entry-points-first; it would bury the diff. OUT: restoring "my
human partner" wording the seed pass stripped from `skills/` — the removal makes
it permissible, not required. OUT: the "eleven checks" and "thirty tests"
figures in `skills/test-discipline/references/genuine-red.md` and
`docs/changelog.md`, which are measurements of their moment, not current state.

## Changes

### 1. Remove `attribution` — whole machinery, one pass

Lands first, as its own commit, so the line-number work starts from ten checks.

- `scripts/check-skills.py`: the check in `check_body`, its row in the module
  docstring's check list, the "my human partner" clause in the docstring's
  leakage paragraph, and the count "Eleven" → "Ten".
- `tests/test_check_skills.py`: delete `test_attribution`. Three tests use the
  phrase as their spoiling defect and are rewritten, not deleted, because they
  pin something else:
  - `test_a_fenced_block_is_not_scanned_as_prose` — drop the
    `# my human partner` comment from the fence; the wikilink and store paths
    still carry it.
  - `test_blanking_code_does_not_hide_prose_on_the_same_line` — the prose defect
    beside the span becomes `[[x]]`, expecting one `wikilink` failure.
  - `test_every_failure_is_reported_not_just_the_first` — drop the phrase and
    its expected line; `name-mismatch` plus `wikilink` still prove accumulation
    across `check_frontmatter` and `check_body`.
- No absence test. Nothing asserts the phrase now passes.
- `docs/design.md`: FR-4 loses the attribution clause and the `attribution`
  check name; Architecture's "Eleven" → "Ten". Record a decision: the phrase is
  house policy, because "user" names the software's user;
  *Rejected: an attribution check*.
- `docs/changelog.md`: one entry — the check existed, was reversed, and why.
- `README.md:100-104`: "eleven" → "ten", and drop "an attribution" from the
  leakage list.
- Verify: whole-tree grep for `attribution` and `human partner` outside `plans/`
  and `memory/` returns only the design doc's new decision.

### 2. Line numbers on locatable checks — TDD

Red and green dispatched separately; test-driver on sonnet.

**Contracts:**

- `line_of(text: str, index: int) -> int` — `1 +` the count of `\n` in
  `text[:index]`. Sits beside `blank_code`. Its docstring states the dependency:
  an index into the blanked prose is an index into the raw text, because
  `blank_code` substitutes rather than deletes.
- `wikilink`, `private-reference` and `broken-link` emit
  `{path}:{line}: {check}: {token}`, one failure per occurrence, each found by
  `finditer` over the blanked prose. `oversized-file`, `orphan-node`,
  `missing-skill` and the frontmatter checks keep `{path}: {check}: …`. The
  mixed format is deliberate: `path:line:` is what a terminal makes clickable.
- `private-reference` becomes per-occurrence (today it is once per pattern). A
  count that hides two of three hits is L-1's unfalsifiability problem again.
- `private-reference` keeps literal patterns; a comment records that none of
  them contains a space, so a reflow cannot split one.
- Correct the `SOURCE_FACTS` comment. "Every one is gone from the store" is
  false: `hook-output-channels` survives, indexed. The check stays — a body
  naming that file is private to any reader without the store — and the comment
  says that instead of resting on an absence.

**Red, each failing against the code as it stands after change 1:**

1. The existing single-defect tests for `wikilink`, the three
   `private-reference` cases and `broken-link`, plus the rewritten same-line and
   accumulation tests, expect `skills/alpha/SKILL.md:<n>:` with `<n>` the
   defect's line in the file `hub()` writes (body starts at line 8).
2. **The L-1 seam:** a body with a three-line fenced block above a `[[x]]` must
   report `[[x]]`'s raw-file line. A `blank_code` that deleted the fence would
   report three lines fewer.
3. **Per-occurrence:** a body with `memory/` on two different lines reports two
   `private-reference` failures, in line order.

Green: all three plus the full suite, then `just precommit`.

### 3. Close L-1

With change 2's commit, never ahead of it: delete L-1 from `docs/design.md`'s
Limitations and renumber L-2, L-3. Update NFR-3's test count to the suite's
actual count after change 2 (re-derive with `pytest --collect-only -q`).
