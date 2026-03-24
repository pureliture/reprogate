# Architecture

**Analysis Date:** 2026-03-24

## Pattern Overview

**Overall:** Artifact-driven documentation-first Python tooling with generated adapter surfaces

**Key Characteristics:**
- The repository is organized around canonical product-definition documents in `docs/` that define the system before implementation details are added, with `docs/strategy/final-definition.md`, `docs/spec/README.md`, and `docs/design/architecture.md` acting as the architectural spine.
- Executable behavior is concentrated in small Python entrypoints under `scripts/`, especially `scripts/init.py`, `scripts/generate.py`, `scripts/gatekeeper.py`, `scripts/search_docs.py`, and `scripts/validate_product_definition.py`.
- The codebase mixes framework-owned assets (`docs/`, `scripts/`, `skills/`, `templates/`) with generated or vendored tool-adapter surfaces (`AGENTS.md`, `WORKSPACE-PROFILE.md`, `.claude/`, `.codex/`, `.github/`, `.gemini/`) following the boundary defined in `docs/portability/ai-tool-artifact-boundary.md`.

## Layers

**Strategy Layer:**
- Purpose: Define product identity, scope, roadmap, and product boundary.
- Location: `docs/strategy/`
- Contains: Canonical intent documents such as `docs/strategy/final-definition.md`, `docs/strategy/vision.md`, `docs/strategy/roadmap.md`, `docs/strategy/product-boundary.md`, and `docs/strategy/scenarios.md`.
- Depends on: Repository governance context from `docs/governance/`.
- Used by: Spec documents in `docs/spec/`, design documents in `docs/design/`, validation policy in `scripts/validate_product_definition.py`, and generated adapter guidance in `AGENTS.md`.

**Specification Layer:**
- Purpose: Turn strategy into implementation contracts and interfaces.
- Location: `docs/spec/`
- Contains: Contract-oriented documents including `docs/spec/product-surface-spec.md`, `docs/spec/record-contract.md`, `docs/spec/rule-gate-spec.md`, `docs/spec/skill-workflow-object-model.md`, and `docs/spec/storage-adapter-spec.md`.
- Depends on: Product boundary and identity docs in `docs/strategy/`.
- Used by: Design docs in `docs/design/`, scripts that implement bootstrap and validation behavior, and future policy/runtime work referenced by `scripts/gatekeeper.py`.

**Design Layer:**
- Purpose: Describe concrete repository structure and runtime surfaces.
- Location: `docs/design/`
- Contains: Architecture and implementation-structure docs such as `docs/design/architecture.md`, `docs/design/README.md`, `docs/design/product-spec.md`, and `docs/design/presets-spec.md`.
- Depends on: `docs/strategy/` and `docs/spec/`.
- Used by: Contributors adding scripts/templates and by adapter-facing docs like `README.md` and `AGENTS.md`.

**Governance and Decision Layer:**
- Purpose: Capture operating rules and durable decisions that constrain implementation.
- Location: `docs/governance/`, `records/adr/`, `records/rfc/`
- Contains: Governance policies in `docs/governance/operating-model.md` and `docs/governance/constitution.md`, architecture decisions in `records/adr/*.md`, and proposal records in `records/rfc/*.md`.
- Depends on: Canonical product docs in `docs/strategy/`.
- Used by: Gate logic in `scripts/gatekeeper.py`, PR validation in `scripts/validate_product_definition.py`, and skill guidance in `skills/*/guidelines.md`.

**Runtime Tooling Layer:**
- Purpose: Provide executable bootstrap, generation, search, validation, and gatekeeper behaviors.
- Location: `scripts/`
- Contains: CLI dispatch in `scripts/cli.py`, config bootstrap in `scripts/init.py`, framework/adaptor generation in `scripts/generate.py`, record gate evaluation in `scripts/gatekeeper.py`, search utilities in `scripts/search_docs.py`, hook enforcement in `scripts/hooks/claude_pretooluse_guard.py`, and workflow validation in `scripts/validate_product_definition.py`.
- Depends on: Configuration in `reprogate.yaml`, framework assets in `docs/`, `skills/`, and `templates/`, plus standard-library modules and `yaml`/`requests` for selected scripts.
- Used by: Local developers, generated adapters, GitHub Actions workflows in `.github/workflows/`, and tool hooks installed from `.claude/` or `.githooks/`.

**Framework Asset Layer:**
- Purpose: Hold reusable, portable assets copied into target repositories.
- Location: `skills/`, `templates/`, selected files in `docs/`, `scripts/`
- Contains: Skill guidance in `skills/decision-documented/guidelines.md`, `skills/record-required/guidelines.md`, `skills/scope-defined/guidelines.md`, and `skills/verification-present/guidelines.md`; template files such as `templates/reprogate.yaml.j2`, `templates/AGENTS.md.j2`, and `templates/project-ops/work-packets/index.md.j2`.
- Depends on: Product decisions captured in docs and records.
- Used by: `scripts/generate.py` when copying framework trees and rendering repository-specific outputs.

