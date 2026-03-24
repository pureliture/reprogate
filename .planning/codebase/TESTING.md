# Testing Patterns

**Analysis Date:** 2026-03-24

## Test Framework

**Runner:**
- Python standard library `unittest`
- Config: Not detected. `pytest.ini`, `tox.ini`, and `.coveragerc` are absent, and `pyproject.toml` does not define test tool configuration.

**Assertion Library:**
- `unittest.TestCase` assertions, including `assertEqual`, `assertTrue`, `assertFalse`, `assertIn`, `assertIsNone`, and `assertIsInstance`, as used in `scripts/tests/test_tdd_gate.py`, `scripts/tests/test_bootstrap_smoke.py`, and `scripts/tests/test_yaml_parsing.py`.

**Run Commands:**
```bash
uv run python3 -m unittest discover -s scripts/tests -v   # Run all current Python tests
uv run python3 scripts/validate_product_definition.py --help   # Validate the CI-gated workflow script entry point
Not applicable                                              # Watch mode is not configured
Not applicable                                              # Coverage command is not configured
```

## Test File Organization

**Location:**
- Tests live in a dedicated directory under `scripts/tests/`, separate from implementation modules in `scripts/`.
- There are no co-located tests beside production modules.

**Naming:**
- Use `test_*.py` for Python test modules: `scripts/tests/test_bootstrap_smoke.py`, `scripts/tests/test_tdd_gate.py`, and `scripts/tests/test_yaml_parsing.py`.
- Use `Test*` class names and `test_*` method names inside those files.

**Structure:**
```text
scripts/
├── cli.py
├── generate.py
├── gatekeeper.py
├── hooks/
│   └── claude_pretooluse_guard.py
└── tests/
    ├── __init__.py
    ├── test_bootstrap_smoke.py
    ├── test_tdd_gate.py
    └── test_yaml_parsing.py
```

## Test Structure

**Suite Organization:**
```python
class TestCheckTddGate(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.root = pathlib.Path(self.temp_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_deny_when_no_test_exists(self):
        impl_path = str(self.root / "src" / "module.py")

        allowed, reason = check_tdd_gate(impl_path, str(self.root), tdd_enabled=True)
        self.assertFalse(allowed)
        self.assertIn("TDD", reason)
```
- This pattern comes directly from `scripts/tests/test_tdd_gate.py`.

**Patterns:**
- Use `setUpClass()` for shared script path discovery in integration-style suites, as in `scripts/tests/test_bootstrap_smoke.py`.
- Use `setUp()` and `tearDown()` to create and remove temporary filesystem fixtures with `tempfile.mkdtemp()` and `shutil.rmtree(...)`, as in `scripts/tests/test_bootstrap_smoke.py`, `scripts/tests/test_tdd_gate.py`, and `scripts/tests/test_yaml_parsing.py`.
- Use subprocess-based assertions for CLI scripts. `scripts/tests/test_bootstrap_smoke.py` runs `init.py` and `generate.py` with `subprocess.run(..., stdout=PIPE, stderr=PIPE, text=True, check=False)` and asserts on `returncode`, file creation, and output text.
- Use direct function imports for pure logic. `scripts/tests/test_tdd_gate.py` imports helpers from `scripts/hooks/claude_pretooluse_guard.py`, and `scripts/tests/test_yaml_parsing.py` imports `load_config()` from `scripts/generate.py`.

## Mocking

**Framework:** `unittest.mock`

**Patterns:**
```python
from unittest.mock import patch
```
- `unittest.mock.patch` is imported in `scripts/tests/test_tdd_gate.py`, but the current test suite does not establish an active patch-based mocking style.
- Current tests prefer real temporary directories, real file writes, and real subprocess execution over mocks.

**What to Mock:**
- External HTTP and GitHub interactions in `meta/progress/build_progress_report.py` are the clearest candidates for future mocking because they call `requests.get(...)` and `gh` via `subprocess.run(...)`.
- Process context and compliance-check subprocesses in `scripts/hooks/claude_pretooluse_guard.py` are also good mock boundaries when writing focused unit tests.

