# ReproGate 제품 상세 설계

> WP-009 산출물 정렬본 | Canonical Definition: [final-definition.md](../strategy/final-definition.md)

---

## 0. 철학 & Scope

### 0.1 ReproGate란?

> **작업 기록을 필수 산출물로 만들고, 그 기록에서 얻은 패턴을 Skill로 누적하며, 이를 규칙으로 강제하는 방법론 컴파일러**

```text
ReproGate = 기록 기반 작업 표면 제공
AI        = 그 위에서 실제 내용을 작성
Gate      = 필수 증거가 없으면 차단
```

### 0.2 핵심 개념

| 개념 | 역할 |
|---|---|
| Work Records | 의도, 범위, 결정, 검증 근거를 남기는 증거 |
| Skills | 기록에서 추출된 반복 패턴 |
| Rules / Gates | 패턴을 강제하는 집행 계층 |
| Adapters | 도구별 연결 표면 |

### 0.3 제품이 하는 것

| 기능 | 설명 |
|---|---|
| 기록 구조 제공 | 작업이 증거로 남게 만드는 기본 표면 |
| Skill 구조 제공 | 반복 패턴을 재사용 가능한 자산으로 만듦 |
| Gate 연결 | OPA/Rego 기반 강제 |
| Adapter 생성 | Claude/Codex 등 도구에 적용 |
| 검증 | 설정/규칙/프리셋 정합성 검사 |

### 0.4 제품이 하지 않는 것

| 기능 | 이유 |
|---|---|
| 모든 판단 자동 생성 | 판단 자체는 여전히 AI/사용자 협업의 영역 |
| 무거운 상태 추적 | ReproGate의 핵심은 state machine이 아니라 artifact enforcement |
| 모든 도구 직접 통합 | adapter boundary를 유지해야 함 |
| 문서 양산 자체 | 목적은 기록의 양이 아니라 강제 가능한 증거 |

### 0.5 legacy naming note

현재 문서와 저장소에는 `dpc` CLI/경로가 남아 있다.
이 문서에서는 제품명은 ReproGate로 설명하되, CLI 예시는 현재 호환 표면을 반영해 `dpc`를 병기한다.

---

## 1. 사용자 여정

### 1.1 전체 흐름

```text
설치 → 초기화 → 기록/Skill 적용 → AI 작업 → Gate 검증
```

### 1.2 기대 UX

| 단계 | 사용자 액션 | 시스템 동작 | 결과 |
|---|---|---|---|
| 설치 | CLI 설치 | bootstrap surface 준비 | 실행 가능 |
| 초기화 | `dpc init` | 설정/기록/adapter 구조 생성 | 기록 가능한 프로젝트 |
| 적용 | preset 또는 custom Skill 구성 | rules.rego 연결 | gateable workflow |
| 작업 | AI 도구 사용 | 기록과 규칙 참조 | 재현 가능한 작업 |
| 검증 | `dpc check` / hook 실행 | 누락 증거 검사 | 허용/차단 |

### 1.3 핵심 경험

사용자는 “무슨 상태인지”보다 **무슨 증거가 부족한지**를 먼저 본다.

예:

```text
[ ReproGate Missing Requirements ]
✅ 작업 계획 기록
❌ 의사결정 기록
❌ 검증 흔적
```

즉 UX의 중심은 state dashboard보다 **missing requirements dashboard**에 가깝다.

---

## 2. 핵심 명령 표면

> 아래 명령명은 현재 legacy CLI 표면을 기준으로 기록한다.

### 2.1 `dpc init`

프로젝트에 ReproGate 실행 표면을 초기화한다.

역할:
- config 생성
- 기본 기록/Skill 구조 생성
- adapter scaffold 생성

예상 결과:
- `.dpc/config.yaml`
- `.dpc/methodology/guidelines.md`
- `.dpc/methodology/rules.rego`
- tool adapter files

### 2.2 `dpc generate`

선택한 설정을 기준으로 adapter와 bootstrap 파일을 생성한다.

역할:
- target repository에 문서/스크립트/템플릿 복사
- 도구별 연결 표면 생성

### 2.3 `dpc check`

현재 규칙과 기록이 요구하는 증거가 충족되는지 검사한다.

역할:
- OPA/Rego 평가
- 누락된 기록/산출물 식별
- 허용/차단 근거 반환

### 2.4 보조 명령

- 상태/적용 상태 확인
- preset scaffold 생성
- preset validate

이들은 모두 **기록/Skill/Gate 생태계 유지**를 돕는 보조 명령이다.

---

## 3. 기록 모델