**Adapter Surface Layer:**
- Purpose: Expose the framework to individual AI tools and automation systems.
- Location: `AGENTS.md`, `WORKSPACE-PROFILE.md`, `.claude/`, `.codex/`, `.github/`, `.gemini/`
- Contains: Tool instructions, vendored `get-shit-done` command packs, agent manifests, GitHub workflow automation, and generated prompt/config scaffolds.
- Depends on: Framework-owned docs/scripts and templates rendered by `scripts/generate.py`.
- Used by: Claude, Codex, GitHub Copilot, Gemini, and repository automation.

**Progress Reporting Layer:**
- Purpose: Build generated project-tracking artifacts from roadmap/config plus repository and GitHub state.
- Location: `meta/progress/`
- Contains: Source config in `meta/progress/progress-map.yaml`, generator logic in `meta/progress/build_progress_report.py`, and generated outputs `meta/progress/progress.md` and `meta/progress/progress.json`.
- Depends on: GitHub API or `gh` CLI state, roadmap files under `docs/strategy/`, and repository file existence.
- Used by: `.github/workflows/update-progress-report.yml` and readers of `meta/progress/progress.md`.

## Data Flow

**Bootstrap and Adapter Generation:**

1. `scripts/init.py` renders `templates/reprogate.yaml.j2` into the repository root as `reprogate.yaml`, filling project metadata and adapter toggles.
2. `scripts/generate.py` loads `reprogate.yaml`, derives template context, copies portable framework directories (`docs/`, `scripts/`, `skills/`, `templates/`), and renders adapter files such as `AGENTS.md`, `WORKSPACE-PROFILE.md`, `.codex/README.md`, and `.claude/settings.json`.
3. Generated adapter files then direct AI tools back to the copied framework docs and scripts, creating a self-contained target-repository surface.

**Record Enforcement and Gate Evaluation:**

1. `scripts/gatekeeper.py` loads lightweight config from `reprogate.yaml` to locate `records/` and `skills/`.
2. It parses Markdown frontmatter and section headers from every record under `records/` and enumerates skills by finding `guidelines.md` folders under `skills/`.
3. Gate rules are evaluated against artifact presence and section requirements; the script emits pass/fail output for direct invocation and for hook or CI entry surfaces.

**Hook Guard Enforcement:**

1. Tool payloads enter `scripts/hooks/claude_pretooluse_guard.py` through the generated wrapper path referenced by `.claude/settings.json` or installed hooks.
2. The guard reads local process context from `.dpc/process-context.json` or `.omc`-style context, classifies the requested tool action, and applies read-only/process restrictions plus TDD-gate checks for implementation files.
3. Before allowing writes or mutating shell commands, it runs the compliance checker path configured in the script and returns an allow/deny JSON response to the invoking tool.

**Product Definition Validation:**

1. `.github/workflows/product-definition-ci.yml` collects changed files and PR body content on pull requests.
2. The workflow runs `scripts/validate_product_definition.py`, which checks PR body sections, validates referenced docs, and enforces that implementation changes in `scripts/`, `skills/`, `templates/`, or `.github/` are paired with spec/strategy/design/decision changes.
3. CI passes only when governance and documentation relationships remain aligned with repository rules.

**Progress Reporting:**

1. `.github/workflows/update-progress-report.yml` invokes `meta/progress/build_progress_report.py` with `meta/progress/progress-map.yaml`.
2. The script queries file existence and GitHub issue/PR state, computes weighted progress, and generates `meta/progress/progress.json` and `meta/progress/progress.md`.
3. The workflow compares generated outputs against the current branch and commits refreshed progress artifacts when meaningful changes are detected.

**State Management:**
- Source-of-truth state is file-based rather than service-based: canonical intent lives in `docs/`, durable decisions live in `records/`, runtime configuration lives in `reprogate.yaml`, and generated adapter or progress outputs are materialized back into the repository.
- Local runtime/session state is intentionally separated into hidden directories like `.omc/` and `.omx/`, which `docs/portability/ai-tool-artifact-boundary.md` classifies as local runtime rather than framework truth.

## Key Abstractions

**Work Record:**
- Purpose: Represent inspectable evidence of intent, decision, scope, or verification.
- Examples: `records/adr/ADR-001-config-schema.md`, `records/adr/ADR-007-uv-toolchain-adoption.md`, `records/rfc/RFC-003-product-boundary.md`
- Pattern: Markdown documents with YAML frontmatter plus named sections parsed by `scripts/gatekeeper.py`.

**Skill:**
- Purpose: Represent a reusable working rule that can later be enforced.
- Examples: `skills/record-required/guidelines.md`, `skills/decision-documented/guidelines.md`, `skills/scope-defined/guidelines.md`, `skills/verification-present/guidelines.md`
- Pattern: Folder-per-skill with `guidelines.md`; rule-engine expansion is planned in docs but current implementation checks skill folder names and guideline presence.

