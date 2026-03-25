#!/usr/bin/env python3
"""Tests for scripts/cli.py — ReproGate CLI branding and routing."""
import subprocess
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from cli import parse_args  # noqa: E402


CLI_PATH = pathlib.Path(__file__).resolve().parents[1] / "cli.py"


class TestCliBranding:
    def test_help_shows_reprogate(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--help"],
            capture_output=True, text=True,
        )
        assert "ReproGate" in result.stdout

    def test_help_no_dpc(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--help"],
            capture_output=True, text=True,
        )
        assert "dpc" not in result.stdout.lower()


class TestCliCommands:
    def test_create_command_accepted(self) -> None:
        args = parse_args(["create"])
        assert args.command == "create"

    def test_check_routes_to_gatekeeper(self) -> None:
        source = CLI_PATH.read_text(encoding="utf-8")
        assert "gatekeeper.py" in source
        assert "check_compliance.py" not in source

    def test_all_commands_accepted(self) -> None:
        for cmd in ["init", "generate", "check", "create", "search",
                     "search-content", "print"]:
            args = parse_args([cmd])
            assert args.command == cmd

    def test_gate_alias_accepted(self) -> None:
        args = parse_args(["gate"])
        assert args.command == "gate"
