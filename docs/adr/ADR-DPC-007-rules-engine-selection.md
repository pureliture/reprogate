# ADR-DPC-007: Rules 엔진 선택 - OPA/Rego 채택

## Status

**Accepted** (2026-03-17)

## Context

dpc의 핵심 기능은 Gate를 통한 규칙 강제이다. WP-DPC-2026-03-008에서 자체 DSL을 설계했으나, 다음 문제가 제기되었다:

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
package dpc.rules

import rego.v1

deny contains msg if {
    input.trigger == "write"
    endswith(input.file, ".py")
    not startswith(file.basename(input.file), "test_")
    not file_exists(sprintf("tests/test_%s.py", [file.stem(input.file)]))
    msg := sprintf("TDD: %s 작성 전에 테스트를 먼저 작성하세요", [input.file])
}
```

### 프리셋 구조 변경

```
presets/
├── tdd/
│   ├── preset.yaml
│   ├── guidelines.md
│   └── rules.rego        # rules.yaml → rules.rego
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
         "--input", "-", "data.dpc.rules.deny"],
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

### 긍정적

- 파서 구현 불필요 → 개발 시간 단축
- 테스트 프레임워크 내장 → 규칙 품질 보장
- 검증된 도구 → 안정성 확보
- 표현력 증가 → 복잡한 규칙도 표현 가능

### 부정적

- OPA 바이너리 의존성 추가
- Rego 학습 필요 (프리셋 제작자만)
- rules.yaml의 직관성 상실

### 완화 조치

- `dpc` CLI에 OPA 번들링 또는 설치 가이드 제공
- Rego 작성 가이드 문서 제공
- 공식 프리셋(tdd, minimal 등)은 dpc 팀이 Rego로 제공

## Alternatives Considered

### 1. 자체 DSL 유지

- 장점: 직관적인 YAML 문법
- 단점: 파서 구현/유지보수 부담, 형식화 필요
- **기각 이유**: 유지보수 비용이 이점을 초과

### 2. CEL (Common Expression Language)

- 장점: 경량, Google 지원
- 단점: Python 라이브러리 통합 필요, OPA만큼 검증되지 않음
- **기각 이유**: OPA가 더 성숙하고 CLI 지원 우수

### 3. 하이브리드 (자체 DSL → Rego 컴파일)

- 장점: 사용자 친화적 문법 유지
- 단점: 컴파일러 구현 필요, 복잡성 증가
- **기각 이유**: 파서 구현과 동일한 문제

## Related

- [WP-DPC-2026-03-008](../work-packets/WP-DPC-2026-03-008-rules-dsl-design.md) - Rules DSL 설계 (superseded)
- [rules-dsl-spec.md](../rules-dsl-spec.md) - 자체 DSL 명세 (deprecated)
- [OPA 공식 문서](https://www.openpolicyagent.org/docs)
- [Rego 언어 레퍼런스](https://www.openpolicyagent.org/docs/latest/policy-language/)
