#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

mkdir -p .claude/hooks .githooks

cat > .claude/hooks/pretooluse-ai-ops-guard.py <<'EOF'
#!/usr/bin/env python3
import pathlib
import runpy

ROOT = pathlib.Path(__file__).resolve().parents[2]
runpy.run_path(str(ROOT / "scripts" / "hooks" / "claude_pretooluse_guard.py"), run_name="__main__")
EOF

cat > .githooks/pre-commit <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
python3 scripts/check_compliance.py --mode staged
EOF

cat > .githooks/pre-push <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
python3 scripts/check_compliance.py --mode working_tree
EOF

chmod +x .claude/hooks/pretooluse-ai-ops-guard.py
chmod +x .githooks/pre-commit .githooks/pre-push
chmod +x scripts/check_compliance.py scripts/set_process_context.py scripts/hooks/claude_pretooluse_guard.py

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git config core.hooksPath .githooks
  echo "Installed AI Ops git hooks, configured core.hooksPath, and synced the Claude hook wrapper."
else
  echo "Installed AI Ops hook files and Claude hook wrapper. Skipped git config because this is not a git worktree."
fi
