#!/usr/bin/env python3
"""Tests for INIT-06: template identity text updated from compiler/gatekeeper to delivery harness."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
AGENTS_TEMPLATE = ROOT / "templates" / "AGENTS.md.j2"
CLAUDE_TEMPLATE = ROOT / "templates" / "claude" / "CLAUDE.md.j2"


def test_agents_md_no_compiler_gatekeeper():
    """AGENTS.md.j2 must not contain 'compiler/gatekeeper'."""
    text = AGENTS_TEMPLATE.read_text(encoding="utf-8")
    assert "compiler/gatekeeper" not in text, (
        "AGENTS.md.j2 still contains stale 'compiler/gatekeeper' identity"
    )


def test_agents_md_has_delivery_harness():
    """AGENTS.md.j2 must contain 'delivery harness'."""
    text = AGENTS_TEMPLATE.read_text(encoding="utf-8")
    assert "delivery harness" in text, (
        "AGENTS.md.j2 does not contain 'delivery harness' identity"
    )


def test_claude_md_no_compiler_gatekeeper():
    """CLAUDE.md.j2 must not contain 'compiler/gatekeeper'."""
    text = CLAUDE_TEMPLATE.read_text(encoding="utf-8")
    assert "compiler/gatekeeper" not in text, (
        "CLAUDE.md.j2 still contains stale 'compiler/gatekeeper' identity"
    )


def test_claude_md_has_delivery_harness():
    """CLAUDE.md.j2 must contain 'delivery harness'."""
    text = CLAUDE_TEMPLATE.read_text(encoding="utf-8")
    assert "delivery harness" in text, (
        "CLAUDE.md.j2 does not contain 'delivery harness' identity"
    )
