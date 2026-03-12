---
packet_id: "WP-AIOPS-2026-03-006"
title: "파일럿 검증 - 프로세스 기반 협업 실증"
goal_ids: ["AIOPS-G3"]
status: "DONE"
work_type: "REVIEW"
priority: "P0"
target_environment: "master"
start_process: "P0"
current_process: "S4"
next_process: "-"
owner: "SHARED"
created_at: "2026-03-07"
last_updated: "2026-03-08"
---
# WP-AIOPS-2026-03-006 파일럿 검증 - 프로세스 기반 협업 실증

## 1. Background
- WP-004: ai-collaboration-guide.md 분해 → AI 도구 참조용 운영 문서 생성
- WP-005: 도구별 설정에 프로세스 선택 질의 규칙 추가
- 운영 문서와 도구 설정이 완료되어도 실제 작업에서 검증되지 않으면 프레임워크 완성 선언 불가
- 실제 product-ops 작업 3건을 프로세스 기반으로 수행하여 프레임워크 유효성 검증 필요

## 2. Goal
- 실제 product-ops 작업 3건을 프로세스 기반으로 수행한다.
- 각 작업에서 다음 흐름이 정상 동작하는지 검증한다:
  1. 프로세스 선택 질의 발생
  2. 사용자가 프로세스 선택
  3. WP 생성/갱신
  4. 선택된 프로세스 절차 준수
  5. 후속 프로세스 연결
- 검증 결과를 바탕으로 AI Ops 프레임워크 완성 여부를 판정한다.

## 3. Scope
### 3.1 파일럿 작업 선정
- 다양한 프로세스를 커버하는 3건의 실제 product-ops 작업 선정
- 권장 조합:
  - P2 → P4 → S1 → S4 (오류 수정)
  - P0 → P1 → P3 → S1 → S4 (기능 개발)
  - P0 → S3 → S1 → S4 (리팩토링)

### 3.2 검증 항목
- 프로세스 선택 질의 발생 여부
- 프로세스 선택 후 절차 준수 여부
- WP 자동/수동 생성 여부
- 후속 프로세스 연결 여부
- 종료 조건 충족 여부

### 3.3 결과 기록
- 각 파일럿 작업별 검증 결과 기록
- 발견된 문제점 및 개선 사항 기록
- 프레임워크 완성 판정

## 4. Out of Scope
- 운영 문서 변경 (WP-004 범위)
- 도구 설정 변경 (WP-005 범위)
- AI Ops 프레임워크 외 작업

## 5. Done Criteria
- [x] 파일럿 작업 3건이 선정됨
- [x] 각 작업에서 프로세스 선택 질의가 발생함
- [x] 각 작업에서 선택된 프로세스 절차가 준수됨
- [x] 각 작업에서 WP가 생성/갱신됨
- [x] 각 작업에서 후속 프로세스가 연결됨
- [x] 파일럿 #2/#3 종료 시 "2회 한정 임시 가드 체크리스트"가 기록됨
- [x] 검증 결과가 기록됨
- [x] **AI Ops 프레임워크 완성 선언 가능** 판정

## 6. Risks / Constraints
- WP-004, WP-005 완료 전제 조건
- 적절한 파일럿 작업 선정 필요
- 검증 중 발견된 문제로 WP-004/005 재작업 가능

## 7. Related References
### 7.1 Related Docs
- [WP-AIOPS-2026-03-004](./WP-AIOPS-2026-03-004-document-structure-transition.md)
- [WP-AIOPS-2026-03-005](./WP-AIOPS-2026-03-005-process-based-collaboration.md)
- [ops-bootstrap-master-plan.md](../ops-bootstrap-master-plan.md)
- [WP-2026-03-002 (product)](../../project-ops/work-packets/WP-2026-03-002-shadow-url-double-encoding-fix.md)

### 7.2 Related Code
- 파일럿 작업에서 변경되는 코드

### 7.3 Related Tests
- 파일럿 작업별 검증 결과

### 7.4 Related Commits
- `313543d40c9d90198c27ae4449d89baeca7d3244` - product fix (Shadow URL 이중 인코딩 버그)
- `133a0c4` - project-ops source WP에 java8 backport trace 기록 보강
- `bef8f60` - P4 backport 경로 강제(master->java8 직접 mvn 우회 차단)
- `f17b592` - project-ops 단일 통합 changelog 체계 복구 + compliance 예외 보강
- `eba1376` - ai-ops 단일 통합 changelog 경로 승격(`docs/ai-ops/CHANGELOG.md`)
- `0e004d5` - 파일럿 #3 P3 구현 (DB 스키마 라우팅 정보 개선)
- `911ed0a` - 파일럿 #3 P4 백포팅 완료 (`wafful4`)

## 8. Process Plan
- P0: 파일럿 작업 후보 선정
- P3: 파일럿 작업 3건 수행 (프로세스 기반)
- S1: 각 작업별 검증 결과 리뷰
- S4: 프레임워크 완성 판정 및 기록

