#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

src="docs/omc-config/AI-OPS-POLICY.template.md"
dst=".omc/AI-OPS-POLICY.md"

mkdir -p .omc
cp "$src" "$dst"
echo "Synced OMC policy template to $dst"
