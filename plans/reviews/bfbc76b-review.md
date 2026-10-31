# Review of bfbc76b — design.md gate and launcher drift

Level: medium. Sources: `/code-review medium bfbc76b` (run through the Skill
tool, findings merged below), plus a claim-by-claim check of FR-8, NFR-3 and D-6
against the primary sources. No file other than this report was written.

## Findings

Severity is my guess. The orchestrator assigns the final severity at triage.

### 1. README.md:102-103: relaunch claimed for a skill edit (low)

- Claim: "A skill edit reaches a session after the next `just dogfood` and
  relaunch."
- Contradicted by: `plugin-dev/manual/dogfood.md:91`, which says skill bodies go
  live "after `/reload-plugins` in the session". Only agent definitions and hook
  events need a relaunch (`dogfood.md:92-94`). The new FR-8
  (`docs/design.md:68-70`) defers to that manual, so README and design.md now
  disagree on what to do after a skill edit.
- Effect: a reader exits and relaunches when `/reload-plugins` would have done.
  The relaunch still works (`dogfood.md:97-99`: "A relaunch after `just dogfood`
  does too"), so the README instruction is heavier than needed, not wrong. That
  makes this low.

### 2. docs/design.md:198-200: wrong reason for rejecting a craft-owned launcher (medium)

- Claim: a craft-owned launcher would leave "nothing to report a session that
  bypassed it".
- Contradicted by: `.claude/settings.json:23-32` and
  `plugin-dev/dogfood.sh:229,262`. The `SessionStart` check is a project hook
  that reads `CLAUDE_CODE_PLUGIN_DIRS`, and it fires whichever launcher started
  the session. A craft launcher that set the same variable would still get the
  report. The old `.bin/claude` escaped the check only because it used
  `--plugin-dir`.
- Effect: one of D-6's three stated reasons is false. The others (duplicated
  `PATH` chaining and its own lint, plus fixes living upstream under NFR-4)
  still hold. (from /code-review)

### 3. docs/design.md:133-135: Architecture `justfile` bullet not swept (low)

- Claim: "`precommit` (`format-docs`, `check-refs`, `check-size`, then the
  checker and its suite) … with the release and size recipes imported from the
  vendored toolkit."
- Source: `justfile:1-13` also imports `plugin-dev/gates.just`, wraps the body
  in `sentinel-guard`/`record-sentinel`, and parses the manifest with `jq`. None
  of this is false, but this is the one mechanism description the drift sweep
  missed. It reads as an uncached gate, next to FR-7 and NFR-3. (from
  /code-review)

### 4. docs/design.md:99-101: "nearly all of it the checker's suite" (low)

- Claim: roughly six seconds cold, "nearly all of it the checker's suite".
- Measured here: `scripts/check-skills.py` plus `pytest tests/ -q` take 3.5 s of
  wall time (pytest itself reports 2.74 s). `just check-refs check-size` takes
  0.4 s and rumdl 0.08 s. The commit message gives 5.2 s cold, which makes the
  suite roughly 55-65% of the total, not nearly all of it. "Roughly six" is
  within tolerance. The 0.75 s sentinel-hit figure from the commit message is
  not in the doc. (partly from /code-review)

### 5. docs/design.md:102-105: hash description is incomplete (low)

- Claim: the sentinel hashes "names, contents and execute bits" of the matched
  files.
- Source: `plugin-dev/gates.just:186-191,232-237` also hashes each symlink's
  target path. The sentence is an omission, not a contradiction.

### 6. docs/design.md:106-109: pathspec-coverage invariant pinned only in prose (low)

- Claim: the sentinel "caches correctly only while everything those three read
  sits inside the pathspec list", and NFR-3 is marked *Done*, pinned by the
  `sentinel-guard precommit` line.
- Source: nothing checks that the list covers the inputs. The legend at
  `docs/design.md:12-13` says *Done* means something re-checks the claim. It
  holds today: `scripts/check-skills.py:36` reads only `skills/`, the suite
  reads `scripts/` and `tests/`, and `jq` reads `.claude-plugin/plugin.json`.
  Whether the invariant needs a Limitations entry is a design question. (from
  /code-review)

### 7. justfile:9: `docs` in the pathspec list is read by none of the three checks (low)

- Source: neither `scripts/check-skills.py` nor `tests/test_check_skills.py`
  reads `docs/` (grep). The extra entry is conservative and never wrong: a docs
  edit only forces a cold run. FR-7's "none of the files they read" therefore
  describes a subset of what the sentinel actually keys on. This is outside the
  diff. (from /code-review)

### 8. Declined or not applicable (from /code-review)

- FR-8 does not say to run `just dogfood` from my human partner's own shell. The
  sandbox-mask hazard in `dogfood.md:113-123` is about root dotfiles such as
  `.mcp.json`. Craft's `dist.include` lists only `.claude-plugin`, `skills` and
  `README.md`, and `dogfood.sh:46` copies only those paths, so no masked dotfile
  reaches the copy. Rare-state finding: decline.
- TODO.md is left with an empty `## Remaining` heading: cosmetic, low.
- FR-7 and NFR-3 both say what the sentinel skips: redundancy, low.

## Claims verified correct

- FR-8: the shim is `plugin-dev/bin/claude`. It sets `CLAUDE_CODE_PLUGIN_DIRS`
  to `<root>/dist/plugin` (`bin/claude:31-32`) and execs the next `claude` with
  itself stripped from `PATH` (`:33-42`). `/dist/` is gitignored
  (`.gitignore:5`). `.envrc:9` is the last `PATH_add`, after `.gitlore/bin`
  (`:2`). Only `just dogfood` writes the copy (`release.just:98-100`; the shim
  "never syncs", `bin/claude:16`). The sync honours `dist.include`
  (`dogfood.sh:46`, `dist.sh paths`). Which changes need `/reload-plugins` and
  which need a relaunch is in `dogfood.md:86-99`. "Every file under a loaded
  plugin root as sensitive" matches `dogfood.md:5`. There are two dogfood hooks
  in `.claude/settings.json` (`pre-tool` and `session-start`), and the
  session-start check reports a session that does not load the copy
  (`dogfood.md:134-142`). `.bin/` no longer exists.
- NFR-3: there are 25 tests (25 `def test_`, 25 passed). The guard sits between
  the deps and the checker, suite and `jq` (`justfile:7-13`). The hash covers
  the justfile and the vendored tree as built-ins (`gates.just:54,225`) and the
  tool versions from `PLUGIN_DEV_GATE_TOOLS` (`justfile:5`,
  `gates.just:214-219`). The pathspec list is as quoted.
- D-6: the shim, sync and hooks are tested together upstream.
  `/Users/david/code/claude-plugin-dev/tests/` has `dogfood-launcher-*`,
  `dogfood-sync-*`, `dogfood-pre-tool-*` and `dogfood-session-*` tests.
  `plugin-dev/VERSION` is 0.13.0.
- The deleted rejected-alternative bullet ("no sentinel file") was contradicted
  by `justfile:9,13`, so deleting it was correct. skills/, CLAUDE.md and the
  rest of README.md carry no stale `.bin/claude`, `--plugin-dir`, shellcheck or
  no-cache claims.

## Upstream note (not a craft finding)

`plugin-dev/manual/dogfood.md:101-102` says the sync copies "everything git does
not ignore". With a `dist.include` present, `dogfood.sh:46-49` copies only the
listed paths. That drift is in the vendored manual, so any fix belongs in
claude-plugin-dev (NFR-4).

END OF REPORT
