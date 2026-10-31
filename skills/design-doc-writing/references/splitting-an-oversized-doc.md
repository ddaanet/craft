# Splitting an oversized doc

Sentence-level trimming of narration has a hard ceiling — cutting further starts
removing the argument that stops a settled decision from being re-litigated,
which is the document's actual job (measured: ~5.6% before the ceiling). When a
living doc has grown too bulky to serve as loaded-before-touching-anything
context, measure per-section and per-decision byte totals before assuming the
fix is wording.

## Two shapes, two cuts

Two shapes come out of that measurement and they take different cuts.

**One entry dominates** — a decision that has become a subsystem rather than a
call (measured: one entry at 28% of the whole document, on par with all the
other decisions combined). Move its content into its own
`docs/references/<subsystem>.md` and shrink the entry to a motivation paragraph
plus a pointer.

**The distribution is flat** — the commoner case, and the one that defeats a
search for a dominant subsystem: a section is large because it enumerates many
small things, none over ~10%. Then the boundary is *need-time* — what a reader
needs while building or debugging one component against what they need to
understand the system — and it cuts across the doc's own headings rather than
along them. Measured on one project: an Architecture section split badly by
component and well by install-time-vs-design, and 25 decisions whose largest was
9% split into four need-time clusters, together taking the doc from 38 ktok to
22 ktok.

## What a split actually returns

Splitting *raises* total bytes; the saving is entirely in the reader not
following most pointers, so the cut only pays where skipping is safe. Measured
over one document's four passes: the graph grew 9.4% (58.5 → 64.0 ktok) while
the entry point fell 73% (56.8 → 15.2 ktok). The overhead is flat at ~1,650
tokens a pass — pointers, conclusion stubs, each node's own framing — so the
return is decided by how self-contained the moved material is, not by how far
along the split is. A cluster that moved whole returned 30:1; a mechanism that
had to be re-stitched with pointers from several places returned 2:1, and that
was the second pass of four, not the last. A ratio near 1:1 means the material
was never separable, not that the document has run out of room.

Every argument that leaves must leave a one-line statement of its conclusion
behind — a reader who cannot see that a decision was made re-litigates it, and
that failure is silent.

## The hub has a floor, and it arrives early

Once every mechanism has moved out, what is left is the five mandated sections,
a component map, one conclusion line per decision and one line per rejected
alternative — and none of it compresses. Rewording returns almost nothing:
measured in lines on one pass, the mandated sections reworded for concision came
back four lines shorter. So budget the hub by *measuring* after the planned
moves rather than estimating: one plan's estimate was 96 lines under on
Architecture alone, which turned "a light concision pass" into two unplanned
moves.

Demoting the conclusion lines into each node's opening summary is not a lever,
though the coverage rule accepts it: a reader weighing a new decision needs
every conclusion and every rejected name in front of them, or they traverse the
graph before they can decide. What does work at the floor is folding the
rejected-alternative names under the decision group they protect (one *Rejected*
line per group, no separate index) and rewording each conclusion to fit one
wrapped line.

Collapse restatements before cutting anything. The tell for a hub past its floor
is a section that restates a node instead of summarizing it; on one project two
sections both restating the same install-time node became one paragraph. That is
noise reduction and stands on its own — the audit below is the structural move.

The last lever is inside the conclusion bullets themselves. A bullet that has
grown carries argument alongside its conclusion: the mechanism, the bug that
motivated it, the "because" clause, the measurement. That material is read when
weighing or changing that one decision, which is a need-time seam; the
conclusion is read on every trip. So once every mechanism section has moved,
audit each bullet and move every clause that argues rather than concludes into
the node that owns the decision, leaving the conclusion, its invariant and the
pointer. The floor is then one line per decision with no argument in it.
Measured on one project, that pass over 67 hub bullets landed the hub under its
cap.

The conclusions themselves never leave the hub — neither one by one into each
node's opening, as above, nor wholesale into a decisions file the hub points at.
Together they are the system overview, and they are all that has to be true. A
decisions index read whole on the way to any decision is the hub under another
name: the cut satisfies the cap without reducing what is read. A hub still over
its cap at the floor has a group that has become a subsystem, which takes one
hub entry for the cluster while its sub-decisions conclude in its node — the
invariant §What the checker enforces states.

A hub at its cap is never a reason to leave a new conclusion out — by that logic
nothing could be added again. It is the signal to move the largest hub-only
detail (a requirement carrying its own measurements, say) into a node, verbatim,
and leave the requirement and its lever behind.

## A split ships with its loading instructions, or the nodes go unread

