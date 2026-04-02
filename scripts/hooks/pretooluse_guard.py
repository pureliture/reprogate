#!/usr/bin/env python3
"""PreToolUse hook — PreCompact state capture (HOOK-04) + advisory governance (HOOK-05)."""
import datetime
import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(__file__))
from reprogate_hook_base import check_disabled, get_profile

ROOT = pathlib.Path(__file__).resolve().parents[2]
SESSION_DATA = ROOT / ".claude" / "session-data"


def _read_payload() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def _allow() -> None:
    print(json.dumps({"permissionDecision": "allow"}))


def main(session_data: pathlib.Path | None = None) -> int:
    check_disabled()
    payload = _read_payload()
    data_dir = session_data or SESSION_DATA

    tool = payload.get("tool_name", "")
    command = (payload.get("tool_input") or {}).get("command", "")

    # HOOK-04: capture pre-compact state when compact is triggered
    if tool == "Bash" and "compact" in command.lower():
        data_dir.mkdir(parents=True, exist_ok=True)
        now = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        state = {
            "captured_at": now,
            "profile": get_profile(),
            "trigger": "compact",
            "session_data_snapshot": {},
        }
        (data_dir / "pre-compact-state.json").write_text(
            json.dumps(state, indent=2), encoding="utf-8"
        )

    _allow()
    return 0


if __name__ == "__main__":
    sys.exit(main())
