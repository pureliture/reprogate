# ReproGate 제품 바운더리

> Canonical Definition: [final-definition.md](../strategy/final-definition.md)
> 관련 RFC: [RFC-003](../../records/rfc/RFC-003-product-boundary.md)

---

## 제품 경계 한 줄 정의

> **ReproGate는 사용자가 workflow·skill·freeform·external storage 중 어떤 방식으로 시작하든, 그 작업을 추적 가능한 기록 단위로 붙잡고 필요 시 구조화하여 Skill과 Rule로 연결함으로써 재현 가능한 작업 방식으로 컴파일하는 제품이다.**

---

## 1. ReproGate가 하는 것 / 안 하는 것

### 한다 (In Scope)

| # | 구체적으로 | 근거 |
|---|---|---|
| **IN-1** | 작업이 기록 단위로 추적되게 만든다 | 기록이 없으면 Gate가 검사할 증거가 없다 |
| **IN-2** | Skill을 독립 단위로 호출·적용·추적한다 | Skill은 workflow의 부속이 아니라 독립 방법론 단위 |
| **IN-3** | Gate가 재현성 결손(기록·결정·검증 누락)을 기준으로 차단한다 | 도구 사용 여부가 아니라 증거 부재가 차단 사유 |
| **IN-4** | Workflow 없이도, freeform에서도 동작한다 | 구조 도입 시점은 사용자가 결정 |
| **IN-5** | freeform 작업을 나중에 기록/Skill 단위로 승격시킨다 (Late Binding) | 구조화가 늦어도 재현성은 확보 가능해야 한다 |
| **IN-6** | Workflow를 수정/우회한 사실 자체를 기록한다 (Deviation Awareness) | 우회는 허용하되 흔적은 남아야 한다 |
| **IN-7** | 명시적 workflow 없어도 현재 작업 상태와 다음 후보를 보여준다 (Flowboard) | skill chain에서 암묵적 흐름을 구성 |

### 안 한다 (Out of Scope)

| # | 구체적으로 | 이유 |
|---|---|---|
| **OUT-1** | Workflow를 강제로 밀어붙이지 않는다 | ReproGate는 workflow runner가 아니라 methodology compiler |
| **OUT-2** | 코드 작성·실행 자체를 하지 않는다 | 실행기가 아님 |
| **OUT-3** | 특정 저장 위치/포맷을 강제하지 않는다 | 저장 방식은 사용자 자유, record contract만 유지 |
| **OUT-4** | 특정 AI 도구에 종속되지 않는다 | Adapter boundary 유지 |
| **OUT-5** | 무거운 상태 머신을 운영하지 않는다 | artifact-driven이지 state-driven이 아님 |
| **OUT-6** | 문서의 양을 늘리는 것을 목표로 하지 않는다 | 목적은 강제 가능한 증거, 양이 아님 |

---

## 2. 최소 불변 계약 (깨지면 제품이 아닌 것)

어떤 시나리오에서든, 아래 5개가 하나라도 빠지면 ReproGate가 아니다.

| ID | 계약 | 구체적 의미 |
|---|---|---|
| **CI-1** | 작업 기록 추적 | 어떤 진입 모드에서든 "이 작업이 어떤 기록 단위인지" 남아야 한다 |
| **CI-2** | Late Structure Binding | 처음에 구조 없이 시작해도, 나중에 기록을 Skill/Rule과 연결할 수 있어야 한다 |
| **CI-3** | Skill 적용 이력 | Skill을 한 번만 호출하고 끝나도 그 호출이 기록과 연결되어야 한다 |
| **CI-4** | 저장 위치 무관 Rule 평가 | 메타데이터 계약만 맞으면 어디에 저장하든 Rule 평가 가능 |
| **CI-5** | 재현성 기준 게이트 | "워크플로 안 썼다"가 아니라 "기록/결정/검증 없다"가 차단 사유 |

---

## 3. 진입 모드별 제품 행동 (구체적 결정)

### A. Workflow-first로 시작할 때

