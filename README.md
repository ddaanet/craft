# craft

Five guidance skills for Claude Code: how to write a design doc that stays
current, how to size a plan, what makes a test evidence rather than
decoration, how to word text an agent will act on, and how to remove a
capability without leaving stumps behind.

Everything it ships is markdown. There are no hooks, no agents, no commands
and no MCP servers — the guidance is prose an agent reads at a moment, and
nothing in it needs to execute. Installing it asks you no permissions
question.

Each skill fires on a *moment*, not on a command you have to remember. A
description names the situation — "when a decision needs recording", "when
inherited tests came back green" — so the skill invokes itself when that
situation shows up. That is the whole reason these are skills: the same
guidance sitting in a memory store is found by matching a symptom, and
nothing routes "you are about to write a design doc" to a fact about design
docs.

## The skills

| skill | use it when |
|---|---|
| `design-doc-writing` | creating, updating, reviewing, splitting or auditing a design doc, spec or architecture reference — or a decision, requirement or rejected alternative needs recording |
| `plan-contracts` | writing, sizing, splitting or reviewing an implementation plan or spec, collapsing passages claimed to be duplicates — or a size cap on a plan, a PR or a source file is in play |
| `test-discipline` | writing, reviewing or dispatching tests, planning a red step, or inherited or subagent-authored tests came back green |
| `directive-writing` | authoring agent-facing text: a hook's `additionalContext`, a probe directive, an instructing error message, a deny reason, a code comment |
| `removing-cleanly` | removing a feature, retiring a file, deleting or splitting a module, renaming a symbol other files cite, or handling a version transition in tooling you also control |

Each one also says what it is *not* for, and means it:

- `design-doc-writing` is not for plans and runbooks, which are frozen and
  date-stamped. A design doc is current truth; a plan is a record of what
  was decided on a day.
- `plan-contracts` is not for the design doc itself.
- `test-discipline` complements test-driven development rather than
  replacing it — it is about whether a test is evidence, not about when to
  write one.
- `directive-writing` is not for user-facing prose. Text a person reads
  wants context; text an agent acts on wants the acts and nothing else.
- `removing-cleanly` is not for migrations at a boundary with users you do
  not control, which need real migration handling.

## Setup

```
/plugin marketplace add ddaanet/claude-plugins
/plugin install craft@ddaanet
```

That is all. There is no per-project setup step and no state to initialise.

## Usage

Nothing to invoke. Start the work the skill names and it fires — write a
design doc, size a plan, plan a red step, word a deny reason, delete a
module. To read one deliberately, invoke it by name: `/craft:plan-contracts`,
`/craft:test-discipline`, and so on.

The five descriptions are loaded into every session that enables the plugin,
whether or not a skill fires. That cost is bounded on purpose — each
description is capped at 600 bytes, so the whole plugin's resident footprint
is roughly 3 KB.

## How a skill is built

A skill is a **hub** with **opt-in nodes**.

- `skills/<name>/SKILL.md` — the hub, read on every invocation. Capped at
  10000 bytes, because every invocation pays for it.
- `skills/<name>/references/*.md` — nodes, read only when the hub sends you
  to one. Capped at 20000 bytes. One of the five skills is hub-only, having no
  material that splits.

Both caps are bytes as `wc -c` counts them, whitespace included, about 5k and
10k tokens, enforced by `just check-size` in `just precommit`. Bytes are
indifferent to line length, so no reflow has to run before the count.

The reasoning behind the caps ships in `craft:plan-contracts` — they are a
rule about what a reader takes in at one go, not a quirk of this repository.

## Requirements

Claude Code. Nothing else: no runtime, no binaries on `$PATH`, nothing that
executes on your machine.

## Files touched on your system

None. The plugin ships markdown and reads nothing outside the session.

## Working on craft itself

`just precommit` is the gate and is required before every commit. It
hard-wraps the Markdown prose at 80 columns, checks references and file sizes,
then checks the skills, runs the skill checker's own test suite and parses the
manifest; those three skip
themselves while none of the files they read has changed since their last pass.

`just dogfood` copies the shipped files to `dist/plugin/`, and the `claude`
shim `direnv` puts on `PATH` launches Claude Code with that copy as its plugin
dir, so a dev session runs the in-tree plugin rather than an installed one. A
skill edit reaches a session after the next `just dogfood` and relaunch.

`plugin-dev/` is a vendored subtree of the shared release toolkit. Never
hand-edit it: fix upstream, cut a `dist-` tag, and re-pull with
`just update-plugin-dev`.

Development: what craft is, how it is built, and why — requirements,
architecture, decisions with their rejected alternatives, and the known
limitations — is in the
[design document](https://github.com/ddaanet/craft/blob/main/docs/design.md).

## License

MIT
