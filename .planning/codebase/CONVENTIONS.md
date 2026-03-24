# Coding Conventions

**Analysis Date:** 2025-02-14

## Naming Patterns

**Files:**
- `snake_case.py` (e.g., `scripts/generate.py`, `scripts/tests/test_yaml_parsing.py`)

**Functions:**
- `snake_case` (e.g., `def parse_args(...)`, `def load_config(...)`)

**Variables:**
- `snake_case` for local variables (e.g., `config_path`, `rendered_outputs`)
- `UPPER_CASE` for module-level constants (e.g., `ROOT`, `TEMPLATES_DIR` in `scripts/generate.py`)

**Types:**
- `PascalCase` for classes (e.g., `class TestBootstrapSmokeTest` in `scripts/tests/test_bootstrap_smoke.py`)
- Extensive use of Python 3.10+ type hints (`|` for unions, `List`, `Dict`, `Any` from `typing` module)

## Code Style

**Formatting:**
- Standard PEP 8 styles are followed.
- Each script and test file starts with a `#!/usr/bin/env python3` shebang.
- Indentation is 4 spaces.

**Linting:**
- Not explicitly configured via `ruff` or `flake8` in `pyproject.toml`, but code adheres to PEP 8.

## Import Organization

**Order:**
1. Standard library imports (e.g., `argparse`, `pathlib`, `sys`)
2. Third-party imports (e.g., `yaml`)
3. Local application imports (e.g., `from generate import load_config`)

**Path Aliases:**
- None detected. `sys.path.insert(0, ...)` is used in test files to include the parent directory for imports.

## Error Handling

**Patterns:**
- Use `try/except` blocks for specific errors (e.g., `ValueError` in `scripts/generate.py`).
- Scripts return non-zero exit codes on failure via `sys.exit(main())`.
- Error messages are printed to `sys.stderr`.

## Logging

**Framework:**
- Primarily uses `print()` for standard output messages and `sys.stderr` for errors.

**Patterns:**
- Success messages inform the user of actions taken (e.g., "Generated {shown}" in `scripts/generate.py`).
- Error messages provide clear context (e.g., "Config file not found: {config_path}").

## Comments

**When to Comment:**
- Comments are used to describe complex logic or TDD cycles.
- Headers in scripts describe the file's purpose and version.

**JSDoc/TSDoc:**
- Not applicable (Python project).

**Docstrings:**
- Modules and classes use triple-quoted docstrings.
- Docstrings describe the purpose and return values of functions/classes.

## Function Design

**Size:**
- Functions are generally concise and focused on a single responsibility (e.g., `render_template` only handles string replacement).

**Parameters:**
- Type hinted parameters with default values where appropriate (e.g., `def parse_args(argv: List[str] | None = None)`).

**Return Values:**
- Explicit return types are provided in type hints (e.g., `-> Dict[str, Any]`).

## Module Design

**Exports:**
- Explicit function and class definitions meant for use across the project.

**Barrel Files:**
- `__init__.py` files are present in `scripts/tests/` to facilitate test discovery and module imports.

---

*Convention analysis: 2025-02-14*
