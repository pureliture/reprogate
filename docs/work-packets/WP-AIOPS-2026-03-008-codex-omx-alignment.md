---
packet_id: "WP-AIOPS-2026-03-008"
title: "Codex+OMX 조합 정렬 및 Claude+OMC 성공패턴 이식"
goal_ids: ["AIOPS-G3", "AIOPS-G5"]
status: "IN_RECORDING"
work_type: "FEATURE"
priority: "P0"
target_environment: "master"
start_process: "P0"
current_process: "P3"
next_process: "S1"
owner: "SHARED"
created_at: "2026-03-08"
last_updated: "2026-03-09"
---
# WP-AIOPS-2026-03-008 Codex+OMX 조합 정렬 및 Claude+OMC 성공패턴 이식

## 1. Background
- `AGENTS.md`가 `oh-my-codex` 템플릿으로 교체되며 프로젝트 어댑터 규칙과 런타임 템플릿 간 경계가 불명확해졌다.
- `claude+omc`는 `/ai-ops` + PreToolUse + 기록 동기화(Traceability) 조합으로 파일럿(WP-006) 검증을 통과했다.
- `codex+omx`도 동일한 운영 구조(프로세스 선택 강제, 팀 모드 안전장치, 기록 라우팅)를 재현해야 한다.
- 이번 라운드의 soft guarantee baseline은 남겨두되, 사용자가 원한 `Claude` 수준의 runtime hard guarantee와 차이가 있어 별도 재분석이 필요하다.
- 추가로, `WP-006`과 동등한 파일럿으로 보려면 `Codex+OMX`에도 `/ai-ops`에 대응하는 명시적 entrypoint parity가 필요하다는 요구가 새로 확인되었다.
- 후속 사용자 결정으로, JetBrains AI Assistant 일반 경로는 `$ai-ops`를 사용하지 않고 `AGENTS.md` + SoT를 직접 따르도록 정리해야 한다는 방향이 확정되었다.

## 2. Goal
- Codex CLI + OMX 경로를 `claude+omc` 성공 구조와 동일한 운영 기준으로 정렬한다.
- 런타임 템플릿(`AGENTS.md`/`.claude/CLAUDE.md` 등)과 프로젝트 정책(`docs/ai-ops`)의 소유 경계를 명시한다.
- 임시 프로세스(2회 한정)로 이식 검증 후 상시 운영 여부를 판정한다.
- 현재 `Codex+OMX` 표면에서 runtime hard guarantee가 가능한지와 필요한 구현 경로를 판단한다.
- `Claude`의 `/ai-ops`와 동등한 사용자 진입점을 `Codex+OMX` 표면에 맞는 형태로 정의한다.
- Codex+OMX `$ai-ops` 경로와 JetBrains AI Assistant 일반 경로의 소유 경계를 다시 분리하고, 비정규 참조와 과잉 토큰 비용을 줄인다.

## 3. Scope
### 3.1 운영 구조 정렬
- Codex 진입/운영 규칙을 `claude+omc`의 핵심 패턴(프로세스 선택 -> 조건부 Team -> 검증/기록)으로 정렬
- `AGENTS.md`의 역할을 "런타임 어댑터 + 정책 진입점"으로 재정의

### 3.2 임시 프로세스 운영
- `WP-008` 범위 한정 임시 프로세스(2회) 정의
- 파일럿별 체크리스트/증빙 항목 강제
- 종료 시 임시 가드 sunset 기록

### 3.3 문서 동기화
- `docs/ai-ops/ops-bootstrap-master-plan.md`
- `docs/ai-ops/work-packets/index.md`
- `docs/ai-ops/CHANGELOG.md`
- 부모 WP(`WP-AIOPS-2026-03-001`) follow-up 연결

### 3.4 Hard Guarantee 재분석
- `Codex CLI`, `OMX hooks`, `derived watcher`, `AGENTS.md` adapter가 mutation 이전 차단점을 제공하는지 재검토
- 지원 표면만으로 불가능하면 그 이유와 외부 wrapper/native hook 의존 여부를 정리

### 3.5 Entrypoint Parity
- `Codex+OMX` 파일럿이 `WP-006`과 동등하다고 볼 수 있도록, 명시적 named entrypoint를 정의
- exact `/ai-ops` 복제보다 `OMX` 표면에 맞는 등가 진입점(`$ai-ops` skill 등)을 우선 검토
- JetBrains AI Assistant 일반 경로는 `$ai-ops` parity에서 분리하고, `AGENTS.md` 중심 일반 진입으로 정리

## 4. Out of Scope
- OMX/OMC 외부 배포본 자체 코드 수정
- 제품 기능(`docs/project-ops`, `src/`) 변경
- 기존 완료 WP(WP-005/006/007)의 재정의

## 5. Done Criteria
- [ ] Codex+OMX 이식 범위와 운영 경계가 문서로 고정됨
- [ ] 임시 프로세스(2회 한정) 단계/체크리스트가 정의됨
- [ ] 파일럿 #1 완료 기록(체크리스트 포함)
- [ ] 파일럿 #2 완료 기록(체크리스트 포함)
- [ ] Team auto 방지/NONE 분기 검증 결과가 기록됨
- [ ] `index.md`, `CHANGELOG.md`, `master-plan` 동기화 완료
- [ ] 임시 프로세스 sunset(종료/상시화 판정) 기록 완료
- [ ] Codex+OMX hard guarantee feasibility와 비지원 경계가 기록됨
- [ ] 외부 wrapper/native hook/비지원 판정 중 후속 경로가 제안됨
- [ ] Codex+OMX용 명시적 entrypoint ownership과 JetBrains AI Assistant decoupling 정책이 정의됨
- [ ] Codex SoT에 사용자 선택 전 Team 금지 규칙이 직접 반영됨

## 6. Risks / Constraints
- 런타임 템플릿 자동 주입 시 프로젝트 규칙이 덮어써질 수 있음
- Codex/Claude 도구 동작 차이로 동일 규칙의 표현 방식이 달라질 수 있음
- 임시 가드 종료 기준이 모호하면 운영 복잡도가 지속될 수 있음
- 현재 Codex CLI에는 Claude `PreToolUse`와 동급의 네이티브 mutation 전 차단 표면이 명확하지 않다.
- OMX 파생 hook 신호는 별도 watcher 기반이라 실행 전 차단보다 사후 감시에 가깝다.

## 7. Related References
### 7.1 Related Docs
- [WP-AIOPS-2026-03-005](./WP-AIOPS-2026-03-005-process-based-collaboration.md)
- [WP-AIOPS-2026-03-006](./WP-AIOPS-2026-03-006-pilot-verification.md)
- [WP-AIOPS-2026-03-007](./WP-AIOPS-2026-03-007-ai-tool-artifact-separation.md)
- [운영체계 구축 상위 계획](../ops-bootstrap-master-plan.md)
- [AI Ops Constitution](../constitution.md)

### 7.2 Related Code
- `AGENTS.md`
- `.codex/`
- `.claude/CLAUDE.md`
- `.claude/hooks/pretooluse-ai-ops-guard.py`
- `docs/ai-ops/tool-hooks/codex-jetbrains-ai-assistant-rules.md`
- `docs/ai-ops/omc-config/AI-OPS-POLICY.template.md`
- `scripts/ai-ops/set_process_context.py`
- `scripts/ai-ops/launch_ai_ops_session.py`
- `scripts/ai-ops/check_ai_ops_compliance.py`
- `.agents/skills/ai-ops/SKILL.md`

### 7.3 Related Tests
- 수동 테스트: 프로세스 미선택 상태 변경성 호출 차단
- 수동 테스트: Team 가능 프로세스의 `team_mode=auto` 차단
- 수동 테스트: `NONE` 분기 단일 실행 허용

### 7.4 Related Commits
- `ed69e1b` - WP-008 P0 분석 완료 및 active board/changelog 반영
- `a194e1d` - WP-008 P1 설계 및 capability-first 운영 방향 고정
- `753eb68` - WP-008 P3 Codex+OMX soft guarantee chain 반영
- `7756dc6` - WP-008 S1 리뷰 완료 및 P3 승인 반영
- `5048bfa` - WP-008 S4 기록 완료 및 현재 라운드 결정사항 고정
- `9dcf893` - WP-008 P0 보강: Codex+OMX hard guarantee feasibility 분석
- `2285144` - WP-008 P3 OMX-centered launch gate 구현
- `e14e4da` - WP-008 P2 완료: OMX 기반 hard gate 우회 전략 확정
- `982debd` - WP-008 P1 완료: OMX-centered hard gate 요구사항 구체화
- `a69c2e1` - Claude+OMC 후속 정렬 방향을 thin-adapter + SoT 원칙으로 명시
- `cb0ab8f` - WP-008 S1 리뷰 완료 및 launch gate 승인 반영
- `eccea3d` - WP-008 P3 Codex named entrypoint parity로 `$ai-ops` skill 추가
- `d4fe1c6` - WP-008 S1 리뷰 완료 및 `$ai-ops` parity 승인 반영
- `9533044` - WP-008 P0 ad-hoc 산출물 소급 복원 범위 분석
- `929b44a` - WP-008 P2 authoritative evidence 기반 소급 복원 전략 선택
- `52ee5bf` - WP-008 S4 retro recovery round 기록 고정

## 8. Process Plan
- P0: Codex+OMX 현재 구조/Gap 분석
- P1: 목표 운영 구조/임시 가드 설계
- P3: 문서/규칙 반영
- S1: 파일럿 검증
- S2: 운영 문서 동기화
- S4: 종료 판정 및 기록
- P0(보강): Codex+OMX hard guarantee feasibility / interception point 재분석

## 9. Execution Notes
### 9.1 임시 프로세스 (2회 한정)
목적:
- `codex+omx` 전환 초기에 누락 방지용 체크리스트를 강제한다.
- 상시 훅으로 즉시 승격하지 않고 WP-008 범위에서만 운영한다.

적용 범위:
- 파일럿 #1, #2
- 파일럿 #2 종료와 함께 임시 프로세스 종료 여부를 판정한다.

체크리스트(파일럿 공통):
- [ ] 대상 WP/문서 경로를 명시했다.
- [ ] 선택 프로세스와 실제 수행 체인을 기록했다.
- [ ] Team auto 방지 검증 결과를 기록했다.
- [ ] `NONE` 분기 검증 결과를 기록했다.
- [ ] `docs/ai-ops/CHANGELOG.md` 동반 갱신을 확인했다.

### 9.2 파일럿 기록 템플릿
- Pilot Target:
- Process Chain:
- 검증 결과:
- 체크리스트 충족 여부:
- 후속 조치(next_process):

### 9.3 G0 목표 정합성 점검 결과
- 점검 시점: `P0` 시작 시점
- North Star 연결: `AIOPS-G3`(추적 가능성 유지), `AIOPS-G5`(AI 운영 문서와 런타임 산출물 경계 분리)
- 현재 Phase / Gate: `Phase 6 / G6`
- 작업 대상 WP: `WP-AIOPS-2026-03-008` / `READY` / `P0`
- 목표 drift: 없음
- 누락 Track/WP: 없음
- 암묵적 작업: 없음
- 확인 기준 문서:
  - `docs/ai-ops/constitution.md`
  - `docs/ai-ops/ops-bootstrap-master-plan.md`
  - `docs/ai-ops/work-packets/index.md`

### 9.4 P0 현재 구조 / Gap 분석
- 분석 대상 요약:
  - Codex+OMX 경로의 저장소 진입점, 프로세스 선택 강제 방식, Team 조건부 활성화 규칙, 기록/검증 라우팅을 `claude+omc` 성공패턴과 비교했다.
- 현재 구성요소 맵:
  - Codex+OMX: `AGENTS.md`(generic OMX runtime), `.codex/jetbrains-ai-assistant-rules.md`, `docs/ai-ops/tool-hooks/codex-jetbrains-ai-assistant-rules.md`
  - Claude+OMC: `.claude/CLAUDE.md`, `docs/ai-ops/omc-config/AI-OPS-POLICY.template.md`, `.claude/hooks/pretooluse-ai-ops-guard.py`
  - 공통 제어면: `docs/ai-ops/commands/ai-ops.md`, `docs/ai-ops/tool-hooks/process-enforcement-matrix.md`, `scripts/ai-ops/set_process_context.py`, `scripts/ai-ops/check_ai_ops_compliance.py`
