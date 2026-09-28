# Changelog

Design-significant changes only: decisions reversed, subsystems built or torn
down, requirements added or dropped, a rationale that turned out false. Git
history is already the full changelog and needs no duplicate here. An entry
earns its place by answering a question a future reader would otherwise ask of
[the design](design.md) and find no answer to.

## 2026-09-28 — `test-discipline` stays out of live probes

A brief proposed extending the pairing rule in `non-vacuous-negatives` to a
guard verified by a live probe — a hook, a sandbox rule, a subagent's
containment — with a must-allow command beside the must-block one, a probe that
is harmless if the guard is dead, and reading the probe's tool result rather
than the agent's report of it. Rejected. Pairing in that node exists because a
suite's negative goes stale silently as the code moves; a probe runs once
against the system as it is, and a guard broken closed announces itself by
refusing legitimate work. The one non-obvious claim, that an agent cannot
witness its own containment, is dispatch evidence rather than test evidence, and
stays in the memory fact about frontmatter hooks, keyed to the symptom that
leads a session to it. The skill already sends a hand-run validation to the
suite rather than teaching how to run one.

## 2026-09-26 — the dev launcher loads a copy of the plugin

`.bin/claude` used to pass the repo root as `--plugin-dir`. Claude Code treats
every path under a `--plugin-dir` root as a sensitive file, so every Edit or
Write in the tree asked, auto mode's classifier gave no verdict on any of them,
and a dev session could not edit its own repo. The launcher now copies the
manifest and `skills/` to a gitignored `dist/plugin/` at each launch and points
there, at the price of a skill edit reaching only the next session. This is a
stopgap: the shared toolkit is building a dist-copy launcher that syncs on edit,
and craft's shim goes when that ships.

## 2026-09-25 — the state layer drops the status stamp and the resume pointer

`design-doc-writing` no longer asks a design doc for a `Status:` line, a
`Verified against: <commit>` stamp or a Focus / Next section. A brief from
another repo showed all three stale two releases on, and this doc had the same
fault: it said v0.1.0 with v0.2.0 tagged. The skill already argued that
refreshing a mutable figure schedules the same correction again, while naming
the stamp as where such state belongs; the stamp was that argument's own
counterexample. The node now states the test that decides which state stays —
the edit that falsifies a claim has to touch it — so per-requirement `Done`
markers and their pins stay, and release state, next action and anchor commit go
to tags, the task frame or a plan, and `git log`. `Do not re-litigate` survives
as a line under the title, since it names decisions rather than state.
*Rejected: keeping the stamp for projects without tags or a task frame* — a
dated plan is always available, and the rot does not depend on whether another
home exists; *a refresh rule* — the correction the skill already rejects.

## 2026-09-25 — `directive-writing` splits out its comments node, and the cut reaches plan vocabulary

The comments cut now covers runbook item and slice ids and `file:NNN` line
numbers: the id names an artifact that lives with the plan while the code
outlives it, and the line number goes stale at the next edit. The brief's
explanation of why subagents write them — the dispatch as the agent's vocabulary
for *why* — was dropped as an unchecked mechanism claim; only the observation
ships. Its sweep was rewritten before landing: the brief's pattern matched bare
`slice` (array slicing), caught only `.bats` line numbers and named a `memory/`
path the hygiene gate refuses; the shipped one scans the staged diff's added
lines and was checked against a fixture of five bad and four clean lines.

The addition would have pushed the hub past its 200-line cap, so the two comment
sections — the maintainer's bar and one telling across four artifacts — moved to
`references/comments-and-changelogs.md` with the sweep, a moment of their own at
pre-commit review. Only `removing-cleanly` is now hub-only.

## 2026-09-25 — `spec-hygiene` widens from call-site lists to any claim a spec makes

