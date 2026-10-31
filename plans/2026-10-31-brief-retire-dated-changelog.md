# Brief: design-doc-writing stops prescribing a changelog

2026-10-31. From a claude-plugin-dev session surveying the changelog convention
across the ddaanet repos. A proposal, not a decision: my human partner proposed
it, nothing is ruled, and nothing here was edited. This is the main brief of the
set; each consumer's `inbox/` carries a shorter one.

## Proposal

Retire the changelog as a section of the living design: no
`docs/changelog/<date>-<title>.md` records, no `docs/changelog.md` index. The
living design stays as it is — present tense, rewritten in place. Commit
messages and `git log -- <path>` become the archaeology.

Why: a record restates its commit (claude-plugin-dev: 54 of 61 records landed
with the change they describe, six more came from splitting an old design doc);
the shared rule says a summary of a change points at the diff rather than
narrating it, and a record is a second summary; git already keeps "how we got
here", which this skill itself says ("Git history is already the full
changelog"); and the size check being designed in claude-plugin-dev loses its
one argued exemption.

What it does not cover: a record often holds reasoning its commit lacks.
Record-adding commits with no body: 30 of 61 in claude-plugin-dev, 20 of 93 in
handoff, 15 of 51 in shell-gotchas, 9 of 124 in gitlore. So the skill has to say
where the why goes instead — the commit body, or the node.

## Touch points in craft

`skills/design-doc-writing/`, the source of the convention:

- `SKILL.md:3`, the description: "the six sections" becomes five.
- `SKILL.md:8–13`: changelog as the sixth section, a separate file, then dated
  files past a size. Replaced by: history is git's; the doc names no file for
  it.
- `SKILL.md:25`: "add to the changelog and update the relevant section" becomes
  "update the section; the commit says why".
- `SKILL.md:31–49`, "Two documents, two jobs": becomes the design and git
  history. The status lines, `(implemented …)` tags and "this retired X"
  narratives it calls changelog material go to the commit message, a task file
  or a plan.
- `SKILL.md:79` and `references/state-layer.md:3`: "the six sections".
- `SKILL.md:91` and `references/writing-style.md:39–50`: the write-time-record
  vs current-truth split survives; its record examples become a commit message,
  a dated plan, a report. Line 71 and the "A commit message is exempt: it *is* a
  changelog" rule (83) stay true.
- `SKILL.md:103` and `references/maintaining-entries.md:75`: ids are cited from
  commits, plans and reports; "changelog entries" goes.
- `references/splitting-an-oversized-doc.md:49, 53, 78–79`: "six mandated
  sections" and the pointer-stub analogy to `changelog.md`.

Other craft skills that lean on it:

- `skills/directive-writing/SKILL.md:76–80` and
  `references/comments-and-changelogs.md` (title, 7, 12, 26–30): "the changelog
  gets the narrative" becomes the commit body.
- `skills/plan-contracts/references/before-you-plan.md:47, 54`: "a changelog" as
  an artifact with its own rules, and the renumbering instance that cites
  "changelog entries".

craft's own docs:

- `docs/changelog.md` (286 lines, inline entries) and
  `docs/design.md:8, 266–270`. `plans/` mentions are frozen.
- `plugin-dev/` (`check-refs.sh:227`, `README.md:235`, migrations) is vendored
  and changes only through a toolkit release.

No craft gate reads the changelog: `scripts/check-skills.py`, `justfile` and
`.rumdl.toml` name no changelog path.

## Out of scope

User-facing release notes. None of the 13 surveyed repos ships its changelog (no
`dist.include` lists one), and GitHub releases are cut with `--generate-notes`,
so no published release notes are affected.

## Open questions, each with a default

1. **Does the retirement cover inline single-file changelogs** — craft's own,
   plugin-craft's, prohibitions', sandbox-lies' — or only dated records and
   their index? Default: both; the skill decides it once, here.
2. **Where does the why go?** Default: the commit body for a design-significant
   change, and the node when a reader of the design needs it. This sits against
   the shared rule's "does not narrate"; the skill should say which why is
   narration and which is reason.
3. **Where does an inverted decision go?** gitlore moves retired decisions into
   a record. Default: deleted from the doc; the commit that deletes it says why,
   and the diff keeps the text.
4. **Records used as the argument layer.** handoff's design nodes link its
   records 120-odd times. Default: the skill says to fold a cited argument into
   the node before a record goes; a repo may keep existing records frozen.
5. **Measurements recorded "in the changelog at each release"** (sandbox-lies
   NFR-3). Default: a dated report under `plans/`, which the skill already names
   as where state lives.
