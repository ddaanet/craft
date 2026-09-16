---
name: directive-writing
description: "Write text an agent will act on — a hook's additionalContext, a probe directive, an instructing error message, a deny reason, a code comment — so it carries acts and not narration, and withholds identifiers instead of forbidding them. Use when authoring or reviewing agent-facing output, hook wording, dispatch text or comments, or when designing where a generator's output gets constrained. Not for user-facing prose."
---

# Directive writing

When authoring text a script emits *for an agent to act on* — a probe directive,
a hook's `additionalContext`, an error message that instructs — include only the
acts the reader performs.

Mechanism a reader cannot act on does not sit inert: it gets verified, narrated
back, and worked around. Guidance restating a condition the reader has already
satisfied asks a question whose only possible answer is narration. Measured
instance: a `with-commit` memory directive shipped as five paragraphs explaining
a pre-commit hook, gitlink staging, mtime freshness, and an explicit "do NOT
write `<sentinel-file>`". The reaction: "This is still saying much more than the
agent needs to know. That kind of prose leads to annoying verbosity when the
agent narrates the superfluous checks."

## The five cuts

- **Mechanism.** What the receiving system does with the file, which hook
  consumes it, the mtime freshness rule behind an ordering, a gitlink being
  staged. State the ordering; never the rule that motivates it.
- **What an earlier step already settled.** If the skill body sequences memory
  before the probe, the probe must not re-order them.
- **A meta-description of the constraint.** "no second file, no trigger" was a
  note about what the text must *avoid*; it got literalized into the text.
- **Rationale for why the mode exists.** The reader is executing, not reviewing
  the design.
- **Prohibitions naming a thing the reader could not otherwise reach.** This one
  has its own test, below.

Keep **one clause of reassurance** where the absence of a visible result would
otherwise read as failure — "the commit that lands these changes carries the
memory" — because that prevents an invented recovery. Make it true of every flow
the mode covers: the first draft said "this turn's commit", false wherever the
commit arrives in a later user turn.

**A transform is described by its input, never its output.** Where a tool
rewrites what the agent writes, the agent sees the rewritten form everywhere
else and can imitate that instead. Measured: told "conventional-commit prefixes
are rewritten with emoji on commit", an agent facing an all-emoji `git log`
wrote the emoji itself, and the hook rejected it. State the form to write —
"prefix with `feat:`, `fix:` …; the hook adds the emoji".

## Withhold, don't forbid

When the only route to an unwanted action is an identifier — a filename, a flag,
an endpoint — the reader has no other source for, **withhold it**. Naming a
sentinel file to say "do not write it" hands a fresh agent the exact string that
triggers the behaviour the mode exists to prevent. The prohibition also
*introduces the concept*, and an introduced concept gets reasoned about.

