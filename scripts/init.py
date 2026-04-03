#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys
from typing import Any, Dict, List


ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "templates" / "reprogate.yaml.j2"
OUTPUT_PATH = ROOT / "reprogate.yaml"

# ReproGate hook entries to inject into .claude/settings.json.
# Each hook carries _reprogate: true so disable() can surgically remove them.
# Phase 2 will create the actual hook scripts; Phase 1 registers the entries.
REPROGATE_HOOKS: Dict[str, List[Dict[str, Any]]] = {
    "SessionStart": [
        {
            "hooks": [
                {
                    "type": "command",
                    "command": "python3 scripts/hooks/session_start.py",
                    "timeout": 10,
                    "_reprogate": True,
                }
            ]
        }
    ],
    "Stop": [
        {
            "hooks": [
                {
                    "type": "command",
                    "command": "python3 scripts/hooks/session_stop.py",
                    "timeout": 30,
                    "_reprogate": True,
                }
            ]
        }
    ],
    "PreToolUse": [
        {
            "hooks": [
                {
                    "type": "command",
                    "command": "python3 scripts/hooks/pretooluse_guard.py",
                    "timeout": 5,
                    "_reprogate": True,
                }
            ],
        }
    ],
    "PostToolUseFailure": [
        {
            "hooks": [
                {
                    "type": "command",
                    "command": "python3 scripts/hooks/failure_logger.py",
                    "timeout": 10,
                    "_reprogate": True,
                }
            ]
        }
    ],
}


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a starter reprogate.yaml file.")
    parser.add_argument("--output", default=str(OUTPUT_PATH), help="Output config path.")
    parser.add_argument("--project-name", default=ROOT.name, help="Project name.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing config file.")
    return parser.parse_args(argv)


def render_template(text: str, context: Dict[str, str]) -> str:
    rendered = text
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{ {key} }}}}", value)
    return rendered


def build_context(args: argparse.Namespace) -> Dict[str, str]:
    return {
        "project_name": args.project_name,
    }


def inject_reprogate_hooks(
    settings_path: pathlib.Path,
    hooks_to_add: Dict[str, List[Dict[str, Any]]],
) -> None:
    """Inject ReproGate hook entries into .claude/settings.json.

    Reads existing settings, merges ReproGate hooks (idempotent — skips
    entries whose command is already present), writes back.
    Never removes non-ReproGate entries.
    """
    data: Dict[str, Any] = {}
    if settings_path.exists():
        raw = settings_path.read_text(encoding="utf-8")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(
                f"Warning: {settings_path} contains invalid JSON ({exc}); treating as empty.",
                file=sys.stderr,
            )
            data = {}
    if "hooks" not in data:
        data["hooks"] = {}

    for event, groups in hooks_to_add.items():
        if event not in data["hooks"]:
            data["hooks"][event] = []
        # Build set of already-registered commands for idempotency check.
        # Use .get("command") to tolerate non-command hook entries gracefully.
        existing_commands: set[str] = {
            h.get("command", "")
            for g in data["hooks"][event]
            for h in g.get("hooks", [])
            if h.get("command")
        }
        for group in groups:
            new_commands = {h["command"] for h in group.get("hooks", [])}
            if not new_commands.intersection(existing_commands):
                data["hooks"][event].append(group)

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def create_session_data_dir(session_dir: pathlib.Path) -> None:
    """Create .claude/session-data/ directory for runtime session state."""
    session_dir.mkdir(parents=True, exist_ok=True)


def _ensure_gitignore_entry(gitignore_path: pathlib.Path, entry: str) -> None:
    """Add entry to .gitignore if not already present (idempotent)."""
    existing = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""
    lines = existing.splitlines()
    if entry not in lines:
        updated = existing.rstrip() + "\n" + entry + "\n"
        gitignore_path.write_text(updated, encoding="utf-8")


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    output_path = pathlib.Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path

    if output_path.exists() and not args.force:
        print(f"Refusing to overwrite existing file without --force: {output_path}", file=sys.stderr)
        return 1

    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    rendered = render_template(template_text, build_context(args))
    output_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")
    try:
        shown = output_path.relative_to(ROOT)
    except ValueError:
        shown = output_path
    print(f"Created {shown}")

    # INIT-01: Inject ReproGate hooks into .claude/settings.json
    settings_path = ROOT / ".claude" / "settings.json"
    inject_reprogate_hooks(settings_path, REPROGATE_HOOKS)
    print("Injected ReproGate hooks into .claude/settings.json")

    # INIT-01: Create .claude/session-data/ directory
    session_data_dir = ROOT / ".claude" / "session-data"
    create_session_data_dir(session_data_dir)
    print(f"Created {session_data_dir.relative_to(ROOT)}")

    # INIT-01: Guard .gitignore against session-data commits (ADR-011)
    gitignore_path = ROOT / ".gitignore"
    _ensure_gitignore_entry(gitignore_path, ".claude/session-data/")

    return 0


if __name__ == "__main__":
    sys.exit(main())
