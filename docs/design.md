# craft — design

**Do not re-litigate** — the hub/node split, the 10000/20000 byte caps, and
markdown-skills-only as the component set. All are settled below with their
reasons.

This document is the living design: what craft is, how it is built, and why. How
it got here is git's: commit bodies and `git log --follow -- <path>`.

## Status legend

- `Done` — implemented, and pinned by something that re-checks it: a test, or
  `just precommit` running over the real tree.
- `Done (prose)` — instructions, not code and nothing re-checking them.
- `Partial`.
- `Planned`.

## Functional requirements

**FR-1 — five guidance skills ship as plugin skills.** `design-doc-writing`,
`plan-contracts`, `test-discipline`, `directive-writing` and `removing-cleanly`
live at `skills/<name>/SKILL.md` and are auto-discovered; the manifest lists no
components. *Done* · Where · pinned by: `skills/`, the `missing-skill` and
`name-mismatch` checks in `check_frontmatter`.

**FR-2 — a skill is a hub with opt-in nodes.** `SKILL.md` carries what every
invocation needs; `references/*.md` carries what only some invocations need, and
the hub links each one. A node no hub points at is unreachable and fails. *Done*
· Where · pinned by: the `orphan-node` and `broken-link` checks in `main` and
`check_body`.

**FR-3 — descriptions are purpose-first and bounded.** What the skill does, then
"Use when", then what it is not for. A description is loaded into every session
whether or not the skill fires, so it is capped at 600 bytes and must be a
quoted YAML scalar. *Done* · Where · pinned by: `MAX_DESCRIPTION_BYTES` and the
`long-description` and `unquoted-description` checks in `check_frontmatter`.

**FR-4 — no shipped body carries a private reference.** Every skill was written
from a private memory store, so the failure mode is leakage: a `[[wikilink]]`
that resolved only there, a `memory/…` path that exists on one machine, or a
retired source-fact filename. None of these stop a skill loading, so only a gate
reports them. *Done* · Where · pinned by: the `wikilink` and `private-reference`
checks in `check_body`, against the `SOURCE_FACTS` set.

**FR-5 — size caps are enforced in bytes.** 10000 bytes for a hub, 20000 for any
other file outside `plans/` and the vendored `plugin-dev/`, as `wc -c` counts
them, whitespace included. Bytes are indifferent to line length, so no reflow
has to run before the count. *Done* · Where · pinned by: `check-size`, a
dependency of `precommit`.

**FR-6 — code samples are not scanned as prose.** A bats expression such as
`[[ "$out" != *"x"* ]]` is a sample, not a wikilink, and a path inside a fence
illustrates rather than points. Fences and inline spans are blanked to spaces
before the prose checks run, preserving line numbers so failures still name the
right line. *Done* · Where · pinned by: `blank_code`.

**FR-7 — the gate runs before every commit.** `just precommit` formats, checks
references and sizes, runs the checker, runs the checker's own suite and parses
the manifest. It is a required step rather than a suggestion. The last three sit
between `sentinel-guard` and `record-sentinel`, so they skip themselves while
none of the files they read has changed since their last pass; the reference and
size checks run on every call. *Done* · Where · pinned by: the `precommit` and
`format-docs` recipes in `justfile`.

**FR-8 — the in-tree plugin is active in a dev session.** The toolkit's dogfood
shim, `plugin-dev/bin/claude`, points `CLAUDE_CODE_PLUGIN_DIRS` at a gitignored
`dist/plugin/` and chains to the next `claude` on `PATH`. `.envrc` adds it last
so it wins over `.gitlore/bin`. Only `just dogfood` writes the copy, holding the
paths `dist.include` allows; a launch never syncs, so an edit reaches a session
only after `just dogfood`, and which kinds of change then need `/reload-plugins`
or a relaunch is in `plugin-dev/manual/dogfood.md`. Not the repo root: Claude
Code treats every path under a loaded plugin root as a sensitive file, so with
the root loaded every Edit or Write in the tree asks, and auto mode's classifier
gives no verdict. *Done* · Where · pinned by: the final `PATH_add` in `.envrc`,
`dist.include`, and the two dogfood hooks in `.claude/settings.json`, whose
`SessionStart` check reports a session that does not load the copy.

**FR-9 — releases go through the vendored toolkit.** `plugin-dev/release.just`
provides `release`, `resume-release` and `check-version`; craft supplies
`precommit` and `prerelease`. Vendored rather than depended on: the release
recipe has to work in a repo that has never been released, which a runtime
dependency resolved from a marketplace cannot guarantee. *Done* — v0.1.0 was cut
through it. Where · pinned by: `import 'plugin-dev/release.just'` and the
`prerelease` recipe in `justfile`, which just refuses to parse without it.

## Non-functional requirements

