---
packet_id: "WP-AIOPS-2026-03-005"
title: "프로세스 기반 협업 전환"
goal_ids: ["AIOPS-G3", "AIOPS-G4"]
status: "DONE"
work_type: "FEATURE"
priority: "P0"
target_environment: "master"
start_process: "P0"
current_process: "S4"
next_process: "-"
owner: "SHARED"
created_at: "2026-03-07"
last_updated: "2026-03-08"
---
# WP-AIOPS-2026-03-005 프로세스 기반 협업 전환

## 1. Background
- ai-collaboration-guide.md의 핵심 목표: "모든 개발 활동을 즉흥적 대화가 아니라 명시된 프로세스와 기록 가능한 산출물 중심으로 운영"
- WP-004에서 ai-collaboration-guide.md를 분해하여 AI 도구 참조용 운영 문서 생성
- 운영 문서가 생성되어도 AI 도구가 이를 자동으로 적용하는 메커니즘이 없으면 목표 달성 불가
- 모든 작업 시작 시 프로세스 선택 질의가 강제되어야 프로세스 기반 협업이 실현됨
- `/ai-ops` 실행 시 `team` 키워드 오탐으로 Team mode가 즉시 활성화되고 Stop hook 대기 루프가 발생함

## 2. Goal
- 모든 작업 시작 시 **프로세스 선택 질의**가 강제되도록 도구별 설정을 구성한다.
- 도구별 설정(.claude/, .codex/)이 분해된 운영 문서를 참조하도록 연결한다.
- 선택된 프로세스의 입력/단계/산출물/종료조건 준수가 강제되도록 한다.
- 사용자가 프로세스 미적용(`NONE`)을 선택하면 일반 작업(single-agent) 분기로 진행 가능하도록 한다.
- 선택 프로세스가 다중 역할 검증을 요구할 때만 Team을 조건부 활성화한다.

## 3. Scope
### 3.1 도구별 프로세스 선택 질의 규칙 추가
- Claude Code (.claude/settings.json, CLAUDE.md)
  - 세션 시작 시 프로세스 선택 질의 규칙
  - 프로세스 선택 가이드 참조 경로
  - 선택된 프로세스 절차 준수 규칙
- Codex by JetBrains AI Assistant (.codex/)
  - AI Assistant 규칙에 프로세스 선택 질의 추가
  - 운영 문서 참조 경로

### 3.2 운영 문서 참조 체계 연결
- 도구 설정 → `docs/ai-ops/process-catalog/README.md` (진입점)
- 프로세스 선택 → `docs/ai-ops/process-catalog/process-selection-guide.md`
- 세션 시작 → `docs/ai-ops/process-catalog/session-start-protocol.md`

### 3.3 `/ai-ops` 안정화
- 사용자 선택 전 Team 자동 활성화 방지
- Team mode 오탐 발생 시 `cancel --force`로 상태 복구 후 재질의
- 프로세스 추천 대상을 `P0~P4 + S1~S4 + NONE`으로 확장
- `NONE` 선택 시 일반 작업 수행 규칙 명시
- 프로세스 선택 결과를 컨텍스트 파일로 기록
- PreToolUse 가드가 선택 프로세스와 실제 도구 호출을 대조해 하드 차단

## 4. Out of Scope
- 프로세스 카탈로그 내용 변경 (WP-004 범위)
- 운영 문서 생성 (WP-004 범위)
- 파일럿 검증 (WP-006 범위)

