#!/usr/bin/env python3
"""
ReproGate Gatekeeper (Stage 1)
- reprogate.yaml에서 설정을 로딩하고
- records/ 디렉토리의 Work Record를 검사하고
- skills/ 디렉토리의 Rego 규칙과 대조하여
- 필수 산출물 누락 시 gate fail을 반환한다.

Stage 0: 파일 존재 검사만 수행
Stage 1: reprogate.yaml 로딩 + 섹션 레벨 검사 + Git Hook 연동
"""
import argparse
import fnmatch
import pathlib
import re
import subprocess
import sys
from typing import Any, Dict, List, Tuple

import yaml  # type: ignore[import]

from _config import merge_config_defaults

VERSION = "0.2.0"
DIVIDER_WIDTH = 50
REQUIRED_ADR_SECTIONS = ["Context", "Decision", "Consequences"]

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Module-level defaults — no I/O at import time.
# evaluate_gate() overrides these from config; tests may monkeypatch them.
RECORDS_DIR = ROOT / "records"
SKILLS_DIR = ROOT / "skills"


def load_config(config_path: pathlib.Path | None = None) -> Dict[str, Any]:
    """reprogate.yaml에서 설정을 로딩한다 (PyYAML 사용)."""
    config_path = config_path or (ROOT / "reprogate.yaml")
    defaults: Dict[str, Any] = {
        "records_dir": "records",
        "skills_dir": "skills",
        "active_skills": [],
        "gatekeeper": {"engine": "opa", "strict_mode": True, "fail_closed": True},
        "record_triggers": [],
    }
    if not config_path.exists():
        return defaults
    text = config_path.read_text(encoding="utf-8")
    loaded = yaml.safe_load(text) or {}
    merge_config_defaults(loaded, defaults)
    return loaded


REQUIRED_FRONTMATTER_FIELDS = ["record_id", "type", "status"]


def parse_frontmatter(path: pathlib.Path) -> Dict[str, Any]:
    """YAML frontmatter를 간단히 파싱한다 (PyYAML 의존 없이)."""
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
    """Markdown 파일의 Section 헤더(## 등)를 파싱한다."""
    text = path.read_text(encoding="utf-8")
    sections = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#"):
            # '## Header' -> 'Header'
            header = re.sub(r"^#+\s*", "", line)
            sections.append(header)
    return sections


def collect_records(records_dir: pathlib.Path) -> List[Tuple[pathlib.Path, Dict[str, Any], List[str]]]:
    """records/ 디렉토리에서 .md 파일을 수집하고 frontmatter와 sections를 파싱한다."""
    records = []
    if not records_dir.exists():
        return records
    for md_file in sorted(records_dir.rglob("*.md")):
        fm = parse_frontmatter(md_file)
        sections = parse_sections(md_file)
        records.append((md_file, fm, sections))
    return records


def collect_skills(skills_dir: pathlib.Path) -> List[pathlib.Path]:
    """skills/ 디렉토리에서 guidelines.md가 있는 Skill을 수집한다."""
    skills = []
    if not skills_dir.exists():
        return skills
    for guidelines in sorted(skills_dir.rglob("guidelines.md")):
        skills.append(guidelines.parent)
    return skills


def get_changed_files() -> List[str]:
    """Return list of staged file paths from git diff --cached --name-only.

    Returns empty list if git is unavailable or not in a repo.
    Uses --cached (staged) rather than HEAD so pre-commit hooks see correct scope.
    """
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [f.strip() for f in result.stdout.splitlines() if f.strip()]


def matches_trigger(filepath: str, pattern: str) -> bool:
    """Return True if filepath matches the given glob pattern.

    Uses fnmatch for Python 3.10/3.11 compatibility (pathlib.match() does not
    support ** cross-directory matching before Python 3.12).

    Examples:
        matches_trigger("scripts/foo.py", "scripts/**")  -> True
        matches_trigger("scripts/sub/bar.py", "scripts/**")  -> True
        matches_trigger("README.md", "scripts/**")  -> False
    """
    normalized = filepath.replace("\\", "/")
    if "**" in pattern:
        # Split on ** and check that filepath starts with the prefix segment
        prefix = pattern.split("**")[0].rstrip("/")
        return normalized.startswith(prefix + "/") or normalized == prefix
    return fnmatch.fnmatch(normalized, pattern)


def is_record_required(config: Dict[str, Any]) -> bool:
    """Return True if the current staged commit touches any record-trigger paths.

    Reads record_triggers from config. If no triggers are defined, returns False
    (no-trigger == no record required). If triggers are defined, checks staged
    files against each pattern using matches_trigger().

    Used by evaluate_gate() to scope enforcement to commits that actually
    warrant a decision record.
    """
    triggers = config.get("record_triggers", [])
    if not triggers:
        return False
    changed = get_changed_files()
    for filepath in changed:
        for trigger in triggers:
            if matches_trigger(filepath, trigger["pattern"]):
                return True
    return False


RecordList = List[Tuple[pathlib.Path, Dict[str, Any], List[str]]]


def _check_record_required(
    records: RecordList,
    skill_names: List[str],
    errors: List[str],
) -> None:
    """Rule 1: 기록 존재 검사."""
    if "record-required" not in skill_names:
        return
    if len(records) == 0:
        errors.append("❌ [record-required] 작업 기록이 필요합니다. records/에 RFC 또는 ADR을 작성해 주세요.")
    else:
        print("✅ [record-required] 통과")


