# Deferred Items — Phase 01 Harness Bootstrap

## Out-of-Scope Pre-existing Test Failures

Discovered during execution of plan 01-01. These failures existed before plan 01-01 changes were applied (verified by stashing changes and confirming failures persisted).

### 1. test_yaml_parsing.py — ModuleNotFoundError: check_compliance

- **File:** `scripts/tests/test_yaml_parsing.py:18`
- **Error:** `from check_compliance import load_config as compliance_load_config`
- **Cause:** `scripts/check_compliance.py` module does not exist in this worktree. The test references a module that was likely renamed or removed.
- **Impact:** All tests in test_yaml_parsing.py fail to collect.
- **Suggested fix:** Either create `scripts/check_compliance.py` as a stub/alias for `gatekeeper.py`, or update `test_yaml_parsing.py` to import from `gatekeeper`.

### 2. test_bootstrap_smoke.py::TestBootstrapSmokeTest — AssertionError: check_compliance.py not found

- **File:** `scripts/tests/test_bootstrap_smoke.py:34`
- **Error:** `assert cls.check_script.exists()` — references `scripts/check_compliance.py`
- **Cause:** Same as above — `check_compliance.py` does not exist.
- **Impact:** 5 tests in TestBootstrapSmokeTest class fail.

### 3. test_bootstrap_smoke.py::TestBootstrapEdgeCases::test_init_with_custom_processes

- **File:** `scripts/tests/test_bootstrap_smoke.py:258`
- **Error:** `assertIn("TDD", content)` — `init.py` template does not include `{{ enabled_process_lines }}` placeholder in `processes.enabled`
- **Cause:** `templates/reprogate.yaml.j2` hardcodes `enabled: []` rather than using the `{{ enabled_process_lines }}` placeholder that `init.py::build_context()` provides.
- **Impact:** `--enabled-processes` flag to `init.py` has no effect on generated config.
- **Suggested fix:** Add `{{ enabled_process_lines }}` placeholder back to the template's `processes.enabled` section.

### 4. test_bootstrap_smoke.py::TestBootstrapEdgeCases::test_generate_with_disabled_claude_skips_claude_files

- **File:** `scripts/tests/test_bootstrap_smoke.py:312`
- **Error:** `CLAUDE.md should not be generated when Claude is disabled`
- **Cause:** Pre-existing logic issue in `generate.py` where `--disable-claude` flag (from init) doesn't propagate correctly.
- **Impact:** Claude adapter is always generated even when disabled.

*Deferred on: 2026-04-02 during plan 01-01 execution*
