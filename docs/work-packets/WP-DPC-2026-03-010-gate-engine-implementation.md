---
packet_id: "WP-DPC-2026-03-010"
title: "Gate 엔진 구현"
goal_ids: ["DPC-G1"]
status: "IN_ANALYSIS"
work_type: "IMPLEMENTATION"
priority: "P0"
target_environment: "master"
start_process: "P0"
current_process: "P0"
next_process: "P1"
owner: "SHARED"
created_at: "2026-03-17"
last_updated: "2026-03-17"
parent: "WP-DPC-2026-03-001"
track: "dpc core implementation"
---

# WP-DPC-2026-03-010: Gate 엔진 구현

## 1. Background

ADR-007에서 OPA/Rego를 rules 엔진으로 채택했다. 이제 실제 Gate 엔진을 구현해야 한다.

Gate 엔진은 dpc의 **"보장(Hard)"** 레이어를 담당하며, LLM이 규칙을 어기면 물리적으로 차단한다.

## 2. Goal

OPA/Rego 기반 Gate 엔진을 구현하여 `dpc check` 및 Claude Hook과 연동한다.

## 3. Scope

- Gate 엔진 Python 모듈 구현
- OPA 바이너리 호출 래퍼
- 입력/출력 스키마 정의
- 기본 프리셋 (minimal, tdd) rules.rego 작성
- `dpc check` CLI 연동
- Claude PreToolUse Hook 연동

## 4. Out of Scope

- npm 패키지화
- 다른 AI 도구 어댑터 (Cursor, Kiro 등)
- 고급 프리셋 (google-practices, adr-driven)

## 5. Done Criteria

- [ ] Gate 엔진 모듈 구현 (`scripts/gate_engine.py`)
- [ ] 입력 스키마 정의
- [ ] 출력 스키마 정의
- [ ] OPA 미설치 시 에러 처리
- [ ] 기본 프리셋 2개 (minimal, tdd)
- [ ] `dpc check` 연동
- [ ] Claude Hook 연동
- [ ] 단위 테스트

---

## 6. P0 분석: 설계 갭 식별

### 6.1 명확한 것

| 항목 | 출처 | 내용 |
|------|------|------|
| 엔진 선택 | ADR-007 | OPA/Rego |
| 호출 방식 | ADR-007 | `opa eval --data rules.rego --input - "data.dpc.rules.deny"` |
| 규칙 패키지 | ADR-007 | `package dpc.rules` |
| 출력 형식 | ADR-007 | `deny contains msg if { ... }` |

### 6.2 불명확한 것 (P1에서 해결 필요)

| 항목 | 질문 | 선택지 |
|------|------|--------|
| **OPA 설치** | 사용자가 직접 설치? dpc가 번들? | A) 사용자 설치 + 가이드<br>B) dpc install-deps 명령<br>C) Python OPA 라이브러리 |
| **내장 함수** | `file_exists()` 등 어떻게 제공? | A) input에 미리 계산해서 전달<br>B) OPA custom built-in<br>C) 외부 데이터로 주입 |
| **입력 스키마** | 어떤 필드가 제공되나? | trigger, file, context 외 추가? |
| **에러 처리** | OPA 없을 때, Rego 오류 시 | 명확한 에러 메시지 정의 필요 |
| **Hook 연동** | Claude PreToolUse와 통합 방식 | 기존 guard.py 확장 vs 새 모듈 |
| **성능** | subprocess 호출 오버헤드 | 허용 가능? 캐싱 필요? |

---

## 7. P1 설계 결정 (TODO)

> P0 분석 후 여기에 결정 사항 기록

### 7.1 OPA 설치 전략

**결정**: (미정)

**근거**:

### 7.2 내장 함수 전략

**결정**: (미정)

**근거**:

### 7.3 입력 스키마

```yaml
# 입력 스키마 (TODO: 확정)
trigger: "write" | "edit" | "bash" | "commit"
file: "path/to/file.py"
context:
  # TODO: 어떤 필드?
```

### 7.4 출력 스키마

```json
{
  "allowed": true | false,
  "deny": ["메시지1", "메시지2"],
  "warn": ["경고1"]
}
```

### 7.5 에러 처리

| 상황 | 동작 |
|------|------|
| OPA 미설치 | (TODO) |
| Rego 문법 오류 | (TODO) |
| 타임아웃 | (TODO) |

### 7.6 Hook 연동 방식

**결정**: (미정)

---

## 8. Related

- [ADR-DPC-007](../adr/ADR-DPC-007-rules-engine-selection.md) - OPA/Rego 채택
- [presets-spec.md](../design/presets-spec.md) - 프리셋 시스템 설계
- [architecture.md](../design/architecture.md) - 전체 아키텍처
