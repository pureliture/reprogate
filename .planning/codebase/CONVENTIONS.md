# Coding Conventions

**Analysis Date:** 2026-03-24

## Naming Patterns

**Files:**
- Use `snake_case` for Python modules and scripts in `scripts/`, such as `scripts/generate.py`, `scripts/validate_product_definition.py`, and `scripts/hooks/claude_pretooluse_guard.py`.
- Use `test_*.py` naming for Python test modules in `scripts/tests/`, such as `scripts/tests/test_tdd_gate.py` and `scripts/tests/test_bootstrap_smoke.py`.
- Use uppercase markdown filenames for generated planning artifacts in `.planning/codebase/`, such as `.planning/codebase/CONVENTIONS.md` and `.planning/codebase/TESTING.md`.
- Use uppercase record IDs in filenames for decision records under `records/adr/` and `records/rfc/`, such as `records/adr/ADR-007-uv-toolchain-adoption.md` and `records/rfc/RFC-002-stage1-hardening.md`.

**Functions:**
- Use `snake_case` for functions and helpers, such as `run_script()` in `scripts/cli.py`, `context_from_config()` in `scripts/generate.py`, `validate_pr_body()` in `scripts/validate_product_definition.py`, and `check_tdd_gate()` in `scripts/hooks/claude_pretooluse_guard.py`.
- Use verb-led names for command and validation functions: `parse_args()`, `load_config()`, `render_outputs()`, `collect_records()`, `extract_section()`, and `fetch_github_state()`.
- Use boolean helper names that read like predicates, such as `is_test_file()`, `is_documentation_target()`, `is_readonly_bash()`, and `should_enforce_tdd_gate()` in `scripts/hooks/claude_pretooluse_guard.py`.

**Variables:**
- Use `snake_case` for locals and parameters, such as `config_path`, `output_root`, `related_docs_block`, `item_weighted_score`, and `tests_root`.
- Use short but descriptive path variables for filesystem-heavy code, such as `ROOT`, `DOCS_DIR`, `TEMPLATES_DIR`, `PROCESS_CONTEXT`, and `CHECKER` in `scripts/generate.py`, `scripts/search_docs.py`, and `scripts/hooks/claude_pretooluse_guard.py`.
- Use plural collection names for lists and mappings, such as `rendered_outputs`, `records`, `skills`, `errors`, `warnings`, `matches`, and `stages_result`.

**Types:**
- Use `PascalCase` for test classes and standard classes, such as `TestBootstrapSmokeTest`, `TestBootstrapEdgeCases`, `TestYAMLParsingWithPyYAML`, and `TestCheckTddGate` in `scripts/tests/`.
- Use `UPPER_CASE` for module-level constants, such as `ROOT`, `CONFIG_PATH`, `FRAMEWORK_DIRECTORIES`, `REQUIRED_PR_SECTIONS`, `IMPLEMENTATION_PATH_PREFIXES`, and `CODE_EXTENSIONS`.
- Use Python type hints throughout core scripts, including modern union syntax like `List[str] | None` in `scripts/cli.py` and `str | None` in `scripts/search_docs.py`, plus `Dict[str, Any]`, `Tuple[bool, str]`, and `Sequence[pathlib.Path]`.

## Code Style

**Formatting:**
- No dedicated formatter config is detected. `.prettierrc*`, `ruff.toml`, `biome.json`, and `.editorconfig` are absent at the repository root.
- Follow the existing Python style in `scripts/*.py`: 4-space indentation, standard blank lines between top-level declarations, and line breaks for long argument lists, as seen in `scripts/generate.py` and `scripts/validate_product_definition.py`.
- Keep executable scripts self-identifying with `#!/usr/bin/env python3` shebangs. This pattern is used in `scripts/cli.py`, `scripts/init.py`, `scripts/generate.py`, `scripts/gatekeeper.py`, `scripts/search_docs.py`, `scripts/validate_product_definition.py`, and test files under `scripts/tests/`.
- Prefer `pathlib.Path` over `os.path` for repository paths. This is the dominant style in `scripts/cli.py`, `scripts/generate.py`, `scripts/init.py`, `scripts/gatekeeper.py`, `scripts/search_docs.py`, `scripts/validate_product_definition.py`, and `meta/progress/build_progress_report.py`.

