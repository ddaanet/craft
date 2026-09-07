# Inline plan — craft-seed

Seed the `craft` plugin with five guidance skills authored from twenty ddaanet
memory facts, retiring each source fact in the same pass. Status:
`inline-planned`, proofed 2026-09-03 (14 items: 2 approved, 11 revised, 1
killed).

## Scope

Source facts are at `memory/ddaanet/<name>.md`. They are inputs *and* targets:
each is deleted once the skill that carries it is written and green.

### `skills/design-doc-writing/`
Sources: `design-doc-writing` (18,635 B, 8 sections),
`design-doc-no-situational-state`, `design-doc-rewire-dead-components`,
`no-doc-history-references`, `reference-doc-scope`, `large-docs-review`.

- `SKILL.md` — hub. The six sections (FR, NFR, architecture, decisions, rejected
  alternatives, changelog), the changelog-is-a-separate-file rule,
  `docs/design.md` as one living doc per project with a stable undated filename,
  the what/how/why vs how-we-got-here split. Pointer stubs to each node, one
  motivation line apiece.
- `references/state-layer.md` — status stamp + `Verified against`, Now (Focus /
  Next / Do-not-re-litigate), the status legend, `Where · pinned by`,
  Limitations vs Non-goals.
- `references/splitting-an-oversized-doc.md` — the ~5.6% trimming ceiling,
  dominant-entry vs flat/need-time cuts, the hub floor, the loading instructions
  a split must ship with, the pointers-to-open-work leak class. Plus
  `large-docs-review`: flag high-risk sections rather than asking for an eyeball
  pass.
- `references/maintaining-entries.md` — superseding a decision, the four rewires
  for a dead component, delete-the-figure / retire-don't-renumber.
- `references/writing-style.md` — prose over tables, compact prose,
  present-tense standing truth, write-time record vs current truth, no draft
  archaeology.
- `references/general-vs-repo-scoped.md` — split a durable guideline from a
  point-in-time audit before delegating the research.

### `skills/plan-contracts/`
Sources: `plan-length-matches-work`, `spec-enumerations-need-rederiving`,
`plan-contracts-not-full-code`, `honest-line-count-caps`,
`spec-contract-size-predicts-pr-size`, `test-with-live-data-before-designing`.

- `SKILL.md` — hub: plan length tracks executable work, not topic; plans carry
  contracts, not full bodies. Description names the same moment as
  `superpowers:writing-plans` so it activates alongside. Two acts the body must
  carry: when that skill demands full code, write `Interfaces:` verbatim, the
  steps as contracts, and **say in the plan that it deviates** — otherwise the
  implementer hunts for code nobody wrote; and never edit the cached skill,
  since an upgrade overwrites it.
- `references/code-in-a-plan.md` — what stays verbatim across a task boundary,
  what is always a contract, the four costs of a plan carrying full bodies, and
  the 1.6x size difference to budget for.
- `references/contracts-and-size.md` — the ~400-line contract as the split
  signal, honest caps (wrap then measure; never cram; never shave docstrings; a
  bounded overage beats a reflexive split).
- `references/spec-hygiene.md` — re-derive a hand-listed enumeration by grep
  before checking conformance; treat "the only place X appears" as a query, not
  a fact.
- `references/before-you-plan.md` — run the pipeline against real data first;
  fixtures encode the same assumptions as the code.

### `skills/test-discipline/`
Sources: `green-is-not-evidence` (15,190 B, 2 sections),
`genuine-red-not-missing-sut`, `outside-in-tdd`, `test-the-invocation-path`.

- `SKILL.md` — hub: a test is evidence only when some state of the world makes
  it fail; red is a failed assertion, never a missing module. The hub also
  carries the source's dispatch discipline — budget one wrong-reason test per
  task, put the reviewer a rung above the implementer, and dispatch the red
  phase separately from the green one, or nobody ever saw the test fail.
  Description names the same moment as `superpowers:test-driven-development` and
  **claims no override**: no source here names any text in that skill.
