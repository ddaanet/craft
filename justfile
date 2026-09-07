import 'plugin-dev/release.just'

precommit: format-docs
    #!/usr/bin/env bash
    set -euo pipefail
    scripts/check-skills.py
    jq . .claude-plugin/plugin.json >/dev/null && echo "jq: plugin.json parses"
    shellcheck .bin/claude && echo "shellcheck: .bin/claude clean"

# Hard-wrap prose at 80 columns. The line caps in check-skills.py are only
# measurable after this runs: an unwrapped file games any line count.
format-docs:
    #!/usr/bin/env bash
    set -euo pipefail
    have=$(rumdl --version) || { echo "format-docs: rumdl not on PATH — run 'uv sync' and let direnv load .envrc" >&2; exit 1; }
    want=$(sed -n 's/.*"rumdl==\([0-9.]*\)".*/\1/p' pyproject.toml)
    [ "$have" = "rumdl $want" ] || { echo "format-docs: $have on PATH, pyproject.toml pins $want — run 'uv sync'" >&2; exit 1; }
    rumdl fmt --no-cache skills plans docs

prerelease: precommit
