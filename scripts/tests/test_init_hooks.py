#!/usr/bin/env python3
"""Tests for INIT-01 (hook injection), INIT-02 (REPROGATE_DISABLED), INIT-03 (disable)."""
import json
import os
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _make_gsd_settings(tmp_path: pathlib.Path) -> pathlib.Path:
    """Create a settings.json that mirrors the live GSD hooks structure."""
    settings = {
        "hooks": {
            "SessionStart": [{"hooks": [{"type": "command", "command": "node .claude/hooks/gsd-check-update.js"}]}],
            "PostToolUse": [{"matcher": "Bash|Edit|Write|MultiEdit|Agent|Task", "hooks": [{"type": "command", "command": "node .claude/hooks/gsd-context-monitor.js", "timeout": 10}]}],
            "PreToolUse": [{"matcher": "Write|Edit", "hooks": [{"type": "command", "command": "node .claude/hooks/gsd-prompt-guard.js", "timeout": 5}]}],
        },
        "statusLine": {"type": "command", "command": "node .claude/hooks/gsd-statusline.js"},
    }
    p = tmp_path / "settings.json"
    p.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    return p


def test_init_injects_reprogate_hooks(tmp_path):
    """inject_reprogate_hooks() must add ReproGate hook entries to settings.json."""
    from init import inject_reprogate_hooks, REPROGATE_HOOKS
    settings_path = tmp_path / "settings.json"
    inject_reprogate_hooks(settings_path, REPROGATE_HOOKS)
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    hooks = data["hooks"]
    for event in ["SessionStart", "Stop", "PostToolUseFailure"]:
        assert event in hooks, f"Missing event {event} after inject"
    # Verify _reprogate tag present on at least one injected hook
    found_tag = False
    for event, groups in hooks.items():
        for group in groups:
            for h in group.get("hooks", []):
                if h.get("_reprogate"):
                    found_tag = True
    assert found_tag, "No injected hook has _reprogate: true tag"


def test_init_preserves_existing_hooks(tmp_path):
    """inject_reprogate_hooks() must not remove pre-existing non-reprogate hooks."""
    from init import inject_reprogate_hooks, REPROGATE_HOOKS
    settings_path = _make_gsd_settings(tmp_path)
    inject_reprogate_hooks(settings_path, REPROGATE_HOOKS)
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    # GSD SessionStart hook must still be there
    session_commands = [
        h["command"]
        for g in data["hooks"].get("SessionStart", [])
        for h in g.get("hooks", [])
    ]
    assert any("gsd-check-update" in cmd for cmd in session_commands), (
        "GSD gsd-check-update hook was removed by inject"
    )
    # GSD statusLine must still be there
    assert data.get("statusLine", {}).get("command", "") == "node .claude/hooks/gsd-statusline.js"


def test_init_idempotent(tmp_path):
    """inject_reprogate_hooks() called twice must not duplicate hook entries."""
    from init import inject_reprogate_hooks, REPROGATE_HOOKS
    settings_path = _make_gsd_settings(tmp_path)
    inject_reprogate_hooks(settings_path, REPROGATE_HOOKS)
    data_after_first = json.loads(settings_path.read_text(encoding="utf-8"))

    inject_reprogate_hooks(settings_path, REPROGATE_HOOKS)
    data_after_second = json.loads(settings_path.read_text(encoding="utf-8"))

    # Count total hook entries in both snapshots
    def count_hooks(data):
        return sum(
            len(g.get("hooks", []))
            for groups in data["hooks"].values()
            for g in groups
        )

    assert count_hooks(data_after_first) == count_hooks(data_after_second), (
        "inject_reprogate_hooks is not idempotent — hook count changed on second call"
    )


def test_init_creates_session_data_dir(tmp_path):
    """init must create .claude/session-data/ directory."""
    from init import create_session_data_dir
    session_dir = tmp_path / ".claude" / "session-data"
    create_session_data_dir(session_dir)
    assert session_dir.exists() and session_dir.is_dir(), (
        f"session-data directory was not created at {session_dir}"
    )


def test_disable_removes_reprogate_hooks(tmp_path):
    """remove_reprogate_hooks() must remove all _reprogate-tagged entries."""
    from init import inject_reprogate_hooks, REPROGATE_HOOKS
    from disable import remove_reprogate_hooks
    settings_path = _make_gsd_settings(tmp_path)
    inject_reprogate_hooks(settings_path, REPROGATE_HOOKS)
    remove_reprogate_hooks(settings_path)
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    for event, groups in data["hooks"].items():
        for group in groups:
            for h in group.get("hooks", []):
                assert not h.get("_reprogate"), (
                    f"_reprogate-tagged hook still present after disable: {h}"
                )


def test_disable_preserves_gsd_hooks(tmp_path):
    """remove_reprogate_hooks() must leave non-reprogate GSD hooks intact."""
    from init import inject_reprogate_hooks, REPROGATE_HOOKS
    from disable import remove_reprogate_hooks
    settings_path = _make_gsd_settings(tmp_path)
    inject_reprogate_hooks(settings_path, REPROGATE_HOOKS)
    remove_reprogate_hooks(settings_path)
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    session_commands = [
        h["command"]
        for g in data["hooks"].get("SessionStart", [])
        for h in g.get("hooks", [])
    ]
    assert any("gsd-check-update" in cmd for cmd in session_commands), (
        "GSD gsd-check-update hook was removed by disable"
    )


def test_disabled_env_var_check_exits_zero(monkeypatch):
    """check_disabled() must call sys.exit(0) when REPROGATE_DISABLED=1."""
    sys.path.insert(0, str(ROOT / "scripts" / "hooks"))
    monkeypatch.setenv("REPROGATE_DISABLED", "1")
    import reprogate_hook_base
    with pytest.raises(SystemExit) as exc_info:
        reprogate_hook_base.check_disabled()
    assert exc_info.value.code == 0, f"Expected exit(0), got exit({exc_info.value.code})"


def test_enabled_env_var_check_does_not_exit(monkeypatch):
    """check_disabled() must NOT exit when REPROGATE_DISABLED is not set."""
    sys.path.insert(0, str(ROOT / "scripts" / "hooks"))
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    import reprogate_hook_base
    # Should return without raising SystemExit
    reprogate_hook_base.check_disabled()  # no exception = pass
