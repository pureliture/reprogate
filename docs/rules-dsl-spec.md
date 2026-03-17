# dpc Rules DSL 명세

> **DEPRECATED**: 이 문서는 더 이상 유효하지 않습니다.
> OPA/Rego 채택으로 대체되었습니다. [ADR-DPC-007](./adr/ADR-DPC-007-rules-engine-selection.md) 참조.

---

> rules.yaml은 Gate가 강제하는 규칙을 선언적으로 정의한다.

---

## 1. 개요

### 1.1 목적

```
guidelines.md → LLM이 이해 → 무시 가능
rules.yaml   → Gate가 강제 → 무시 불가
```

### 1.2 기본 구조

```yaml
version: "1"

rules:
  - id: "rule-id"
    trigger: "write"
    condition: "..."
    require: "..."
    message: "차단 시 표시할 메시지"
    severity: "error"
```

---

## 2. 스키마

### 2.1 루트

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `version` | string | Y | 스키마 버전 ("1") |
| `rules` | array | Y | 규칙 배열 |

### 2.2 Rule 객체

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `id` | string | Y | 규칙 식별자 (프리셋 내 유니크) |
| `trigger` | string | Y | 트리거 타입 |
| `condition` | string | N | 규칙 적용 조건 (없으면 항상 적용) |
| `require` | string | Y | 요구 조건 |
| `message` | string | Y | 차단 시 메시지 |
| `severity` | string | N | error (기본) / warning |

---

## 3. Trigger 타입

Gate가 감지하는 이벤트 타입.

| trigger | 설명 | 대상 도구 |
|---------|------|----------|
| `write` | 파일 생성/수정 | Write, Edit, MultiEdit |
| `bash` | 쉘 명령 실행 | Bash |
| `commit` | 커밋 시도 | Bash (git commit) |
| `read` | 파일 읽기 | Read |

### 3.1 trigger 별 컨텍스트 변수

각 trigger는 condition/require에서 사용할 수 있는 변수를 제공한다.

| trigger | 변수 | 설명 |
|---------|------|------|
| `write` | `file` | 대상 파일 경로 |
| `write` | `ext` | 파일 확장자 |
| `write` | `dir` | 파일 디렉토리 |
| `bash` | `command` | 실행할 명령어 |
| `commit` | `files` | 커밋 대상 파일 목록 |
| `commit` | `message` | 커밋 메시지 |

---

## 4. Condition 문법

규칙 적용 여부를 결정하는 조건.

### 4.1 파일 패턴

```yaml
condition: "file matches 'src/**/*.py'"
condition: "file matches 'src/**/*.{ts,js}'"
condition: "ext in ['.py', '.ts', '.js']"
```

### 4.2 부정

```yaml
condition: "not file matches 'test_*.py'"
condition: "not ext in ['.md', '.yaml']"
```

### 4.3 논리 연산

```yaml
condition: "file matches 'src/**' and not file matches '**/__init__.py'"
condition: "ext == '.py' or ext == '.ts'"
```

### 4.4 컨텍스트 변수

```yaml
condition: "process in ['P3', 'P4']"
condition: "tdd_mode == true"
```

---

## 5. Require 문법

충족해야 하는 요구 조건.

### 5.1 파일 존재

```yaml
require: "file 'tests/test_{stem}.py' exists"
require: "file '{dir}/../tests/test_{name}' exists"
require: "any file matching 'tests/**/test_{stem}.py' exists"
```

### 5.2 파일 수정

```yaml
require: "file 'README.md' modified"
require: "file 'README.md' modified if file matches 'src/**'"
```

### 5.3 명령어 패턴 (bash)

```yaml
require: "command is readonly"
require: "command matches '^git (status|log|diff)'"
```

### 5.4 변수 치환

| 변수 | 설명 | 예시 |
|------|------|------|
| `{file}` | 전체 경로 | `src/utils/helper.py` |
| `{dir}` | 디렉토리 | `src/utils` |
| `{name}` | 파일명 | `helper.py` |
| `{stem}` | 확장자 제외 | `helper` |
| `{ext}` | 확장자 | `.py` |

---

## 6. Message 포맷

### 6.1 기본

```yaml
message: "테스트 파일이 필요합니다"
```

### 6.2 변수 사용

```yaml
message: "TDD: '{name}' 작성 전에 테스트를 먼저 작성하세요"
message: |
  테스트 파일을 찾을 수 없습니다.
  예상 위치: tests/test_{stem}.py
```

---

## 7. Severity

| 값 | 동작 |
|----|------|
| `error` | 차단 (기본값) |
| `warning` | 경고만 (차단 안 함) |

---

## 8. 예시

### 8.1 TDD 규칙

```yaml
version: "1"

rules:
  - id: "tdd-require-test"
    trigger: "write"
    condition: |
      ext in ['.py', '.ts', '.js', '.java', '.go']
      and not file matches '**/test_*'
      and not file matches '**/*_test.*'
      and not file matches '**/*.test.*'
      and not file matches '**/__init__.py'
    require: "any file matching 'tests/**/test_{stem}.py' exists"
    message: |
      TDD Gate: 테스트 없이 구현 파일을 작성할 수 없습니다.
      먼저 테스트를 작성하세요: tests/test_{stem}.py
    severity: "error"
```

