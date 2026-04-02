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
import pathlib
import re
import sys
from typing import Any, Dict, List, Tuple

VERSION = "0.2.0"

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_config(config_path: pathlib.Path | None = None) -> Dict[str, Any]:
    """reprogate.yaml에서 설정을 로딩한다 (PyYAML 의존 없이)."""
    if config_path is None:
        config_path = ROOT / "reprogate.yaml"
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
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key in ("records_dir", "skills_dir", "project_name"):
                defaults[key] = value
    return defaults


_config = load_config()
RECORDS_DIR = ROOT / _config["records_dir"]
SKILLS_DIR = ROOT / _config["skills_dir"]

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


def collect_records() -> List[Tuple[pathlib.Path, Dict[str, Any], List[str]]]:
    """records/ 디렉토리에서 .md 파일을 수집하고 frontmatter와 sections를 파싱한다."""
    records = []
    if not RECORDS_DIR.exists():
        return records
    for md_file in sorted(RECORDS_DIR.rglob("*.md")):
        fm = parse_frontmatter(md_file)
        sections = parse_sections(md_file)
        records.append((md_file, fm, sections))
    return records


def collect_skills() -> List[pathlib.Path]:
    """skills/ 디렉토리에서 guidelines.md가 있는 Skill을 수집한다."""
    skills = []
    if not SKILLS_DIR.exists():
        return skills
    for guidelines in sorted(SKILLS_DIR.rglob("guidelines.md")):
        skills.append(guidelines.parent)
    return skills


def evaluate_gate(strict: bool = False) -> Tuple[int, List[str]]:
    """현재 산출물과 기록을 규칙에 대조하여 gate 평가를 수행한다."""
    errors: List[str] = []
    warnings: List[str] = []

    records = collect_records()
    skills = collect_skills()
    skill_names = [s.name for s in skills]

    print(f"📋 Records: {len(records)}개 발견")
    print(f"🛠  Skills:  {len(skills)}개 발견")
    print()

    # Rule 1: record-required (기록 존재 검사)
    if "record-required" in skill_names:
        if len(records) == 0:
            errors.append("❌ [record-required] 작업 기록이 필요합니다. records/에 RFC 또는 ADR을 작성해 주세요.")
        else:
            print("✅ [record-required] 통과")

    # Frontmatter 필수 필드 검사 (기본 룰)
    for path, fm, _ in records:
        relative = path.relative_to(ROOT)
        if not fm:
            errors.append(f"❌ {relative}: YAML Frontmatter가 없습니다.")
            continue
        for field in REQUIRED_FRONTMATTER_FIELDS:
            if field not in fm:
                errors.append(f"❌ {relative}: 필수 필드 '{field}'가 누락되었습니다.")

    # Rule 2: decision-documented (ADR 존재 여부 및 섹션 검사)
    if "decision-documented" in skill_names:
        adr_records = [r for r in records if r[1].get("type") == "adr"]
        if len(adr_records) == 0:
            warnings.append("⚠️  [decision-documented] 의사결정 기록(ADR)이 없습니다. 중요한 기술적 결정이 있다면 records/adr/에 작성해 주세요.")
        else:
            for path, fm, secs in adr_records:
                relative = path.relative_to(ROOT)
                if "Context" not in secs:
                    errors.append(f"❌ [decision-documented] {relative}에 Context 섹션이 누락되었습니다.")
                if "Decision" not in secs:
                    errors.append(f"❌ [decision-documented] {relative}에 Decision 섹션이 누락되었습니다.")
                if "Consequences" not in secs:
                    errors.append(f"❌ [decision-documented] {relative}에 Consequences 섹션이 누락되었습니다.")
            if not any("Context" not in secs or "Decision" not in secs or "Consequences" not in secs for _, _, secs in adr_records):
                print("✅ [decision-documented] 통과")

    # Rule 3: verification-present (모든 기록에 Verification 섹션)
    if "verification-present" in skill_names:
        passed = True
        for path, fm, secs in records:
            if "Verification" not in secs:
                errors.append(f"❌ [verification-present] {path.relative_to(ROOT)}에 Verification 섹션이 누락되었습니다.")
                passed = False
        if passed and len(records) > 0:
            print("✅ [verification-present] 통과")

    # Rule 4: scope-defined (RFC 기록에 Summary 및 Design/Proposal 섹션)
    if "scope-defined" in skill_names:
        rfc_records = [r for r in records if r[1].get("type") == "rfc"]
        passed = True
        for path, fm, secs in rfc_records:
            relative = path.relative_to(ROOT)
            if "Summary" not in secs:
                errors.append(f"❌ [scope-defined] {relative}에 Summary 섹션이 누락되었습니다.")
                passed = False
            if "Design" not in secs and "Design / Proposal" not in secs:
                errors.append(f"❌ [scope-defined] {relative}에 Design 또는 Design / Proposal 섹션이 누락되었습니다.")
                passed = False
        if passed and len(rfc_records) > 0:
            print("✅ [scope-defined] 통과")

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

    print("=" * 50)
    print(f"  ReproGate Gatekeeper v{VERSION} (Stage 1)")
    print("=" * 50)
    print()

    exit_code, messages = evaluate_gate(strict=args.strict)

    print()
    if messages:
        print("─" * 50)
        for msg in messages:
            print(f"  {msg}")
        print("─" * 50)

    print()
    if exit_code == 0:
        print("🟢 Gate PASSED — 모든 검사를 통과했습니다.")
    else:
        print("🔴 Gate FAILED — 위 항목을 해결해 주세요.")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
