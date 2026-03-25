#!/usr/bin/env python3
"""
End-to-end integration tests for the ReproGate pipeline.

Tests the full init -> create -> gatekeeper flow using subprocess calls,
verifying that all CORE requirements (01-05) work together as a system.

CORE-01: Record creation (create_record.py)
CORE-02: Gate enforcement (gatekeeper.py)
CORE-03: Skill-based policy checks (OPA/structural fallback)
CORE-04: Repository initialization (init.py)
CORE-05: CLI entry point (cli.py)

NOTE on gatekeeper isolation: The gatekeeper uses ROOT (script parent dir) to
locate records/ and skills/ at module import time.  Integration tests that need
an isolated environment use monkeypatch to override the module-level constants
(RECORDS_DIR, SKILLS_DIR) or run gatekeeper against the real repository root.
"""
import pathlib
import shutil
import subprocess
import sys

import pytest
import yaml

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parents[1]
ROOT = SCRIPTS_DIR.parent


def run_script(
    script: str,
    args: list,
    cwd: pathlib.Path | None = None,
) -> subprocess.CompletedProcess:
    """Run a script from the scripts directory as a subprocess."""
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script)] + args,
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else str(ROOT),
        timeout=30,
    )


# ---------------------------------------------------------------------------
# CORE-04: init.py creates valid config
# ---------------------------------------------------------------------------


def test_init_creates_expanded_config(tmp_path: pathlib.Path) -> None:
    """init.py produces reprogate.yaml with expected keys (CORE-04)."""
    config_path = tmp_path / "reprogate.yaml"
    result = run_script(
        "init.py",
        ["--output", str(config_path), "--project-name", "TestProject", "--force"],
    )
    assert result.returncode == 0, f"init.py failed: {result.stderr}"
    assert config_path.exists()

    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    assert data["project_name"] == "TestProject"
    assert "active_skills" in data
    assert "record_types" in data
    assert data["gatekeeper"]["fail_closed"] is True


# ---------------------------------------------------------------------------
# CORE-01: create_record.py produces valid records
# ---------------------------------------------------------------------------


def test_create_adr_produces_valid_record(tmp_path: pathlib.Path) -> None:
    """create_record.py creates ADR with correct frontmatter and sections (CORE-01)."""
    result = run_script(
        "create_record.py",
        ["--type", "adr", "--title", "Test Decision", "--output-dir", str(tmp_path)],
    )
    assert result.returncode == 0, f"create_record.py failed: {result.stderr}"

    adr_dir = tmp_path / "adr"
    assert adr_dir.exists(), "adr/ subdirectory not created"
    files = list(adr_dir.glob("ADR-*.md"))
    assert len(files) == 1, f"Expected 1 ADR file, found {len(files)}"

    content = files[0].read_text(encoding="utf-8")
    # Verify frontmatter fields
    fm = yaml.safe_load(content.split("---")[1])
    assert fm["type"] == "adr"
    assert fm["status"] == "DRAFT"
    assert "record_id" in fm

    # Verify required sections
    for section in ("Context", "Decision", "Consequences", "Verification"):
        assert f"# {section}" in content, f"Missing section: {section}"


def test_create_rfc_produces_valid_record(tmp_path: pathlib.Path) -> None:
    """create_record.py creates RFC with correct sections (CORE-01)."""
    result = run_script(
        "create_record.py",
        ["--type", "rfc", "--title", "Test Proposal", "--output-dir", str(tmp_path)],
    )
    assert result.returncode == 0, f"create_record.py failed: {result.stderr}"

    rfc_dir = tmp_path / "rfc"
    files = list(rfc_dir.glob("RFC-*.md"))
    assert len(files) == 1

    content = files[0].read_text(encoding="utf-8")
    for section in ("Summary", "Design / Proposal", "Verification"):
        assert f"# {section}" in content, f"Missing section: {section}"


# ---------------------------------------------------------------------------
# CORE-02 / CORE-03: gatekeeper.py evaluates records against skills
# ---------------------------------------------------------------------------


