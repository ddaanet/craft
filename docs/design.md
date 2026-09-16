# craft — design

Status: released. Five skills ship at v0.1.0, listed in the `ddaanet`
marketplace. Verified against: `56bfebf` (2026-09-17).

This document is the living design: what craft is, how it is built, and why. How
it got here is [the changelog](changelog.md).

## Now

- **Focus** — dogfooding the five skills on real work. They were written from
  retired memory facts and reviewed as prose. Four have now met live work:
  `design-doc-writing` wrote this document, `test-discipline` drove the
  checker's suite, and `plan-contracts` shaped and `removing-cleanly` executed
  the plan that removed `attribution` and gave failures a line.
- **What that plan showed** — the contracts carried two sonnet dispatches, red
  and green, with no rework, and naming each red test's seam let one mutation
  confirm it. `removing-cleanly`'s machinery grep caught every mention by name
  but not a count derived from the removed thing: NFR-3's test count went stale
  and was caught by reading. The outline told execution to renumber Limitations,
  against `design-doc-writing`'s retire-don't-renumber; it was written without
  loading the skill that governs the doc it edits, and the renumber landed
  before that skill was invoked.
- **Next** — dogfood `directive-writing`, the one still unexercised, against
  real agent-facing output. Decide whether the two misses feed back: derived
  counts into `removing-cleanly`, and loading the governing skill into
  `plan-contracts`.
- **Do not re-litigate** — the hub/node split, the 200/400 line caps, the
  formatter-before-checker ordering, and markdown-skills-only as the component
  set. All are settled below with their reasons.

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

**FR-5 — line caps are enforced against wrapped prose.** 200 lines for a hub,
400 for a node or a maintainer script, measured only after `just format-docs`
hard-wraps at 80 columns — an unwrapped file games any line count. *Done* ·
Where · pinned by: `MAX_HUB_LINES`, `MAX_NODE_LINES`, the `oversized-file`
check, and `format-docs` running as `precommit`'s first dependency.

**FR-6 — code samples are not scanned as prose.** A bats expression such as
`[[ "$out" != *"x"* ]]` is a sample, not a wikilink, and a path inside a fence
illustrates rather than points. Fences and inline spans are blanked to spaces
before the prose checks run, preserving line numbers so failures still name the
right line. *Done* · Where · pinned by: `blank_code`.

**FR-7 — the gate runs before every commit.** `just precommit` formats, runs the
checker, runs the checker's own suite, parses the manifest and shellchecks the
launcher. It is a required step rather than a suggestion, and it carries no
cache or sentinel. *Done* · Where · pinned by: the `precommit` and `format-docs`
recipes in `justfile`.

**FR-8 — the in-tree plugin is active in a dev session.** `.bin/claude` prepends
`--plugin-dir <repo root>` and chains to the next `claude` on `PATH` with its
own directory stripped, passing the stripped `PATH` through the `exec`. `.envrc`
adds it last so it wins over `.gitlore/bin`. *Done* · Where · pinned by:
`.bin/claude`, the final `PATH_add` in `.envrc`, and `shellcheck` in
`precommit`.

**FR-9 — releases go through the vendored toolkit.** `plugin-dev/release.just`
provides `release`, `resume-release` and `check-version`; craft supplies
`precommit` and `prerelease`. *Done* — v0.1.0 was cut through it. Where · pinned
by: `import 'plugin-dev/release.just'` and the `prerelease` recipe in
`justfile`, which just refuses to parse without it.

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

**NFR-3 — the gate is cheap enough to be unconditional.** Roughly six seconds on
the whole tree, nearly all of it the checker's suite: thirty-one tests, each
spawning the checker as a subprocess so the invocation matches the one
`precommit` makes. That is what lets the gate run on every commit with no cache
to invalidate and no sentinel to go stale — the sub-second figure this recorded
before the suite existed bought nothing that the absence of a cache does not buy
at six. *Done* · Where · pinned by: `precommit` having no cache step.

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
  reader to one. Two skills are hub-only, having no material that splits.
- **`scripts/check-skills.py`** — maintainer tooling, not a shipped component.
  Ten blocking checks, grouped as frontmatter shape (`check_frontmatter`), body
  hygiene and caps (`check_body`), and reachability (in `main`).