- 현재 동작 요약:
  - 두 경로 모두 `set_process_context.py`와 `docs/ai-ops` 문서를 공통 기준으로 사용한다.
  - Claude+OMC는 정책 템플릿 + PreToolUse 가드로 실행 중 차단과 품질 게이트 연계를 수행한다.
  - Codex+OMX는 AGENTS 및 `.codex` 규칙 중심이며, 최종 방어선은 Git hooks / compliance checker다.
- 식별된 Gap:
  1. 저장소 진입점 경계 불명확:
     - `AGENTS.md`는 generic OMX 팀/실행 파이프라인 중심이며, AI Ops 전용 로컬 오버레이가 없다.
     - 반면 Codex 프로세스 게이트는 `.codex/jetbrains-ai-assistant-rules.md`에 위치해 저장소 공통 진입점과 분리되어 있다.
  2. 강제 수준 비대칭:
     - Codex 문서는 스스로 "네이티브 차단 훅이 없으므로 소프트 강제"라고 정의한다.
     - Claude는 PreToolUse 가드에서 미선택/`team_mode=auto`/읽기전용 위반을 런타임에 즉시 차단한다.
  3. Source of Truth / 동기화 경로 비대칭:
     - OMC는 `docs/ai-ops/omc-config/`를 정책 원본으로 두고 로컬 `.omc/`로 동기화하는 경로가 명시돼 있다.
     - Codex는 `AGENTS.md` + `.codex/` 조합만 정의되어 있어, "정책 원본 -> 런타임 반영" 경계가 Claude 경로만큼 명확하지 않다.
  4. 컨텍스트 drift 탐지 약점:
     - 프로세스 컨텍스트는 `.omc/ai-ops-process-context.json`에 기록되지만, Codex에는 Claude PreToolUse에 해당하는 실행 중 하드가드가 없다.
     - 실제 재선택 직전 컨텍스트가 `selected_process=P2`, `selected_wp=""` 상태로 남아 있었다.
- 위험 포인트:
  - generic OMX 기본 Team 파이프라인이 AI Ops의 "프로세스 선택 후 조건부 Team" 원칙과 충돌할 수 있다.
  - `.codex/`는 로컬 전용 경로라 원격 추적으로 관리할 수 없으므로 정책 drift가 발생하기 쉽다.
  - Codex 경로는 최종 Git hook 단계에서야 차단되므로 오류 탐지가 늦다.
- 미확정 항목:
  - AI Ops 로컬 오버레이를 `AGENTS.md`에 직접 고정할지, marker-bounded 런타임 블록으로 주입할지
  - Codex용 "소프트 강제"를 어디까지 유지하고, 어떤 항목을 문서/스크립트 계층으로 상향할지
  - WP-008 파일럿 #1/#2의 증빙 템플릿을 WP 내부에 둘지 별도 문서로 분리할지
- 후속 권장 프로세스:
  - `P1`: 목표 운영 구조, 오버레이 소유 경계, 임시 체크리스트/파일럿 기록 형식을 설계

### 9.5 우선순위 / 장기 방향 메모
- 현재 세션 우선순위:
  - `Codex+OMX` 경로 완성 및 G6 범위(정렬, 파일럿, sunset 판정) 달성을 우선한다.
- 후순위로 미루는 항목:
  - `CLAUDE.md` 수정/재구성 계획
  - marker block / sync script / installer 전략
  - 마켓플레이스/즉시 설치형 프로덕트 패키징 설계
- 장기 방향:
  - `ai-ops`는 장기적으로 `oh-my-claudecode`와 유사한 오픈소스이자, AI 도구에 간단한 명령 또는 마켓플레이스 등록으로 바로 사용할 수 있는 프로덕트로 발전시키는 것을 목표로 한다.
- 현재 판단 근거:
  - 위 장기 방향은 유지하되, 현 단계에서는 `ai-ops` 자체의 정렬/안정화가 우선이며 제품화 메커니즘 설계는 시기상조로 본다.

### 9.6 P1 목표 운영 구조 / 임시 가드 설계
- 설계 목표:
  - `Codex+OMX`를 개별 엔진 재구현이 아니라 `ai-ops` 운영체계 레이어의 한 실행 경로로 정렬한다.
  - `CLAUDE.md` 개편이나 제품화 메커니즘 설계 없이도, 현재 저장소에서 `Codex+OMX` 경로를 일관된 규칙 아래 동작시키는 최소 구조를 정의한다.
- capability-first 원칙:
  - 운영 규칙은 특정 명령어/기능명이 아니라 capability 기준으로 정의한다.
  - 도구별 명령, UI, 플러그인 기능은 adapter 계층의 현재 매핑으로만 취급한다.
- 목표 구조:
  1. Framework SoT:
     - 정책/프로세스/검사기는 `docs/ai-ops/`, `scripts/ai-ops/`를 단일 진실 소스로 유지한다.
  2. Project Adapter:
     - `AGENTS.md`, `WORKSPACE-PROFILE.md`는 `Codex+OMX`가 SoT를 읽고 진입하도록 연결하는 얇은 어댑터로 취급한다.
     - `AGENTS.md`는 generic OMX 런타임 위에 `AI Ops Local Overlay`를 추가하는 방향으로 정렬한다.
  3. Local Runtime:
     - `.omx/`, `.codex/`, `.omc/`는 Local-only 실행 영역으로 유지하고, 정책 본문 저장소로 사용하지 않는다.
- capability 계약:
  1. Context Loading:
     - 현재 워크스페이스, 상위 계획, active WP를 읽고 작업 기준선을 복원할 수 있어야 한다.
  2. Process Selection:
     - 사용자에게 권장 프로세스와 대안을 제시하고, 선택 결과를 상태 파일에 기록할 수 있어야 한다.
  3. Delegation / Multi-role Execution:
     - 하위 작업 위임 또는 병렬 오케스트레이션 capability가 있을 때만 다중 역할 경로를 사용할 수 있다.
     - 해당 capability가 없거나 불안정하면 `single` 경로로 degrade 한다.
  4. Verification / Enforcement:
     - 실행 중 훅 또는 종료 전 게이트를 통해 규칙 위반을 탐지/차단할 수 있어야 한다.
- Codex+OMX 표준 진입 흐름:
  1. `WORKSPACE-PROFILE.md` -> `constitution.md` -> `ops-bootstrap-master-plan.md` -> `work-packets/index.md` 확인
  2. 권장 프로세스 제시 + 사용자 선택
  3. `set_process_context.py`로 선택 프로세스 기록
  4. 다중 역할 경로가 필요한 프로세스(`P3`, `P4`, `S3`, 필요 시 `S1`)는 현재 toolchain이 위임/병렬 실행 capability를 제공할 때만 `team_mode`를 확정 후 진입
  5. 단계 종료 시 `current_process`, 수행 내용, 산출물 경로, 체크리스트 충족 여부, `next_process`를 보고
  6. 종료 전 `check_ai_ops_compliance.py --mode working_tree` 검증
- Codex 경로 정렬 원칙:
  - `AGENTS.md`는 Codex 경로의 1차 진입점으로 강화하되, 정책 본문을 과도하게 내장하지 않는다.
  - `.codex/jetbrains-ai-assistant-rules.md`는 로컬 보조 규칙으로 유지하되, 핵심 규칙의 출처는 `docs/ai-ops`로 명시한다.
  - Codex 경로는 현재 Claude PreToolUse와 같은 실행 중 하드가드를 보장하지 않으므로, `AGENTS.md` 안내 + 문서 구조 + 최종 compliance 게이트 조합으로 정렬한다.
  - 문서 본문은 `subagent`, `team orchestration` 같은 가변 기능명을 규범 문장으로 쓰지 않고, 필요한 경우 "현재 매핑 예시"로만 기록한다.
- WP-008 임시 프로세스 설계:
  - 파일럿 #1, #2는 아래 6개 항목을 공통 증빙으로 남긴다.
    1. 대상 WP/문서 경로
    2. 선택 프로세스
    3. 실제 수행 체인
    4. Team auto 방지 검증 결과
    5. `NONE` 분기 검증 결과
    6. `docs/ai-ops/CHANGELOG.md` 동반 갱신 여부
  - 파일럿 #2 종료 시 sunset 판정을 기록하고, 목적 달성 시 임시 가드는 재사용하지 않는다.
- 이번 WP에서 명시적으로 후순위로 두는 항목:
  - `.claude/CLAUDE.md` 재구성
  - marker block / sync script / installer
  - 오픈소스/마켓플레이스 배포 포맷
- P3 구현 범위:
  - `scripts/ai-ops/set_process_context.py`에 team-capable process의 single fallback logical role 유지 반영
  - `AGENTS.md`에 Codex+OMX용 AI Ops 어댑터 오버레이 정렬
  - `docs/ai-ops/tool-hooks/codex-jetbrains-ai-assistant-rules.md`와 `process-enforcement-matrix.md`를 capability-first 문구로 보강
  - WP-008 파일럿 기록 템플릿 및 종료 보고 형식 반영
- P1 종료 판단:
  - `Codex+OMX` 목표 구조, 경계, 임시 프로세스 증빙 형식, P3 구현 범위가 문서화되었으므로 구현 단계로 넘길 입력이 준비되었다.

### 9.7 S1 리뷰 결과
- 리뷰 대상:
  - `P3` 커밋 `753eb68`
  - `AGENTS.md`, `scripts/ai-ops/set_process_context.py`, Codex 규칙 문서, 강제 매트릭스, WP/관제 문서
- 검토 결과:
  - `P3` 목표였던 Codex+OMX soft guarantee chain 반영은 완료되었다.
  - `team_mode=single` fallback에서도 `DELIVERY_MIN3` 논리 역할이 유지되도록 컨텍스트 스크립트가 보강되었다.
  - Codex 경로의 소프트 보장 체계(`AGENTS.md` -> 컨텍스트 기록 -> 종료 보고 -> compliance gate)가 문서와 스크립트에 반영되었다.
- S1 중 식별 및 보정한 문서 불일치:
  - G0 결과 섹션의 상태 표기를 점검 시점 기준으로 명확화
  - `P3 구현 범위(예정)` 표현을 완료 기준 서술로 정정
- 승인 판단:
  - **승인(Approve)**. `P3` 결과는 설계 의도와 완료 기준에 대체로 부합한다.
- 잔여 리스크 / 보완 후보:
  - Codex 경로는 여전히 Claude PreToolUse 같은 실행 중 하드가드가 없으므로, 실제 유도력은 후속 파일럿에서 검증이 필요하다.
  - `P0`, `P1`, `S1` 같은 프로세스 코드가 직관적이지 않다는 사용자 관찰이 있어, 추후 alias 또는 명시적 라벨 체계 검토가 필요하다.
- 후속 권장 프로세스:
  - `S4`: 이번 단계의 리뷰 결과와 승인 판단을 변경 이력/의사결정으로 고정

### 9.8 S4 변경 이력 / 의사결정 기록
- 작업 배경:
  - WP-008은 `Codex+OMX` 경로를 `Claude+OMC` 성공패턴과 정렬하되, 현재 단계에서는 하드가드보다 소프트 보장 체계를 우선 반영하는 작업이다.
- 실제 변경 요약:
  - `P0`: Codex+OMX vs Claude+OMC 구조/강제 지점/gap 분석 기록
  - `P1`: SoT/Adapter/Local Runtime 경계와 capability-first 문서 원칙 설계
  - `P3`: Codex+OMX soft guarantee chain, `single` fallback logical role 유지, 종료 시 커밋 질의 규칙 반영
  - `S1`: P3 결과 승인 및 문서 불일치 2건 보정
- 선택한 방식과 이유:
  - 선택: Codex 경로는 `AGENTS.md` adapter + context file + 종료 보고 + compliance gate 조합의 soft guarantee로 정렬
  - 이유: 현재 toolchain에서는 Claude PreToolUse와 같은 실행 중 하드 차단을 동일하게 보장할 수 없고, 제품화 메커니즘 설계는 아직 후순위이기 때문이다.
