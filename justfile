import 'plugin-dev/release.just'
import 'plugin-dev/gates.just'

# Tool versions no lockfile pins: the venv's python3 and the system jq.
export PLUGIN_DEV_GATE_TOOLS := "python3 --version\njq --version"

precommit: format-docs check-refs check-size
    #!{{ plugin_dev_gate_prolog }}
    sentinel-guard precommit .claude-plugin skills scripts tests docs pyproject.toml uv.lock .gitignore
    scripts/check-skills.py
    pytest tests/ -q
    jq . .claude-plugin/plugin.json >/dev/null && echo "jq: plugin.json parses"
    record-sentinel

# Hard-wrap prose at 80 columns, so every edit diffs and reads by paragraph line.
format-docs:
    #!/usr/bin/env bash
    set -euo pipefail
    have=$(rumdl --version) || { echo "format-docs: rumdl not on PATH — run 'uv sync' and let direnv load .envrc" >&2; exit 1; }
    want=$(sed -n 's/.*"rumdl==\([0-9.]*\)".*/\1/p' pyproject.toml)
    [ "$have" = "rumdl $want" ] || { echo "format-docs: $have on PATH, pyproject.toml pins $want — run 'uv sync'" >&2; exit 1; }
    rumdl fmt --no-cache skills plans docs

prerelease: precommit
