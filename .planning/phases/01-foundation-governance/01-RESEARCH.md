# Phase 1: Foundation & Governance - Research

**Researched:** 2026-03-25
**Domain:** Python CLI tooling, OPA/Rego policy enforcement, YAML-based configuration, work record governance
**Confidence:** HIGH

## Summary

Phase 1 builds on a substantial existing codebase. The repository already has a working CLI (`scripts/cli.py`), repository initializer (`scripts/init.py`), framework generator (`scripts/generate.py`), and a gatekeeper (`scripts/gatekeeper.py` v0.2.0) that performs Python-native record inspection. Four Skills exist with both `guidelines.md` and `rules.rego` files. Seven ADRs and three RFCs populate the `records/` directory. The work record template is defined in `templates/records/WORK-RECORD-TEMPLATE.md`.

The primary gap is that the gatekeeper currently performs hardcoded Python checks rather than evaluating the `.rego` rule files. OPA is not installed on the development machine. The CLI still uses the legacy name "dpc" in its description and lacks a `create` subcommand for generating new work records. The `reprogate.yaml` schema is minimal and does not yet express the full Skill activation or gate configuration model described in governance docs.

**Primary recommendation:** Evolve the existing scripts rather than rewriting. Focus on (1) adding a `create` CLI command for record scaffolding, (2) strengthening the gatekeeper to either integrate OPA or provide a Python-native Rego-equivalent evaluation path, (3) making `reprogate.yaml` the single source of truth for Skill activation and gate behavior, and (4) renaming/rebranding CLI surfaces from "dpc" to "reprogate."

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Treat GSD as a reference input, not as the product architecture or authority model for ReproGate.
- **D-02:** Position ReproGate as a harness-agnostic governance layer; GSD, SDD/Kiro-style workflows, and freeform chat are ingress paths, not the core identity.
- **D-03:** Future workflow automation should be described generically rather than as GSD-bound product scope.
- **D-04:** GSD-style artifacts such as `CONTEXT.md`, `PLAN.md`, `SUMMARY.md`, and `STATE.md` are helper artifacts, not authoritative proof on their own.
- **D-05:** Official gate authority remains in ReproGate-owned records, Skills, rules, and explicit verification evidence.
- **D-06:** ReproGate must support both explicit workflow entry and workflow extraction from general conversation.
- **D-07:** Regardless of ingress, all paths must converge on the same evidence contract before implementation, merge, or release.
- **D-08:** The gatekeeper should fail closed on missing required evidence rather than treating workflow completion itself as success.
- **D-09:** The core CLI should remain ReproGate-native and harness-neutral.
- **D-10:** Workflow-specific command experiences should live in adapters or outer harness layers instead of redefining the core product around one harness's vocabulary.

### Claude's Discretion
- Exact naming and packaging of future harness adapters
- Canonical schema names for intent, scope, execution, and verification records
- Whether adapter translations are one-way or partially round-trippable, as long as governance truth remains ReproGate-owned

### Deferred Ideas (OUT OF SCOPE)
- Full adapter design for non-GSD harnesses belongs to later phases
- Exact Kiro/SDD adapter semantics belong outside Phase 1
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CORE-01 | Support mandatory work record creation (ADRs, RFCs) via CLI | Existing `templates/records/WORK-RECORD-TEMPLATE.md` provides scaffold. CLI needs a `create` subcommand. Frontmatter schema already defined (`record_id`, `type`, `status`). |
| CORE-02 | Enforce work record presence and structure via `scripts/gatekeeper.py` | Gatekeeper v0.2.0 already checks records, frontmatter, and sections. Needs strengthening: fail-closed behavior (D-08), configurable Skill activation from `reprogate.yaml`. |
| CORE-03 | Validate work records against "Skills" (OPA/Rego policies) in `skills/` | Four Skills with `.rego` files exist. OPA is NOT installed. Must decide: install OPA binary or build Python-native Rego evaluator. See Architecture section. |
| CORE-04 | Support repository initialization and framework porting via `scripts/init.py` and `scripts/generate.py` | Both scripts exist and work. `init.py` creates `reprogate.yaml`; `generate.py` copies framework tree and renders templates. May need schema evolution for new gate/skill config. |
| CORE-05 | Provide a unified CLI entry point via `scripts/cli.py` | CLI exists with commands: `init`, `generate`, `check`, `search`, `search-content`, `print`. Needs: `create` command, rename from "dpc" to "reprogate", add `gate`/`check` that invokes gatekeeper properly. |
</phase_requirements>

