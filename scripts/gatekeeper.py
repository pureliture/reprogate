#!/usr/bin/env python3
"""
ReproGate Gatekeeper v1.0.0

Evaluates repository records against skill policies using OPA/Rego (ADR-002).
Falls back to structural checks when OPA is not installed (degraded mode).

- Loads config from reprogate.yaml using PyYAML
- Collects records from records/ directory
- Delegates evaluation to OPA wrapper (opa_wrapper.py)
- Enforces fail-closed behavior per D-08
- Filters skills by active_skills config
"""
import argparse
import pathlib
import re
import sys
from typing import Any, Dict, List, Tuple

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from opa_wrapper import (
    SkillResult,
    build_input_data,
    evaluate_skill_opa,
    evaluate_skill_structural,
    is_opa_available,
)

VERSION = "1.0.0"

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_config(config_path: pathlib.Path | None = None) -> Dict[str, Any]:
    """Load configuration from reprogate.yaml using PyYAML.

    Args:
        config_path: Optional path to config file. Defaults to ROOT / reprogate.yaml.

    Returns:
        Configuration dict with records_dir, skills_dir, active_skills, gatekeeper keys.
    """
    path = config_path or (ROOT / "reprogate.yaml")
    defaults: Dict[str, Any] = {
        "records_dir": "records",
        "skills_dir": "skills",
        "active_skills": [],
        "gatekeeper": {"engine": "opa", "strict_mode": True, "fail_closed": True},
    }
    if not path.exists():
        return defaults
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    for key, default in defaults.items():
        if key not in data:
            data[key] = default
    return data


_config = load_config()
RECORDS_DIR = ROOT / _config["records_dir"]
SKILLS_DIR = ROOT / _config["skills_dir"]

REQUIRED_FRONTMATTER_FIELDS = ["record_id", "type", "status"]


def parse_frontmatter(path: pathlib.Path) -> Dict[str, Any]:
    """Parse YAML frontmatter from a Markdown file (simple regex-based)."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    frontmatter: Dict[str, Any] = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            # Handle YAML lists like [tag1, tag2]
            if value.startswith("[") and value.endswith("]"):
                value = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",")]
            frontmatter[key] = value
    return frontmatter


def parse_sections(path: pathlib.Path) -> List[str]:
    """Parse section headers (## etc.) from a Markdown file."""
    text = path.read_text(encoding="utf-8")
    sections = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#"):
            header = re.sub(r"^#+\s*", "", line)
            sections.append(header)
    return sections


def collect_records() -> List[Tuple[pathlib.Path, Dict[str, Any], List[str]]]:
    """Collect .md files from records/ directory with frontmatter and sections."""
    records = []
    if not RECORDS_DIR.exists():
        return records
    for md_file in sorted(RECORDS_DIR.rglob("*.md")):
        fm = parse_frontmatter(md_file)
        sections = parse_sections(md_file)
        records.append((md_file, fm, sections))
    return records


def collect_skills() -> List[pathlib.Path]:
    """Collect skill directories that contain guidelines.md."""
    skills = []
    if not SKILLS_DIR.exists():
        return skills
    for guidelines in sorted(SKILLS_DIR.rglob("guidelines.md")):
        skills.append(guidelines.parent)
    return skills


def evaluate_gate(
    config: Dict[str, Any] | None = None,
    strict: bool = False,
) -> Tuple[int, List[str]]:
    """Evaluate repository records against skill policies.

    Delegates to OPA wrapper for Rego evaluation (or structural fallback).
    Per D-08: fails closed when required evidence is missing.
    Per D-05: gate authority comes from OPA evaluating .rego files.

    Args:
        config: Configuration dict. If None, loads from reprogate.yaml.
        strict: If True, treat warnings as errors (overrides config strict_mode).

    Returns:
        Tuple of (exit_code, list_of_messages). exit_code 0 = pass, 1 = fail.
    """
    if config is None:
        config = load_config()

    records = collect_records()
    skills = collect_skills()
    active = config.get("active_skills", [])
    gate_cfg = config.get("gatekeeper", {})
    strict_mode = strict or gate_cfg.get("strict_mode", True)
    fail_closed = gate_cfg.get("fail_closed", True)

    # Determine evaluation mode
    opa_available = is_opa_available()
    evaluate_fn = evaluate_skill_opa if opa_available else evaluate_skill_structural

    print(f"Records: {len(records)} found")
    print(f"Skills: {len(skills)} found")
    print(f"Mode: {'OPA' if opa_available else 'Structural (degraded)'}")
    print()

    # Fail-closed: no skills and fail_closed -> fail
    if not skills and fail_closed:
        return 1, ["FAIL-CLOSED: No skills found but fail_closed=true"]

    input_data = build_input_data(records, ROOT)
    all_messages: List[str] = []
    has_deny = False

    for skill_dir in skills:
        if active and skill_dir.name not in active:
            continue
        result: SkillResult = evaluate_fn(skill_dir, input_data)
        if result.deny:
            has_deny = True
            for msg in result.deny:
                all_messages.append(f"DENY [{result.skill_id}]: {msg}")
            print(f"FAIL [{result.skill_id}]")
        elif result.warn:
            for msg in result.warn:
                all_messages.append(f"WARN [{result.skill_id}]: {msg}")
            if strict_mode:
                has_deny = True
                print(f"FAIL [{result.skill_id}] (strict mode)")
            else:
                print(f"WARN [{result.skill_id}]")
        else:
            print(f"PASS [{result.skill_id}]")

    exit_code = 1 if has_deny else 0
    return exit_code, all_messages


def main() -> int:
    """CLI entry point for the gatekeeper."""
    parser = argparse.ArgumentParser(
        description="ReproGate Gatekeeper -- evaluates records against skill policies."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors.",
    )
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        default=None,
        help="Path to reprogate.yaml config file.",
    )
    args = parser.parse_args()

    print("=" * 50)
    print(f"  ReproGate Gatekeeper v{VERSION}")
    print("=" * 50)
    print()

    config = load_config(config_path=args.config)
    exit_code, messages = evaluate_gate(config=config, strict=args.strict)

    print()
    if messages:
        print("-" * 50)
        for msg in messages:
            print(f"  {msg}")
        print("-" * 50)

    print()
    if exit_code == 0:
        print("Gate PASSED")
    else:
        print("Gate FAILED")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
