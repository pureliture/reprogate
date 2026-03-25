# Phase 1: Foundation & Governance - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in `01-CONTEXT.md` — this log preserves the alternatives considered.

**Date:** 2026-03-24
**Phase:** 01-foundation-governance
**Areas discussed:** GSD relationship, evidence authority, gate model, workflow ingress, CLI / architecture direction

---

## GSD relationship

| Option | Description | Selected |
|--------|-------------|----------|
| GSD as external orchestration layer, ReproGate as governance/gate engine | Use GSD directly as the outer workflow shell | |
| GSD as embedded workflow engine | Adopt GSD into the ReproGate product structure | |
| GSD compatibility target | Design around GSD artifact compatibility | |
| GSD as reference only | Use GSD as inspiration, not product structure | ✓ |

**User's choice:** GSD는 참고용 레퍼런스일 뿐, 제품 구조에는 직접 반영하지 않음
**Notes:** User wants freedom to use different harness engineering approaches over time rather than hard-binding ReproGate to one orchestrator.

---

## Workflow automation naming follow-up

| Option | Description | Selected |
|--------|-------------|----------|
| Generalize the Phase 3 name later | Remove explicit GSD branding from roadmap language | ✓ |
| Keep the GSD name but treat it as internal only | Retain the current label for convenience | |
| Decide later in Phase 3 | Leave the roadmap wording unchanged for now | |

**User's choice:** 예, GSD 이름을 빼고 일반적 workflow automation으로 정리
**Notes:** This was treated as a follow-up implication of the "reference only" decision and was applied by updating the planning docs after review.

---

## Evidence authority

| Option | Description | Selected |
|--------|-------------|----------|
| Helper-only artifacts | GSD artifacts help execution but do not become authoritative evidence | ✓ |
| Auxiliary evidence | Some GSD artifacts may support a gate, but are not final authority | |
| Official evidence | Properly structured GSD artifacts can count as gate-authoritative proof | |
| Leave open by phase | Decide evidence status later per phase | |

**User's choice:** 작업 보조 산출물로만 취급하고, 공식 증거는 ADR/RFC/Skill/rule 쪽에 둠
**Notes:** User wants enterprise-grade guarantees to remain anchored in ReproGate-owned evidence, not harness-local files.

---

## Gate model and workflow ingress

| Option | Description | Selected |
|--------|-------------|----------|
| Strong fail-closed gate with multiple ingress modes | Support forced workflow and conversation-derived workflow, but converge on the same evidence/gates | ✓ |
| Workflow-first validation | Follow a GSD-like procedural validation model | |
| Python structure checks first, stronger gating later | Keep Phase 1 mostly lightweight | |
| CI-only enforcement | Delay strong local enforcement | |

**User's choice:** 강제 workflow 진입 + 일반 대화 유도 진입 둘 다 지원하고, 동일한 증거/gate로 수렴
**Notes:** User explicitly raised the need to support both guided workflow use and general conversation that later derives a workflow. The conclusion was that this still points to a stronger fail-closed evidence layer rather than a weaker gate.

---

## CLI / architecture direction

| Option | Description | Selected |
|--------|-------------|----------|
| Harness-agnostic governance layer | ReproGate keeps a neutral core; GSD/SDD/chat become adapter ingress paths | ✓ |
| GSD-optimized v1 | Start more directly optimized for GSD and generalize later | |
| Keep evaluating | Do not lock the principle yet | |

**User's choice:** ReproGate는 harness-agnostic governance layer로 두고, GSD/SDD/chat은 adapter ingress로 취급
**Notes:** User described the target as an enterprise-grade decorating or layered harness that can preserve artifact guarantees even if the active workflow system changes in the future.

---

## the agent's Discretion

- Exact future command names for adapter-driven ingress
- Concrete canonical artifact schema names
- Adapter packaging and translation mechanics

## Deferred Ideas

- Design explicit non-GSD adapters in a later phase

---

*Phase: 01-foundation-governance*
*Discussion log generated: 2026-03-24*