### 3.1 왜 기록이 기본 기능인가

작업 패턴을 강제하려면 규칙이 검사할 수 있는 증거가 필요하다.

따라서 ReproGate의 기록 모델은 부가 기능이 아니라 핵심 기능이다.

### 3.2 기록 범주

| 범주 | 질문 |
|---|---|
| 작업 계획 기록 | 무엇을 하려는가? 범위와 완료조건은 무엇인가? |
| 의사결정 기록 | 왜 그렇게 판단했는가? 어떤 대안을 버렸는가? |
| 설계 기록 | 무엇을 만들 구조인가? |
| 변경 기록 | 무엇이 바뀌었는가? |
| 검증 기록 | 무엇이 증명되었는가? |

### 3.3 상태 저장과의 차이

런타임 상태는 재개를 돕지만, 판단을 설명하지 못한다.

ReproGate 설계에서:
- runtime state = 보조
- work records = 강제와 설명의 기준선

---

## 4. Skill / Preset 모델

### 4.1 Skill

하나의 작업 패턴 단위.

구성:
- `guidelines.md`
- `rules.rego`

### 4.2 Preset / Workflow

여러 Skill을 작업 유형별로 묶은 적용 단위.

예:
- bugfix
- feature
- refactor
- design-change

### 4.3 기대 동작

```text
기록이 쌓인다
  ↓
좋은 반복 패턴이 보인다
  ↓
Skill로 승격한다
  ↓
Preset/Workflow로 묶는다
  ↓
이후 작업에서 Gate가 강제한다
```

---

## 5. Gate 엔진 설계

### 5.1 역할

Gate는 “규칙이 있는가”만 보는 것이 아니라, **규칙이 요구하는 증거가 실제로 존재하는가**를 본다.

### 5.2 입력

예상 입력:

```yaml
trigger: write | edit | bash | commit
target:
  file: path/to/file
records:
  available:
    - design
    - decision
    - verification
context:
  tool: claude
  mode: implementation
```

### 5.3 출력

```json
{
  "allowed": false,
  "deny": [
    "의사결정 기록이 필요합니다",
    "검증 흔적이 없습니다"
  ],
  "warn": []
}
```

### 5.4 집행 방식

- hook 시점 차단
- commit 전 차단
- 명시적 `check` 시 차단 이유 보고

---

## 6. Adapter 설계

### 6.1 목표

같은 Skill / Rule / Record 모델을 여러 도구에 연결한다.

### 6.2 원칙

- 제품 정의는 도구 기능명보다 상위여야 한다
- adapter는 연결 표면이지 제품 핵심이 아니다
- 특정 도구 종속성이 제품 정체성을 지배하면 안 된다

### 6.3 지원 형태

| 형태 | 설명 |
|---|---|
| 공식 adapter | hooks, settings, entrypoint |
| prompt adapter | 비공식 도구에 대한 적응 힌트 |
| repo adapter | 기록 경로와 저장소 규칙 연결 |

---

## 7. 프리셋/설정 UX

### 7.1 설정 원칙

사용자가 모든 규칙을 직접 코딩할 필요는 없다.

기본 경로:
1. preset 선택
2. AI와 협업하며 guidelines/rules 보강
3. 반복되면 Skill로 승격

### 7.2 설정 파일 역할

설정 파일은 “상태 저장”이 아니라,
어떤 Skill과 Gate 구조를 적용할지 정하는 **컴파일 입력**이다.

---

## 8. 예시 시나리오

### 8.1 기능 개발

1. 기능 작업 시작
2. 작업 계획 기록 생성
3. 설계 기록 확인
4. 구현 시도
5. Gate가 누락된 검증 흔적 차단
6. 검증 후 진행

### 8.2 팀 표준화

1. 리드가 반복적으로 필요한 패턴 발견
2. Skill 추가
3. 저장소에 커밋
4. 팀원 도구에 동일 규칙 적용
5. 결과물 편차 감소

---

## 9. 설계 요약

ReproGate 제품 설계의 핵심은 다음이다.

- 작업 기록이 기본 기능이다
- Skill은 기록에서 나온다
- Gate는 기록과 산출물을 검사한다
- preset은 Skill 묶음이다
- runtime state는 보조이지 중심이 아니다
- UX는 “무엇이 빠졌는가”를 보여주는 데 집중한다

## Related

- [final-definition.md](../strategy/final-definition.md)
- [vision.md](../strategy/vision.md)
- [presets-spec.md](./presets-spec.md)
- [ADR-DPC-007](../adr/ADR-DPC-007-rules-engine-selection.md)
