# craft recommends rumdl without the evidence, and states a cap procedure its default setting breaks

2026-09-26 — from a `gitlore` session reviewing the `ddaanet` memory tier.

Two shipped sentences in craft assert behaviour that the memory fact
`ddaanet/markdown-formatter-choice.md` is the measured evidence for. One is
correct but unsupported; the other is incomplete in a way that makes the
procedure it prescribes give wrong answers under the tool craft recommends.

The memory fact is being retired down to its gate-wiring half, which fires when
a formatter gate misbehaves rather than when a document is written. The
doc-authoring half has no home once that happens, and craft is where it belongs:
craft is the plugin that recommends the tool and states the procedure.

## Defect 1 — the cap procedure is wrong under rumdl's default

`skills/plan-contracts/references/contracts-and-size.md`, "Measure the cap
honestly":

> Hard-wrap prose at the repo's convention first, **then** measure; if it
> exceeds the cap, split into multiple focused documents.

`reflow-mode` decides whether a rumdl pass normalizes the tree,
**and the default does not**. With `reflow = true` alone, rumdl breaks only
lines already over the column and leaves a paragraph hand-wrapped narrower
exactly as it is. Widths never converge. A document hand-wrapped at ~70 columns
came out 2 lines *longer* after the pass.

So "wrap first, then measure" does not produce a comparable number: prose
wrapped at 60 sits at roughly 1.3x the line count of the same words at 80. The
artifact fails a cap it should pass, and — the direction that matters more — a
file that passes the cap may never have been normalized at all, so the count
protecting reviewability was never measured against the convention.

`reflow-mode = "normalize"` re-fills every paragraph and is what a line-count
cap has to be measured against. Measured switching one tree: 85 lines changed
under the default, 276 across 31 files under `normalize`.

A second omission in the same section: a file carrying 150–300-character lines —
the gaming the section already warns about — gains most of its post-reflow line
count from the reflow itself, not from new words. Any ceiling has to be taken
from post-reflow counts, and the formatter check has to sit *ahead* of the line
guard in the same gate.

## Defect 2 — the render claim ships without its evidence

`skills/design-doc-writing/references/splitting-an-oversized-doc.md`:

> `rumdl` with MD013 reflow at 80 columns is the wrapper that does this without
> changing what the markdown renders to.

True as measured, and the sentence is the conclusion of a comparison craft does
not carry. The method that establishes it is the transferable part, because it
applies to any markdown re-serializer and not only to a wrapper:

**Render every file to HTML with cmark-gfm before and after, and diff the result
whitespace-collapsed.** A token-level or whitespace-insensitive text diff passes
changes that alter rendering — a line broken before a `>&2` or a `+ …`, inside a
code span or in plain prose, so it opens a blockquote or list item; a sentence
split inside a heading or table cell; a code-span edge space dropped.

The render diff also surfaces pre-existing malformed markdown — a three-backtick
fence nested in a three-backtick fence — which every re-serializer reinterprets
differently. That is a source fix, not a tool criterion.

Measured on ~100 files of design docs and plans, hard-wrapping at 80:

- **rumdl** (`enable = ["MD013"]`, `reflow = true`; `headings`, `code-blocks`,
  `tables = false` to silence what it cannot wrap): zero rendering changes on
  well-formed input, emphasis markers untouched, idempotent. Subject to the
  `reflow-mode` caveat above.
- **prettier** `--prose-wrap always`: rewrites `*em*` to `_em_` with no option
  to keep it; one bold whose first word was a code span starting `**` broke.
- **dprint** markdown (`emphasisKind`/`strongKind: asterisks`): keeps emphasis,
  but dedents fenced code block content to the fence's indent and strips a
  one-sided space inside code spans.
- **mdformat** (+gfm): `---` rules become underscores (hardcoded), ordered lists
  renumber to `1. 1. 1.`.
- **mdslw**, **remark** + `@webpro/remark-wrap-prose`: break inside code spans,
  headings and table cells, and wrap a prose line so it starts `+ …`, which
  re-parses as a list item and truncates the paragraph. prettier, dprint and
  rumdl all avoid leaving a list marker at line start. remark is not idempotent.
- **pandoc** `-t gfm --columns`: reflows and drops code fences, escapes `#` and
  `**`.

## What is proposed, as input

1. `contracts-and-size.md` names `reflow-mode = "normalize"` as the condition
   under which "wrap then measure" is honest, and states that the formatter
   check precedes the line guard in the same gate.
2. `splitting-an-oversized-doc.md` keeps its one-line recommendation and points
   at a reference node carrying the render-diff method and the comparison.

Whether the comparison table is worth a node at all is craft's call: it is spent
evidence for a decision already taken across the ddaanet repos, and its value is
in not re-running ~100 files of measurement if the choice is ever reopened. The
render-diff *method* is the part with ongoing use.

Measurements are against rumdl 0.2.74. Nothing here was verified against a newer
release.

## Not acted on from this side

No craft file is edited by this brief — the gitlore session that wrote it treats
other repositories as read-only. The memory-store half of the change (retiring
the fact down to its gate-wiring residue) happens in gitlore independently and
does not wait on a ruling here.