- 선택하지 않은 대안:
  - `CLAUDE.md`/installer/marker block 중심 개편
  - 이유: 장기 방향에는 부합하지만, 현재 WP-008의 우선순위는 `Codex+OMX` 완성과 G6 정렬이다.
- 남은 TODO / 리스크:
  - soft guarantee의 실제 유도력은 파일럿 #1/#2에서 검증 필요
  - `NONE` 분기와 Team auto 방지 결과를 파일럿 증빙으로 실제 기록해야 함
  - 프로세스 코드 가독성 개선 여부는 후속 과제로 남음
- 관련 커밋 연결:
  - `ed69e1b`, `a194e1d`, `753eb68`, `7756dc6`

### 9.9 P0 보강 - Codex+OMX Hard Guarantee Feasibility
- 분석 목적:
  - 현재 `Codex+OMX` 표면만으로 `Claude`의 `PreToolUse`와 유사한 runtime hard guarantee를 만들 수 있는지 재평가한다.
- 프로세스/OMX 적용 범위 정리:
  - 핵심 프로세스(`P0~P4`)는 도구-중립 정의이며, 특정 프로세스가 `OMX` 사용을 직접 요구하지 않는다.
  - `P0`, `P1`, `P2`는 Team 사용 가능 프로세스가 아니며, `P3`, `P4`, `S3`, 필요 시 `S1`만 toolchain capability가 있을 때 `team` 경로를 사용할 수 있다.
  - 따라서 `P0`는 `Codex+OMX` 런타임 안에서 수행할 수는 있지만, `OMX` 팀 오케스트레이션을 전제로 하지는 않는다.
- 확인한 표면:
  1. 현재 저장소 규칙:
     - Codex 경로는 `AGENTS.md` + `.codex` + compliance gate 기반의 soft guarantee로 정의되어 있다.
  2. Codex CLI:
     - approvals/sandbox 제어는 있으나, Claude `PreToolUse`와 같은 네이티브 mutation 전 deny hook은 현재 표면에서 확인되지 않았다.
  3. OMX hooks:
     - `omx hooks` 플러그인 표면과 `session-start`, `session-end`, `turn-complete` 같은 이벤트는 존재한다.
     - 그러나 플러그인 dispatch는 결과를 기록/반환할 뿐, 실패 결과를 Codex 실행 차단으로 연결하는 contract가 없다.
  4. OMX derived watcher:
     - `pre-tool-use` / `post-tool-use`는 `~/.codex/sessions/.../rollout-*.jsonl`를 폴링하는 watcher가 추론하는 derived signal이다.
     - watcher는 opt-in(`OMX_HOOK_DERIVED_SIGNALS=1`)이며 실행 전 차단이 아니라 사후 감시에 가깝다.
     - OMX 설치본 주석도 `pre-tool-use`, `post-tool-use`가 Codex CLI 네이티브 훅이 아니라 OMC 쪽 전용 개념임을 명시한다.
- 결론:
  - **현재 지원되는 Codex+OMX 표면만으로는 Claude급 runtime hard guarantee를 구현할 수 없다고 판단한다.**
  - 이유는 mutation 직전의 네이티브 deny point가 없고, OMX hook/plugin 표면도 차단 contract보다 관찰/부수효과 실행에 가깝기 때문이다.
- 가능한 후속 경로:
  1. 외부 wrapper / gateway:
     - Codex 실행 외부에서 승인/명령 경로를 감싸는 별도 차단 레이어를 설계한다.
  2. derived watcher 기반 best-effort 중단:
     - 세션/툴 사용을 감지해 종료시키는 우회는 가능할 수 있으나, race condition 때문에 hard guarantee로 보기 어렵다.
  3. Codex native hook 지원:
     - upstream 수준의 pre-tool deny API가 추가되어야 Claude와 동급의 보장을 만들 수 있다.
- 위험 포인트:
  - unsupported kill-switch나 tmux/send-keys 기반 중단은 brittle하고 capability-first 원칙에도 맞지 않는다.
  - hard guarantee 목표를 유지하더라도 현재 Phase 6 범위에서 달성 가능한 수준과 불가능한 수준을 구분해야 한다.
- 후속 권장 프로세스:
  - `P2`: 현재 지원 표면에서 가능한 우회/대체 enforcement 전략과 외부 wrapper 후보를 비교해 우선 전략을 도출

### 9.10 P2 트러블슈팅 전략 도출 - Hard Guarantee 우회 경로 비교
- 문제 정의:
  - 사용자가 원하는 것은 `Codex+OMX`에서 `Claude PreToolUse`와 유사한 수준으로, 프로세스/실행 경로가 확정되기 전 변경을 물리적으로 막는 hard guarantee다.
- 증상 / 재현 조건:
  - 현재 Codex 경로는 `AGENTS.md`/`.codex`/compliance gate 조합의 soft guarantee만 제공한다.
  - `P0`, `P1`, `P2`처럼 원래 변경이 없어야 하는 단계에서도, 현재 지원 표면만으로는 Claude와 동일한 runtime pre-tool 차단을 보장할 수 없다.
- 영향 범위:
  - `Codex+OMX` 전체 경로
  - 특히 write-capable 세션 진입, Team 가능 프로세스(`P3`, `P4`, `S3`, 필요 시 `S1`)의 `team_mode=auto` 방지, 프로세스 미선택 상태 변경 방지가 직접 영향권이다.
- 원인 가설:
  1. Codex CLI에는 Claude `PreToolUse`와 동급의 네이티브 mutation 전 deny hook이 없다.
  2. OMX hooks는 observer/additive surface이며, plugin failure를 leader 실행 차단으로 연결하지 않는다.
  3. derived watcher는 세션 로그 폴링 기반이라 사후 감지 구조다.
  4. 따라서 현재 저장소 내부 문서/스크립트만으로는 runtime hard guarantee를 만들 수 없다.
- 해결안 후보:
  1. OMX-centered process-aware launch wrapper / gateway
     - 개념: `omx` launch 진입점에서 프로세스 컨텍스트를 읽고, 허용된 launch profile만 열어 주는 wrapper/gateway를 둔다.
     - 방식:
       - `P0/P1/P2/S2/S4` 같은 분석/기록 계열은 read-only 세션으로 강제
       - `P3/P4/S3/(조건부 S1)`는 `team_mode`와 컨텍스트가 확정된 경우에만 write-capable 세션 시작 허용
       - 세션 전환이 필요하면 재실행/재진입으로 처리
       - 필요 시 `OMX_HOOK_PLUGINS=1`을 켜고 `session-start`/`turn-complete` 계열 hook plugin으로 기록/점검/탐지를 보강
     - 장점:
       - 현재 Codex/OMX가 이미 가진 outer CLI + launch arg passthrough 표면을 활용 가능
       - session-entry 시점에는 soft가 아닌 hard gate를 만들 수 있음
       - `team_mode=auto` 상태의 write-capable 세션 시작 자체를 막을 수 있음
     - 한계:
       - Claude처럼 tool call 단위 pre-tool granularity는 아님
       - write-capable 세션 안에 들어간 뒤의 세부 역할 위반까지 물리적으로 막아 주지는 못함
       - 프로세스 전환 시 재실행 UX가 필요함
       - 현재 OMX plugin contract만으로 leader 실행을 deny 하지는 못하므로, hook은 wrapper의 보조층으로만 사용 가능
  2. derived watcher 기반 best-effort kill switch
     - 장점: 현재 OMX surface만으로도 실험 가능
     - 한계: post-hoc/race condition/unsupported side effect로 hard guarantee라고 보기 어려움
  3. Git pre-commit / pre-push hard gate 유지
     - 장점: 커밋 트랜잭션 수준에서는 여전히 가장 확실한 최종 방어선
     - 한계: mutation 자체를 막지는 못하고 사후 차단이다.
  4. OS 레벨 readonly 잠금
     - 장점: 특정 고정 문서/경로에 대해 가장 물리적인 차단이 가능하다.
     - 한계: 운영 부담이 크고, 자주 바뀌는 문서/일반 개발 흐름에는 너무 brittle하다.
  5. upstream native hook 대기
     - 장점: Claude와 가장 유사한 보장 가능성
     - 한계: 현 세션/현 저장소에서 구현 불가, 일정이 외부 의존적
- 우선 전략 선택:
  - **1순위: OMX-centered process-aware launch wrapper / gateway**
  - 선택 이유:
    - 현재 지원되는 표면 안에서 가장 강한 보장을 줄 수 있다.
    - capability-first 원칙에 맞고, `Codex+OMX`를 엔진이 아니라 운영체계 레이어의 실행 경로로 다룰 수 있다.
    - `OMX`를 버리는 전략이 아니라, `OMX`의 launch/hook surface를 운영체계 게이트에 편입하는 방향이라 현재 아키텍처와도 맞다.
    - derived watcher 같은 brittle 우회보다 운영체계 설계로 설명 가능하다.
- 보조 전략:
  - `OMX hooks`는 단독 hard gate가 아니라 wrapper/gateway의 탐지/telemetry 보강용으로 제한한다.
  - Git hook은 최종 트랜잭션 hard gate로 유지한다.
  - OS readonly 잠금은 매우 제한된 경로에만 선택적으로 고려한다.
  - upstream native hook은 장기 추적 항목으로 남긴다.
- 수정 전 추가 관측 / 검증 필요 항목:
  1. `omx` launch 경로에서 Codex launch args(`--sandbox read-only`, `workspace-write`, approval policy 등)를 wrapper가 일관되게 주입할 수 있는지 확인
  2. write-capable 세션 시작 전 컨텍스트 파일 검증 실패 시 wrapper가 명확히 실패하도록 UX 정의
  3. 프로세스 전환 시 read-only -> write-capable 재진입 절차와 기록 위치 정의
  4. `NONE` 분기에서 wrapper가 어떤 launch profile을 허용할지 결정
- 후속 권장 프로세스:
  - `P1`: wrapper/gateway 기반 hard gate를 구현 가능한 요구사항으로 구체화

### 9.11 P1 요구사항 구체화 - OMX-centered Hard Gate
- 설계 목표:
  - `Codex+OMX` 경로에서 `Claude PreToolUse`와 동일한 tool-call parity를 재현하려 하지 않고, 현재 지원 표면 안에서 가장 강한 **session-entry hard gate**를 정의한다.
  - 외부 소규모 오픈소스(`Codex-Wrapper` 등)는 개념 참고만 하고, 저장소 구현은 `OMX` 중심 구조로 설계한다.
- 문제 정의:
  - 현재 `Codex+OMX`는 soft guarantee와 Git hook 최종 차단은 갖고 있지만, writable session 시작 전 hard gate가 없다.
- 범위:
  1. Launch entrypoint wrapper / gateway
     - `omx` 또는 Codex launch 직전에 프로세스 컨텍스트를 읽고 허용된 launch profile만 열어 준다.
  2. Launch profile 분리
     - `READ_ONLY_ANALYSIS`: `G0`, `P0`, `P1`, `P2`, `S2`, `S4`
     - `WRITE_DELIVERY_SINGLE`: `P3`, `P4`, `S3`, 필요 시 `S1` + `team_mode=single`
     - `WRITE_DELIVERY_TEAM`: `P3`, `P4`, `S3`, 필요 시 `S1` + `team_mode=team`
     - `WRITE_NONE_OPT_OUT`: `NONE` + 명시적 opt-out 경고
  3. Context validation
     - 선택 프로세스 존재
     - `NONE`이 아닌 경우 `selected_wp` 존재
     - Team 가능 프로세스에서 `team_mode=auto` 금지
     - `team_mode=team`이면 최소 역할/멤버 매핑 충족
     - read-only 프로세스에서 writable profile 요청 금지
  4. OMX 보조층
     - `OMX_HOOK_PLUGINS=1` 기반 hook은 `session-start`, `turn-complete` 기록/점검/탐지용으로만 사용
     - hard deny는 wrapper/gateway가 담당
  5. 최종 방어선
     - 기존 `pre-commit`, `pre-push`, `check_ai_ops_compliance.py` 유지
- 비범위:
  - Codex native pre-tool hook 직접 추가
  - OMX upstream 자체 코드 수정
  - 전역 OS readonly 잠금을 기본 운영 모델로 채택
  - 외부 오픈소스 의존성 직접 편입