**Linting:**
- No lint configuration is detected. `.eslintrc*`, `eslint.config.*`, `ruff.toml`, `mypy.ini`, `pytest.ini`, `tox.ini`, and `.coveragerc` are absent.
- Treat `pyproject.toml` as dependency metadata only. It declares runtime dependencies in `pyproject.toml` but does not define formatter, linter, or test tool sections.
- Preserve the codebase’s manually maintained readability conventions: explicit imports, direct control flow, and small helper functions.

## Import Organization

**Order:**
1. Standard library imports first, such as `argparse`, `pathlib`, `sys`, `json`, `re`, and `subprocess` in `scripts/*.py`.
2. Third-party imports second, such as `yaml` in `scripts/generate.py` and `yaml` plus `requests` in `meta/progress/build_progress_report.py`.
3. Local imports last, when needed, such as `from hooks.claude_pretooluse_guard import ...` in `scripts/tests/test_tdd_gate.py` and `from generate import load_config ...` in `scripts/tests/test_yaml_parsing.py`.

**Path Aliases:**
- No import alias system is used. There are no package aliases configured in `pyproject.toml`.
- Tests currently adjust module resolution directly with `sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))` in `scripts/tests/test_tdd_gate.py` and `scripts/tests/test_yaml_parsing.py`. Follow the existing layout when adding tests beside scripts.

## Error Handling

**Patterns:**
- Return integer exit codes from `main()` and terminate with `sys.exit(main())`. This pattern is consistent in `scripts/cli.py`, `scripts/init.py`, `scripts/generate.py`, `scripts/gatekeeper.py`, `scripts/search_docs.py`, `scripts/validate_product_definition.py`, and `scripts/hooks/claude_pretooluse_guard.py`.
- Print actionable failure messages to `stderr` for user-facing CLI errors, such as `Config file not found: ...` in `scripts/generate.py` and overwrite refusal messages in `scripts/init.py`.
- Use defensive parsing and safe fallbacks instead of crashing when inputs are missing or malformed. Examples include:
  - returning defaults from `load_config()` in `scripts/generate.py`
  - returning `{}` on malformed hook payloads in `scripts/hooks/claude_pretooluse_guard.py`
  - returning `"not_found"` on GitHub lookup failures in `meta/progress/build_progress_report.py`
  - skipping unreadable markdown files in `scripts/search_docs.py`
- Keep validation logic additive and explicit. `scripts/validate_product_definition.py` accumulates `errors: list[str]` and prints all failures before returning exit code `1`.

## Logging

**Framework:** `print()`

**Patterns:**
- Use plain `print()` for normal CLI feedback and status reporting. Examples include `Generated ...` and `Copied framework directories ...` in `scripts/generate.py`, and pass/fail banners in `scripts/gatekeeper.py`.
- Use emoji-prefixed status lines for human-readable gate output in `scripts/gatekeeper.py` and `scripts/validate_product_definition.py` (`✅`, `⚠️`, `🔴`, `🟢`).
- Keep logs concise and step-oriented in workflows. `.github/workflows/product-definition-ci.yml` prints changed files, and `meta/progress/build_progress_report.py` prints per-stage scoring during report generation.

## Comments