Two briefs shared one mechanism: every artifact downstream of a spec is a
faithful transformation of it, so a review of the returned work confirms only
conformance, and a wrong spec passes every layer. `spec-hygiene` now covers
three claims queried rather than carried: a call-site list by grep, a claimed
duplicate by `diff` (with substantive differences declared and the replacement
scoped to the block's line range), and a contract sentence by the case table of
whoever enumerates the cases, since it reaches the docstring verbatim and code
review reads code against it. The brief's writer-side rule, to check a contract
as a standalone proposition, was dropped as a restatement of being correct. The
description gains collapsing passages claimed to be duplicates, the moment the
`diff` rule is for and one no plan-writing trigger names.

Its dispatch incident was aimed at `directive-writing` and lands in
`contracts-and-size` instead: a directive specifying `line.strip()` stated a
function body where a contract over inputs belonged, so it is a second measured
case of the contract form catching what code hides. The general form it offered
without a home — a fix narrowing a guard by normalizing re-opens the defect one
step along — joins `non-vacuous-negatives` beside the decoy rule, whose shape it
is: the row past the boundary is the one where the two implementations disagree.

## 2026-09-25 — `removing-cleanly` absorbs the reference-audit fact

A brief proposed generalizing the derived-figures paragraph from figures to
forms: pointer verbs, caller enumerations. Dropped. Its stale caller count was a
numeral the change moved, which the paragraph already covers, and its drifted
pointer verb was a `directive-writing` defect the sweep happened to find, not a
dependent of the removal. Its open question landed instead: the shared-tier fact
saying a stale-reference sweep runs over the whole tree with every hit
classified, never over the diff under review, fires at the moment this skill
does and now lives in it. The fact is retired and joins `SOURCE_FACTS`, and the
description gains splitting a module and renaming a symbol, the moments the fact
fired on that no removal trigger named.

A second brief, on checking a dedup's premise by `diff`, was aimed here and
belongs to `plan-contracts`: its trigger is a plan claiming two passages are the
same, and its rule is `spec-hygiene`'s claim-about-the-corpus rule with `diff`
as the query. It waits in the inbox for that group.

## 2026-09-24 — three `test-discipline` briefs, and the matrix-staleness rule rejected

Two briefs proposed that a mutation matrix describes the bytes it ran against:
run the mutations last, re-run after any later edit, re-run an inherited matrix
before believing it, and re-confirm the same test reds after a
behaviour-changing edit. Rejected. The proof a mutation run gives is
behaviour-bound — the test discriminates a behaviour, and a later green run
shows the behaviour is still there — so a later edit invalidates it no more than
it invalidates any other test in the suite. What is byte-bound is the recipe:
the string pair or comment naming the mutation, which a later edit can move out
from under. A stale recipe re-applied neuters nothing, and the survived mutation
reads as a vacuous test, which is what the instance behind the rule actually
was. `genuine-red` now says to prove a mutation landed, symmetrical with proving
the restore, and names the stale recipe as the reading to check before the two
`non-vacuous-negatives` gives a survived mutation.

Taken besides: a red is evidence for the one assertion it landed on, the
assertions below it being born green in a test that passed its red step; a
mutation's red must be a failed assertion, not a setup exception; and the
vacuous-green catalogue gains end state standing in for the moment. Dropped as
already implied: asserting a fixture property rather than trusting a helper's
name, since the pairing rule catches the drift; mutating a pass-through fixture
value, since the node already says to mutate the subject; and a refusal's
message as a behaviour of its own, which is the born-green-assertion point from
the other side. The gitlore brief stays in the inbox for its `directive-writing`
section.

## 2026-09-17 — dogfooding `directive-writing` on text that had already fired

The skill was run against agent-facing text whose effect on an agent had been
observed in the same session, rather than reviewed cold: a deny from a `git add`
guard, a memory tool's SessionStart context, and a commit-msg hook's
SessionStart context. Each finding went to its own repository as a brief. One
fed back: the commit-msg context described its rewrite ("prefixes are rewritten
with emoji"), and the agent, facing an all-emoji log, wrote the emoji itself.
The five cuts did not cover a directive describing a transform by its output, so
the skill now says to state the input form. The checker's own comments took the
code-comment cut in the same pass.

The skill did not fire on the two dispatch prompts written that session,
although its description names dispatch text. That is recorded against L-2, not
fixed: one miss does not say whether the wording or the boundary is wrong.

## 2026-09-17 — dogfooding `plan-contracts` and `removing-cleanly` fed two gaps back

The plan that removed `attribution` and gave failures a line was the first live
run of both skills, and each let one thing through. `removing-cleanly`'s sweep
greps for the removed thing's name, and the test count the removal changed does
not contain it; the skill now says to grep for the figures a removal changes and
re-derive them. The outline told execution to renumber Limitations, which
`design-doc-writing` forbids, because it was written without loading that skill;
`plan-contracts` now says to load the skill governing any artifact a plan edits
and check each step against it. Both land where the miss happened rather than in
the skill that was contradicted, which already said the right thing.

## 2026-09-17 — failures name a line, closing the old L-1

L-1 was that `blank_code`'s line-preservation could not be observed: it
substitutes spaces for code so that a failure would name the right line, and no
failure named one. `wikilink`, `private-reference` and `broken-link` now report
`path:line:`, and a test puts a fence above a wikilink so a `blank_code` that
deleted instead would report the wrong line — verified by making that mutation
and watching exactly that test fail. `private-reference` became per occurrence
on the same ground: once per pattern hid every hit after the first. The
frontmatter checks and whole-file checks keep `path:`, having no line worth
naming. L-1 is retired and its id left unused.

## 2026-09-17 — the `attribution` check is removed, as wrong policy

The checker failed any body saying "my human partner", on the theory that the
phrase names somebody a reader does not know. That is backwards: the phrase is
house policy, because "user" already names whoever uses the software being
built, and the collaborator needs a name of its own. The check was found while
grounding L-1 — a reflow could split the phrase across a newline and disarm the
substring match — and removing it replaces hardening it. Recorded as D-10.

## 2026-09-08 — dogfooding `test-discipline` fed a gap back into it

Writing the checker's suite was the skill's first run against live work, and it
found the skill covering only half its own subject. `genuine-red` prescribed
stub-then-assert, which presumes the code does not exist yet, and noted in
passing that a suite validated against a finished implementation "has to
manufacture the absence the ordering would have given" — without saying how.
Everything the suite actually needed was in that unwritten half: one mutation
per behaviour, the whole suite run against each, and the three distinct things a
surviving or misdirected red tells you.

Added there rather than to the hub, and phrased to lean on the existing
mutate-in-place rule instead of restating it. The exactness requirement travels
with it: a test asserting only that the run failed survives the mutation of its
own check whenever the fixture trips a second one, which is why the suite
asserts complete output.

## 2026-09-07 — the checker gets a suite, and the gate stops being sub-second

L-1 was the last thing the design doc named as unpinned: eleven checks gating
every requirement, and nothing showing that any of them would fail if it
regressed. The suite closes it with one test per check, each spoiling an
otherwise-clean tree in exactly one way and asserting the *complete* output
rather than the exit code — a test that only asserted "something failed" would
pass just as well when a different check fired on an accidental second defect.

Thirty tests, all green the first time they ran, which is no evidence at all
that they discriminate. A mutation pass supplied the missing red: each check was
neutered in turn in a copy of the checker, and every one of the thirteen
mutations turned the test named for it red. No mutation survived.

The suite runs in `precommit`, which takes the gate from well under a second to
around six. NFR-3 was rewritten rather than quietly left standing: the property
that lets the gate be unconditional is that it has no cache and no sentinel, and
a sub-second figure was never what bought that. The cost is thirty subprocess
spawns, which is the price of running the checker the way `precommit` runs it
instead of importing its functions.

L-1 is now a different limitation. `blank_code` substitutes spaces for code
rather than deleting it, so that a failure message would name the right line —
but no check reports a line number, and the one line-derived figure counts the
raw text. Nothing can tell the implementation apart from one that deletes. The
behaviour stays; what is missing is the seam that would let a test see it.

## 2026-09-07 — the living design doc, and the gate widened to cover it

Craft shipped `design-doc-writing` and had no `docs/design.md`. Writing one from
the skill was the first real dogfooding pass, and it found two gaps in the
plugin's own tooling: `just format-docs` wrapped `skills` and `plans` but not
`docs`, and `scripts/check-skills.py` capped skill bodies but nothing else. A
design doc that is neither wrapped nor capped cannot obey the rule its own skill
states, so both were widened (D-9).

Every requirement is pinned by `just precommit` rather than by a unit test, and
that is what a pin is for: the gate re-checks the claim on every commit, which
is the property that makes a `Done` more than an assertion. What stays unpinned
is the checker itself, which has no test suite, so nothing shows a check would
fail if it regressed (L-1).

## 2026-09-07 — two inbound briefs applied to `design-doc-writing`

FR and NFR rows were named as an example of genuinely tabular data. They are
not: a requirement stated as a sentence is neither short nor uniform, which is
the test the section already gave. The error had two carriers — the
prose-over-tables rule and the state layer's `Where · pinned by` item, which
prescribed a *column* — and fixing one alone left the skill contradicting
itself. The requirement sections in this design doc are the corrected form.

The same pass added the decisions index to the levers available at a hub's
floor: the `## Design Decisions` heading is a need-time seam, so the conclusions
can move whole into a `docs/decisions.md` while the hub keeps its six sections
as pointer stubs. Recorded as a lever rather than a default shape, because it
does not pay the way other splits do — nobody skips a decisions index, so the
saving is in *when* it is read, not whether.

`inbox/` became a tracked directory in the same commit, and
`brief-craft-seed.md` moved off the repo root where it read as a tracked project
document (D-8).

## 2026-09-07 — five skills seeded, twenty memory facts retired

The plugin's reason to exist: guidance that a private memory store already
encoded but structurally could not deliver. A memory fact is retrieved by
matching an index line against a symptom, which never fires on a *moment* — "you
are about to write a design doc" routes to nothing. A skill description names
the moment.

Twenty source facts were rewritten into five skills and deleted from the store
in the same pass, so there is no second copy to drift. Their names survive in
`SOURCE_FACTS` in the checker, where a surviving mention in a shipped body is
now a dangling private reference rather than a citation (D-4).

`scripts/check-skills.py` and the rumdl reflow pass were built alongside, for a
failure mode that is leakage rather than breakage: a wikilink or a `memory/`
path does not stop a skill loading, so nothing but a gate reports it.

## 2026-09-02 — plugin stubbed and the release toolkit vendored

`.claude-plugin/plugin.json`, the justfile, and `plugin-dev/` pulled in as a git
subtree from a pinned `dist-` tag. Vendoring rather than depending: the release
recipe has to work in a repo that has never been released, which a runtime
dependency resolved from a marketplace cannot guarantee.
