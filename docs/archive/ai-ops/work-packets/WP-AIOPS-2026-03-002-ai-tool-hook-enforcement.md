---
packet_id: "WP-AIOPS-2026-03-002"
title: "AI tool별 작업 중 훅 강제 레이어 구축"
goal_ids: ["AIOPS-G2", "AIOPS-G3", "AIOPS-G4", "AIOPS-G5"]
status: "DONE"
work_type: "DOCUMENTATION"
priority: "P0"
target_environment: "master"
start_process: "P1"
current_process: "S4"
next_process: "DONE"
owner: "SHARED"
created_at: "2026-03-07"
last_updated: "2026-03-07"
---
# WP-AIOPS-2026-03-002 AI tool별 작업 중 훅 강제 레이어 구축

## 1. Background
- 프롬프트 기반 소프트 규칙만으로는 컨텍스트 꼬임 시 체리피킹 위험이 크다.
- 운영체계 준수를 작업 중에 강제하는 실행 레이어가 필요하다.
- 사용자 요청에 따라 tool별 메커니즘을 분리해서 관리해야 한다.

## 2. Goal
- 작업 과정에서 운영체계 준수와 품질 유지가 강제되도록 tool별 훅/게이트 설계를 확정한다.
- Codex(JetBrains AI Assistant), Claude Code, OMC에 대해 각기 다른 강제 지점을 문서화한다.

## 3. Scope
- Codex(JetBrains AI Assistant): AI Assistant 규칙 추가 전략 정의
- Claude Code: `PreToolUse` 기반 차단/질의 게이트 정의
- OMC: `quality gates`, `Ultra QA` 검증 루프 강제 정의
- 훅 실패 시 상태 전이 차단 규칙(ADR-AIOPS-001 연계)
- 훅 수명주기 정책(정기 점검/오탐 미탐 보정/규칙 확장) 정의

## 4. Out of Scope
- 최종 산출물 검토용 Git hook 구현(별도 WP-AIOPS-2026-03-003)
- 문서 재배치 전체 실행

## 5. Done Criteria
- [x] tool별 강제 포인트와 실패 시 동작이 문서화됨
- [x] Codex/Claude/OMC별 적용 체크리스트 생성
- [x] 훅 우회/미적용 시 차단 정책이 ADR/WP/index/CHANGELOG에 반영됨
- [x] 최소 1회 샘플 작업에서 게이트 동작을 확인함

## 6. Risks / Constraints
- Codex는 Claude Code/OMC와 같은 형태의 네이티브 훅 개념이 다를 수 있다.
- 훅 규칙이 과도하면 작업 속도가 급감할 수 있다.
- 로컬/CI 환경 차이로 훅 실행 결과가 달라질 수 있다.

## 7. Related References
### 7.1 Related Docs
- [WP-AIOPS-2026-03-001](./WP-AIOPS-2026-03-001-ai-ops-bootstrap.md)
- [AI Ops Constitution](../constitution.md)
- [운영체계 구축 상위 계획](../ops-bootstrap-master-plan.md)
- [ADR-AIOPS-001](../adr/ADR-AIOPS-001-bootstrap-requirement-change-sync.md)
- [Tool Hooks](../tool-hooks/README.md)
- [work-packets index](./index.md)

### 7.2 Related Code
- `.claude/settings.local.json`
- `docs/ai-ops/omc-config/` (OMC 정책 원본)
- `scripts/ai-ops/sync_omc_policy.sh` (로컬 `.omc` 반영)
- `.codex/` (추후 생성될 tool-specific 규칙 자산)

### 7.3 Related Tests
- 샘플 변경 작업 1건에 대해 훅 게이트 통과/차단 로그 확인

### 7.4 Related Commits
- `9a8704e` - Track 1 P3→S1, Git hooks 공유 설정
- `ae3c7bb` - S2 tool-hooks 운영 문서 보강
- `c544992` - ADR-AIOPS-002 G0 프로세스, WP-004 생성
- `f5599b3` - G0 강제 메커니즘 (스킵 불가)
- `1e01457` - 4개 핵심 강제 메커니즘 완성

## 8. Process Plan
- P1: tool별 강제 메커니즘 상세 설계
- P3: 각 tool별 적용 파일/설정 반영
- S1: 우회 시나리오 포함 검증
- S2: 운영 문서와 사용법 정리
- S4: 결정과 변경 이력 기록

## 9. Execution Notes
- 이 WP는 트랙1(작업 중 강제) 전용 패킷이다.
- 운영체계 준수 갱신 누락 시 `READY -> IN_DEVELOPMENT` 전이를 금지한다.
- 훅은 초기 1회 설정으로 종료하지 않고, 운영체계 변경에 맞춰 반복 갱신한다.

