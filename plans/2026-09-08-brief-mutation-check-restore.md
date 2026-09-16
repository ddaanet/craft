## Brief: restoring a mutation-check without a backup

2026-09-08 — from a session in `ddaanet/handoff`

Concerns `test-discipline`. Mutation-checking is the practice that skill already
asks for — after a new test goes green, mutate the code it claims to cover and
confirm *that test alone* reds. What the skill does not say is how to get the
source back, and the obvious ways to do it fail in this environment in ways that
leave the mutation live.

### Observed

Mutation applied to `scripts/checkpoint.py` by exact string replacement, with a
backup taken first:

```
cp scripts/checkpoint.py "$TMPDIR/checkpoint.py.bak" && python3 - <<'PY'
… replace the branch with `return []` …
PY
```

The check worked: one test redded, 137 passed. The restore did not.

```
cp "$TMPDIR/checkpoint.py.bak" scripts/checkpoint.py
→ cp: cannot stat '/checkpoint.py.bak': No such file or directory
```

`$TMPDIR` was set for the call that wrote the backup and empty for the call that
read it. Verified after the fact: the backup is on disk at
`/tmp/claude-1000/checkpoint.py.bak`, holding the pre-mutation content, while
`echo "[$TMPDIR]"` returned empty in every subsequent call of the same session.
A separate probe confirmed that writes to `/` genuinely fail under the sandbox
(`Permission denied`, rc 1), so nothing was silently swallowed — the variable
simply is not stable across Bash calls.

Net effect: a mutated source file, uncommitted work in the tree, and the
intended restore route broken. Recovery was to re-run the replacement with `old`
and `new` swapped, then re-run the suite.

### Proposal

**Restore by inverting the edit, not by restoring a copy.** A mutation applied
as an exact string replacement is invertible: swap the two strings and apply it
again. No backup file, no `$TMPDIR`, no git, and nothing to clean up. It also
makes the mutation self-documenting — the pair of strings *is* the record of
what was changed.

**Then prove the restore**, since "restored" is a claim about the file: grep for
the mutation marker and re-run the full suite. Green is the evidence; the `cp`
exiting 0 is not.

### Constraints

- Craft ships prose only — this is a paragraph in `test-discipline`, not a
  helper script.
- Environment: Claude Code's sandboxed Bash. Its write allowlist includes `.`
  and `$TMPDIR`, which is what makes `$TMPDIR` the reflexive choice for a
  scratch copy.
- The two commands are separate tool calls by construction (mutate, run suite,
  restore), so anything that depends on a variable surviving between them is the
  hazard, not the specific variable.

### Rejected approaches

- **`${TMPDIR:-/tmp}`** — fixes the unset case and keeps the cross-call
  assumption, plus a file to clean up. The observed failure was not an unset
  variable at write time; it was a variable that changed between calls.
- **`git checkout -- <file>`** — discards uncommitted work in any session that
  has already applied its own fixes, which is exactly the session that is
  mutation-checking a test it just wrote. Strictly worse than the `cp`.
- **`git stash`** — same hazard, with more moving parts.
- **Reading `&&` success as backup success** — the chain succeeded here and the
  backup was still unreachable one call later. Chain success says the backup was
  written, never that it can be found again.

### Additional context

There is a related, benign polarity already recorded in the ddaanet memory tier:
with `$TMPDIR` unset *at write time*, the `cp` fails, the `&&` short-circuits,
and the mutation never runs. That one costs a wasted call and announces itself.
The one above is the dangerous half, because the mutation does run.

A stray `/tmp/claude/checkpoint.py.bak` from an unrelated session on the same
day suggests the backup-file idiom is in general use and this is reachable
again.
