# Codebase Structure

**Analysis Date:** 2026-03-24

## Directory Layout

```text
reprogate/
├── docs/                  # Canonical strategy, spec, design, governance, and portability documents
├── scripts/               # Python and shell entrypoints for bootstrap, generation, validation, search, and hooks
├── skills/                # Reusable rule/guideline units enforced by gate logic
├── templates/             # Template sources rendered into generated adapter and project-ops files
├── records/               # ADR and RFC decision history
├── meta/progress/         # Progress-report generator plus generated progress artifacts
├── .github/               # GitHub automation, issue/PR templates, Copilot instructions, and GSD assets
├── .claude/               # Claude adapter assets and vendored GSD command set
├── .codex/                # Codex adapter assets and vendored GSD command set
├── .gemini/               # Gemini adapter assets present in the working tree
├── .planning/             # Planning state plus generated codebase maps for orchestration
├── .omc/                  # Local runtime memory/state for OMC-style tooling
├── .omx/                  # Local runtime state, plans, and HUD/session files
├── config/                # Reserved config directory; currently only `.gitkeep` is present
├── AGENTS.md              # Repository-level adapter instructions for AI tools
├── WORKSPACE-PROFILE.md   # Workspace identity, branch, and runtime notes
├── README.md              # Human-readable repository entrypoint
├── pyproject.toml         # Python project metadata and dependencies
├── reprogate.yaml         # Root runtime/config file consumed by scripts
└── uv.lock                # Locked Python dependency graph for `uv`
```

## Directory Purposes

**`docs/`:**
- Purpose: Hold canonical product-definition content and repository policy.
- Contains: Strategy docs in `docs/strategy/`, contract docs in `docs/spec/`, concrete design docs in `docs/design/`, governance docs in `docs/governance/`, and portability notes in `docs/portability/`.
- Key files: `docs/strategy/final-definition.md`, `docs/strategy/product-boundary.md`, `docs/spec/product-surface-spec.md`, `docs/design/architecture.md`, `docs/governance/operating-model.md`, `docs/portability/ai-tool-artifact-boundary.md`

**`scripts/`:**
- Purpose: Hold executable repository tooling.
- Contains: Python command entrypoints, hook helpers, and tests under `scripts/tests/`.
- Key files: `scripts/cli.py`, `scripts/init.py`, `scripts/generate.py`, `scripts/gatekeeper.py`, `scripts/search_docs.py`, `scripts/validate_product_definition.py`, `scripts/hooks/claude_pretooluse_guard.py`

**`skills/`:**
- Purpose: Hold reusable working rules that gate logic can inspect.
- Contains: One directory per skill with at least `guidelines.md`.
- Key files: `skills/record-required/guidelines.md`, `skills/decision-documented/guidelines.md`, `skills/scope-defined/guidelines.md`, `skills/verification-present/guidelines.md`

**`templates/`:**
- Purpose: Hold reusable text templates used for bootstrapping target repositories.
- Contains: Root-level templates and tool/project-specific subdirectories.
- Key files: `templates/reprogate.yaml.j2`, `templates/AGENTS.md.j2`, `templates/WORKSPACE-PROFILE.md.j2`, `templates/project-ops/CHANGELOG.md.j2`, `templates/project-ops/work-packets/index.md.j2`, `templates/claude/settings.json.j2`

**`records/`:**
- Purpose: Hold durable decision and proposal history.
- Contains: `records/adr/` for accepted or proposed architecture decisions and `records/rfc/` for broader proposals.
- Key files: `records/adr/ADR-001-config-schema.md`, `records/adr/ADR-007-uv-toolchain-adoption.md`, `records/rfc/RFC-003-product-boundary.md`

**`meta/progress/`:**
- Purpose: Isolate progress-report generation from the product-definition layers.
- Contains: Generator script, YAML config, and generated JSON/Markdown outputs.
- Key files: `meta/progress/build_progress_report.py`, `meta/progress/progress-map.yaml`, `meta/progress/progress.md`, `meta/progress/progress.json`

**`.github/`:**
- Purpose: Own repository automation and GitHub-facing policy assets.
- Contains: Workflows in `.github/workflows/`, issue templates in `.github/ISSUE_TEMPLATE/`, PR template in `.github/PULL_REQUEST_TEMPLATE.md`, Copilot guidance in `.github/copilot-instructions.md`, and vendored GSD adapters in `.github/agents/`, `.github/skills/`, and `.github/get-shit-done/`.
- Key files: `.github/workflows/product-definition-ci.yml`, `.github/workflows/update-progress-report.yml`, `.github/CODEOWNERS`, `.github/copilot-instructions.md`