## Project Constraints (from CLAUDE.md)

- **Language:** Python 3.10+ for all core tooling
- **Shell:** Bash for Git hooks and installation scripts
- **Runtime:** uv as Python toolchain (`pyproject.toml` + `uv.lock`)
- **Testing:** pytest in `scripts/tests/`
- **Config:** `reprogate.yaml` in project root
- **Naming:** `snake_case.py`, `PascalCase` classes, `UPPER_CASE` constants
- **Style:** PEP 8, 4-space indentation, type hints
- **Error handling:** `try/except` for specific errors, non-zero exit codes, `sys.stderr` for errors
- **GSD Workflow:** Must use GSD entry points for changes, not direct edits

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| PyYAML | >=6.0 (in pyproject.toml) | YAML config and frontmatter parsing | Already a dependency; used by `generate.py` |
| requests | >=2.28 (in pyproject.toml) | HTTP requests | Already a dependency |
| argparse | stdlib | CLI argument parsing | Already used in all scripts |
| pathlib | stdlib | Path manipulation | Already used throughout |
| re | stdlib | Regex for frontmatter parsing | Already used in gatekeeper |
| shutil | stdlib | File copying for framework porting | Already used in generate.py |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest | latest | Test framework | For all `scripts/tests/` tests (needs adding to dev deps) |
| OPA binary | latest | Rego policy evaluation | If pursuing native OPA integration for CORE-03 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| OPA binary for Rego eval | Python-native rule evaluation (current approach in gatekeeper.py) | OPA is the standard for Rego but adds a binary dependency; Python-native is simpler to distribute but diverges from Rego syntax |
| Simple string template rendering | Jinja2 | Current `{{ key }}` replacement works for existing templates; Jinja2 adds power but also a dependency |

**Installation:**
```bash
uv add --dev pytest
```

## Architecture Patterns

### Current Project Structure
```
reprogate/
├── scripts/
│   ├── cli.py              # CLI entry point
│   ├── init.py             # Config bootstrap
│   ├── generate.py         # Framework porting/rendering
│   ├── gatekeeper.py       # Gate enforcement (v0.2.0)
│   ├── search_docs.py      # Document search
│   ├── check_compliance.py # (referenced in cli.py but missing on disk)
│   ├── hooks/              # Git hook scripts
│   └── tests/              # pytest tests
├── skills/
│   ├── record-required/    # guidelines.md + rules.rego
│   ├── decision-documented/
│   ├── scope-defined/
│   └── verification-present/
├── records/
│   ├── adr/                # 7 existing ADRs
│   └── rfc/                # 3 existing RFCs
├── templates/
│   ├── records/WORK-RECORD-TEMPLATE.md
│   ├── claude/             # Claude adapter templates
│   ├── codex/              # Codex adapter templates
│   └── project-ops/        # Operational doc templates
├── docs/
│   ├── strategy/           # Product definition
│   └── governance/         # Constitution, operating model
├── reprogate.yaml          # Central configuration
└── pyproject.toml          # Python project config
```

### Pattern 1: Skill as a Two-File Unit
**What:** Each Skill is a directory under `skills/` containing `guidelines.md` (human-readable intent + expectations) and `rules.rego` (machine-evaluable rules).
**When to use:** Every governance rule must follow this pattern.
**Example:** `skills/record-required/` already demonstrates this:
```
skills/record-required/
├── guidelines.md   # Frontmatter: skill_id, name, version, tags
└── rules.rego      # package reprogate.rules with deny/warn rules
```

