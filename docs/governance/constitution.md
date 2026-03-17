# ReproGate Constitution

> Document ID: `DPC-CONSTITUTION`
> Version: `1.0.0`
> Status: Active

## Purpose

This document defines the non-negotiable foundation of ReproGate.
Its goals and guardrails remain stable even when prompts, tools, or project contexts change.

Legacy goal IDs remain in the `DPC-*` form for continuity with existing work packets and decision records.

## Immutable Goals

### DPC-G1 Record-Backed Intent
Each unit of work should preserve its intent through explicit work records rather than relying on chat memory alone.

### DPC-G2 Dual Enforcement
Compliance should be enforced both during execution and at final artifact boundaries.

### DPC-G3 Traceability First
Major changes should remain traceable through work records, decision records, indexes, changelogs, and program-level plans.

### DPC-G4 Hook Lifecycle
Hooks are not one-time setup artifacts. They should evolve with the operating model.

### DPC-G5 Domain Separation
Framework assets and project-specific adapter assets must remain physically and conceptually separated.

## Non-Negotiable Rules

1. Goal changes require an explicit decision record rather than an informal prompt.
2. When a project uses work packets, each packet must include `goal_ids`.
3. If a rule depends on evidence, the corresponding work record or artifact must exist in an inspectable form.
4. Requirement changes must sync the relevant packet, index, changelog, decision record, and program plan before state transitions.
5. Enforcement gates fail closed.
6. Project-specific runtime, branch, and environment rules belong in adapter-owned documents, not in the core framework.

## Product / Governance Boundary

The product definition of ReproGate belongs in strategy documents led by `docs/strategy/final-definition.md`.

This constitution governs the framework's non-negotiable rules and the repository's traceability discipline. It is not the product vision document.

## Change Control

Update this constitution only when the supporting governance and strategy artifacts are updated together:

1. `docs/strategy/final-definition.md` when the core identity itself changes
2. Relevant decision records
3. Work-packet index or equivalent control board
4. Changelog
5. Program-level plan or operating roadmap
