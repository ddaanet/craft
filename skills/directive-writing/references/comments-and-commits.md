# Comments and commits

## Code comments take the same cut

Against a different bar:
**what a maintainer needs in order to change the code safely.** Where a repo
keeps its design history in commit bodies, comments drift into retelling it —
the defect that motivated the shape, what an earlier draft said, a clause
defending the choice against an alternative.

The rule, the constraint and the contract stay; the story, the incident and the
self-commentary belong to the commit body, which is where a reader who wants
them is already headed. Rationale a maintainer needs in order not to break the
code is not narration: "the arrays expand this way because bash 3.2" stays.

"Remove narration" is the instruction that makes the cut.

**Plan vocabulary goes too.** A runbook item or slice id (`Item 1.3`, "the GREEN
report") names an artifact that lives with the plan, and the code outlives it; a
`file:NNN` line number goes stale at the next edit above it. Subagent-written
comments carry both by default. State the constraint the id stood for, or cut
the clause.

## One change, four artifacts, one telling

A change that touches code, tests, a commit body and a design doc invites
writing the incident into all four, and each copy reads as reasonable in
isolation.

- The **commit body** gets the narrative — it is the write-time record.
- The **design doc** gets the standing rule, in present tense.
- The **code and test comments** get the constraint alone.

Watch for a signature phrase recurring across them: "load-bearing", "the shape
of", "by construction" carry real meaning the first time and become verbal tics
by the fourth, at which point they read as emphasis substituting for content.
Grep the diff for recurring favourites before committing.

## The sweep

Run over the staged diff's added lines, before committing:

```sh
git diff --cached -U0 | grep -nE '^\+.*(plans/|runbook|\b(Item|Step|Slice|Phase) [0-9]|\b(RED|GREEN)\b|\.[a-z]+:[0-9]+)'
```

Every hit is a candidate, not a verdict: a URL with a port (`host.com:8080`) or
a test named for its red phase matches too. Read each and keep what a maintainer
needs.