def _setup_gatekeeper_env(
    base: pathlib.Path,
    *,
    create_record: bool = True,
    strict: bool = False,
) -> pathlib.Path:
    """Create an isolated gatekeeper environment with config, skills, and optional record.

    Returns the config file path.
    """
    # Copy skills from real repo
    skills_src = ROOT / "skills"
    skills_dst = base / "skills"
    if skills_src.exists():
        shutil.copytree(skills_src, skills_dst)

    # Create records directory
    records_dir = base / "records"
    records_dir.mkdir(parents=True, exist_ok=True)

    if create_record:
        adr_dir = records_dir / "adr"
        adr_dir.mkdir(parents=True, exist_ok=True)
        adr_content = (
            '---\nrecord_id: "ADR-001"\ntitle: "Test"\n'
            'type: "adr"\nstatus: "DRAFT"\n---\n\n'
            "# Context\n\nTest context.\n\n"
            "# Decision\n\nTest decision.\n\n"
            "# Consequences\n\nTest consequences.\n\n"
            "# Verification\n\nTest verification.\n"
        )
        (adr_dir / "ADR-001-test.md").write_text(adr_content, encoding="utf-8")

    # Create reprogate.yaml
    config = {
        "project_name": "TestGate",
        "records_dir": "records",
        "skills_dir": "skills",
        "active_skills": ["record-required"],
        "gatekeeper": {
            "engine": "opa",
            "strict_mode": strict,
            "fail_closed": True,
        },
    }
    config_path = base / "reprogate.yaml"
    config_path.write_text(yaml.dump(config), encoding="utf-8")
    return config_path


def test_gatekeeper_passes_with_valid_records(tmp_path: pathlib.Path, monkeypatch) -> None:
    """gatekeeper.py returns exit 0 when valid records exist (CORE-02)."""
    config_path = _setup_gatekeeper_env(tmp_path, create_record=True)

    # Monkeypatch the gatekeeper module-level ROOT to use tmp_path
    monkeypatch.setenv("_REPROGATE_TEST_ROOT", str(tmp_path))

    # Import and patch gatekeeper module constants
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import importlib
        import gatekeeper

        monkeypatch.setattr(gatekeeper, "ROOT", tmp_path)
        monkeypatch.setattr(gatekeeper, "RECORDS_DIR", tmp_path / "records")
        monkeypatch.setattr(gatekeeper, "SKILLS_DIR", tmp_path / "skills")
        # Also patch the opa_wrapper ROOT so structural fallback uses tmp_path
        import opa_wrapper

        monkeypatch.setattr(opa_wrapper, "ROOT", tmp_path)
        monkeypatch.setattr(opa_wrapper, "SKILLS_DIR", tmp_path / "skills")

        config = gatekeeper.load_config(config_path)
        exit_code, messages = gatekeeper.evaluate_gate(config=config, strict=False)
    finally:
        sys.path.pop(0)

    deny_messages = [m for m in messages if m.startswith("DENY")]
    assert exit_code == 0, f"Gate should pass but got exit {exit_code}: {deny_messages}"


def test_gatekeeper_fails_with_no_records(tmp_path: pathlib.Path, monkeypatch) -> None:
    """gatekeeper.py returns exit 1 when no records exist (CORE-02, fail-closed)."""
    config_path = _setup_gatekeeper_env(tmp_path, create_record=False)

    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import importlib
        import gatekeeper

        monkeypatch.setattr(gatekeeper, "ROOT", tmp_path)
        monkeypatch.setattr(gatekeeper, "RECORDS_DIR", tmp_path / "records")
        monkeypatch.setattr(gatekeeper, "SKILLS_DIR", tmp_path / "skills")
        import opa_wrapper

        monkeypatch.setattr(opa_wrapper, "ROOT", tmp_path)
        monkeypatch.setattr(opa_wrapper, "SKILLS_DIR", tmp_path / "skills")

        config = gatekeeper.load_config(config_path)
        exit_code, messages = gatekeeper.evaluate_gate(config=config, strict=False)
    finally:
        sys.path.pop(0)

    assert exit_code == 1, f"Gate should fail but got exit {exit_code}: {messages}"
    combined = " ".join(messages).lower()
    assert "deny" in combined or "fail" in combined or "no records" in combined, (
        f"Expected deny/fail message, got: {messages}"
    )


