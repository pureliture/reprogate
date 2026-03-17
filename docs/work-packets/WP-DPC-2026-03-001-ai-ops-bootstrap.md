---
packet_id: "WP-DPC-2026-03-001"
title: "AI 협업 운영체계 구축 부트스트랩"
goal_ids: ["DPC-G1", "DPC-G2", "DPC-G3", "DPC-G4", "DPC-G5"]
status: "IN_REFINEMENT"
work_type: "DOCUMENTATION"
priority: "P0"
target_environment: "master"
start_process: "P1"
current_process: "P1"
next_process: "P3"
owner: "SHARED"
created_at: "2026-03-07"
last_updated: "2026-03-12"
---
# WP-DPC-2026-03-001 AI 협업 운영체계 구축 부트스트랩

## 1. Background
- `ai-collaboration-guide.md`에 운영 원칙이 집중되어 있어 실행 시 참조 비용이 높다.
- 운영체계 구축 작업 자체도 WP/ADR 기반으로 진행해야 한다는 요구가 명확해졌다.
- 기존 마이그레이션 과정에서 작성된 WP/ADR 템플릿을 버리지 않고 표준으로 재사용해야 한다.

## 2. Goal
- 운영체계 구축의 초기 설계를 단계별로 확정한다.
- 구축 작업 자체를 부모 WP로 관리하고, 요구사항 변경 시 강제 동기화 규칙을 적용한다.
- 향후 `ai-collaboration-guide.md`를 분해/퇴역해도 운영이 유지되도록 산출물 구조를 준비한다.
- `ai-ops`를 개별 엔진 개발이 아니라, 지속적으로 등장하는 AI 실행 엔진/도구를 활용하는 운영체계 레이어로 정립한다.

## 3. Scope
- 운영체계 구축 초기 설계(Phase/Gate) 수립
- 운영체계 구축 상위 계획 문서(Program Plan) 별도 관리
- 기존 WP/ADR 포맷을 `v1 표준`으로 동결
- `work-packets/index.md`, `CHANGELOG.md` 생성
- 요구사항 변경 시 계획/산출물 강제 갱신 규칙 정의(ADR 연계)
- 강제 운영을 2개 트랙으로 분리
  - 트랙 1: 작업 중 준수/품질 강제 (AI tool별 훅)
  - 트랙 2: 최종 산출물 준수 검토 (Git hook)

## 4. Out of Scope
- 전체 문서 일괄 재배치 완료
- `wafful4` 워크스페이스 파일 생성/동기화 완료
- 모든 세부 하위 프로세스 문서 신규 작성 완료

## 5. Done Criteria
- [x] 운영체계 구축 초기 설계(Phase 0~3, Gate 포함)가 본 패킷에 기록됨
- [x] 작업 1번(기존 WP/ADR 템플릿 그대로 표준화)이 명시적으로 반영됨
- [x] 요구사항 변경 강제 동기화 규칙이 ADR로 공식화됨
- [x] `work-packets/index.md`, `CHANGELOG.md`가 생성되고 본 패킷이 반영됨
- [x] 단위 작업 망각 방지용 상위 운영체계 구축 계획 문서가 생성됨
- [x] 하위 실행 WP 분리 및 착수(트랙1/트랙2 분리)
- [ ] 운영체계 구축 파일럿 1회 완료(P1 -> P3 -> S1 -> S2 -> S4)

## 6. Risks / Constraints
- 기존 문서 참조 경로가 많아 한 번에 이동하면 링크 파손 가능성이 있다.
- 요구사항이 중간에 바뀌면 문서/계획/상태 불일치가 다시 발생할 수 있다.
- 운영체계 구축 중에도 기능 개발 요청이 들어오면 우선순위 충돌이 생길 수 있다.

## 7. Related References
### 7.1 Related Docs
- [AI Ops Constitution](../governance/constitution.md)
- [AI 협업 가이드](../../project-ops/ai-collaboration-guide.md)
- [ADR-DPC-001: 요구사항 변경 동기화 강제 규칙](../adr/ADR-DPC-001-bootstrap-requirement-change-sync.md)
- [운영체계 구축 상위 계획](../governance/ops-bootstrap-master-plan.md)
- [work-packets index](./index.md)
- [AI Ops CHANGELOG](../CHANGELOG.md)

### 7.2 Related Code
- N/A (문서 운영체계 구축 작업)

### 7.3 Related Tests
- 운영 검증 체크: 패킷/ADR/인덱스/체인지로그 갱신 누락 여부 수동 점검

