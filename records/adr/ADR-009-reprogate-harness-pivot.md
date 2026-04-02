---
record_id: "ADR-009"
title: "ReproGate product pivot to a Claude Code-centered delivery harness"
type: "adr"
status: "Draft"
created_at: "2026-04-02"
tags: ["pivot", "product", "harness", "claude-code", "strategy"]
---

# ADR-009: ReproGate product pivot to a Claude Code-centered delivery harness

## Status
Draft

## Context
ReproGate의 현재 전략 문서와 planning artifacts는 제품을 **artifact-driven compiler/gatekeeper**로 정의하고 있다. 이 framing 아래에서 현재 roadmap은 repository governance, Claude Code workflow integration, HUD 순으로 확장되는 구조다.

하지만 2026-04-02 피벗 노트(`.github/notes/2026-04-02-reprogate-harness-ecc-gsd.md`)는 더 이상 이 제품을 단순한 방법론 컴파일러로 보지 않는다. 새 방향은 다음과 같다.

- ReproGate를 **Claude Code 중심의 artifact-driven enterprise delivery harness**로 재정의한다.
- 하네스 운영 코어는 ECC 방식(hook lifecycle, state persistence, audit/gate, skill generation/evolution)을 채용한다.
- workflow와 phase 흐름은 GSD 방식(discuss -> plan -> execute -> verify, phase artifact packet, thin orchestrator + specialist agents)을 채용한다.
- OMC는 현재 참조 범위에서 제외한다.
- 사용자 표면은 단순한 상위 명령으로 유지하되, 내부 구현은 primitive operations로 안전하게 분해한다.

이 변화는 기존 milestone의 다음 기능 추가가 아니라, **제품 정체성, 경계, 로드맵 분해 방식** 자체를 바꾸는 피벗이다. 따라서 기존 `.planning/PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`의 연속성을 그대로 유지하면 traceability가 손상된다.

## Decision
We will treat the 2026-04-02 direction change as a product pivot and redefine ReproGate as a **Claude Code-centered, artifact-driven enterprise delivery harness**.

This pivot fixes the following product shape:

1. **Harness core:** adopt ECC-style operating primitives for hook lifecycle, state persistence, audit/gate surfaces, and skill generation/evolution.
2. **Phase workflow:** adopt GSD-style discuss -> plan -> execute -> verify flow with explicit phase artifact packets and specialist-agent routing.
3. **Artifact lifecycle:** extend ReproGate with product-specific enterprise artifact lifecycle coverage, including report/share and operate/maintain surfaces.
4. **User surface:** keep simple top-level commands while decomposing execution into safer internal primitive operations.
5. **Scope exclusion:** exclude OMC from the current reference set unless a later decision record reintroduces it.

Operationally, this decision means:

- the current milestone roadmap should be treated as **superseded planning**, not as the active product roadmap,
- surviving technical assets from completed work may be retained,
- strategy documents must be rewritten to match the new identity before a new planning cycle starts,
- the next planning cycle should start as a **new project initialization**, not as a normal next milestone.

## Consequences
- Positive: The product definition matches the intended user-facing outcome instead of forcing the harness concept into the old compiler/gatekeeper framing.
- Positive: ECC and GSD are incorporated intentionally at the architecture level rather than leaking in ad hoc through implementation choices.
- Positive: Future roadmap decomposition can align to harness core, workflow surfaces, and enterprise lifecycle stages.
- Neutral: Existing completed Phase 1 governance work remains useful as technical substrate, but its product framing must be reclassified.
- Negative: Current `.planning/PROJECT.md`, `REQUIREMENTS.md`, and `ROADMAP.md` can no longer be treated as the authoritative forward plan.
- Negative: Pivot follow-through now requires synchronized updates to strategy docs, planning artifacts, and milestone history before normal execution resumes.

## Verification
- [x] The pivot note is captured in a durable decision record.
- [x] The decision explicitly states why the existing milestone continuity is no longer sufficient.
- [ ] `docs/strategy/final-definition.md` is updated to reflect the harness-centered identity.
- [ ] `docs/strategy/vision.md`, `docs/strategy/roadmap.md`, and `docs/strategy/product-boundary.md` are updated to align with the new identity.
- [ ] `docs/strategy/scenarios.md` is updated if the product boundary changes user flows materially.
- [ ] Existing milestone/planning artifacts are archived, superseded, or reset in a traceable way.
- [ ] A new project planning cycle is initialized from the new strategy baseline.