- `references/vacuous-green.md` — the shapes that pass whatever the code does.
- `references/non-vacuous-negatives.md` — absent-string / path / proxy
  staleness, pairing over one fixture, decoy-first ordering, exact-block
  equality, errexit ordering, deleting an untestable negative whole.
- `references/genuine-red.md` — stub-then-assert, the inert-stub batch run and
  what it does not prove, one contract per line, mutate the SUT in place.
- `references/coverage-shape.md` — outside-in when the architecture is settled;
  assert the invocation contract (`[ -x ]`, recorded mode) and that the suite is
  reached at all.

Cross-plugin: the bats and shellcheck mechanics point at
`shell-scripting:shell-gotchas` by name — the only one of the brief's dangling
links with a published destination.

### `skills/directive-writing/`
Sources: `directive-states-acts` (6,099 B), §7 "Wording" of
`hook-output-channels` (1.9 KB), `loose-generation`.

- `SKILL.md` only, ~8 KB, no nodes. Include only the acts the reader performs;
  the five cuts; withhold-don't-forbid; one change, four artifacts, one telling;
  the code-comment bar. Then §7 inline, all three of its rules including the
  scope limiter — the deny rule governs deny channels; a directive channel
  exists to drive the agent, so imperative wording is correct there.
  `_wipe-emit.sh` is dropped as a path that dangles for a consumer; its three
  example lines stay.
- `loose-generation` lands here rather than in `removing-cleanly`: the moment is
  shared — designing a step where an agent emits text something else acts on —
  and withhold-don't-forbid is the same constraint-placement decision one level
  in.

### `skills/removing-cleanly/`
Sources: `remove-cleanly-no-vestigial`, `no-transition-special-cases`.

- `SKILL.md` only, ~2.9 KB, no nodes. Cut the whole machinery in one pass —
  helpers, constants, fixtures, absence-guards, docs, inbound references; fix
  forward instead of branching for a transition in tooling you also control. One
  inlined clause for the dropped link: read-only liveness detection of a foreign
  tool's state is a different thing and still applies.

### Supporting files
- `scripts/check-skills.py` — the validator, see Dependencies.
- `.bin/claude` — dev launcher shim copied from `../handoff/.bin/claude`:
  prepends `--plugin-dir <repo root>` and chains to the next `claude` on PATH
  with its own dir stripped **and the stripped PATH passed through the exec**,
  or it and gitlore's shim exec each other forever.
- `.envrc` — `PATH_add .bin` as the last line, so it wins over `.gitlore/bin`.
- `justfile` — `precommit` calls the validator, `jq` on the manifest, and
  `shellcheck .bin/claude`. `prerelease: precommit` unchanged.
- `.claude-plugin/plugin.json` — unchanged. Skills auto-discover; `version`
  stays `0.0.0` for the release recipe. Its stub `description` ships to the
  marketplace row and is not covered by this plan.

## Boundaries

**IN**
- Five skill directories under `skills/`, hub plus the nodes listed above.
- Descriptions purpose-first — what it does, then "Use when", then exclusions —
  **quoted**, and ≤ 600 bytes each (~3 KB always-loaded for the five). Measured
  against comparable installed skills, which run 54–756 B; `shell-gotchas` is
  551.
- Keep every measurement and every named instance from the sources; gloss an
  opaque name on first use ("gitlore, a git-backed memory plugin"); cut only
  what presupposes the reader is inside that repo, such as a `check-docs` recipe
  read as an instruction. The figures are what a reader cannot reconstruct and
  are the reason a section survives being read once.
- Strip the sources' second-person attribution — "my human partner pushed back",
  "my human partner's call" — to the impersonal rule or "measured on one
  project". On the order of fifteen occurrences; the largest mechanical edit in
  the job.
- Four dangling links inlined as one clause each; the fifth
  (`bats-shellcheck-gotchas`) points at `shell-scripting:shell-gotchas`.
  Within-set links become cross-skill references. No `[[wikilink]]` and no
  memory path survives.
- Imperative form applied per classified hit — instruction-subject rewritten,
  load-bearing intensifier replaced, referent kept — never a `grep -w you`
  sweep.
