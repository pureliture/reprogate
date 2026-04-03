#!/usr/bin/env python3
"""Tests for HOOK-05 (advisory governance) and HOOK-06 (gate failure logger)."""
import io
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "hooks"))


# ---------------------------------------------------------------------------
# HOOK-06: failure_logger tests
# ---------------------------------------------------------------------------

def test_failure_logger_creates_gate_failure_record(tmp_path, monkeypatch):
    """failure_logger.main() creates a gate-failure-*.md file in gate_failures_dir."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.delenv("REPROGATE_HOOK_PROFILE", raising=False)
    payload = {"tool_name": "Bash", "tool_input": {"command": "git commit"}, "error": "failed"}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    import failure_logger
    result = failure_logger.main(gate_failures_dir=tmp_path)
    assert result == 0
    files = list(tmp_path.glob("gate-failure-*.md"))
    assert len(files) == 1, f"Expected 1 gate-failure-*.md, found {len(files)}"


def test_failure_logger_creates_dir(tmp_path, monkeypatch):
    """failure_logger.main() creates gate_failures_dir if it does not exist."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.delenv("REPROGATE_HOOK_PROFILE", raising=False)
    non_existent = tmp_path / "gate-failures"
    assert not non_existent.exists(), "Pre-condition: dir must not exist before test"
    payload = {"tool_name": "Write", "tool_input": {"file_path": "foo.py"}, "error": "hook error"}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    import failure_logger
    result = failure_logger.main(gate_failures_dir=non_existent)
    assert result == 0
    assert non_existent.exists() and non_existent.is_dir(), (
        "gate_failures_dir was not created"
    )
    files = list(non_existent.glob("gate-failure-*.md"))
    assert len(files) == 1, f"Expected 1 file after dir creation, found {len(files)}"


def test_failure_logger_record_has_frontmatter(tmp_path, monkeypatch):
    """gate-failure-*.md written by failure_logger contains 'type: gate-failure' in frontmatter."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.delenv("REPROGATE_HOOK_PROFILE", raising=False)
    payload = {"tool_name": "Bash", "tool_input": {"command": "git commit"}, "error": "fail"}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    import failure_logger
    failure_logger.main(gate_failures_dir=tmp_path)
    files = list(tmp_path.glob("gate-failure-*.md"))
    assert len(files) == 1
    content = files[0].read_text(encoding="utf-8")
    assert "type: gate-failure" in content, (
        "gate-failure record must contain 'type: gate-failure' in YAML frontmatter"
    )


def test_failure_logger_disabled(tmp_path, monkeypatch):
    """failure_logger.main() exits 0 without creating any file when REPROGATE_DISABLED=1."""
    monkeypatch.setenv("REPROGATE_DISABLED", "1")
    payload = {"tool_name": "Bash", "tool_input": {"command": "git commit"}, "error": "failed"}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    import failure_logger
    with pytest.raises(SystemExit) as exc_info:
        failure_logger.main(gate_failures_dir=tmp_path)
    assert exc_info.value.code == 0
    files = list(tmp_path.glob("gate-failure-*.md"))
    assert len(files) == 0, "No file should be created when REPROGATE_DISABLED=1"


# ---------------------------------------------------------------------------
# HOOK-05: governance advisory in pretooluse_guard tests
# ---------------------------------------------------------------------------

def test_governance_advisory_appends_tool_call_standard(tmp_path, monkeypatch, capsys):
    """pretooluse_guard.main() appends tool_call entry to current-session.json at standard profile."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.setenv("REPROGATE_HOOK_PROFILE", "standard")
    # Create an existing current-session.json with empty tool_calls
    session_file = tmp_path / "current-session.json"
    session_file.write_text(
        json.dumps({"session_id": "test-123", "started_at": "2026-04-02T00:00:00Z",
                    "profile": "standard", "tool_calls": []}),
        encoding="utf-8",
    )
    payload = {"tool_name": "Write", "tool_input": {"file_path": "foo.py"}}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    import pretooluse_guard
    result = pretooluse_guard.main(session_data=tmp_path)
    assert result == 0
    data = json.loads(session_file.read_text(encoding="utf-8"))
    assert len(data["tool_calls"]) == 1, (
        f"Expected 1 tool_call entry, found {len(data['tool_calls'])}"
    )
    assert data["tool_calls"][0]["tool_name"] == "Write"


def test_governance_advisory_minimal_skips_logging(tmp_path, monkeypatch, capsys):
    """pretooluse_guard.main() does NOT append tool_call at minimal profile."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.setenv("REPROGATE_HOOK_PROFILE", "minimal")
    session_file = tmp_path / "current-session.json"
    session_file.write_text(
        json.dumps({"session_id": "test-456", "started_at": "2026-04-02T00:00:00Z",
                    "profile": "minimal", "tool_calls": []}),
        encoding="utf-8",
    )
    payload = {"tool_name": "Write", "tool_input": {"file_path": "bar.py"}}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    import pretooluse_guard
    result = pretooluse_guard.main(session_data=tmp_path)
    assert result == 0
    data = json.loads(session_file.read_text(encoding="utf-8"))
    assert len(data["tool_calls"]) == 0, (
        f"Minimal profile must NOT log tool_calls; found {len(data['tool_calls'])} entries"
    )


def test_governance_advisory_always_allows(tmp_path, monkeypatch, capsys):
    """pretooluse_guard.main() always outputs permissionDecision allow (advisory-only)."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.setenv("REPROGATE_HOOK_PROFILE", "strict")
    payload = {"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    import pretooluse_guard
    result = pretooluse_guard.main(session_data=tmp_path)
    assert result == 0
    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert output.get("permissionDecision") == "allow", (
        "Governance hook must always output permissionDecision: allow (advisory-only)"
    )