## 5. Done Criteria
- [x] Claude Code 명령(`/ai-ops`)에 프로세스 추천/선택/분기 규칙 반영
- [x] Codex 규칙에 프로세스 선택 게이트(`P0~P4`, `S1~S4`, `NONE`) 반영
- [x] 도구 규칙이 운영 문서(process-catalog/)를 참조함
- [x] `/ai-ops`에서 `NONE` 선택 시 일반 작업 분기 규칙이 문서화됨
- [x] Team 활성화가 "사용자 선택 + 다중 역할 필요" 조건부로 문서화됨
- [x] Team 오탐 발생 시 mode safety(`cancel --force`)가 문서화됨
- [x] `set_process_context.py`로 선택 프로세스 컨텍스트 기록 경로가 구현됨
- [x] `claude_pretooluse_guard.py`가 프로세스별(P0/P3/S4 등) 도구 허용/차단을 수행함
- [x] 프로세스별 Team 사용 가능 범위(`P3/P4/S3`, 필요 시 `S1`)가 규칙에 반영됨
- [x] 훅 원본 스크립트와 로컬 `.claude/hooks` 동기화 경로가 마련됨
- [x] 프로세스별 최소 논리 역할 세트/팀 프로파일 문서가 정의됨
- [x] Team 가능 프로세스에서 `team_mode=auto` 상태 구현 변경이 차단됨
- [x] Team 경로에서 최소 역할 프로파일 미충족 시 차단됨
- [x] Team 경로에서 팀원별 실제 역할(`member:role`) 미정의/누락 시 차단됨
- [x] Claude OMC/비OMC 모두에서 팀원별 실제 역할 정의 가이드가 제공됨
- [x] `master`/`java8(wafful4)` 물리 분리 운영 규칙이 워크스페이스 프로파일로 문서화됨
- [x] `java8` 디렉토리에 branch-specific 방어 문서(`AI-RULES.md`, `BRANCH-SAFETY.md`, `docs/branch-specific/`)가 생성됨
- [x] 제품 변경 기록은 `docs/project-ops` WP/ADR로 라우팅되고, `docs/ai-ops` 오사용이 compliance 체크에서 차단됨
- [x] `java8` 빌드/테스트가 `scripts/workspace/java8-build.sh`로 강제되고 Claude PreToolUse에서 mvn 직접 호출이 차단됨
- [x] 새 세션에서 `/ai-ops` 실행 시 사용자 선택 전 Team 자동 활성화가 발생하지 않음 (수동 테스트)
- [x] 선택된 프로세스/`NONE` 분기가 실제 실행에서 의도대로 동작함 (수동 테스트)
- [x] compliance check 통과

## 6. Risks / Constraints
- WP-004 (운영 문서 생성) 완료 전제 조건
- 도구별 설정 방식 차이로 인한 구현 복잡도
- 프로세스 선택 질의가 사용자 경험에 미치는 영향 (질의 피로)
- OMC 업그레이드 시 키워드 트리거 정책이 재변경될 수 있음

## 7. Related References
### 7.1 Related Docs
- [ops-bootstrap-master-plan.md](../ops-bootstrap-master-plan.md)
- [WP-AIOPS-2026-03-004](./WP-AIOPS-2026-03-004-document-structure-transition.md) - 선행 WP
- [ADR-AIOPS-003](../adr/ADR-AIOPS-003-conditional-team-activation-and-optout.md)
- [ai-ops command](../commands/ai-ops.md)

### 7.2 Related Code
- `.claude/` - Claude Code 설정
- `.codex/` - Codex 설정
- `AGENTS.md` - AI 도구 공통 규칙
- `.omc/` - OMC 로컬 정책 반영 대상

### 7.3 Related Tests
- 수동 테스트: 새 세션에서 프로세스 선택 질의 발생 여부
- 수동 테스트: `/ai-ops`에서 Team 자동 활성화 여부
- 수동 테스트: `NONE` 분기 일반 작업 경로 확인

### 7.4 Related Commits
- `20034bb` - WP-006 파일럿 #3 완료 및 G4 종료 판정 동기화

## 8. Process Plan
- P0: 현재 도구별 설정 구조 분석
- P1: 프로세스 선택 질의 규칙 설계
- P3: 도구별 설정 구현
- S1: 프로세스 선택 질의 동작 테스트
- S2: 운영 문서 참조 정합성 점검
- S4: 결정과 변경 이력 기록

## 9. Execution Notes
- Phase 3 (G3) 주관 WP
- Track 4 (프로세스 기반 협업 전환) 핵심 작업
- WP-004 완료 후 착수

### P0 분석 결과 (2026-03-08)
- `.omc/state/agent-replay-*.jsonl`에서 `keyword_detected: team -> mode_change: none->team` 확인
- `/ai-ops` 의도와 달리 사용자 선택 전 Team mode가 활성화됨
- Stop hook이 `Team mode active. Continue working.`을 반복해 대기 루프 발생
- `.claude/settings.json` 기준 Claude 네이티브 강제 지점은 `PreToolUse`가 핵심이며, 여기서 프로세스별 차단 로직 구현 가능함

### P1 설계 결과 (2026-03-08)
- `/ai-ops` 흐름을 "추천 -> 사용자 선택 -> 선택 분기 -> 조건부 Team"으로 고정
- 사용자가 프로세스 미적용(`NONE`)을 선택할 수 있도록 정책 추가
- Team 강제 규칙은 ADR-AIOPS-003으로 조건부 규칙으로 개정
- 최소 논리 역할 세트(도구 독립)와 최소 팀 프로파일을 프로세스별로 고정
- Team 모드에서 팀원별 실제 역할(`member:role`) 매핑을 강제로 기록
- 물리 작업 환경 분리 전략(guide 7번)을 master/java8 디렉토리 설정으로 고정
- 프로세스 강제 방식 설계:
  - 선택 결과를 `.omc/ai-ops-process-context.json`에 기록
  - PreToolUse 가드가 선택 프로세스와 도구 호출을 대조
  - `G0/P0/P1/P2/S1/S2/S4`는 읽기/문서 중심, `P3/P4/S3`는 구현 허용