### Pattern 2: Gate Evaluation as Artifact Inspection
**What:** The gatekeeper collects records from `records/`, collects skills from `skills/`, and evaluates deny/warn rules against the collected evidence.
**When to use:** Every gate check follows this collect-then-evaluate pattern.
**Key insight:** The current gatekeeper hardcodes rule logic in Python rather than evaluating `.rego` files. Phase 1 should either:
- (A) Implement a Python-native rule evaluator that reads `.rego` files, or
- (B) Shell out to the `opa` binary to evaluate `.rego` against JSON input

**Recommendation:** Start with option (A) since OPA is not installed and the current `.rego` rules are simple enough (deny/warn pattern with `count`, `not`, `sprintf`). Add OPA binary support as an optional enhancement. This keeps distribution simple (pure Python) while maintaining the `.rego` file format for future OPA compatibility.

### Pattern 3: CLI as a Thin Router
**What:** `cli.py` is a thin command dispatcher that delegates to individual scripts via `subprocess.run`.
**When to use:** All user-facing commands route through `cli.py`.
**Extension strategy:** Add new commands (e.g., `create`) by adding script files and routing entries. Do not put business logic in `cli.py` itself.

### Pattern 4: Config-Driven Behavior
**What:** `reprogate.yaml` controls which skills are active, where records live, and how gates behave.
**Current limitation:** The config schema is minimal (only `project_name`, `skills_dir`, `records_dir`, `gatekeeper` section). It needs expansion to control:
- Which skills are active/required vs optional
- Gate strictness per skill
- Record type definitions and their required sections

### Anti-Patterns to Avoid
- **Hardcoding rule logic in Python:** The current gatekeeper embeds rule semantics (e.g., "ADR must have Context, Decision, Consequences sections") directly. This should come from Skill definitions or `.rego` files.
- **Importing GSD vocabulary into the core CLI:** Per D-09 and D-10, the CLI must use ReproGate-native terminology, not GSD phase/plan/summary language.
- **Treating workflow completion as gate success:** Per D-08, gates must independently verify evidence regardless of workflow state.
- **Skipping `reprogate.yaml` for configuration:** All configurable behavior should be driven by the config file, not scattered across script defaults.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| YAML parsing | Custom line-by-line parser | PyYAML (`yaml.safe_load`) | `gatekeeper.py` currently does manual YAML parsing for config; `generate.py` already uses PyYAML. Unify on PyYAML. |
| Frontmatter extraction | Regex-based parser (current) | PyYAML after splitting `---` delimiters | Current regex approach works but PyYAML handles edge cases better (multiline values, complex types) |
| CLI argument parsing | Manual arg handling | argparse (already used) | Consistent with existing codebase |
| File template rendering | Custom replacement | Current `{{ key }}` approach is sufficient | Jinja2 is overkill for current needs |

**Key insight:** The gatekeeper (`gatekeeper.py`) has a custom YAML parser that reads `reprogate.yaml` line-by-line to avoid PyYAML dependency. But PyYAML is already a project dependency used by `generate.py`. The gatekeeper should simply use PyYAML too.

## Common Pitfalls

### Pitfall 1: Dual YAML Parsing Implementations
**What goes wrong:** `gatekeeper.py` uses a hand-rolled YAML parser while `generate.py` uses PyYAML. Behavior can diverge on edge cases.
**Why it happens:** The gatekeeper was written to avoid external dependencies, but PyYAML is already in `pyproject.toml`.
**How to avoid:** Unify on PyYAML across all scripts.
**Warning signs:** Config values parsed differently by gatekeeper vs generate.

### Pitfall 2: Missing `check_compliance.py`
**What goes wrong:** `cli.py` routes the `check` command to `check_compliance.py`, but this file does not exist on disk.
**Why it happens:** Likely renamed or removed without updating the CLI router.
**How to avoid:** Either create `check_compliance.py` or update `cli.py` to route to `gatekeeper.py` instead.
**Warning signs:** `reprogate check` fails with a file-not-found error.

### Pitfall 3: Legacy "dpc" Naming
**What goes wrong:** `cli.py` still describes itself as "dpc helper CLI." Users see inconsistent branding.
**Why it happens:** The project was renamed from DPC to ReproGate but not all references were updated.
**How to avoid:** Grep for "dpc" across the codebase and update to "reprogate."
**Warning signs:** Help text, comments, or variable names referencing "dpc."

