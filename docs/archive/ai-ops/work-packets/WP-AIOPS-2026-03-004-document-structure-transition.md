---
packet_id: "WP-AIOPS-2026-03-004"
title: "문서 구조 전환 및 G0 프로세스 신설"
goal_ids: ["AIOPS-G3", "AIOPS-G5"]
status: "DONE"
work_type: "DOCUMENTATION"
priority: "P0"
target_environment: "master"
start_process: "P0"
current_process: "S4"
next_process: "DONE"
owner: "AI-CLAUDE"
created_at: "2026-03-07"
last_updated: "2026-03-08"
---
# WP-AIOPS-2026-03-004 문서 구조 전환 및 G0 프로세스 신설

## 1. Background
- ai-collaboration-guide.md가 1500줄 단일 문서로 운영 모델/프로세스 카탈로그/업무 패킷 규격을 모두 포함
- ops-bootstrap-master-plan.md North Star #3: "ai-collaboration-guide.md 의존도를 단계적으로 줄이고 분해 가능한 구조로 전환"
- 기존 프로세스 카탈로그(P0~S4)에 목표 점검 프로세스가 없어 목표 drift 감지 불가
- ADR-AIOPS-002에서 G0 프로세스 신설 결정

## 2. Goal
- ai-collaboration-guide.md를 분해하여 독립 문서 체계로 전환한다.
- G0 (목표 정합성 점검) 프로세스를 프로세스 카탈로그에 추가한다.
- **AI 도구가 참조할 운영 문서 체계를 구축한다** (설계 문서 ≠ 운영 문서).
- 분해된 문서들이 AI Ops 체계와 정합하도록 구조화한다.

## 3. Scope
### 3.1 분해 대상
- Part 1. 운영 모델 → `docs/ai-ops/operating-model.md`
- Part 2. 프로세스 카탈로그 → `docs/ai-ops/process-catalog/`
- Part 3. 업무 패킷 규격 → `docs/ai-ops/work-packet-spec.md`

### 3.2 G0 프로세스 신설
- G0 프로세스 정의 문서 생성
- 목표 점검 체크리스트 생성
- master-plan "망각 방지 규칙"과 연결

### 3.3 AI 도구 참조용 운영 문서 생성
- `docs/ai-ops/process-catalog/process-selection-guide.md` - 프로세스 선택 가이드 (도구 참조용)
- `docs/ai-ops/process-catalog/session-start-protocol.md` - 세션 시작 프로토콜
- 각 프로세스(P0~S4, G0)별 실행 가이드 문서

### 3.4 문서 체계 정비
- ai-collaboration-guide.md를 **설계/사상 문서로 보존** (Archive)
- 분해된 운영 문서들의 상호 참조 체계 구축
- 도구 설정(.claude/, .codex/)이 참조할 진입점 명확화

## 4. Out of Scope
- 프로세스 카탈로그 내용 변경 (G0 추가 외)
- 업무 패킷 규격 내용 변경
- 프로젝트 기능 ADR/WP (docs/project-ops)

## 5. Done Criteria
- [x] ai-collaboration-guide.md가 설계/사상 문서로 보존됨 (Archive 표시)
- [x] Part 1/2/3이 독립 운영 문서로 분리됨
- [x] G0 프로세스가 프로세스 카탈로그에 추가됨
- [x] 목표 점검 체크리스트가 생성됨
- [x] **프로세스 선택 가이드가 독립 문서로 존재함** (도구 참조용)
- [x] **세션 시작 프로토콜 문서가 존재함**
- [x] 분해된 문서 간 상호 참조가 정합함
- [x] **도구 설정이 참조할 진입점이 명확함**
- [x] compliance check 통과

## 6. Risks / Constraints
- 분해 과정에서 정보 손실 위험
- 기존 가이드 참조 링크 깨짐 가능성
- 분해 후 중복/불일치 발생 가능성

## 7. Related References
### 7.1 Related Docs
- [ai-collaboration-guide.md](../ai-collaboration-guide.md)
- [ops-bootstrap-master-plan.md](../ops-bootstrap-master-plan.md)
- [ADR-AIOPS-002](../adr/ADR-AIOPS-002-goal-alignment-process.md)
- [WP-AIOPS-2026-03-001](./WP-AIOPS-2026-03-001-ai-ops-bootstrap.md)

