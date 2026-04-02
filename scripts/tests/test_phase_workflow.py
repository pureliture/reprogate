#!/usr/bin/env python3
"""Tests for phase workflow commands and artifacts."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent.parent
GITIGNORE = ROOT / ".gitignore"
COMMANDS_DIR = ROOT / ".claude" / "commands"
AGENT_CONTRACT = ROOT / "docs" / "spec" / "agent-contract.md"

RG_COMMANDS = ["rg-discuss", "rg-plan", "rg-execute", "rg-verify"]
AGENT_EMBEDDINGS = {
    "rg-plan": "planner.md",
    "rg-execute": "executor.md",
    "rg-verify": "verifier.md",
}
PREREQUISITES = {
    "rg-plan": "CONTEXT.md",
    "rg-execute": "PLAN.md",
    "rg-verify": "EXECUTION-LOG.md",
}


class TestPhaseArtifactPacket:
    """6.1 .rg/ gitignore addition."""

    def test_rg_directory_is_gitignored(self):
        content = GITIGNORE.read_text()
        assert ".rg/" in content, \
            ".gitignore must contain .rg/ to ignore phase artifact packets"

    def test_agent_contract_has_phase_workflow_section(self):
        content = AGENT_CONTRACT.read_text()
        assert "Phase Workflow" in content, \
            "docs/spec/agent-contract.md must have a Phase Workflow section"

    def test_agent_contract_rg_directory_convention(self):
        content = AGENT_CONTRACT.read_text()
        assert ".rg/" in content, \
            "agent-contract.md must reference .rg/ directory convention"

    def test_agent_contract_command_sequence(self):
        content = AGENT_CONTRACT.read_text()
        for cmd in ["/rg:discuss", "/rg:plan", "/rg:execute", "/rg:verify"]:
            assert cmd in content, \
                f"agent-contract.md must document {cmd} in Phase Workflow section"


class TestRgCommandsExistence:
    """6.2 All four /rg:* command files exist with required keywords."""

    @pytest.mark.parametrize("command", RG_COMMANDS)
    def test_command_file_exists(self, command):
        path = COMMANDS_DIR / f"{command}.md"
        assert path.exists(), f".claude/commands/{command}.md must exist"

    @pytest.mark.parametrize("command", RG_COMMANDS)
    def test_command_has_arguments_variable(self, command):
        content = (COMMANDS_DIR / f"{command}.md").read_text()
        assert "$ARGUMENTS" in content, \
            f"{command}.md must use $ARGUMENTS for phase name"

    def test_discuss_command_has_context_md_output(self):
        content = (COMMANDS_DIR / "rg-discuss.md").read_text()
        assert "CONTEXT.md" in content, \
            "rg-discuss.md must reference CONTEXT.md as output"

    def test_discuss_command_has_goal_and_requirements_questions(self):
        content = (COMMANDS_DIR / "rg-discuss.md").read_text()
        assert "Goal" in content and "Requirements" in content, \
            "rg-discuss.md must ask for Goal and Requirements"

    def test_rg_commands_tracked_in_gitignore(self):
        content = GITIGNORE.read_text()
        for cmd in RG_COMMANDS:
            assert f"{cmd}.md" in content, \
                f".gitignore must have exception for .claude/commands/{cmd}.md"


class TestAgentEmbeddingPattern:
    """6.3 Each command embeds its agent file."""

    @pytest.mark.parametrize("command,agent_file", AGENT_EMBEDDINGS.items())
    def test_command_references_agent_file(self, command, agent_file):
        content = (COMMANDS_DIR / f"{command}.md").read_text()
        assert agent_file in content, \
            f"{command}.md must reference .claude/agents/{agent_file}"

    @pytest.mark.parametrize("command", AGENT_EMBEDDINGS.keys())
    def test_command_instructs_reading_agent(self, command):
        content = (COMMANDS_DIR / f"{command}.md").read_text()
        assert "Read" in content or "read" in content, \
            f"{command}.md must instruct reading the agent file"

    @pytest.mark.parametrize("command", AGENT_EMBEDDINGS.keys())
    def test_command_acting_as_agent(self, command):
        content = (COMMANDS_DIR / f"{command}.md").read_text()
        assert "acting as" in content.lower() or "agent" in content.lower(), \
            f"{command}.md must indicate acting as the agent role"


class TestPrerequisiteChecks:
    """6.4 Each command checks for its prerequisite artifact."""

    @pytest.mark.parametrize("command,prereq", PREREQUISITES.items())
    def test_command_checks_prerequisite(self, command, prereq):
        content = (COMMANDS_DIR / f"{command}.md").read_text()
        assert prereq in content, \
            f"{command}.md must check for {prereq} as prerequisite"

    @pytest.mark.parametrize("command", PREREQUISITES.keys())
    def test_command_has_error_message_on_missing_prereq(self, command):
        content = (COMMANDS_DIR / f"{command}.md").read_text()
        assert "not found" in content.lower() or "❌" in content or "missing" in content.lower(), \
            f"{command}.md must show error when prerequisite is missing"

    @pytest.mark.parametrize("command", PREREQUISITES.keys())
    def test_command_suggests_previous_step(self, command):
        content = (COMMANDS_DIR / f"{command}.md").read_text()
        previous = {
            "rg-plan": "/rg:discuss",
            "rg-execute": "/rg:plan",
            "rg-verify": "/rg:execute",
        }
        assert previous[command] in content, \
            f"{command}.md must suggest running {previous[command]} when prerequisite is missing"

    def test_discuss_idempotent_check(self):
        content = (COMMANDS_DIR / "rg-discuss.md").read_text()
        assert "already exists" in content.lower() or "Overwrite" in content, \
            "rg-discuss.md must check for existing CONTEXT.md before overwriting"
