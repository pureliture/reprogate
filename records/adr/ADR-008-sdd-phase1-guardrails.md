---
record_id: "ADR-008"
title: "SDD Phase 1 GitHub Guardrails"
type: "adr"
status: "Accepted"
created_at: "2026-03-19"
tags: ["sdd", "ci", "guardrails", "phase-1"]
---

# ADR-008: SDD Phase 1 GitHub Guardrails

## Status
Accepted

## Context
ReproGate는 `.specify` 기반 Spec-Driven Development(SDD) workflow를 도입하려 한다. 이를 GitHub surface에서 강제하기 위해 PR CI에 guardrail을 추가해야 한다.

Phase 1에서는 semantic adequacy 판단 없이 **presence / linkage / routing**만 검사한다. 이는 운영 경험을 축적한 후 Phase 2에서 hard enforcement로 전환하기 위한 준비 단계다.

## Decision
We will implement Phase 1 SDD guardrails with the following characteristics:

1. **Advisory Mode**: 모든 SDD 관련 검사는 warning만 출력하고 exit 0을 유지한다.
2. **Routing Taxonomy**: PR은 `in-scope`, `sdd-exempt`, `reprogate-waiver` 중 하나를 선택해야 한다.
3. **Presence Check**: `in-scope` 선택 시 `.specify/specs/<feature>/spec.md|plan.md|tasks.md` 경로 존재 여부를 확인한다.
4. **Waiver Path**: `reprogate-waiver` 선택 시 `records/*` 참조를 요구한다.
5. **Non-trivial Rule**: `scripts/`, `skills/`, `templates/`, `.github/` 변경은 기본적으로 non-trivial로 분류한다.
6. **Exempt Rule**: `.specify/` 자체 변경은 SDD artifact requirement를 trigger하지 않는다.

## Consequences
- 긍정: SDD workflow 도입의 첫 단계로 운영 경험 축적 가능
- 긍정: Advisory mode이므로 기존 workflow를 즉시 차단하지 않음
- 긍정: Routing taxonomy를 통해 명시적인 의도 표현 가능
- 중립: Semantic adequacy 판단은 #21에서 별도 구현 필요
- 중립: 실제 GitHub label 생성은 out-of-band operational setup

## Verification
- [x] PR template에 SDD Workflow 섹션 추가
- [x] `.specify/`가 CODEOWNERS에 포함
- [x] `.github/SDD-LABELS.md` 운영 문서 생성
- [x] validator가 routing / presence / linkage를 advisory mode로 검사
- [x] 8개 테스트 케이스 수동 검증 완료