| 사용자 행동 | ReproGate **한다** | ReproGate **안 한다** |
|---|---|---|
| 워크플로를 그대로 따른다 | 단계별 기록 검사, 게이트 실행 | 워크플로를 유일한 정답으로 제시 |
| 워크플로 단계를 수정한다 | deviation 자체를 기록, 변경 후 재평가 | 수정을 비정상으로 차단 |
| 워크플로 단계를 건너뛴다 | 건너뛴 사실 기록, 필수 증거만 게이트 | 빈 단계를 에러 처리 |

### B. Skill-first로 시작할 때

| 사용자 행동 | ReproGate **한다** | ReproGate **안 한다** |
|---|---|---|
| Skill 1개만 호출하고 종료 | skill trace 기록, 작업 기록 연결 | 워크플로 미사용을 문제시 |
| 긴 세션에서 Skill N개 사용 | skill timeline 구성, flowboard로 암묵적 흐름 시각화 | 워크플로 선언 강제 |

### C. Freeform으로 시작할 때

| 사용자 행동 | ReproGate **한다** | ReproGate **안 한다** |
|---|---|---|
| 구조 없이 자유 대화만 | 최소 raw trace 유지, 비간섭적 제안 | 워크플로/Skill 선택 강매 |
| 중간에 갑자기 스킬 호출 | freeform trace → 기록/skill 승격 (late binding) | 이전 대화를 구조화 안 된 상태로 방치 |
| 끝까지 구조 안 쓴다 | raw trace만 보존, 나중에 승격 가능한 상태 유지 | 구조 미사용에 페널티 부과 |

### D. 저장 방식 커스터마이징

| 사용자 행동 | ReproGate **한다** | ReproGate **안 한다** |
|---|---|---|
| built-in 저장 사용 | 기본 제공, record contract 자동 충족 | — |
| built-in 거부 | 메타데이터 계약(record identity, timestamp, decision linkage) 제공 | 특정 저장소/포맷 강제 |
| built-in + external 혼합 | canonical metadata layer 제공 | source-of-truth 정책 결정을 대신 |

> [!NOTE]
> 저장 커스터마이징의 **구현 설계** (external adapter, sync 정책, contract schema)는 별도 RFC에서 다룬다.

---

## 4. Gate 차단 기준 (구체적 결정)

### 차단한다 (재현성 결손)

- 작업 기록이 없다 (형식 무관, 추적 가능한 기록 단위가 존재하지 않음)
- 의사결정 근거가 없다 (왜 이렇게 판단했는지 흔적이 없음)
- 검증 흔적이 없다 (무엇을 확인했는지 증거가 없음)
- required skill에 대한 적용 trace가 없다

> [!NOTE]
> 차단 기준은 **기록 범주**(작업 계획, 의사결정, 검증)로 정의한다.
> 특정 템플릿 형식(RFC, ADR 등)이나 저장 방식에 종속되지 않는다.

### 차단하지 않는다

- Workflow를 안 썼다
- Built-in 저장소를 안 썼다
- Skill을 선택하지 않았다 (freeform 상태)
- 특정 도구를 안 썼다
- 특정 템플릿 형식을 따르지 않았다

---

## 5. 3층 바운더리 모델

| 층 | 내용 | 바꿀 수 있는가 |
|---|---|---|
| **Core** | 기록 단위, 의사결정 흔적, Skill 이력, Rule 평가, 재현성 계약 | ❌ 불변 |
| **Flexible** | Workflow 정의, Gate 강도, Skill 선택 방식, 시각화, 세션 UX, 저장 백엔드, 네이밍 | ✅ 사용자/조직 선택 |
| **Integration** | IDE/CLI, LLM 런타임, Rule 엔진, CI/CD, 외부 저장소, 오케스트레이터 | ✅ 연결면, 흡수 안 함 |

---

## 6. 제품 원칙 (7개)

| ID | 원칙 | 요약 | 근거 (§1~4) |
|---|---|---|---|
| **P-1** | Record Identity | 모든 작업은 추적 가능한 기록 단위를 가진다. 형식은 자유 | IN-1, CI-1 |
| **P-2** | Late Entry | 구조 도입을 늦춰도 나중에 기록/Skill 단위로 승격 가능 | IN-4, IN-5, CI-2 |
| **P-3** | Deviation Awareness | workflow 우회는 허용하되 그 사실 자체가 기록된다 | IN-6, §3-A |
| **P-4** | Storage Agnosticism | 저장 방식은 자유, record contract만 유지 | CI-4, OUT-3 |
| **P-5** | Reproducibility Gate | 차단 기준은 재현성 결손(기록·결정·검증 부재)이지, 도구·템플릿·workflow 사용 여부가 아님 | IN-3, CI-5, §4 |
| **P-6** | Skill Independence | Skill은 workflow의 부속이 아니라 독립적 방법론 단위 | IN-2, CI-3, §3-B |
| **P-7** | Emergent Flow | 명시적 workflow 없어도 기록/Skill chain에서 현재 상태와 다음 후보를 도출한다 | IN-7, §3-B |

