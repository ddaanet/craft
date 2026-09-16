#!/usr/bin/env python3
"""Hygiene gate over `skills/`: the shipped bodies carry no private references.

Every skill here was written from a private memory store, so the failure mode is
leakage rather than breakage: a `[[wikilink]]` that resolved in that store, or a
`memory/…` path that exists on one machine. Neither stops the skill loading, so
nothing but a gate reports them.

The rest is shape. A description is loaded into every session whether or not the
skill fires, so it is capped; a hub is read on every invocation and a node only
when the hub sends the reader there, so the hub's line cap is the tighter one.
The same node cap covers `scripts/*.py`, `tests/*.py` and `docs/*.md`, which
are read at one go by the same reader and are wrapped by the same formatter
pass.

Ten checks, all blocking:

- `missing-skill`        a `skills/<name>/` with no `SKILL.md`
- `missing-field`        frontmatter without `name` or `description`
- `name-mismatch`        `name` disagreeing with the directory
- `unquoted-description` a description that is not a quoted scalar
- `long-description`     a description past the byte cap
- `wikilink`             `[[…]]`, which resolves only inside the memory store
- `private-reference`    a `memory/…` path, `MEMORY.md`, or a source-fact slug
- `broken-link`          a relative pointer whose target is not on disk
- `orphan-node`          a `references/*.md` no hub points at
- `oversized-file`       a file past the cap for its kind

Repo-local maintainer tooling, not a shipped plugin component.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

SKILLS = Path("skills")

# A description is paid for by every session that loads the plugin, fired or
# not. 600 B sits above the largest comparable installed skill measured
# (`shell-scripting:shell-gotchas`, 551 B) and well under the point where five
# of them stop being free.
MAX_DESCRIPTION_BYTES = 600

# A hub is read on every invocation; a node only when the hub sends the reader
# there. Both are hard-wrapped at 80 columns by `just format-docs`, which is
# what makes a line count mean anything at all — an unwrapped file games any
# cap. See `scripts/check-skills.py`'s caller in the justfile. The living design
# doc is capped as a node: it is prose a reader takes in at one go, so exempting
# it because it is maintainer-facing would be exempting it from its own rule.
MAX_HUB_LINES = 200
MAX_NODE_LINES = 400

# The memory facts these skills were written from, plus the two the same pass
# retired to other venues. Some still live in the store (`hook-output-channels`
# is indexed there), so a body naming one is private to a reader without the
# store, whether or not the fact itself survives.
SOURCE_FACTS = frozenset(
    {
        "design-doc-writing",
        "design-doc-no-situational-state",
        "design-doc-rewire-dead-components",
        "no-doc-history-references",
        "reference-doc-scope",
        "large-docs-review",
        "plan-length-matches-work",
        "spec-enumerations-need-rederiving",
        "honest-line-count-caps",
        "spec-contract-size-predicts-pr-size",
        "test-with-live-data-before-designing",
        "green-is-not-evidence",
        "genuine-red-not-missing-sut",
        "outside-in-tdd",
        "test-the-invocation-path",
        "directive-states-acts",
        "hook-output-channels",
        "loose-generation",
        "remove-cleanly-no-vestigial",
        "no-transition-special-cases",
        "plan-contracts-not-full-code",
        "precommit-line-caps",
    },
)

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
WIKILINK = re.compile(r"\[\[[^\]]+\]\]")
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
DESCRIPTION_LINE = re.compile(r"^description:\s*(.*)$", re.MULTILINE)
FENCE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
CODE_SPAN = re.compile(r"`[^`\n]+`")


def blank_code(text: str) -> str:
    """Blank fenced blocks and inline spans, keeping line count and offsets.

    A bash test expression quoted as `[[ "$out" != *"x"* ]]` is a code sample,
    not a wikilink, and a path inside a fence is an illustration rather than a
    pointer. Substituting spaces rather than deleting keeps every line number
    in a failure message pointing at the right line.
    """
    blanked = FENCE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
    return CODE_SPAN.sub(lambda m: " " * len(m.group(0)), blanked)


def line_of(text: str, index: int) -> int:
    """1-based line of `index` into `text`.

    `blank_code` substitutes spaces for code rather than deleting, so an
    index into the blanked prose is also an index into the raw text.
    """
    return 1 + text.count("\n", 0, index)


def check_frontmatter(skill_md: Path, failures: list[str]) -> None:
    """Parse a hub's frontmatter and check its name, description and quoting."""
    text = skill_md.read_text()
    match = FRONTMATTER.match(text)
    if match is None:
        failures.append(f"{skill_md}: missing-field: no YAML frontmatter")
        return
    raw = match.group(1)
    try:
        meta = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        # An unquoted description containing `: ` is the case that lands here.
        # Claude Code loads it fine, so requiring the quote is what keeps this
        # gate from being stricter than the runtime for no reason — but an
        # unparseable frontmatter still has to be reported as what it is.
        failures.append(f"{skill_md}: unquoted-description: {exc.__class__.__name__}")
        return

    for field in ("name", "description"):
        if not meta.get(field):
            failures.append(f"{skill_md}: missing-field: {field}")
    if meta.get("name") and meta["name"] != skill_md.parent.name:
        failures.append(
            f"{skill_md}: name-mismatch: {meta['name']!r} vs directory "
            f"{skill_md.parent.name!r}",
        )

    value = DESCRIPTION_LINE.search(raw)
    if value and not value.group(1).startswith(('"', "'")):
        failures.append(f"{skill_md}: unquoted-description: quote the scalar")

    size = len(str(meta.get("description", "")).encode())
    if size > MAX_DESCRIPTION_BYTES:
        failures.append(
            f"{skill_md}: long-description: {size} B > {MAX_DESCRIPTION_BYTES} B",
        )


