# ReproGate

> **AI 협업을 대화 기반 감각 작업에서 재현 가능한 엔지니어링 체계로**

ReproGate turns AI work from memory-dependent coding into reproducible engineering by making work records mandatory, accumulating durable Skills from those records, and enforcing them through gates (OPA/Rego).

## Core Value

ReproGate ensures that AI-assisted development remains rigorous and reproducible by centering the workflow around durable artifacts (Records and Skills) rather than ephemeral chat context.

## Context

ReproGate is designed as an **artifact-driven compiler/gatekeeper** and an **installable software framework** that can be ported directly into target projects. It addresses the "slop" and fragmentation in AI collaboration by enforcing a record-backed methodology.

## Requirements

### Validated

- ✓ **INIT-01**: Repository initialization via `scripts/init.py` and `reprogate.yaml` configuration.
- ✓ **GEN-01**: Adaptive file generation and framework porting via `scripts/generate.py` and Jinja2-style templates.
- ✓ **GATE-01**: Mandatory work record enforcement (ADRs, RFCs) via `scripts/gatekeeper.py`.
- ✓ **SKILL-01**: Skill-based policy checks using OPA/Rego and human-readable guidelines in `skills/`.
- ✓ **DOCS-01**: Documentation-first architecture with structured strategy, specification, and design docs in `docs/`.
- ✓ **CLI-01**: Unified CLI entry point via `scripts/cli.py` for all framework operations.

### Active

- [ ] **INTEG-01**: Enhanced integration with AI orchestrators (Claude, Codex, Gemini) via specialized agents.
- [ ] **SCALE-01**: Support for team-based standard sharing and remote policy synchronization.
- [ ] **AUTO-01**: Full automation of the GSD (Get Shit Done) workflow within the ReproGate framework.
- [ ] **UI-01**: Visual dashboard or HUD for real-time gate status and progress tracking.

### Out of Scope

- [ ] **STATE-01**: Heavy server-side state tracking (prioritize local, artifact-driven state).
- [ ] **EXEC-01**: Direct code execution outside of defined scripts/gates.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Artifact-driven vs State-driven | Reduces fragility and context dependency. | — Validated |
| OPA/Rego for Gates | Industry standard for policy-as-code. | — Validated |
| Python-based Tooling | High portability and accessibility for AI/Dev workflows. | — Validated |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-24 after initialization*
