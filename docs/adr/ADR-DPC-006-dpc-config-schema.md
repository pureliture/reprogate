# ADR-DPC-006: .dpc/config.yaml 스키마 정의

## Status

**Draft** (2026-03-13)

## Context

dpc architecture.md에서 사용자 프로젝트 구조를 다음과 같이 정의했다:

```
my-project/
├── .dpc/
│   ├── config.yaml          # 메인 설정
│   ├── methodology/         # 커스텀 방법론 (선택)
│   │   ├── guidelines.md
│   │   └── rules.yaml
│   └── context/             # 런타임 상태
```

그러나 `config.yaml`의 구체적인 스키마가 정의되지 않았다.

현재 dpc는 `dpc.config.yaml`(프로젝트 루트)을 사용하고 있으며,
이를 `.dpc/config.yaml`로 통합할지, 별도로 유지할지 결정이 필요하다.

## Decision

### 1. 설정 파일 위치

- **프레임워크 설정**: `dpc.config.yaml` (프로젝트 루트) - 유지
- **방법론 설정**: `.dpc/config.yaml` - 신규

두 파일은 역할이 다르다:
- `dpc.config.yaml`: 프로젝트 메타데이터, 도구 활성화, 레코드 경로
- `.dpc/config.yaml`: 프리셋 선택, 방법론 오버라이드, 런타임 옵션

### 2. .dpc/config.yaml 스키마

```yaml
# .dpc/config.yaml

# 옵션 A: 프리셋 사용
preset: "tdd"

# 옵션 B: 프리셋 + 오버라이드
preset: "tdd"
override:
  guidelines: |
    TDD 따르되, 유틸 함수는 테스트 생략 허용.
  rules:
    - trigger: "write"
      pattern: "src/utils/**"
      skip: true

# 옵션 C: 완전 커스텀
methodology:
  guidelines: |
    테스트 먼저 작성하고 구현해.
    문서는 README만 관리.
  rules:
    - trigger: "write"
      pattern: "src/**/*.py"
      require: "tests/**/test_*.py exists"

# 옵션 D: 외부 프리셋
preset: "@mycompany/our-methodology"
```

### 3. 스키마 필드 정의

| 필드 | 타입 | 설명 |
|------|------|------|
| `preset` | string | 프리셋 이름 또는 npm 패키지 |
| `override.guidelines` | string | guidelines 추가/덮어쓰기 |
| `override.rules` | array | rules 추가/수정 |
| `methodology.guidelines` | string | 완전 커스텀 guidelines |
| `methodology.rules` | array | 완전 커스텀 rules |

### 4. 우선순위

```
methodology > override > preset > default
```

## Consequences

### 긍정적

- 프레임워크 설정과 방법론 설정이 명확히 분리된다
- 프리셋 기반으로 빠르게 시작하고, 필요시 오버라이드 가능
- 외부 npm 프리셋 지원 가능

### 부정적

- 설정 파일이 2개로 분산된다
- 마이그레이션 경로 필요 (기존 dpc.config.yaml 사용자)

### 완화 조치

- `dpc init`에서 두 파일을 함께 생성
- 문서에 역할 차이 명확히 설명

## Related

- [architecture.md](../design/architecture.md)
- [WP-DPC-2026-03-007](../work-packets/WP-DPC-2026-03-007-presets-system-design.md)
