# ReproGate

> **ECC 코어 + GSD 플로우로 구성된 Claude Code 중심의 artifact-driven delivery harness**

ReproGate는 ECC(Everything-Claude-Code) 방식의 hook/skill 코어와 GSD(Get-Shit-Done) 방식의 phase 워크플로우를 하나로 묶은 린 하네스다. 범용 프레임워크에서 필요한 것만 추려 1인 개발자에게 최적화된 형태로 재조합한다.

## Core Value

ECC와 GSD의 핵심 기제를 과부하 없이 조합해, 1인 개발자가 Claude Code 위에서 재현 가능하고 기록 기반의 AI 보조 개발을 할 수 있게 한다.

## Context

이 정의는 ADR-009(`records/adr/ADR-009-reprogate-harness-pivot.md`)를 기반으로 한다. 이전 milestone의 compiler/gatekeeper framing은 superseded 처리되었고, Phase 1의 기술 산출물(record 구조, gatekeeper 기반)은 기술 기반으로 유지하되 제품 정체성은 harness로 재정의한다.

**하네스 구조:**
- **Layer 1 — 하네스 코어 (ECC 방식)**: hook lifecycle, state persistence, audit/gate surface, skill generation/evolution
- **Layer 2 — Phase 플로우 (GSD 방식)**: discuss → plan → execute → verify, phase artifact packet, thin orchestrator + specialist agents
- **Layer 3 — ReproGate 고유**: enterprise artifact lifecycle — report/share, operate/maintain 표면
- **실행 환경**: Claude Code가 orchestrator, slash command로 다른 CLI를 sub-agent로 스폰 (토큰 효율화)
- **강제 정책**: ReproGate 활성화 시 command 레이어와 hook 레이어 모두 강제 적용; 비활성화는 명시적 조치 필요

## Requirements

### Validated

- ✓ **FOUND-01**: `reprogate` CLI 통합 진입점 (`scripts/cli.py`) — Phase 1에서 완성
- ✓ **FOUND-02**: 작업 기록(ADR/RFC) 생성·시퀀셜 ID 부여 — Phase 1에서 완성
- ✓ **FOUND-03**: OPA/Rego 기반 gatekeeper 검증 — Phase 1에서 완성
- ✓ **FOUND-04**: Skill 정책 구조 (`skills/*/rules.rego` + `guidelines.md`) — Phase 1에서 완성
- ✓ **FOUND-05**: pre-commit hook으로 gatekeeper 자동 실행 — Phase 1에서 완성

### Active

- [ ] **HOOK-01**: ECC 방식 hook lifecycle 구현 — pre/post-tool, session persistence hook
- [ ] **HOOK-02**: audit/gate surface — hook 트리거 기반 자동 gate 평가
- [ ] **SKILL-EVO-01**: skill generation/evolution — 세션에서 패턴 추출 → Skill 자동 초안 생성
- [ ] **PHASE-01**: GSD discuss→plan→execute→verify 플로우 — CC slash command 기반 진입
- [ ] **PHASE-02**: phase artifact packet — 각 phase의 계획·실행·검증 산출물을 하나의 단위로 묶기
- [ ] **AGENT-01**: thin orchestrator + specialist agent 라우팅 — CC가 orchestrator, 다른 CLI를 sub-agent로 스폰
- [ ] **LIFECYCLE-01**: report/share 표면 — 완료된 phase의 산출물 요약·공유
- [ ] **LIFECYCLE-02**: operate/maintain 표면 — 하네스 상태 점검·유지 명령

### Out of Scope

- OMC — 현재 참조 범위 제외 (ADR-009)
- 팀 단위 기능 (공유, 원격 정책 동기화) — v1은 1인 개발자 전용; 팀 확장은 이후 결정
- 무거운 서버 측 상태 추적 — 로컬·Git 기반 상태만 허용
- Textual HUD — 이전 milestone의 우선순위; harness 코어 완성 후 재검토

## Constraints

- **Runtime**: Claude Code가 primary orchestrator — 다른 런타임에서의 독립 실행은 v1 범위 외
- **Target user**: 1인 개발자 — 팀 기능은 out of scope
- **Activation model**: ReproGate 켜면 두 레이어 모두 강제; 해제는 명시적 비활성화 필요

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Compiler/gatekeeper → delivery harness | 제품 정체성이 실제 사용 방식(CC 중심 phase 워크플로우)과 불일치 — ADR-009 | — Pending |
| ECC 코어 채택 | hook lifecycle·skill evolution이 harness 운영에 필요한 기제를 이미 정의하고 있음 | — Pending |
| GSD 플로우 채택 | discuss→plan→execute→verify + phase artifact packet이 재현 가능한 작업 단위를 명확히 함 | — Pending |
| OMC 제외 | 현재 참조 범위 축소로 범위 명확화; 필요시 이후 ADR로 재도입 | — Pending |
| CC를 orchestrator로 고정 | 토큰 효율화를 위해 CC가 중심에서 다른 CLI를 sub-agent로 라우팅 | — Pending |

## Current Milestone: v1.0 ReproGate Delivery Harness

**Goal:** ECC 코어(hook lifecycle, skill evolution)와 GSD 플로우(discuss→plan→execute→verify)를 통합한 1인 개발자용 artifact-driven delivery harness 완성

**Target features:**
- 하네스 설치/활성화/비활성화 (INIT)
- Hook lifecycle — session, compact, tool-use, failure capture (HOOK)
- Skill evolution — observation → instinct → prose skill (SKILL-EVO)
- Phase workflow — CC slash command 기반 discuss/plan/execute/verify (PHASE)
- 전문 에이전트 MVP — executor, verifier, planner (AGENT)
- Artifact lifecycle — phase summary, harness health check (LIFECYCLE)

**Foundation (validated):** FOUND-01~05 — CLI, record creation, gatekeeper, skill policy, pre-commit hook

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-next`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-02 — milestone v1.0 harness pivot started*
