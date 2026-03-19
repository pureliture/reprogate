# SDD Workflow Labels (Phase 1)

This document defines the GitHub labels used for SDD (Spec-Driven Development) workflow routing in Phase 1.

## Label Definitions

### `sdd-exempt`

**Definition**: This PR is out-of-scope for SDD guardrails.

**Use when**:
- Typo-only documentation edits
- Generated progress/report refreshes with no logic changes
- Formatting-only updates
- Metadata-only updates with no workflow or logic impact
- Changes that do not affect repository operating behavior, validation behavior, or enforcement expectations

**What it means**:
- No `.specify/` artifact linkage is required
- No `records/*` evidence is required
- The change is considered trivial or out-of-scope by nature

### `reprogate-waiver`

**Definition**: This PR is in-scope for SDD guardrails but uses an alternate compliance path with recorded justification.

**Use when**:
- The change would normally require `.specify/` artifacts
- But there is a valid reason to deviate from the normal spec-first workflow
- A `records/*` reference (ADR, RFC, or other decision record) documents the deviation

**What it means**:
- Normal `.specify/` artifact linkage requirement is waived
- A `records/*` reference is required instead
- The deviation is intentional and documented

## Phase 1 Non-trivial Rules

The following changes are considered **non-trivial** by default and require SDD routing:
- `scripts/`
- `skills/`
- `templates/`
- `.github/`
- Governance, design, or documentation changes that affect repository operating behavior, validation behavior, or enforcement expectations

The following changes are **exempt candidates** by default:
- Typo-only docs edits
- Generated progress/report refreshes with no logic changes
- Formatting-only updates
- Metadata-only updates with no workflow or logic impact

**Note**: Changes to `.specify/` itself do not trigger SDD artifact requirements.

## Important Clarifications

### Labels are signals, not evidence
- Labels indicate routing intent
- Labels do NOT substitute for `records/*` evidence
- Waiver routing requires actual `records/*` references in the PR body

### Label creation is out-of-band
- Actual GitHub label creation is a manual operational setup task
- This document defines semantics; repository maintainers create labels separately

## Phase 1 Behavior

In Phase 1, the validator operates in **advisory mode**:
- Routing issues produce warnings, not failures
- Missing artifact linkage produces warnings, not failures
- Exit code remains 0 regardless of warnings

Hard enforcement policies will be established in future phases after operational experience.