### Pitfall 4: OPA Binary Dependency
**What goes wrong:** Phase claims Rego evaluation but OPA is not installed, making gate checks impossible.
**Why it happens:** OPA is listed as the engine in `reprogate.yaml` but never installed.
**How to avoid:** Either (A) make OPA optional with a Python-native fallback, or (B) install OPA as a documented prerequisite, or (C) implement a minimal Python Rego subset evaluator.
**Warning signs:** `gatekeeper.py` silently skips `.rego` files.

### Pitfall 5: Fail-Open vs Fail-Closed Gate Default
**What goes wrong:** Missing Skills or records cause warnings instead of errors, allowing non-compliant work through.
**Why it happens:** Current gatekeeper treats some missing items as warnings (e.g., no ADRs only warns for `decision-documented`).
**How to avoid:** Per D-08 and constitution rule 5, default to fail-closed. Make `--strict` the default or use `reprogate.yaml` `strict_mode: true`.
**Warning signs:** Gate passes when required evidence is absent.

## Code Examples

### Current Record Frontmatter Schema
```yaml
# Source: templates/records/WORK-RECORD-TEMPLATE.md
---
record_id: "WR-YYYYMMDD-001"
title: "Title"
status: "DRAFT"  # DRAFT, IN_PROGRESS, DONE
created_at: "YYYY-MM-DD"
---
```

### Current Skill Frontmatter Schema
```yaml
# Source: skills/record-required/guidelines.md
---
skill_id: "record-required"
name: "Name"
version: "0.1.0"
tags: ["core", "stage-0"]
---
```

### Current Rego Rule Pattern
```rego
# Source: skills/record-required/rules.rego
package reprogate.rules

import rego.v1

deny contains msg if {
    count(input.records) == 0
    msg := "Message explaining the failure."
}
```

### Proposed CLI `create` Command Pattern
```python
# Pattern for new record creation subcommand
def create_record(record_type: str, title: str, output_dir: pathlib.Path) -> pathlib.Path:
    """Create a new work record from template."""
    template = ROOT / "templates" / "records" / "WORK-RECORD-TEMPLATE.md"
    today = date.today().isoformat()
    record_id = f"WR-{today.replace('-', '')}-001"
    # ... render template with context, write to output_dir
```

