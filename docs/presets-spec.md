# dpc Presets 시스템 명세

> 프리셋은 재사용 가능한 방법론 패키지다. guidelines(의도)와 rules(보장)를 묶어 배포한다.

---

## 1. 프리셋 디렉토리 구조

```
presets/
├── <preset-name>/
│   ├── preset.yaml          # 프리셋 메타데이터 (필수)
│   ├── guidelines.md        # 방법론 설명 (필수)
│   ├── rules.rego           # 강제 규칙 - OPA/Rego (선택)
│   └── examples/            # 예시 파일 (선택)
│       └── ...
```

### 1.1 preset.yaml 스키마

```yaml
# preset.yaml
name: "tdd"                    # 프리셋 식별자 (필수)
version: "1.0.0"               # 시맨틱 버전 (필수)
description: "Test-Driven Development methodology"  # 설명 (필수)
author: "dpc"                  # 작성자 (선택)
tags: ["testing", "quality"]   # 태그 (선택)
extends: null                  # 상속할 프리셋 (선택)
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `name` | string | Y | 프리셋 식별자 |
| `version` | string | Y | 시맨틱 버전 |
| `description` | string | Y | 프리셋 설명 |
| `author` | string | N | 작성자 |
| `tags` | string[] | N | 검색/분류용 태그 |
| `extends` | string | N | 상속할 부모 프리셋 |

---

## 2. guidelines.md 포맷

guidelines.md는 LLM이 이해하고 따를 방법론을 자연어로 정의한다.

> 상세 근거: [llm-document-format-reference.md](./references/llm-document-format-reference.md)

### 2.1 포맷 제약 (공식 근거)

> 출처: [Anthropic 공식 문서](https://code.claude.com/docs/en/memory)

| 항목 | 제약 | 공식 인용 |
|------|------|----------|
| 길이 | < 200줄 | "target under 200 lines per CLAUDE.md file" |
| 구조 | 헤딩 + 불릿 | "use markdown headers and bullets to group related instructions" |
| 구체성 | 검증 가능 | "write instructions that are concrete enough to verify" |
| 일관성 | 충돌 제거 | "if two rules contradict each other, Claude may pick one arbitrarily" |

### 2.2 필수 섹션

```markdown
# {Preset Name} Guidelines

> 한 줄 요약 (핵심 철학)

## Philosophy
- 핵심 원칙 1
- 핵심 원칙 2
- 핵심 원칙 3

## Workflow
1. 단계 1
2. 단계 2
3. 단계 3

## Conventions
### 카테고리 A
- 규칙 1
- 규칙 2

### 카테고리 B
- 규칙 1

## Examples
### Good
```python
# 좋은 예시
```

### Bad
```python
# 나쁜 예시
```
```

### 2.3 권장 섹션 (선택)

```markdown
## When Not to Apply
- 예외 상황 1
- 예외 상황 2

## References
- [상세 문서](path): 설명
```

### 2.4 피해야 할 것 (공식 근거)

| 안티패턴 | 공식 인용 |
|----------|----------|
| 200줄 초과 | "Longer files consume more context and reduce adherence" |
| 모호한 지시 | "Format properly" → "Use 2-space indentation" |
| 규칙 간 충돌 | "if two rules contradict each other, Claude may pick one arbitrarily" |
| 긴 단락 | "use markdown headers and bullets" |

---

## 3. rules.rego (OPA/Rego)

> [ADR-DPC-007](./adr/ADR-DPC-007-rules-engine-selection.md)에서 OPA/Rego 채택.
> 자체 DSL 대신 검증된 정책 엔진을 사용하여 파서 구현 부담 제거.

```rego
# rules.rego
package dpc.rules

import rego.v1

# TDD: 테스트 파일 요구
deny contains msg if {
    input.trigger == "write"
    endswith(input.file, ".py")
    not startswith(file.basename(input.file), "test_")
    not file_exists(sprintf("tests/test_%s.py", [file.stem(input.file)]))
    msg := sprintf("TDD: %s 작성 전에 테스트를 먼저 작성하세요", [input.file])
}

# README 동기화 경고
warn contains msg if {
    input.trigger == "commit"
    input.files_modified[_] == "src/"
    not input.files_modified[_] == "README.md"
    msg := "README.md를 업데이트하세요"
}
```

### 3.1 Gate 호출

```python
import subprocess, json

def evaluate_rules(trigger: str, context: dict) -> dict:
    input_data = {"trigger": trigger, **context}
    result = subprocess.run(
        ["opa", "eval", "--data", "rules.rego",
         "--input", "-", "data.dpc.rules.deny"],
        input=json.dumps(input_data),
        capture_output=True, text=True
    )
    denies = json.loads(result.stdout).get("result", [{}])[0].get("expressions", [{}])[0].get("value", [])
    return {"allowed": False, "messages": denies} if denies else {"allowed": True}
