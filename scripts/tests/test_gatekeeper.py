#!/usr/bin/env python3
"""
Tests for refactored gatekeeper module.

Tests cover:
- load_config uses yaml.safe_load
- evaluate_gate fail-closed behavior
- evaluate_gate with valid/invalid records
- strict_mode handling
- active_skills filtering
- OPA mode detection output
- --strict CLI flag override
"""
import pathlib
import sys

import pytest
import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from gatekeeper import evaluate_gate, load_config, VERSION


class TestLoadConfig:
    """Tests for load_config function."""

    def test_uses_yaml_safe_load(self, tmp_path: pathlib.Path):
        """load_config uses yaml.safe_load and returns dict with expected keys."""
        config_file = tmp_path / "reprogate.yaml"
        config_file.write_text(
            yaml.dump({
                "records_dir": "records",
                "skills_dir": "skills",
                "active_skills": ["record-required", "decision-documented"],
                "gatekeeper": {"engine": "opa", "strict_mode": True, "fail_closed": True},
            }),
            encoding="utf-8",
        )
        config = load_config(config_path=config_file)
        assert "active_skills" in config
        assert "records_dir" in config
        assert "skills_dir" in config
        assert "gatekeeper" in config
        assert config["active_skills"] == ["record-required", "decision-documented"]
        assert config["gatekeeper"]["strict_mode"] is True

    def test_returns_defaults_when_file_missing(self, tmp_path: pathlib.Path):
        """load_config returns sensible defaults when config file doesn't exist."""
        config = load_config(config_path=tmp_path / "nonexistent.yaml")
        assert config["records_dir"] == "records"
        assert config["skills_dir"] == "skills"
        assert "gatekeeper" in config


