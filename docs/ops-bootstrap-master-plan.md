# 운영체계 구축 상위 계획 (Master Plan)

> Status: Active  
> Last Updated: 2026-03-11  
> Parent WP: [WP-DPC-2026-03-001](./work-packets/WP-DPC-2026-03-001-ai-ops-bootstrap.md)  
> Governing ADR: [ADR-DPC-001](./adr/ADR-DPC-001-bootstrap-requirement-change-sync.md)  
> Constitution: [AI Ops Constitution](./constitution.md)  
 
## 1. 목적

단위 작업(WP)이 분할/확장되는 동안에도 운영체계 구축의 최상위 목표와 현재 진행 위치를 잃지 않도록,
프로그램 단위 계획을 별도 문서로 유지한다.
또한 AI 운영체계 기록을 프로젝트 기능 ADR/WP와 물리적으로 분리해 혼선을 방지한다.

## 2. 최상위 목표 (North Star)

1. 운영체계 구축 작업 자체를 WP/ADR/index/changelog로 관리한다.
2. 운영체계 준수를 2개 트랙으로 강제한다.
3. `ai-collaboration-guide.md` 의존도를 단계적으로 줄이고 분해 가능한 구조로 전환한다.
4. `ai-ops`를 개별 AI 엔진이 아니라, 지속적으로 등장하는 실행 엔진/도구를 활용하는 운영체계 레이어로 발전시킨다.
5. 운영 문서는 도구 고유 기능명보다 capability 계약을 우선해 기술한다.
6. 프로세스 종료 시 커밋 여부를 사용자에게 질의해 프로세스 단위 이력을 최대한 보존한다.

## 3. 운영 트랙

### Track 1. 작업 과정 강제 (AI tool별 훅)
- Codex CLI + OMX: 런타임 어댑터 규칙 + 프로세스 진입점 강제
- Claude Code + OMC: `PreToolUse` 중심 차단/질의 게이트 + `quality gates`, `Ultra QA` 검증 루프
- 작업 WP: [WP-DPC-2026-03-002](./archive/ai-ops/work-packets/WP-DPC-2026-03-002-ai-tool-hook-enforcement.md)
- 도구 훅 레퍼런스: [tool-hooks/README.md](./tool-hooks/README.md)

### Track 2. 최종 산출물 강제 (Git hook)
- pre-commit/pre-push 단계에서 운영체계 준수 흔적 점검
- 준수 의심 시 차단 또는 리뷰 요구
- 작업 WP: [WP-DPC-2026-03-003](./archive/ai-ops/work-packets/WP-DPC-2026-03-003-git-hook-output-compliance-gate.md)

### Track 3. 문서 구조 전환/운영 파일 정착
- ai-collaboration-guide.md 분해 → 독립 운영 문서 체계 구축
- 허브/진입점/인덱스 체계 정착
- 기존 문서 재배치 및 deprecated 처리
- **G0 프로세스 신설 및 프로세스 카탈로그 확장** (ADR-DPC-002)
- 작업 WP: [WP-DPC-2026-03-004](./archive/ai-ops/work-packets/WP-DPC-2026-03-004-document-structure-transition.md)

### Track 4. 프로세스 기반 협업 전환
- 모든 작업 시작 시 **프로세스 선택 질의** 강제
- 사용자가 프로세스 미적용(`NONE`)을 선택하면 일반 작업(single-agent) 허용
- 선택 프로세스를 컨텍스트 파일(`.omc/ai-ops-process-context.json`)로 기록
- 도구별 설정이 분해된 운영 문서를 참조하도록 연결
  - Claude Code (.claude/): 프로세스 선택 규칙 추가
  - Codex / JetBrains AI Assistant: `AGENTS.md` 중심 진입 규칙으로 연결
