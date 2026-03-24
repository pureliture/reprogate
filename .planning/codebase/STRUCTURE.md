# Codebase Structure

**Analysis Date:** 2025-02-14

## Directory Layout

```
reprogate/
├── .github/          # GitHub workflow and agent configurations
├── .claude/          # Anthropic Claude agent configurations
├── .gemini/          # Google Gemini agent configurations
├── .codex/           # Codex (IDE-integrated) agent configurations
├── config/           # Reserved for runtime configuration files
├── docs/             # Tiered documentation (Strategy, Spec, Design)
│   ├── design/       # Implementation structure and module design
│   ├── strategy/     # Vision, Roadmap, and Product Boundary
│   └── spec/         # Contracts, Object Models, and APIs
├── meta/             # Internal metadata for progress and rendering
├── records/          # Persistent history of decisions
│   ├── adr/          # Architecture Decision Records
│   └── rfc/          # Request for Comments
├── scripts/          # Core Python CLI and automation scripts
├── skills/           # Policy-as-code definitions (OPA/Rego)
├── templates/        # Jinja2 blueprints for scaffolding project files
└── reprogate.yaml    # Central configuration for the framework
```

## Directory Purposes

**scripts/:**
- Purpose: Logic for initialization, generation, and compliance.
- Contains: Python scripts, git hooks, and helper tools.
- Key files: `cli.py`, `gatekeeper.py`, `generate.py`.

**skills/:**
- Purpose: Enforceable rules for repository governance.
- Contains: Directories with `rules.rego` (OPA) and `guidelines.md`.
- Key files: `skills/decision-documented/rules.rego`.

**docs/:**
- Purpose: Multi-layered documentation for the product lifecycle.
- Contains: Strategy, Spec, and Design documents.
- Key files: `docs/STRUCTURE.md`, `docs/README.md`.

**records/:**
- Purpose: Immutable audit log of architecture and design decisions.
- Contains: Markdown files with YAML frontmatter.
- Key files: `records/adr/*.md`.

**templates/:**
- Purpose: Blueprint files used by `generate.py` to synchronize the repository state.
- Contains: Agent profiles (`AGENTS.md.j2`), configs, and project-ops templates.
- Key files: `templates/reprogate.yaml.j2`.

## Key File Locations

**Entry Points:**
- `scripts/cli.py`: Dispatcher for all CLI operations.
- `scripts/gatekeeper.py`: Primary script for pre-commit validation and compliance.

**Configuration:**
- `reprogate.yaml`: The single source of truth for project-specific framework settings.
- `pyproject.toml`: Python project metadata and dependencies.

**Core Logic:**
- `scripts/generate.py`: Renders templates based on configuration.
- `scripts/validate_product_definition.py`: Logic for verifying the product core.

**Testing:**
- `scripts/tests/`: Unit tests for the Python scripts.

## Naming Conventions

**Files:**
- [Python Scripts]: `snake_case.py` (e.g., `gatekeeper.py`)
- [Documentation]: `kebab-case.md` (e.g., `final-definition.md`)
- [Templates]: `UPPERCASE-SNAKE.md.j2` (e.g., `AGENTS.md.j2`)

**Directories:**
- [Standard]: `kebab-case` or `plural` (e.g., `records`, `scripts`)

## Where to Add New Code

**New Feature (Automation):**
- Primary code: `scripts/`
- Tests: `scripts/tests/`

**New Governance Rule:**
- Implementation: `skills/[skill-name]/rules.rego`
- Guidelines: `skills/[skill-name]/guidelines.md`

**New Project Blueprint:**
- Template: `templates/[target-path].j2`

**New Design Spec:**
- Location: `docs/spec/` or `docs/design/` depending on depth.

## Special Directories

**.planning/:**
- Purpose: Contains agent-generated plans and codebase mapping docs.
- Generated: Yes.
- Committed: Yes.

**meta/:**
- Purpose: Holds state or metadata for internal framework rendering/progress tracking.
- Generated: Yes.
- Committed: No (typically ignored or selectively committed).

---

*Structure analysis: 2025-02-14*