### 8.2 문서 동기화 규칙

```yaml
  - id: "readme-sync"
    trigger: "commit"
    condition: "any file matches 'src/**'"
    require: "file 'README.md' modified"
    message: "src/ 변경 시 README.md도 업데이트하세요"
    severity: "warning"
```

### 8.3 프로세스 기반 규칙

```yaml
  - id: "readonly-process"
    trigger: "write"
    condition: "process in ['P0', 'P1', 'P2'] and not file matches '**/*.md'"
    require: "false"
    message: "{process}에서는 문서만 수정할 수 있습니다"
    severity: "error"
```

### 8.4 Bash readonly 규칙

```yaml
  - id: "bash-readonly"
    trigger: "bash"
    condition: "process in ['P0', 'P1', 'P2']"
    require: "command is readonly"
    message: "{process}에서는 읽기 전용 명령만 실행할 수 있습니다"
    severity: "error"
```

---

## 9. 기존 하드코딩 → DSL 변환

기존 `claude_pretooluse_guard.py`의 규칙을 DSL로 표현:

```yaml
version: "1"

rules:
  # 프로세스 미선택 시 차단
  - id: "require-process"
    trigger: "write"
    condition: "process == ''"
    require: "false"
    message: "프로세스를 선택한 후 작업하세요"
    severity: "error"

  # READ_ONLY_PROCESSES에서 문서만 허용
  - id: "readonly-process-docs-only"
    trigger: "write"
    condition: |
      process in ['G0', 'P0', 'P1', 'P2', 'S2', 'S4']
      and not ext == '.md'
      and not dir == 'docs'
    require: "false"
    message: "{process}에서는 문서만 수정할 수 있습니다"
    severity: "error"

  # TEAM_ELIGIBLE에서 team_mode 결정 필요
  - id: "team-mode-required"
    trigger: "write"
    condition: "process in ['P3', 'P4', 'S3', 'S1'] and team_mode == 'auto'"
    require: "false"
    message: "team_mode를 team 또는 single로 결정한 후 작업하세요"
    severity: "error"

  # TDD Gate
  - id: "tdd-gate"
    trigger: "write"
    condition: |
      tdd_mode == true
      and ext in ['.py', '.ts', '.js', '.tsx', '.jsx', '.java', '.kt', '.go', '.rs', '.rb', '.swift']
      and not file matches '**/test_*'
      and not file matches '**/*_test.*'
      and not file matches '**/*.test.*'
      and not file matches '**/*.spec.*'
      and not file matches '**/__init__.py'
      and not ext in ['.yaml', '.yml', '.json', '.toml', '.md']
    require: "corresponding test file exists"
    message: |
      TDD Gate: '{name}' 작성 전에 테스트를 먼저 작성하세요.
      예: test_{stem}.py
    severity: "error"

  # Bash: 프로세스 미선택 시 readonly만 허용
  - id: "bash-require-process"
    trigger: "bash"
    condition: "process == '' and not command is readonly"
    require: "false"
    message: "프로세스를 선택한 후 명령을 실행하세요"
    severity: "error"

  # Bash: READ_ONLY_PROCESSES에서 readonly만 허용
  - id: "bash-readonly-process"
    trigger: "bash"
    condition: "process in ['G0', 'P0', 'P1', 'P2', 'S2', 'S4'] and not command is readonly"
    require: "false"
    message: "{process}에서는 읽기 전용 명령만 실행할 수 있습니다"
    severity: "error"
```

---

## 10. Gate 엔진 인터페이스

### 10.1 입력

```python
@dataclass
class GateContext:
    trigger: str              # "write", "bash", "commit"
    tool_name: str            # "Write", "Bash", etc.
    tool_input: dict          # 도구 입력
    process: str              # 현재 프로세스
    team_mode: str            # "auto", "single", "team"
    tdd_mode: bool            # TDD 모드 활성화 여부
    # trigger별 추가 변수
    file: Optional[str]       # write: 대상 파일
    command: Optional[str]    # bash: 명령어
```

### 10.2 출력

```python
@dataclass
class GateResult:
    allowed: bool
    rule_id: Optional[str]    # 차단한 규칙 ID
    message: Optional[str]    # 차단 메시지
    severity: str             # "error" or "warning"
```

### 10.3 평가 순서

1. 모든 rules 순회
2. trigger 매칭 확인
3. condition 평가 (True면 계속)
4. require 평가 (False면 차단)
5. 첫 번째 차단에서 중단 (severity=error) 또는 계속 (severity=warning)

---

## 11. JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["version", "rules"],
  "properties": {
    "version": {
      "type": "string",
      "const": "1"
    },
    "rules": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "trigger", "require", "message"],
        "properties": {
          "id": { "type": "string" },
          "trigger": {
            "type": "string",
            "enum": ["write", "bash", "commit", "read"]
          },
          "condition": { "type": "string" },
          "require": { "type": "string" },
          "message": { "type": "string" },
          "severity": {
            "type": "string",
            "enum": ["error", "warning"],
            "default": "error"
          }
        }
      }
    }
  }
}
```

---

## 12. 관련 문서

- [presets-spec.md](./presets-spec.md) - 프리셋 시스템 명세
- [architecture.md](./architecture.md) - dpc 전체 아키텍처
