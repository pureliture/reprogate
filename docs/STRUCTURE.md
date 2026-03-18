# ReproGate Documentation Structure

ReproGate 문서는 다음 4개 레이어로 구분한다.

## `docs/strategy/`

제품의 정체성, 범위, 비전, 로드맵, 시나리오를 정의한다.

질문:
- ReproGate는 무엇이어야 하는가?
- 어디까지를 제품 책임으로 볼 것인가?
- 어떤 사용자 시나리오와 entry mode를 우선할 것인가?

대표 문서:
- `final-definition.md`
- `vision.md`
- `roadmap.md`
- `product-boundary.md`
- `scenarios.md`

## `docs/spec/`

strategy에서 정의된 방향을 구현 가능한 계약으로 내린다.

질문:
- 어떤 입력/출력/상태/계약이 필요한가?
- 어떤 object model / policy input / scope model을 표준화할 것인가?
- implementation이 의존할 canonical contract는 무엇인가?

대표 문서:
- `record-contract.md`
- `rule-gate-spec.md`
- `skill-workflow-object-model.md`
- `storage-adapter-spec.md`
- `governance-scope-spec.md`
- `product-surface-spec.md`
- `preset-bundle-spec.md`

## `docs/design/`

실제 구현 구조와 모듈/실행 표면 설계를 다룬다.

질문:
- 어떤 모듈 구조와 실행 표면으로 구현할 것인가?
- bootstrap / generator / gatekeeper를 어떻게 구성할 것인가?
- spec을 코드/스크립트/템플릿으로 어떻게 옮길 것인가?

대표 문서:
- `architecture.md`
- `README.md`

## `records/`

RFC/ADR 등 제품 결정 이력을 저장한다.

질문:
- 왜 이런 구조/규칙/방향을 채택했는가?
- 어떤 대안을 버렸는가?
- 이후 문서/구현이 어떤 결정을 따라야 하는가?

---

## Canonical Rule

- `strategy`는 **무엇/왜**를 정의한다.
- `spec`은 **어떤 계약으로 구현할지**를 정의한다.
- `design`은 **어떤 구조로 구현할지**를 정의한다.
- `records`는 **왜 그렇게 결정했는지**를 남긴다.

## Transitional Note

기존 `docs/design/product-spec.md`, `docs/design/presets-spec.md`는 과거 위치에 남아 있는 legacy 문서다.
이제부터 canonical 위치는 아래와 같다.

- `docs/design/product-spec.md` → `docs/spec/product-surface-spec.md`
- `docs/design/presets-spec.md` → `docs/spec/preset-bundle-spec.md`

후속 정리 PR에서 legacy 경로 제거 또는 deprecation 처리할 수 있다.
