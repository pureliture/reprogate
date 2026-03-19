---
record_id: "ADR-007"
title: "uv Python toolchain adoption"
type: "adr"
status: "Accepted"
created_at: "2026-03-19"
tags: ["tooling", "python", "uv", "stage-1"]
---

# ADR-007: uv Python toolchain adoption

## Status
Accepted

## Context
Repository tooling scripts require Python with dependencies (PyYAML, requests). Previously, contributors needed to manually create venv, install pip packages, and activate environments. This caused:

- Inconsistent local vs CI environments
- Manual `pip install -r requirements.txt` steps
- No dependency lock guaranteeing reproducibility
- Friction for new contributors

## Decision
We will adopt `uv` as the standard Python execution method. All Python scripts should be invoked via `uv run python3 <script>`. Dependencies are declared in `pyproject.toml` and locked in `uv.lock`.

Key changes:
- Remove `requirements.txt` (replaced by `pyproject.toml`)
- Add `uv.lock` for reproducible dependency resolution
- Update CI workflows to use `uv run`
- Update `AGENTS.md` with new execution guidance

## Consequences
- Positive: Zero manual environment setup - `uv run` handles everything
- Positive: CI and local execution use identical method
- Positive: `uv.lock` guarantees reproducible builds
- Positive: Faster dependency resolution than pip
- Neutral: Contributors need `uv` installed (available via `brew install uv` or `pip install uv`)

## Verification
- [x] `uv run python3 scripts/validate_product_definition.py --help` works
- [x] `uv.lock` generated with all dependencies
- [x] CI workflow updated to use `uv run`
