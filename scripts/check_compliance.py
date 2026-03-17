#!/usr/bin/env python3
import argparse
import pathlib
import re
import subprocess
import sys
from typing import Any, Dict, Iterable, List, Set

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
CONSTITUTION = DOCS_DIR / "constitution.md"
OPERATING_MODEL = DOCS_DIR / "operating-model.md"
PROCESS_CATALOG = DOCS_DIR / "process-catalog" / "README.md"
CONFIG_FILE = ROOT / "dpc.config.yaml"
DEFAULT_CHANGELOG = DOCS_DIR / "CHANGELOG.md"
DEFAULT_WORK_PACKET_DIR = DOCS_DIR / "work-packets"
DEFAULT_ADR_DIR = DOCS_DIR / "adr"
LOCAL_RUNTIME_PREFIXES = (".claude/", ".codex/", ".omc/", ".omx/", ".dpc/")

VALID_STATUSES = {
    "DRAFT",
    "READY",
    "IN_ANALYSIS",
    "IN_REFINEMENT",
    "IN_TROUBLESHOOTING",
    "IN_DEVELOPMENT",
    "IN_REFACTORING",
    "IN_REVIEW",
    "IN_DOCUMENTATION",
    "IN_RECORDING",
    "BLOCKED",
    "ON_HOLD",
    "DONE",
    "CANCELLED",
}

REQUIRED_FRONTMATTER_FIELDS = [
    "packet_id",
    "title",
    "goal_ids",
    "status",
    "work_type",
    "priority",
    "target_environment",
    "start_process",
    "current_process",
    "next_process",
    "owner",
    "created_at",
    "last_updated",
]


def load_config(path: pathlib.Path) -> Dict[str, Any]:
    """Load YAML configuration using PyYAML.

    Returns a dictionary with default values for missing sections to maintain
    backward compatibility with existing code.
    """
    default_data: Dict[str, Any] = {
        "records": {},
    }

    if not path.exists():
        return default_data

    text = path.read_text(encoding="utf-8")
    loaded = yaml.safe_load(text)

    if loaded is None:
        return default_data

    # Ensure records section exists
    if "records" not in loaded:
        loaded["records"] = {}

    return loaded


CONFIG = load_config(CONFIG_FILE)
RECORDS = CONFIG.get("records", {}) if isinstance(CONFIG, dict) else {}
CHANGELOG = ROOT / str(RECORDS.get("changelog_path") or DEFAULT_CHANGELOG.relative_to(ROOT))
WORK_PACKET_DIR = ROOT / str(RECORDS.get("wp_path") or DEFAULT_WORK_PACKET_DIR.relative_to(ROOT))
ADR_DIR = ROOT / str(RECORDS.get("adr_path") or DEFAULT_ADR_DIR.relative_to(ROOT))


