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
    ".github/",
)

DOC_OR_DECISION_PREFIXES = (
    "docs/spec/",
    "docs/strategy/",
    "docs/design/",
    "docs/governance/",
    "records/adr/",
    "records/rfc/",
)

# Phase 1 SDD non-trivial path prefixes
SDD_NONTRIVIAL_PATH_PREFIXES = (
    "scripts/",
    "skills/",
    "templates/",
    ".github/",
)

# SDD routing options
SDD_ROUTING_OPTIONS = ("in-scope", "sdd-exempt", "reprogate-waiver")


def read_lines(path: Path) -> list[str]:
    return [line.rstrip("\n") for line in path.read_text(encoding="utf-8").splitlines()]


def contains_any_prefix(paths: list[str], prefixes: tuple[str, ...]) -> bool:
    return any(path.startswith(prefixes) for path in paths)


def extract_section(pr_body: str, heading: str) -> str:
    if heading not in pr_body:
        return ""
    return pr_body.split(heading, 1)[1].split("\n## ", 1)[0].strip()


def extract_markdown_paths(block: str) -> list[str]:
    paths: list[str] = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        candidate = line[2:].strip()
        if candidate.startswith(("docs/", "records/", ".specify/")):
            paths.append(candidate)
    return paths


def parse_sdd_routing(pr_body: str) -> str | None:
    """Parse SDD routing checkbox from PR body. Returns routing option or None."""
    routing_section = extract_section(pr_body, "### Routing")
    if not routing_section:
        return None

    for option in SDD_ROUTING_OPTIONS:
        # Match checked checkbox: - [x] option or - [X] option
        pattern = rf"-\s*\[x\]\s*{re.escape(option)}"
        if re.search(pattern, routing_section, re.IGNORECASE):
            return option
    return None


def extract_spec_artifact_paths(pr_body: str) -> dict[str, str]:
    """Extract spec artifact paths from PR body."""
    artifacts_section = extract_section(pr_body, "### Spec Artifacts")
    if not artifacts_section:
        return {}

    result: dict[str, str] = {}
    for line in artifacts_section.splitlines():
        line = line.strip()
        if line.startswith("- Spec:"):
            result["spec"] = line[7:].strip()
        elif line.startswith("- Plan:"):
            result["plan"] = line[7:].strip()
        elif line.startswith("- Tasks:"):
            result["tasks"] = line[8:].strip()
    return result


def extract_waiver_record_paths(pr_body: str) -> list[str]:
    """Extract waiver/deviation record paths from PR body."""
    waiver_section = extract_section(pr_body, "### Waiver/Deviation Record")
    if not waiver_section:
        return []

    paths: list[str] = []
    for line in waiver_section.splitlines():
        line = line.strip()
        if line.startswith("- ") and line[2:].strip().startswith("records/"):
            paths.append(line[2:].strip())
    return paths


def has_nontrivial_changes(changed_files: list[str]) -> bool:
    """Check if any changed files are non-trivial (require SDD routing)."""
    for path in changed_files:
        # .specify/ changes do not trigger SDD requirements
        if path.startswith(".specify/"):
            continue
        if path.startswith(SDD_NONTRIVIAL_PATH_PREFIXES):
            return True
    return False


