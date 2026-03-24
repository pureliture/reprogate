# External Integrations

**Analysis Date:** 2025-03-24

## Libraries & Packages

- **requests (>=2.28):** Used for making HTTP requests to external APIs or services.
- **PyYAML:** Primary library for parsing and generating `reprogate.yaml` and other YAML-based configuration files.
- **rego (OPA):** Integrated via policies in `skills/` for enforcing engineering standards and workflow rules.

## Tooling & Infrastructure

- **uv:** The primary Python package manager and toolchain orchestrator, as specified in `pyproject.toml` and `reprogate.yaml`.
- **Git Hooks:** Custom hooks (e.g., `pre-commit`, `pre-push`) are used to enforce gates and validate project definitions before commits or pushes.
- **GitHub Workflows:** CI/CD integration for automated testing and progress report updates (e.g., `.github/workflows/update-progress-report.yml`).

## Data Flow

- **Local File System:** Most "integrations" are currently local, involving the generation of adapter files from `reprogate.yaml` and the synchronization of policies across `.omc`, `.omx`, and `.gemini` directories.
- **AI Tooling Context:** The codebase is designed to be consumed by AI agents (Claude, Gemini), with specific hooks and guards to manage the interaction between the agent and the repository.
