# `.specify/` Workspace

This directory contains **structured repository development workflow artifacts** for ReproGate.

## Purpose

`.specify/` provides a workspace for development workflow artifacts that are:
- **Not canonical** - working documents, not authoritative definitions
- **Transient** - may evolve or be removed as features complete
- **Process-focused** - supporting development workflow, not defining the product

## What `.specify/` Does NOT Contain

| Content Type | Canonical Location | Notes |
|--------------|-------------------|-------|
| Product definition | `docs/strategy`, `docs/spec`, `docs/design` | ReproGate product specs |
| Governance constitution | `docs/governance/constitution.md` | Repository governance |
| Decision history | `records/adr/`, `records/rfc/` | Durable decision evidence |

> **Important:** `.specify/` does NOT replace `docs/governance/constitution.md`.
> `records/` remains canonical and serves as dogfooding/self-application evidence.

## 3-Layer Separation

ReproGate maintains clear separation between three layers:

| Layer | Location | Content | Canonical |
|-------|----------|---------|-----------|
| Product Definition | `docs/strategy`, `docs/spec`, `docs/design` | ReproGate product definition | Yes |
| Self-Application Evidence | `records/` | Dogfooding evidence (ADR, RFC) | Yes |
| Dev Workflow Artifacts | `.specify/` | Structured workflow artifacts | No |

### Why This Separation Matters

- **`docs/**`: Defines what ReproGate IS as a product
- **`records/**`: Proves ReproGate applies its own framework (self-hosting)
- **`.specify/**`: Supports HOW we develop this repository

## Directory Structure

```
.specify/
├── README.md           # This file
└── specs/              # Feature specifications
    └── README.md       # Specs directory convention
```

## Feature Path Convention

Each feature under development follows this structure:

```
.specify/specs/<feature-slug>/
├── spec.md     # Feature specification
├── plan.md     # Implementation plan
└── tasks.md    # Task breakdown
```

## Relationship with `records/`

- `.specify/specs/` contains **pre-implementation and in-progress** specifications
- When a spec requires **durable decision evidence**, reference or create entries in `records/*`
- After completion, **architectural decisions** are recorded in `records/adr/`
- `records/` is canonical; `.specify/` is not