- 선택된 프로세스의 입력/단계/산출물/종료조건 준수 강제
- 프로세스별 최소 논리 역할 세트/팀 프로파일 강제
- Team 경로에서 팀원별 실제 역할(`member:role`) 강제
- Team 활성화는 **조건부**로 수행
  - 프로세스 선택 완료
  - 다중 역할 검증이 필요한 작업(다중 파일/고위험 변경/사용자 명시 요청)
- ai-collaboration-guide.md는 설계 문서로 보존, 운영 문서는 별도 분해본 참조
- 작업 WP: [WP-DPC-2026-03-005](./archive/ai-ops/work-packets/WP-DPC-2026-03-005-process-based-collaboration.md)

### Track 5. 물리 워크스페이스 분리 운영 정착
- `master`와 `wafful4(java8)`를 디렉토리 단위로 분리 운영
- 각 워크스페이스 전용 규칙 문서/진입점 설정 유지
- master-first backporting 워크플로우 강제
- 레퍼런스: [workspace-profiles/README.md](./workspace-profiles/README.md)

### Track 6. AI 도구 산출물 경계 정렬 (분리 준비)
- 숨김 도구 디렉토리(`.claude/.codex/.omc`)를 로컬 전용으로 고정
- 원격 관리 정책/지침을 `docs/`/`scripts/` 비숨김 경로로 이관
- ai-ops Framework 자산과 타겟 프로젝트 Adapter 자산의 경계를 명시
- 작업 WP: [WP-DPC-2026-03-007](./archive/ai-ops/work-packets/WP-DPC-2026-03-007-ai-tool-artifact-separation.md)

### Track 7. Codex+OMX 운영 정렬 (Claude+OMC 성공패턴 이식)
- Codex 도구 조합을 `codex + omx` 기준으로 표준화
- `claude + omc` 파일럿 성공패턴(프로세스 선택 -> 조건부 Team -> 검증/기록)을 Codex 경로에 이식
- 임시 프로세스(2회 한정)로 누락 방지 후 상시화 여부를 판정
- soft guarantee baseline 이후, `Codex+OMX` 지원 표면만으로 runtime hard guarantee가 가능한지 별도 분석하고 불가능한 경계는 명시한다.
- 현재 우선순위는 `Codex+OMX` 정렬 및 G6 완료이며, `CLAUDE.md` 개편과 제품화 메커니즘(marker block / sync script / installer / marketplace)은 후순위로 둔다.
- 장기적으로는 `ai-ops`를 오픈소스 + 간단 명령/마켓플레이스 기반 프로덕트로 발전시키되, 현 Phase 6 범위에는 포함하지 않는다.
- Codex/Claude adapter 문서는 가변적인 기능명보다 capability 계약과 현재 매핑 예시를 분리해 기록한다.
- JetBrains AI Assistant 일반 경로는 `AGENTS.md` + SoT를 따르고, `$ai-ops`는 Codex+OMX 전용 named entrypoint로 유지한다.
- hidden local rule-pack에 대한 canonical 정책 의존을 줄이고, active WP는 index/context를 통해 해석한다.
- 현재 판단으로는 Claude급 hard guarantee는 Codex native hook 또는 외부 wrapper 없이 달성하기 어렵다.
- 외부 소규모 Codex wrapper 프로젝트는 직접 의존성으로 들이지 않고, 개념 참고 후 OMX 중심 설계로 흡수한다.
- 현 단계의 1순위 전략은 OMX-centered process-aware launch wrapper / gateway이며, native hook parity는 장기 추적 대상으로 둔다.
- Codex+OMX에서 먼저 정립한 얇은 어댑터 + SoT 중심 구조는 후속 Claude+OMC 개편 시에도 동일한 방향으로 적용한다.
- 작업 WP: [WP-DPC-2026-03-002](./work-packets/WP-DPC-2026-03-002-codex-omx-alignment.md)