- **Retire each source fact once its skill is written and the validator
  passes:** delete the file, drop its root `MEMORY.md` line (composition mirrors
  the deletion into the tier index), then sweep the surviving tier facts for
  inbound links and restate the rule inline wherever the link carried meaning.
  Precedent cost: 24 files retired took 40 such rewrites across 30 survivors.
  Order matters — the source text is the input to the writing, so a `rm` that
  lands first makes the rest of the work depend on `git show`.
- 400-line ceiling on reference nodes and source files; ~200-line target on each
  `SKILL.md` hub, since a hub is paid on every invocation and a node is opt-in.

**OUT**
- Any write to `ddaanet/claude-plugins` or another repo. The marketplace row is
  created by `just release` from here.
- A release. `just release` and the marketplace entry are a later, separate
  step.
- Hooks, scripts, agents or commands as plugin components — markdown skills
  only. (`scripts/check-skills.py` is maintainer tooling, not a shipped
  component.)
- The two sibling routings the brief defers: shell-scripting facts, and the
  unnamed hook/skill/agent/plugin repo.

## Dependencies

- **`direnv allow`** after `.envrc` changes — a human action; until it runs the
  shim is not on `PATH` and nothing loads the plugin.
- The plugin root resolves at process start, so `--plugin-dir` first takes
  effect in the next session. Within a session after that, `/reload-plugins`
  picks up edited skill bodies and descriptions; no restart, since no hooks or
  agents are in scope.
- Retirement rides the gitlore gate: deleting tier files and index lines is an
  ordinary edit, the parent commit's pre-commit hook records and gates memory,
  and `/gitlore:push` publishes the deletion to the other consumers. Never a
  commit inside the submodule.
- `hook-output-channels` §7 is one section of a 17.6 KB file — read the section.

### `scripts/check-skills.py` (stdlib + PyYAML 6.0.2, `pathlib` globbing)

1. Every `skills/*/` has a `SKILL.md`; frontmatter carries `name` and
   `description`; `name` equals the directory name; `description` is a
   **quoted** scalar — `yaml.safe_load` rejects unquoted descriptions containing
   `: `, which Claude Code itself loads fine, so requiring the quote is what
   keeps the gate from being stricter than the runtime.
2. `description` ≤ 600 bytes.
3. No `[[wikilink]]` anywhere under `skills/`.
4. No `memory/…` path, `MEMORY.md`, or bare source-fact filename under
   `skills/`.
5. No `my human partner` under `skills/`.
6. Every relative link in a hub or node resolves to a file that exists.
7. No orphan node: every `references/*.md` is reachable from its hub.
8. No file over its cap: 200 lines for a `SKILL.md` hub, 400 for a node or a
   `scripts/*.py`, measured after `just format-docs` hard-wraps at 80 columns.

Plus `just format-docs` ahead of it, `jq . .claude-plugin/plugin.json` and
`shellcheck .bin/claude`. No cache or sentinel — the run is well under a second.
Whether a description *triggers* well is judgement and stays with review.

## Decisions taken

1. **`plan-contracts-not-full-code` migrates into the skill.** The earlier
   reading kept it in memory as a patch for `superpowers:writing-plans`; the
   ruling is that it ships. It lands as
   `skills/plan-contracts/references/code-in-a-plan.md`, with the two acts —
   `Interfaces:` verbatim plus a stated deviation, and never patch the cached
   skill — in the hub, and the description extended to name the moment another
   plan-writing skill asks for complete code. All twenty source facts are
   retired.
2. **`rumdl` adopted, and the caps enforced.** `.rumdl.toml` pins MD013 reflow
   at 80 columns, `just format-docs` runs ahead of the checker, and
   `scripts/check-skills.py` fails a `SKILL.md` over 200 lines or any other file
   over 400.
3. **The 400/200 cap is a `shared-claude.md` rule.** It governs every artifact
   written anywhere, not only the moment a precommit checker is wired, so it has
   to act without being looked up. The `precommit-line-caps` memory fact it was
   first written as is retired into that entry, which carries the caps, the
   soft-guideline and never-cram clauses, and the formatter-before-checker
   wiring, and points at `craft:plan-contracts` for the argument.