```

### 3.2 테스트

```bash
# OPA 내장 테스트
opa test rules.rego rules_test.rego
```

---

## 4. 프리셋 로딩

### 4.1 Resolution Order

프리셋은 다음 순서로 탐색한다:

```
1. 빌트인 프리셋: <dpc-package>/presets/{name}/
2. 글로벌 프리셋: ~/.dpc/presets/{name}/
3. 로컬 프리셋:   .dpc/presets/{name}/
4. npm 프리셋:    node_modules/{name}/ (prefix: @, dpc-preset-)
```

먼저 발견된 경로를 사용한다.

### 4.2 로딩 알고리즘

```
load_preset(name):
  1. resolve_preset_path(name) → 경로 결정
  2. preset.yaml 로드 및 검증
  3. guidelines.md 로드
  4. rules.rego 로드 (있으면)
  5. extends가 있으면 부모 로드 후 머지
  6. Preset 객체 반환
```

### 4.3 extends (상속)

프리셋은 다른 프리셋을 상속할 수 있다:

```yaml
# presets/tdd/preset.yaml
name: "tdd"
extends: "minimal"
```

상속 시 머지 규칙:
- `guidelines`: 부모 뒤에 자식 append
- `rules`: ID 기준 머지 (자식이 부모 덮어씀)

---

## 5. 오버라이드 우선순위

`.dpc/config.yaml`에서 프리셋을 사용할 때 오버라이드 가능:

```yaml
# .dpc/config.yaml
preset: "tdd"
override:
  guidelines: |
    TDD 따르되, 유틸 함수는 테스트 생략 허용.
  rules:
    - id: "require-test"
      pattern: "src/core/**/*.py"  # 범위 축소
```

### 5.1 우선순위

```
methodology > override > preset > default
```

| 레벨 | 설명 |
|------|------|
| `default` | 아무것도 없을 때 빈 상태 |
| `preset` | 프리셋에서 로드 |
| `override` | 프리셋 위에 추가/수정 |
| `methodology` | 프리셋 무시하고 완전 커스텀 |

### 5.2 머지 전략

| 필드 | 머지 방식 |
|------|----------|
| `guidelines` | **Append** - 하위 레벨이 상위에 추가됨 |
| `rules` | **Merge by ID** - 같은 ID는 덮어쓰기, 새 ID는 추가 |

### 5.3 rules 머지 로직

```
merge_rules_by_id(base, overlay):
  result = {r.id: r for r in base}

  for rule in overlay:
    if rule.skip == true:
      del result[rule.id]    # 해당 규칙 제거
    else:
      result[rule.id] = rule # 덮어쓰기 또는 추가

  return list(result.values())
```

`skip: true`로 부모 규칙 비활성화 가능:

```yaml
override:
  rules:
    - id: "require-test"
      skip: true              # 이 규칙 비활성화
```

---

## 6. 공식 프리셋

### 6.1 minimal

가장 단순한 프리셋. 강제 규칙 없음.

```yaml
# preset.yaml
name: "minimal"
version: "1.0.0"
description: "최소한의 방법론 - 자유롭게 개발하되 기본 품질만 유지"
```

```markdown
# guidelines.md (요약)
- 복잡한 프로세스 없이 빠르게 개발
- 필수적인 것만 요구, 나머지는 자율
```

```rego
# rules.rego
package dpc.rules
import rego.v1
# 강제 규칙 없음 - deny/warn 정의 없음
```

### 6.2 tdd

Test-Driven Development 프리셋.

```yaml
# preset.yaml
name: "tdd"
version: "1.0.0"
description: "Test-Driven Development - 테스트 먼저, 구현은 나중에"
extends: "minimal"
```

```markdown
# guidelines.md (요약)
- Red → Green → Refactor
- 테스트는 문서이자 안전망
```

```rego
# rules.rego
package dpc.rules
import rego.v1

deny contains msg if {
    input.trigger == "write"
    regex.match(`src/.*\.(py|ts|js)$`, input.file)
    not file_exists(test_file_for(input.file))
    msg := sprintf("TDD: %s에 대응하는 테스트 파일이 필요합니다", [input.file])
}
```

---

## 7. 관련 문서

- [architecture.md](./architecture.md) - dpc 전체 아키텍처
- [ADR-DPC-007](./adr/ADR-DPC-007-rules-engine-selection.md) - OPA/Rego 채택 결정
- [OPA 공식 문서](https://www.openpolicyagent.org/docs) - Rego 언어 레퍼런스
- [ADR-DPC-006](./adr/ADR-DPC-006-dpc-config-schema.md) - config.yaml 스키마

### 레퍼런스

- [preset-system-reference.md](./references/preset-system-reference.md) - 프리셋 시스템 설계 근거 (ESLint)
- [llm-document-format-reference.md](./references/llm-document-format-reference.md) - guidelines.md 포맷 근거 (Anthropic, OpenAI, llms.txt)
