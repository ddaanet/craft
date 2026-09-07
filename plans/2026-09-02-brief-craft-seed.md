## Brief: seed the craft plugin from ddaanet design-moment memory facts

2026-09-02

Process this after mounting the ddaanet memory tier (`/gitlore:add-tier`). Every
source file named below is then at `memory/ddaanet/<name>.md` in this repo.

### What this repo is

A Claude Code plugin holding guidance that ddaanet memory facts already encode
but structurally cannot deliver. Five skills: design docs, plans and specs,
tests, agent-facing directives, tooling-change hygiene. It gets a marketplace
row in `ddaanet/claude-plugins`.

### Why this content leaves memory

Two mechanical findings, both measured rather than argued.

**Recall delivers the first 4096 bytes of a memory file and stops.**
`design-doc-writing.md` is 18,635 bytes, so 22% of it is reachable;
`green-is-not-evidence.md` is 15,190 (27%); `directive-states-acts.md` is 6,099
(67%). The content has outgrown the format, not merely the store.

**Trigger shape.** A memory index line fires when a tool result surfaces a token
— an error string, a flag, a path. These facts trigger on a *design moment*, an
activity with no string to match. Analysis over the 2026-W30…W36 transcript
corpus (`plans/2026-09-02-recall-log-analysis.md` and
`plans/2026-09-02-ddaanet-design-moment-facts.md`, both in the gitlore repo)
found 20 never-read facts and that every one was of this shape.

A skill triggers on a task shape and has no size cap. That is the whole reason
for the move.

### The five skills and their sources

| skill | source facts | bodies |
| ----- | ------------ | -----: |
| design-doc writing | `design-doc-writing`, `design-doc-no-situational-state`, `design-doc-rewire-dead-components`, `no-doc-history-references`, `reference-doc-scope`, `large-docs-review` | 28.1KB |
| plan and spec writing | `plan-length-matches-work`, `spec-enumerations-need-rederiving`, `plan-contracts-not-full-code`, `honest-line-count-caps`, `spec-contract-size-predicts-pr-size`, `test-with-live-data-before-designing` | 12.6KB |
| test discipline | `green-is-not-evidence`, `genuine-red-not-missing-sut`, `outside-in-tdd`, `test-the-invocation-path` | 23.7KB |
| directive writing | `directive-states-acts`, plus §7 of `hook-output-channels` (user-facing wording vs agent-facing deny) | 6.1KB + one section |
| tooling-change hygiene | `remove-cleanly-no-vestigial`, `no-transition-special-cases`, `loose-generation` | 4.3KB |

Twenty facts, ~74.8KB of body, holding 4,748 bytes of always-loaded index.

### Decisions

- **Five skills, one plugin.** Every enabled skill's `description` is injected
  at session start and counted under `/context`'s *Skills*, so context cost is
  per-skill and packaging is neutral on it. The plugin boundary is therefore an
  enablement decision, and these five share one — nobody wants doc discipline on
  and test discipline off.
- **Named for the theme, not the provenance.** A plugin called "graduated
  memories" would trigger nothing; each *skill* carries the trigger, the plugin
  only needs a coherent theme.
- **Two skills override third-party skills** — `superpowers:writing-plans` and
  `superpowers:test-driven-development` are from `obra/superpowers` and cannot
  be edited. The overriding skill's description must name the same moment so it
  activates alongside.
- **`SKILL.md` plus `references/`** progressive disclosure. `shell-gotchas`
  already uses that shape, and `design-doc-writing` itself prescribes hub +
  pointer-stub nodes for oversized documents.
- **`loose-generation` ships only with a trigger** naming its moment ("designing
  an agent step that must emit a constrained artifact"). Zero reads and no
  project example otherwise; drop it rather than carry it untriggered.

### Constraints

- **Distributed skill text never cites a memory file.** Consumers do not have
  this store, so a `[[wikilink]]` or a `memory/ddaanet/…` path dangles for every
  one of them. Inline the criteria at write time. Links pointing *outside* the
  set above, which must be resolved rather than rewritten:
  `[[examine-evidence-drift]]` (in `design-doc-writing`,
  `spec-enumerations-need-rederiving`), `[[gitlore-tier-index-budget]]` (in
  `design-doc-no-situational-state`), `[[hook-output-channels]]` (in
  `design-doc-writing`), `[[bats-shellcheck-gotchas]]` (in
  `green-is-not-evidence`), `[[detect-liveness-not-presence]]` (in
  `no-transition-special-cases`). Links *within* the set become ordinary
  cross-references between skills or sections. `remove-cleanly-no-vestigial`
  carries a `[[link]]` that is a generic example, not a reference — drop it.
- **Description form: purpose first, then "Use when", then exclusions.** Never a
  bare trigger list. Length is a per-session cost in every repo where the plugin
  is enabled, so keep it tight.
- **Vendor the release toolkit, don't write one.** Run `claude-plugin-dev`'s
  `install.sh` from this repo's root; it resolves the newest `dist-vX.Y.Z` tag
  and does the `git subtree add` itself. Never pin a bare `vX.Y.Z` source tag or
  `main`, and never hand-edit anything under `plugin-dev/`. The consumer must
  define `precommit` and `prerelease` recipes or `just` refuses every recipe.
- **Do not delete or edit the source memory facts.** Retiring them from the
  ddaanet tier is a separate gitlore-side pass; this repo has no authority over
  that store, and the tier is shared with nine other repos.
- Never `--no-verify`. Do not create or switch branches — work on what is
  checked out.

### Rejected approaches

- **A new memory tier for design guidance.** Fixes nothing: the 4096-byte recall
  cap is per file regardless of tier, and every mounting repo still pays index
  bytes for lines that never fire.
- **One repo per skill.** Five toolkit vendorings, five marketplace rows, five
  releases to cut — and no context saving, since the cost is per-skill either
  way.
- **Folding into `ddaanet/skills` (the `ddaa` / `ddaa-fr` plugins).** That repo
  ships bilingual skills that run in claude.ai. This content is Claude-Code- and
  repo-specific (`docs/design.md`, `plans/`, changelog file layout); it neither
  translates nor runs there.
- **Leaving it in memory and trimming the bodies under 4KB.** Sentence-level
  trimming of a living document hits a ceiling around 5.6% before it starts
  cutting the argument that keeps settled decisions settled — measured, and
  recorded in `design-doc-writing` itself.

### Additional context

- The ddaanet index is 25,505 bytes against a ~24,985-byte loader cutoff, so it
  truncates today: entries past the cutoff never reach a session. Converting
  these 20 lines frees 4,748 bytes. That is a real motive but the secondary one
  — reachability of the bodies is the primary.
- **Conversion is usually a split, not a move.** The general rule goes to the
  skill; the error string and the reproduction stay in memory, where a tool
  result can surface them. `shell-gotchas` already does this with git hook
  environment leakage, and it is the pattern to follow wherever a source fact
  carries both.
- Sibling routing decided in the same pass, out of scope here: bats/shellcheck
  and justfile facts go to `ddaanet/shell-scripting` (brief already dropped in
  that repo); hook, skill, agent and plugin-authoring facts go to a separate new
  repo whose name is still open.