### 7.2 Related Code
- 없음 (문서 작업)

### 7.3 Related Tests
- compliance check 통과 여부

### 7.4 Related Commits
- 추후 연결

## 8. Process Plan
- P0: ai-collaboration-guide.md 구조 분석
- P1: 분해 계획 구체화 (파일 구조, 상호 참조 설계)
- P3: 분해 실행 및 G0 프로세스 문서 생성
- S1: 분해 결과 리뷰 (정보 손실, 링크 정합성)
- S2: 허브 문서 및 인덱스 갱신
- S4: 결정과 변경 이력 기록

## 9. Execution Notes
- Phase 2 (G2) 주관 WP
- Track 3 (문서 구조 전환) 핵심 작업
- ADR-AIOPS-002 결정에 따라 G0 프로세스 포함

### 2026-03-08 실행 기록 (W1~W5 프로세스 준수)

**W1. 목표 정합성 점검 완료**
- goal_ids: AIOPS-G3, AIOPS-G5 확인
- Phase 2, Track 3 위치 확인
- 상위 WP-001 상태: DONE

**W2. 템플릿 필드 검증**
- compliance check 통과

**W3. Done Criteria 구체화**
- 모든 항목이 검증 가능한 형태로 정의됨

**W4. 중간 점검**
- ai-collaboration-guide.md 구조 분석 완료 (Part 1/2/3 식별)
- 분해 계획 수립 완료

**실제 분해 작업 수행 (P3)**
- ai-collaboration-guide.md → Archive 표시 추가
- Part 1 → operating-model.md 생성
- Part 2 → process-catalog/ 디렉토리 생성
  - README.md (진입점)
  - session-start-protocol.md
  - process-selection-guide.md
  - G0-goal-alignment.md
  - P0-P4-core-processes.md
  - S1-S4-support-processes.md
- Part 3 → work-packet-spec.md 생성
- goal-alignment-checklist.md 생성
- README.md에 AI 도구 진입점 명확화

## 10. Deliverables
### 10.1 분해된 운영 문서
- `docs/ai-ops/operating-model.md`
- `docs/ai-ops/work-packet-spec.md`
- `docs/ai-ops/goal-alignment-checklist.md`

### 10.2 프로세스 카탈로그
- `docs/ai-ops/process-catalog/README.md` - 진입점
- `docs/ai-ops/process-catalog/process-selection-guide.md` - **프로세스 선택 가이드 (도구 참조용)**
- `docs/ai-ops/process-catalog/session-start-protocol.md` - **세션 시작 프로토콜**
- `docs/ai-ops/process-catalog/G0-goal-alignment.md`
- `docs/ai-ops/process-catalog/P0-P4-core-processes.md`
- `docs/ai-ops/process-catalog/S1-S4-support-processes.md`

### 10.3 설계 문서 보존
- ai-collaboration-guide.md (Archive 표시, 설계/사상 문서로 보존)

## 11. Review Notes
- 분해 후 정보 손실 여부 집중 점검 필요
- 기존 링크 호환성 확인 필요

### S1 리뷰 결과 (2026-03-08)
- 9개 산출물 모두 생성됨 (ls 명령으로 확인)
- ai-collaboration-guide.md에 Archive 표시 추가됨
- README.md에 AI 도구 진입점 명확화됨
- 각 문서 간 상호 참조 링크 정합 확인
- compliance check 통과

## 12. Decisions
| 결정 | 선택 | 이유 |
|------|------|------|
| G0 프로세스 추가 | 분해와 동시 진행 | gap을 이관하지 않기 위해 (ADR-AIOPS-002) |
| 분해 단위 | Part 1/2/3 기준 | 기존 구조 활용, 최소 변경 |

## 13. Follow-ups
- WP-AIOPS-2026-03-005 (파일럿 사이클 검증)와 연결
- G0 프로세스 실제 적용 검증

## 14. Timeline
- [2026-03-07] 작업 생성 (ADR-AIOPS-002 결정 반영)
- [2026-03-08] W1~W4 점검 완료, P3 분해 작업 실행
- [2026-03-08] S4 완료, DONE 전이
