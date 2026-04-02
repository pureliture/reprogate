#!/usr/bin/env python3
"""PostToolUseFailure hook -- logs gate failures to records/gate-failures/ (HOOK-06)."""
import datetime
import json
import os
import pathlib
import secrets
import sys

sys.path.insert(0, os.path.dirname(__file__))
from reprogate_hook_base import check_disabled, get_profile

ROOT = pathlib.Path(__file__).resolve().parents[2]
GATE_FAILURES_DIR = ROOT / "records" / "gate-failures"


def _read_payload() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def main(gate_failures_dir: pathlib.Path | None = None) -> int:
    check_disabled()
    payload = _read_payload()
    failures_dir = gate_failures_dir or GATE_FAILURES_DIR
    failures_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    suffix = secrets.token_hex(2)
    profile = get_profile()
    tool_name = payload.get("tool_name", "unknown")
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command", "") or tool_input.get("file_path", "")
    error = payload.get("error", "")

    fm_sep = "---"
    content = (
        f"{fm_sep}\n"
        "type: gate-failure\n"
        f"captured_at: \"{now}\"\n"
        f"profile: {profile}\n"
        f"tool_name: {tool_name}\n"
        f"tool_input_command: \"{command}\"\n"
        f"hook_event: PostToolUseFailure\n"
        f"{fm_sep}\n\n"
        f"# Gate Failure: {tool_name}\n\n"
        f"**Captured at:** {now}  \n"
        f"**Profile:** {profile}  \n"
        "**Hook event:** PostToolUseFailure\n\n"
        "## Tool Input\n"
        f"```\n{command}\n```\n\n"
        "## Error\n"
        f"```\n{error}\n```\n\n"
        "## Notes\n"
        "Auto-captured by failure_logger.py. Review and resolve or dismiss.\n"
    )
    (failures_dir / f"gate-failure-{now}-{suffix}.md").write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
