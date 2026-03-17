# Work Packets Index

> Last Updated: 2026-03-17
> Control Board: `docs/work-packets/`
> Canonical Definition: [ReproGate 최종 정의](../strategy/final-definition.md)

## 0. Program Plan

- [ReproGate Constitution](../governance/constitution.md)
- [ReproGate Governance Master Plan](../governance/ops-bootstrap-master-plan.md)
- [ReproGate Architecture](../design/architecture.md)
- [ADR-DPC-007 OPA/Rego 채택](../adr/ADR-DPC-007-rules-engine-selection.md)
- [Integrated CHANGELOG](../CHANGELOG.md)

## 1. Active

| Packet ID | Title | Status | Priority | Updated |
|-----------|-------|--------|----------|---------|
| [WP-001](./WP-DPC-2026-03-001-ai-ops-bootstrap.md) | ReproGate 기록 기반 엔지니어링 부트스트랩 | IN_PROGRESS | P0 | 2026-03-17 |
| [WP-010](./WP-DPC-2026-03-010-gate-engine-implementation.md) | ReproGate Gate 엔진 구현 | READY | P0 | 2026-03-17 |

## 2. Done

| Packet ID | Title | Status | Updated |
|-----------|-------|--------|---------|
| [WP-009](./WP-DPC-2026-03-009-product-design-spec.md) | ReproGate 제품 설계 구체화 | DONE | 2026-03-17 | 4인 팀 리뷰 + 재설계 완료 |
| [WP-002](./WP-DPC-2026-03-002-codex-omx-alignment.md) | Codex+OMX 조합 정렬 | DONE | 2026-03-09 |
| [WP-003](./WP-DPC-2026-03-003-framework-extraction.md) | 프레임워크 추출 | DONE | 2026-03-11 |
| [WP-004](./WP-DPC-2026-03-004-public-history-replay-plan.md) | 히스토리 리플레이 | DONE | 2026-03-11 |
| [WP-005](./WP-DPC-2026-03-005-external-canonical-migration-inventory.md) | 마이그레이션 인벤토리 | DONE | 2026-03-12 |
| [WP-006](./WP-DPC-2026-03-006-public-strategy-docs.md) | ReproGate 전략 문서 | DONE | 2026-03-17 |
| [WP-007](./WP-DPC-2026-03-007-presets-system-design.md) | ReproGate presets / Skills 시스템 설계 | DONE | 2026-03-17 |

## 3. Next (구현 예정)

- **Gate 엔진 구현**: work-record-aware OPA integration, `dpc check` evidence evaluation
- **기본 프리셋**: `minimal`, `tdd`, record-aware Skill bundles 정리

## 4. Hard Rules

요구사항 변경 시 **같은 세션에서 동시 갱신**:
1. 본 인덱스(`index.md`)
2. `../CHANGELOG.md`
3. 정책 변경 시 ADR

근거: [ADR-DPC-001](../adr/ADR-DPC-001-bootstrap-requirement-change-sync.md)