### P3 실행 기록 (2026-03-07)
- **verify 결과**: `check_ai_ops_compliance.py --mode none` 통과
- **Ultra QA 우회 시나리오**: AI Ops 파일만 staged 후 index/changelog 누락 상태에서 `--mode staged` 실행 → 정상 차단 확인
- **정합성 수정**: `AI-OPS-POLICY.template.md`에 Source Of Truth 경로, sync 스크립트, WP 연결 명시 추가 → `omc-quality-gates-ultraqa.md`와 일치
- **sync 실행**: `sync_omc_policy.sh` → `.omc/AI-OPS-POLICY.md` 동기화 완료

### S1 실행 기록 (2026-03-07)
- **우회 시나리오 검증**: AI Ops 파일만 staged 후 index/changelog 누락 → `--mode staged` 정상 차단 확인
- **Git hooks 공유**: `.githooks/` 저장소 추가, 로컬 전용 설정(.claude/, .codex/) gitignore 처리
- **커밋**: `9a8704e` - 트랙2 Git hooks 공유 설정 완료

### S2 실행 기록 (2026-03-07)
- **tool-hooks 문서 보강**: README.md 및 3개 도구별 문서에 다음 항목 추가
  - 목적, 실행 타이밍, 실패 시 동작, 유지보수 책임, 업데이트 주기
  - "훅은 운영체계 고도화에 따라 지속 업데이트 대상" 명시
- **누락 방지**: 공통 수명주기 정책을 README.md에 집약, 도구별 문서에서 참조

### S4 실행 기록 (2026-03-07)
- **Decisions 보강**: 7개 결정 기록 (Git hooks 공유, G0 신설, 강제 수준, 스킵 정책, 상태 전이)
- **Timeline 갱신**: P1→P3→S1→S2→S4 전체 이력 + 커밋 연결
- **Related Commits 연결**: 5개 커밋 (`9a8704e`, `ae3c7bb`, `c544992`, `f5599b3`, `1e01457`)
- **Follow-ups 정리**: 완료 2건 체크, 잔여 3건 명시
- **완료 판정**: Done Criteria 4/4 충족, 후속 WP 연결 완료

## 10. Deliverables
- tool별 훅/게이트 설계 문서
- 적용 체크리스트
- 검증 로그 요약
- `AGENTS.md`
- `.codex/jetbrains-ai-assistant-rules.md`
- `.claude/settings.json`
- `.claude/hooks/pretooluse-ai-ops-guard.py`
- `docs/ai-ops/tool-hooks/`
- `docs/ai-ops/omc-config/`

## 11. Review Notes
- 강제 정책이 실무 속도와 품질 사이 균형을 갖는지 점검 필요

## 12. Decisions
| 결정 | 선택 | 이유 |
|------|------|------|
| 운영 구분 | 트랙1 단독 WP로 분리 | 책임 경계 명확화 |
| 대상 도구 | Codex/Claude/OMC 모두 포함 | 도구 전환 시 일관성 유지 |
| Git hooks 공유 방식 | `.githooks/` 저장소 추가, `.claude/`, `.codex/` gitignore | 트랙2 게이트는 공유 필요, AI tool 설정은 개인 |
| G0 프로세스 신설 | ADR-AIOPS-002로 결정 | 목표 점검을 프로세스로 강제, 세션 시작 시 스킵 불가 |
| 강제 수준 | 핵심 4개만 강제, 나머지 권장 | 토큰 효율성 + 실패 방지 균형 |
| 프로세스 스킵 | 허용하되 스킵 이유 기록 필수 | 유연성 유지하면서 추적 가능 |
| 상태 전이 규칙 | DRAFT→DONE 금지, 최소 S4 필요 | 불법 전이로 인한 프로세스 무시 방지 |

## 13. Follow-ups
- [x] G0 프로세스 신설 (ADR-AIOPS-002로 완료)
- [x] 4개 핵심 강제 메커니즘 정의 (AGENTS.md, OMC Policy에 반영)
- [ ] WP-AIOPS-2026-03-003 (트랙2 Git hook 게이트) S1 검증 진행
- [ ] WP-AIOPS-2026-03-004 (문서 구조 전환) P0 시작
- [ ] 필요 시 도구별 하위 WP 분할 (현재 불필요)

## 14. Timeline
- [2026-03-07] 작업 생성 (분리 요청 반영)
- [2026-03-07] P1 완료 - tool별 강제 메커니즘 상세 설계
- [2026-03-07] P3 완료 - 각 tool별 적용 파일/설정 반영
- [2026-03-07] S1 완료 - 우회 시나리오 검증, Git hooks 공유 설정 (`9a8704e`)
- [2026-03-07] S2 완료 - tool-hooks 운영 문서 보강 (`ae3c7bb`)
- [2026-03-07] G0 프로세스 신설 - ADR-AIOPS-002 (`c544992`)
- [2026-03-07] 4개 핵심 강제 메커니즘 완성 (`f5599b3`, `1e01457`)
- [2026-03-07] S4 진행 - 결정과 변경 이력 기록
