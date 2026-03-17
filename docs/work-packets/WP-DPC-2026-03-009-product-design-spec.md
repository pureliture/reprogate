---
packet_id: "WP-DPC-2026-03-009"
title: "ReproGate 제품 설계 구체화"
goal_ids: ["DPC-G1"]
status: "DONE"
work_type: "DESIGN"
priority: "P0"
target_environment: "master"
start_process: "P0"
current_process: "P0"
next_process: "P1"
owner: "SHARED"
created_at: "2026-03-17"
last_updated: "2026-03-17"
parent: "WP-DPC-2026-03-001"
track: "reprogate core design"
---

# WP-DPC-2026-03-009: ReproGate 제품 설계 구체화

> Current interpretation: 이 WP는 legacy `dpc` 제품 설계 문서를 넘어, **ReproGate의 기록 기반 UX / Skill 축적 / Gate 강제**를 구현 가능한 수준으로 구체화한 설계 패킷이다.

## 1. Background

architecture.md, presets-spec.md, ADR-006/007, final-definition.md로 기본 개념과 구조는 정의되었으나,
실제 구현에 필요한 상세 설계가 부족하다.

구현 전에 사용자 여정, UX, 상세 메커니즘을 구체화해야 한다.

## 2. Goal

ReproGate 제품의 구현 가능한 수준의 상세 설계 문서를 작성한다.

## 3. Scope

- 사용자 여정 (설치 → 초기화 → 설정 → 사용)
- CLI UX 설계 (출력, 에러, 피드백)
- 프리셋 로딩 메커니즘
- 어댑터 생성 상세
- config 머지/충돌 해결 로직
- 첫 사용 경험 (dpc init 상세)

## 4. Out of Scope

- 실제 구현
- npm 패키지 배포
- 마케팅/문서화

## 5. Done Criteria

- [x] 사용자 여정 문서 → [product-spec.md §1](../design/product-spec.md#1-사용자-여정)
- [x] CLI 명령어별 상세 스펙 (init, generate, check) → [product-spec.md §2](../design/product-spec.md#2-cli-명령어-상세-스펙)
- [x] 프리셋 로딩/머지 알고리즘 → [product-spec.md §3](../design/product-spec.md#3-프리셋-로딩-메커니즘)
- [x] 어댑터 생성 상세 (파일 목록, 템플릿 로직) → [product-spec.md §4](../design/product-spec.md#4-어댑터-생성-상세)
- [x] 에러/피드백 메시지 설계 → [product-spec.md §5](../design/product-spec.md#5-에러피드백-메시지-설계)
- [x] 첫 사용 경험 시나리오 → [product-spec.md §6](../design/product-spec.md#6-첫-사용-경험-시나리오)

---

## 6. 설계 필요 항목

### 6.1 사용자 여정

```
설치 → 초기화 → 설정 → 사용 → 검증
  ?       ?        ?       ?       ?
```

### 6.2 CLI 명령어 상세

| 명령어 | 입력 | 출력 | 에러 케이스 |
|--------|------|------|------------|
| `dpc init` | ? | ? | ? |
| `dpc generate` | ? | ? | ? |
| `dpc check` | ? | ? | ? |

### 6.3 프리셋 로딩

- 어디서 찾나? (builtin, local, npm)
- 로딩 순서?
- 머지 로직?
- 충돌 해결?

### 6.4 어댑터 생성

- `dpc generate`가 만드는 파일 목록?
- 템플릿 → 실제 파일 변환 로직?
- 이미 파일 있을 때?

### 6.5 에러/피드백

- 성공 시 출력?
- 실패 시 메시지?
- 도움말?

---

## 7. Related

- [architecture.md](../design/architecture.md)
- [presets-spec.md](../design/presets-spec.md)
- [ADR-DPC-006](../adr/ADR-DPC-006-dpc-config-schema.md)
- [ADR-DPC-007](../adr/ADR-DPC-007-rules-engine-selection.md)
- [WP-DPC-2026-03-010](./WP-DPC-2026-03-010-gate-engine-implementation.md) - Gate 엔진 구현 (후속)