# ---------------------------------------------------------------------------
# Full pipeline: init -> create -> gatekeeper (CORE-01 through CORE-05)
# ---------------------------------------------------------------------------


def test_full_pipeline(tmp_path: pathlib.Path, monkeypatch) -> None:
    """Full pipeline: init -> create record -> gatekeeper passes (all CORE reqs)."""
    # Step 1: Init (CORE-04)
    init_result = run_script(
        "init.py",
        [
            "--output", str(tmp_path / "reprogate.yaml"),
            "--project-name", "PipelineTest",
            "--force",
        ],
    )
    assert init_result.returncode == 0, f"init failed: {init_result.stderr}"

    # Step 2: Copy skills from real repo
    skills_src = ROOT / "skills"
    skills_dst = tmp_path / "skills"
    if skills_src.exists():
        shutil.copytree(skills_src, skills_dst)

    # Step 3: Create records directory and record (CORE-01)
    records_dir = tmp_path / "records"
    create_result = run_script(
        "create_record.py",
        ["--type", "adr", "--title", "Pipeline Test ADR", "--output-dir", str(records_dir)],
    )
    assert create_result.returncode == 0, f"create_record failed: {create_result.stderr}"

    # Step 4: Run gatekeeper with monkeypatched ROOT (CORE-02, CORE-03)
    # Override the init-generated config: use strict_mode=false so structural
    # fallback warnings (OPA not installed) don't cause failures, and limit
    # active_skills to record-required since we only created one ADR.
    config_data = yaml.safe_load((tmp_path / "reprogate.yaml").read_text(encoding="utf-8"))
    config_data["gatekeeper"]["strict_mode"] = False
    config_data["active_skills"] = ["record-required"]
    (tmp_path / "reprogate.yaml").write_text(yaml.dump(config_data), encoding="utf-8")

    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import gatekeeper
        import opa_wrapper

        monkeypatch.setattr(gatekeeper, "ROOT", tmp_path)
        monkeypatch.setattr(gatekeeper, "RECORDS_DIR", tmp_path / "records")
        monkeypatch.setattr(gatekeeper, "SKILLS_DIR", tmp_path / "skills")
        monkeypatch.setattr(opa_wrapper, "ROOT", tmp_path)
        monkeypatch.setattr(opa_wrapper, "SKILLS_DIR", tmp_path / "skills")

        config = gatekeeper.load_config(tmp_path / "reprogate.yaml")
        exit_code, messages = gatekeeper.evaluate_gate(config=config, strict=False)
    finally:
        sys.path.pop(0)

    deny_messages = [m for m in messages if m.startswith("DENY")]
    assert exit_code == 0, (
        f"Full pipeline gate should pass but got exit {exit_code}: {deny_messages}"
    )


# ---------------------------------------------------------------------------
# CORE-05: CLI routes create command correctly
# ---------------------------------------------------------------------------


def test_cli_routes_create(tmp_path: pathlib.Path) -> None:
    """cli.py routes 'create' command to create_record.py (CORE-05)."""
    result = run_script(
        "cli.py",
        ["create", "--", "--type", "adr", "--title", "CLI Test", "--output-dir", str(tmp_path)],
    )
    assert result.returncode == 0, f"cli.py create failed: {result.stderr}"

    adr_dir = tmp_path / "adr"
    assert adr_dir.exists(), "adr/ directory not created via CLI"
    files = list(adr_dir.glob("ADR-*.md"))
    assert len(files) == 1, f"Expected 1 ADR file via CLI, found {len(files)}"


def test_cli_routes_check(tmp_path: pathlib.Path) -> None:
    """cli.py routes 'check' command to gatekeeper.py (CORE-05)."""
    result = run_script("cli.py", ["check"])
    # Should run without crashing -- exit code depends on repo state
    assert result.returncode in (0, 1), f"cli.py check crashed: {result.stderr}"
    combined = result.stdout + result.stderr
    assert "gate passed" in combined.lower() or "gate failed" in combined.lower(), (
        f"Expected gate verdict in output: {combined}"
    )
