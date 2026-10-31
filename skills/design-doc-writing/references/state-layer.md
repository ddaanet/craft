# The state layer

The five sections say what the system is and why. They do not say how much to
trust each claim, or which questions are already closed, and a cold reader
cannot tell a pinned requirement from an aspiration or a settled decision from
an open one. Four additions carry that, and they sit around the five rather than
inside them.

1. **A `Do not re-litigate` line** directly under the title, pointing at the
   decisions a new session is most likely to reopen. It names design decisions,
   not state, so it cannot go stale the way a status line does.

2. **A status legend** — fixed vocabulary, so "Done" means one thing.

   - `Done` — implemented, and pinned by something that re-checks the claim on
     its own: a test, or a gate that runs over the real tree on every commit.
     What makes a pin a pin is the re-check, not which of the two it is.
   - `Done (prose)` — instructions, not code and nothing re-checking them.
   - `Partial`.
   - `Planned`.

3. **A `Where · pinned by` clause** on every FR and NFR entry, mapping each
   requirement to its code symbol and to whatever proves it — a test, or the
   gate check that would fail if it regressed. This turns the document into a
   navigation index and makes "Done" re-checkable rather than a bare claim.
   *Verify the symbols and the pins exist before writing them* — never assert an
   unverified pin. A project whose requirements are all pinned by one gate still
   owes that gate its own pin: a check nothing tests is a `Done` resting on an
   untested claim, and belongs in Limitations until it has one.

4. **Limitations** (inherent — *can't*) split from **Non-goals** (deliberate —
   *won't, for now*). Conflating them hides whether an exclusion is a hard wall
   or revisitable scope.

These are facts about the system, so they belong to the design doc rather than
to any behavioral-rules file. They are a different axis from project
instructions, not a leftover bucket.

## Which state stays

A state claim belongs in the design doc only when the edit that falsifies it has
to touch it. A requirement's `Planned` becomes `Done` in the commit that
implements it, which edits that entry anyway, and a `Done` is re-checked by its
pin. A release status, a next action or a checked-against commit changes by
tagging, by finishing work or by the next commit — none of which touches the doc
— so each is stale from the moment the world moves on.

So the doc carries no `Status:` line, no `Verified against: <commit>` stamp and
no Focus / Next resume pointer. Each already has a home that updates itself or
is read as of-a-moment by construction: release state in git tags and the
distribution channel, the next action in the task frame, handoff or a
date-stamped plan, and the doc's own age in `git log` on the file. Refreshing
them by hand schedules the same correction again.

Measured instance: one plugin's design doc still read
`Status: seeded, unreleased` two releases later, anchored to a commit before
either, with a Next line asking for the first release to be cut. Nothing in the
doc had changed but those lines.

Dates that ground a claim are a different thing and stay — "verified against CC
2.1.150" supports the claim beside it rather than describing the doc.
