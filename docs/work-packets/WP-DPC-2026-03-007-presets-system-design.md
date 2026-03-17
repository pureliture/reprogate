---
packet_id: "WP-DPC-2026-03-007"
title: "presets 시스템 설계"
goal_ids: ["DPC-G1", "DPC-G4"]
status: "DONE"
work_type: "DESIGN"
priority: "P1"
target_environment: "master"
start_process: "P0"
current_process: "P2"
next_process: null
owner: "SHARED"
created_at: "2026-03-13"
last_updated: "2026-03-17"
parent: null
track: "dpc core design"
---

# WP-DPC-2026-03-007: presets 시스템 설계

## 1. Background

dpc architecture.md에서 presets 시스템을 정의했으나 구체적인 설계가 없다.

```
presets/
├── tdd/
│   ├── guidelines.md    # 방법론 설명 (의도)
│   └── rules.yaml       # 강제 규칙 (보장)
├── google-practices/
├── adr-driven/
└── minimal/
```

## 2. Goal

presets 시스템의 구체적인 설계를 정의한다:

- 프리셋 디렉토리 구조
- guidelines.md 포맷
- rules.yaml 스키마
- 프리셋 로딩 메커니즘
- 오버라이드 방식

## 3. Scope

- 프리셋 구조 설계
- 로딩/머지 로직 설계
- 최소 1개 프리셋 예시 (tdd 또는 minimal)

## 4. Out of Scope

- 구현
- npm 패키지화
- 모든 프리셋 작성

## 5. Done Criteria

- [x] 프리셋 디렉토리 구조 정의 → 6.1
- [x] guidelines.md 포맷 정의 → 6.2
- [x] rules.rego 구조 정의 (→ ADR-DPC-007 OPA/Rego 채택) → 6.3
- [x] 프리셋 로딩 알고리즘 정의 → 6.4
- [x] 오버라이드 우선순위 정의 → 6.5
- [x] 예시 프리셋 1개 작성 → 6.6 (minimal), 6.7 (tdd)
- [x] ADR-DPC-006 참조 반영 → 6.5 우선순위 섹션

## 6. Design

설계 문서: **[presets-spec.md](../design/presets-spec.md)**

### 요약

| 항목 | 내용 |
|------|------|
| 디렉토리 구조 | `preset.yaml` + `guidelines.md` + `rules.rego` |
| 로딩 순서 | builtin → global → local → npm |
| 오버라이드 | `methodology > override > preset > default` |
| 머지 전략 | guidelines=append, rules=merge by ID |
| 예시 프리셋 | `minimal`, `tdd`

## 7. Related

- [architecture.md](../design/architecture.md)
- [ADR-DPC-007](../adr/ADR-DPC-007-rules-engine-selection.md) - OPA/Rego 채택 (WP-015 대체)
- [ADR-DPC-006](../adr/ADR-DPC-006-dpc-config-schema.md)
