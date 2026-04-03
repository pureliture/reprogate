#!/usr/bin/env python3
"""Tests for INIT-04: record_triggers path-pattern gating in gatekeeper.py."""
import pathlib
import sys
from typing import Any, Dict, List
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import gatekeeper


# --- matches_trigger tests ---

def test_trigger_pattern_match_scripts():
    """matches_trigger must return True for scripts/foo.py against scripts/**."""
    assert gatekeeper.matches_trigger("scripts/foo.py", "scripts/**") is True


def test_trigger_pattern_match_scripts_nested():
    """matches_trigger must return True for nested paths under scripts/**."""
    assert gatekeeper.matches_trigger("scripts/sub/bar.py", "scripts/**") is True


def test_trigger_pattern_no_match_readme():
    """matches_trigger must return False for README.md against scripts/**."""
    assert gatekeeper.matches_trigger("README.md", "scripts/**") is False


def test_trigger_pattern_match_skills():
    """matches_trigger must return True for skills/** paths."""
    assert gatekeeper.matches_trigger("skills/foo/rules.rego", "skills/**") is True


def test_trigger_pattern_no_match_docs():
    """matches_trigger must return False for docs/ paths against skills/**."""
    assert gatekeeper.matches_trigger("docs/foo.md", "skills/**") is False


# --- is_record_required tests ---

def _config_with_triggers() -> Dict[str, Any]:
    return {
        "record_triggers": [
            {"pattern": "scripts/**", "record_type": "adr", "reason": "Script changes"},
            {"pattern": "skills/**", "record_type": "adr", "reason": "Skill changes"},
        ]
    }


def test_is_record_required_triggers_on_match():
    """is_record_required must return True when a changed file matches a trigger."""
    config = _config_with_triggers()
    with patch.object(gatekeeper, "get_changed_files", return_value=["scripts/cli.py"]):
        assert gatekeeper.is_record_required(config) is True


def test_is_record_required_no_trigger_on_no_match():
    """is_record_required must return False when changed files don't match any trigger."""
    config = _config_with_triggers()
    with patch.object(gatekeeper, "get_changed_files", return_value=["README.md", "docs/foo.md"]):
        assert gatekeeper.is_record_required(config) is False


def test_is_record_required_empty_triggers():
    """is_record_required must return False when record_triggers is empty."""
    config = {"record_triggers": []}
    with patch.object(gatekeeper, "get_changed_files", return_value=["scripts/cli.py"]):
        assert gatekeeper.is_record_required(config) is False
