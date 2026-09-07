# The state layer

The six sections say what the system is and why. They do not say what is true
*right now* or how much to trust it, and a snapshot that omits that tells a cold
reader nothing about where the code is, what is live, or what the next action
is. Five additions carry that, and they sit around the six rather than inside
them.

1. **A `Status:` line and a `Verified against: <commit> (<date>)` stamp** at the
   top. Every state claim in the document is anchored to that commit, so a
   reader knows what to `git diff` for drift. Point-in-time "Done" rots without
   it.

2. **Now** — the resume pointer: Focus / Next / Do-not-re-litigate. The single
   highest-value section; without it the next action is only inferrable from
   limitations plus changelog.

3. **A status legend** — fixed vocabulary, so "Done" means one thing.

   - `Done` — implemented and pinned by a test.
   - `Done (prose)` — instructions, not code and not tested.
   - `Partial`.
   - `Planned`.

4. **A `Where · pinned by` column** on the FR and NFR tables, mapping each
   requirement to its code symbol and the test that proves it. This turns the
   document into a navigation index and makes "Done" re-checkable rather than a
   bare claim. *Verify the symbols and tests exist before writing them* — never
   assert an unverified pin.

5. **Limitations** (inherent — *can't*) split from **Non-goals** (deliberate —
   *won't, for now*). Conflating them hides whether an exclusion is a hard wall
   or revisitable scope.

These are facts about the system's current state, so they belong to the design
doc rather than to any behavioral-rules file. They are a different axis from
project instructions, not a leftover bucket.

The status stamp is also where a genuinely mutable measurement goes when one has
to be recorded at all — it is read as of-a-moment by construction, which the
design record is not.