Withholding is not politeness — it is what makes the action unreachable. The
counter-argument ("a reader who already knows the protocol needs it forbidden,
not omitted") assumes a rare reader and pays for it with the common one;
maintainer docs like a project `CLAUDE.md` are not in a foreign project's
context.

**Ask who else could supply the identifier.** Nobody → say nothing. Only when
the reader demonstrably already has it — it appeared earlier in the same context
— is a prohibition worth its cost, and then forbid by role rather than by name.

## Distributed text never cites private files

A skill body or agent definition ships to consumers who do not have the author's
notes; a private file named there dangles for every one of them. Inline the
needed criteria into the agent's own text or reference material at write time.

Plan-scoped artifacts — a recall artifact under `plans/<job>/`, a dispatch
prompt naming paths — are the channel for by-path references. They live with the
plan, not with the plugin.

## Code comments take the same cut

Against a different bar:
**what a maintainer needs in order to change the code safely.** Where a repo
keeps its design history in a changelog, comments drift into retelling it — the
defect that motivated the shape, what an earlier draft said, a clause defending
the choice against an alternative.

The rule, the constraint and the contract stay; the story, the incident and the
self-commentary belong to the changelog, which is where a reader who wants them
is already headed. Rationale a maintainer needs in order not to break the code
is not narration: "the arrays expand this way because bash 3.2" stays.

"Remove narration" is the instruction that makes the cut.

## One change, four artifacts, one telling

A change that touches code, tests, a changelog entry and a design doc invites
writing the incident into all four, and each copy reads as reasonable in
isolation.

- The **changelog** gets the narrative — it is the write-time record.
- The **design doc** gets the standing rule, in present tense.
- The **code and test comments** get the constraint alone.

Watch for a signature phrase recurring across them: "load-bearing", "the shape
of", "by construction" carry real meaning the first time and become verbal tics
by the fourth, at which point they read as emphasis substituting for content.
Grep the diff for recurring favourites before committing.

## How to apply

Draft the directive, then **delete every sentence that is not an act**. Ask what
a reader would *do* with each remaining line; if the answer is "check it" or
"explain it back", cut it.

Test the negatives on the whole word (`[[ "$output" != *"trigger"* ]]`) and pair
each with a positive over the same fixture — see the `test-discipline` skill.

When a rule is an ordering between the *caller's own steps*, it belongs where
the steps are described: a prohibition must be front-loaded, a procedure defers
to its trigger.

## Wording by channel

### The user-facing channel: curt and informative

`systemMessage` and similar user-facing output: **lowercase, em-dash separator,
factual, no instructions or actionable phrases.** One short line — enough for
the user to know what happened, no more. No "to fix this, run X"; that is the
agent's job via `additionalContext`, not the user's.

- `handoff loaded — 3.2 KiB, saved 8m ago`
- `handoff: wiped prior handoff-task.md, handoff.md`
- `handoff extracted to /path/to/handoff.md`

**`systemMessage` renders ANSI escapes rather than showing them as literal
bytes.** So a hook that speaks only when something went wrong can lead its line
with a style reset (`$'\033[0m'`) to escape the dimming applied to ordinary hook
chatter. Curt and informative still governs the words; this is only about not
being rendered as noise.

### An agent-facing DENY: no actionable phrases

When `permissionDecisionReason` — or any agent-facing message — denies a tool
call, never include phrases like "stop and report it to the user" (the agent
tries to invoke a reporting tool), "if you really need X, run Y" (the agent
treats it as authorisation), "revert via git rather than editing here" (the
agent runs git revert), or the canonical "remove the lock if stale" (the agent
removes the lock immediately).

Agents lack the contextual filter that lets a human read diagnostic prose as
descriptive rather than prescriptive.
**Any imperative phrasing in a deny-reason gets executed literally.** Even when
the work is correctly in a hook, the *wording* of agent-facing output still
needs care.

Phrase deny reasons as unconditional refusal plus a redirect to the legitimate
path: "the release recipe owns this — invoke it instead of editing the file."
Never offer escape hatches the agent can self-authorise. Put human-facing detail
in a separate curt `systemMessage`. Writing "if you … then …" in an agent
channel means rewriting it as "do not …".

### Scope: this rule governs DENY channels, not DIRECTIVE channels

A `PreToolUse` deny is meant to *stop* the agent, so any actionable phrase is
harmful. But `additionalContext` used as a *directive* — where the whole point
is that the agent acts, presenting a line to the user or summarizing and
committing per a probe's output — is the opposite case:
**imperative wording is correct and required there.** Do not over-apply.

The tell: is this channel trying to **halt** the agent (deny → descriptive only)
or **drive** it (directive → imperative is fine)? A reviewer once flagged a
`/rename` `additionalContext` as a violation; it was not — that channel directs
the agent to relay the line, and the probe's own summarize → approve → commit
directive is equally imperative by design.

## Where to constrain a generator

For constrained agent output, let generation be **loose** — scaffolding tokens,
priming labels like `**Analysis:**` — and enforce output constraints via a
separate post-hoc pass using the full generated context.

Training pressure against scaffolding forces the generator to either compensate
with silent reasoning, at extra cost, or produce lower-quality output.
Scaffolding is not waste: it is the attention mechanism doing its work, and the
priming label is attention drafting the content that follows. Separating
generator from validator follows the compiler model — parsing versus
typechecking. Do not conflate them.

**When designing agent workflows that produce artifacts, do not try to suppress
scaffolding at generation time.** The agent drafts freely; cleanup, linting and
review apply at the **artifact boundary** — file write, commit, user
presentation. Self-review is the cheap form; a separate lint is the thorough
form.

Exception: derived artifacts — a compressed summary built from context already
present, such as a commit message — need none of this. They are already
compression rather than fresh generation, and the compression *is* the review.
