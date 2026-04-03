#!/usr/bin/env python3
"""
OPA Wrapper for ReproGate Gatekeeper.

Provides OPA binary integration for Rego policy evaluation per ADR-002,
with a structural fallback for environments without OPA installed.

Per ADR-002: OPA is the rules engine. The structural fallback is explicitly
NOT a Rego interpreter -- it performs basic structural checks only.
Per D-08: Fail closed on errors -- OPA failures produce deny, not silent pass.
"""
import json
import pathlib
import re
import subprocess
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"


@dataclass
class SkillResult:
    """Result of evaluating a single skill's rules."""

    skill_id: str
    deny: List[str] = field(default_factory=list)
    warn: List[str] = field(default_factory=list)
    mode: str = "opa"  # "opa" or "structural"


def is_opa_available() -> bool:
    """Check whether the OPA binary is installed and accessible.

    Returns True if ``opa version`` exits with code 0, False otherwise.
    """
    try:
        result = subprocess.run(
            ["opa", "version"],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _parse_skill_id(skill_dir: pathlib.Path) -> str:
    """Read skill_id from guidelines.md frontmatter."""
    guidelines_path = skill_dir / "guidelines.md"
    if not guidelines_path.exists():
        return skill_dir.name

    text = guidelines_path.read_text(encoding="utf-8")
    match = re.search(r'skill_id:\s*["\']?([^"\'\n]+)["\']?', text)
    if match:
        return match.group(1).strip()
    return skill_dir.name


def build_input_data(
    records: List[Tuple[pathlib.Path, Dict[str, Any], List[str]]],
    root: pathlib.Path,
) -> Dict[str, Any]:
    """Convert gatekeeper's collect_records() output to the OPA input JSON contract.

    Args:
        records: List of (path, frontmatter_dict, section_names_list) tuples.
        root: Project root path for computing relative paths.

    Returns:
        Dict matching the OPA input JSON contract.
    """
    return {
        "records": [
            {
                "path": str(path.relative_to(root)),
                "frontmatter": frontmatter_dict,
                "sections": {name: True for name in sections_list},
            }
            for path, frontmatter_dict, sections_list in records
        ]
    }


def evaluate_skill_opa(skill_dir: pathlib.Path, input_data: Dict[str, Any]) -> SkillResult:
    """Evaluate a skill's Rego rules using the OPA binary.

    Shells out to ``opa eval`` per the ADR-002 pattern. If OPA exits non-zero
    or output cannot be parsed, the result is treated as a deny (fail-closed
    per D-08).

    Args:
        skill_dir: Path to the skill directory containing rules.rego and guidelines.md.
        input_data: The OPA input JSON data (from build_input_data).

    Returns:
        SkillResult with deny/warn messages and mode="opa".
    """
    skill_id = _parse_skill_id(skill_dir)
    rego_path = skill_dir / "rules.rego"

    if not rego_path.exists():
        return SkillResult(
            skill_id=skill_id,
            deny=[f"rules.rego not found in skill '{skill_id}'"],
            mode="opa",
        )

    deny_msgs: List[str] = []
    warn_msgs: List[str] = []
    input_json = json.dumps(input_data)

    # Evaluate deny rules
    try:
        deny_cmd = [
            "opa", "eval",
            "--data", str(rego_path),
            "--stdin-input",
            "--format", "json",
            "data.reprogate.rules.deny",
        ]
        deny_result = subprocess.run(
            deny_cmd,
            input=input_json,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if deny_result.returncode != 0:
            return SkillResult(
                skill_id=skill_id,
                deny=[f"OPA eval failed for '{skill_id}': {deny_result.stderr.strip()}"],
                mode="opa",
            )
        deny_output = json.loads(deny_result.stdout)
        deny_values = deny_output.get("result", [{}])[0].get("expressions", [{}])[0].get("value", [])
        if isinstance(deny_values, list):
            deny_msgs.extend(deny_values)
        elif isinstance(deny_values, set):
            deny_msgs.extend(sorted(deny_values))
    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError, IndexError) as exc:
        return SkillResult(
            skill_id=skill_id,
            deny=[f"OPA eval error for '{skill_id}': {exc}"],
            mode="opa",
        )

    # Evaluate warn rules
    try:
        warn_cmd = [
            "opa", "eval",
            "--data", str(rego_path),
            "--stdin-input",
            "--format", "json",
            "data.reprogate.rules.warn",
        ]
        warn_result = subprocess.run(
            warn_cmd,
            input=input_json,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if warn_result.returncode == 0:
            warn_output = json.loads(warn_result.stdout)
            warn_values = warn_output.get("result", [{}])[0].get("expressions", [{}])[0].get("value", [])
            if isinstance(warn_values, list):
                warn_msgs.extend(warn_values)
            elif isinstance(warn_values, set):
                warn_msgs.extend(sorted(warn_values))
    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError, IndexError):
        # Warn evaluation failure is not critical -- deny still applies
        pass

    return SkillResult(skill_id=skill_id, deny=deny_msgs, warn=warn_msgs, mode="opa")


def evaluate_skill_structural(skill_dir: pathlib.Path, input_data: Dict[str, Any]) -> SkillResult:
    """Evaluate a skill using basic structural checks (degraded mode).

    This is the fallback when OPA is not installed. It performs a SUBSET of
    what OPA would catch -- checking record presence, frontmatter fields,
    and Verification sections -- WITHOUT attempting to parse Rego syntax.

    Args:
        skill_dir: Path to the skill directory containing guidelines.md.
        input_data: The OPA input JSON data (from build_input_data).

    Returns:
        SkillResult with deny/warn messages and mode="structural".
    """
    skill_id = _parse_skill_id(skill_dir)
    deny_msgs: List[str] = []
    warn_msgs: List[str] = []

    records = input_data.get("records", [])

    # Check if records list is empty
    if len(records) == 0:
        deny_msgs.append("No records found. Add records to records/ directory.")
    else:
        for record in records:
            path = record.get("path", "<unknown>")
            frontmatter = record.get("frontmatter", {})
            sections = record.get("sections", {})

            # Check frontmatter has record_id and status
            if "record_id" not in frontmatter:
                deny_msgs.append(
                    f"Record '{path}' is missing required frontmatter field 'record_id'."
                )
            if "status" not in frontmatter:
                deny_msgs.append(
                    f"Record '{path}' is missing required frontmatter field 'status'."
                )

            # Check for Verification section
            if "Verification" not in sections:
                deny_msgs.append(
                    f"Record '{path}' is missing required 'Verification' section."
                )

    # Always warn that OPA is not available in structural mode
    warn_msgs.append(
        "OPA is not installed. Running in degraded structural-check mode. "
        "Install OPA for full Rego policy evaluation. "
        "See: https://www.openpolicyagent.org/docs/latest/#running-opa"
    )

    return SkillResult(skill_id=skill_id, deny=deny_msgs, warn=warn_msgs, mode="structural")
