# Technology Stack

**Analysis Date:** 2026-03-24

## Languages

**Primary:**
- Python 3.10+ - Repository tooling and automation in `scripts/cli.py`, `scripts/init.py`, `scripts/generate.py`, `scripts/gatekeeper.py`, `scripts/search_docs.py`, `scripts/validate_product_definition.py`, and `meta/progress/build_progress_report.py`.
- Markdown - Canonical product, governance, ADR/RFC, and generated artifact content under `README.md`, `docs/`, `records/`, `AGENTS.md`, and `templates/records/WORK-RECORD-TEMPLATE.md`.

**Secondary:**
- Rego v1 syntax - Policy rules in `skills/record-required/rules.rego`, `skills/decision-documented/rules.rego`, `skills/scope-defined/rules.rego`, and `skills/verification-present/rules.rego`.
- Bash - Bootstrap and Git hook scripts in `scripts/install_git_hooks.sh`, `scripts/sync_omc_policy.sh`, and `scripts/hooks/git_pre_commit.sh`.
- YAML / TOML / JSON - Configuration and workflow definitions in `reprogate.yaml`, `meta/progress/progress-map.yaml`, `pyproject.toml`, `.codex/config.toml`, `.claude/settings.json`, `.gemini/settings.json`, and `.github/workflows/*.yml`.
- Jinja-style text templates - Generated adapter/config content in `templates/*.j2`; rendering is custom string replacement from `scripts/generate.py` and `scripts/init.py`, not the Jinja2 runtime package.

## Runtime

**Environment:**
- Python >=3.10 required by `pyproject.toml`; `README.md` documents Python `3.13.3` as the verified local workspace version.
- Python 3.11 is the CI runtime in `.github/workflows/product-definition-ci.yml` and `.github/workflows/update-progress-report.yml`.
- Node.js runtime is required for local AI-tool hooks because `.claude/settings.json`, `.gemini/settings.json`, and `.codex/config.toml` invoke `node` commands; no repository-pinned Node version was detected.
- OPA CLI is an external runtime requirement documented in `README.md` and selected as the gate engine in `reprogate.yaml`.

**Package Manager:**
- `uv` - Standard Python toolchain declared in `pyproject.toml` (`[tool.reprogate].python_toolchain = "uv"`) and adopted in `records/adr/ADR-007-uv-toolchain-adoption.md`.
- Lockfile: present in `uv.lock`.

## Frameworks

**Core:**
- No web application framework detected. The repository is a tooling/framework distribution centered on filesystem artifacts, Python scripts, and policy files in `scripts/`, `templates/`, `skills/`, and `docs/`.
- Open Policy Agent (OPA) / Rego - Policy layer selected in `reprogate.yaml` and implemented as rule assets in `skills/*/rules.rego`.
- GitHub Actions - Automation framework in `.github/workflows/product-definition-ci.yml` and `.github/workflows/update-progress-report.yml`.

**Testing:**
- Python standard library `unittest` - Test suites in `scripts/tests/test_bootstrap_smoke.py`, `scripts/tests/test_tdd_gate.py`, and `scripts/tests/test_yaml_parsing.py`.
- No `pytest`, `jest`, or `vitest` configuration file was detected at the repository root.

**Build/Dev:**
- `uv run python3 ...` - Preferred execution pattern documented in `records/adr/ADR-007-uv-toolchain-adoption.md` and used in `.github/workflows/product-definition-ci.yml`.
- Plain `python3 ...` - Still used in `README.md`, `scripts/install_git_hooks.sh`, `scripts/hooks/git_pre_commit.sh`, and `.github/workflows/update-progress-report.yml`.
- Git hooks - Local enforcement via `.githooks/pre-commit`, `scripts/hooks/git_pre_commit.sh`, and installer `scripts/install_git_hooks.sh`.

## Key Dependencies

**Critical:**
- `PyYAML` `6.0.3` - Locked in `uv.lock`, declared in `pyproject.toml`, and used by `scripts/generate.py` and `meta/progress/build_progress_report.py` for YAML parsing.
- `requests` `2.32.5` - Locked in `uv.lock`, declared in `pyproject.toml`, and used by `meta/progress/build_progress_report.py` for GitHub API access.

**Infrastructure:**
- `gh` CLI - Optional fallback client in `meta/progress/build_progress_report.py` when `GITHUB_TOKEN` is unavailable.
- `git` CLI - Required by `README.md`, used by `scripts/install_git_hooks.sh`, `scripts/hooks/git_pre_commit.sh`, and both GitHub Actions workflows.
- `opa` CLI - Required by `README.md` and referenced as the selected gate engine in `reprogate.yaml`; current Python gate evaluation in `scripts/gatekeeper.py` is file-based and does not yet invoke the CLI directly.
- `actions/checkout` - CI checkout action in `.github/workflows/product-definition-ci.yml` and `.github/workflows/update-progress-report.yml`.
- `actions/setup-python` - CI Python provisioning in `.github/workflows/product-definition-ci.yml` and `.github/workflows/update-progress-report.yml`.
- `astral-sh/setup-uv` - CI `uv` installation in `.github/workflows/product-definition-ci.yml`.

## Configuration

**Environment:**
- Project-level ReproGate settings live in `reprogate.yaml`; the starter template is `templates/reprogate.yaml.j2`.
- Python dependency and interpreter constraints live in `pyproject.toml` and `uv.lock`.
- AI-tool adapter settings live in `.claude/settings.json`, `.gemini/settings.json`, `.codex/config.toml`, and `.github/copilot-instructions.md`.
- Progress-report inputs live in `meta/progress/progress-map.yaml`.
- No `.env` file was detected at the repository root during this scan.

**Build:**
- GitHub workflow definitions: `.github/workflows/product-definition-ci.yml` and `.github/workflows/update-progress-report.yml`.
- Entry-point commands documented in `README.md`:
  - `python3 scripts/init.py --project-name sample-app --force`
  - `python3 scripts/generate.py --force`
  - `python3 scripts/gatekeeper.py`
- Additional command router: `scripts/cli.py` dispatches `init`, `generate`, `check`, `search`, `search-content`, and `print` subcommands for the local tooling surface.
- Generated adapter/config files are rendered from `templates/` by `scripts/generate.py`; framework payload copy roots are `docs/`, `scripts/`, `skills/`, and `templates/`.

## Platform Requirements

**Development:**
- Python 3.10+ with dependencies from `pyproject.toml` / `uv.lock`.
- `uv` installed for the standard local execution path described in `records/adr/ADR-007-uv-toolchain-adoption.md`.
- `git` available for hook installation and repository checks from `scripts/install_git_hooks.sh` and `scripts/hooks/git_pre_commit.sh`.
- `opa` installed for the intended policy-engine workflow documented in `README.md` and configured in `reprogate.yaml`.
- Node.js available for hook commands referenced by `.claude/settings.json`, `.gemini/settings.json`, and `.codex/config.toml`.
- Optional `gh` CLI for GitHub-state lookup fallback in `meta/progress/build_progress_report.py`.

**Production:**
- No long-running production service or deployable application target was detected.
- Operational execution targets are developer worktrees and GitHub-hosted runners (`ubuntu-24.04`) in `.github/workflows/product-definition-ci.yml` and `.github/workflows/update-progress-report.yml`.

---

*Stack analysis: 2026-03-24*