A `docs/references/` graph only pays if the agent opens the node before it
touches the mechanism, and nothing in Claude Code loads a node for it: the hub
is what gets read (or `@`-imported), and a pointer inside a section the agent
skimmed is not a trigger. So the split is not done until two files carry the
instruction.

- **The hub's opening states the shape**: "this document is a hub;
  `docs/references/` holds one node per mechanism; read the node before making a
  claim about, or changing, the mechanism it argues". Every requirement and
  decision stub names its node inline, so a reader at the FR is one hop from the
  argument.
- **The repo's `CLAUDE.md` carries a routing table** from what the agent touches
  to what it reads first: code symbols, FR ids and decision ids in one column,
  the node path in the other, plus the commit rule (hub conclusion and node
  argument change together). Symbols are the load-bearing column — an agent
  about to edit `_worktree_root` matches on the name, not on a prose description
  of worktree handling.

Whether an always-on instruction reliably causes the read is not established; it
is the current mechanism, and the routing table is the part that has the best
chance because it matches the token the agent is already looking at.

Enforce the graph's shape mechanically alongside: a gate that fails a hub or
node over the size cap (20000 bytes, `check-size`) and any pointer that stops
resolving. A formatter is not needed for the count, since bytes ignore line
length; if the repo wraps prose anyway, `rumdl` with MD013 reflow at 80 columns
does it without changing what the markdown renders to.

Establish that claim for any markdown re-serializer — a wrapper, a formatter, a
converter — by rendering every file to HTML with cmark-gfm before and after, and
diffing the results whitespace-collapsed. A text diff, even token-level or
whitespace-insensitive, passes changes that alter rendering: a line broken
before a `>&2` or a `+ …`, in plain prose or inside a code span, so it opens a
blockquote or a list item; a sentence split inside a heading or a table cell; a
code-span edge space dropped. The render diff also surfaces markdown that was
already malformed — a three-backtick fence nested inside another — which every
re-serializer reinterprets differently. That is a fix to the source, not a mark
against the tool.

## The class that leaks is pointers to open work

Not argument and not mechanism: those have sections that carry them into a node
whole. A lead — "`bats -T` reports per-test timings, so the breakdown comes
free" — attaches to whatever paragraph states the problem and survives only if
that paragraph travels verbatim. A compressed tail drops it with no trace.

Audit for it by splitting the pre-split doc into sentences, discarding those
found verbatim anywhere in the new graph, and ranking the remainder by how much
of their distinctive vocabulary (backticked identifiers, long words) survives.
Measured over one four-pass split: 852 sentences, 245 rewritten rather than
moved, 12 under 85% vocabulary coverage, and exactly one genuine loss — the rest
being museum narrative whose load-bearing half survived, corrections of prior
belief, or claims that survived compressed.

Numbered sub-decisions inside a moved cluster still resolve as bare citations
(`D26`, `D30`, …) elsewhere in the living doc; a reader who does not know where
one lives finds it one hop away, from the hub entry.

## What the checker enforces

Past a few reference files the crosslinking is load-bearing and nothing enforces
it: a decision with no stub line, or a pointer that stops resolving, needs a
checker.

The invariant that checker enforces is
**a conclusion is reachable before its argument**, not
*every decision has a hub line*. A cluster that has become a subsystem takes one
hub entry rather than one line per sub-decision, and its sub-decisions conclude
in the moved file's own opening summary — the stricter reading flags the whole
cluster. Only the hub's own bullets are required to point at an argument that
exists somewhere.

Worth checking alongside: that each reference file's heading enumeration matches
the bodies it actually holds, since a stale enumeration reads as coverage.

## Reviewing the result

Do not commit a large planning or design document and ask for a look-over. Large
docs hide errors in volume, and reviewers — human or LLM — skim instead of
inspect. One measured instance: a ~680-line plan drew exactly one annotation on
its first review pass, and the reviewer said afterwards they "should have looked
for changes and did not". The volume defeated the review.

- Before asking for a review, do a fresh-eyes pass first and
  **flag specific high-risk sections**: concrete shell snippets, cross-repo
  paths, file lists, anything that requires checking against the world rather
  than reading prose. "Lines X–Y do Z — worth verifying" beats "review the whole
  plan."
- For doc edits, prefer a revision-only diff (`HEAD~1`) over a cumulative one
  (`HEAD~N`) when the reviewer only needs to verify a targeted change.
- Split structurally: spec in its own commit, implementation plan in its own.
  Smaller diffs review better than one large drop.
- A spec self-review step exists for exactly this reason — do it with rigor
  rather than ticking the checkboxes.
