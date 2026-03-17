# Work Packets Index

> Last Updated: 2026-03-17
> Control Board: `docs/work-packets/`

## 0. Program Plan

- [dpc Constitution](../governance/constitution.md)
- [운영체계 구축 상위 계획](../governance/ops-bootstrap-master-plan.md)
- [Architecture](../design/architecture.md)
- [ADR-DPC-007 OPA/Rego 채택](../adr/ADR-DPC-007-rules-engine-selection.md)
- [AI Ops CHANGELOG](../CHANGELOG.md)

## 1. Active

| Packet ID | Title | Status | Priority | Updated |
|-----------|-------|--------|----------|---------|
| [WP-001](./WP-DPC-2026-03-001-ai-ops-bootstrap.md) | 운영체계 구축 부트스트랩 | IN_PROGRESS | P0 | 2026-03-17 |

## 2. Done

| Packet ID | Title | Status | Updated |
|-----------|-------|--------|---------|
| [WP-002](./WP-DPC-2026-03-002-codex-omx-alignment.md) | Codex+OMX 조합 정렬 | DONE | 2026-03-09 |
| [WP-003](./WP-DPC-2026-03-003-framework-extraction.md) | 프레임워크 추출 | DONE | 2026-03-11 |
| [WP-004](./WP-DPC-2026-03-004-public-history-replay-plan.md) | 히스토리 리플레이 | DONE | 2026-03-11 |
| [WP-005](./WP-DPC-2026-03-005-external-canonical-migration-inventory.md) | 마이그레이션 인벤토리 | DONE | 2026-03-12 |
| [WP-006](./WP-DPC-2026-03-006-public-strategy-docs.md) | 전략 문서 | DONE | 2026-03-12 |
| [WP-007](./WP-DPC-2026-03-007-presets-system-design.md) | presets 시스템 설계 | DONE | 2026-03-17 |
| [WP-008](./WP-DPC-2026-03-008-rules-dsl-design.md) | rules DSL 설계 | SUPERSEDED | 2026-03-17 |

## 3. Next (구현 예정)

- **Gate 엔진 구현**: OPA 통합, `dpc check` 명령어
- **기본 프리셋**: `minimal`, `tdd` rules.rego 작성

## 4. Hard Rules

요구사항 변경 시 **같은 세션에서 동시 갱신**:
1. 본 인덱스(`index.md`)
2. `../CHANGELOG.md`
3. 정책 변경 시 ADR

근거: [ADR-DPC-001](../adr/ADR-DPC-001-bootstrap-requirement-change-sync.md)