### Track 8. ai-ops framework extraction / legacy surface sunset
- source repo의 canonical AI Ops surface를 root `docs/*`, `scripts/*`로 고정한다.
- legacy `docs/ai-ops/*`, `scripts/ai-ops/*`는 sunset 완료. archive 제거됨 (핵심 결정은 ADR/CHANGELOG에 보존).
- discussion helper / frozen discussion / migration-review docs / shim / hook-source의 최종 처리 정책을 분리한다.
- P3에서 legacy bridge/shim 제거와 archive relocation을 수행했고, 다음 S1에서 최종 deletion readiness PASS/NO-GO를 판정한다.
- 작업 WP: [WP-DPC-2026-03-003](./work-packets/WP-DPC-2026-03-003-framework-extraction.md)

### Track 9. public repository history replay
- external `ai-ops` repo의 file contents 정리와 별도로, public-facing git history를 framework evolution narrative 기준으로 재구성한다.
- source repo의 기존 WP/ADR 의미 단위를 external repo commit sequence(`wp001`, `adr001`, ...)로 replay한다.
- product-specific pilot/migration 흔적은 제외하고 framework-only 서사를 유지한다.
- 작업 WP: [WP-DPC-2026-03-004](./work-packets/WP-DPC-2026-03-004-public-history-replay-plan.md)

### Track 10. external canonical migration inventory
- external `ai-ops` repo를 future canonical workspace로 채택한다고 가정하고, source repo에만 남아 있는 ai-ops 관련 자산을 다시 분류한다.
- framework surface만이 아니라 control-board, ADR, changelog, roadmap, repo-local adapters까지 포함해 must-move / archive-only / do-not-move를 정한다.
- cutover 이후 source repo는 archive/source-of-origin only로 두고, live AI Ops control-board는 external repo로 옮긴다.
- 작업 WP: [WP-DPC-2026-03-005](./work-packets/WP-DPC-2026-03-005-external-canonical-migration-inventory.md)

## 4. 단계 및 게이트

| Phase | Gate | 핵심 목표 | 주관 WP |
|------|------|----------|--------|
| Phase 0 | G0 | 기존 WP/ADR 템플릿 동결 + 동기화 강제 규칙 확정 | WP-DPC-2026-03-001 |
| Phase 1 | G1 | 트랙1/트랙2 강제 메커니즘 분리 및 착수 | WP-DPC-2026-03-002, WP-DPC-2026-03-003 |
| Phase 2 | G2 | 문서 구조 전환: ai-collaboration-guide.md 분해 → AI 도구 참조용 운영 문서 생성 | WP-DPC-2026-03-004 |
| Phase 3 | G3 | 프로세스 기반 협업 전환: 프로세스 선택 질의 강제 + 도구 설정 연결 | WP-DPC-2026-03-005 |
| Phase 4 | G4 | 파일럿 검증: 실제 product-ops 작업 3건을 프로세스 기반으로 수행 | WP-DPC-2026-03-006 |
| Phase 5 | G5 | AI 도구 산출물 원격/로컬 경계 정렬 및 포팅 경계 고정 | WP-DPC-2026-03-007 |
| Phase 6 | G6 | Codex+OMX 운영 정렬: 임시 프로세스 2회 검증 및 상시화 판정 | WP-DPC-2026-03-002 |

### Phase 완료 기준

**Phase 2 (G2) 완료 기준:**
- ai-collaboration-guide.md가 허브 문서로 전환됨
- 프로세스 카탈로그가 독립 문서로 분리됨 (P0~S4 + G0)
- AI 도구가 참조할 운영 문서 체계가 완성됨
- 프로세스 선택 가이드가 독립 문서로 존재함

