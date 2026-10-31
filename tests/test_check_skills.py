"""The gate's own gate: every check in `scripts/check-skills.py` is load-bearing.

The checker pins every requirement in `docs/design.md` by running over the real
tree on each commit. Nothing pinned the checker itself, so a check that stopped
firing would look exactly like a tree with nothing to report.

Each test here spoils an otherwise-clean tree in exactly one way and asserts the
**complete** output — not that a failure occurred, but that this failure and no
other did. That is what makes the test discriminate: delete the check it names
and the tree becomes clean, the exit code flips to 0, and the assertion has
something to be wrong about. Asserting merely on the exit code would pass just
as well when a different check fired on an accidental second defect.

The checker is run the way `just precommit` runs it — as a subprocess from a
tree root, reading relative paths — rather than by importing its functions, so
the paths and the exit code are exercised as production exercises them.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHECKER = REPO / "scripts" / "check-skills.py"


def hub(name: str = "alpha", description: str = "What alpha does.", body: str = "Body.") -> str:
    """A well-formed `SKILL.md`, for a caller to spoil in one place."""
    return f'---\nname: {name}\ndescription: "{description}"\n---\n\n# {name}\n\n{body}\n'


def build(tmp_path: Path, files: dict[str, str] | None = None, dirs: tuple[str, ...] = ()) -> Path:
    """Write a tree rooted at `tmp_path`, defaulting to one clean skill."""
    for rel in dirs:
        (tmp_path / rel).mkdir(parents=True, exist_ok=True)
    for rel, text in (files if files is not None else {"skills/alpha/SKILL.md": hub()}).items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    (tmp_path / "skills").mkdir(exist_ok=True)
    return tmp_path


def check(tmp_path: Path) -> tuple[int, list[str]]:
    """Run the checker from `tmp_path` and return its exit code and lines."""
    proc = subprocess.run(
        [sys.executable, str(CHECKER)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout.splitlines()


# --- the clean cases, without which every negative below would pass vacuously


def test_clean_tree_passes(tmp_path):
    assert check(build(tmp_path)) == (0, ["check-skills: 1 files, all checks passed"])


def test_linked_node_is_not_an_orphan(tmp_path):
    tree = build(
        tmp_path,
        {
            "skills/alpha/SKILL.md": hub(body="See [the node](references/node.md)."),
            "skills/alpha/references/node.md": "# Node\n",
        },
    )
    assert check(tree) == (0, ["check-skills: 2 files, all checks passed"])


# --- one test per check, each asserting the complete output


def test_missing_skill(tmp_path):
    tree = build(tmp_path, dirs=("skills/beta",))
    assert check(tree) == (1, ["skills/beta: missing-skill: no SKILL.md"])


def test_missing_frontmatter(tmp_path):
    tree = build(tmp_path, {"skills/alpha/SKILL.md": "# alpha\n\nBody.\n"})
    assert check(tree) == (1, ["skills/alpha/SKILL.md: missing-field: no YAML frontmatter"])


def test_missing_name(tmp_path):
    tree = build(tmp_path, {"skills/alpha/SKILL.md": '---\ndescription: "d"\n---\n\nBody.\n'})
    assert check(tree) == (1, ["skills/alpha/SKILL.md: missing-field: name"])


def test_missing_description(tmp_path):
    tree = build(tmp_path, {"skills/alpha/SKILL.md": "---\nname: alpha\n---\n\nBody.\n"})
    assert check(tree) == (1, ["skills/alpha/SKILL.md: missing-field: description"])


def test_name_mismatch(tmp_path):
    tree = build(tmp_path, {"skills/alpha/SKILL.md": hub(name="beta")})
    assert check(tree) == (
        1,
        ["skills/alpha/SKILL.md: name-mismatch: 'beta' vs directory 'alpha'"],
    )


def test_unquoted_description(tmp_path):
    """Parseable, but unquoted — the gate is deliberately stricter than YAML."""
    tree = build(tmp_path, {"skills/alpha/SKILL.md": "---\nname: alpha\ndescription: What alpha does.\n---\n\nBody.\n"})
    assert check(tree) == (1, ["skills/alpha/SKILL.md: unquoted-description: quote the scalar"])


def test_unquoted_description_that_yaml_cannot_parse(tmp_path):
    """The `: ` case, which Claude Code loads and `yaml.safe_load` rejects."""
    tree = build(tmp_path, {"skills/alpha/SKILL.md": "---\nname: alpha\ndescription: Use when: always.\n---\n\nBody.\n"})
    assert check(tree) == (1, ["skills/alpha/SKILL.md: unquoted-description: ScannerError"])


def test_long_description(tmp_path):
    tree = build(tmp_path, {"skills/alpha/SKILL.md": hub(description="x" * 601)})
    assert check(tree) == (1, ["skills/alpha/SKILL.md: long-description: 601 B > 600 B"])


def test_long_description_is_measured_in_bytes_not_characters(tmp_path):
    """600 non-ASCII characters are 1200 bytes, and the cap is a byte cap."""
    tree = build(tmp_path, {"skills/alpha/SKILL.md": hub(description="é" * 400)})
    assert check(tree) == (1, ["skills/alpha/SKILL.md: long-description: 800 B > 600 B"])


def test_wikilink(tmp_path):
    tree = build(tmp_path, {"skills/alpha/SKILL.md": hub(body="See [[some-fact]].")})
    assert check(tree) == (1, ["skills/alpha/SKILL.md:8: wikilink: [[some-fact]]"])


def test_private_reference_to_the_store(tmp_path):
    tree = build(tmp_path, {"skills/alpha/SKILL.md": hub(body="Written in memory/ddaanet.")})
    assert check(tree) == (1, ["skills/alpha/SKILL.md:8: private-reference: memory/"])


def test_private_reference_to_the_index(tmp_path):
    tree = build(tmp_path, {"skills/alpha/SKILL.md": hub(body="Indexed in MEMORY.md.")})
    assert check(tree) == (1, ["skills/alpha/SKILL.md:8: private-reference: MEMORY.md"])


def test_private_reference_to_a_retired_source_fact(tmp_path):
    tree = build(tmp_path, {"skills/alpha/SKILL.md": hub(body="From outside-in-tdd.md.")})
    assert check(tree) == (1, ["skills/alpha/SKILL.md:8: private-reference: outside-in-tdd.md"])


def test_private_reference_reports_every_occurrence(tmp_path):
    """Each occurrence is its own failure, in line order."""
    tree = build(
        tmp_path,
        {"skills/alpha/SKILL.md": hub(body="See memory/one.\nAlso memory/two.")},
    )
    assert check(tree) == (
        1,
        [
            "skills/alpha/SKILL.md:8: private-reference: memory/",
            "skills/alpha/SKILL.md:9: private-reference: memory/",
        ],
    )


def test_broken_link(tmp_path):
    tree = build(tmp_path, {"skills/alpha/SKILL.md": hub(body="See [gone](references/gone.md).")})
    assert check(tree) == (1, ["skills/alpha/SKILL.md:8: broken-link: references/gone.md"])


def test_external_and_anchor_links_are_not_targets_on_disk(tmp_path):
    tree = build(
        tmp_path,
        {"skills/alpha/SKILL.md": hub(body="[a](https://example.invalid) and [b](#heading).")},
    )
    assert check(tree) == (0, ["check-skills: 1 files, all checks passed"])


def test_orphan_node(tmp_path):
    tree = build(
        tmp_path,
        {"skills/alpha/SKILL.md": hub(), "skills/alpha/references/node.md": "# Node\n"},
    )
    assert check(tree) == (1, ["skills/alpha/references/node.md: orphan-node: no hub link"])


# --- code is a sample, not prose (FR-6)


def test_a_fenced_block_is_not_scanned_as_prose(tmp_path):
    body = "```bash\n[[ \"$out\" != *x* ]]\ncat memory/MEMORY.md\n```\n"
    tree = build(tmp_path, {"skills/alpha/SKILL.md": hub(body=body)})
    assert check(tree) == (0, ["check-skills: 1 files, all checks passed"])


def test_an_inline_span_is_not_scanned_as_prose(tmp_path):
    tree = build(tmp_path, {"skills/alpha/SKILL.md": hub(body="Write `[[x]]` under `memory/`.")})
    assert check(tree) == (0, ["check-skills: 1 files, all checks passed"])


def test_blanking_code_does_not_hide_prose_on_the_same_line(tmp_path):
    """Only the span is blanked, so a defect beside it is still reported."""
    tree = build(tmp_path, {"skills/alpha/SKILL.md": hub(body="Run `cd memory/` and see [[x]].")})
    assert check(tree) == (1, ["skills/alpha/SKILL.md:8: wikilink: [[x]]"])


def test_blanking_a_fence_keeps_lines_below_it_at_their_raw_line(tmp_path):
    """A `blank_code` that deleted the fence instead of substituting spaces
    would report the wikilink three lines earlier than its true line."""
    body = "```\ncode\n```\n[[x]]"
    tree = build(tmp_path, {"skills/alpha/SKILL.md": hub(body=body)})
    assert check(tree) == (1, ["skills/alpha/SKILL.md:11: wikilink: [[x]]"])


# --- the run as a whole


def test_every_failure_is_reported_not_just_the_first(tmp_path):
    """Checks accumulate: a second defect does not hide behind the first."""
    tree = build(
        tmp_path,
        {"skills/alpha/SKILL.md": hub(name="beta", body="See [[x]].")},
    )
    assert check(tree) == (
        1,
        [
            "skills/alpha/SKILL.md: name-mismatch: 'beta' vs directory 'alpha'",
            "skills/alpha/SKILL.md:8: wikilink: [[x]]",
        ],
    )


def test_the_real_tree_passes(tmp_path):
    """The invocation `just precommit` makes, against the tree it makes it on."""
    code, out = check(REPO)
    assert code == 0, "\n".join(out)
