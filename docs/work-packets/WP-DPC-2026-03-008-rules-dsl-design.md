---
packet_id: "WP-DPC-2026-03-008"
title: "rules DSL 설계"
goal_ids: ["DPC-G1", "DPC-G2", "DPC-G4"]
status: "SUPERSEDED"
superseded_by: "ADR-DPC-007"
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

# WP-DPC-2026-03-008: rules DSL 설계

> **SUPERSEDED**: OPA/Rego 채택으로 자체 DSL 설계가 대체되었습니다.
> [ADR-DPC-007](../adr/ADR-DPC-007-rules-engine-selection.md) 참조.

## 1. Background

dpc의 핵심 개념은 `guidelines(의도) + rules(보장)`의 하이브리드다.

현재 rules는 Python 코드로 하드코딩되어 있다 (`scripts/hooks/claude_pretooluse_guard.py`).
이를 선언적 YAML DSL로 전환하여 사용자가 규칙을 정의할 수 있게 해야 한다.

```yaml
# 목표 형태 예시
rules:
  - trigger: "write"
    pattern: "src/**/*.py"
    require: "tests/**/test_*.py exists"

  - trigger: "commit"
    require: "README.md modified if src/ modified"
```

## 2. Goal

rules DSL의 구체적인 설계를 정의한다:

- YAML 문법 정의
- 지원하는 trigger 타입
- 조건/요구사항 표현식
- Gate 엔진 변환 로직
- 에러 메시지 포맷

## 3. Scope

- rules.yaml 스키마 정의
- trigger 타입 정의 (write, edit, commit, bash 등)
- 조건 표현식 문법
- Gate 엔진 인터페이스 설계

## 4. Out of Scope

- 구현
- 복잡한 조건 로직 (1차는 단순 패턴 매칭)
- 런타임 성능 최적화

## 5. Done Criteria

- [x] rules.yaml JSON Schema 정의 → 11절
- [x] trigger 타입 목록 정의 → 3절
- [x] 조건 표현식 문법 정의 → 4절 (condition), 5절 (require)
- [x] Gate 엔진 인터페이스 정의 → 10절
- [x] deny 메시지 포맷 정의 → 6절
- [x] 예시 rules.yaml 작성 → 8절
- [x] 기존 하드코딩 규칙을 DSL로 표현한 예시 → 9절

## 6. Design

설계 문서: **[rules-dsl-spec.md](../rules-dsl-spec.md)**

### 요약

| 항목 | 내용 |
|------|------|
| trigger | write, bash, commit, read |
| condition | 파일 패턴, 논리 연산, 컨텍스트 변수 |
| require | 파일 존재, 파일 수정, 명령어 패턴 |
| severity | error (차단), warning (경고) |
| 변수 치환 | {file}, {dir}, {name}, {stem}, {ext} |

## 7. Related

- [architecture.md](../architecture.md)
- [WP-DPC-2026-03-007](./WP-DPC-2026-03-007-presets-system-design.md)
- [claude_pretooluse_guard.py](../../scripts/hooks/claude_pretooluse_guard.py)