- 제약사항:
  - tool-call 단위 hard gate parity는 여전히 불가
  - 모든 진입점이 wrapper를 거치지 않으면 우회 가능
  - 프로세스 전환 시 재실행/재진입 UX가 필요하다
- 완료 기준:
  - wrapper/gateway가 검사해야 할 입력/출력/실패 조건이 정의됨
  - launch profile별 허용 프로세스와 거부 조건이 정의됨
  - OMX hook / Git hook / compliance checker의 역할 경계가 정의됨
  - `NONE` 분기와 Team 가능 프로세스의 예외 규칙이 정의됨
  - P3 구현 범위가 파일 단위로 식별됨
- P3 구현 범위:
  - launch wrapper/gateway 스크립트 추가
  - 프로세스 컨텍스트 검증 로직 추가
  - `AGENTS.md`, `docs/ai-ops/commands/ai-ops.md`, `process-enforcement-matrix.md`에 진입 경로 갱신
  - 선택 시 `OMX hooks` 보조 플러그인 스캐폴드 또는 운영 규칙 추가
- 의사결정:
  - `Codex-Wrapper`는 직접 도입하지 않고, launch profile 분리/working-dir/sandbox 강제라는 개념만 참고한다.
  - 주 구현 축은 `OMX-centered wrapper + optional hook telemetry + Git hard gate` 조합으로 둔다.
- 후속 권장 프로세스:
  - `P3`: wrapper/gateway 구현과 문서/규칙 반영

### 9.12 P3 구현 - OMX-centered Launch Gate
- 구현 목표:
  - `P1`에서 정의한 session-entry hard gate를 실제 스크립트와 진입 문서에 반영한다.
- 반영 내용:
  1. launch wrapper/gateway 스크립트 추가
     - `scripts/ai-ops/launch_ai_ops_session.py`
     - 현재 프로세스 컨텍스트를 읽어 `READ_ONLY_ANALYSIS`, `WRITE_DELIVERY_SINGLE`, `WRITE_DELIVERY_TEAM`, `WRITE_NONE_OPT_OUT` 프로필로 분기
     - `team_mode=auto` writable 진입, bypass flag, `danger-full-access`, 잘못된 sandbox 조합을 세션 시작 전에 차단
     - `team_mode=team` 경로에서는 `OMX_TEAM_WORKER_LAUNCH_ARGS`를 `workspace-write` 기준으로 보정
  2. 저장소 진입 문서 갱신
     - `AGENTS.md`에 launch gate 진입 규칙 추가
     - `docs/ai-ops/commands/ai-ops.md`에 Codex+OMX launch gate 사용법 추가
     - `docs/ai-ops/tool-hooks/process-enforcement-matrix.md`에 session-entry hard gate 추가
     - `docs/ai-ops/tool-hooks/codex-jetbrains-ai-assistant-rules.md`에 launch gate와 session-entry hard gate chain 반영
  3. 로컬 runtime 보강
     - `.codex/jetbrains-ai-assistant-rules.md`에도 동일한 launch gate 문구를 반영
     - 로컬 runtime 파일이라 커밋 대상은 아니다
- 검증 결과:
  - `WRITE_DELIVERY_SINGLE` dry-run:
    - `omx --model gpt-5 --sandbox workspace-write`
  - `READ_ONLY_ANALYSIS` dry-run:
    - `omx --model gpt-5 --sandbox read-only`
  - `WRITE_NONE_OPT_OUT` dry-run:
    - 기본: `read-only`
    - `--allow-none-write`: `workspace-write`
  - `WRITE_DELIVERY_TEAM` dry-run:
    - `omx team 3:executor task`
    - `OMX_TEAM_WORKER_LAUNCH_ARGS=--sandbox workspace-write`
- 한계:
  - 이 구현은 session-entry hard gate이며, Claude `PreToolUse`와 같은 tool-call 단위 hard deny를 재현하지는 않는다.
  - 기존 세션 안에서 우회 진입한 경우까지 물리적으로 되돌리지는 못한다.
- 후속 권장 프로세스:
  - `S1`: launch gate가 설계 의도와 맞는지 리뷰하고, 실제 사용 시나리오 기준 누락/우회 가능성을 점검

### 9.13 S1 리뷰 결과 - Launch Gate
- 리뷰 대상:
  - `P3` 커밋 `2285144`
  - `scripts/ai-ops/launch_ai_ops_session.py`
  - `AGENTS.md`, `docs/ai-ops/commands/ai-ops.md`, `docs/ai-ops/tool-hooks/process-enforcement-matrix.md`, `docs/ai-ops/tool-hooks/codex-jetbrains-ai-assistant-rules.md`
- 검토 결과:
  - `launch_ai_ops_session.py`는 설계한 4개 프로필(`READ_ONLY_ANALYSIS`, `WRITE_DELIVERY_SINGLE`, `WRITE_DELIVERY_TEAM`, `WRITE_NONE_OPT_OUT`)을 반영했다.
  - `P3 + single` dry-run에서 `workspace-write`가 기본 적용되는 것을 확인했다.
  - `P0` read-only 프로필에서 `--full-auto`가 차단되는 것을 확인했다.
  - `P3 + team_mode=auto` 상태에서는 writable 진입이 차단되는 것을 확인했다.
  - `P3 + team` dry-run에서 `OMX_TEAM_WORKER_LAUNCH_ARGS=--sandbox workspace-write`가 주입되는 것을 확인했다.
- 승인 판단:
  - **승인(Approve)**. 현재 `P3` 산출물은 `P1` 설계 의도와 완료 기준에 대체로 부합한다.
- 잔여 리스크:
  - launch gate는 session-entry hard gate이며, Claude `PreToolUse`와 같은 tool-call parity는 제공하지 않는다.
  - 사용자가 wrapper를 거치지 않고 직접 `omx`/`codex`를 실행하면 우회 가능성이 남는다.
  - 로컬 `.codex` runtime 파일 갱신은 비커밋 상태이므로, 원격 추적 자산은 아니다.
- 후속 권장 프로세스:
  - `S4`: launch gate 구현/승인 결과와 잔여 리스크를 변경 이력으로 고정

### 9.14 S4 변경 이력 / 의사결정 고정 - Launch Gate Round
- 현재 라운드 체인:
  - `P0(보강) -> P2 -> P1 -> P3 -> S1 -> S4`
- 이번 라운드의 핵심 결과:
  - `Codex+OMX` 경로에 session-entry hard gate를 구현했다.
  - hard gate의 주축은 `OMX-centered process-aware launch wrapper / gateway`이며, `OMX hooks`는 보조 telemetry 계층으로 정리했다.
  - `Codex+OMX`에서 먼저 정립한 얇은 어댑터 + `docs/ai-ops` SoT 중심 구조를 추후 `Claude+OMC` 개편에도 동일 적용하기로 했다.
- 구현/검증 결과 요약:
  - `launch_ai_ops_session.py`가 `READ_ONLY_ANALYSIS`, `WRITE_DELIVERY_SINGLE`, `WRITE_DELIVERY_TEAM`, `WRITE_NONE_OPT_OUT` 프로필을 강제한다.
  - read-only 프로세스에서 `--full-auto`가 차단된다.
  - `team_mode=auto`인 Team 가능 프로세스는 writable 세션 진입이 차단된다.
  - Team 경로에서는 `OMX_TEAM_WORKER_LAUNCH_ARGS=--sandbox workspace-write`가 주입된다.
- 선택한 방식과 이유:
  - 선택: launch gate + 문서 가드 + compliance gate의 다층 구조
  - 이유: 현재 Codex 표면에서 tool-call hard gate parity는 불가능하지만, session-entry 시점 하드 게이트는 구현 가능하기 때문이다.
- 선택하지 않은 대안:
  - `OMX hooks` 단독 hard gate
    - 이유: plugin contract가 leader 실행 deny를 제공하지 않음
  - OS readonly 잠금 기본 운영화
    - 이유: 물리적으로 강하지만 운영 비용이 높고 범용 흐름에 brittle함
  - 외부 wrapper 프로젝트 직접 의존
    - 이유: 소규모 외부 프로젝트에 묶이지 않고 OMX 중심으로 흡수하는 편이 일관적임
- 잔여 리스크 / TODO:
  - wrapper를 거치지 않는 직접 `omx`/`codex` 실행 우회 가능성
  - Claude `PreToolUse` 같은 tool-call hard gate parity 부재
  - launch gate를 실제 파일럿 작업에서 사용했을 때의 유도력과 UX 검증 필요
- 다음 라운드 입력:
  - WP-008의 다음 실무는 launch gate를 포함한 파일럿 검증 재진입(`S1`)이다.
  - 이후 필요 시 `S4`에서 임시 프로세스 sunset/상시화 판정을 이어서 기록한다.

### 9.15 P1 요구사항 구체화 - Codex Entrypoint Parity
- 문제 정의:
  - 현재 `Codex+OMX` 경로는 launch gate와 문서 가드는 갖췄지만, `Claude`의 `/ai-ops`에 대응하는 명시적 named entrypoint가 없다.
  - 따라서 지금 상태로 파일럿을 돌리면 `WP-006`과 동등한 검증이라고 보기 어렵다.
- 목표:
  - exact `/ai-ops` 문법 복제 대신, Codex+OMX 표면에 맞는 **명시적 entrypoint parity**를 정의한다.
- 대안 비교:
  1. OMX project skill `$ai-ops`
     - 장점:
       - OMX의 기본 workflow surface와 맞는다.
       - named entrypoint가 분명하고 파일럿 기록 시 “같은 종류의 진입”으로 설명 가능하다.
       - skill body를 얇게 두고 `docs/ai-ops/*` SoT를 참조하게 할 수 있어 thin-adapter 원칙과 맞다.
     - 한계:
       - `/ai-ops` exact syntax는 아니다.
  2. Codex prompt surface(`/prompts:ai-ops`)
     - 장점: 이름 있는 진입점은 된다.
     - 한계: prompt는 역할/문체 표면에 가깝고, 프로세스 선택/상태기록/후속 제안 같은 workflow 표면으로는 덜 적합하다.
  3. Shell alias / launcher script
     - 장점: 구현은 쉽다.
     - 한계: 사용자 UX가 Codex 내부 진입점보다 약하고, named workflow surface로서의 일관성이 떨어진다.
  4. raw prompt만 사용
     - 장점: 추가 구현 없음
     - 한계: 명시적 entrypoint parity가 없으므로 이번 요구를 충족하지 못한다.
- 선택:
  - **1순위: OMX project skill `$ai-ops`**
- 선택 이유:
  - `Codex+OMX` 표면에서 가장 자연스러운 named workflow entrypoint다.
  - thin-adapter + SoT 원칙을 유지한 채 `Claude /ai-ops`와 기능 등가에 가장 가깝다.
  - launch gate(`launch_ai_ops_session.py`)와 결합하면 entrypoint parity + session-entry hard gate를 함께 가져갈 수 있다.
- 비범위:
  - `Claude`와 완전히 동일한 slash command 문법 복제
  - 외부 오픈소스 의존성 직접 편입
- P3 구현 범위:
  - project skill `.agents/skills/ai-ops/SKILL.md` 추가
  - 필요 시 `agents/openai.yaml` 메타데이터 추가
  - skill 본문은 얇게 유지하고 SoT 문서(`docs/ai-ops/commands/ai-ops.md`, process catalog, matrix)를 참조
  - `AGENTS.md`, `.codex/README.md`, 관련 문서에 `$ai-ops` entrypoint 사용법 반영
- 후속 권장 프로세스:
  - `P3`: `$ai-ops` skill과 관련 진입 문서 반영

### 9.16 P3 구현 - `$ai-ops` Entrypoint Parity
- 구현 목표:
  - `Codex+OMX`에서 `Claude /ai-ops`에 대응하는 명시적 named entrypoint를 추가한다.
