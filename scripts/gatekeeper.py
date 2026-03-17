#!/usr/bin/env python3
"""
ReproGate Gatekeeper
- records/ 디렉토리의 Work Record를 검사하고
- skills/ 디렉토리의 Rego 규칙과 대조하여
- 필수 산출물 누락 시 gate fail을 반환한다.

현재 Stage 0에서는 OPA 엔진 없이 Python으로 직접 검사한다.
Stage 1에서 OPA/Rego 엔진을 연동할 예정이다.
"""
import argparse
import pathlib
import re
import sys
from typing import Any, Dict, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parents[1]

# reprogate.yaml에서 읽어야 하지만, Stage 0에서는 하드코딩
RECORDS_DIR = ROOT / "records"
SKILLS_DIR = ROOT / "skills"

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


def collect_records() -> List[Tuple[pathlib.Path, Dict[str, Any]]]:
    """records/ 디렉토리에서 .md 파일을 수집하고 frontmatter를 파싱한다."""
    records = []
    if not RECORDS_DIR.exists():
        return records
    for md_file in sorted(RECORDS_DIR.rglob("*.md")):
        fm = parse_frontmatter(md_file)
        records.append((md_file, fm))
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

    print(f"📋 Records: {len(records)}개 발견")
    print(f"🛠  Skills:  {len(skills)}개 발견")
    print()

    # Gate 1: 기록 존재 검사
    if len(records) == 0:
        errors.append("❌ 작업 기록이 필요합니다. records/ 디렉토리에 RFC 또는 ADR을 작성해 주세요.")
    else:
        print("✅ 작업 기록이 존재합니다.")

    # Gate 2: Frontmatter 필수 필드 검사
    for path, fm in records:
        relative = path.relative_to(ROOT)
        if not fm:
            errors.append(f"❌ {relative}: YAML Frontmatter가 없습니다.")
            continue
        for field in REQUIRED_FRONTMATTER_FIELDS:
            if field not in fm:
                errors.append(f"❌ {relative}: 필수 필드 '{field}'가 누락되었습니다.")

    # Gate 3: Skill 존재 검사
    if len(skills) == 0:
        if strict:
            errors.append("❌ Skill이 없습니다. skills/ 디렉토리에 최소 1개의 Skill을 추가해 주세요.")
        else:
            warnings.append("⚠️  Skill이 없습니다. 규칙 없이 모든 것이 통과됩니다.")
    else:
        print(f"✅ {len(skills)}개 Skill이 활성화되었습니다.")

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
    print("  ReproGate Gatekeeper v0.1.0 (Stage 0)")
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
