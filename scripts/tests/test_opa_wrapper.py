#!/usr/bin/env python3
"""
Tests for OPA wrapper module.

Tests cover:
- is_opa_available() detection
- build_input_data() conversion
- evaluate_skill_opa() OPA binary integration (skipped if OPA not installed)
- evaluate_skill_structural() degraded mode fallback
- SkillResult dataclass
"""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from opa_wrapper import (
    SkillResult,
    build_input_data,
    evaluate_skill_opa,
    evaluate_skill_structural,
    is_opa_available,
)


class TestIsOpaAvailable:
    """Tests for is_opa_available function."""

    def test_returns_bool(self):
        """is_opa_available returns a boolean."""
        result = is_opa_available()
        assert isinstance(result, bool)


class TestBuildInputData:
    """Tests for build_input_data function."""

    def test_converts_records_to_json_contract(self, tmp_path: pathlib.Path):
        """build_input_data converts collected records to OPA input JSON format."""
        root = tmp_path
        records = [
            (
                root / "records" / "adr" / "ADR-001.md",
                {"record_id": "ADR-001", "type": "adr", "status": "Accepted"},
                ["Context", "Decision", "Consequences", "Verification"],
            ),
        ]
        result = build_input_data(records, root)

        assert "records" in result
        assert len(result["records"]) == 1
        rec = result["records"][0]
        assert rec["path"] == "records/adr/ADR-001.md"
        assert rec["frontmatter"]["record_id"] == "ADR-001"
        assert rec["sections"]["Context"] is True
        assert rec["sections"]["Verification"] is True

    def test_empty_records(self, tmp_path: pathlib.Path):
        """build_input_data with empty records list produces empty records array."""
        result = build_input_data([], tmp_path)
        assert result == {"records": []}

    def test_multiple_records(self, tmp_path: pathlib.Path):
        """build_input_data handles multiple records."""
        root = tmp_path
        records = [
            (root / "records" / "adr" / "ADR-001.md", {"record_id": "ADR-001"}, ["Context"]),
            (root / "records" / "rfc" / "RFC-001.md", {"record_id": "RFC-001"}, ["Summary"]),
        ]
        result = build_input_data(records, root)
        assert len(result["records"]) == 2


class TestSkillResult:
    """Tests for SkillResult dataclass."""

    def test_skill_result_has_required_fields(self):
        """SkillResult has skill_id, deny, warn, and mode fields."""
        result = SkillResult(skill_id="test-skill", deny=["error"], warn=["warning"], mode="opa")
        assert result.skill_id == "test-skill"
        assert result.deny == ["error"]
        assert result.warn == ["warning"]
        assert result.mode == "opa"

    def test_skill_result_mode_structural(self):
        """SkillResult can have mode='structural'."""
        result = SkillResult(skill_id="test", deny=[], warn=[], mode="structural")
        assert result.mode == "structural"


class TestEvaluateSkillOpa:
    """Tests for evaluate_skill_opa function (requires OPA binary)."""

    @pytest.mark.skipif(not is_opa_available(), reason="OPA not installed")
    def test_returns_deny_when_no_records(self, tmp_path: pathlib.Path):
        """evaluate_skill_opa returns deny messages when records are empty."""
        # Set up a skill directory with record-required rules.rego
        skill_dir = tmp_path / "record-required"
        skill_dir.mkdir()
        # Copy the real rules.rego content
        (skill_dir / "rules.rego").write_text(
            'package reprogate.rules\n\nimport rego.v1\n\n'
            'deny contains msg if {\n'
            '    count(input.records) == 0\n'
            '    msg := "No records found"\n'
            '}\n',
            encoding="utf-8",
        )
        (skill_dir / "guidelines.md").write_text(
            '---\nskill_id: "record-required"\nname: "Record Required"\n---\n',
            encoding="utf-8",
        )
        input_data = {"records": []}
        result = evaluate_skill_opa(skill_dir, input_data)
        assert isinstance(result, SkillResult)
        assert result.mode == "opa"
        assert len(result.deny) > 0

    @pytest.mark.skipif(not is_opa_available(), reason="OPA not installed")
    def test_returns_empty_deny_with_valid_records(self, tmp_path: pathlib.Path):
        """evaluate_skill_opa returns empty deny when valid records provided."""
        skill_dir = tmp_path / "record-required"
        skill_dir.mkdir()
        (skill_dir / "rules.rego").write_text(
            'package reprogate.rules\n\nimport rego.v1\n\n'
            'deny contains msg if {\n'
            '    count(input.records) == 0\n'
            '    msg := "No records found"\n'
            '}\n',
            encoding="utf-8",
        )
        (skill_dir / "guidelines.md").write_text(
            '---\nskill_id: "record-required"\nname: "Record Required"\n---\n',
            encoding="utf-8",
        )
        input_data = {
            "records": [
                {
                    "path": "records/adr/ADR-001.md",
                    "frontmatter": {"record_id": "ADR-001", "type": "adr", "status": "Accepted"},
                    "sections": {"Context": True, "Decision": True},
                }
            ]
        }
        result = evaluate_skill_opa(skill_dir, input_data)
        assert isinstance(result, SkillResult)
        assert result.mode == "opa"
        assert len(result.deny) == 0


