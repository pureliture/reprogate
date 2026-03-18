---
record_id: "ADR-002"
title: "Rules 엔진 선택 — OPA/Rego 채택"
type: "adr"
status: "Accepted"
created_at: "2026-03-17"
tags: ["opa", "rego", "gate", "stage-0"]
supersedes: "ADR-DPC-007"
---

# ADR-002: Rules 엔진 선택 — OPA/Rego 채택

## Status
Accepted (2026-03-17, 원본 ADR-DPC-007에서 이관)

## Context
ReproGate의 핵심 기능은 Gate를 통한 규칙 강제이다. 초기에 자체 DSL을 설계했으나, 다음 문제가 제기되었다:

1. **파서 구현 부담**: 자체 DSL은 파서를 직접 구현해야 함
2. **유지보수 비용**: 문법 확장, 버그 수정, 테스트 프레임워크 모두 직접 개발
3. **형식화 부족**: BNF/EBNF 없이 예시로만 정의되어 구현자마다 해석이 다를 수 있음

기존 정책 엔진 검토 결과:

| 도구 | 적합성 | 비고 |
|------|--------|------|
| OPA/Rego | O | CNCF 졸업, 범용, CLI 지원 |
| Sentinel | X | HashiCorp 제품 전용 |
| Kyverno | X | Kubernetes 전용 |
| CEL | △ | 경량하지만 별도 통합 필요 |

## Decision

**OPA/Rego를 rules 엔진으로 채택한다.**

### 이유

1. **파서 불필요**: OPA가 Rego 파싱/평가 제공
2. **테스트 내장**: `opa test` 명령으로 규칙 테스트 가능
3. **검증된 도구**: CNCF 졸업 프로젝트, 프로덕션 검증됨
4. **CLI 지원**: `opa eval`로 동기 실행 가능, 훅에서 호출 적합
5. **사용자 영향 최소**: 일반 사용자는 presets 선택만, Rego는 프리셋 제작자만 다룸

### 변경 사항

**Before (자체 DSL):**
```yaml
# rules.yaml
rules:
  - id: "tdd-gate"
    trigger: "write"
    condition: "ext == '.py' and not file matches 'test_*'"
    require: "file 'tests/test_{stem}.py' exists"
    message: "TDD: 테스트를 먼저 작성하세요"
```

**After (Rego):**
```rego
# rules.rego
package reprogate.rules

import rego.v1

deny contains msg if {
    input.trigger == "write"
    endswith(input.file, ".py")
    not startswith(file.basename(input.file), "test_")
    not file_exists(sprintf("tests/test_%s.py", [file.stem(input.file)]))
    msg := sprintf("TDD: %s 작성 전에 테스트를 먼저 작성하세요", [input.file])
}
```

### Gate 호출 방식

```python
import subprocess
import json

def evaluate_rules(trigger: str, context: dict) -> dict:
    """OPA로 규칙 평가"""
    input_data = {"trigger": trigger, **context}

    result = subprocess.run(
        ["opa", "eval", "--data", "rules.rego",
         "--input", "-", "data.reprogate.rules.deny"],
        input=json.dumps(input_data),
        capture_output=True,
        text=True
    )

    output = json.loads(result.stdout)
    denies = output.get("result", [{}])[0].get("expressions", [{}])[0].get("value", [])

    if denies:
        return {"allowed": False, "messages": denies}
    return {"allowed": True}
```

## Consequences
- 긍정: 파서 구현 불필요 → 개발 시간 단축
- 긍정: 테스트 프레임워크 내장 → 규칙 품질 보장
- 긍정: 검증된 도구 → 안정성 확보
- 부정: OPA 바이너리 의존성 추가
- 부정: Rego 학습 필요 (프리셋 제작자만)
- 완화: CLI에 OPA 번들링 또는 설치 가이드 제공, 공식 프리셋은 ReproGate 측에서 Rego로 제공

## Verification
- [x] Rego 규칙 예시 작성 완료 (skills/record-required/rules.rego)
- [ ] OPA 바이너리 연동 (Stage 1)
- [ ] `opa test` 기반 규칙 테스트 프레임워크 구축 (Stage 2)