- 반영 내용:
  1. project skill 추가
     - `.agents/skills/ai-ops/SKILL.md`
     - 역할: named entrypoint parity
     - 원칙: skill 본문은 얇게 유지하고 `docs/ai-ops/*`, `scripts/ai-ops/*`를 SoT로 참조
  2. 저장소 진입 문서 갱신
     - `AGENTS.md`에 `/ai-ops` vs `$ai-ops` parity 명시
     - `docs/ai-ops/commands/ai-ops.md`에 Codex+OMX named entrypoint parity 설명 추가
     - `docs/ai-ops/tool-hooks/process-enforcement-matrix.md`에 `$ai-ops`를 Codex 공통 진입점에 포함
     - `docs/ai-ops/tool-hooks/codex-jetbrains-ai-assistant-rules.md`에 `$ai-ops` entrypoint 반영
- 구현 결과:
  - Codex+OMX는 exact slash command 복제 대신, OMX workflow surface에 맞는 `$ai-ops`를 공식 parity entrypoint로 갖게 된다.
  - launch gate와 결합하면 “named entrypoint + session-entry hard gate” 구조가 된다.
- 한계:
  - `$ai-ops`는 `/ai-ops`와 문법은 다르다.
  - 실제 skill 로딩/노출은 OMX runtime이 `.agents/skills/`를 읽는 흐름에 의존한다.
- 후속 권장 프로세스:
  - `S1`: `$ai-ops`가 named entrypoint parity로 충분한지와 실제 사용성을 리뷰

### 9.17 S1 리뷰 결과 - `$ai-ops` Entrypoint Parity
- 리뷰 대상:
  - `P3` 커밋 `eccea3d`
  - `.agents/skills/ai-ops/SKILL.md`
  - `.agents/skills/ai-ops/agents/openai.yaml`
  - `AGENTS.md`, `docs/ai-ops/commands/ai-ops.md`, `docs/ai-ops/tool-hooks/process-enforcement-matrix.md`, `docs/ai-ops/tool-hooks/codex-jetbrains-ai-assistant-rules.md`
- 검토 결과:
  - `$ai-ops`는 `Codex+OMX`에서 이름 있는 공식 workflow entrypoint로 기능한다.
  - skill 본문은 얇은 어댑터로 유지되고, `docs/ai-ops/*`, `scripts/ai-ops/*`를 SoT로 참조한다.
  - `AGENTS.md`, command 문서, Codex 규칙, 강제 매트릭스가 모두 `$ai-ops` parity를 일관되게 반영한다.
  - 따라서 launch gate만 있는 상태보다 `WP-006`과 비교 가능한 “명시적 entrypoint + workflow 진입” 구조에 더 가까워졌다.
- 승인 판단:
  - **승인(Approve)**. `$ai-ops`는 현재 `Codex+OMX` 표면에서 합리적인 entrypoint parity로 인정 가능하다.
- 잔여 리스크:
  - `/ai-ops`와 `$ai-ops`는 문법이 다르므로 완전한 UI 동일성은 아니다.
  - 실제 skill discoverability/사용 습관은 파일럿에서 한 번 더 확인해야 한다.
- 후속 권장 프로세스:
  - `S4`: entrypoint parity 구현/승인 결과를 기록으로 고정하고, 이후 실제 pilot #1로 재진입

### 9.18 S4 변경 이력 / 의사결정 고정 - Entrypoint Parity Round
- 현재 라운드 체인:
  - `P1(entrypoint parity) -> P3($ai-ops skill 구현) -> S1(parity 승인) -> S4`
- 이번 라운드의 핵심 결과:
  - `Codex+OMX`는 이제 launch gate만 있는 상태가 아니라, 명시적 named workflow entrypoint `$ai-ops`를 갖는다.
  - `$ai-ops`는 `/ai-ops` exact syntax 복제가 아니라, `Codex+OMX` 표면에 맞는 parity entrypoint로 정의되었다.
  - skill 본문은 얇은 어댑터로 유지하고 `docs/ai-ops/*`, `scripts/ai-ops/*` SoT를 참조하게 했다.
- 선택한 방식과 이유:
  - 선택: OMX project skill `$ai-ops`
  - 이유:
    - `Codex+OMX` 표면에서 가장 자연스러운 named workflow surface이기 때문
    - thin-adapter + SoT 구조를 유지하면서도 `Claude /ai-ops`와 기능 등가에 가장 가깝기 때문
    - launch gate와 결합해 “명시적 진입점 + session-entry hard gate” 조합을 만들 수 있기 때문
- 선택하지 않은 대안:
  - exact slash command 복제
    - 이유: Codex 표면과 맞지 않고 구현 가능성이 낮음
  - raw prompt만 사용
    - 이유: named entrypoint parity 요구를 충족하지 못함
  - shell alias 중심 접근
    - 이유: 사용자 체감/가시성이 skill surface보다 약함
- 잔여 리스크 / TODO:
  - `/ai-ops`와 `$ai-ops`는 문법이 달라 UI 완전 동일성은 없다.
  - 실제 pilot #1에서 skill discoverability와 사용자 체감을 검증해야 한다.
  - launch gate와 `$ai-ops`를 함께 사용한 실제 작업 흐름에서 누락이 없는지 추가 확인이 필요하다.
- 다음 라운드 입력:
  - 이제 WP-008은 실제 pilot #1로 재진입할 조건을 갖췄다.
  - 다음 실무는 실제 작업 하나를 `$ai-ops`로 시작해 pilot #1 증빙을 남기는 것이다.

### 9.19 P0 재진입 - Ad-hoc 산출물의 소급 프로세스 복원 분석
- 분석 목적:
  - AI Ops 프로세스 선택 이전 또는 프로세스 준수 없이 생성된 산출물을, 어떤 근거와 한계 안에서 추적 가능한 기록으로 복원할 수 있는지 판단한다.
- 분석 대상:
  - `WP-AIOPS-2026-03-008` 최근 라운드 산출물
  - 현재 Git working tree / index 상태
  - `docs/ai-ops/CHANGELOG.md`, `work-packets/index.md`, 최근 커밋 이력
  - `.omc/ai-ops-process-context.json` 컨텍스트 상태
- 현재 관측:
  1. 현재 Git index에는 staged 변경이 없다.
     - 사용자는 "현재 staged된 변경사항"을 언급했으나, 현 시점 기준 recoverable staged diff는 비어 있다.
  2. 저장소 기준의 남은 작업 트리 변화는 매우 제한적이다.
     - tracked diff: `.agents/skills/ai-ops/SKILL.md`의 description quoting 변경 1건
     - untracked diff: `.omx/*` runtime 산출물 다수
  3. `.omx/*`는 Local Runtime 산출물이므로 공식 증빙/커밋 대상이 아니다.
     - AI Ops 정책상 `.codex/.omx/.omc`는 원격 추적용 산출물이 아니라 local-only 실행 영역이다.
  4. 반면, 공식적으로 복원 가능한 근거는 이미 존재한다.
     - WP 기록: `WP-AIOPS-2026-03-008`의 `9.15 ~ 9.18`
     - 통합 변경이력: `docs/ai-ops/CHANGELOG.md`의 2026-03-09 WP-008 parity round 기록
     - 관련 커밋: `eccea3d`, `d4fe1c6`, `0b686ac`
     - 현재 프로세스 컨텍스트: `.omc/ai-ops-process-context.json`
- 주요 구성요소 맵:
  - authoritative trace:
    - `docs/ai-ops/work-packets/WP-AIOPS-2026-03-008-codex-omx-alignment.md`
    - `docs/ai-ops/work-packets/index.md`
    - `docs/ai-ops/CHANGELOG.md`
  - supplementary evidence:
    - `git log`
    - `.omc/ai-ops-process-context.json`
  - non-authoritative / local-only evidence:
    - `.omx/*`
    - `.codex/*`
    - 기타 세션 런타임 산출물
- 현재 동작 요약:
  - 이 작업에서 실제로 복원 가능한 것은 "원래 ad-hoc하게 생성된 산출물 전체"가 아니라, 이미 남아 있는 공식 문서/커밋/컨텍스트를 기준으로 한 사후 재구성 기록이다.
  - 즉, 지금부터 만들 수 있는 것은 "처음부터 프로세스를 완벽히 준수한 척하는 이력"이 아니라, "사후 복원(post-hoc reconstruction)" 이력이다.
- 진입점 / 흐름 / 의존성 정리:
  - 현재 합리적인 복원 흐름은 다음과 같다.
    - `P0`: recoverable 범위와 공식 증빙 경계 분석
    - `P2`: 복원 전략(최소 기록 / 증거 기반 재구성 / local discard) 비교 및 선택
    - `S4`: 선택 전략과 판단 근거를 WP/CHANGELOG에 고정
    - `S1`: 기록의 정직성, 누락, 과장 여부 리뷰
- 관련 문서 / 테스트 현황:
  - 관련 문서:
    - `docs/ai-ops/commands/ai-ops.md`
    - `docs/ai-ops/process-catalog/P0-P4-core-processes.md`
    - `docs/ai-ops/process-catalog/S1-S4-support-processes.md`
    - `docs/ai-ops/tool-hooks/process-enforcement-matrix.md`
    - `docs/ai-ops/work-packets/index.md`
    - `docs/ai-ops/CHANGELOG.md`
  - 관련 테스트:
    - 현재 요청은 제품 기능 테스트가 아니라 기록 복원/운영 추적성 분석이므로 코드 테스트 대상은 없다.
    - 대신 `git status`, `git log`, process context, existing WP/CHANGELOG consistency가 핵심 검증 입력이다.
- 위험 포인트:
  1. 현재 시점에서는 원래의 staged mutation sequence를 Git만으로 복원할 수 없다.
  2. local runtime 산출물을 공식 근거처럼 취급하면 AI tool artifact boundary 원칙을 위반한다.
  3. 사후 복원을 "원래부터 프로세스를 준수한 실행"처럼 과장 기록하면 traceability 품질이 떨어진다.
- 미확정 항목:
  1. `.agents/skills/ai-ops/SKILL.md`의 현재 quoting 변경을 이번 복원 범위에 포함할지 여부
  2. 복원 전략을 최소 기록으로 둘지, evidence-based reconstructed chain으로 확장할지 여부
  3. 이번 라운드를 pilot #1 재진입 전 preparatory 기록으로 볼지, 별도 retroactive recovery round로 고정할지 여부
- 결론:
  - recoverable scope는 "코드/기능 산출물 재현"이 아니라 "문서화 가능한 process trace 복원"이다.
  - 따라서 다음 단계에서는 문제 해결 전략을 고르는 `P2`가 자연스럽다.
- 후속 권장 프로세스:
  - `P2`: 소급 복원 전략 비교 및 우선 방식 선택

### 9.20 P2 트러블슈팅 전략 도출 - Ad-hoc 산출물 소급 복원 방식 선택
- 문제 정의:
  - 사용자가 원하는 것은 이미 ad-hoc하게 실행된 결과물에 대해, AI Ops 프로세스를 준수해 생성된 것에 가까운 추적 가능한 과정을 남기는 것이다.
  - 그러나 현재는 원래 staged mutation sequence가 남아 있지 않고, 공식 근거와 local runtime 산출물의 경계도 분리해야 한다.
- 증상 / 재현 조건:
  1. 현재 Git index에는 복원 가능한 staged diff가 없다.
  2. 남아 있는 워킹트리 변화는 `.agents/skills/ai-ops/SKILL.md` 1건과 `.omx/*` local runtime 파일들이다.
  3. 반면 `WP-AIOPS-2026-03-008`, `docs/ai-ops/CHANGELOG.md`, 최근 커밋 이력에는 실제 라운드의 공식 흔적이 남아 있다.
- 영향 범위:
  - WP-008의 추적성 품질
  - 이후 pilot #1 증빙 신뢰도
  - local-only artifact boundary(`.omx/.codex/.omc`) 준수 여부
- 원인 가설 목록:
  1. 원래 staged 상태는 이미 소실되어, 코드 단위 원본 복원은 불가능하다.
  2. 공식 문서/커밋/컨텍스트만으로는 "무슨 판단이 있었는지"는 복원 가능하다.
  3. `.omx/*`를 증빙에 섞으면 기록이 풍부해 보일 수는 있으나, 근거 신뢰도와 정책 준수성이 오히려 낮아진다.
  4. 현재 남은 `.agents/skills/ai-ops/SKILL.md` quoting diff는 복원 라운드의 본체가 아니라 별도 미정리 변경일 가능성이 높다.
