#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PR_SECTIONS = [
    "## Change Type",
    "## Why",
    "## Linked Issue",
    "## Product Layer",
    "## Related Docs",
    "## Decision Record",
    "## Verification",
]

IMPLEMENTATION_PATH_PREFIXES = (
    "scripts/",
    "skills/",
    "templates/",
    ".github/workflows/",
)

DOC_OR_DECISION_PREFIXES = (
    "docs/spec/",
    "docs/strategy/",
    "docs/design/",
    "records/adr/",
    "records/rfc/",
)


def read_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def contains_any_prefix(paths: list[str], prefixes: tuple[str, ...]) -> bool:
    return any(path.startswith(prefixes) for path in paths)


def validate_pr_body(pr_body: str, errors: list[str]) -> None:
    for section in REQUIRED_PR_SECTIONS:
        if section not in pr_body:
            errors.append(f"PR body missing required section: {section}")

    weak_markers = ["TBD", "todo", "N/A", "n/a", "없음"]
    if "## Related Docs" in pr_body:
        related_docs_block = pr_body.split("## Related Docs", 1)[1].split("##", 1)[0].strip()
        if not related_docs_block or any(marker in related_docs_block for marker in weak_markers):
            errors.append("PR body has weak or empty Related Docs section.")

    if "## Verification" in pr_body:
        verification_block = pr_body.split("## Verification", 1)[1].split("##", 1)[0].strip()
        if not verification_block or any(marker in verification_block for marker in weak_markers):
            errors.append("PR body has weak or empty Verification section.")


def validate_changed_files(changed_files: list[str], errors: list[str]) -> None:
    changed = set(changed_files)

    if "docs/strategy/final-definition.md" in changed:
        required = {
            "docs/strategy/vision.md",
            "docs/strategy/roadmap.md",
            "docs/strategy/product-boundary.md",
        }
        missing = sorted(required - changed)
        if missing:
            errors.append(
                "final-definition.md changed, but related strategy docs were not updated: "
                + ", ".join(missing)
            )

    if "docs/strategy/product-boundary.md" in changed and "docs/strategy/scenarios.md" not in changed:
        errors.append(
            "product-boundary.md changed, but scenarios.md was not updated in the same PR."
        )

    if contains_any_prefix(changed_files, IMPLEMENTATION_PATH_PREFIXES):
        if not contains_any_prefix(changed_files, DOC_OR_DECISION_PREFIXES):
            errors.append(
                "Implementation-layer files changed without related spec/strategy/design/ADR/RFC changes."
            )


def validate_scenarios_file(repo_root: Path, changed_files: list[str], errors: list[str]) -> None:
    if "docs/strategy/scenarios.md" not in changed_files:
        return

    scenarios_path = repo_root / "docs" / "strategy" / "scenarios.md"
    if not scenarios_path.exists():
        errors.append("scenarios.md is marked as changed but file is missing.")
        return

    text = scenarios_path.read_text(encoding="utf-8")
    ids = re.findall(r"^###\s+(SC-\d+\.\d+):", text, flags=re.MULTILINE)

    if not ids:
        errors.append("scenarios.md changed, but no scenario IDs matching `SC-x.y` were found.")
        return

    duplicates = sorted({sid for sid in ids if ids.count(sid) > 1})
    if duplicates:
        errors.append("Duplicate scenario IDs found: " + ", ".join(duplicates))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ReproGate product-definition workflow.")
    parser.add_argument("--changed-file-list", required=True)
    parser.add_argument("--pr-body-file", required=True)
    args = parser.parse_args()

    repo_root = Path.cwd()
    changed_files = read_lines(Path(args.changed_file_list))
    pr_body = Path(args.pr_body_file).read_text(encoding="utf-8")

    errors: list[str] = []

    validate_pr_body(pr_body, errors)
    validate_changed_files(changed_files, errors)
    validate_scenarios_file(repo_root, changed_files, errors)

    if errors:
        print("🔴 product-definition-ci FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("🟢 product-definition-ci PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
