#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

echo "🔒 ReproGate pre-commit gate check..."
python3 scripts/gatekeeper.py
