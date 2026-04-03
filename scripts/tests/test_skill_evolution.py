#!/usr/bin/env python3
"""Tests for Skill Evolution pipeline — SKILL-EVO-01 (tasks 5.1–5.4)."""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "hooks"))


# ---------------------------------------------------------------------------
# 5.1 / 5.2 — observation extraction and schema validation
# ---------------------------------------------------------------------------

def test_build_observation_template_has_required_fields():
    """_build_observation_template returns YAML with all required instinct schema fields."""
    import session_stop
    yaml_text = session_stop._build_observation_template(
        session_id="test-session-123",
        captured_at="20260402T120000Z",
        profile="standard",
        tool_calls_count=5,
    )
    required_keys = [
        "id:",
        "session_id:",
        "captured_at:",
        "observations:",
        "confidence:",
        "reviewed:",
        "promoted:",
        "raw_summary:",
    ]
    for key in required_keys:
        assert key in yaml_text, f"YAML template must contain '{key}'"


def test_build_observation_template_embeds_session_id():
    """_build_observation_template embeds the provided session_id."""
    import session_stop
    yaml_text = session_stop._build_observation_template(
        session_id="my-unique-session",
        captured_at="20260402T120000Z",
        profile="minimal",
        tool_calls_count=0,
    )
    assert "my-unique-session" in yaml_text


def test_build_observation_template_reviewed_false():
    """_build_observation_template sets reviewed: false and promoted: false by default."""
    import session_stop
    yaml_text = session_stop._build_observation_template(
        session_id="s1",
        captured_at="20260402T120000Z",
        profile="minimal",
        tool_calls_count=0,
    )
    assert "reviewed: false" in yaml_text
    assert "promoted: false" in yaml_text


def test_build_observation_template_unique_ids():
    """Two consecutive calls produce different id values."""
    import session_stop
    yaml1 = session_stop._build_observation_template("s1", "t1", "minimal", 0)
    yaml2 = session_stop._build_observation_template("s2", "t2", "minimal", 0)
    # Extract id lines
    id1 = next(line for line in yaml1.splitlines() if line.startswith("id:"))
    id2 = next(line for line in yaml2.splitlines() if line.startswith("id:"))
    assert id1 != id2, "Each observation must have a unique id"


# ---------------------------------------------------------------------------
# 5.1 — homunculus instincts dir creation and observation file saving
# ---------------------------------------------------------------------------

def test_session_stop_creates_instinct_in_homunculus_dir(tmp_path, monkeypatch):
    """session_stop saves observation YAML to instincts_dir (SKILL-EVO-01)."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.delenv("REPROGATE_HOOK_PROFILE", raising=False)
    import session_stop
    inst_dir = tmp_path / "instincts"
    result = session_stop.main(session_data=tmp_path, instincts_dir=inst_dir)
    assert result == 0
    assert inst_dir.exists(), "instincts_dir must be auto-created"
    instinct_files = list(inst_dir.glob("*.yaml"))
    assert len(instinct_files) == 1, f"Expected 1 instinct YAML in homunculus dir, found {len(instinct_files)}"


def test_session_stop_instinct_file_named_by_session_id(tmp_path, monkeypatch):
    """Instinct YAML filename matches the session_id."""
    import json
    import session_stop
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.delenv("REPROGATE_HOOK_PROFILE", raising=False)
    # Pre-create a session with known session_id
    session_json = {"session_id": "my-test-session", "tool_calls": [], "started_at": "2026-04-02"}
    (tmp_path / "current-session.json").write_text(json.dumps(session_json))
    inst_dir = tmp_path / "instincts"
    session_stop.main(session_data=tmp_path, instincts_dir=inst_dir)
    assert (inst_dir / "my-test-session.yaml").exists(), "Instinct file must be named <session_id>.yaml"


# ---------------------------------------------------------------------------
# 5.1 — error resilience: observation error must not block session exit
# ---------------------------------------------------------------------------

def test_session_stop_observation_error_does_not_block(tmp_path, monkeypatch, capsys):
    """Observation save failure writes a warning but returns 0 (ADR-016)."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.delenv("REPROGATE_HOOK_PROFILE", raising=False)
    import session_stop
    # Use a path that will fail (a file, not a directory)
    bad_path = tmp_path / "not-a-dir"
    bad_path.write_text("I am a file")
    result = session_stop.main(session_data=tmp_path, instincts_dir=bad_path)
    assert result == 0, "session_stop must return 0 even when observation save fails"
    captured = capsys.readouterr()
    assert "observation 저장 실패" in captured.err


# ---------------------------------------------------------------------------
# 5.1 — pending instinct count
# ---------------------------------------------------------------------------

def test_count_pending_instincts_none(tmp_path):
    """_count_pending_instincts returns 0 when no YAML files exist."""
    import session_stop
    inst_dir = tmp_path / "instincts"
    inst_dir.mkdir()
    assert session_stop._count_pending_instincts(inst_dir) == 0


def test_count_pending_instincts_counts_unreviewed(tmp_path):
    """_count_pending_instincts counts files with 'reviewed: false'."""
    import session_stop
    inst_dir = tmp_path / "instincts"
    inst_dir.mkdir()
    (inst_dir / "s1.yaml").write_text("reviewed: false\n")
    (inst_dir / "s2.yaml").write_text("reviewed: false\n")
    (inst_dir / "s3.yaml").write_text("reviewed: true\n")
    assert session_stop._count_pending_instincts(inst_dir) == 2


def test_session_stop_prints_pending_notification(tmp_path, monkeypatch, capsys):
    """Stop hook prints pending count notification when instincts exist."""
    monkeypatch.delenv("REPROGATE_DISABLED", raising=False)
    monkeypatch.delenv("REPROGATE_HOOK_PROFILE", raising=False)
    import session_stop
    inst_dir = tmp_path / "instincts"
    # Pre-populate with a pending instinct
    inst_dir.mkdir()
    (inst_dir / "old-session.yaml").write_text("reviewed: false\n")
    session_stop.main(session_data=tmp_path, instincts_dir=inst_dir)
    captured = capsys.readouterr()
    assert "미평가 instinct" in captured.err
    assert "learn-eval" in captured.err


# ---------------------------------------------------------------------------
# 5.3 — prose skill storage path and structure (via learn-eval command file)
# ---------------------------------------------------------------------------

def test_learn_eval_command_file_exists():
    """`.claude/commands/learn-eval.md` must exist."""
    repo_root = pathlib.Path(__file__).resolve().parents[2]
    cmd_file = repo_root / ".claude" / "commands" / "learn-eval.md"
    assert cmd_file.exists(), f"learn-eval.md command file not found at {cmd_file}"


def test_learn_eval_command_file_has_required_sections():
    """learn-eval.md must cover storage path and quality gate steps."""
    repo_root = pathlib.Path(__file__).resolve().parents[2]
    cmd_file = repo_root / ".claude" / "commands" / "learn-eval.md"
    content = cmd_file.read_text(encoding="utf-8")
    required_fragments = [
        "homunculus/evolved/skills",     # storage path
        "homunculus/instincts",          # instincts source
        "reviewed: true",                # state transition
        "promoted:",                     # promotion tracking
        "confidence: low",               # low-confidence handling
    ]
    for fragment in required_fragments:
        assert fragment in content, f"learn-eval.md must contain '{fragment}'"
