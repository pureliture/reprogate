#!/usr/bin/env python3
"""Tests for artifact lifecycle commands and schema (Phase 06)."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent.parent
COMMANDS_DIR = ROOT / ".claude" / "commands"
AGENTS_DIR = ROOT / ".claude" / "agents"
COMMANDS_GITIGNORE = COMMANDS_DIR / ".gitignore"
SUMMARIES_DIR = ROOT / "records" / "summaries"
SUMMARY_SCHEMA = ROOT / "docs" / "spec" / "phase-summary-schema.md"
RG_SUMMARY = COMMANDS_DIR / "rg-summary.md"
RG_HEALTH = COMMANDS_DIR / "rg-health.md"


class TestPhaseSummarySchema:
    """Task group 1: Phase summary schema and infrastructure."""

    def test_summaries_directory_exists(self):
        assert SUMMARIES_DIR.exists(), \
            "records/summaries/ directory must exist"

    def test_summaries_directory_has_gitkeep(self):
        gitkeep = SUMMARIES_DIR / ".gitkeep"
        assert gitkeep.exists(), \
            "records/summaries/.gitkeep must exist to track empty directory in git"

    def test_phase_summary_schema_exists(self):
        assert SUMMARY_SCHEMA.exists(), \
            "docs/spec/phase-summary-schema.md must exist"

    def test_phase_summary_schema_naming_convention(self):
        content = SUMMARY_SCHEMA.read_text()
        assert "YYYY-MM-DD" in content, \
            "phase-summary-schema.md must define YYYY-MM-DD naming convention"
        assert "records/summaries/" in content, \
            "phase-summary-schema.md must reference records/summaries/ path"

    def test_phase_summary_schema_required_sections(self):
        content = SUMMARY_SCHEMA.read_text()
        for section in ["## Goal", "## Outcome", "## Key Decisions", "## Deviations"]:
            assert section in content, \
                f"phase-summary-schema.md must define {section} section"

    def test_phase_summary_schema_result_field(self):
        content = SUMMARY_SCHEMA.read_text()
        assert "**Result:**" in content or "Result" in content, \
            "phase-summary-schema.md must define a Result field"

    def test_commands_gitignore_includes_rg_summary(self):
        content = COMMANDS_GITIGNORE.read_text()
        assert "!rg-summary.md" in content, \
            ".claude/commands/.gitignore must allowlist rg-summary.md"

    def test_commands_gitignore_includes_rg_health(self):
        content = COMMANDS_GITIGNORE.read_text()
        assert "!rg-health.md" in content, \
            ".claude/commands/.gitignore must allowlist rg-health.md"


class TestRgSummaryCommand:
    """Task group 2: /rg:summary command."""

    def test_rg_summary_exists(self):
        assert RG_SUMMARY.exists(), \
            ".claude/commands/rg-summary.md must exist"

    def test_rg_summary_arguments_reference(self):
        content = RG_SUMMARY.read_text()
        assert "$ARGUMENTS" in content, \
            "rg-summary.md must use $ARGUMENTS for phase name"

    def test_rg_summary_prerequisite_check(self):
        content = RG_SUMMARY.read_text()
        assert "VERIFICATION.md" in content, \
            "rg-summary.md must check for VERIFICATION.md as prerequisite"

    def test_rg_summary_reads_context(self):
        content = RG_SUMMARY.read_text()
        assert "CONTEXT.md" in content, \
            "rg-summary.md must read CONTEXT.md for Goal"

    def test_rg_summary_reads_execution_log(self):
        content = RG_SUMMARY.read_text()
        assert "EXECUTION-LOG.md" in content, \
            "rg-summary.md must read EXECUTION-LOG.md for deviations"

    def test_rg_summary_output_path_convention(self):
        content = RG_SUMMARY.read_text()
        assert "records/summaries/" in content, \
            "rg-summary.md must write output to records/summaries/"

    def test_rg_summary_date_stamped_output(self):
        content = RG_SUMMARY.read_text()
        assert "date" in content.lower() and ("YYYY-MM-DD" in content or "%Y-%m-%d" in content), \
            "rg-summary.md must produce date-stamped output file"

    def test_rg_summary_references_schema(self):
        content = RG_SUMMARY.read_text()
        assert "phase-summary-schema" in content, \
            "rg-summary.md must reference docs/spec/phase-summary-schema.md"

    def test_rg_summary_handles_pass_and_fail(self):
        content = RG_SUMMARY.read_text()
        assert "FAIL" in content, \
            "rg-summary.md must handle FAIL results explicitly"
        assert "PASS" in content, \
            "rg-summary.md must handle PASS results"


class TestRgHealthCommand:
    """Task group 3: /rg:health command."""

    def test_rg_health_exists(self):
        assert RG_HEALTH.exists(), \
            ".claude/commands/rg-health.md must exist"

    def test_rg_health_is_read_only(self):
        content = RG_HEALTH.read_text()
        lower = content.lower()
        assert "read-only" in lower or "does not modify" in lower or "not modify" in lower, \
            "rg-health.md must declare it is read-only and does not modify files"

    def test_rg_health_checks_hooks(self):
        content = RG_HEALTH.read_text()
        assert ".githooks" in content or "pre-commit" in content, \
            "rg-health.md must check git hooks"

    def test_rg_health_checks_skills(self):
        content = RG_HEALTH.read_text()
        assert "skills/" in content or "rules.rego" in content, \
            "rg-health.md must check skills/rules.rego files"

    def test_rg_health_checks_agents(self):
        content = RG_HEALTH.read_text()
        for agent in ["planner.md", "executor.md", "verifier.md"]:
            assert agent in content, \
                f"rg-health.md must check {agent}"

    def test_rg_health_checks_all_rg_commands(self):
        content = RG_HEALTH.read_text()
        for cmd in ["rg-discuss.md", "rg-plan.md", "rg-execute.md",
                    "rg-verify.md", "rg-summary.md", "rg-health.md"]:
            assert cmd in content, \
                f"rg-health.md must check {cmd}"

    def test_rg_health_checks_spec_docs(self):
        content = RG_HEALTH.read_text()
        assert "agent-contract.md" in content, \
            "rg-health.md must check docs/spec/agent-contract.md"
        assert "phase-summary-schema.md" in content, \
            "rg-health.md must check docs/spec/phase-summary-schema.md"

    def test_rg_health_includes_file_existence_caveat(self):
        content = RG_HEALTH.read_text()
        lower = content.lower()
        assert "file existence" in lower or "does not guarantee" in lower or "behavior" in lower, \
            "rg-health.md must note that checks are file-existence based, not behavioral"

    def test_rg_health_produces_dashboard_output(self):
        content = RG_HEALTH.read_text()
        assert "Overall" in content or "healthy" in content.lower(), \
            "rg-health.md must produce a summary dashboard with overall status"

    def test_rg_health_optional_phase_arg(self):
        content = RG_HEALTH.read_text()
        assert "$ARGUMENTS" in content, \
            "rg-health.md must support optional $ARGUMENTS for phase-specific check"


class TestArtifactLifecycleIntegration:
    """Integration: all 6 /rg:* commands are tracked."""

    def test_all_six_rg_commands_exist(self):
        expected = [
            "rg-discuss.md", "rg-plan.md", "rg-execute.md",
            "rg-verify.md", "rg-summary.md", "rg-health.md",
        ]
        for name in expected:
            assert (COMMANDS_DIR / name).exists(), \
                f".claude/commands/{name} must exist"

    def test_gitignore_allows_all_rg_commands(self):
        content = COMMANDS_GITIGNORE.read_text()
        expected = [
            "!rg-discuss.md", "!rg-plan.md", "!rg-execute.md",
            "!rg-verify.md", "!rg-summary.md", "!rg-health.md",
        ]
        for pattern in expected:
            assert pattern in content, \
                f".claude/commands/.gitignore must contain {pattern}"

    def test_summary_schema_references_rg_summary_command(self):
        content = SUMMARY_SCHEMA.read_text()
        assert "/rg:summary" in content or "rg:summary" in content, \
            "phase-summary-schema.md must reference the /rg:summary command"

    def test_phase_lifecycle_complete(self):
        """All 6 components of the lifecycle are present."""
        components = {
            "planner agent": AGENTS_DIR / "planner.md",
            "executor agent": AGENTS_DIR / "executor.md",
            "verifier agent": AGENTS_DIR / "verifier.md",
            "rg-summary command": COMMANDS_DIR / "rg-summary.md",
            "rg-health command": COMMANDS_DIR / "rg-health.md",
            "phase-summary-schema": SUMMARY_SCHEMA,
            "summaries directory": SUMMARIES_DIR,
        }
        for name, path in components.items():
            assert path.exists(), f"Phase lifecycle component missing: {name} at {path}"
