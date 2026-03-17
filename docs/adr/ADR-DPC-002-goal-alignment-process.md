# ADR-DPC-002: 목표 점검 프로세스(G0) 신설 및 프로세스 카탈로그 확장

## Status

**Accepted** (2026-03-07)

> Note (2026-03-08): Team 활성화 정책은 [ADR-DPC-003](./ADR-DPC-003-conditional-team-activation-and-optout.md)로 부분 개정되었다.

## Context

### 배경

ai-collaboration-guide.md는 프로젝트의 모든 작업을 "프로세스 단위로 관리"하고 "계획 → 실행 → 검토 → 기록" 흐름을 따르도록 정의한다.

그러나 현재 프로세스 카탈로그(P0~P4, S1~S4)에는 **목표 정합성 점검** 프로세스가 없다.

### 발견된 문제

1. 세션 중간에 목표 drift가 발생해도 감지할 프로세스가 없음
2. master-plan의 "망각 방지 규칙"이 있지만 프로세스 카탈로그와 분리되어 있음
3. 목표 점검이 프로세스화되지 않아 WP/ADR로 기록되지 않음
4. ai-collaboration-guide.md 분해 시 이 gap이 그대로 이관될 위험

### 근거 원칙

> **ai-collaboration-guide.md Section 8.5**
> "각 프로세스는 가능한 후속 프로세스를 명시하고, 단독 수행으로 끝내지 않는다."

> **ops-bootstrap-master-plan.md North Star #3**
> "ai-collaboration-guide.md 의존도를 단계적으로 줄이고 분해 가능한 구조로 전환한다."

분해하면서 기존 gap을 그대로 이관하는 것은 North Star 위반이다.

## Decision

### 1. G0 프로세스 신설

프로세스 카탈로그에 **G0 (Goal Alignment Check)** 프로세스를 추가한다.

```
G0: 목표 정합성 점검
- 목적: 현재 작업이 상위 목표(North Star, Phase, Track)와 정합하는지 검증
- 시점: 세션 시작, 세션 중간(Phase/Track 전환 시), 마일스톤 완료 시
- 산출물: 정합성 점검 결과, gap 목록, 보정 조치 권고
- 후속: 보정 필요 시 WP 생성/갱신 또는 ADR 작성
```

### 2. G0 실행 시점

| 시점 | 트리거 | 필수 여부 |
|------|--------|----------|
| 세션 시작 | 첫 작업 전 | 필수 |
| Phase/Track 전환 | WP 상태 전이 시 | 필수 |
| 세션 중간 | 사용자 요청 또는 1시간 경과 | 권장 |
| 마일스톤 완료 | Phase Gate 통과 전 | 필수 |

### 3. G0 필수 점검 항목

1. 현재 작업이 어떤 North Star와 연결되는가?
2. 현재 Phase/Gate 위치는 어디인가?
3. 진행 중인 WP가 상위 목표에서 drift하지 않았는가?
4. 누락된 Track/WP가 있는가?
5. 계획에 없는 작업이 암묵적으로 진행되고 있지 않은가?

### 4. G0 산출물

- 점검 결과 요약 (정합/불일치)
- 불일치 시 gap 목록
- 보정 조치 권고 (WP 생성, ADR 작성, master-plan 갱신 등)
- WP Execution Notes 또는 Review Notes에 기록

### 5. 프로세스 카탈로그 구조 확장

기존:
```
P0~P4: 핵심 프로세스
S1~S4: 보조 프로세스
```

확장:
```
G0: 목표 정합성 점검 (신설)
P0~P4: 핵심 프로세스
S1~S4: 보조 프로세스
```

### 6. 핵심 강제 메커니즘 (실패 방지)

프로세스 보장을 위해 4개 지점에서 강제한다.

| # | 강제 지점 | 방지하는 실패 | 구현 |
|---|----------|--------------|------|
| ① | G0 (세션 시작) | WP 없이 작업, 목표 drift | **Claude Team Verifier** |
| ② | 상태 전이 검증 | 불법 전이 (DRAFT→DONE) | **Claude Team Verifier** |
| ③ | 완료 전 검증 | 산출물/후속 누락 | **Claude Team Verifier** |
| ④ | 커밋 검증 | 문서 정합성 | Git hooks, compliance check |

### 6.4 Claude Team 강제 구성

AI Ops 작업은 반드시 Team 구성(Executor + Verifier)으로 진행한다.

| 역할 | 책임 |
|------|------|
| Executor | 실제 작업 수행 |
| Verifier | G0, 상태 전이, 완료 전 검증 (①②③ 담당) |

**단독 작업 금지**. Verifier 없이 작업을 완료하면 안 된다.

### 6.1 G0 확장: 작업 대상 WP 확인

G0 점검에 다음을 추가한다:
- 이번 세션의 작업 대상 WP가 존재하는가?
- 해당 WP의 현재 상태(status, current_process)가 무엇인가?
- WP 없이 AI Ops 작업을 진행하려 하지 않는가?

### 6.2 상태 전이 규칙

금지된 전이:
- `DRAFT` → `DONE` (불법)
- `READY` → `DONE` (불법)
- `IN_DEVELOPMENT` → `DONE` (최소 S4 필요)

프로세스 스킵 시 `Execution Notes`에 스킵 이유 기록 필수.

### 6.3 완료 전 검증 (DONE 전이 조건)

1. Done Criteria 모든 항목 체크
2. next_process가 "종료"이거나 후속 WP 생성
3. Deliverables에 명시된 산출물 존재

**핵심 원칙**: 점검 결과가 "이상 없음"이어도 점검 자체는 반드시 수행한다. 스킵 불가.

### 7. ai-collaboration-guide.md 분해 시 반영

Phase 2 (WP-004)에서 ai-collaboration-guide.md를 분해할 때:
1. G0 프로세스를 프로세스 카탈로그에 포함
2. 목표 점검 체크리스트를 독립 문서로 분리
3. master-plan "망각 방지 규칙"과 G0 프로세스를 연결

## Consequences

### 긍정적

- 목표 drift가 프로세스 수준에서 감지됨
- 점검 결과가 WP/ADR로 기록되어 추적 가능
- ai-collaboration-guide.md 분해 시 gap 없이 이관 가능
- "프로세스 중심 운영" 원칙이 목표 점검에도 적용됨

### 부정적

- 점검 오버헤드가 추가됨
- 세션 시작 시 읽어야 할 문서가 늘어남
- 프로세스 카탈로그 복잡도 증가

### 완화 조치

- G0는 간소화된 체크리스트 기반으로 수행
- 자동화 가능한 부분(compliance check)은 스크립트로 보조
- 세션 시작 시 필수 읽기는 3개(constitution, master-plan, index) 유지

## Related

- [AI Ops Constitution](../governance/constitution.md)
- [ops-bootstrap-master-plan.md](../governance/ops-bootstrap-master-plan.md)
- [ai-collaboration-guide.md](../ai-collaboration-guide.md)
- [ADR-DPC-001](./ADR-DPC-001-bootstrap-requirement-change-sync.md)
- [WP-DPC-2026-03-004](../work-packets/WP-DPC-2026-03-004-document-structure-transition.md) (예정)
