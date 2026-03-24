# Architecture

**Analysis Date:** 2025-02-14

## Pattern Overview

**Overall:** Rule-based Repository Governance & Spec-driven Development

**Key Characteristics:**
- **Policy-as-Code:** Uses "Skills" (defined in `skills/`) to enforce repository standards via automated checks.
- **Documentation-First:** Architecture and product decisions are driven by a tiered documentation structure (`strategy` -> `spec` -> `design`).
- **Template-driven Scaffolding:** Uses a central configuration (`reprogate.yaml`) to generate project-specific adapters and agent configurations.

## Layers

**Documentation Layer:**
- Purpose: Defines the "what", "why", and "how" of the project through structured Markdown.
- Location: `docs/`
- Contains: Strategy, Specifications, and Design documents.
- Depends on: None.
- Used by: Developers and the `gatekeeper.py` for compliance checks.

**Governance Layer (Skills):**
- Purpose: Defines the rules and guidelines that the repository must follow.
- Location: `skills/`
- Contains: Rego policies (`rules.rego`) and human-readable `guidelines.md`.
- Depends on: OPA (Open Policy Agent) concepts.
- Used by: `scripts/gatekeeper.py`.

**Tooling Layer (Scripts):**
- Purpose: Provides the CLI and automation logic for the framework.
- Location: `scripts/`
- Contains: Python scripts for initialization, generation, and gatekeeping.
- Depends on: Python 3.10+, PyYAML.
- Used by: CI/CD pipelines, Git hooks, and developers via `cli.py`.

**Persistence Layer (Records):**
- Purpose: Stores the immutable history of architectural and product decisions.
- Location: `records/`
- Contains: ADRs (Architecture Decision Records) and RFCs (Request for Comments).
- Depends on: None.
- Used by: `scripts/gatekeeper.py` (to verify decisions are documented).

## Data Flow

**Configuration & Scaffolding:**

1. User modifies `reprogate.yaml` with project-specific settings.
2. `scripts/generate.py` reads the config and processes files in `templates/`.
3. Generated files (e.g., `AGENTS.md`, `.claude/` configs) are written to the repository root or subdirectories.

**Governance Gatekeeping:**

1. `scripts/gatekeeper.py` is triggered (manually, via Git hook, or CI).
2. It scans `records/` for mandatory documents (ADRs, RFCs).
3. It validates the presence and structure (frontmatter, sections) of these records against active "Skills" in `skills/`.
4. It outputs a PASS/FAIL status based on compliance.

## Key Abstractions

**Skill:**
- Purpose: A modular unit of governance or capability.
- Examples: `skills/record-required`, `skills/decision-documented`.
- Pattern: Strategy pattern for repository rules.

**Record:**
- Purpose: Formal documentation of a work item or decision.
- Examples: `records/adr/*.md`, `records/rfc/*.md`.
- Pattern: Immutable audit log.

**Template:**
- Purpose: Blueprint for project files.
- Examples: `templates/reprogate.yaml.j2`, `templates/claude/commands/`.
- Pattern: Jinja2-style placeholders (though currently using simple string replacement in `generate.py`).

## Entry Points

**CLI Dispatcher:**
- Location: `scripts/cli.py`
- Triggers: User execution (`python scripts/cli.py <command>`).
- Responsibilities: Routes commands to `init.py`, `generate.py`, `gatekeeper.py`, or `search_docs.py`.

**Gatekeeper:**
- Location: `scripts/gatekeeper.py`
- Triggers: Git `pre-commit` hooks or CI pipelines.
- Responsibilities: Validates repository state against active skills.

**Generator:**
- Location: `scripts/generate.py`
- Triggers: Post-config updates or `init` command.
- Responsibilities: Synchronizes project files with the `reprogate.yaml` definition.

## Error Handling

**Strategy:** Fail-fast gatekeeping.

**Patterns:**
- **Strict Mode:** `gatekeeper.py --strict` fails if any mandatory record or section is missing.
- **Validation Messages:** Clear console output with ❌ and ⚠️ emojis to indicate errors and warnings.

## Cross-Cutting Concerns

**Logging:** Standard console output (stdout/stderr).
**Validation:** Regex-based frontmatter and section parsing in `scripts/gatekeeper.py`.
**Authentication:** Not applicable (local repository tooling).

---

*Architecture analysis: 2025-02-14*
