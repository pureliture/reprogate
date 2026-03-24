# Testing Patterns

**Analysis Date:** 2025-02-14

## Test Framework

**Runner:**
- `unittest` (standard library)
- Config: Configured within `pyproject.toml` dependencies (`PyYAML`, `requests`), though no explicit `unittest` config file is present.

**Assertion Library:**
- `unittest.TestCase` assertions (standard library).

**Run Commands:**
```bash
python3 -m unittest discover scripts/tests/  # Run all tests
python3 scripts/tests/test_yaml_parsing.py  # Run specific test file
```

## Test File Organization

**Location:**
- Separate directory: `scripts/tests/`

**Naming:**
- `test_*.py` (e.g., `scripts/tests/test_yaml_parsing.py`, `scripts/tests/test_bootstrap_smoke.py`)

**Structure:**
```
scripts/tests/
├── __init__.py
├── test_bootstrap_smoke.py
├── test_tdd_gate.py
└── test_yaml_parsing.py
```

## Test Structure

**Suite Organization:**
```python
import unittest

class TestFeatureName(unittest.TestCase):
    """Docstring describing the test suite"""

    def setUp(self):
        # Set up test environment
        pass

    def tearDown(self):
        # Clean up test environment
        pass

    def test_specific_behavior(self):
        # Test code here
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
```

**Patterns:**
- **Setup pattern:** `setUp` for creating temporary directories or files, `setUpClass` for shared initialization (e.g., in `test_bootstrap_smoke.py`).
- **Teardown pattern:** `tearDown` for deleting temporary directories/files using `shutil.rmtree`.
- **Assertion pattern:** Use standard `self.assertEqual`, `self.assertTrue`, `self.assertIn`, `self.assertIsNone`.

## Mocking

**Framework:**
- Standard library `pathlib` and `tempfile` for isolation instead of mocking frameworks.

**Patterns:**
```python
import tempfile
import pathlib
import shutil

class TestFileSystem(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = pathlib.Path(self.temp_dir) / "test-config.yaml"

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
```

**What to Mock:**
- None detected. The project avoids external mocks by using filesystem and subprocess isolation.

**What NOT to Mock:**
- File system access (instead, use `tempfile`).
- YAML parsing (tested against actual PyYAML behavior).

## Fixtures and Factories

**Test Data:**
- YAML strings are defined inline in `setUp` or test methods as multiline strings.
- Example from `scripts/tests/test_yaml_parsing.py`:
```python
self.test_yaml_content = '''version: "1.0"
project:
  name: "test-project"
'''
```

**Location:**
- Defined within the test files themselves.

## Coverage

**Requirements:**
- Not explicitly enforced.

**View Coverage:**
- No coverage tool (like `coverage.py`) detected in `pyproject.toml`.

## Test Types

**Unit Tests:**
- Test individual logic components (e.g., `test_yaml_parsing.py` for YAML loading).

**Integration Tests:**
- Smoke tests for end-to-end flows (e.g., `test_bootstrap_smoke.py`).
- Use `subprocess.run` to execute scripts as external processes and check return codes/output.

**E2E Tests:**
- `test_bootstrap_smoke.py` covers the full bootstrap flow (`init` → `generate` → `check`).

## Common Patterns

**Async Testing:**
- Not detected (project is synchronous).

**Error Testing:**
- Verifies return codes of `subprocess.run` (e.g., `self.assertEqual(result.returncode, 1)` for expected failures).

---

*Testing analysis: 2025-02-14*
