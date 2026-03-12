# Work Packets Index

> Last Updated: 2026-03-12 (WP-012 P1: external canonical migration policy fixed)
> Control Board: `docs/work-packets/`

## 0. Program Plan

- [AI Ops Constitution](../constitution.md)
- [운영체계 구축 상위 계획](../ops-bootstrap-master-plan.md)
- [ADR-AIOPS-003](../adr/ADR-AIOPS-003-conditional-team-activation-and-optout.md)
- [ADR-AIOPS-005](../adr/ADR-AIOPS-005-codex-entrypoint-ownership-and-ai-assistant-decoupling.md)
- [프로세스 기반 AI Ops Command](../commands/ai-ops.md)
- [프로세스 강제 매트릭스](../tool-hooks/process-enforcement-matrix.md)
- [최소 논리 역할 세트](../process-catalog/minimum-logical-role-set.md)
- [Workspace Profiles](../workspace-profiles/README.md)
- [AI Tool Artifact Boundary](../portability/ai-tool-artifact-boundary.md)
- [AI Ops CHANGELOG](../CHANGELOG.md)

## 1. Active

| Packet ID | Title | Status | Current | Next | Priority | Updated |
|------|------|------|------|------|------|------|
| [WP-AIOPS-2026-03-001](./WP-AIOPS-2026-03-001-ai-ops-bootstrap.md) | AI 협업 운영체계 구축 부트스트랩 | IN_REFINEMENT | P1 | P3 | P0 | 2026-03-07 |
| [WP-AIOPS-2026-03-008](./WP-AIOPS-2026-03-008-codex-omx-alignment.md) | Codex+OMX 조합 정렬 | IN_DEVELOPMENT | P3 | S1 | P0 | 2026-03-09 |
| [WP-AIOPS-2026-03-011](./WP-AIOPS-2026-03-011-public-history-replay-plan.md) | ai-ops public repo replay history plan | IN_REFINEMENT | P1 | P3 | P1 | 2026-03-11 |
| [WP-AIOPS-2026-03-012](./WP-AIOPS-2026-03-012-external-canonical-migration-inventory.md) | external ai-ops canonical migration inventory | IN_REFINEMENT | P1 | P3 | P0 | 2026-03-12 |

## 2. On Hold

- 없음

## 3. Historical / Recent Done

> Closed historical packets are now archived under `docs/archive/ai-ops/work-packets/`; legacy `docs/ai-ops/work-packets/*` paths remain thin redirect stubs only.

- [WP-AIOPS-2026-03-009 Claude+OMC SoT 구조 적용](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-009-claude-omc-sot-application.md) **DONE**
- [WP-AIOPS-2026-03-010 ai-ops 프레임워크 추출 및 오픈소스화](./WP-AIOPS-2026-03-010-framework-extraction.md) **DONE** (final deletion readiness PASS, legacy namespace sunset complete)
- [WP-AIOPS-2026-03-004 문서 구조 전환](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-004-document-structure-transition.md)
- [WP-AIOPS-2026-03-003 Git hook output compliance gate](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-003-git-hook-output-compliance-gate.md)
- [WP-AIOPS-2026-03-002 AI tool hook enforcement](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-002-ai-tool-hook-enforcement.md)
- [WP-AIOPS-2026-03-007 AI 도구 산출물 경계 정렬](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-007-ai-tool-artifact-separation.md) **DONE**
- [WP-AIOPS-2026-03-006 파일럿 검증](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-006-pilot-verification.md) **DONE**
- [WP-AIOPS-2026-03-005 프로세스 기반 협업 전환](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-005-process-based-collaboration.md) **DONE**

## 4. High Priority Queue

- [WP-AIOPS-2026-03-001](./WP-AIOPS-2026-03-001-ai-ops-bootstrap.md) (P0): 운영체계 구축 기준선 확정 및 단계 실행
- [WP-AIOPS-2026-03-008](./WP-AIOPS-2026-03-008-codex-omx-alignment.md) (P3): Claude+OMC SoT 구조 적용 구현

## 5. Parent / Child Topology

- Parent: [WP-AIOPS-2026-03-001](./WP-AIOPS-2026-03-001-ai-ops-bootstrap.md)
  - Child(Track 1, Phase 1): [WP-AIOPS-2026-03-002](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-002-ai-tool-hook-enforcement.md) **DONE**
  - Child(Track 2, Phase 1): [WP-AIOPS-2026-03-003](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-003-git-hook-output-compliance-gate.md) **DONE**
  - Child(Track 3, Phase 2): [WP-AIOPS-2026-03-004](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-004-document-structure-transition.md) **DONE** (문서 구조 전환 + 운영 문서 생성)
  - Child(Track 4, Phase 3): [WP-AIOPS-2026-03-005](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-005-process-based-collaboration.md) **DONE** (프로세스 기반 협업 전환)
  - Child(Phase 4): [WP-AIOPS-2026-03-006](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-006-pilot-verification.md) **DONE** (파일럿 검증 - 프레임워크 완성 판정)
  - Child(Track 6, Phase 5): [WP-AIOPS-2026-03-007](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-007-ai-tool-artifact-separation.md) **DONE** (AI 도구 산출물 경계 정렬)
  - Child(Track 7, Phase 6): [WP-AIOPS-2026-03-008](./WP-AIOPS-2026-03-008-codex-omx-alignment.md) (Codex+OMX 운영 정렬)
  - Child(Track 8, Phase 6): [WP-AIOPS-2026-03-009](../archive/ai-ops/work-packets/WP-AIOPS-2026-03-009-claude-omc-sot-application.md) **DONE** (Claude+OMC SoT 구조 적용)
  - Child(Track 9): [WP-AIOPS-2026-03-010](./WP-AIOPS-2026-03-010-framework-extraction.md) (ai-ops 프레임워크 추출 및 오픈소스화)
  - Child(Track 10): [WP-AIOPS-2026-03-011](./WP-AIOPS-2026-03-011-public-history-replay-plan.md) (public repo replay history 재구성 계획)
  - Child(Track 11): [WP-AIOPS-2026-03-012](./WP-AIOPS-2026-03-012-external-canonical-migration-inventory.md) (external canonical 기준 migration target 재분석)

## 6. Hard Rules (Mandatory)

요구사항이 변경되면 아래를 **같은 세션에서 동시 갱신**한다.

1. 부모 WP 및 영향받는 자식 WP
2. 본 인덱스(`index.md`)
3. `../CHANGELOG.md`
4. 정책 변경 시 ADR
5. 상위 계획 문서(`ops-bootstrap-master-plan.md`)
6. 헌법 문서(`constitution.md`)

위 동기화가 끝나기 전에는 상태 전이(`current_process` 변경)를 금지한다.
근거 규칙: [ADR-AIOPS-001](../adr/ADR-AIOPS-001-bootstrap-requirement-change-sync.md)
