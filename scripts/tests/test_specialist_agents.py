#!/usr/bin/env python3
"""Tests for specialist agent definitions and agent-contract.md."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent.parent
DOCS_SPEC = ROOT / "docs" / "spec"
AGENTS_DIR = ROOT / ".claude" / "agents"


class TestAgentContractDoc:
    """5.1 docs/spec/agent-contract.md existence and required sections."""

    def test_agent_contract_exists(self):
        assert (DOCS_SPEC / "agent-contract.md").exists(), \
            "docs/spec/agent-contract.md must exist"

    def test_agent_contract_has_context_section(self):
        content = (DOCS_SPEC / "agent-contract.md").read_text()
        assert "## CONTEXT.md" in content, \
            "agent-contract.md must define CONTEXT.md schema"

    def test_agent_contract_has_plan_section(self):
        content = (DOCS_SPEC / "agent-contract.md").read_text()
        assert "## PLAN.md" in content, \
            "agent-contract.md must define PLAN.md schema"

    def test_agent_contract_has_execution_log_section(self):
        content = (DOCS_SPEC / "agent-contract.md").read_text()
        assert "## EXECUTION-LOG.md" in content, \
            "agent-contract.md must define EXECUTION-LOG.md schema"

    def test_agent_contract_has_verification_section(self):
        content = (DOCS_SPEC / "agent-contract.md").read_text()
        assert "## VERIFICATION.md" in content, \
            "agent-contract.md must define VERIFICATION.md schema"

    def test_agent_contract_has_rules_section(self):
        content = (DOCS_SPEC / "agent-contract.md").read_text()
        assert "## Rules" in content, \
            "agent-contract.md must have a Rules section"

    def test_agent_contract_handoff_pipeline(self):
        content = (DOCS_SPEC / "agent-contract.md").read_text()
        assert "planner" in content.lower()
        assert "executor" in content.lower()
        assert "verifier" in content.lower()


class TestPlannerAgent:
    """5.2 planner agent file existence and input/output contract keywords."""

    def test_planner_agent_exists(self):
        assert (AGENTS_DIR / "planner.md").exists(), \
            ".claude/agents/planner.md must exist"

    def test_planner_has_input_contract(self):
        content = (AGENTS_DIR / "planner.md").read_text()
        assert "CONTEXT.md" in content, \
            "planner.md must reference CONTEXT.md as input"

    def test_planner_has_output_contract(self):
        content = (AGENTS_DIR / "planner.md").read_text()
        assert "PLAN.md" in content, \
            "planner.md must reference PLAN.md as output"

    def test_planner_has_code_guardrail(self):
        content = (AGENTS_DIR / "planner.md").read_text()
        assert "MUST NOT" in content, \
            "planner.md must have MUST NOT guardrail for code modification"
        # Check that no-code-modification is explicitly stated
        assert any(phrase in content for phrase in [
            "MUST NOT modify any source code",
            "MUST NOT** modify any source code",
        ]), "planner must explicitly forbid modifying source code files"

    def test_planner_has_requirements_coverage_check(self):
        content = (AGENTS_DIR / "planner.md").read_text()
        assert "requirement" in content.lower(), \
            "planner.md must reference requirements coverage"


class TestExecutorAgent:
    """5.3 executor agent file existence and deviation handling spec."""

    def test_executor_agent_exists(self):
        assert (AGENTS_DIR / "executor.md").exists(), \
            ".claude/agents/executor.md must exist"

    def test_executor_has_input_contract(self):
        content = (AGENTS_DIR / "executor.md").read_text()
        assert "PLAN.md" in content, \
            "executor.md must reference PLAN.md as input"

    def test_executor_has_output_contract(self):
        content = (AGENTS_DIR / "executor.md").read_text()
        assert "EXECUTION-LOG.md" in content, \
            "executor.md must reference EXECUTION-LOG.md as output"

    def test_executor_has_deviation_handling(self):
        content = (AGENTS_DIR / "executor.md").read_text()
        assert "deviation" in content.lower(), \
            "executor.md must describe deviation handling"

    def test_executor_deviation_must_be_recorded(self):
        content = (AGENTS_DIR / "executor.md").read_text()
        assert "MUST" in content and "record" in content.lower(), \
            "executor.md must require recording deviations"

    def test_executor_no_plan_rewrite_guardrail(self):
        content = (AGENTS_DIR / "executor.md").read_text()
        assert "MUST NOT" in content, \
            "executor.md must have MUST NOT guardrail"
        assert any(phrase in content for phrase in [
            "rewrite", "modify PLAN.md",
        ]), "executor must explicitly forbid rewriting PLAN.md"

    def test_executor_has_failure_handling(self):
        content = (AGENTS_DIR / "executor.md").read_text()
        assert "FAILED" in content or "Failed Tasks" in content, \
            "executor.md must describe failure handling"


class TestVerifierAgent:
    """5.4 verifier agent file existence and PASS/FAIL structure."""

    def test_verifier_agent_exists(self):
        assert (AGENTS_DIR / "verifier.md").exists(), \
            ".claude/agents/verifier.md must exist"

    def test_verifier_has_input_contract(self):
        content = (AGENTS_DIR / "verifier.md").read_text()
        assert "EXECUTION-LOG.md" in content, \
            "verifier.md must reference EXECUTION-LOG.md as input"
        assert "CONTEXT.md" in content, \
            "verifier.md must reference CONTEXT.md (requirements)"

    def test_verifier_has_pass_fail_output(self):
        content = (AGENTS_DIR / "verifier.md").read_text()
        assert "PASS" in content and "FAIL" in content, \
            "verifier.md must define PASS/FAIL verdict"

    def test_verifier_has_requirements_coverage(self):
        content = (AGENTS_DIR / "verifier.md").read_text()
        assert "Requirements Coverage" in content, \
            "verifier.md must require Requirements Coverage table"

    def test_verifier_has_deviation_review(self):
        content = (AGENTS_DIR / "verifier.md").read_text()
        assert "Deviation Review" in content, \
            "verifier.md must require Deviation Review section"

    def test_verifier_no_code_modification_guardrail(self):
        content = (AGENTS_DIR / "verifier.md").read_text()
        assert "MUST NOT" in content, \
            "verifier.md must have MUST NOT guardrail"
        assert any(phrase in content for phrase in [
            "MUST NOT modify any source code",
            "MUST NOT** modify any source code",
        ]), "verifier must explicitly forbid modifying source code files"

    def test_verifier_evidence_requirement(self):
        content = (AGENTS_DIR / "verifier.md").read_text()
        assert "evidence" in content.lower(), \
            "verifier.md must require evidence for requirements coverage"