- **`tests/test_check_skills.py`** — the gate's own gate. One test per check,
  each spoiling an otherwise-clean tree in exactly one way and asserting the
  *complete* output, so the assertion fails if the check it names stops firing.
- **`justfile`** — `format-docs` then `precommit` then `prerelease`, with the
  release recipes imported from the vendored toolkit.
- **`.rumdl.toml`** — MD013 only, reflow at 80 columns in `normalize` mode.
  rumdl is used as a prose wrapper, not a linter: headings, code and tables are
  neither wrapped nor reported.
- **`memory/`** — a git submodule holding the gitlore memory store, including
  the `ddaanet` shared tier that `CLAUDE.md` imports.
- **`inbox/`** and **`plans/`** — what arrives from other repositories, and what
  this repo plans for itself. See `inbox/README.md`.

The ordering is load-bearing in one place: the formatter must run before the
checker, because a line count means nothing until the prose is hard-wrapped.
`precommit` expresses this as a just dependency rather than as a step inside the
recipe, so it cannot be skipped by running the checker directly.

## Design decisions

**D-1 — the hub cap is tighter than the node cap.** 200 lines against 400. A hub
is paid on every invocation of the skill; a node only when the hub sends the
reader there, so the two are not the same budget. *Rejected: one uniform cap.*

**D-2 — hard-wrap, then measure.** A line count is only honest once a formatter
has normalized the prose, otherwise a file with 300-character lines passes a cap
it plainly violates. rumdl in `normalize` mode re-joins each paragraph before
wrapping, so the count reflects the prose rather than where an earlier edit left
the breaks. *Rejected: counting characters instead of lines* — it stops matching
what a reader takes in at one go, which is what the cap is about.

**D-3 — a quoted description is required, though the runtime does not need
one.** `yaml.safe_load` rejects an unquoted scalar containing `: `, which Claude
Code itself loads fine. Requiring the quote is what keeps the gate from being
stricter than the runtime for no reason: with it, the gate parses everything the
runtime parses. *Rejected: a bespoke frontmatter parser* — more code to be wrong
than the rule is worth.

**D-4 — retired source facts are named in the checker.** The twenty facts these
skills were written from, plus two retired to other venues, are enumerated in
`SOURCE_FACTS`. Every one is gone from the store, so a surviving mention in a
body is a dangling private reference rather than a citation.
*Rejected: matching any `*.md` filename* — it would flag legitimate references
to shipped files.

**D-5 — markdown skills only.** No hooks, scripts, agents or commands as plugin
components. The guidance is prose that an agent reads at a moment; nothing in it
needs to execute. Keeping the component set empty also keeps the plugin
installable with no permissions question.
*Rejected: shipping the checker as a plugin hook* — it validates this repo's own
authoring, which no consumer runs.

**D-6 — the dev launcher chains rather than resolves.** `.bin/claude` strips its
own directory from `PATH` and passes the stripped `PATH` through the `exec`,
because the next shim on the chain resolves *its* next `claude` against the
inherited `PATH`; leaving ourselves on it makes the two shims exec each other
forever. *Rejected: hard-coding the real binary's path* — it breaks the moment
another shim is installed or the binary moves.

**D-7 — the caps are a shared-tier rule, not a craft rule.** They govern every
artifact written anywhere, not only where a checker happens to be wired, so they
have to act without being looked up. The checker enforces them here; the
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

**D-9 — the design doc is covered by the same formatter and cap as a skill.**
Written while dogfooding `design-doc-writing`, which requires both.
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
- **A `docs/decisions.md` index for this document.** That is the lever at a
  hub's floor, and this hub is nowhere near it. Recorded here so the option is
  not re-derived: see
  `skills/design-doc-writing/references/splitting-an-oversized-doc.md`.
- **Per-check caching or a sentinel file in `precommit`.** A cache would add
  invalidation bugs to buy back a few seconds on a gate nobody waits on (NFR-3).

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

## Changelog

Design-significant history lives in [`docs/changelog.md`](changelog.md) — what
was decided, reversed, built or torn down, never a line-by-line account of every
edit. Git history is already the full changelog.
