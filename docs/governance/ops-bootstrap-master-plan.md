# ReproGate Governance Master Plan

> Status: Active  
> Last Updated: 2026-03-17  
> Canonical Definition: [final-definition.md](../strategy/final-definition.md)  
> Product Vision: [vision.md](../strategy/vision.md)  
> Product Roadmap: [roadmap.md](../strategy/roadmap.md)  
> Parent WP: [WP-DPC-2026-03-001](../work-packets/WP-DPC-2026-03-001-ai-ops-bootstrap.md)  
> Governing ADR: [ADR-DPC-001](../adr/ADR-DPC-001-bootstrap-requirement-change-sync.md)  
> Constitution: [ReproGate Constitution](./constitution.md)  

## 1. 문서 역할

이 문서는 **제품 비전 문서가 아니라 저장소 운영용 프로그램 계획 문서**다.

- `final-definition.md`는 제품의 정체성을 정의한다.
- `vision.md`는 왜 ReproGate가 필요한지 설명한다.
- `roadmap.md`는 제품 방향과 우선순위를 설명한다.
- **이 문서(master plan)** 는 그 정의와 방향을 이 저장소의 거버넌스, 설계, 구현 계획에 어떻게 주입하고 실행할지를 관리한다.

즉, master plan은 roadmap과 중복되는 전략 소개 문서가 아니라, **control-board 성격의 실행 계획 문서**이기 때문에 `docs/governance/` 아래에 유지한다.

## 2. 왜 master plan이 필요한가

비전과 로드맵만으로는 다음을 관리하기 어렵다.

1. 어떤 문서군을 어떤 순서로 정렬할 것인가
2. 어떤 변경이 역사 보존 대상이고 어떤 변경이 살아 있는 정의 변경인가
3. 어떤 work packet / ADR / changelog가 같은 세션에서 함께 갱신되어야 하는가
4. 제품 철학과 저장소 운영 규칙을 어디서 분리해 설명할 것인가

ReproGate는 기록 기반 엔지니어링을 지향하므로, 이 저장소 자체도 **제품 정체성 주입 작업을 기록 가능한 계획 문서로 관리**해야 한다.

## 3. 현재 프로그램 목표

이 저장소의 현재 상위 목표는 다음과 같다.

1. `final-definition.md`를 ReproGate의 기준 문서(SoT)로 고정한다.
2. 살아 있는 방향성/거버넌스/설계/구현 계획 문서를 이 기준에 맞춰 정렬한다.
3. 과거 `dpc` 시기의 기록은 보존하되, 현재 제품 정체성은 `ReproGate`로 읽히게 만든다.
4. 작업 기록, Skill 축적, Rule/Gate 강제, artifact-driven workflow라는 핵심 구조가 문서 전반에서 일관되게 보이도록 한다.
5. 제품 철학과 저장소 운영 방식의 경계를 명확히 한다.

## 4. 운영 트랙

### Track A. 방향성 문서 정렬
- 대상: `README.md`, `docs/README.md`, `docs/strategy/*`, `docs/guide/*`
- 목적: 외부/내부 독자에게 ReproGate 정체성이 먼저 일치되게 보이도록 한다.
- 현재 상태: 진행 중

### Track B. 거버넌스 문서 정렬
- 대상: `docs/governance/*`
- 목적: 제품 철학과 저장소 운영 규칙의 역할 분리를 명시한다.
- 현재 상태: 진행 중

### Track C. 명세 문서 정렬
- 대상: `docs/spec/*`
- 목적: 기록 → Skill → Rule → Gate 구조가 구현 관점의 명세(Contract)로 정착되도록 한다.
- 현재 상태: 진행 중

### Track D. 실행 계획 / historical alignment
- 대상: `docs/work-packets/*`, 관련 ADR, changelog
- 목적: 과거 `dpc` 계획 문서를 ReproGate 기준 해석으로 재정렬하되, 역사적 사실은 보존한다.
- 현재 상태: 예정

## 5. 실행 구조

현재 실행은 아래 wave 순서로 진행한다.

### Wave 1. 핵심 방향성 문서
- `README.md`
- `docs/README.md`
- `docs/strategy/vision.md`
- `docs/strategy/roadmap.md`
- `docs/guide/why-dpc.md`

### Wave 2. 거버넌스 문서
- `docs/governance/constitution.md`
- `docs/governance/operating-model.md`
- `docs/governance/ops-bootstrap-master-plan.md`
- `docs/governance/goal-alignment-checklist.md`
- `docs/governance/work-packet-spec.md`

### Wave 3. 명세 문서 (Spec)
- `docs/design/architecture.md`
- `docs/spec/product-surface-spec.md`
- `docs/spec/preset-bundle-spec.md`

### Wave 4. 실행 계획 / 기록 문서
- `docs/work-packets/index.md`
- active work packets
- historical alignment work packets
- relevant ADRs
- `docs/CHANGELOG.md`

`final-definition` 주입 계획(Wave 1~5)은 2026-03-17 기준 완료되었으며, 상세 계획 문서는 제거했다.

## 6. Master Plan과 Vision/Roadmap의 경계

| 문서 | 역할 | 질문 |
|---|---|---|
| `final-definition.md` | 제품 정체성 SoT | ReproGate는 무엇인가? |
| `vision.md` | 문제/철학/도착점 | 왜 필요한가? |
| `roadmap.md` | 제품 우선순위 | 어디로 갈 것인가? |
| `ops-bootstrap-master-plan.md` | 저장소 실행 계획 | 이 저장소에서 어떻게 정렬하고 추진할 것인가? |

결론:

- master plan은 **필요하다**
- 다만 strategy 문서와 같은 톤으로 쓰면 중복되므로, **거버넌스 실행 계획 문서**로 범위를 좁혀 유지한다
- 따라서 **전략 폴더로 이동하지 않고 `docs/governance/`에 유지**한다

## 7. 망각 방지 규칙

1. 현재 세션에서 제품 정체성을 설명할 때는 `final-definition.md`를 우선 확인한다.
2. 저장소 실행 순서나 동기화 범위를 판단할 때는 이 문서를 확인한다.
3. 실제 변경 이력은 `docs/CHANGELOG.md`에 남긴다.
4. requirement 성격의 변경은 관련 work packet / ADR / index / changelog / master plan을 같은 흐름에서 함께 갱신한다.
5. historical 문서를 수정할 때는 사실 보존과 현재 해석을 분리한다.

## 8. 완료 조건

이 master plan 기준의 현재 프로그램은 아래 조건이 충족되면 한 사이클 완료로 본다.

- 기준 정의가 살아 있는 문서군 전체에 주입된다
- 거버넌스 문서가 제품 철학과 저장소 운영을 혼동하지 않는다
- 설계 문서가 ReproGate 핵심 구조를 반영한다
- 실행 계획/이력 문서가 ReproGate 기준으로 재해석된다
- legacy `dpc` 표기는 역사적 식별자/맥락으로만 남는다

## 9. 다음 액션

현재 다음 액션은 **Wave 2 거버넌스 문서 정렬 완료**다.
