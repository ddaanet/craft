## Brief: the state layer asks a design doc to duplicate state that goes stale

2026-09-17

Concerns `skills/design-doc-writing/references/state-layer.md` and the line in
`skills/design-doc-writing/SKILL.md` that names "the doc's status stamp" as a
place state lives. Arrived from the `plugin-craft` repo.

### What happened

`plugin-craft/docs/design.md` carried the state layer as the skill specifies it:

- `Status: seeded, unreleased.`
- `Verified against: <sha> (2026-09-03)`
- a `## Now` section with **Focus**, **Next** and **Do not re-litigate**

After the plugin shipped two releases (0.1.0 and 0.1.1), the top of the doc
still said it was unreleased. It pointed at a commit from before either release,
and its Next line asked for the first release to be cut. Nothing in the doc had
changed except these lines.

Asked whether to refresh them, my human partner ruled: remove redundant
descriptions of state that can go stale, instead of updating them. The status
line, the stamp, Focus and Next were deleted. The `## Now` heading went with
them, and the Do-not-re-litigate line moved directly under the title.

### Why they were redundant

Each fact already had a home that updates itself or is read as a snapshot:

- **Released or not** — git tags and the marketplace entry.
- **What is in flight, what comes next** — the session task frame or handoff,
  which is read as a snapshot by construction.
- **Commit the doc was checked against** — a volatile sha. The shared ddaanet
  conventions already ban this kind of state in memory files for the same
  reason.

### What was kept, and why

- **Do not re-litigate.** It points at design decisions, not at state, so it
  cannot go stale.
- **Per-requirement `Done` / `Done (prose)` markers and their legend.** These
  are state too, but no other place records them, and each `Done` names the
  check that re-verifies it. My human partner has not ruled on them.

### Tension inside the skill

`SKILL.md` § "No measurement of mutable state" already argues that refreshing a
stale figure "schedules the same correction again". Yet it names the status
stamp as where such state belongs, and `state-layer.md` calls the stamp and Now
"the single highest-value section". The plugin-craft case is that argument
applied to the stamp itself: Status and Next went stale the same way a byte
count does.

### Constraints

- Not decided for craft. The ruling above covers plugin-craft's design doc; how
  the skill should change is for a craft session to put to my human partner.
- Keep the "Do not re-litigate" pointer in whatever shape results. It is the
  part of Now that does not rot.
- Grounded dates stay (FR-8-style "verified against CC 2.1.x" evidence). The
  target is the doc-level stamp, not dates that support a claim.

### Options seen, not ranked

1. Drop items 1 and 2 of the state layer except Do-not-re-litigate; send
   Focus/Next to the task frame and release state to tags.
2. Keep them, but only for docs without tags, releases or a task-frame
   mechanism, and say so.
3. Keep them and add a rule for refreshing them. This runs straight into the
   skill's own "schedules the same correction again" argument.