> [!NOTE]
> 원칙은 **특정 템플릿(RFC/ADR), 저장 형식, 도구명에 종속되지 않는다.**
> 이 원칙이 깨지면 ReproGate는 "특정 포맷을 쓰게 강제하는 도구"로 축소된다.

---

## 7. 필수 요구사항

| ID | 요구사항 | In/Out 영향 |
|---|---|---|
| **R1** | Multi-entry | 4가지 진입 모드 모두 지원 (IN-4) |
| **R2** | Late structure binding | freeform→structured 승격 (IN-5) |
| **R3** | Workflow deviation awareness | deviation 기록 (IN-6) |
| **R4** | Skill traceability | 단발/다회 모두 기록 연결 (IN-2) |
| **R5** | Storage abstraction | 저장 강제 안 함, contract만 (별도 RFC) |
| **R6** | Reproducibility-first gate | 재현성 결손 기준 차단 (IN-3) |
| **R7** | Flowboard | workflow 없어도 상태/다음 후보 표시 (IN-7) |

---

## 8. 시나리오 카탈로그 템플릿

```markdown
## SC-NNN: [시나리오 이름]

### 맥락
- **시작 모드**: workflow / skill / freeform / external
- **전환 여부**: 있음 / 없음 (전환 경로)
- **세션 길이**: 단발 / 장기 / 누적
- **저장 선호**: built-in / external / 혼합
- **강제 수준**: 안내 / soft / hard / CI

### 사용자의 거부 포인트
### ReproGate 최소 개입
### ReproGate 필수 책임
### 허용 가능한 우회
### 절대 허용 불가한 계약 위반
### 최종 산출물
### 추출 가능한 Skill
### 적용 가능한 Rule
```

---

## 9. 기존 문서와의 관계

| 문서 | 관계 |
|---|---|
| [final-definition.md](final-definition.md) | Core Identity 유지. 바운더리는 적용 범위를 추가 |
| [product-surface-spec.md](../spec/product-surface-spec.md) | 기능 설계의 적용 경계를 이 문서가 정의 |
| [architecture.md](../design/architecture.md) | 3층 모델이 아키텍처 확장 가능성을 정의 |
| [preset-bundle-spec.md](../spec/preset-bundle-spec.md) | Skill/Preset은 Flexible 층에 위치 |

---

## 10. 다음 단계

### 즉시 (제품 구체화)

1. **전략 문서 갱신**
   - [roadmap.md](roadmap.md) — Near-Term에 바운더리 반영, Mid-Term을 Multi-entry/Late binding 관점으로 재정의
   - [vision.md](vision.md) — Design Commitments에 원칙 P-1~P-5 반영
2. **설계 문서 정합성**
   - [product-surface-spec.md](../spec/product-surface-spec.md) — legacy `dpc` 정리 + 바운더리 정합
   - [architecture.md](../design/architecture.md) — 3층 모델 반영
3. **시나리오 카탈로그** — 15개 구체 시나리오 축적

### 이후 (제품 구체화 완료 후)

4. **저장 커스터마이징 RFC** — Storage abstraction 구현 설계

### Deferred (제품 정의 안정 후)

5. **Stage 2: Distribution** — 제품이 "무엇을 배포하는가"가 명확해진 뒤에 착수

> [!IMPORTANT]
> Stage 2는 부트스트랩 기능 구현(init/generate/check CLI, npm 패키지화, Preset 시스템)이다.
> 제품 바운더리와 시나리오 카탈로그가 안정되지 않은 상태에서 배포 구조를 잡으면
> "무엇을 배포하는가"가 흐려진다. 제품 구체화가 선행되어야 한다.
