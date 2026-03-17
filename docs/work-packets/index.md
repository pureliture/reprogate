# Work Packets Index

> Last Updated: 2026-03-17 (WP-015 SUPERSEDED by ADR-007, WP-014 DONE)
> Control Board: `docs/work-packets/`

## 0. Program Plan

- [dpc Constitution](../constitution.md)
- [운영체계 구축 상위 계획](../ops-bootstrap-master-plan.md)
- [ADR-DPC-003](../adr/ADR-DPC-003-conditional-team-activation-and-optout.md)
- [ADR-DPC-005](../adr/ADR-DPC-005-codex-entrypoint-ownership-and-ai-assistant-decoupling.md)
- [ADR-DPC-006](../adr/ADR-DPC-006-dpc-config-schema.md)
- [프로세스 기반 dpc Command](../commands/dpc.md)
- [프로세스 강제 매트릭스](../tool-hooks/process-enforcement-matrix.md)
- [최소 논리 역할 세트](../process-catalog/minimum-logical-role-set.md)
- [Workspace Profiles](../workspace-profiles/README.md)
- [AI Tool Artifact Boundary](../portability/ai-tool-artifact-boundary.md)
- [AI Ops CHANGELOG](../CHANGELOG.md)

## 1. Active

| Packet ID | Title | Status | Current | Next | Priority | Updated |
|------|------|------|------|------|------|------|
| [WP-DPC-2026-03-001](./WP-DPC-2026-03-001-ai-ops-bootstrap.md) | AI 협업 운영체계 구축 부트스트랩 | IN_REFINEMENT | P1 | P3 | P0 | 2026-03-07 |
| [WP-DPC-2026-03-002](./WP-DPC-2026-03-002-codex-omx-alignment.md) | Codex+OMX 조합 정렬 | IN_DEVELOPMENT | P3 | S1 | P0 | 2026-03-09 |
| [WP-DPC-2026-03-004](./WP-DPC-2026-03-004-public-history-replay-plan.md) | ai-ops public repo replay history plan | IN_REFINEMENT | P1 | P3 | P1 | 2026-03-11 |
| [WP-DPC-2026-03-006](./WP-DPC-2026-03-006-public-strategy-docs.md) | external ai-ops public strategy docs | IN_DEVELOPMENT | P3 | S1 | P1 | 2026-03-12 |
| [WP-DPC-2026-03-005](./WP-DPC-2026-03-005-external-canonical-migration-inventory.md) | external ai-ops canonical migration inventory | IN_REFINEMENT | P1 | P3 | P0 | 2026-03-12 |
| [WP-DPC-2026-03-007](./WP-DPC-2026-03-007-presets-system-design.md) | presets 시스템 설계 | DONE | P2 | - | P1 | 2026-03-17 |
| [WP-DPC-2026-03-002](./WP-DPC-2026-03-008-rules-dsl-design.md) | rules DSL 설계 | SUPERSEDED | - | - | - | 2026-03-17 |

## 2. On Hold

- 없음

## 3. Historical / Done

- WP-DPC-2026-03-002 ~ 009: **DONE** (archived, see CHANGELOG)

## 4. High Priority Queue

- [WP-DPC-2026-03-001](./WP-DPC-2026-03-001-ai-ops-bootstrap.md) (P0): 운영체계 구축 기준선 확정 및 단계 실행
- [WP-DPC-2026-03-002](./WP-DPC-2026-03-002-codex-omx-alignment.md) (P3): Claude+OMC SoT 구조 적용 구현

## 5. Parent / Child Topology

- Parent: [WP-DPC-2026-03-001](./WP-DPC-2026-03-001-ai-ops-bootstrap.md)
  - Phase 1-5: WP-002 ~ 007 **DONE**
  - Phase 6: [WP-DPC-2026-03-002](./WP-DPC-2026-03-002-codex-omx-alignment.md) (Codex+OMX 운영 정렬)
  - Track 9: [WP-DPC-2026-03-003](./WP-DPC-2026-03-003-framework-extraction.md) **DONE**
  - Track 10: [WP-DPC-2026-03-004](./WP-DPC-2026-03-004-public-history-replay-plan.md)
  - Track 11: [WP-DPC-2026-03-005](./WP-DPC-2026-03-005-external-canonical-migration-inventory.md)

## 6. Hard Rules (Mandatory)

요구사항이 변경되면 아래를 **같은 세션에서 동시 갱신**한다.

1. 부모 WP 및 영향받는 자식 WP
2. 본 인덱스(`index.md`)
3. `../CHANGELOG.md`
4. 정책 변경 시 ADR
5. 상위 계획 문서(`ops-bootstrap-master-plan.md`)
6. 헌법 문서(`constitution.md`)

위 동기화가 끝나기 전에는 상태 전이(`current_process` 변경)를 금지한다.
근거 규칙: [ADR-DPC-001](../adr/ADR-DPC-001-bootstrap-requirement-change-sync.md)
