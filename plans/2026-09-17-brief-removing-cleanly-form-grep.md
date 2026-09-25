## Brief: generalize `removing-cleanly`'s name-grep rule from derived figures to derived forms

2026-09-17

### Decisions

- The rule belongs in `craft:removing-cleanly`, not in a memory fact. It was
  first written into the `ddaanet` tier and withdrawn: per
  `gitlore:memory-writing` §1.2 a memory repeating what another artifact owns is
  in the wrong home, and this skill already states the mechanism at the moment
  it matters — during a removal.
- The existing paragraph stays and becomes the first case of a two-case rule.
  Nothing about derived figures is wrong; it is stated for one dependent class
  and the mechanism covers more.

### The paragraph this concerns

`skills/removing-cleanly/SKILL.md`, under §How to apply:

> **A grep for the name misses every figure derived from it.** "Eleven checks",
> "thirty tests", a file total: none contains the removed thing's name, so each
> survives the sweep and goes stale on the commit that lands. Grep for the
> number words and numerals the removal changes, and re-derive each from its
> source — collect the suite, count the list — rather than decrementing, since a
> removal rewrites some dependents and deletes others.

### Evidence

From edify, retiring a routing verdict's name from a skill's prose. A sweep
required every whole-tree hit of the retired name classified accurate or stale.
A review found three live hits classified nowhere; the proof pass that followed
re-ran the grep, confirmed that three-hit set complete, then found two further
defects of the same class on surfaces every prior pass had judged covered:

- **A pointer verb that drifted.** One reference file reached the extracted
  routing node with "names its route **per** `<node>`" where its two sibling
  call sites said "**Read** `<node>` and route by it". The imperative form is
  what makes an agent open the target; "per" is answerable without opening it.
  The pointer contains none of the retired vocabulary.
- **A caller enumeration that went stale.** The skill hub described the node as
  reached from two callers; there were three. The project's design doc stated it
  correctly, so the hub was the single wrong surface. This one is a derived
  figure in the existing rule's sense — but derived from the *refactor*, not
  from the removed name, so a grep for the name misses it exactly as the rule
  predicts for test counts.

Neither defect contains the retired name. No grep for that name could reach
either, and the sweep's stated exit condition was satisfied.

### Proposed addition

> A sweep that satisfies its stated exit condition can still leave the class it
> was aimed at. Give the *form* its own exit condition alongside the name's:
> grep the pointer verb, the enumeration, the derived figure — then re-derive
> each from its source.

### Constraints

- This is a proposal, not a decision. Per the ddaanet convention, a brief's
  recommendation and its stated constraints are the authoring agent's input;
  surface the choice to my human partner before writing the change.
- `SKILL.md` bodies are capped around 200 lines, so the addition is worth
  landing as a sentence or two folded into the existing paragraph rather than a
  new section. `removing-cleanly` is currently well under the cap.
- The illustrations above are deliberately generalized. The originating files
  live in another repository and a reader here cannot open them, so the shapes
  are described rather than cited.

### Rejected approaches

- **Keeping it as a `ddaanet` memory fact**, appended to
  `reference-audit-after-a-move`. Rejected on the owner test above. That file
  keeps its own distinct claim — that scoping a reference audit to the move
  under review inherits that move's blind spot — which is about the audit's
  *scope*, not the grep's predicate.
- **A note in the consuming repo's `inbox/`.** Written, then removed: the fact
  is about this skill, so the proposal belongs where the skill lives.

### Open question

Whether `reference-audit-after-a-move` should survive as a memory fact once this
skill carries the predicate rule, or whether its scope-of-audit claim belongs
here too. Both fire at the same moment — auditing references after a rename or a
removal — which is the memory-writing skill's own test for merging.
