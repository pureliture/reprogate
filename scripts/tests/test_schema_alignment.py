#!/usr/bin/env python3
"""Tests for INIT-05: canonical schema alignment between generate.py, gatekeeper.py, and reprogate.yaml.j2."""
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import generate
import gatekeeper

ROOT = pathlib.Path(__file__).resolve().parents[2]
TEMPLATE_PATH = ROOT / "templates" / "reprogate.yaml.j2"


def test_generate_load_config_has_canonical_fields(tmp_path):
    """generate.load_config() must return all canonical schema fields."""
    cfg_file = tmp_path / "reprogate.yaml"
    cfg_file.write_text("project_name: TestProject\n", encoding="utf-8")
    cfg = generate.load_config(cfg_file)
    required_keys = [
        "project", "workspaces", "processes", "tools", "records",
        "records_dir", "skills_dir", "active_skills", "gatekeeper",
        "reprogate_version", "record_types", "record_triggers",
    ]
    for key in required_keys:
        assert key in cfg, f"Missing key in generate.load_config(): {key}"


def test_generate_load_config_record_triggers_default(tmp_path):
    """generate.load_config() must default record_triggers to empty list."""
    cfg_file = tmp_path / "reprogate.yaml"
    cfg_file.write_text("project_name: TestProject\n", encoding="utf-8")
    cfg = generate.load_config(cfg_file)
    assert cfg["record_triggers"] == [], (
        f"Expected record_triggers==[], got {cfg['record_triggers']!r}"
    )


def test_gatekeeper_load_config_has_record_triggers(tmp_path):
    """gatekeeper.load_config() must include record_triggers in defaults."""
    cfg_file = tmp_path / "reprogate.yaml"
    cfg_file.write_text("project_name: TestProject\n", encoding="utf-8")
    cfg = gatekeeper.load_config(cfg_file)
    assert "record_triggers" in cfg, "gatekeeper.load_config() missing record_triggers key"
    assert cfg["record_triggers"] == [], (
        f"Expected record_triggers==[], got {cfg['record_triggers']!r}"
    )


def test_init_template_has_all_sections():
    """templates/reprogate.yaml.j2 must contain all canonical schema sections."""
    text = TEMPLATE_PATH.read_text(encoding="utf-8")
    required_sections = ["project:", "workspaces:", "tools:", "records:", "record_triggers:"]
    for section in required_sections:
        assert section in text, f"Template missing section: {section}"
