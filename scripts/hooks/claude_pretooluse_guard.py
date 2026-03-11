#!/usr/bin/env python3
import json
import os
import pathlib
import re
import subprocess
import sys
from typing import Dict, Optional, Tuple


ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts" / "check_compliance.py"
PROCESS_CONTEXT = pathlib.Path(
    os.getenv("AI_OPS_CONTEXT_FILE", ROOT / ".ai-ops" / "process-context.json")
)

GUARDED_TOOLS = {"Write", "Edit", "MultiEdit", "Bash"}
READ_ONLY_PROCESSES = {"G0", "P0", "P1", "P2", "S2", "S4"}
TEAM_ELIGIBLE_PROCESSES = {"P3", "P4", "S3", "S1"}

READONLY_BASH_PATTERNS = [
    re.compile(r"^(pwd|date)$"),
    re.compile(r"^(ls|find|cat|head|tail|wc|grep|rg|cut|sort|uniq|echo)\b"),
    re.compile(r"^sed\s+-n\b"),
    re.compile(r"^git\s+(status|log|show|diff|rev-parse|branch)\b"),
    re.compile(r"^python3\s+scripts/check_compliance.py\b"),
    re.compile(r"^(pytest|python3?\s+-m\s+pytest|python3?\s+-m\s+unittest)\b"),
]


def read_payload() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def tool_name(payload: dict) -> str:
    return payload.get("tool_name") or payload.get("toolName") or payload.get("tool") or ""


def tool_input(payload: dict) -> dict:
    value = payload.get("tool_input") or payload.get("input") or {}
    return value if isinstance(value, dict) else {}


def extract_file_path(payload: dict) -> str:
    item = tool_input(payload)
    return item.get("file_path") or item.get("path") or ""


def extract_command(payload: dict) -> str:
    item = tool_input(payload)
    return item.get("command") or item.get("cmd") or ""


def as_repo_relative(path_str: str) -> Optional[str]:
    if not path_str:
        return None
    path = pathlib.Path(path_str)
    if not path.is_absolute():
        path = (ROOT / path).resolve()
    else:
        path = path.resolve()
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def is_documentation_target(path_str: str) -> bool:
    rel = as_repo_relative(path_str)
    if not rel:
        return False
    return rel.startswith("docs/") or rel.endswith(".md") or rel in {"README.md", "AGENTS.md"}


def load_process_context() -> Dict[str, object]:
    if not PROCESS_CONTEXT.exists():
        return {}
    try:
        data = json.loads(PROCESS_CONTEXT.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:  # noqa: BLE001
        return {}


def selected_process(context: Dict[str, object]) -> str:
    value = str(context.get("selected_process") or context.get("process") or "").strip().upper()
    return value


def team_mode(context: Dict[str, object]) -> str:
    value = str(context.get("team_mode") or "auto").strip().lower()
    return value if value in {"auto", "single", "team", "none"} else "auto"


def is_readonly_bash(command: str) -> bool:
    cmd = (command or "").strip()
    if not cmd:
        return True
    segments = re.split(r"&&|;|\|\|", cmd)
    for segment in segments:
        part = segment.strip()
        if not part:
            continue
        if any(pattern.match(part) for pattern in READONLY_BASH_PATTERNS):
            continue
        return False
    return True


def deny(reason: str) -> int:
    print(json.dumps({"permissionDecision": "deny", "permissionDecisionReason": reason}))
    return 0


def allow() -> int:
    print(json.dumps({"permissionDecision": "allow"}))
    return 0


def run_checker() -> Tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(CHECKER), "--mode", "none"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return True, ""
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    return False, lines[0] if lines else "AI Ops compliance check failed."


def main() -> int:
    payload = read_payload()
    name = tool_name(payload)
    if name and name not in GUARDED_TOOLS:
        return allow()

    context = load_process_context()
    process = selected_process(context)

    if name in {"Write", "Edit", "MultiEdit"}:
        if not process:
            return deny("Select a process before using write/edit tools.")
        if process in TEAM_ELIGIBLE_PROCESSES and team_mode(context) == "auto":
            return deny("Resolve team_mode to team or single before implementation on a team-capable process.")
        if process in READ_ONLY_PROCESSES and not is_documentation_target(extract_file_path(payload)):
            return deny(f"{process} only allows documentation or record updates.")

    if name == "Bash":
        command = extract_command(payload)
        readonly = is_readonly_bash(command)
        if not process and not readonly:
            return deny("Select a process before running mutating shell commands.")
        if process in TEAM_ELIGIBLE_PROCESSES and not readonly and team_mode(context) == "auto":
            return deny("Resolve team_mode to team or single before mutating shell commands.")
        if process in READ_ONLY_PROCESSES and not readonly:
            return deny(f"{process} only allows read-only shell commands.")

    ok, reason = run_checker()
    if not ok:
        return deny(reason)
    return allow()


if __name__ == "__main__":
    sys.exit(main())
