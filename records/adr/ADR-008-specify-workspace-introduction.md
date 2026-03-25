---
record_id: "ADR-008"
title: ".specify/ workspace introduction"
type: "adr"
status: "Accepted"
created_at: "2026-03-19"
tags: ["workspace", "separation", "sdd", "stage-1"]
---

# ADR-008: .specify/ workspace introduction

## Status
Accepted

## Context
ReproGate is self-hosting: it applies its own framework to its own development (RFC-001). This creates a need to distinguish between:

1. **Product definition** - what ReproGate IS (`docs/`)
2. **Self-application evidence** - proof that ReproGate uses its own framework (`records/`)
3. **Development workflow artifacts** - supporting HOW we develop this repository

Without clear separation, there is risk of:
- Mixing canonical product specs with transient working documents
- Diluting the purpose of `records/` as dogfooding evidence
- Confusion about what constitutes authoritative documentation

## Decision
We introduce `.specify/` as a workspace for structured repository development workflow artifacts.

### 3-Layer Separation

| Layer | Location | Content | Canonical |
|-------|----------|---------|-----------|
| Product Definition | `docs/strategy`, `docs/spec`, `docs/design` | ReproGate product definition | Yes |
| Self-Application Evidence | `records/` | Dogfooding evidence (ADR, RFC) | Yes |
| Dev Workflow Artifacts | `.specify/` | Structured workflow artifacts | No |

### Feature Path Convention

```
.specify/specs/<feature-slug>/
├── spec.md     # Feature specification
├── plan.md     # Implementation plan
└── tasks.md    # Task breakdown
```

### Relationship with `records/`

- `.specify/specs/` contains pre-implementation and in-progress specifications
- When durable decision evidence is needed, reference or create `records/*` entries
- Architectural decisions are recorded in `records/adr/` after completion

## Consequences

### Positive
- Clear separation between canonical and non-canonical content
- `records/` role as dogfooding/self-application evidence is preserved and clarified
- Development workflow has a dedicated, inspectable location

### Neutral
- New convention requires documentation and learning
- Existing workflows continue unchanged; this adds rather than replaces

## Non-Goals

This decision explicitly does NOT:
- Replace `docs/governance/constitution.md` - it remains the governance constitution
- Move existing ADR/RFC history out of `records/`
- Replace any canonical layer (`docs/`, `records/`)
- Introduce CI hard enforcement or gatekeeper integration (future work)

## Verification
- [x] `.specify/README.md` exists with 3-layer separation guidance
- [x] `.specify/specs/README.md` exists with directory convention
- [x] `records/adr/ADR-008-specify-workspace-introduction.md` exists
- [x] `docs/**` unchanged
- [x] `records/**` has no changes except ADR-008