**Phase 3 (G3) 완료 기준:**
- 모든 도구 설정(.claude/, .codex/)에 프로세스 선택 질의 규칙 추가됨
- 선택 프로세스 컨텍스트 기록 경로(`set_process_context.py`)가 적용됨
- Claude PreToolUse에서 프로세스별 하드 차단이 동작함
- Team 가능 프로세스에서 `team_mode=auto` 상태 구현 변경이 차단됨
- Team 경로에서 최소 역할 프로파일 미충족 시 차단됨
- Team 경로에서 팀원별 실제 역할 미정의/누락 시 차단됨
- 도구 설정이 분해된 운영 문서를 참조함 (ai-collaboration-guide.md 직접 참조 금지)
- 프로세스 선택 → 절차 준수 흐름이 도구 수준에서 강제됨
- `/ai-ops` 실행 시 사용자 선택 전 Team 자동 활성화가 발생하지 않음
- 프로세스 미적용(`NONE`) 분기가 정상 동작함

**Phase 4 (G4) 완료 기준:**
- 실제 product-ops 작업 3건이 프로세스 기반으로 수행됨
- 각 작업에서 프로세스 선택 질의 → WP 생성 → 절차 준수 → 후속 연결이 검증됨
- 프레임워크 완성 선언 가능

**Phase 5 (G5) 완료 기준:**
- 숨김 도구 디렉토리(`.claude/.codex/.omc`) 원격 비추적 정책이 워크스페이스 간 일치함
- 원격 관리 대상 정책/지침이 비숨김 경로(`docs/`, `scripts/`)에 존재함
- ai-ops Framework vs Project Adapter 경계 문서가 고정됨

**Phase 6 (G6) 완료 기준:**
- `codex + omx` 운영 경로가 `claude + omc` 성공패턴과 동일한 절차 기준으로 문서화됨
- JetBrains AI Assistant 일반 경로와 Codex+OMX `$ai-ops` 경로의 소유 경계가 문서로 고정됨
- 임시 프로세스(2회 한정) 파일럿 #1/#2 체크리스트가 모두 충족됨
- Team auto 방지 / `NONE` 분기 검증 결과가 파일럿 기록에 남음
- 임시 프로세스 sunset(종료/상시화 판정) 결정이 기록됨

## 5. 망각 방지 규칙 (Traceability Rules)

1. 모든 단위 WP는 반드시 상위 목표(Track/Phase) 1개 이상과 연결한다.
2. 단위 WP 제목만으로 목적이 불명확하면 `Goal`과 `Scope`를 먼저 갱신한다.
3. 세션 시작 시 아래 3개를 우선 확인한다.
   - `work-packets/index.md`
   - 본 문서(상위 계획)
   - 부모 WP(현재는 WP-DPC-2026-03-001)
4. 세션 종료 전 `next_process`와 후속 WP 연결을 확인한다.
5. **G0 목표 정합성 점검**을 다음 시점에 수행한다 (ADR-DPC-002):
   - 세션 시작 시 (필수)
   - Phase/Track 전환 시 (필수)
   - 마일스톤 완료 시 (필수)
   - 세션 중간 (권장, 사용자 요청 또는 1시간 경과)

## 6. 훅 수명주기 정책 (필수)

훅은 1회성 설정이 아니라 운영체계 고도화와 함께 계속 갱신해야 한다.

1. 신규 규칙이 추가되면 트랙1/트랙2 훅 규칙도 같은 주기에 업데이트한다.
2. 오탐/미탐 또는 우회 사례가 발견되면 즉시 보정 WP를 생성/갱신한다.
3. 마일스톤 종료 시 훅 유효성 리뷰를 수행하고 결과를 ADR/WP에 기록한다.

## 7. 변경 관리 프로토콜 (Hard)

요구사항 변경 시 반드시 같은 세션에서 아래를 함께 갱신한다.

1. [constitution.md](./constitution.md) (불변 목표/규칙 변경 시)
2. 관련 WP(부모/자식)
3. [work-packets/index.md](./work-packets/index.md)
4. [CHANGELOG.md](./CHANGELOG.md)
5. ADR(정책 변경 시)
6. 본 문서(상위 계획)

누락 시 상태 전이 금지.