**NFR-1 — the always-loaded cost stays bounded.** Five descriptions at the
600-byte cap is roughly 3 KB paid by every session that enables the plugin,
fired or not. The cap sits above the largest comparable installed skill measured
(`shell-scripting:shell-gotchas`, 551 B) and well under the point where five of
them stop being free. *Done* · Where · pinned by: `MAX_DESCRIPTION_BYTES` and
its comment.

**NFR-2 — a body is self-contained for a reader without the store.** The skills
were cut from memory facts whose neighbours are not shipped, so a surviving
cross-reference dangles for every consumer. Where a dropped link carried
meaning, the rule it pointed at is restated inline instead. *Done (prose)* ·
Where · pinned by: FR-4's checks catch the mechanical classes; the judgement
that an inlined clause reads correctly stays with review.

**NFR-3 — the gate is cheap enough to run on every commit.** Roughly six seconds
cold, nearly all of it the checker's suite: twenty-five tests, each spawning the
checker as a subprocess so the invocation matches the one `precommit` makes. The
toolkit's gate sentinel buys most of that back: it hashes the names, contents
and execute bits of the files the `sentinel-guard` pathspecs match, with the
justfile, the vendored toolkit and the tool versions `PLUGIN_DEV_GATE_TOOLS`
lists, and skips the checker, suite and manifest parse when the hash matches the
last pass. It caches correctly only while everything those three read sits
inside the pathspec list, so a new input to the checker or its suite joins the
list in the same change. *Done* · Where · pinned by: the
`sentinel-guard precommit` line in `justfile`.

**NFR-4 — the vendored subtree is never hand-edited.** `plugin-dev/` is
generated content pulled from a pinned `dist-` tag of the toolkit repo; a fix
belongs upstream, followed by a re-pull. *Done (prose)* · Where · pinned by:
`toolkit_url` and `toolkit_prefix` in `plugin-dev/release.just`; nothing
mechanical enforces it.

## Architecture

Craft is a Claude Code plugin whose entire shipped surface is markdown. There
are no hooks, agents, commands or MCP servers, and the manifest declares no
component paths — skills are discovered from `skills/`.

- **`skills/<name>/SKILL.md`** — the hub, read on every invocation of that
  skill.
- **`skills/<name>/references/*.md`** — nodes, read only when the hub sends the
  reader to one. One skill is hub-only, having no material that splits.
- **`scripts/check-skills.py`** — maintainer tooling, not a shipped component.
  Nine blocking checks, grouped as frontmatter shape (`check_frontmatter`), body
  hygiene (`check_body`), and reachability (in `main`).
- **`tests/test_check_skills.py`** — the gate's own gate. One test per check,
  each spoiling an otherwise-clean tree in exactly one way and asserting the
  *complete* output, so the assertion fails if the check it names stops firing.
- **`justfile`** — `precommit` (`format-docs`, `check-refs`, `check-size`, then
  the checker and its suite) then `prerelease`, with the release and size
  recipes imported from the vendored toolkit.
- **`.rumdl.toml`** — MD013 only, reflow at 80 columns in `normalize` mode.
  rumdl is used as a prose wrapper, not a linter: headings, code and tables are
  neither wrapped nor reported.
- **`memory/`** — a git submodule holding the gitlore memory store, including
  the `ddaanet` shared tier that `CLAUDE.md` imports.
- **`inbox/`** and **`plans/`** — what arrives from other repositories, and what
  this repo plans for itself. See `inbox/README.md`.

## Design decisions

**D-1 — the hub cap is tighter than the node cap.** 10000 bytes against 20000. A
hub is paid on every invocation of the skill; a node only when the hub sends the
reader there, so the two are not the same budget. *Rejected: one uniform cap*,
and *rejected: counting lines* — a line count rewards long lines, where a byte
count is indifferent to them.

**D-2 — rumdl hard-wraps the prose.** In `normalize` mode it re-joins each
paragraph before wrapping, so the breaks do not depend on where an earlier edit
left them; its default mode only breaks lines over the column, leaving narrower
hand-wrapping as it is.

rumdl is the wrapper because it alone left rendering untouched. Measured by
cmark-gfm render diff over ~100 files of design docs and plans, on rumdl 0.2.74
(craft pins 0.2.60), rumdl showed zero rendering changes on well-formed input,
left emphasis markers alone, and was idempotent. *Rejected:*

- **prettier** `--prose-wrap always` — rewrites `*em*` to `_em_` with no option
  to keep it, and broke a bold whose first word was a code span starting `**`.
- **dprint** — keeps emphasis, but dedents fenced code to the fence's indent and
  strips a one-sided space inside a code span.
- **mdformat** (+gfm) — turns `---` rules into underscores and renumbers ordered
  lists `1. 1. 1.`, both hardcoded.
- **mdslw**, **remark** with `@webpro/remark-wrap-prose` — break inside code
  spans, headings and table cells, and start a wrapped line with `+ …`, which
  re-parses as a list item; remark is not idempotent either.
- **pandoc** `-t gfm --columns` — drops code fences and escapes `#` and `**`.