**Portable Framework Asset:**
- Purpose: Represent reusable content that should be copied into target repositories.
- Examples: `docs/`, `scripts/`, `skills/`, `templates/`
- Pattern: `scripts/generate.py` iterates these trees from `FRAMEWORK_DIRECTORIES` and copies them verbatim to the target output root.

**Adapter Surface:**
- Purpose: Bridge the framework into a tool-specific interaction model.
- Examples: `AGENTS.md`, `WORKSPACE-PROFILE.md`, `.claude/settings.json`, `.github/copilot-instructions.md`, `.codex/README.md`
- Pattern: Small entrypoint files that reference framework docs/scripts and keep project-specific guidance outside the core framework boundary.

**Generated Project Scaffold:**
- Purpose: Materialize repository-specific records and operational files from templates.
- Examples: `templates/project-ops/README.md.j2`, `templates/project-ops/CHANGELOG.md.j2`, `templates/project-ops/adr/README.md.j2`, `templates/project-ops/work-packets/index.md.j2`
- Pattern: Jinja-style placeholder replacement implemented by `render_template()` in both `scripts/init.py` and `scripts/generate.py`.

**Progress Stage Map:**
- Purpose: Define measurable roadmap progress outside the core product-definition layers.
- Examples: `meta/progress/progress-map.yaml`, `meta/progress/progress.md`, `meta/progress/progress.json`
- Pattern: Weighted configuration items resolved by `meta/progress/build_progress_report.py` into generated reports.

## Entry Points

**Repository Overview Entry Point:**
- Location: `README.md`
- Triggers: Human readers, new contributors, and generated-adapter users landing in the repository.
- Responsibilities: Explain ReproGate identity, list core scripts, and point readers to canonical docs and quick-start commands.

**CLI Dispatcher:**
- Location: `scripts/cli.py`
- Triggers: Direct shell invocation via `python3 scripts/cli.py <command>`.
- Responsibilities: Dispatch `init`, `generate`, `check`, `search`, `search-content`, and `print` subcommands to underlying scripts.

**Bootstrap Config Generator:**
- Location: `scripts/init.py`
- Triggers: `python3 scripts/init.py ...`
- Responsibilities: Create `reprogate.yaml` from `templates/reprogate.yaml.j2`, apply defaults, and refuse overwrites unless `--force` is supplied.

**Framework/Adapter Generator:**
- Location: `scripts/generate.py`
- Triggers: `python3 scripts/generate.py --config ... --output-root ...`
- Responsibilities: Load config, copy framework directories, and render adapter plus project-ops files into a target repository.

**Gatekeeper:**
- Location: `scripts/gatekeeper.py`
- Triggers: Direct execution, future CI/hook use, and adapter-driven checks.
- Responsibilities: Load config, inspect records and skills, and emit pass/fail messages based on artifact requirements.

**Tool Guard Hook:**
- Location: `scripts/hooks/claude_pretooluse_guard.py`
- Triggers: Claude pre-tool-use hook payloads and wrapper scripts installed into `.claude/hooks/`.
- Responsibilities: Enforce process restrictions, read-only shell policies, and TDD-before-implementation checks before allowing tool execution.

**PR Governance Validator:**
- Location: `scripts/validate_product_definition.py`
- Triggers: `.github/workflows/product-definition-ci.yml`
- Responsibilities: Enforce PR-body completeness, changed-file relationships, and scenario/document consistency rules.

**Progress Builder:**
- Location: `meta/progress/build_progress_report.py`
- Triggers: `.github/workflows/update-progress-report.yml` and manual CLI execution.
- Responsibilities: Read stage map config, query file/GitHub state, and render generated progress artifacts.

## Error Handling

**Strategy:** Fail fast with process exit codes and human-readable console output.

**Patterns:**
- Scripts that mutate repository state use explicit overwrite guards and return non-zero codes on refusal, as shown in `scripts/init.py` and `scripts/generate.py`.
- Validation-style scripts accumulate errors before exiting, as shown in `scripts/gatekeeper.py` and `scripts/validate_product_definition.py`, so callers receive a complete list of actionable failures.
- Search and metadata utilities prefer permissive behavior for missing or unreadable files; `scripts/search_docs.py` skips unreadable docs and `meta/progress/build_progress_report.py` degrades to `"not_found"` or partial scores when GitHub state is unavailable.

## Cross-Cutting Concerns

**Logging:** Console print output is the standard observability surface across `scripts/init.py`, `scripts/generate.py`, `scripts/gatekeeper.py`, `scripts/validate_product_definition.py`, and `meta/progress/build_progress_report.py`.
**Validation:** Structural validation is distributed across `scripts/gatekeeper.py` for records/skills, `scripts/validate_product_definition.py` for PR/document workflow, and `scripts/hooks/claude_pretooluse_guard.py` for tool-time restrictions.
**Authentication:** GitHub API access is isolated to `meta/progress/build_progress_report.py`, which reads `GITHUB_TOKEN` when available and otherwise falls back to `gh`; no application-level auth subsystem is implemented in repository code.

---

*Architecture analysis: 2026-03-24*
