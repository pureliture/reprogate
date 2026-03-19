# ReproGate Spec Layer

이 디렉토리는 `docs/strategy/`에서 정의된 제품 정체성/바운더리/시나리오를
구현 가능한 명세로 내리는 레이어다.

원칙:
- strategy는 "무엇이어야 하는가"
- spec은 "어떤 입력/출력/상태/계약으로 구현할 것인가"
- implementation은 spec 없이 직접 merge하지 않는다

현재 spec 문서:
- product-surface-spec.md: CLI 명령어 및 제품 노출 표면 명세
- preset-bundle-spec.md: 프리셋 및 Skill 번들링 구조 명세
- record-contract.md
- rule-gate-spec.md
- skill-workflow-object-model.md
- storage-adapter-spec.md
- governance-scope-spec.md
