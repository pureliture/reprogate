# ReproGate Design Layer

`docs/design/`는 strategy/spec에서 닫힌 내용을
실제 구현 구조와 실행 표면으로 내리는 문서를 둔다.

## 이 레이어가 답하는 질문

- 어떤 모듈 구조로 구현할 것인가?
- 어떤 CLI / bootstrap / generator / gatekeeper 표면이 필요한가?
- spec을 코드/스크립트/템플릿으로 어떻게 옮길 것인가?

## Canonical Documents

- `architecture.md`

## Legacy Documents

아래 문서는 과거 `design/`에 위치했지만,
이제는 canonical 위치가 `docs/spec/`로 이동했다.

- `product-spec.md` → `../spec/product-surface-spec.md`
- `presets-spec.md` → `../spec/preset-bundle-spec.md`

후속 cleanup PR에서 legacy 경로 제거 또는 deprecation 처리할 수 있다.