**`.claude/`:**
- Purpose: Hold Claude-specific adapter assets and a vendored command framework.
- Contains: Agent prompts, command definitions, hook wrapper files, and `get-shit-done` content.
- Key files: `.claude/settings.json`, `.claude/package.json`, `.claude/agents/gsd-codebase-mapper.md`

**`.codex/`:**
- Purpose: Hold Codex-specific adapter assets and skill packs.
- Contains: Agent definitions, TOML config, skills, and vendored `get-shit-done` content.
- Key files: `.codex/config.toml`, `.codex/agents/gsd-codebase-mapper.md`, `.codex/agents/gsd-codebase-mapper.toml`

**`.gemini/`:**
- Purpose: Hold Gemini-specific adapter assets present in the current working tree.
- Contains: Agent definitions, settings, package metadata, and vendored `get-shit-done` content.
- Key files: `.gemini/settings.json`, `.gemini/package.json`, `.gemini/agents/gsd-codebase-mapper.md`

**`.planning/`:**
- Purpose: Hold planning state and generated analysis artifacts for orchestration.
- Contains: Planning summaries, requirements, research docs, and codebase maps.
- Key files: `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/STATE.md`, `.planning/research/ARCHITECTURE.md`, `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/STRUCTURE.md`

**`.omc/` and `.omx/`:**
- Purpose: Hold local runtime/session state and tool-generated memory.
- Contains: Session JSON files, state files, plans, HUD metrics, and local notes.
- Key files: `.omc/project-memory.json`, `.omc/state/mission-state.json`, `.omx/state/session.json`, `.omx/metrics.json`

**`config/`:**
- Purpose: Reserved configuration directory.
- Contains: Only `.gitkeep` in the current working tree.
- Key files: `config/.gitkeep`

## Key File Locations

**Entry Points:**
- `README.md`: Main human entrypoint and quick-start guide.
- `scripts/cli.py`: Command multiplexer for `init`, `generate`, `check`, and search subcommands.
- `scripts/init.py`: Root config bootstrap command.
- `scripts/generate.py`: Framework and adapter generation command.
- `scripts/gatekeeper.py`: Record/skill gate evaluation command.
- `scripts/search_docs.py`: Documentation search CLI.
- `scripts/validate_product_definition.py`: Pull-request workflow validator.
- `meta/progress/build_progress_report.py`: Progress report generator.

**Configuration:**
- `pyproject.toml`: Python project metadata and dependencies.
- `uv.lock`: Locked dependency graph for `uv`.
- `reprogate.yaml`: Runtime/project config consumed by `scripts/init.py`, `scripts/generate.py`, and `scripts/gatekeeper.py`.
- `.github/CODEOWNERS`: Ownership boundary for major directories.
- `.github/workflows/*.yml`: CI and automation configuration.
- `.planning/config.json`: Planning-system configuration.

**Core Logic:**
- `docs/strategy/`: Canonical product identity and roadmap.
- `docs/spec/`: Contracts that implementation should follow.
- `scripts/`: Executable logic that implements bootstrap, validation, and gate behavior.
- `skills/`: Reusable enforcement units consumed by `scripts/gatekeeper.py`.
- `templates/`: Generation sources consumed by `scripts/init.py` and `scripts/generate.py`.

**Testing:**
- `scripts/tests/`: Python `unittest`-based tests for bootstrap flow and hook logic.
- `.github/workflows/product-definition-ci.yml`: CI entrypoint for PR validation behavior.
- `.github/workflows/update-progress-report.yml`: CI entrypoint for generated progress reporting.

## Naming Conventions

**Files:**
- Strategy/spec/design/governance documents use lowercase kebab-case Markdown names, for example `docs/strategy/product-boundary.md` and `docs/spec/record-contract.md`.
- Decision records use uppercase prefixes plus zero-padded numeric IDs, for example `records/adr/ADR-001-config-schema.md` and `records/rfc/RFC-003-product-boundary.md`.
- Script files use snake_case Python names, for example `scripts/validate_product_definition.py` and `scripts/search_docs.py`.
- Template files mirror their generated targets and add `.j2`, for example `templates/AGENTS.md.j2` and `templates/claude/settings.json.j2`.
- Generated planning references in `.planning/codebase/` use uppercase document names such as `.planning/codebase/ARCHITECTURE.md`.