def validate_sdd_workflow(
    repo_root: Path, pr_body: str, changed_files: list[str], warnings: list[str]
) -> None:
    """Validate SDD workflow routing, presence, and linkage (Phase 1 advisory mode)."""

    # Check if PR has non-trivial changes
    nontrivial = has_nontrivial_changes(changed_files)
    if not nontrivial:
        # No non-trivial changes, SDD validation not needed
        return

    # Parse routing
    routing = parse_sdd_routing(pr_body)

    if routing is None:
        warnings.append(
            "SDD Workflow: Non-trivial changes detected but no routing option selected. "
            "Please check one of: in-scope, sdd-exempt, reprogate-waiver."
        )
        return

    if routing == "sdd-exempt":
        # Exempt routing selected, no further checks
        return

    if routing == "in-scope":
        # Check spec artifact linkage
        artifacts = extract_spec_artifact_paths(pr_body)
        missing_artifacts: list[str] = []

        for key in ("spec", "plan", "tasks"):
            path = artifacts.get(key, "")
            if not path:
                missing_artifacts.append(key)
            elif not (repo_root / path).exists():
                warnings.append(
                    f"SDD Workflow: Spec artifact '{key}' path does not exist: {path}"
                )

        if missing_artifacts:
            warnings.append(
                f"SDD Workflow: in-scope routing selected but missing spec artifacts: "
                f"{', '.join(missing_artifacts)}. "
                "Please provide paths to .specify/specs/<feature>/spec.md, plan.md, tasks.md."
            )
        return

    if routing == "reprogate-waiver":
        # Check waiver record linkage
        waiver_paths = extract_waiver_record_paths(pr_body)

        if not waiver_paths:
            warnings.append(
                "SDD Workflow: reprogate-waiver routing selected but no records/* path provided. "
                "Please provide a records/* reference documenting the deviation."
            )
            return

        for path in waiver_paths:
            if not (repo_root / path).exists():
                warnings.append(
                    f"SDD Workflow: Waiver record path does not exist: {path}"
                )


def validate_pr_body(repo_root: Path, pr_body: str, errors: list[str]) -> None:
    for section in REQUIRED_PR_SECTIONS:
        if section not in pr_body:
            errors.append(f"PR body missing required section: {section}")

    weak_markers = ["TBD", "todo", "N/A", "n/a", "없음"]

    related_docs_block = extract_section(pr_body, "## Related Docs")
    decision_record_block = extract_section(pr_body, "## Decision Record")
    verification_block = extract_section(pr_body, "## Verification")

    def is_weak(block: str) -> bool:
        return not block or block.strip() == "-" or any(marker in block for marker in weak_markers)

    if is_weak(related_docs_block):
        errors.append("PR body has weak or empty Related Docs section.")

    if is_weak(decision_record_block):
        errors.append("PR body has weak or empty Decision Record section.")

    if is_weak(verification_block):
        errors.append("PR body has weak or empty Verification section.")

    related_paths = extract_markdown_paths(related_docs_block)
    if not related_paths:
        errors.append("Related Docs section does not contain repository paths.")
    else:
        missing_paths = [p for p in related_paths if not (repo_root / p).exists()]
        if missing_paths:
            errors.append(
                "Related Docs contains non-existent paths: " + ", ".join(sorted(missing_paths))
            )


def validate_changed_files(repo_root: Path, changed_files: list[str], pr_body: str, errors: list[str]) -> None:
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
                "Implementation/governance files changed without related spec/strategy/design/ADR/RFC changes."
            )

    related_docs_block = extract_section(pr_body, "## Related Docs")
    related_paths = extract_markdown_paths(related_docs_block)
    missing_from_repo = [p for p in related_paths if not (repo_root / p).exists()]
    if missing_from_repo:
        errors.append(
            "PR body references docs that are missing in repository state: "
            + ", ".join(sorted(missing_from_repo))
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
    changed_files = [line.strip() for line in read_lines(Path(args.changed_file_list)) if line.strip()]
    pr_body = Path(args.pr_body_file).read_text(encoding="utf-8")

    errors: list[str] = []
    warnings: list[str] = []

    validate_pr_body(repo_root, pr_body, errors)
    validate_changed_files(repo_root, changed_files, pr_body, errors)
    validate_scenarios_file(repo_root, changed_files, errors)

    # Phase 1 SDD validation (advisory mode - warnings only)
    validate_sdd_workflow(repo_root, pr_body, changed_files, warnings)

    if errors:
        print("🔴 product-definition-ci FAILED")
        for error in errors:
            print(f"- {error}")
        # Print warnings even on failure
        if warnings:
            print("\n🟡 SDD Workflow Warnings (Phase 1 - advisory):")
            for warning in warnings:
                print(f"  - {warning}")
        return 1

    # Print warnings (advisory mode - does not fail)
    if warnings:
        print("🟡 SDD Workflow Warnings (Phase 1 - advisory):")
        for warning in warnings:
            print(f"  - {warning}")
        print()

    print("🟢 product-definition-ci PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())