- 확인 방법:
  1. WP / CHANGELOG / commit history가 서로 모순 없이 같은 round를 가리키는지 확인한다.
  2. 현재 process context가 `P2`로 전환되었는지 확인한다.
  3. local-only runtime 산출물을 공식 산출물 경로에 포함하지 않았는지 점검한다.
  4. 복원 기록이 "당시 실시간 준수"가 아니라 "사후 재구성"임을 명시했는지 확인한다.
- 해결안 후보:
  1. 최소 기록 전략
     - 현재 staged diff가 사라졌음을 짧게 남기고 종료한다.
     - 장점: 가장 안전하고 단순함
     - 한계: 사용자가 원하는 "과정 흔적"을 충분히 제공하지 못함
  2. 증거 기반 재구성 전략
     - 공식 문서, 커밋, 컨텍스트를 근거로 실제로 확인 가능한 범위까지만 process trace를 복원한다.
     - 장점: traceability와 정직성을 함께 지킬 수 있음
     - 한계: 원래 실시간 실행 로그 수준의 디테일은 복원 불가
  3. local artifact 보강 전략
     - `.omx/*` 같은 런타임 파일을 참고해 더 많은 흔적을 남긴다.
     - 장점: 표면적으로는 정보량이 많아짐
     - 한계: local-only 정책 위반 위험, 근거 신뢰도 불안정
  4. staged 상태 재현 전략
     - 기억/추정에 의존해 원래 staged 상태를 다시 만들어 기록한다.
     - 장점: 겉보기에는 가장 그럴듯함
     - 한계: 사실성과 재현 가능성이 낮아 traceability를 훼손함
- 우선 적용 전략:
  - **2번, 증거 기반 재구성 전략**을 선택한다.
- 선택 이유:
  - 사용자 요구인 "과정 흔적 남기기"를 충족하면서도, AI Ops의 Traceability First 원칙을 가장 덜 훼손한다.
  - `WP`, `CHANGELOG`, `commit`, `process context`라는 authoritative source만 사용하므로 근거 경계가 분명하다.
  - "처음부터 준수한 실행처럼 보이게" 꾸미지 않고, "사후 복원된 process trace"라는 사실을 유지할 수 있다.
- 선택하지 않은 대안:
  - 최소 기록 전략: 너무 빈약해서 후속 세션/리뷰에 도움을 주기 어렵다.
  - local artifact 보강 전략: `.omx/*` local-only 원칙과 충돌한다.
  - staged 상태 재현 전략: 현재 증거 수준에서 과장/오기록 위험이 가장 크다.
- 수정 전에 필요한 추가 관측 / 정리 항목:
  1. 현재 남아 있는 `.agents/skills/ai-ops/SKILL.md` quoting diff를 이번 retro round에 포함할지, 별도 변경으로 분리할지 결정 필요
  2. `.omx/*`는 계속 local-only로 유지하고 커밋 범위에서 제외
- 후속 입력값:
  - `S4`에서 아래를 고정한다.
    - 이번 라운드의 성격: post-hoc reconstruction
    - authoritative evidence 목록
    - 제외한 evidence(local runtime)의 이유
    - 남은 stray working-tree diff 처리 방침
- 후속 권장 프로세스:
  - `S4`: 복원 전략, 선택 이유, 제외 근거를 변경 이력/의사결정으로 고정

### 9.21 S4 변경 이력 / 의사결정 고정 - Retro Recovery Round
- 현재 라운드 체인:
  - `P0(소급 복원 가능 범위 분석) -> P2(복원 전략 선택) -> S4(기록 고정)`
- 이번 라운드의 핵심 결과:
  - ad-hoc하게 실행된 결과물에 대해서는, 이제부터 남기는 기록을 "처음부터 프로세스를 준수한 실행 이력"으로 꾸미지 않고 `post-hoc reconstruction`으로 고정한다.
  - 공식 근거는 `WP`, `CHANGELOG`, `commit`, `process context`에 한정한다.
  - `.omx/*`와 같은 local runtime 산출물은 공식 trace에서 제외한다.
- 관련 커밋:
  - `9533044` - WP-008 P0: ad-hoc 산출물 소급 복원 범위 분석
  - `929b44a` - WP-008 P2: authoritative evidence 기반 복원 전략 선택
- 선택한 방식과 이유:
  - 선택: authoritative evidence 기반 post-hoc reconstruction
  - 이유:
    - 과정 흔적은 남기되, 사실성과 근거 경계를 유지할 수 있기 때문
    - local-only artifact를 섞지 않고도 세션 전환/리뷰에 필요한 수준의 traceability를 확보할 수 있기 때문
- 선택하지 않은 대안:
  - 최소 기록 전략
    - 이유: 정보량이 너무 적어 후속 리뷰와 세션 복원에 도움을 주기 어렵다.
  - local artifact 보강 전략
    - 이유: `.omx/*` local-only 원칙과 충돌한다.
  - staged 상태 재현 전략
    - 이유: 실제 증거보다 추정이 앞서 traceability를 훼손할 가능성이 크다.
- 남은 TODO / 리스크:
  - `.agents/skills/ai-ops/SKILL.md`의 현재 quoting diff를 이번 retro recovery round 범위에 포함할지 별도 변경으로 분리할지 아직 결정되지 않았다.
  - `.omx/*`는 계속 local-only로 유지해야 하며, 공식 커밋/증빙 경로에 포함되면 안 된다.
  - 이 round의 기록이 과장 없이 충분한지, 후속 `S1` 리뷰에서 다시 확인해야 한다.
- 다음 라운드 입력:
  - `S1`에서 아래를 검토한다.
    - retro recovery round 기록이 과장/누락 없이 충분한가
    - stray diff(`.agents/skills/ai-ops/SKILL.md`)를 별도 변경으로 분리하는 게 맞는가
    - 실제 pilot #1 재진입 전에 이 복원 라운드가 더 필요한 보강 없이 승인 가능한가

### 9.22 S1 리뷰 결과 - Retro Recovery Round
- 리뷰 대상:
  - `P0` 커밋 `9533044`
  - `P2` 커밋 `929b44a`
  - `S4` 커밋 `52ee5bf`
  - `WP-AIOPS-2026-03-008`의 `9.19 ~ 9.21`
  - `docs/ai-ops/CHANGELOG.md`, `docs/ai-ops/work-packets/index.md`
- 검토 결과:
  - retro recovery round는 "사후 복원"이라는 성격을 숨기지 않고 명시하고 있다.
  - 공식 근거를 `WP`, `CHANGELOG`, `commit`, `process context`로 제한해 traceability 경계가 분명하다.
  - `.omx/*`를 공식 증빙에서 제외한 판단은 AI tool artifact boundary 원칙과 일치한다.
  - 따라서 이번 라운드는 "처음부터 프로세스를 지킨 척하는 이력"이 아니라, evidence-based reconstruction으로서 충분히 정직하고 재검토 가능하다.
- 승인 판단:
  - **승인(Approve)**
- 누락 / 보완 사항:
  - `.agents/skills/ai-ops/SKILL.md`의 stray diff는 이번 retro recovery round 범위와 직접 연결되지 않으므로 별도 변경으로 분리하는 편이 적절하다.
  - actual pilot #1 재진입 시에는 이 retro round를 참조하되, 새 작업은 다시 명시적 프로세스 선택에서 시작해야 한다.
- 잔여 리스크:
  - 원래 staged mutation sequence 자체는 여전히 복원되지 않으므로, 세부 실행 로그의 완전 재현까지 기대하면 안 된다.
  - 후속 세션에서 `.omx/.omc` local runtime 파일을 다시 공식 근거처럼 오인하지 않도록 주의가 필요하다.
- 후속 권장 프로세스:
  - `P0`: 실제 pilot #1 대상 작업이 정해지면, 그 작업에 대해 새 분석 체인으로 재진입

### 9.23 P1 Codex entrypoint ownership 재정렬
- 배경:
  - `WP-008 P3`에서 Codex parity를 위해 `.codex/jetbrains-ai-assistant-rules.md`와 `$ai-ops` entrypoint를 함께 강화했지만, 사용자 체감상 Claude 경로와 다른 동작과 높은 토큰 비용이 발생했다.
  - 사용자는 JetBrains AI Assistant 일반 경로에서 `$ai-ops`를 더 이상 사용하지 않겠다고 명확히 했고, `.codex/jetbrains-ai-assistant-rules.md`는 전면 제거 대상으로 지정했다.
- 요구사항 정의:
  1. `$ai-ops`는 Codex+OMX 경로 전용 named entrypoint로 유지한다.
  2. JetBrains AI Assistant 일반 경로는 `AGENTS.md`와 `docs/ai-ops/*` SoT를 직접 따른다.
  3. `.codex/jetbrains-ai-assistant-rules.md`에 대한 canonical 정책 의존은 제거하고, P3에서 파일 자체도 제거한다.
  4. `$ai-ops` skill은 active WP(`WP-008` 등)를 직접 참조하지 않는 thin adapter로 축소한다.
  5. Codex SoT에는 사용자 프로세스 선택 전 `omx team ...` 또는 동등 Team 진입 금지 규칙을 직접 명시한다.
- 범위:
  - 원격 관리 문서(`docs/ai-ops/*`)와 ADR/WP/index/changelog/master-plan 동기화
  - P3에서 `.codex/jetbrains-ai-assistant-rules.md` 제거, `$ai-ops` skill 축소, 관련 로컬 어댑터 정리
- 비범위:
  - Claude `/ai-ops` 경로 재설계
  - OMX/OMC 외부 배포본 수정
- 의사결정 근거:
  - ADR-AIOPS-004 기준상 hidden local adapter는 canonical 정책 저장소가 될 수 없다.
  - Claude parity의 본질은 exact syntax 복제가 아니라, 선택 후 Team/기록/검증 흐름의 일관성이다.
  - active WP 직접 참조는 thin adapter 원칙과 토큰 효율을 동시에 훼손한다.
- 제약 및 리스크:
  - JetBrains AI Assistant 일반 경로에서 `AGENTS.md` 유도력이 충분한지 P3/S1에서 다시 확인해야 한다.
  - `.codex/README.md` 등 로컬 보조 자산은 P3 범위에서 함께 정리해야 문서/로컬 동작의 괴리가 남지 않는다.
- 후속 권장 프로세스:
  - `P3`: `.codex/jetbrains-ai-assistant-rules.md` 제거, `$ai-ops` skill 참조 축소, Codex SoT 반영

### 9.24 P3 Codex entrypoint ownership 반영
- 구현 내용:
  - `.codex/jetbrains-ai-assistant-rules.md`를 제거하고, JetBrains AI Assistant 일반 경로의 로컬 rule-pack 의존을 정리했다.
  - `AGENTS.md`에 JetBrains AI Assistant 일반 경로는 `$ai-ops`를 기본 진입점으로 사용하지 않는다는 규칙과, 사용자 선택 전 Team 금지 규칙을 직접 추가했다.
  - `.agents/skills/ai-ops/SKILL.md`에서 `WP-008` 직접 참조를 제거하고, JetBrains AI Assistant 일반 경로에는 사용하지 않는다는 범위를 명시했다.
  - `.codex/README.md`를 `AGENTS.md` + SoT 직접 참조 구조로 단순화했다.
- 기대 효과:
  - `$ai-ops`의 기본 컨텍스트 부하를 줄인다.
  - Codex+OMX 전용 entrypoint와 JetBrains AI Assistant 일반 경로의 소유 경계를 명확히 한다.
  - Codex SoT에도 선택 전 Team 금지 규칙이 직접 드러난다.
- 잔여 검증 포인트:
  - JetBrains AI Assistant 일반 경로가 `AGENTS.md`만으로도 충분히 유도되는지 확인 필요
  - `$ai-ops`가 active WP 직접 참조 없이도 프로세스 진입 품질을 유지하는지 확인 필요
- 후속 권장 프로세스:
  - `S1`: 문서/로컬 어댑터 정렬 결과와 잔여 리스크 검토