**When to Comment:**
- Use top-of-file docstrings to declare file purpose, scope, or workflow context. This is common in `scripts/gatekeeper.py`, `scripts/search_docs.py`, `scripts/validate_product_definition.py`, and test files under `scripts/tests/`.
- Add inline comments only when behavior is not obvious from code, such as search strategy notes in `scripts/hooks/claude_pretooluse_guard.py`, heredoc safety notes in `.github/workflows/product-definition-ci.yml`, and comparison notes in `.github/workflows/update-progress-report.yml`.
- Preserve repository workflow rules in markdown documents instead of burying them in code. `AGENTS.md`, `WORKSPACE-PROFILE.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and `.github/copilot-instructions.md` are the active convention carriers.

**JSDoc/TSDoc:**
- Not applicable for production code. No TypeScript or JavaScript source modules are present outside generated/tooling metadata like `.claude/package.json` and `.gemini/package.json`.
- Use Python docstrings for modules, functions, and test classes where explanation is needed, as seen in `scripts/generate.py`, `scripts/search_docs.py`, and `scripts/tests/test_tdd_gate.py`.

## Function Design

**Size:** Keep functions narrowly scoped and composable.
- `scripts/cli.py` delegates subcommands through small wrappers like `run_script()` and `run_search()`.
- `scripts/validate_product_definition.py` separates path parsing, section extraction, PR validation, changed-file validation, scenario validation, and CLI orchestration into distinct helpers.
- `scripts/hooks/claude_pretooluse_guard.py` isolates payload parsing, process checks, bash mutability checks, and TDD checks into separate functions.

**Parameters:** Pass explicit paths and simple primitives.
- Most helpers accept `Path`, `str`, `list[str]`, or `dict` inputs instead of hidden globals, such as `load_config(path: pathlib.Path)` in `scripts/generate.py`, `validate_changed_files(repo_root: Path, changed_files: list[str], pr_body: str, errors: list[str])` in `scripts/validate_product_definition.py`, and `check_tdd_gate(file_path: str, root_dir: str, tdd_enabled: bool = True)` in `scripts/hooks/claude_pretooluse_guard.py`.
- CLI entry points centralize argument parsing with `argparse` in `scripts/cli.py`, `scripts/init.py`, `scripts/generate.py`, `scripts/gatekeeper.py`, `scripts/search_docs.py`, and `scripts/validate_product_definition.py`.

**Return Values:** Prefer explicit, inspectable return values.
- Return structured values for reusable logic, such as `Tuple[int, List[str]]` from `evaluate_gate()` in `scripts/gatekeeper.py`, `Tuple[bool, str]` from `check_tdd_gate()` in `scripts/hooks/claude_pretooluse_guard.py`, and lists of dictionaries from `search_content()` in `scripts/search_docs.py`.
- Reserve printing for outer orchestration layers and CLI `main()` functions.

## Module Design

**Exports:** Modules expose plain functions and constants directly.
- There is no formal package API layer. Scripts are imported directly in tests, for example `from generate import load_config ...` in `scripts/tests/test_yaml_parsing.py`.
- Entry points stay executable as scripts and reusable as modules by keeping logic outside the `if __name__ == "__main__":` block.

**Barrel Files:** Minimal usage.
- `scripts/tests/__init__.py` exists only to mark the test package and contains no re-export pattern.
- No barrel modules or `__all__` export layers are used elsewhere.

## Repository Workflow Expectations

- Follow record-first workflow conventions in `AGENTS.md`: read `WORKSPACE-PROFILE.md`, `docs/governance/constitution.md`, `docs/governance/operating-model.md`, and `docs/strategy/final-definition.md` before substantial work.
- Keep pull requests document-backed. `.github/PULL_REQUEST_TEMPLATE.md` and `scripts/validate_product_definition.py` require populated `## Related Docs`, `## Decision Record`, and `## Verification` sections with repository paths.
- When changing implementation surfaces in `scripts/`, `skills/`, `templates/`, or `.github/`, pair the change with doc or decision updates under `docs/spec/`, `docs/strategy/`, `docs/design/`, `docs/governance/`, `records/adr/`, or `records/rfc/` as enforced by `scripts/validate_product_definition.py`.
- Use `uv` as the repository-standard Python invocation for new documented workflows, per `AGENTS.md` and `records/adr/ADR-007-uv-toolchain-adoption.md`, even though some existing examples still invoke `python3` directly in `README.md`, `scripts/hooks/git_pre_commit.sh`, and `scripts/install_git_hooks.sh`.
- Treat `.github/CODEOWNERS` ownership boundaries as part of review workflow: `docs/strategy/`, `docs/spec/`, `docs/design/`, `records/`, `scripts/`, `skills/`, `templates/`, and `.github/` are all owned by `@pureliture`.

---

*Convention analysis: 2026-03-24*