### 7.4 Related Commits
- 추후 연결

## 8. Process Plan
- **Phase 0 (정합성 고정 / Gate G0):** 현재 템플릿과 기록 체계를 기준선으로 동결한다.
  - 작업 1번: 기존 WP/ADR 템플릿을 `v1 표준`으로 채택
  - 산출물: 본 WP, ADR-DPC-001, index, CHANGELOG
- **Phase 1 (강제 메커니즘 분리 / Gate G1):**
  - 트랙 1: AI tool별 실행 중 강제 훅
    - Codex(JetBrains AI Assistant): `AGENTS.md` 중심 진입 규칙 연결
    - Claude Code: `PreToolUse` 기반 차단/질의 게이트
    - OMC: `quality gates`, `Ultra QA` 기반 검증 루프
  - 트랙 2: Git hook 기반 최종 산출물 검토 게이트
    - 운영체계 준수 흔적(WP/ADR/index/changelog) 검증
    - 준수 의심 항목 리뷰/차단 정책
- **Phase 2 (재배치 / Gate G2):** 기존 문서를 역할 기반으로 이동/통합
  - 대상: user-guide, maintenance, publishing, project-ops 분리
- **Phase 3 (운영 개시 / Gate G3):** 실제 업무 패킷 1건을 새 체계로 끝까지 수행
  - 목표: 계획-실행-리뷰-기록 사이클 재현

## 9. Execution Notes
### 9.1 초기 설계(운영체계 구축용)
| Phase | 목적 | 주요 작업 | 완료 게이트 |
|------|------|----------|------------|
| 0 | 표준 확정 | 기존 WP/ADR 템플릿 유지 채택, 강제 규칙 수립 | G0 |
| 1 | 강제 메커니즘 분리 | 트랙1(AI 훅) + 트랙2(Git 훅)로 분리 설계 | G1 |
| 2 | 자산 편입 | 기존 문서 이동, 중복 통합, deprecated 처리 | G2 |
| 3 | 실전 검증 | 실제 패킷 1건 풀사이클 수행 | G3 |

### 9.2 요구사항 변경 강제 동기화 프로토콜 (Hard Gate)
- 요구사항이 변경되면 **같은 세션 내** 아래 항목을 반드시 갱신한다.
  1. `constitution.md` (목표/규칙 변경이 있는 경우)
  2. 부모 WP(본 문서)의 Scope/Done Criteria/Process Plan/Timeline
  3. 영향받는 자식 WP(없으면 신규 생성)
  4. `work-packets/index.md` 상태/우선순위
  5. `CHANGELOG.md` 변경 이력
  6. 정책 변경이면 ADR 신규 생성 또는 기존 ADR 수정
- 위 1~6 중 하나라도 누락되면 **다음 프로세스 전이 금지** (`current_process` 유지).

### 9.3 훅 수명주기 관리 규칙
- 트랙1/트랙2 훅은 고정 규칙이 아니라 운영체계 성숙도에 따라 지속 갱신한다.
- 신규 규칙 추가, 오탐/미탐 발견, 우회 사례 확인 시 훅 갱신 WP를 생성 또는 기존 훅 WP를 갱신한다.
- 훅 변경이 발생하면 `ADR-DPC-001`, `index.md`, `CHANGELOG.md`, 상위 계획 문서를 같은 세션에서 동기화한다.

## 10. Deliverables
- `docs/ai-ops/work-packets/WP-DPC-2026-03-001-ai-ops-bootstrap.md`
- `docs/ai-ops/ops-bootstrap-master-plan.md`
- `docs/ai-ops/constitution.md`
- `docs/ai-ops/work-packets/WP-DPC-2026-03-002-ai-tool-hook-enforcement.md`
- `docs/ai-ops/work-packets/WP-DPC-2026-03-003-git-hook-output-compliance-gate.md`
- `docs/ai-ops/adr/ADR-DPC-001-bootstrap-requirement-change-sync.md`
- `docs/ai-ops/work-packets/index.md`
- `docs/ai-ops/CHANGELOG.md`
- `scripts/ai-ops/check_ai_ops_compliance.py`

## 11. Review Notes
- 기존 WP/ADR 누적 포맷과 충돌 없는지 검토 필요
- 새 규칙이 문서 부담만 증가시키지 않는지 파일럿에서 점검 필요