### 9.25 S1 리뷰 결과 - Codex entrypoint ownership 반영
- 리뷰 대상:
  - `AGENTS.md`
  - `.agents/skills/ai-ops/SKILL.md`
  - `.codex/README.md`
  - `docs/ai-ops/commands/ai-ops.md`
  - `docs/ai-ops/tool-hooks/process-enforcement-matrix.md`
  - `docs/ai-ops/tool-hooks/codex-jetbrains-ai-assistant-rules.md`
  - `docs/ai-ops/tool-hooks/README.md`
  - `docs/ai-ops/ops-bootstrap-master-plan.md`
  - `docs/ai-ops/work-packets/WP-AIOPS-2026-03-001-ai-ops-bootstrap.md`
  - `docs/ai-ops/work-packets/WP-AIOPS-2026-03-008-codex-omx-alignment.md`
  - `docs/ai-ops/work-packets/index.md`
  - `docs/ai-ops/CHANGELOG.md`
  - `docs/ai-ops/adr/ADR-AIOPS-005-codex-entrypoint-ownership-and-ai-assistant-decoupling.md`
- 검토 결과:
  - `$ai-ops`의 역할이 Codex+OMX 전용으로 다시 좁혀졌고, JetBrains AI Assistant 일반 경로와의 소유 경계가 문서상 일관되게 반영됐다.
  - `WP-008` 직접 참조 제거와 선택 전 Team 금지 규칙이 SoT/adapter 문서에 모두 반영됐다.
  - working tree 기준 `check_ai_ops_compliance.py --mode working_tree`는 통과했다.
- 승인 판단:
  - **승인(Approve)**
- 잔여 리스크:
  - JetBrains AI Assistant 일반 경로에서 `AGENTS.md` 단독 유도력이 충분한지는 실제 사용 과정에서 한 번 더 확인이 필요하다.
  - `.codex/`는 local-only 영역이므로, 사용자 로컬 환경에서 남은 캐시/보조 파일은 별도 정리가 필요할 수 있다.
- 후속 권장 프로세스:
  - `S4`: 이번 라운드의 변경 이력과 승인 판단을 기록으로 고정

### 9.26 S4 변경 이력 고정 - Codex entrypoint ownership round
- 기록 대상:
  - P1 Codex entrypoint ownership 재정렬
  - P3 Codex entrypoint ownership 반영
  - S1 승인 결과
- 고정한 핵심 판단:
  - `$ai-ops`는 Codex+OMX 전용 named entrypoint로 유지한다.
  - JetBrains AI Assistant 일반 경로는 `$ai-ops`를 사용하지 않고 `AGENTS.md` + SoT를 직접 따른다.
  - `.codex/jetbrains-ai-assistant-rules.md`는 제거하고, hidden local rule-pack을 canonical 정책 경로로 쓰지 않는다.
  - Codex SoT에 사용자 선택 전 Team 금지 규칙을 직접 반영한다.
- 산출물:
  - `AGENTS.md`
  - `.agents/skills/ai-ops/SKILL.md`
  - `.codex/README.md`
  - `docs/ai-ops/adr/ADR-AIOPS-005-codex-entrypoint-ownership-and-ai-assistant-decoupling.md`
  - `docs/ai-ops/commands/ai-ops.md`
  - `docs/ai-ops/tool-hooks/process-enforcement-matrix.md`
  - `docs/ai-ops/tool-hooks/codex-jetbrains-ai-assistant-rules.md`
  - `docs/ai-ops/tool-hooks/README.md`
  - `docs/ai-ops/ops-bootstrap-master-plan.md`
  - `docs/ai-ops/work-packets/WP-AIOPS-2026-03-001-ai-ops-bootstrap.md`
  - `docs/ai-ops/work-packets/WP-AIOPS-2026-03-008-codex-omx-alignment.md`
  - `docs/ai-ops/work-packets/index.md`
  - `docs/ai-ops/CHANGELOG.md`
- 잔여 TODO:
  - 실제 JetBrains AI Assistant 사용 흐름에서 `AGENTS.md` 유도력 점검
  - 필요 시 후속 pilot/P0에서 실제 사용 체감 재확인
- 후속 권장 프로세스:
  - `P0`: 후속 사용 흐름 또는 새 요구가 정해지면 그 범위로 재진입

## 10. Deliverables
- Codex+OMX 정렬 정책 문서
- P0 현재 구조 / Gap 분석 기록
- P2 hard guarantee 우회 전략 비교 및 우선 전략
- P2 ad-hoc 산출물 소급 복원 전략 비교 및 우선 전략
- S4 retro recovery round 기록
- S1 retro recovery round 리뷰 결과
- P1 OMX-centered hard gate 요구사항 정의
- P3 OMX-centered launch gate 구현
- S1 launch gate 리뷰 결과
- S4 launch gate round 기록
- P1 Codex entrypoint parity 요구사항 정의
- P3 `$ai-ops` entrypoint parity 구현
- S1 `$ai-ops` parity 리뷰 결과
- S4 `$ai-ops` parity round 기록
- 파일럿 #1/#2 기록
- 임시 프로세스 sunset 판정 기록

## 11. Review Notes
- Codex/Claude 도구 간 차이로 동일 규칙의 실행 표면을 분리해 기록할 필요가 있다.
- `P3` 산출물은 승인 가능하지만, soft guarantee의 실제 유도력은 파일럿 검증이 필요하다.
- 프로세스 코드(`P0`, `P1`, `S1`)의 가독성 개선 여부는 별도 후속 검토 주제로 유지한다.
- 이번 라운드는 `P0 -> P1 -> P3 -> S1 -> S4`까지 닫았지만, WP 전체 완료는 파일럿 검증 전이므로 `DONE`으로 전이하지 않는다.
- hard guarantee는 현재 Codex+OMX 지원 표면만으로는 미달성이므로, 별도 전략 단계가 필요하다.
- 현재 P2 판단상 session-entry hard gate는 가능성이 있으나, tool-call 단위 hard gate parity는 여전히 native hook 부재에 묶인다.
- 현재 P1 판단상 외부 OSS는 개념 참고만 하고, 저장소 구현은 `OMX-centered wrapper + hook telemetry + Git gate`로 수렴한다.
- 현재 P3 구현은 새 세션 진입 hard gate까지 반영했지만, tool-call parity는 여전히 후속 과제로 남아 있다.
- 현재 S1 판단상 구현은 승인 가능하나, wrapper 미사용 우회 가능성과 tool-call parity 부재는 명시적으로 남겨야 한다.
- 현재 S4 판단상 이번 라운드의 설계/구현/리뷰 결과는 기록 완료 상태이며, 남은 과제는 실제 파일럿 적용 검증이다.
- 현재 P1 판단상 파일럿 재진입 전 `$ai-ops` 같은 named entrypoint parity를 먼저 추가해야 한다.
- 현재 P3 판단상 named entrypoint parity는 구현됐고, 남은 건 실제 런타임 체감/파일럿 적합성 리뷰다.
- 현재 S1 판단상 `$ai-ops` parity는 승인 가능하나, 실제 pilot #1에서 discoverability와 사용자 체감은 한 번 더 검증해야 한다.
- 현재 S4 판단상 entrypoint parity round는 기록까지 완료되었고, 다음은 실제 pilot #1 검증이다.
- 현재 S1 판단상 retro recovery round는 승인 가능하며, stray diff는 별도 변경으로 분리하는 편이 적절하다.

## 12. Decisions
| 결정 | 선택 | 이유 |
|------|------|------|
| 전환 방식 | 임시 프로세스(2회 한정) | 무중단 전환 + 운영 리스크 최소화 |
| 기준 참조 | Claude+OMC 성공패턴 우선 | 검증된 운영 패턴 재사용 |
| 정책 소유 | docs/ai-ops를 SoT로 유지 | 런타임 템플릿 overwrite 리스크 완화 |
| 현재 우선순위 | Codex+OMX 완성 우선 | G6 완료 전 제품화/어댑터 개편을 병행하면 초점이 분산됨 |
| 제품화 전략 시점 | 후순위 보류 | marker block/sync/installer/marketplace 전략은 추후 성숙도 상승 후 검토 |
| Codex 정렬 방식 | `AGENTS.md` 얇은 어댑터 + `docs/ai-ops` SoT | generic OMX 런타임과 프로젝트 운영 규칙의 경계를 분리하기 위함 |
| 로컬 디렉토리 취급 | `.codex/.omx/.omc`는 Local Runtime | 정책 본문 저장소로 쓰지 않고 drift 리스크를 낮추기 위함 |
| 이번 WP 범위 제한 | `CLAUDE.md` 개편은 제외 | Codex+OMX 완성 우선, Claude 경로 개편은 후속 과제로 분리 |
| 문서 기술 방식 | capability-first | 도구 고유 기능/명령 변경 주기가 짧아도 운영 규칙이 빨리 낡지 않게 하기 위함 |
| 프로세스 종료 규칙 | 커밋 여부 질의 필수 | 단계 종료 후 워킹트리 혼합을 줄이고 프로세스 단위 이력을 보존하기 위함 |
| Hard Guarantee 판정 | 현재 Codex+OMX 지원 표면만으로는 불가 | 네이티브 pre-tool deny point가 없고 OMX hook/plugin 표면이 차단 contract를 제공하지 않기 때문 |
| Hard Guarantee 우선 전략 | OMX-centered process-aware launch wrapper / gateway | 현재 지원 표면 안에서 session-entry 시점 hard gate를 만들 수 있고, OMX launch/hook surface를 보조층으로 활용할 수 있기 때문 |
| 외부 오픈소스 활용 방식 | 개념 참고만 사용 | 소규모 wrapper 프로젝트 의존성 없이 저장소/OMX 기준 설계로 가져가기 위함 |
| Claude 경로 후속 정렬 방향 | 동일한 얇은 어댑터 + SoT 중심 구조 | Codex+OMX에서 먼저 정립한 원칙을 추후 Claude+OMC 경로에도 동일 적용하기 위함 |
| Ad-hoc 산출물 복원 방식 | authoritative evidence 기반 post-hoc reconstruction | 과정 흔적은 남기되, local-only artifact나 추정 복원으로 traceability를 훼손하지 않기 위함 |

## 13. Follow-ups
- 장기 방향 메모는 유지하되, `CLAUDE.md` 개편 및 제품화 전략은 별도 후속 WP/Track 후보로 분리 검토한다.
- 파일럿에서 Codex 경로의 soft guarantee 유도력과 `NONE` 분기 증빙 형식을 검증한다.
- 프로세스 코드의 명시적 라벨/alias 체계 필요 여부를 별도 후속 과제로 검토한다.
- 파일럿 종료 후 상시화 여부를 ADR 또는 WP 갱신으로 확정
- 필요 시 `process-enforcement-matrix.md`에 Codex+OMX 전용 기준 확장
- `P3`에서 wrapper/gateway 기반 hard gate의 스크립트/진입 규칙/보조 hook을 실제 반영한다.
- `S1`에서 launch gate 스크립트와 문서 반영의 정합성, 우회 가능성, 실제 사용성을 리뷰한다.
- `S4`에서 launch gate 승인 결과, 잔여 우회 리스크, 추후 Claude+OMC 적용 방향을 기록으로 고정한다.
- 파일럿 재진입 시 launch gate 사용성을 실제 작업 흐름에서 검증하고, 임시 프로세스 sunset/상시화 판단 입력으로 삼는다.
- `P3`에서 `$ai-ops` skill을 구현하고 named entrypoint parity를 확보한 뒤 파일럿으로 재진입한다.
- `S1`에서 `$ai-ops`가 WP-006과 동등한 파일럿 진입점으로 인정 가능한지 검토한다.
- `S4`에서 `$ai-ops` parity 승인 결과를 고정하고, 이후 실제 pilot #1 대상으로 재진입한다.
- `Codex+OMX`에서 먼저 정립한 얇은 어댑터 + `docs/ai-ops` SoT 원칙은 후속 시점에 `Claude+OMC` 경로에도 동일하게 적용한다.
- 실제 pilot #1에서는 `$ai-ops` 진입, 프로세스 선택, launch gate, 종료 보고가 한 흐름으로 작동하는지 확인한다.
- retro recovery round에서는 `.agents/skills/ai-ops/SKILL.md` stray diff를 별도 변경으로 분리할지 판단하고, `.omx/*`는 계속 local-only로 유지한다.