### P3 구현 결과 (2026-03-08)
- `.claude/commands/ai-ops.md` 재작성
- `docs/ai-ops/commands/ai-ops.md` 동기화
- 명령 리네임: `/ai-ops-team` -> `/ai-ops`
- `.claude/CLAUDE.md` team 키워드 트리거 축소 (`"team"` 제거)
- `AGENTS.md`, `.codex/jetbrains-ai-assistant-rules.md` 규칙 동기화
- `docs/ai-ops/omc-config/AI-OPS-POLICY.template.md` 정책 갱신
- `scripts/ai-ops/claude_pretooluse_guard.py` 신규 추가 (프로세스별 하드 차단 + 정합성 검사)
- `scripts/ai-ops/set_process_context.py` 신규 추가 (프로세스 선택 결과 기록)
- `scripts/ai-ops/install_git_hooks.sh`에 Claude guard 동기화 단계 추가
- `docs/ai-ops/tool-hooks/process-enforcement-matrix.md` 신규 추가 (프로세스별 강제 매트릭스)
- `docs/ai-ops/process-catalog/minimum-logical-role-set.md` 신규 추가 (최소 논리 역할/프로파일)
- `set_process_context.py` 확장 (`team_mode`, `profile`, `roles`, `members`)
- `claude_pretooluse_guard.py` 확장 (Team 가능 프로세스에서 `team_mode` 확정/역할 프로파일/팀원 역할 검증)
- `.claude/CLAUDE.md` 로컬 오버레이 추가 (OMC/비OMC 팀원 role 정의 가이드)
- `WORKSPACE-PROFILE.md` 및 `docs/ai-ops/workspace-profiles/` 추가 (master/java8 분리 전략)
- `java8` 디렉토리 방어 문서/도구 규칙 추가 (`AI-RULES.md`, `BRANCH-SAFETY.md`, `.claude`, `.codex`, `docs/branch-specific`)
- `scripts/ai-ops/check_ai_ops_compliance.py`에 기록 라우팅 강제 규칙 추가
  - 제품 코드 변경 시 `docs/project-ops` WP/ADR 기록 동반 강제
  - 제품 변경을 `docs/ai-ops` WP/ADR에 기록하는 오사용 차단
  - 제품 코드/설정 변경 또는 `docs/project-ops` WP/ADR 변경 시 `docs/project-ops/CHANGELOG.md` 동반 갱신 하드 차단
- `java8`에 빌드 강제 스크립트 추가
  - `scripts/workspace/session-check.sh`
  - `scripts/workspace/java8-build.sh`
- `java8` Claude PreToolUse 훅 추가
  - `.claude/settings.json`
  - `.claude/hooks/pretooluse-java8-build-guard.py`
- `master` Claude PreToolUse 훅 보강
  - `master` 세션에서 `cd ../ncube-regression-verify-java8 && mvn ...` 우회 경로 차단
  - `java8` 대상 빌드/테스트는 `./scripts/workspace/java8-build.sh`만 허용
- `/ai-ops` 명령 규칙 보강
  - P4 + backport/java8/wafful4 요청 시 Backport 서브플로우 강제
  - 백포팅 완료 후 `master` source WP에 Backport Trace 기록 의무화
- ai-ops/project-ops 기록 경계 정리
  - `docs/project-ops/work-packets/index.md` 복구
  - `docs/project-ops/CHANGELOG.md` 단일 통합 changelog 체계 복구
  - `docs/ai-ops/work-packets/index.md`에서 제품 WP 참조 제거
- ai-ops 통합 changelog 경로 승격
  - `docs/ai-ops/work-packets/CHANGELOG.md` -> `docs/ai-ops/CHANGELOG.md`로 이동
  - compliance checker/헌법/계획/훅 문서의 참조 경로 동기화
- `python3 scripts/ai-ops/check_ai_ops_compliance.py --mode none|working_tree` 통과
- `claude_pretooluse_guard.py` 샘플 페이로드 테스트 통과
  - P0 컨텍스트에서 코드 수정 요청 차단
  - P3 컨텍스트에서 구현 변경 허용

