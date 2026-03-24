# Claude Code Notes

Claude Code should follow the repository-wide rules in `AGENTS.md`.

If Claude-specific operational details are needed later, keep them here without duplicating tool-neutral repository policy.

<!-- GSD:project-start source:PROJECT.md -->
## Project

**ReproGate**

**Core Value:** ReproGate ensures that AI-assisted development remains rigorous and reproducible by centering the workflow around durable artifacts (Records and Skills) rather than ephemeral chat context.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.10+ - Used for all core tooling, scripts, and gatekeeper logic in `scripts/`.
- Shell (Bash) - Used for Git hooks and installation scripts in `.githooks/` and `scripts/`.
- Markdown - Used for documentation, records, and skills across `docs/`, `records/`, and `skills/`.
## Runtime
- Python 3.10+
- uv - Specified in `pyproject.toml` and `reprogate.yaml` as the python toolchain.
- Lockfile: `uv.lock` is present.
## Frameworks
- ReproGate (Custom) - A repository tooling framework defined by `reprogate.yaml`.
- pytest - Used for testing scripts, located in `scripts/tests/`.
- uv - Used for dependency management and environment isolation.
## Key Dependencies
- `PyYAML` (>=6.0) - Used for parsing configuration files and frontmatter in Markdown records.
- `requests` (>=2.28) - Used for external HTTP requests.
- Git - Used for version control and hook-based enforcement.
## Configuration
- Configured via `reprogate.yaml` in the project root.
- Python dependencies managed via `pyproject.toml`.
- `pyproject.toml`
- `reprogate.yaml`
## Platform Requirements
- Python 3.10 or higher.
- `uv` toolchain recommended.
- Primarily a development-time tooling suite; runs in local developer environments and CI/CD pipelines.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- `snake_case.py` (e.g., `scripts/generate.py`, `scripts/tests/test_yaml_parsing.py`)
- `snake_case` (e.g., `def parse_args(...)`, `def load_config(...)`)
- `snake_case` for local variables (e.g., `config_path`, `rendered_outputs`)
- `UPPER_CASE` for module-level constants (e.g., `ROOT`, `TEMPLATES_DIR` in `scripts/generate.py`)
- `PascalCase` for classes (e.g., `class TestBootstrapSmokeTest` in `scripts/tests/test_bootstrap_smoke.py`)
- Extensive use of Python 3.10+ type hints (`|` for unions, `List`, `Dict`, `Any` from `typing` module)
## Code Style
- Standard PEP 8 styles are followed.
- Each script and test file starts with a `#!/usr/bin/env python3` shebang.
- Indentation is 4 spaces.
- Not explicitly configured via `ruff` or `flake8` in `pyproject.toml`, but code adheres to PEP 8.
## Import Organization
- None detected. `sys.path.insert(0, ...)` is used in test files to include the parent directory for imports.
## Error Handling
- Use `try/except` blocks for specific errors (e.g., `ValueError` in `scripts/generate.py`).
- Scripts return non-zero exit codes on failure via `sys.exit(main())`.
- Error messages are printed to `sys.stderr`.
## Logging
- Primarily uses `print()` for standard output messages and `sys.stderr` for errors.
- Success messages inform the user of actions taken (e.g., "Generated {shown}" in `scripts/generate.py`).
- Error messages provide clear context (e.g., "Config file not found: {config_path}").
## Comments
- Comments are used to describe complex logic or TDD cycles.
- Headers in scripts describe the file's purpose and version.
- Not applicable (Python project).
- Modules and classes use triple-quoted docstrings.
- Docstrings describe the purpose and return values of functions/classes.
## Function Design
- Functions are generally concise and focused on a single responsibility (e.g., `render_template` only handles string replacement).
- Type hinted parameters with default values where appropriate (e.g., `def parse_args(argv: List[str] | None = None)`).
- Explicit return types are provided in type hints (e.g., `-> Dict[str, Any]`).
## Module Design
- Explicit function and class definitions meant for use across the project.
- `__init__.py` files are present in `scripts/tests/` to facilitate test discovery and module imports.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern Overview
- **Policy-as-Code:** Uses "Skills" (defined in `skills/`) to enforce repository standards via automated checks.
- **Documentation-First:** Architecture and product decisions are driven by a tiered documentation structure (`strategy` -> `spec` -> `design`).
- **Template-driven Scaffolding:** Uses a central configuration (`reprogate.yaml`) to generate project-specific adapters and agent configurations.
## Layers
- Purpose: Defines the "what", "why", and "how" of the project through structured Markdown.
- Location: `docs/`
- Contains: Strategy, Specifications, and Design documents.
- Depends on: None.
- Used by: Developers and the `gatekeeper.py` for compliance checks.
- Purpose: Defines the rules and guidelines that the repository must follow.
- Location: `skills/`
- Contains: Rego policies (`rules.rego`) and human-readable `guidelines.md`.
- Depends on: OPA (Open Policy Agent) concepts.
- Used by: `scripts/gatekeeper.py`.
- Purpose: Provides the CLI and automation logic for the framework.
- Location: `scripts/`
- Contains: Python scripts for initialization, generation, and gatekeeping.
- Depends on: Python 3.10+, PyYAML.
- Used by: CI/CD pipelines, Git hooks, and developers via `cli.py`.
- Purpose: Stores the immutable history of architectural and product decisions.
- Location: `records/`
- Contains: ADRs (Architecture Decision Records) and RFCs (Request for Comments).
- Depends on: None.
- Used by: `scripts/gatekeeper.py` (to verify decisions are documented).
## Data Flow
## Key Abstractions
- Purpose: A modular unit of governance or capability.
- Examples: `skills/record-required`, `skills/decision-documented`.
- Pattern: Strategy pattern for repository rules.
- Purpose: Formal documentation of a work item or decision.
- Examples: `records/adr/*.md`, `records/rfc/*.md`.
- Pattern: Immutable audit log.
- Purpose: Blueprint for project files.
- Examples: `templates/reprogate.yaml.j2`, `templates/claude/commands/`.
- Pattern: Jinja2-style placeholders (though currently using simple string replacement in `generate.py`).
## Entry Points
- Location: `scripts/cli.py`
- Triggers: User execution (`python scripts/cli.py <command>`).
- Responsibilities: Routes commands to `init.py`, `generate.py`, `gatekeeper.py`, or `search_docs.py`.
- Location: `scripts/gatekeeper.py`
- Triggers: Git `pre-commit` hooks or CI pipelines.
- Responsibilities: Validates repository state against active skills.
- Location: `scripts/generate.py`
- Triggers: Post-config updates or `init` command.
- Responsibilities: Synchronizes project files with the `reprogate.yaml` definition.
## Error Handling
- **Strict Mode:** `gatekeeper.py --strict` fails if any mandatory record or section is missing.
- **Validation Messages:** Clear console output with ❌ and ⚠️ emojis to indicate errors and warnings.
## Cross-Cutting Concerns
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd:quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd:debug` for investigation and bug fixing
- `/gsd:execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd:profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
