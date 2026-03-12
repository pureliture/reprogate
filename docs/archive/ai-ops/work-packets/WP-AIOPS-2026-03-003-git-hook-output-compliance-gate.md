---
packet_id: "WP-AIOPS-2026-03-003"
title: "최종 산출물 준수 검토 Git Hook 게이트 구축"
goal_ids: ["AIOPS-G1", "AIOPS-G2", "AIOPS-G3", "AIOPS-G4", "AIOPS-G5"]
status: "DONE"
work_type: "DOCUMENTATION"
priority: "P0"
target_environment: "master"
start_process: "P1"
current_process: "S4"
next_process: "-"
owner: "SHARED"
created_at: "2026-03-07"
last_updated: "2026-03-07"
---
# WP-AIOPS-2026-03-003 최종 산출물 준수 검토 Git Hook 게이트 구축

## 1. Background
- 작업 중 훅만으로는 최종 결과물이 운영체계를 충분히 거쳤는지 보장하기 어렵다.
- 커밋 직전/푸시 전 단계에서 결과물 단위 검토 게이트가 필요하다.

## 2. Goal
- Git hook 기반으로 최종 산출물의 운영체계 준수 여부를 자동 점검한다.
- 준수 의심 항목은 차단 또는 리뷰 요구로 전환한다.

## 3. Scope
- pre-commit 또는 pre-push 훅에서 수행할 준수 점검 규칙 정의
- 필수 산출물 연계 점검
  - 변경 작업과 관련된 WP 존재 여부
  - `work-packets/index.md`, `CHANGELOG.md` 갱신 여부
  - 정책 변경 시 ADR 반영 여부(룰 기반 휴리스틱)
- 실패 시 차단 메시지/리뷰 안내 규약 정의
- 훅 규칙의 지속 개선 정책(오탐/미탐 기반 보정) 정의

## 4. Out of Scope
- AI tool별 실행 중 훅 구현(별도 WP-AIOPS-2026-03-002)
- CI 서버 정책 전체 설계

## 5. Done Criteria
- [x] Git hook 점검 규칙이 명시됨
- [x] 훅 스크립트 초안(또는 운영 스크립트) 생성됨
- [x] 실패 케이스 예시와 우회 금지 규칙 문서화됨
- [x] 샘플 커밋 1건에서 차단/통과 동작 확인됨
  - 차단: AIOPS-G6 undefined goal → "compliance check failed"
  - 통과: goal_ids 수정 후 → "compliance check passed"

## 6. Risks / Constraints
- 훅 규칙이 과도하면 정상 커밋을 막을 수 있다.
- 휴리스틱 점검은 오탐/미탐 가능성이 있다.
- 팀별 로컬 환경 차이로 훅 설치 누락 위험이 있다.

## 7. Related References
### 7.1 Related Docs
- [WP-AIOPS-2026-03-001](./WP-AIOPS-2026-03-001-ai-ops-bootstrap.md)
- [WP-AIOPS-2026-03-002](./WP-AIOPS-2026-03-002-ai-tool-hook-enforcement.md)
- [AI Ops Constitution](../constitution.md)
- [운영체계 구축 상위 계획](../ops-bootstrap-master-plan.md)
- [ADR-AIOPS-001](../adr/ADR-AIOPS-001-bootstrap-requirement-change-sync.md)
- [AI Ops CHANGELOG](../CHANGELOG.md)

### 7.2 Related Code
- `.githooks/` (추후 생성)
- `scripts/` (검증 스크립트 위치는 추후 결정)

### 7.3 Related Tests
- 정상/비정상 커밋 케이스별 훅 동작 테스트

### 7.4 Related Commits
- `9a8704e` - Git hooks 공유 설정 (.githooks/ 커밋)
- `8ae4715` - Master Plan 보강 시 compliance check 차단/통과 검증

## 8. Process Plan
- P1: 훅 규칙 정의 및 차단/리뷰 기준 확정
- P3: 훅 스크립트/설정 구현
- S1: 샘플 커밋으로 동작 검증
- S2: 팀 적용 가이드 문서화
- S4: 최종 기록/의사결정 정리

## 9. Execution Notes
- 이 WP는 트랙2(최종 산출물 게이트) 전용 패킷이다.
- 훅 정책이 바뀌면 ADR 및 index/changelog를 같은 세션에서 갱신한다.
- Git hook 규칙은 운영체계 고도화에 맞춰 지속 업데이트한다.

## 10. Deliverables
- Git hook 규칙 문서
- 훅 스크립트 및 적용 가이드
- 검증 결과 요약
- `scripts/ai-ops/check_ai_ops_compliance.py`
- `scripts/ai-ops/install_git_hooks.sh`
- `.githooks/pre-commit`
- `.githooks/pre-push`

## 11. Review Notes
- 차단 전략과 개발 생산성 간 균형점 확인 필요

## 12. Decisions
| 결정 | 선택 | 이유 |
|------|------|------|
| 운영 구분 | 트랙2 단독 WP로 분리 | 책임/검증 타이밍 명확화 |
| 검증 시점 | 커밋/푸시 직전 | 최종 결과물 기준 통제 가능 |
| 검증 범위 | goal_ids 정합성 + WP 연결 | 최소 필수 검증으로 시작, 점진 확장 |
| 실패 정책 | fail-closed (차단) | 운영체계 준수 강제 (AIOPS-G2) |
| Git hooks 공유 | .githooks/ 커밋 | 팀 전체 일관성 보장 (WP-002 결정) |

## 13. Follow-ups
- CI 파이프라인 연동 필요 시 후속 WP 생성

## 14. Timeline
- [2026-03-07 AM] 작업 생성 (분리 요청 반영)
- [2026-03-07 AM] P1 → P3: 훅 규칙 정의 및 스크립트 구현
- [2026-03-07 PM] Git hooks 공유 설정 (.githooks/ 커밋)
- [2026-03-07 PM] S1: 샘플 커밋 차단/통과 검증 완료
- [2026-03-07 PM] S4: 최종 기록 완료 → **DONE**
