#!/usr/bin/env python3
import argparse
import json
import pathlib
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, List


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTEXT_FILE = ROOT / ".ai-ops" / "process-context.json"

READ_ONLY_PROCESSES = {"G0", "P0", "P1", "P2", "S2", "S4"}
TEAM_CAPABLE_PROCESSES = {"P3", "P4", "S3", "S1"}
TEAM_COMMAND = "team"


@dataclass
class LaunchPlan:
    launcher: str
    args: List[str]
    notes: List[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Launch Codex/OMX with AI Ops-aware defaults from the recorded process context."
    )
    parser.add_argument("--launcher", choices=["omx", "codex"], default="omx")
    parser.add_argument("--allow-none-write", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("launch_args", nargs=argparse.REMAINDER)
    return parser.parse_args()


def load_context() -> Dict[str, object]:
    if not CONTEXT_FILE.exists():
        raise SystemExit(
            "Missing .ai-ops/process-context.json. Record a process first with scripts/set_process_context.py."
        )
    return json.loads(CONTEXT_FILE.read_text(encoding="utf-8"))


def normalize_launch_args(raw_args: List[str]) -> List[str]:
    if raw_args and raw_args[0] == "--":
        return raw_args[1:]
    return raw_args


def get_sandbox(args: List[str]) -> str:
    for index, arg in enumerate(args):
        if arg == "--sandbox" and index + 1 < len(args):
            return args[index + 1]
        if arg.startswith("--sandbox="):
            return arg.split("=", 1)[1]
    return ""


def replace_or_append_sandbox(args: List[str], mode: str) -> List[str]:
    updated = list(args)
    for index, arg in enumerate(updated):
        if arg == "--sandbox" and index + 1 < len(updated):
            updated[index + 1] = mode
            return updated
        if arg.startswith("--sandbox="):
            updated[index] = f"--sandbox={mode}"
            return updated
    updated.extend(["--sandbox", mode])
    return updated


def resolve_plan(parsed: argparse.Namespace, context: Dict[str, object]) -> LaunchPlan:
    process = str(context.get("selected_process") or "").strip().upper()
    if not process:
        raise SystemExit("selected_process is missing from .ai-ops/process-context.json")

    team_mode = str(context.get("team_mode") or "auto").strip().lower()
    args = normalize_launch_args(parsed.launch_args)
    notes: List[str] = []

    if process in TEAM_CAPABLE_PROCESSES and team_mode == "auto":
        raise SystemExit("Resolve team_mode to team or single before a writable team-capable launch.")

    if process in TEAM_CAPABLE_PROCESSES and team_mode == "team":
        if parsed.launcher != "omx":
            raise SystemExit("team_mode=team currently requires launcher=omx.")
        if not args or args[0] != TEAM_COMMAND:
            raise SystemExit("team_mode=team requires `omx team ...` launch arguments.")
        notes.append("Using team-capable launch path from recorded AI Ops context.")
        return LaunchPlan(launcher=parsed.launcher, args=args, notes=notes)

    sandbox = get_sandbox(args)
    if process in READ_ONLY_PROCESSES:
        args = replace_or_append_sandbox(args, "read-only")
        notes.append(f"{process} is read-only; forcing read-only sandbox.")
    elif process == "NONE":
        if parsed.allow_none_write:
            if not sandbox:
                args = replace_or_append_sandbox(args, "workspace-write")
            notes.append("NONE write override enabled.")
        else:
            args = replace_or_append_sandbox(args, "read-only")
            notes.append("NONE defaults to read-only without --allow-none-write.")
    else:
        if not sandbox:
            args = replace_or_append_sandbox(args, "workspace-write")
        notes.append("Writable delivery path resolved from recorded process context.")

    return LaunchPlan(launcher=parsed.launcher, args=args, notes=notes)


def main() -> int:
    parsed = parse_args()
    context = load_context()
    plan = resolve_plan(parsed, context)

    command = [plan.launcher, *plan.args]
    if parsed.dry_run:
        print("command: " + shlex.join(command))
        for note in plan.notes:
            print("- " + note)
        return 0

    if shutil.which(plan.launcher) is None:
        raise SystemExit(f"Launcher not found on PATH: {plan.launcher}")

    for note in plan.notes:
        print(note)
    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())