**D-3 — a quoted description is required, though the runtime does not need
one.** `yaml.safe_load` rejects an unquoted scalar containing `: `, which Claude
Code itself loads fine. Requiring the quote is what keeps the gate from being
stricter than the runtime for no reason: with it, the gate parses everything the
runtime parses. *Rejected: a bespoke frontmatter parser* — more code to be wrong
than the rule is worth.

**D-4 — retired source facts are named in the checker.** The twenty facts these
skills were written from, two retired to other venues, and one absorbed into a
skill after release are enumerated in `SOURCE_FACTS`. Every one is gone from the
store, so a surviving mention in a body is a dangling private reference rather
than a citation. *Rejected: matching any `*.md` filename* — it would flag
legitimate references to shipped files.

**D-5 — markdown skills only.** No hooks, scripts, agents or commands as plugin
components. The guidance is prose that an agent reads at a moment; nothing in it
needs to execute. Keeping the component set empty also keeps the plugin
installable with no permissions question.
*Rejected: shipping the checker as a plugin hook* — it validates this repo's own
authoring, which no consumer runs.

**D-6 — the dev launcher is the toolkit's.** Craft loads its dogfood copy
through the vendored `plugin-dev/bin/claude` rather than a launcher of its own:
the shim, the sync and the two hooks that guard the copy and report a session
not loading it ship and are tested together upstream, and NFR-4 keeps fixes to
them there. *Rejected: a craft-owned launcher script* — it would duplicate the
shim's `PATH` chaining and need its own lint.

**D-7 — the caps are a shared-tier rule, not a craft rule.** They govern every
artifact written anywhere, not only where a checker happens to be wired, so they
have to act without being looked up. `check-size` enforces them here; the
argument for them ships in `craft:plan-contracts`.
*Rejected: documenting them only in this repo.*

**D-8 — briefs from other repositories land in `inbox/`.** A brief at the repo
root reads as a tracked project document, which is how `brief-craft-seed.md` was
read. `plans/` holds what this repo plans for itself; `inbox/` holds what
arrives. A brief's recommendation is input, not a decision: its constraints get
verified against the shipped code before anything is edited. Once acted on, a
brief moves into `plans/` under its own dateline, so `inbox/` holds only what is
still untriaged. *Rejected: leaving inbox untracked as scratch* — the briefs are
the provenance for the edits they cause, and deleting a spent one throws that
away.

**D-9 — the design doc is covered by the same formatter pass and cap as a
skill.** Written while dogfooding `design-doc-writing`, which requires the cap.
*Rejected: exempting `docs/` as maintainer-only prose* — the cap exists because
a reader takes a document in at one go, which is as true here as under
`skills/`.

**D-10 — "my human partner" is house policy, not leakage.** "User" names whoever
uses the software being built, so the collaborator needs a name of its own, and
the phrase ships in skill bodies on purpose. *Rejected: an attribution check* —
it failed every body using the phrase, enforcing the opposite of the policy.

## Rejected alternatives

Alternatives rejected against a specific decision are recorded with it above.
The ones that stand alone:

- **Keeping the guidance in the memory store.** It is where the twenty facts
  started. A memory fact is found by matching an index line against a symptom,
  which works for a symptom and fails for a moment: nothing routes "you are
  about to write a design doc" to a fact about design docs. A skill's
  description names the moment, so it fires on it.
- **One skill holding all the guidance.** Its description would have to name
  every moment at once, which is how a description stops discriminating; and
  every invocation would pay for all five topics.
- **A `docs/decisions.md` index for this document.** A decisions file read whole
  on the way to any decision is the hub under another name: it meets the cap
  without reducing what is read. At a hub's floor the argument moves out of the
  conclusion bullets instead, and the conclusions stay; see
  `skills/design-doc-writing/references/splitting-an-oversized-doc.md`.
- **Re-running a mutation matrix after every later edit.** A mutation run's
  proof is behaviour-bound: a later green run shows the behaviour is still
  there, so an edit invalidates it no more than any other test. What is
  byte-bound is the recipe naming the mutation, and `genuine-red` covers that by
  proving a mutation landed before reading its result.

## Limitations

- **L-2 — whether a description actually triggers is not mechanically
  checkable.** The gate enforces the description's shape and size; whether the
  wording causes the skill to fire at the right moment is judgement, and stays
  with review and with dogfooding.
- **L-3 — NFR-4 is unenforced.** Nothing detects a hand-edit to `plugin-dev/`;
  it is a convention held by the author.

## Non-goals

- **Shipping executable components.** Not "not yet" — the guidance is prose, and
  a hook or agent would be a different product (D-5).
- **Supporting consumers who have the memory store.** The bodies are written for
  a reader who does not, and no shipped text assumes otherwise (NFR-2).
- **Backward compatibility across skill revisions.** A skill is loaded fresh
  each session; there is no stored state to migrate and no pinned version to
  keep working.