## 12. Decisions
| 결정 | 선택 | 이유 |
|------|------|------|
| 템플릿 전략 | 기존 WP/ADR 템플릿 유지(v1 동결) | 누적 자산과 즉시 호환 |
| 계획 저장 위치 | 부모 WP 중심 | 실행/상태/이력 동시 추적 가능 |
| 요구사항 변경 대응 | 동기화 프로토콜 하드 게이트 | 계획-산출물 불일치 방지 |
| ai-ops 정체성 | 엔진 재구현이 아닌 운영체계 레이어 | Codex/Claude/향후 엔진을 공통 프로세스/기록/검증 규칙 아래 정렬하기 위함 |
| 운영 문서 기술 방식 | capability-first | 도구 고유 기능/명령보다 장기 유지되는 운영 계약을 우선하기 위함 |
| 프로세스 이력 보존 방식 | 종료 시 커밋 여부 질의 | 프로세스별 변경이 뒤섞인 채 누적되는 것을 줄이기 위함 |
| 도구 경로 정렬 원칙 | 얇은 어댑터 + SoT 중심 구조 | Codex+OMX에서 먼저 정립하고, 추후 Claude+OMC 개편에도 동일 원칙을 적용하기 위함 |
| Codex entrypoint ownership | `$ai-ops`는 Codex+OMX 전용, JetBrains AI Assistant는 `AGENTS.md` 일반 진입 | 행동 parity는 유지하되 hidden local rule-pack 의존과 과잉 토큰 비용을 줄이기 위함 |

## 13. Follow-ups
- WP-DPC-2026-03-002: 작업 중 준수/품질 강제용 AI tool별 훅 적용(트랙1)
- WP-DPC-2026-03-003: 최종 산출물 준수 검토 Git hook 적용(트랙2)
- WP-DPC-2026-03-004: 문서 재배치/분해 실행(Phase 2)
- WP-DPC-2026-03-005: 파일럿 운영 사이클 검증(Phase 3)
- WP-DPC-2026-03-002: Codex+OMX 운영 정렬 임시 프로세스(2회) 수행 및 G6 판정(Phase 6)
- WP-DPC-2026-03-002: soft baseline 이후 Codex+OMX hard guarantee feasibility와 외부 wrapper/native hook 의존 경계 재분석
- WP-DPC-2026-03-002: OMX-centered launch wrapper/gateway 요구사항 정의 및 구현 반영
- WP-DPC-2026-03-004: external `ai-ops` public repo history를 framework evolution narrative 기준으로 replay
- WP-DPC-2026-03-005: external canonical 전제하에 must-move / archive-only 자산 재분류
- WP-DPC-2026-03-005: source archive-only cutoff와 external live control-board 이관 정책 실행
- 장기적으로는 오픈소스 + 간단 명령/마켓플레이스형 프로덕트 방향을 유지하되, 현재는 운영체계 레이어 정렬을 우선한다.

## 14. Timeline
- [2026-03-07] 작업 생성
- [2026-03-07] 초기 설계 확정 (Phase 0)
- [2026-03-07] 강제 동기화 ADR 등록
- [2026-03-07] index/CHANGELOG 생성 및 관제 시작
- [2026-03-07] 강제 메커니즘을 트랙1/트랙2로 분리 확정
- [2026-03-08] WP-DPC-2026-03-002 추가: Codex+OMX 운영 정렬(Track 7, Phase 6/G6)
- [2026-03-08] `ai-ops` 정체성 보강: 엔진 재구현이 아닌 운영체계 레이어 + 장기 제품화 방향 메모 반영
- [2026-03-08] WP-DPC-2026-03-002 재개: soft guarantee baseline 이후 hard guarantee feasibility를 별도 분석하도록 범위 보강
- [2026-03-08] WP-DPC-2026-03-002 설계 보강: 외부 소규모 wrapper는 개념 참고만 하고 OMX-centered hard gate 요구사항으로 정리
- [2026-03-09] WP-DPC-2026-03-002 설계 보강: `$ai-ops`를 Codex+OMX 전용으로 유지하고, JetBrains AI Assistant 일반 경로는 `AGENTS.md` + SoT로 정리하는 방향과 ADR-DPC-005를 추가
- [2026-03-09] WP-DPC-2026-03-002 구현 반영: `.codex/jetbrains-ai-assistant-rules.md` 제거, `$ai-ops` skill 참조 축소, Codex 선택 전 Team 금지 규칙을 직접 반영
- [2026-03-09] WP-DPC-2026-03-002 round 기록 고정: Codex entrypoint ownership 재정렬 round를 `S4`까지 완료