**Directories:**
- Documentation layers use semantic lowercase directory names: `docs/strategy/`, `docs/spec/`, `docs/design/`, `docs/governance/`, `docs/portability/`.
- Skills use lowercase slug directory names under `skills/`, for example `skills/record-required/`.
- Tool adapters are rooted under hidden vendor directories like `.claude/`, `.codex/`, `.gemini/`, and `.github/`.
- Test code for scripts lives in a nested `tests/` directory under the executable area: `scripts/tests/`.

## Where to Add New Code

**New Feature:**
- Primary code: Add new Python tooling under `scripts/` when the feature is executable behavior, or under `meta/progress/` when it belongs to progress reporting rather than the core framework.
- Tests: Add `unittest` coverage under `scripts/tests/` for script behavior, naming test files `test_<feature>.py`.

**New Component/Module:**
- Implementation: Put portable framework behavior in `scripts/`, reusable guidance in `skills/<skill-slug>/guidelines.md`, and generated-text sources in `templates/`.
- Design/spec docs: Add or update the governing contract in `docs/spec/` and the implementation description in `docs/design/` when behavior changes.
- Decisions: Add an ADR in `records/adr/` when the change introduces a durable technical decision.

**Utilities:**
- Shared helpers: Keep script-only helper functions in the closest existing Python entrypoint until a reusable module emerges; if extraction becomes necessary, place the helper module under `scripts/` beside the scripts that import it.
- Documentation lookup helpers: Extend `scripts/search_docs.py` for document search behavior instead of creating parallel search locations.

**Tool Adapter Changes:**
- Claude-specific behavior: Update `templates/claude/` for generated behavior and `.claude/` only when modifying repository-local or vendored adapter assets already committed here.
- Codex-specific behavior: Update `.codex/` for current-repository adapter assets and `templates/` when the change must be portable.
- GitHub automation: Put workflows in `.github/workflows/`, issue forms in `.github/ISSUE_TEMPLATE/`, and Copilot guidance in `.github/copilot-instructions.md`.

**Documentation Tasks:**
- Product identity or scope: `docs/strategy/`
- Contracts/specifications: `docs/spec/`
- Implementation shape: `docs/design/`
- Repository policy: `docs/governance/`
- Portability or boundary rules: `docs/portability/`

## Ownership Boundaries

**Framework-Owned Assets:**
- Purpose: Shared reusable ReproGate content intended for copying into other repositories.
- Location: `docs/`, `scripts/`, `skills/`, `templates/`
- Boundary rule: Keep these paths portable and repository-agnostic as required by `docs/portability/ai-tool-artifact-boundary.md`.
- Ownership: `.github/CODEOWNERS` assigns `@pureliture` to `/docs/`, `/scripts/`, `/skills/`, and `/templates/`.

**Project Adapter Assets:**
- Purpose: Repository-specific entry surfaces that connect tools to the framework.
- Location: `AGENTS.md`, `WORKSPACE-PROFILE.md`, `.claude/`, `.codex/`, `.github/`, `.gemini/`
- Boundary rule: Keep generated adapters traceable back to `reprogate.yaml` and template sources.
- Ownership: `.github/CODEOWNERS` assigns `@pureliture` to `/.github/`; `AGENTS.md` and `WORKSPACE-PROFILE.md` are root adapter files rendered from `templates/`.

**Local Runtime Assets:**
- Purpose: Session state and machine-local memory that should not be treated as the canonical product source.
- Location: `.omc/`, `.omx/`, local hook/state files referenced in `docs/portability/ai-tool-artifact-boundary.md`
- Boundary rule: Treat these directories as operational state, not as the durable architecture definition.

## Special Directories

**`.planning/codebase/`:**
- Purpose: Generated codebase reference documents consumed by orchestration commands.
- Generated: Yes
- Committed: Yes, when maintained as part of planning artifacts

**`.github/get-shit-done/`, `.claude/get-shit-done/`, `.codex/get-shit-done/`, `.gemini/get-shit-done/`:**
- Purpose: Vendored command/agent framework content for each AI tool surface.
- Generated: Effectively yes; they behave like copied framework payloads.
- Committed: Yes

**`meta/progress/`:**
- Purpose: Generated reporting subsystem isolated from core product-definition layers.
- Generated: Mixed; `build_progress_report.py` and `progress-map.yaml` are maintained source files, while `progress.md` and `progress.json` are generated outputs.
- Committed: Yes

**`config/`:**
- Purpose: Placeholder for future config assets.
- Generated: No
- Committed: Yes

**`.omc/` and `.omx/`:**
- Purpose: Tool runtime state and local operational memory.
- Generated: Yes
- Committed: Present in the current working tree; treat contents as runtime artifacts rather than framework source.

---

*Structure analysis: 2026-03-24*
