#!/usr/bin/env python3
"""Tests for HOOK-02 (SessionStart), HOOK-03 (Stop), HOOK-04 (PreCompact)."""
import io
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "hooks"))


# ---------------------------------------------------------------------------
# HOOK-02: session_start tests
# ---------------------------------------------------------------------------

def test_session_start_creates_current_session(tmp_path, monkeypatch):
    """session_start.main() creates current-session.json with required keys."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.delenv("REPROGATE_HOOK_PROFILE", raising=False)
    import session_start
    result = session_start.main(session_data=tmp_path)
    assert result == 0
    session_file = tmp_path / "current-session.json"
    assert session_file.exists(), "current-session.json was not created"
    data = json.loads(session_file.read_text(encoding="utf-8"))
    for key in ("session_id", "started_at", "profile", "tool_calls"):
        assert key in data, f"Missing key '{key}' in current-session.json"
    assert data["tool_calls"] == [], "tool_calls should be an empty list"


def test_session_start_profile_in_json(tmp_path, monkeypatch):
    """session_start.main() writes the active profile into current-session.json."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.setenv("REPROGATE_HOOK_PROFILE", "standard")
    import session_start
    session_start.main(session_data=tmp_path)
    data = json.loads((tmp_path / "current-session.json").read_text(encoding="utf-8"))
    assert data["profile"] == "standard"


def test_session_start_disabled(tmp_path, monkeypatch):
    """session_start.main() exits 0 without creating any file when REPROGATE_DISABLED=1."""
    monkeypatch.setenv("REPROGATE_DISABLED", "1")
    import session_start
    with pytest.raises(SystemExit) as exc_info:
        session_start.main(session_data=tmp_path)
    assert exc_info.value.code == 0
    assert not (tmp_path / "current-session.json").exists(), (
        "current-session.json must NOT be created when disabled"
    )


# ---------------------------------------------------------------------------
# HOOK-03: session_stop tests
# ---------------------------------------------------------------------------

def test_session_stop_creates_summary(tmp_path, monkeypatch):
    """session_stop.main() creates a session-*-summary.json file."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.delenv("REPROGATE_HOOK_PROFILE", raising=False)
    import session_stop
    result = session_stop.main(session_data=tmp_path)
    assert result == 0
    summaries = list(tmp_path.glob("session-*-summary.json"))
    assert len(summaries) == 1, f"Expected 1 summary file, found {len(summaries)}"


def test_session_stop_creates_observation(tmp_path, monkeypatch):
    """session_stop.main() creates a session-*-observation.yaml file with observation_id key."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.delenv("REPROGATE_HOOK_PROFILE", raising=False)
    import session_stop
    session_stop.main(session_data=tmp_path)
    observations = list(tmp_path.glob("session-*-observation.yaml"))
    assert len(observations) == 1, f"Expected 1 observation file, found {len(observations)}"
    content = observations[0].read_text(encoding="utf-8")
    assert "observation_id:" in content, "observation YAML must contain 'observation_id:' key"


def test_session_stop_disabled(tmp_path, monkeypatch):
    """session_stop.main() exits 0 without creating any files when REPROGATE_DISABLED=1."""
    monkeypatch.setenv("REPROGATE_DISABLED", "1")
    import session_stop
    with pytest.raises(SystemExit) as exc_info:
        session_stop.main(session_data=tmp_path)
    assert exc_info.value.code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 0, f"No files should be created when disabled; found: {files}"


# ---------------------------------------------------------------------------
# HOOK-04: pretooluse_guard (PreCompact) tests
# ---------------------------------------------------------------------------

def test_precompact_saves_state(tmp_path, monkeypatch, capsys):
    """pretooluse_guard.main() saves pre-compact-state.json when compact is triggered."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.delenv("REPROGATE_HOOK_PROFILE", raising=False)
    payload = {"tool_name": "Bash", "tool_input": {"command": "compact"}}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    import pretooluse_guard
    result = pretooluse_guard.main(session_data=tmp_path)
    assert result == 0
    state_file = tmp_path / "pre-compact-state.json"
    assert state_file.exists(), "pre-compact-state.json must be created on compact trigger"
    data = json.loads(state_file.read_text(encoding="utf-8"))
    assert data["trigger"] == "compact"
    assert "captured_at" in data
    assert "profile" in data


def test_precompact_non_compact_pass_through(tmp_path, monkeypatch, capsys):
    """pretooluse_guard.main() does NOT create pre-compact-state.json for non-compact commands."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    payload = {"tool_name": "Bash", "tool_input": {"command": "ls -la"}}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    import pretooluse_guard
    result = pretooluse_guard.main(session_data=tmp_path)
    assert result == 0
    assert not (tmp_path / "pre-compact-state.json").exists(), (
        "pre-compact-state.json must NOT be created for non-compact commands"
    )


def test_precompact_disabled(tmp_path, monkeypatch):
    """pretooluse_guard.main() exits 0 (pass-through) when REPROGATE_DISABLED=1."""
    monkeypatch.setenv("REPROGATE_DISABLED", "1")
    payload = {"tool_name": "Bash", "tool_input": {"command": "compact"}}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    import pretooluse_guard
    with pytest.raises(SystemExit) as exc_info:
        pretooluse_guard.main(session_data=tmp_path)
    assert exc_info.value.code == 0
    assert not (tmp_path / "pre-compact-state.json").exists(), (
        "pre-compact-state.json must NOT be created when disabled"
    )