## 9. Execution Notes
- Phase 4 (G4) 주관 WP
- WP-004, WP-005 완료 후 착수
- 이 WP 완료 시 AI Ops 프레임워크 완성 선언

### 9.1 파일럿 #1 결과 (완료)

- Pilot Target: `WP-2026-03-002-shadow-url-double-encoding-fix`
- Product Commit: `313543d40c9d90198c27ae4449d89baeca7d3244`
- Process Chain: `P2 -> P4 -> S4` (product) + `P3`(ai-ops 보완)

식별된 ai-ops 누락/결함과 보완:
1. `master` 세션에서 `java8` 대상 직접 `mvn` 호출 우회 가능
   - 보완: `bef8f60` (P4 backport 실행 하드가드 추가)
2. source WP의 backport trace 기록 누락 가능
   - 보완: `133a0c4` (project-ops WP trace 기록)
3. project-ops 관제(changelog/index) 누락으로 제품 이력 탐색 비용 증가
   - 보완: `f17b592` (project-ops 단일 통합 changelog 체계 복구)
4. ai-ops changelog 경로가 `work-packets` 하위에 고정되어 운영 혼선
   - 보완: `eba1376` (`docs/ai-ops/CHANGELOG.md`로 통합)

판정:
- Pilot #1은 product fix 자체뿐 아니라 ai-ops 운영체계의 방어 규칙 보완까지 유도한 유효 케이스로 판정.
- 남은 파일럿 #2, #3 수행 후 최종 완성 판정(`S1 -> S4`) 진행.

### 9.2 파일럿 #2/#3 전용 "2회 한정 임시 가드"

목적:
- 남은 파일럿 2회에서 누락 방지(요구사항 망각 방지)만 보장한다.
- 상시 프로세스/훅으로 승격하지 않는다.

적용 범위:
- `WP-AIOPS-2026-03-006`의 파일럿 #2, #3에만 적용
- 파일럿 #3 완료와 함께 자동 종료

운영 규칙:
1. `/ai-ops`로 수행한 product 작업을 종료 보고할 때 아래 체크리스트를 반드시 포함한다.
2. 체크리스트 누락 시 해당 파일럿을 완료로 판정하지 않는다.
3. #3 완료 후 본 가드는 재사용하지 않고 WP-006 기록으로만 남긴다.

