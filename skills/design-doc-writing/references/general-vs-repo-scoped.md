# General vs repo-scoped

When asked to research best practices and produce a *lasting guideline* — the
point being to amortize generation and research cost across releases — keep the
guideline **general and project-agnostic**. Do not ground it in the current repo
or frame it as an audit input.

A guideline is meant to be reusable until the toolchain changes. Scoping the
research prompt to "ground in THIS project" plus "so an agent can audit
`scripts/*.py`" is what makes it a one-off: on one measured attempt at a
mypy/typing guideline it leaked ~19 "this repo does X" intrusions plus a
Repo-notes and a Review-log section into a doc meant to be durable.
Repo-specific commentary makes a general reference read as a stale one-off and
will not transfer.

Split the two artifacts cleanly:

- **The guideline** — general DO/AVOID rules, neutral illustrative examples
  (`Json = dict[str, Any]`, not `Entry` in `scripts/extract.py`),
  version-grounded but not repo-grounded.
- **The audit or application** — the repo-specific findings: the actual aliases,
  magic strings, config hygiene. Point-in-time.

When a multi-stage research → review → audit pipeline is requested, the research
and review stages feed the *general* doc; only the audit stage is repo-specific.

Confirm the intended scope — general or project-specific — **before** delegating
the research. The leak is cheap to prevent in the prompt and expensive to strip
out of a finished document.