### Proposed Gate Input JSON for Rego Evaluation
```json
{
  "records": [
    {
      "path": "records/adr/ADR-001-config-schema.md",
      "frontmatter": {
        "record_id": "ADR-001",
        "type": "adr",
        "status": "Accepted"
      },
      "sections": {
        "Context": true,
        "Decision": true,
        "Consequences": true
      }
    }
  ],
  "skills": ["record-required", "decision-documented"],
  "config": {
    "strict_mode": true
  }
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual YAML parsing in gatekeeper | PyYAML available as dependency | Already in pyproject.toml | Should unify all YAML parsing on PyYAML |
| "dpc" branding | "ReproGate" branding | Project identity established in docs/ | CLI and script references need updating |
| Hardcoded gate rules in Python | Rego rules exist in skills/ | rules.rego files written | Need bridge between .rego files and Python evaluator |

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | All scripts | Yes | 3.13.3 | -- |
| uv | Toolchain | Yes | 0.10.11 | pip3 |
| PyYAML | Config parsing | Yes | In pyproject.toml deps | -- |
| pytest | Testing | No (not in uv env) | -- | `uv add --dev pytest` to install |
| OPA | Rego evaluation (CORE-03) | No | -- | Python-native rule evaluation (recommended) |
| Git | Hooks, version control | Yes | System default | -- |

**Missing dependencies with no fallback:**
- None that block execution

**Missing dependencies with fallback:**
- **pytest:** Not currently in dev dependencies. Install with `uv add --dev pytest`.
- **OPA:** Not installed. Use Python-native rule evaluation as the primary path; support OPA as optional when available.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (needs installing via `uv add --dev pytest`) |
| Config file | None -- needs creation (Wave 0) |
| Quick run command | `uv run python3 -m pytest scripts/tests/ -x -q` |
| Full suite command | `uv run python3 -m pytest scripts/tests/ -v` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CORE-01 | CLI `create` generates valid ADR/RFC from template | unit | `uv run python3 -m pytest scripts/tests/test_record_creation.py -x` | No -- Wave 0 |
| CORE-02 | Gatekeeper blocks on missing/invalid records | unit | `uv run python3 -m pytest scripts/tests/test_gatekeeper.py -x` | No -- Wave 0 (test_tdd_gate.py exists but tests TDD gate, not record gate) |
| CORE-03 | Skills/rules evaluated against records | unit | `uv run python3 -m pytest scripts/tests/test_skill_evaluation.py -x` | No -- Wave 0 |
| CORE-04 | Init creates valid reprogate.yaml; generate renders templates | unit | `uv run python3 -m pytest scripts/tests/test_bootstrap_smoke.py -x` | Yes |
| CORE-05 | CLI routes all commands correctly | unit | `uv run python3 -m pytest scripts/tests/test_cli.py -x` | No -- Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run python3 -m pytest scripts/tests/ -x -q`
- **Per wave merge:** `uv run python3 -m pytest scripts/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `scripts/tests/test_record_creation.py` -- covers CORE-01
- [ ] `scripts/tests/test_gatekeeper.py` -- covers CORE-02 (record presence/structure enforcement)
- [ ] `scripts/tests/test_skill_evaluation.py` -- covers CORE-03 (Skill/rule evaluation)
- [ ] `scripts/tests/test_cli.py` -- covers CORE-05 (command routing, help text)
- [ ] Install pytest: `uv add --dev pytest`
- [ ] Fix missing `check_compliance.py` or update CLI routing

## Open Questions

1. **OPA Integration Depth**
   - What we know: `reprogate.yaml` declares `gatekeeper.engine: "opa"`. Four `.rego` files exist. OPA binary is not installed.
   - What's unclear: Should Phase 1 require OPA binary, or is Python-native evaluation acceptable?
   - Recommendation: Implement Python-native evaluation that reads `.rego` file patterns. Add OPA binary support as optional. This keeps distribution pure-Python while maintaining `.rego` as the rule format. Document as an ADR.

2. **Record Type Taxonomy**
   - What we know: Current types are `adr` and `rfc`. The template uses a generic `WR-` prefix.
   - What's unclear: Should Phase 1 define additional record types (e.g., work-record, verification-record)?
   - Recommendation: Keep `adr` and `rfc` for Phase 1. The `create` command should accept `--type adr|rfc` and use type-specific templates. Expansion is deferred.

3. **`check_compliance.py` Status**
   - What we know: `cli.py` references `check_compliance.py` for the `check` command, but the file does not exist on disk.
   - What's unclear: Was it renamed to `gatekeeper.py` or deleted?
   - Recommendation: Route the `check` command to `gatekeeper.py`. Remove or create `check_compliance.py`. The test file `test_yaml_parsing.py` imports from `check_compliance`, so this needs careful handling.

## Sources

### Primary (HIGH confidence)
- Direct codebase inspection of all scripts, skills, templates, records, and config files
- `docs/strategy/final-definition.md` -- ReproGate core identity
- `docs/governance/constitution.md` -- Non-negotiable rules (fail-closed, traceability)
- `docs/governance/operating-model.md` -- Record-backed engineering model
- `.planning/research/GSD-COMPARISON.md` -- GSD vs ReproGate comparison and integration guidance

### Secondary (MEDIUM confidence)
- OPA/Rego patterns from existing `.rego` files in `skills/` -- syntax verified against Rego v1 conventions

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all libraries are already in the codebase or are Python stdlib
- Architecture: HIGH -- patterns observed directly from existing code; evolution path is clear
- Pitfalls: HIGH -- all identified from direct codebase inspection (missing files, dual parsers, naming inconsistencies)

**Research date:** 2026-03-25
**Valid until:** 2026-04-25 (stable domain, no external API dependencies)