**What NOT to Mock:**
- Local filesystem behavior around generated files in `scripts/init.py` and `scripts/generate.py`. Existing tests treat these as integration surfaces and verify real file outputs.
- Pure helper logic in `scripts/hooks/claude_pretooluse_guard.py` and `scripts/validate_product_definition.py`. Existing coverage style favors direct function calls over mocked behavior.

## Fixtures and Factories

**Test Data:**
```python
self.test_yaml_content = '''version: "1.0"

project:
  name: "test-project"
  description: "A test project"

workspaces:
  primary:
    name: "main"
    branch: "main"
    runtime: "python3.11"
'''
```
- This inline fixture style is used in `scripts/tests/test_yaml_parsing.py`.

**Location:**
- Fixtures are defined inline in test classes rather than in dedicated fixture modules.
- Temporary directories are created inside each suite instead of using reusable factory helpers.

## Coverage

**Requirements:** None enforced.
- No coverage threshold or reporting configuration is present in `pyproject.toml`, `.coveragerc`, or GitHub Actions workflows.
- No CI workflow runs the `scripts/tests/` suite. `.github/workflows/product-definition-ci.yml` validates PR metadata and changed-file relationships only, and `.github/workflows/update-progress-report.yml` regenerates progress artifacts.

**View Coverage:**
```bash
Not configured
```

## Test Types

**Unit Tests:**
- `scripts/tests/test_tdd_gate.py` exercises pure helper behavior in `scripts/hooks/claude_pretooluse_guard.py`, including filename classification, test-file discovery, TDD enforcement scope, and gate decisions.
- `scripts/tests/test_yaml_parsing.py` targets config parsing behavior in `scripts/generate.py` and expects a parallel `check_compliance.py` parser API.

**Integration Tests:**
- `scripts/tests/test_bootstrap_smoke.py` performs end-to-end script execution across bootstrap steps (`init.py` → `generate.py` → expected compliance check script) using temporary output directories.
- GitHub Actions workflows act as workflow-level validation:
  - `.github/workflows/product-definition-ci.yml` runs `uv run python3 scripts/validate_product_definition.py --changed-file-list changed_files.txt --pr-body-file pr_body.md`
  - `.github/workflows/update-progress-report.yml` installs Python dependencies and runs `python meta/progress/build_progress_report.py --config ... --output-md ... --output-json ...`

**E2E Tests:**
- Not used beyond repository workflow automation. No browser, API, or full-environment E2E framework is present.

## Common Patterns

**Async Testing:**
```python
result = subprocess.run(
    [sys.executable, str(script)] + args,
    cwd=str(cwd or self.root_dir),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)
```
- The suite uses synchronous subprocess execution with captured output in `scripts/tests/test_bootstrap_smoke.py`.
- No async event loop testing framework is present.

**Error Testing:**
```python
result = self.run_script(self.init_script, ["--output", str(config_path)])
self.assertEqual(result.returncode, 1, "init.py should fail without --force")
```
- Error-path testing relies on exit-code assertions and message inspection, as seen in `scripts/tests/test_bootstrap_smoke.py`.
- Denial-path testing for policy helpers asserts both boolean outcome and explanation text, as in `scripts/tests/test_tdd_gate.py`.

## Current Verification Signals

- The scripted workflow validator is executable: `uv run python3 scripts/validate_product_definition.py --help` succeeds in the current working tree.
- The repository test suite is not green in the current working tree. Running `uv run python3 -m unittest discover -s scripts/tests -v` reports:
  - `scripts/tests/test_bootstrap_smoke.py` failing because it expects `scripts/check_compliance.py`, which is not present
  - `scripts/tests/test_yaml_parsing.py` failing to import `check_compliance`
  - additional bootstrap assertions still referencing older `ai-ops` naming and schema expectations that do not match current outputs from `scripts/init.py` and `scripts/generate.py`
- Treat the existing tests as valuable intent documentation for bootstrap and TDD guard behavior, but verify them against current script names and config schema before extending the suite.

---

*Testing analysis: 2026-03-24*