def check_body(path: Path, failures: list[str]) -> None:
    """Check one body for private references, broken links and its line cap."""
    text = path.read_text()
    prose = blank_code(text)

    for match in WIKILINK.finditer(prose):
        line = line_of(prose, match.start())
        failures.append(f"{path}:{line}: wikilink: {match.group(0)}")
    # None of these literal patterns contains a space, so a reflow by the
    # formatter cannot split one across lines.
    for pattern in ("memory/", "MEMORY.md"):
        for match in re.finditer(re.escape(pattern), prose):
            line = line_of(prose, match.start())
            failures.append(f"{path}:{line}: private-reference: {pattern}")
    for slug in sorted(SOURCE_FACTS):
        pattern = f"{slug}.md"
        for match in re.finditer(re.escape(pattern), prose):
            line = line_of(prose, match.start())
            failures.append(f"{path}:{line}: private-reference: {pattern}")

    for match in LINK.finditer(prose):
        target = match.group(1)
        if "://" in target or target.startswith("#"):
            continue
        if not (path.parent / target.split("#", 1)[0]).exists():
            line = line_of(prose, match.start())
            failures.append(f"{path}:{line}: broken-link: {target}")

    cap = MAX_HUB_LINES if path.name == "SKILL.md" else MAX_NODE_LINES
    lines = len(text.splitlines())
    if lines > cap:
        failures.append(f"{path}: oversized-file: {lines} lines > {cap}")


def main() -> int:
    """Run every check over `skills/` and print each failure on its own line."""
    failures: list[str] = []

    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            failures.append(f"{skill_dir}: missing-skill: no SKILL.md")
            continue
        check_frontmatter(skill_md, failures)

        hub_text = skill_md.read_text()
        linked = {t.split("#", 1)[0] for t in LINK.findall(hub_text)}
        for node in sorted(skill_dir.glob("references/*.md")):
            if node.relative_to(skill_dir).as_posix() not in linked:
                failures.append(f"{node}: orphan-node: no hub link")

    for path in sorted(SKILLS.rglob("*.md")):
        check_body(path, failures)

    capped = (
        sorted(Path("scripts").glob("*.py"))
        + sorted(Path("tests").glob("*.py"))
        + sorted(Path("docs").glob("*.md"))
    )
    for path in capped:
        lines = len(path.read_text().splitlines())
        if lines > MAX_NODE_LINES:
            failures.append(f"{path}: oversized-file: {lines} lines > {MAX_NODE_LINES}")

    for failure in failures:
        print(failure)
    if failures:
        return 1
    print(f"check-skills: {len(list(SKILLS.rglob('*.md')))} files, all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
