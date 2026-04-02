#!/usr/bin/env python3
"""SessionStart hook — initializes current-session.json (HOOK-02)."""
import datetime
import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(__file__))
from reprogate_hook_base import check_disabled, get_profile

ROOT = pathlib.Path(__file__).resolve().parents[2]
SESSION_DATA = ROOT / ".claude" / "session-data"


def main(session_data: pathlib.Path | None = None) -> int:
    check_disabled()
    data_dir = session_data or SESSION_DATA
    data_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    payload = {
        "session_id": f"sess-{now}",
        "started_at": now,
        "profile": get_profile(),
        "tool_calls": [],
    }
    (data_dir / "current-session.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
