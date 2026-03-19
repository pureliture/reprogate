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

### 0.5 legacy naming note (Deprecated)

기존 문서와 저장소에 남아 있던 `dpc` CLI/경로는 이제 공식적으로 `reprogate`로 통합된다. 이 문서부터 `reprogate` 명칭을 일관되게 적용한다.

---

## 1. 사용자 여정 (Multi-entry 지원)

### 1.1 유연한 진입로

사용자는 **어떤 구조로 시작할지** 자유롭게 선택할 수 있다.

- **Workflow-first**: 준비된 워크플로를 따르며 시작
- **Skill-first**: 필요할 때 특정 Skill 1~N개만 호출하여 적용
- **Freeform-first**: 의식적 구조 없이 대화로 시작 (나중에 기록/Skill로 승격)
- **External-first**: 기존 외부 도구나 저장소를 활용하며 시작

### 1.2 전체 흐름 (표준 경로 예시)

```text
설치 → 초기화 → [자유 대화 / Skill 적용 / Workflow 진행] → 기록/승격(Late Binding) → Gate 검증
```

### 1.2 기대 UX

| 단계 | 사용자 액션 | 시스템 동작 | 결과 |
|---|---|---|---|
| 설치 | CLI 설치 | bootstrap surface 준비 | 실행 가능 |
| 초기화 | `reprogate init` | 설정/기록/adapter 구조 생성 | 기록 가능한 프로젝트 |
| 적용 | preset 또는 custom Skill 구성 | rules.rego 연결 | gateable workflow |
| 작업 | AI 도구 사용 | 기록과 규칙 참조 | 재현 가능한 작업 |
| 검증 | `reprogate check` / hook 실행 | 누락 증거 검사 | 허용/차단 |

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

### 2.1 `reprogate init`

프로젝트에 ReproGate 실행 표면을 초기화한다.

역할:
- config 생성
- 기본 기록/Skill 구조 생성
- adapter scaffold 생성

예상 결과:
- `.reprogate/config.yaml`
- `.reprogate/methodology/guidelines.md`
- `.reprogate/methodology/rules.rego`
- tool adapter files

### 2.2 `reprogate generate`

선택한 설정을 기준으로 adapter와 bootstrap 파일을 생성한다.

역할:
- target repository에 문서/스크립트/템플릿 복사
- 도구별 연결 표면 생성

### 2.3 `reprogate check`

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

### 3.3 상태 저장과의 차이 및 Storage Agnosticism

런타임 상태는 재개를 돕지만, 판단을 설명하지 못한다.

ReproGate 설계에서:
- runtime state = 보조
- work records = 강제와 설명의 기준선 (**Record Identity**)

또한, 이 기록들이 **어디에 어떻게 저장되는가(built-in vs Notion/Git 등)**는 부차적이다. 핵심은 메타데이터 계약(누가, 언제, 왜 결정했는가)을 유지하는 것이다.

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
- **Reproducibility-first**: 차단은 워크플로 사용 여부가 아닌 증거(기록/결정/검증) 누락을 기준으로 발생한다.

---

## 6. Adapter 설계

### 6.1 목표

같은 Skill / Rule / Record 모델을 여러 도구에 연결한다.

### 6.2 3층 바운더리 모델에 따른 위상

- **Layer 1 (Core)**: 기록 단위, Skill 이력, Rule 평가는 Adapter 단에서 무시할 수 없다.
- **Layer 2 (Flexible)**: Adapter는 도구 편의성에 맞춰 저장소 구조, 세션 UX를 유연하게 제공할 수 있다.
- **Layer 3 (Integration)**: 도구 고유 기능(IDE, LLM Runtime)은 Adapter에 흡수하지 않고 연결만 한다.

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
- [preset-bundle-spec.md](./preset-bundle-spec.md)
- [ADR-002-rules-engine-selection.md](../../records/adr/ADR-002-rules-engine-selection.md)
