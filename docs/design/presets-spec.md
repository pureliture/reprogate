# ReproGate Presets / Skills 명세

> Canonical Definition: [final-definition.md](../strategy/final-definition.md)

프리셋은 재사용 가능한 **Skill 묶음**이다.
각 Skill은 `guidelines.md`(의도)와 `rules.rego`(강제)를 통해 기록 기반 패턴을 재사용 가능하게 만든다.

---

## 1. 역할

Preset은 다음을 담당한다.

1. 특정 작업 유형에 필요한 Skill 조합 정의
2. 기록 기반 작업 패턴의 재사용
3. Gate가 검사할 규칙 집합 제공

즉 preset은 단순 템플릿이 아니라, **반복되는 작업 패턴의 번들**이다.

---

## 2. 디렉토리 구조

```text
presets/
├── <preset-name>/
│   ├── preset.yaml
│   ├── guidelines.md
│   ├── rules.rego
│   ├── records.yaml        # optional: 기대 기록 범주 설명
│   └── examples/
```

### 2.1 구성 의미

| 파일 | 역할 |
|---|---|
| `preset.yaml` | 메타데이터 및 조합 정보 |
| `guidelines.md` | AI가 따라야 할 기대 행동 |
| `rules.rego` | Gate가 검사하는 강제 규칙 |
| `records.yaml` | 어떤 기록 범주가 필요한지 문서화하는 선택 표면 |

---

## 3. Skill 모델

Preset 내부에서 실질적 핵심은 Skill이다.

### 3.1 Skill의 최소 단위

```text
skill/
├── guidelines.md
└── rules.rego
```

### 3.2 Skill의 의미

- `guidelines.md`는 왜/어떻게 일해야 하는지 설명
- `rules.rego`는 어떤 증거가 없으면 차단할지 정의

### 3.3 Skill과 기록의 관계

Skill은 기록 없이 성립하지 않는다.

예:
- 설계 기록이 있어야 설계 우선 Skill을 강제할 수 있다
- 의사결정 기록이 있어야 판단 근거 기록 Skill을 강제할 수 있다
- 검증 기록이 있어야 verification Skill을 강제할 수 있다

---

## 4. preset.yaml

```yaml
name: "feature-standard"
version: "1.0.0"
description: "Feature delivery with required records and verification"
author: "reprogate"
tags: ["feature", "records", "gate"]
extends: "minimal"
skills:
  - "planning"
  - "decision-log"
  - "verification"
```

### 4.1 주요 필드

| 필드 | 설명 |
|---|---|
| `name` | 프리셋 식별자 |
| `version` | 버전 |
| `description` | 프리셋 설명 |
| `extends` | 부모 프리셋 |
| `skills` | 적용할 Skill 목록 |

---

## 5. guidelines.md 포맷

guidelines는 LLM이 이해하고 따를 기대 행동을 정의한다.

### 5.1 포맷 원칙

- 짧고 구체적일 것
- 기록 요구사항을 모호하게 쓰지 않을 것
- 검증 가능한 문장으로 작성할 것
- 서로 충돌하는 규칙을 넣지 않을 것

### 5.2 권장 섹션

```markdown
# {Preset Name} Guidelines

## Goal
- 이 preset이 무엇을 보장하려는가

## Required Records
- 어떤 종류의 기록이 필요한가

## Workflow Expectations
- 어떤 순서와 판단 기준을 기대하는가

## Verification
- 어떤 검증 흔적이 필요하나
```

### 5.3 중요한 점

guidelines는 “문서를 많이 써라”가 아니라  
**Gate가 나중에 검사할 수 있는 증거를 남겨라**를 설명해야 한다.

---

## 6. rules.rego

OPA/Rego는 preset이 요구하는 패턴을 실제 강제한다.

### 6.1 예시

```rego
package dpc.rules

import rego.v1

deny contains msg if {
    input.trigger == "commit"
    not input.records.decision_log
    msg := "의사결정 기록이 필요합니다"
}

deny contains msg if {
    input.trigger == "commit"
    not input.records.verification
    msg := "검증 기록이 필요합니다"
}
```

### 6.2 ReproGate 관점의 규칙 원칙

- 규칙은 가능한 한 **기록과 산출물**을 본다
- 런타임 상태만을 단독 근거로 삼지 않는다
- 차단 메시지는 무엇이 빠졌는지 설명해야 한다

---

## 7. 로딩 모델

### 7.1 Resolution Order

```text
1. built-in presets
2. global presets
3. local presets
4. external package presets
```

### 7.2 머지 원칙

```text
guidelines  → append
rules       → merge by rule identity
skills      → union with override support
records     → additive expectations unless explicitly disabled
```

### 7.3 우선순위

```text
custom methodology > override > preset > default
```

---

## 8. 예시 프리셋

### 8.1 minimal

- 최소한의 기록과 기본 gate만 요구
- 도입 비용이 낮음

### 8.2 tdd

- 테스트 우선 패턴
- 구현 전/후 검증 흔적 요구

### 8.3 feature-standard

- 작업 계획 기록
- 의사결정 기록
- 검증 기록
- 변경 기록

---

## 9. Team 확장

Preset과 Skill은 개인 설정에 머무르지 않는다.

팀 리드가 다듬은 패턴은:
- preset으로 묶이고
- 저장소에 커밋되며
- 팀원 도구에서 동일하게 적용된다

이렇게 개인 노하우가 팀 운영 표준으로 확장된다.

---

## 10. 설계 요약

- preset은 Skill 묶음이다
- Skill은 기록 기반 패턴이다
- rules.rego는 기록과 산출물을 검사한다
- preset의 목적은 템플릿 배포가 아니라 반복 가능한 방법론 배포다

## Related

- [architecture.md](./architecture.md)
- [product-spec.md](./product-spec.md)
- [ADR-DPC-007](../adr/ADR-DPC-007-rules-engine-selection.md)