def _check_frontmatter(records: RecordList, errors: List[str]) -> None:
    """Frontmatter 필수 필드 검사 (모든 레코드)."""
    for path, fm, _ in records:
        relative = path.relative_to(ROOT)
        if not fm:
            errors.append(f"❌ {relative}: YAML Frontmatter가 없습니다.")
            continue
        for field in REQUIRED_FRONTMATTER_FIELDS:
            if field not in fm:
                errors.append(f"❌ {relative}: 필수 필드 '{field}'가 누락되었습니다.")


def _check_decision_documented(
    records: RecordList,
    skill_names: List[str],
    errors: List[str],
    warnings: List[str],
) -> None:
    """Rule 2: ADR 존재 여부 및 섹션 검사."""
    if "decision-documented" not in skill_names:
        return
    adr_records = [r for r in records if r[1].get("type") == "adr"]
    if len(adr_records) == 0:
        warnings.append("⚠️  [decision-documented] 의사결정 기록(ADR)이 없습니다. 중요한 기술적 결정이 있다면 records/adr/에 작성해 주세요.")
        return
    for path, _, secs in adr_records:
        relative = path.relative_to(ROOT)
        for section in REQUIRED_ADR_SECTIONS:
            if section not in secs:
                errors.append(f"❌ [decision-documented] {relative}에 {section} 섹션이 누락되었습니다.")
    if all(
        all(section in secs for section in REQUIRED_ADR_SECTIONS)
        for _, _, secs in adr_records
    ):
        print("✅ [decision-documented] 통과")


def _check_verification_present(
    records: RecordList,
    skill_names: List[str],
    errors: List[str],
) -> None:
    """Rule 3: 모든 기록에 Verification 섹션."""
    if "verification-present" not in skill_names:
        return
    passed = True
    for path, _, secs in records:
        if "Verification" not in secs:
            errors.append(f"❌ [verification-present] {path.relative_to(ROOT)}에 Verification 섹션이 누락되었습니다.")
            passed = False
    if passed and len(records) > 0:
        print("✅ [verification-present] 통과")


def _check_scope_defined(
    records: RecordList,
    skill_names: List[str],
    errors: List[str],
) -> None:
    """Rule 4: RFC 기록에 Summary 및 Design/Proposal 섹션."""
    if "scope-defined" not in skill_names:
        return
    rfc_records = [r for r in records if r[1].get("type") == "rfc"]
    passed = True
    for path, _, secs in rfc_records:
        relative = path.relative_to(ROOT)
        if "Summary" not in secs:
            errors.append(f"❌ [scope-defined] {relative}에 Summary 섹션이 누락되었습니다.")
            passed = False
        if "Design" not in secs and "Design / Proposal" not in secs:
            errors.append(f"❌ [scope-defined] {relative}에 Design 또는 Design / Proposal 섹션이 누락되었습니다.")
            passed = False
    if passed and len(rfc_records) > 0:
        print("✅ [scope-defined] 통과")


def evaluate_gate(strict: bool = False, config: Dict[str, Any] | None = None) -> Tuple[int, List[str]]:
    """현재 산출물과 기록을 규칙에 대조하여 gate 평가를 수행한다."""
    errors: List[str] = []
    warnings: List[str] = []

    if config is None:
        config = load_config()

    records_dir = ROOT / config["records_dir"]
    skills_dir = ROOT / config["skills_dir"]

    # INIT-04: Check if any staged file triggers a record requirement.
    # If record_triggers are defined and no staged file matches, skip enforcement.
    triggers = config.get("record_triggers", [])
    if triggers and not is_record_required(config):
        print("No record-trigger paths in staged changes. Gate skipped.")
        return 0, []

    records = collect_records(records_dir)
    skills = collect_skills(skills_dir)
    skill_names = [s.name for s in skills]

    print(f"📋 Records: {len(records)}개 발견")
    print(f"🛠  Skills:  {len(skills)}개 발견")
    print()

    _check_record_required(records, skill_names, errors)
    _check_frontmatter(records, errors)
    _check_decision_documented(records, skill_names, errors, warnings)
    _check_verification_present(records, skill_names, errors)
    _check_scope_defined(records, skill_names, errors)

    return (1 if errors else 0), errors + warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ReproGate Gatekeeper — 작업 기록과 산출물을 검사합니다."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="기록이나 규칙이 없으면 실패 처리합니다.",
    )
    args = parser.parse_args()

    print("=" * DIVIDER_WIDTH)
    print(f"  ReproGate Gatekeeper v{VERSION} (Stage 1)")
    print("=" * DIVIDER_WIDTH)
    print()

    exit_code, messages = evaluate_gate(strict=args.strict)

    print()
    if messages:
        print("─" * DIVIDER_WIDTH)
        for msg in messages:
            print(f"  {msg}")
        print("─" * DIVIDER_WIDTH)

    print()
    if exit_code == 0:
        print("🟢 Gate PASSED — 모든 검사를 통과했습니다.")
    else:
        print("🔴 Gate FAILED — 위 항목을 해결해 주세요.")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
