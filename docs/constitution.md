# AI Ops Constitution

> Document ID: `AIOPS-CONSTITUTION`
> Version: `1.0.0`
> Status: Active

## Purpose

This document defines the non-negotiable foundation of the AI Ops framework.
Its goals and guardrails remain stable even when prompts, tools, or project contexts change.

## Immutable Goals

### AIOPS-G1 Goal Stability
Each unit of work should preserve its higher-level intent while refining only the implementation details.

### AIOPS-G2 Dual Enforcement
Process compliance should be enforced both during execution and at final artifact boundaries.

### AIOPS-G3 Traceability First
Major changes should remain traceable through work packets, decision records, indexes, changelogs, and program-level plans.

### AIOPS-G4 Hook Lifecycle
Hooks are not one-time setup artifacts. They should evolve with the operating model.

### AIOPS-G5 Domain Separation
Framework assets and project-specific adapter assets must remain physically and conceptually separated.

## Non-Negotiable Rules

1. Goal changes require an explicit decision record rather than an informal prompt.
2. When a project uses work packets, each AI Ops packet must include `goal_ids`.
3. Requirement changes must sync the relevant packet, index, changelog, decision record, and program plan before state transitions.
4. Enforcement gates fail closed.
5. Project-specific runtime, branch, and environment rules belong in adapter-owned documents, not in the core framework.

## Change Control

Update this constitution only when the supporting governance artifacts are updated together:

1. Relevant decision records
2. Work-packet index or equivalent control board
3. Changelog
4. Program-level plan or operating roadmap
