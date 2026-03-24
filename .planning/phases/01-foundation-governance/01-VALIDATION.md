---
phase: 1
slug: foundation-governance
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-25
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest scripts/tests/ -x -q` |
| **Full suite command** | `uv run pytest scripts/tests/ -v` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest scripts/tests/ -x -q`
- **After every plan wave:** Run `uv run pytest scripts/tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | CORE-01 | unit | `uv run pytest scripts/tests/test_init.py -v` | ❌ W0 | ⬜ pending |
| 01-02-01 | 02 | 1 | CORE-02 | unit | `uv run pytest scripts/tests/test_generate.py -v` | ✅ | ⬜ pending |
| 01-03-01 | 03 | 1 | CORE-03 | unit | `uv run pytest scripts/tests/test_gatekeeper.py -v` | ❌ W0 | ⬜ pending |
| 01-04-01 | 04 | 2 | CORE-04 | unit | `uv run pytest scripts/tests/test_cli.py -v` | ❌ W0 | ⬜ pending |
| 01-05-01 | 05 | 2 | CORE-05 | integration | `uv run pytest scripts/tests/test_yaml_parsing.py -v` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `scripts/tests/test_init.py` — stubs for CORE-01 (init command)
- [ ] `scripts/tests/test_gatekeeper.py` — stubs for CORE-03 (policy enforcement)
- [ ] `scripts/tests/test_cli.py` — stubs for CORE-04 (unified CLI)
- [ ] `scripts/tests/conftest.py` — shared fixtures (temp directories, sample configs)
- [ ] `pytest` added to dev dependencies in pyproject.toml

*Existing test files cover CORE-02 (generate) and CORE-05 (YAML parsing).*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Git hook blocks invalid commit | CORE-03 | Requires actual git commit attempt | 1. Stage a commit without required record 2. Run `git commit` 3. Verify hook rejects |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