체크리스트(파일럿 #2/#3 공통):
- [x] 이번 작업의 대상 product WP(`docs/project-ops/work-packets/...`)를 명시했다.
- [x] 선택 프로세스와 실제 수행 체인을 명시했다.
- [x] `docs/project-ops` WP/ADR 갱신 여부를 기록했다.
- [x] `docs/project-ops/CHANGELOG.md` 갱신 여부를 기록했다.
- [x] P4/백포팅 수행 시 source WP Backport Trace 기록 여부를 명시했다.

## 10. Deliverables
- 파일럿 작업 3건의 WP
- 각 작업별 검증 결과 기록
- AI Ops 프레임워크 완성 판정 문서

## 11. Review Notes
- 파일럿 작업이 다양한 프로세스를 커버하는지 점검
- 프레임워크 완성 판정 기준 명확화 필요

## 12. Decisions
| 결정 | 선택 | 이유 |
|------|------|------|
| 파일럿 작업 수 | 3건 | 다양한 프로세스 커버 + 적절한 검증 비용 |

## 13. Follow-ups
- 프레임워크 완성 후 ai-collaboration-guide.md 공식 Archive 처리
- 운영체계 유지보수 WP 생성

### 9.3 파일럿 #2 결과 (P0→P3 완료)

- Pilot Target: `WP-2026-03-004-canary-routing-support`
- Process Chain: `P0` (설계) → `P3` (구현) → `S1` (검증 대기)
- 요구사항: Canary 배포 환경에서 Shadow Traffic 검증 지원
  - 헤더룰: `X-Traffic-Type` 양방향 토글 (stable ↔ canary)
  - 웨이트룰: Envelope 기반 Pod 판별 + 동일 Pod 스킵

산출물:
- [ADR-015: Canary 라우팅 전략](../../project-ops/adr/ADR-015-canary-routing-strategy.md) (Proposed)
- [WP-2026-03-004](../../project-ops/work-packets/WP-2026-03-004-canary-routing-support.md) (IN_DEVELOPMENT)
- P3 구현 커밋: `108022f`

파일럿 #2 프로세스 검증:
- [x] 프로세스 선택 질의 발생 (P0/P1/P3 추천 → P0 선택)
- [x] 프로세스 선택 후 절차 준수 (P0 → P3 → S1 → S2 → S3 → P4 → S4)
- [x] WP 생성/갱신 (WP-2026-03-004)
- [x] ADR 생성 (ADR-015)
- [x] 후속 프로세스 연결 완료 (S4: DONE)
- [x] docs/project-ops/CHANGELOG.md 갱신
- [x] P4 백포팅 완료 + source WP Backport Trace 기록

**2회 한정 임시 가드 체크리스트 (파일럿 #2):**
- [x] 이번 작업의 대상 product WP: `docs/project-ops/work-packets/WP-2026-03-004-canary-routing-support.md`
- [x] 선택 프로세스: P0 → 실제 수행 체인: P0 → P3 → S1 → S2 → S3 → P4 → S4
- [x] `docs/project-ops` WP/ADR 갱신: WP-2026-03-004 (DONE), ADR-015 (Proposed)
- [x] `docs/project-ops/CHANGELOG.md` 갱신: 완료
- [x] P4/백포팅 수행 시 source WP Backport Trace 기록: WP-2026-03-004 Section 15

## 14. Timeline
- [2026-03-07] 작업 생성 (Master Plan 보강 시)
- [2026-03-08] 파일럿 #1 수행: product commit `313543d...` 완료
- [2026-03-08] 파일럿 #1에서 식별된 운영 결함 보완: `133a0c4`, `bef8f60`, `f17b592`, `eba1376`
- [2026-03-08] 남은 파일럿 #2/#3 누락 방지용 "2회 한정 임시 가드" 추가 (WP-006 범위 한정)
- [2026-03-08] 파일럿 #2 착수: WP-2026-03-004 (Canary 라우팅 지원)
- [2026-03-08] 파일럿 #2 P0 완료: ADR-015, WP-2026-03-004 생성 (`dd9e856`)
- [2026-03-08] 파일럿 #2 P3 완료: Canary 라우팅 구현 (`108022f`)
- [2026-03-08] 파일럿 #2 S1+S2+S3 완료: 테스트/문서화/리팩토링 검토 (`07be824`)
- [2026-03-08] 파일럿 #2 P4 완료: wafful4 백포팅 (`6507664`)
- [2026-03-08] 파일럿 #2 S4 완료: WP-2026-03-004 DONE (`1d28267`)
- [2026-03-08] 파일럿 #3 착수: WP-2026-03-005 (DB 스키마 라우팅 정보 개선)
- [2026-03-08] 파일럿 #3 P3 완료: DB 스키마 라우팅 정보 개선 (`0e004d5`)
- [2026-03-08] 파일럿 #3 S2 완료: `docs/user-guide.md` DB 스키마 섹션 갱신
- [2026-03-08] 파일럿 #3 P4 완료: wafful4 백포팅 (`911ed0a`)
- [2026-03-08] 파일럿 #3 S4 완료: WP-2026-03-005 DONE 및 Backport Trace 기록 동기화
- [2026-03-08] 파일럿 #2/#3 2회 한정 임시 가드 종료 (WP-006 기록 보존)
- [2026-03-08] WP-AIOPS-2026-03-006 DONE (Phase 4/G4 완료 판정)

### 9.4 파일럿 #3 결과 (P0→P4 완료)

- Pilot Target: `WP-2026-03-005-db-schema-routing-enhancement`
- Process Chain: `P0` → `P3` → `S1` → `S2` → `P4` → `S4`
- 요구사항:
  - `routing_mode` 컬럼 추가 (HEADER_RULE / WEIGHT_RULE)
  - `origin_url`, `shadow_url` 분리 (`target_url` 삭제)
  - `traffic_type` 의미 통일 (STABLE/CANARY 명시, null 제거)

산출물:
- [WP-2026-03-005](../../project-ops/work-packets/WP-2026-03-005-db-schema-routing-enhancement.md) (**DONE**)
- P3 구현 커밋: `0e004d5`
- S2 문서화: `docs/user-guide.md` DB 스키마 섹션 업데이트
- P4 백포팅 커밋: `911ed0a` (`wafful4`)

파일럿 #3 프로세스 검증:
- [x] 프로세스 선택 질의 발생 (P0/P1/P3 추천 → P0 선택)
- [x] 프로세스 선택 후 절차 준수 (P0 → P3 → S1 → S2 → P4 → S4)
- [x] WP 생성/갱신 (WP-2026-03-005)
- [x] 후속 프로세스 연결 완료 (S4: DONE)
- [x] docs/project-ops/CHANGELOG.md 갱신
- [x] P4 백포팅 완료 + source WP Backport Trace 기록

**2회 한정 임시 가드 체크리스트 (파일럿 #3):**
- [x] 이번 작업의 대상 product WP: `docs/project-ops/work-packets/WP-2026-03-005-db-schema-routing-enhancement.md`
- [x] 선택 프로세스: P0 → 실제 수행 체인: P0 → P3 → S1 → S2 → P4 → S4
- [x] `docs/project-ops` WP/ADR 갱신: WP-2026-03-005 (DONE), ADR-015 영향 없음
- [x] `docs/project-ops/CHANGELOG.md` 갱신: 완료
- [x] P4/백포팅 수행 시 source WP Backport Trace 기록: WP-2026-03-005 Section 15

### 9.5 파일럿 종합 판정 (S4)

- 파일럿 #1/#2/#3의 프로세스 체인 검증을 모두 충족했다.
- 파일럿 #2/#3 2회 한정 임시 가드는 목적 달성 후 종료한다(재사용 금지, 기록만 유지).
- 판정: **AI Ops 프레임워크 완성 선언 가능** (G4 완료).