## 10. Deliverables
- `.claude/commands/ai-ops.md`
- `docs/ai-ops/commands/ai-ops.md`
- `.claude/CLAUDE.md`
- `.codex/` 규칙 업데이트
- `AGENTS.md` 규칙 업데이트
- `docs/ai-ops/omc-config/AI-OPS-POLICY.template.md`
- `scripts/ai-ops/claude_pretooluse_guard.py`
- `scripts/ai-ops/set_process_context.py`
- `docs/ai-ops/tool-hooks/process-enforcement-matrix.md`
- `docs/ai-ops/process-catalog/minimum-logical-role-set.md`
- `.claude/CLAUDE.md` (AI Ops Local Overlay)
- `java8/scripts/workspace/java8-build.sh`
- `java8/.claude/hooks/pretooluse-java8-build-guard.py`
- 수동 테스트 결과(후속 S1)

## 11. Review Notes
- 수동 테스트로 Team 자동 활성화 방지/`NONE` 분기 동작을 재검증했고 기준 충족으로 판정
- 사용자 경험 (질의 피로) 검토 필요

## 12. Decisions
| 결정 | 선택 | 이유 |
|------|------|------|
| 운영 문서 참조 | ai-collaboration-guide.md 대신 process-catalog/ | 설계 문서 ≠ 운영 문서 분리 원칙 |
| Team 정책 | 필수 강제에서 조건부 활성화로 변경 | 사용자 선택 전 자동 활성화/대기 루프 방지 |
| opt-out | `NONE` 분기 허용 | 사용자가 프로세스 미적용 경로를 선택할 수 있도록 보장 |
| 최소 역할 세트 | 도구 독립 Logical Role + 프로세스별 최소 프로파일 | 팀원 변동에도 프로세스 보장/누락 방지 |
| 팀원 role 매핑 | `team_mode=team` 시 `member:role` 필수 | OMC 사용 유무와 무관한 역할 책임 고정 |
| 물리 환경 분리 | master/java8 워크스페이스 별 전용 규칙 문서화 | 브랜치/런타임 혼동으로 인한 오작동 방지 |
| 제품 이력 동기화 | project-ops 기록 변경 시 통합 changelog 동반 강제 | `/ai-ops` 수행 중 제품 이력 누락 방지 |

## 13. Follow-ups
- WP-AIOPS-2026-03-006 (파일럿 검증)과 연결
- 프로세스 선택 질의 사용자 경험 피드백 반영
- WP-AIOPS-2026-03-001 종료 정합성 점검(부모 WP 상태 전이)

## 14. Timeline
- [2026-03-07] 작업 생성 (Master Plan 보강 시)
- [2026-03-08] P0 분석: Team 자동 활성화/Stop hook 대기 루프 원인 확인
- [2026-03-08] P1 설계: 추천/선택/분기/조건부 Team 흐름 확정
- [2026-03-08] P3 구현: 명령/정책/규칙 파일 반영
- [2026-03-08] P3 구현: 프로세스 컨텍스트 + Claude PreToolUse 강제 가드 반영
- [2026-03-08] P3 구현: 최소 논리 역할 세트 + team_mode/역할 프로파일 강제 반영
- [2026-03-08] P3 구현: 팀원별 실제 역할(`member:role`) 강제 + Claude OMC/비OMC 병행 가이드 반영
- [2026-03-08] P3 구현: Claude 진입 명령을 `/ai-ops`로 리네임하고 참조 경로 동기화
- [2026-03-08] P3 구현: ai-collaboration-guide 7번 기준 master/java8 물리 분리 설정 반영
- [2026-03-08] P3 구현: ai-ops/project-ops 기록 라우팅 하드 강제 + java8 빌드 명령/JDK8 강제 훅 반영
- [2026-03-08] P3 구현: master 세션의 java8 직접 mvn 우회 경로 차단 + P4 백포팅 trace 기록 규칙 추가
- [2026-03-08] P3 구현: ai-ops/project-ops 분리 정합성 보강 (project-ops index/changelog 복구, ai-ops 인덱스 제품 참조 제거)
- [2026-03-08] P3 구현: ai-ops changelog를 docs/ai-ops/CHANGELOG.md 단일 경로로 승격하고 참조/검사 규칙 동기화
- [2026-03-08] P3 구현: 제품 코드/설정 + project-ops WP/ADR 변경 시 `docs/project-ops/CHANGELOG.md` 동반 갱신 하드 차단 추가
- [2026-03-08] S1 수동 검증 완료 (WP-006 결과 + guard 재검증)
  - 프로세스 미선택 상태에서 수정도구 호출 시 차단 확인
  - Team 가능 프로세스(`P3`)에서 `team_mode=auto`일 때 구현 변경 차단 확인
- [2026-03-08] S2 수동 검증 완료 (`NONE` 분기)
  - `NONE` + `team_mode=single` 컨텍스트에서 수정도구 허용 확인
- [2026-03-08] S4 완료: WP-005 DONE 상태 전이 및 ai-ops 인덱스/체인지로그 동기화