## 14. Timeline
- [2026-03-08] WP 생성 (READY)
- [2026-03-08] 임시 프로세스(2회 한정) 정의
- [2026-03-08] `P0` 선택 및 컨텍스트 기록: `python3 scripts/ai-ops/set_process_context.py --process P0 --wp WP-AIOPS-2026-03-008 --team-mode auto`
- [2026-03-08] `P0` 분석 완료: Codex+OMX vs Claude+OMC 구조/강제 지점/gap 정리, 후속 권장 프로세스 `P1`
- [2026-03-08] 장기 방향 메모 기록: `Codex+OMX` 완성 우선, `CLAUDE.md` 개편/제품화 전략은 후순위로 보류
- [2026-03-08] `P1` 선택 및 컨텍스트 기록: `python3 scripts/ai-ops/set_process_context.py --process P1 --wp WP-AIOPS-2026-03-008 --team-mode auto`
- [2026-03-08] `P1` 설계 완료: Codex+OMX 목표 운영 구조, 임시 가드 증빙 형식, P3 구현 범위 확정
- [2026-03-08] `P1` 설계 보강: 도구 고유 기능명이 아닌 capability-first 문구로 정리
- [2026-03-08] `P3` 선택 및 컨텍스트 기록: `python3 scripts/ai-ops/set_process_context.py --process P3 --wp WP-AIOPS-2026-03-008 --team-mode auto`
- [2026-03-08] `P3` 실행 경로 확정: `python3 scripts/ai-ops/set_process_context.py --process P3 --wp WP-AIOPS-2026-03-008 --team-mode single`
- [2026-03-08] `P3` 구현: Codex+OMX soft guarantee를 위한 adapter 오버레이, single fallback logical role 유지, capability-first Codex 문서 보강
- [2026-03-08] 프로세스 종료 규칙 보강: 다음 프로세스 전이 전 커밋 여부 질의 필수
- [2026-03-08] `S1` 리뷰 완료: P3 승인, 문서 불일치 2건 보정, 후속 프로세스 `S4`
- [2026-03-08] `S4` 기록 완료: 현재 라운드 변경/의사결정/관련 커밋/남은 TODO 고정, 다음 프로세스 `S1`
- [2026-03-08] 새 요구 반영: 기존 soft guarantee baseline이 목표에 미달함을 확인하고 WP-008을 `P0` 분석 단계로 재개
- [2026-03-08] `P0` 보강: P0는 team-capable 프로세스가 아니며, `P3/P4/S3/(조건부 S1)`만 toolchain capability가 있을 때 `OMX` team 경로를 활용함을 명시
- [2026-03-08] `P0` 보강: 현재 Codex+OMX 지원 표면만으로는 Claude급 runtime hard guarantee 불가 판정, 후속 권장 프로세스 `P2`
- [2026-03-08] `P2` 수행: hard guarantee 우회 전략 비교 결과, Process-aware launch wrapper / gateway를 1순위 전략으로 선택
- [2026-03-08] `P2` 종료 판단: 다음 프로세스를 `P1`로 전환해 wrapper/gateway 요구사항을 구체화
- [2026-03-08] `P1` 수행: 소규모 외부 OSS는 개념 참고만 하고, `OMX-centered wrapper + hook telemetry + Git gate` 조합으로 구현 요구사항을 구체화
- [2026-03-08] `P3` 수행: `launch_ai_ops_session.py` 추가, `AGENTS.md`/명령문서/Codex 규칙/강제 매트릭스에 session-entry hard gate 반영, 로컬 `.codex` runtime 규칙 보강
- [2026-03-08] `S1` 리뷰 완료: launch gate 구현 승인, 우회 가능성/Parity 한계를 잔여 리스크로 기록, 후속 프로세스 `S4`
- [2026-03-08] `S4` 기록 완료: hard gate round의 체인/의사결정/잔여 리스크/Claude+OMC 후속 정렬 방향을 기록으로 고정, 다음 프로세스 `S1`
- [2026-03-09] entrypoint parity 요구 추가: launch gate만으로는 WP-006과 동등한 파일럿으로 보기 어렵다고 판단, `P1`로 재진입
- [2026-03-09] `P1` 설계: `Codex+OMX` 표면의 명시적 entrypoint parity는 OMX project skill `$ai-ops`로 가는 방향을 선택
- [2026-03-09] `P3` 수행: `.agents/skills/ai-ops/SKILL.md` 추가, `$ai-ops` parity와 관련 진입 문서 반영
- [2026-03-09] `S1` 리뷰 완료: `$ai-ops`를 named entrypoint parity로 승인, 후속 프로세스 `S4`
- [2026-03-09] `S4` 기록 완료: `$ai-ops` parity round의 체인/결정/잔여 리스크를 고정하고, 실제 pilot #1 재진입 조건 충족으로 정리
- [2026-03-09] 사용자 요청으로 WP-008을 `P0`에 재진입: ad-hoc 산출물의 소급 프로세스 복원 가능 범위를 분석하기 위해 컨텍스트를 `P0`로 재설정
- [2026-03-09] `P0` 분석 결과: recoverable staged diff는 비어 있고, 공식 복원 근거는 WP/CHANGELOG/commit/context에 한정되며 `.omx/*`는 local-only runtime 산출물로 분리해야 함을 확인, 후속 권장 프로세스 `P2`
- [2026-03-09] `P2` 선택 및 컨텍스트 기록: `python3 scripts/ai-ops/set_process_context.py --process P2 --wp WP-AIOPS-2026-03-008 --team-mode auto`
- [2026-03-09] `P2` 전략 선택: ad-hoc 산출물 소급 복원은 authoritative evidence만 사용하는 증거 기반 재구성 전략을 채택, 후속 권장 프로세스 `S4`
- [2026-03-09] `S4` 선택 및 컨텍스트 기록: `python3 scripts/ai-ops/set_process_context.py --process S4 --wp WP-AIOPS-2026-03-008 --team-mode auto`
- [2026-03-09] `S4` 기록 고정: retro recovery round를 authoritative evidence 기반 post-hoc reconstruction으로 확정, 후속 권장 프로세스 `S1`
- [2026-03-09] `S1` 선택 및 컨텍스트 기록: `python3 scripts/ai-ops/set_process_context.py --process S1 --wp WP-AIOPS-2026-03-008 --team-mode single`
- [2026-03-09] `S1` 리뷰 완료: retro recovery round를 승인하고, stray diff는 별도 변경으로 분리 권장, 후속 권장 프로세스 `P0`
- [2026-03-09] `P1` 선택 및 컨텍스트 기록: `python3 scripts/ai-ops/set_process_context.py --process P1 --wp WP-AIOPS-2026-03-008 --team-mode auto`
- [2026-03-09] `P1` 설계: JetBrains AI Assistant 일반 경로는 `$ai-ops`를 사용하지 않고, `$ai-ops`는 Codex+OMX 전용으로 유지하며, `.codex/jetbrains-ai-assistant-rules.md` 제거와 선택 전 Team 금지 규칙을 다음 `P3` 범위로 고정
- [2026-03-09] `P3` 선택 및 컨텍스트 기록: `python3 scripts/ai-ops/set_process_context.py --process P3 --wp WP-AIOPS-2026-03-008 --team-mode single`
- [2026-03-09] `P3` 구현: `.codex/jetbrains-ai-assistant-rules.md` 제거, `AGENTS.md` 선택 전 Team 금지 보강, `$ai-ops` skill의 `WP-008` 직접 참조 제거
- [2026-03-09] `S1` 선택 및 컨텍스트 기록: `python3 scripts/ai-ops/set_process_context.py --process S1 --wp WP-AIOPS-2026-03-008 --team-mode single`
- [2026-03-09] `S1` 리뷰 완료: Codex entrypoint ownership 반영을 승인하고, 다음 프로세스를 `S4`로 권장
- [2026-03-09] `S4` 선택 및 컨텍스트 기록: `python3 scripts/ai-ops/set_process_context.py --process S4 --wp WP-AIOPS-2026-03-008 --team-mode auto`
- [2026-03-09] `S4` 기록 고정: Codex entrypoint ownership round의 설계/구현/리뷰 결과를 고정하고, 후속 권장 프로세스를 `P0`로 정리
- [2026-03-09] `P0` 선택 및 컨텍스트 기록: `python3 scripts/ai-ops/set_process_context.py --process P0 --wp WP-AIOPS-2026-03-008 --team-mode single`
- [2026-03-09] `P0` 분석 완료: Claude+OMC SoT 구조 적용 갭 분석 - AGENTS.md 대비 .claude/CLAUDE.md에서 Mandatory References 2개 누락, Named Entrypoint Parity/Capability-First Rules/Soft Execution Contract 섹션 부재 확인, 후속 권장 프로세스 `P3`
- [2026-03-09] `P3` 선택 및 컨텍스트 기록: `python3 scripts/ai-ops/set_process_context.py --process P3 --wp WP-AIOPS-2026-03-008 --team-mode single`
- [2026-03-09] `P3` 구현: .claude/CLAUDE.md AI Ops Local Overlay 섹션을 AGENTS.md와 동등 수준으로 확장 - Named Entrypoint Parity, Mandatory References 6개, Capability-First Rules, Process Context 상세 절차, P3 Soft Execution Contract 추가
- [2026-03-09] `P3` 구현 보강: .gitignore 수정으로 .claude/.codex/.omc 설정/정책 파일 tracking 활성화 (runtime state 제외)

## 15. Claude+OMC SoT 구조 적용 분석 (P0)

### 15.1 분석 대상
- **목표**: Codex+OMX에서 정립된 "얇은 어댑터 + SoT 중심 구조"를 Claude Code + OMC에 동일하게 적용
- **SoT(Source of Truth)**: `docs/ai-ops/*`, `scripts/ai-ops/*`

### 15.2 현재 동작 비교

| 구성요소 | AGENTS.md (Codex+OMX) | .claude/CLAUDE.md (Claude+OMC) |
|---------|----------------------|-------------------------------|
| **Mandatory References** | 6개 (constitution, master-plan, index 포함) | 4개 (constitution, master-plan, index **누락**) |
| **Named Entrypoint 설명** | `$ai-ops` → SoT 연결 명시 | `/ai-ops` 언급 없음 |
| **Capability-First Rules** | 4개 규칙 | **없음** |
| **Process Context 절차** | 상세 (team/single 분기) | 예시만 |
| **Launch Gate** | launch_ai_ops_session.py 사용 | 없음 (PreToolUse 대체이나 명시 없음) |
| **Soft Execution Contract** | P3 명시 | **없음** |

### 15.3 갭 상세

**누락된 Mandatory References:**
- `docs/ai-ops/constitution.md`
- `docs/ai-ops/ops-bootstrap-master-plan.md`
- `docs/ai-ops/work-packets/index.md`

**누락된 섹션:**
1. Named Entrypoint Parity (`/ai-ops` → SoT 연결)
2. Capability-First Rules (도구 독립적 원칙)
3. Process Context 상세 절차
4. P3 Soft Execution Contract

### 15.4 위험 포인트
1. Claude 사용자가 constitution/master-plan/index를 참조하지 않고 작업 시작 가능
2. `/ai-ops`가 SoT와 어떻게 연결되는지 불명확
3. 도구 기능명에 종속될 위험 (Capability-First 부재)
4. P3 수행 시 품질 보장 계약 없음

### 15.5 후속 권장 프로세스
- **P3**: `.claude/CLAUDE.md`의 "AI Ops Local Overlay" 섹션을 AGENTS.md와 동등한 수준으로 확장

### 15.6 P3 구현 범위
1. Mandatory References 확장 (6개로)
2. Named Entrypoint Parity 섹션 추가
3. Capability-First Rules 섹션 추가
4. Process Context 상세 절차 추가
5. P3 Soft Execution Contract 추가

### 15.7 변경 대상 파일
- `.claude/CLAUDE.md` (AI Ops Local Overlay 섹션)

### 15.8 변경 제외 대상
- PreToolUse hook 동작 (그대로 유지)
- OMC 템플릿 블록 (`<!-- OMC:START -->` ~ `<!-- OMC:END -->`)
- `scripts/ai-ops/claude_pretooluse_guard.py`
