#!/usr/bin/env python3
"""Tests for HOOK-01: REPROGATE_HOOK_PROFILE gating in reprogate_hook_base."""
import pathlib
import sys
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "hooks"))

from reprogate_hook_base import check_disabled, get_profile, VALID_PROFILES


def test_get_profile_default(monkeypatch):
    """get_profile() returns 'minimal' when REPROGATE_HOOK_PROFILE is unset."""
    monkeypatch.delenv("REPROGATE_HOOK_PROFILE", raising=False)
    assert get_profile() == "minimal"


def test_get_profile_minimal(monkeypatch):
    """get_profile() returns 'minimal' when REPROGATE_HOOK_PROFILE='minimal'."""
    monkeypatch.setenv("REPROGATE_HOOK_PROFILE", "minimal")
    assert get_profile() == "minimal"


def test_get_profile_standard(monkeypatch):
    """get_profile() returns 'standard' when REPROGATE_HOOK_PROFILE='standard'."""
    monkeypatch.setenv("REPROGATE_HOOK_PROFILE", "standard")
    assert get_profile() == "standard"


def test_get_profile_strict(monkeypatch):
    """get_profile() returns 'strict' when REPROGATE_HOOK_PROFILE='strict'."""
    monkeypatch.setenv("REPROGATE_HOOK_PROFILE", "strict")
    assert get_profile() == "strict"


def test_get_profile_invalid(monkeypatch):
    """get_profile() returns 'minimal' (default) when REPROGATE_HOOK_PROFILE has an invalid value."""
    monkeypatch.setenv("REPROGATE_HOOK_PROFILE", "turbo")
    assert get_profile() == "minimal"


def test_valid_profiles_constant():
    """VALID_PROFILES constant contains exactly {'minimal', 'standard', 'strict'}."""
    assert VALID_PROFILES == {"minimal", "standard", "strict"}


def test_check_disabled_regression(monkeypatch):
    """check_disabled() still exits 0 when REPROGATE_DISABLED=1 (no regression)."""
    monkeypatch.setenv("REPROGATE_DISABLED", "1")
    with pytest.raises(SystemExit) as exc_info:
        check_disabled()
    assert exc_info.value.code == 0, f"Expected exit(0), got exit({exc_info.value.code})"