class TestEvaluateSkillStructural:
    """Tests for evaluate_skill_structural function (degraded mode)."""

    def _make_skill_dir(self, tmp_path: pathlib.Path, skill_id: str = "record-required") -> pathlib.Path:
        """Helper to create a minimal skill directory."""
        skill_dir = tmp_path / skill_id
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "guidelines.md").write_text(
            f'---\nskill_id: "{skill_id}"\nname: "Test Skill"\n---\n',
            encoding="utf-8",
        )
        (skill_dir / "rules.rego").write_text(
            'package reprogate.rules\nimport rego.v1\n',
            encoding="utf-8",
        )
        return skill_dir

    def test_detects_missing_records(self, tmp_path: pathlib.Path):
        """evaluate_skill_structural produces deny when no records exist."""
        skill_dir = self._make_skill_dir(tmp_path)
        input_data = {"records": []}
        result = evaluate_skill_structural(skill_dir, input_data)
        assert isinstance(result, SkillResult)
        assert result.mode == "structural"
        assert any("No records found" in msg for msg in result.deny)

    def test_detects_missing_frontmatter_fields(self, tmp_path: pathlib.Path):
        """evaluate_skill_structural detects missing record_id and status."""
        skill_dir = self._make_skill_dir(tmp_path)
        input_data = {
            "records": [
                {
                    "path": "records/adr/ADR-001.md",
                    "frontmatter": {},
                    "sections": {"Verification": True},
                }
            ]
        }
        result = evaluate_skill_structural(skill_dir, input_data)
        assert result.mode == "structural"
        assert any("record_id" in msg for msg in result.deny)
        assert any("status" in msg for msg in result.deny)

    def test_detects_missing_verification_section(self, tmp_path: pathlib.Path):
        """evaluate_skill_structural detects missing Verification section."""
        skill_dir = self._make_skill_dir(tmp_path)
        input_data = {
            "records": [
                {
                    "path": "records/adr/ADR-001.md",
                    "frontmatter": {"record_id": "ADR-001", "status": "Accepted"},
                    "sections": {"Context": True},
                }
            ]
        }
        result = evaluate_skill_structural(skill_dir, input_data)
        assert result.mode == "structural"
        assert any("Verification" in msg for msg in result.deny)

    def test_emits_opa_unavailable_warning(self, tmp_path: pathlib.Path):
        """evaluate_skill_structural warns that OPA is not available."""
        skill_dir = self._make_skill_dir(tmp_path)
        input_data = {
            "records": [
                {
                    "path": "records/adr/ADR-001.md",
                    "frontmatter": {"record_id": "ADR-001", "status": "Accepted"},
                    "sections": {"Verification": True},
                }
            ]
        }
        result = evaluate_skill_structural(skill_dir, input_data)
        assert result.mode == "structural"
        assert any("OPA is not installed" in msg or "degraded" in msg.lower() for msg in result.warn)

    def test_passes_with_valid_records(self, tmp_path: pathlib.Path):
        """evaluate_skill_structural has no deny for valid records."""
        skill_dir = self._make_skill_dir(tmp_path)
        input_data = {
            "records": [
                {
                    "path": "records/adr/ADR-001.md",
                    "frontmatter": {"record_id": "ADR-001", "status": "Accepted"},
                    "sections": {"Verification": True},
                }
            ]
        }
        result = evaluate_skill_structural(skill_dir, input_data)
        assert result.mode == "structural"
        assert len(result.deny) == 0