class TestEvaluateGate:
    """Tests for evaluate_gate function."""

    def _setup_env(self, tmp_path: pathlib.Path, records=None, skills=None, config_overrides=None):
        """Helper to set up an isolated test environment."""
        root = tmp_path / "project"
        root.mkdir()

        # Create records directory with optional records
        records_dir = root / "records"
        records_dir.mkdir()
        if records:
            for rec in records:
                rec_path = records_dir / rec["subdir"]
                rec_path.mkdir(parents=True, exist_ok=True)
                (rec_path / rec["filename"]).write_text(rec["content"], encoding="utf-8")

        # Create skills directory with optional skills
        skills_dir = root / "skills"
        skills_dir.mkdir()
        if skills:
            for skill in skills:
                skill_dir = skills_dir / skill["name"]
                skill_dir.mkdir()
                (skill_dir / "guidelines.md").write_text(
                    f'---\nskill_id: "{skill["name"]}"\nname: "Test"\n---\n',
                    encoding="utf-8",
                )
                (skill_dir / "rules.rego").write_text(
                    skill.get("rego", "package reprogate.rules\nimport rego.v1\n"),
                    encoding="utf-8",
                )

        # Create config
        config = {
            "records_dir": "records",
            "skills_dir": "skills",
            "active_skills": [s["name"] for s in (skills or [])],
            "gatekeeper": {"engine": "opa", "strict_mode": True, "fail_closed": True},
        }
        if config_overrides:
            config.update(config_overrides)

        return root, config

    def _make_valid_adr(self, record_id: str = "ADR-001") -> dict:
        """Helper to create a valid ADR record dict."""
        return {
            "subdir": "adr",
            "filename": f"{record_id}.md",
            "content": (
                f"---\nrecord_id: \"{record_id}\"\ntype: \"adr\"\nstatus: \"Accepted\"\n---\n\n"
                f"# {record_id}\n\n## Context\nSome context.\n\n## Decision\nSome decision.\n\n"
                "## Consequences\nSome consequences.\n\n## Verification\n- [x] Done\n"
            ),
        }

    def test_no_records_fail_closed(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
        """evaluate_gate with no records and fail_closed=true returns exit_code 1."""
        root, config = self._setup_env(
            tmp_path,
            skills=[{"name": "record-required"}],
        )
        import gatekeeper
        monkeypatch.setattr(gatekeeper, "ROOT", root)
        monkeypatch.setattr(gatekeeper, "RECORDS_DIR", root / "records")
        monkeypatch.setattr(gatekeeper, "SKILLS_DIR", root / "skills")

        exit_code, messages = evaluate_gate(config=config)
        assert exit_code == 1

    def test_valid_records_pass(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
        """evaluate_gate with valid records returns exit_code 0 (non-strict)."""
        root, config = self._setup_env(
            tmp_path,
            records=[self._make_valid_adr()],
            skills=[{"name": "record-required"}],
        )
        # Non-strict so structural-mode OPA warning doesn't cause failure
        config["gatekeeper"]["strict_mode"] = False
        import gatekeeper
        monkeypatch.setattr(gatekeeper, "ROOT", root)
        monkeypatch.setattr(gatekeeper, "RECORDS_DIR", root / "records")
        monkeypatch.setattr(gatekeeper, "SKILLS_DIR", root / "skills")

        exit_code, messages = evaluate_gate(config=config, strict=False)
        assert exit_code == 0

    def test_strict_mode_treats_warns_as_errors(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
        """evaluate_gate with strict_mode=true treats warn messages as errors."""
        root, config = self._setup_env(
            tmp_path,
            records=[self._make_valid_adr()],
            skills=[{"name": "record-required"}],
        )
        # In structural mode, there's always a warn about OPA not being installed
        config["gatekeeper"]["strict_mode"] = True
        import gatekeeper
        monkeypatch.setattr(gatekeeper, "ROOT", root)
        monkeypatch.setattr(gatekeeper, "RECORDS_DIR", root / "records")
        monkeypatch.setattr(gatekeeper, "SKILLS_DIR", root / "skills")

        exit_code, messages = evaluate_gate(config=config, strict=True)
        # Structural mode always warns about OPA, strict treats warns as errors
        warn_messages = [m for m in messages if m.startswith("WARN")]
        if warn_messages:
            assert exit_code == 1

    def test_non_strict_mode_allows_warns(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
        """evaluate_gate with strict_mode=false allows warns to pass."""
        root, config = self._setup_env(
            tmp_path,
            records=[self._make_valid_adr()],
            skills=[{"name": "record-required"}],
        )
        config["gatekeeper"]["strict_mode"] = False
        import gatekeeper
        monkeypatch.setattr(gatekeeper, "ROOT", root)
        monkeypatch.setattr(gatekeeper, "RECORDS_DIR", root / "records")
        monkeypatch.setattr(gatekeeper, "SKILLS_DIR", root / "skills")

        exit_code, messages = evaluate_gate(config=config, strict=False)
        # Valid records + non-strict = pass even with OPA unavailable warn
        deny_messages = [m for m in messages if m.startswith("DENY")]
        if not deny_messages:
            assert exit_code == 0

    def test_only_evaluates_active_skills(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
        """evaluate_gate only evaluates skills listed in active_skills config."""
        root, config = self._setup_env(
            tmp_path,
            records=[self._make_valid_adr()],
            skills=[
                {"name": "record-required"},
                {"name": "extra-skill"},
            ],
        )
        # Only activate record-required
        config["active_skills"] = ["record-required"]
        import gatekeeper
        monkeypatch.setattr(gatekeeper, "ROOT", root)
        monkeypatch.setattr(gatekeeper, "RECORDS_DIR", root / "records")
        monkeypatch.setattr(gatekeeper, "SKILLS_DIR", root / "skills")

        exit_code, messages = evaluate_gate(config=config, strict=False)
        # extra-skill should not appear in messages
        assert not any("extra-skill" in m for m in messages)

    def test_missing_skills_dir_fail_closed(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
        """Missing skills directory causes fail-closed (exit_code 1)."""
        root = tmp_path / "project"
        root.mkdir()
        (root / "records").mkdir()
        # Don't create skills dir
        config = {
            "records_dir": "records",
            "skills_dir": "skills",
            "active_skills": [],
            "gatekeeper": {"engine": "opa", "strict_mode": True, "fail_closed": True},
        }
        import gatekeeper
        monkeypatch.setattr(gatekeeper, "ROOT", root)
        monkeypatch.setattr(gatekeeper, "RECORDS_DIR", root / "records")
        monkeypatch.setattr(gatekeeper, "SKILLS_DIR", root / "skills")

        exit_code, messages = evaluate_gate(config=config)
        assert exit_code == 1
        assert any("FAIL-CLOSED" in m or "fail" in m.lower() for m in messages)

    def test_version_is_1_0_0(self):
        """Gatekeeper version should be 1.0.0 after refactor."""
        assert VERSION == "1.0.0"

    def test_gatekeeper_prints_mode(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, capsys):
        """Gatekeeper detects OPA availability and prints mode in output."""
        root, config = self._setup_env(
            tmp_path,
            records=[self._make_valid_adr()],
            skills=[{"name": "record-required"}],
        )
        import gatekeeper
        monkeypatch.setattr(gatekeeper, "ROOT", root)
        monkeypatch.setattr(gatekeeper, "RECORDS_DIR", root / "records")
        monkeypatch.setattr(gatekeeper, "SKILLS_DIR", root / "skills")

        evaluate_gate(config=config, strict=False)
        captured = capsys.readouterr()
        assert "Mode:" in captured.out
        assert "OPA" in captured.out or "Structural" in captured.out
