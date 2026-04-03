#!/usr/bin/env bash
set -euo pipefail
# Resolve repository root so this hook works regardless of the caller's cwd.
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"
uv run python3 scripts/gatekeeper.py