def run_git(args: List[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git command failed")
    return proc.stdout


def changed_files(mode: str) -> Set[str]:
    if mode == "none":
        return set()
    if mode == "staged":
        out = run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMRTUXB"])
    else:
        out = run_git(["diff", "--name-only", "HEAD"])
    return {line.strip() for line in out.splitlines() if line.strip()}


def get_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    if end == -1:
        return ""
    return text[4:end]


def load_goal_ids_from_constitution() -> Set[str]:
    if not CONSTITUTION.exists():
        return set()
    text = CONSTITUTION.read_text(encoding="utf-8")
    return set(re.findall(r"^###\s+(DPC-G\d+)\b", text, flags=re.MULTILINE))


def load_goal_ids_from_wp(path: pathlib.Path) -> Set[str]:
    text = path.read_text(encoding="utf-8")
    frontmatter = get_frontmatter(text)
    if not frontmatter:
        return set()
    return set(re.findall(r"\bDPC-G\d+\b", frontmatter))


def iter_wp_files() -> Iterable[pathlib.Path]:
    if not WORK_PACKET_DIR.exists():
        return []
    return sorted(WORK_PACKET_DIR.glob("WP-*.md"))


def validate_wp_fields(wp_path: pathlib.Path, errors: List[str]) -> None:
    try:
        text = wp_path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Cannot read work packet {wp_path}: {exc}")
        return

    frontmatter = get_frontmatter(text)
    if not frontmatter:
        errors.append(f"{wp_path.name}: YAML frontmatter is missing or malformed.")
        return

    for field in REQUIRED_FRONTMATTER_FIELDS:
        if not re.search(rf"^{re.escape(field)}\s*:", frontmatter, flags=re.MULTILINE):
            errors.append(f"{wp_path.name}: missing required frontmatter field '{field}'.")

    status_match = re.search(r'^status\s*:\s*["\']?(\w+)["\']?', frontmatter, flags=re.MULTILINE)
    if status_match:
        status_value = status_match.group(1).upper()
        if status_value not in VALID_STATUSES:
            errors.append(f"{wp_path.name}: invalid status '{status_value}'.")

    goal_ids_match = re.search(r"^goal_ids\s*:\s*(.+)$", frontmatter, flags=re.MULTILINE)
    if goal_ids_match and goal_ids_match.group(1).strip() in {"[]", "", '""', "''"}:
        errors.append(f"{wp_path.name}: 'goal_ids' must not be empty.")


def validate_static(errors: List[str]) -> None:
    required = [CONSTITUTION, OPERATING_MODEL, PROCESS_CATALOG]
    for path in required:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    goal_ids = load_goal_ids_from_constitution()
    for wp in iter_wp_files():
        validate_wp_fields(wp, errors)
        if not goal_ids:
            continue
        wp_goals = load_goal_ids_from_wp(wp)
        if not wp_goals:
            errors.append(f"{wp.relative_to(ROOT)} missing 'goal_ids' in frontmatter.")
            continue
        unknown = sorted(wp_goals - goal_ids)
        if unknown:
            errors.append(f"{wp.relative_to(ROOT)} uses undefined goal ids: {', '.join(unknown)}")


def validate_runtime_tracking(files: Set[str], errors: List[str]) -> None:
    for path in sorted(files):
        if path.startswith(LOCAL_RUNTIME_PREFIXES):
            errors.append(f"Local runtime directory must not be committed: {path}")


def validate_namespace(files: Set[str], errors: List[str]) -> None:
    wp_prefix = WORK_PACKET_DIR.relative_to(ROOT).as_posix().rstrip("/") + "/"
    adr_prefix = ADR_DIR.relative_to(ROOT).as_posix().rstrip("/") + "/"

    for path in sorted(files):
        name = pathlib.Path(path).name
        if path.startswith(wp_prefix) and path.endswith(".md"):
            if name == "index.md":
                continue
            if not name.startswith("WP-DPC-"):
                errors.append(f"{path}: dpc work packets must use the 'WP-DPC-' prefix.")
        if path.startswith(adr_prefix) and path.endswith(".md"):
            if not name.startswith("ADR-DPC-"):
                errors.append(f"{path}: dpc decision records must use the 'ADR-DPC-' prefix.")


def validate_change_sync(files: Set[str], errors: List[str]) -> None:
    docs_changes = {path for path in files if path.startswith("docs/")}
    if not docs_changes:
        return

    changelog_rel = CHANGELOG.relative_to(ROOT).as_posix()

    if CHANGELOG.exists() and changelog_rel not in files and any(
        path != changelog_rel for path in docs_changes
    ):
        errors.append(f"Documentation changes require updating {changelog_rel} when that file exists.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate portable dpc compliance.")
    parser.add_argument(
        "--mode",
        choices=["none", "staged", "working_tree"],
        default="none",
        help="Include git diff based checks for staged or working tree changes.",
    )
    parser.add_argument(
        "--wp-file",
        default=None,
        help="Validate a specific work packet file.",
    )
    args = parser.parse_args()

    errors: List[str] = []
    try:
        validate_static(errors)
        files = changed_files(args.mode)
        if files:
            validate_runtime_tracking(files, errors)
            validate_namespace(files, errors)
            validate_change_sync(files, errors)
        if args.wp_file:
            wp_path = pathlib.Path(args.wp_file)
            if not wp_path.is_absolute():
                wp_path = ROOT / wp_path
            validate_wp_fields(wp_path, errors)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Compliance checker runtime error: {exc}")

    if errors:
        print("dpc compliance check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("dpc compliance check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
