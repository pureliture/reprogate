---
packet_id: "WP-DPC-2026-03-004"
title: "ai-ops public repository replay history plan"
goal_ids: ["DPC-G1", "DPC-G4", "DPC-G5"]
status: "IN_REFINEMENT"
work_type: "MIGRATION"
priority: "P1"
target_environment: "master"
start_process: "P1"
current_process: "P1"
next_process: "P3"
owner: "SHARED"
created_at: "2026-03-11"
last_updated: "2026-03-11"
parent: "WP-DPC-2026-03-001"
track: "public-history replay"
---

# WP-DPC-2026-03-004: ai-ops public repository replay history plan

> Historical interpretation note: 이 문서는 external public repo history를 framework narrative로 재구성하려던 계획 기록이다. 현재 ReproGate 관점에서는 **브랜드/역사 정렬을 준비한 historical replay packet**으로 읽는다.

## 1. Background

- `WP-DPC-2026-03-003`을 통해 source repo의 legacy namespace sunset과 external `ai-ops` framework repo bootstrap completeness는 완료되었다.
- 그러나 external repo ``ai-ops` (this repository)`의 현재 git history는 `C1~C7 + bootstrap completion` 중심이며,
  **"ai-ops를 처음부터 독립 framework로 구축해온 것 같은 서사"**를 충분히 보여주지 못한다.
- 사용자 의도는 단순한 추출 이력 보존이 아니라, 기존 ai-ops의 framework 진화 과정을
  **WP/ADR 의미 단위로 replay** 하여 public repo history 자체를 제품 구축 이력처럼 보이게 만드는 것이다.

## 2. Goal

- external `ai-ops` repo를 public release 가능한 상태로 유지하되,
  git history는 **기존 ai-ops의 framework 진화 순서**를 반영하도록 재구성한다.
- replay 대상/비대상 단위, 커밋 순서, 메시지 규칙, 검증 게이트를 명확히 고정한다.
- 다음 `P3`에서 실제 history rewrite / replay를 수행할 수 있을 정도로 구체적인 실행 계획을 만든다.

## 3. Scope

- replay 대상 WP/ADR 의미 단위 선정
- external repo용 target commit sequence 설계
- commit naming / numbering convention 고정
- replay execution mechanics(오픈소스 공개 전 rewrite 전략) 정의
- validation / publication gate 정의

## 4. Out of Scope

- 이번 P1에서 external repo history를 실제로 rewrite 하는 작업
- public remote 생성/푸시
- framework 기능 추가
- product-specific pilot/backport history를 public repo에 포함하는 작업

## 5. Done Criteria

- [x] replay 대상 WP/ADR 의미 단위와 제외 단위가 구분된다.
- [x] external repo target commit sequence가 고정된다.
- [x] numbering / commit message 규칙이 고정된다.
- [x] replay 실행 방식(새 orphan/fresh replay branch 기준)이 고정된다.
- [x] validation / publish 직전 게이트가 정의된다.
- [x] 다음 `P3` 실행 입력값이 준비된다.

## 6. Risks / Constraints

- source repo의 실제 historical commit과 public replay commit은 1:1 동일할 필요가 없지만,
  **의미 단위와 서사**는 일관되어야 한다.
- external repo에는 framework-only asset만 남겨야 하므로, source repo의 WP/ADR 문서 자체를 옮기는 것이 아니라
  **그 결정이 만들어낸 framework artifact snapshot**을 replay 대상으로 삼아야 한다.
- product-specific 검증 round(`WP-006` 등)를 public repo history에 섞으면 framework history가 오염된다.
- 이미 생성된 external repo의 현재 8개 커밋은 초안으로 보고, public push 전에 rewrite 가능해야 한다.

## 7. Related References

### 7.1 Related Docs
- [WP-DPC-2026-03-001](./WP-DPC-2026-03-001-ai-ops-bootstrap.md)
- [WP-DPC-2026-03-002](./WP-DPC-2026-03-002-codex-omx-alignment.md)
- [WP-DPC-2026-03-003](./WP-DPC-2026-03-003-framework-extraction.md)
- [AI Ops CHANGELOG](../CHANGELOG.md)
- [운영체계 구축 상위 계획](../governance/ops-bootstrap-master-plan.md)
- [ADR-DPC-001](../adr/ADR-DPC-001-bootstrap-requirement-change-sync.md)
- [ADR-DPC-002](../adr/ADR-DPC-002-goal-alignment-process.md)
- [ADR-DPC-003](../adr/ADR-DPC-003-conditional-team-activation-and-optout.md)
- [ADR-DPC-004](../adr/ADR-DPC-004-ai-tool-artifact-boundary.md)
- [ADR-DPC-005](../adr/ADR-DPC-005-codex-entrypoint-ownership-and-ai-assistant-decoupling.md)

### 7.2 Related Code
- external framework repo: ``ai-ops` (this repository)`

### 7.3 Related Tests
- external repo:
  - `python3 scripts/cli.py check --mode none`
  - `python3 scripts/check_compliance.py --mode none`
  - `init -> generate -> generated target compliance` smoke

### 7.4 Related Commits
- external repo current draft chain:
  - `15a7422`
  - `8628810`
  - `7f7e1be`
  - `fa9a1ec`
  - `32103e6`
  - `6d90120`
  - `49a4ece`
  - `30a287f`

## 8. Process Plan

### 8.1 Current problem statement

현재 external repo는 **추출 작업을 수행한 흔적**은 남아 있지만,
사용자 목적이었던 **"ai-ops가 처음부터 독립 framework로 구축되어 온 제품 이력"**을 보여주지는 못한다.

따라서 다음 `P3`의 목적은 파일 내용 이관이 아니라
**external repo git history의 public-facing narrative rewrite**다.

### 8.2 Replay 대상 선정 원칙

Replay commit은 source repo의 WP/ADR **문서 자체**를 옮기는 것이 아니라,
그 단위가 만들어낸 **framework artifact snapshot**을 external repo history로 재구성한다.

#### 포함 대상

- `WP-DPC-2026-03-001` bootstrap foundation
- `ADR-DPC-001` requirement change sync rule
- `WP-DPC-2026-03-002` tool hook enforcement
- `WP-DPC-2026-03-003` git hook compliance gate
- `WP-DPC-2026-03-004` document structure transition
- `ADR-DPC-002` goal alignment process
- `WP-DPC-2026-03-005` process-based collaboration
- `ADR-DPC-003` conditional team activation / opt-out
- `WP-DPC-2026-03-007` AI tool artifact boundary preparation
- `ADR-DPC-004` AI tool artifact boundary
- `WP-DPC-2026-03-002` Codex+OMX alignment (framework-relevant subset)
- `WP-DPC-2026-03-009` Claude+OMC SoT application (template/adapter-relevant subset)
- `ADR-DPC-005` codex entrypoint ownership / AI assistant decoupling
- `WP-DPC-2026-03-003` framework extraction + portable bootstrap completion

#### 제외 대상

- `WP-DPC-2026-03-006` pilot verification
  - 이유: product WP와 backport trace가 섞인 검증 round라 public framework history로 replay하기 부적절
- source repo migration cleanup only records
  - legacy namespace sunset의 source-repo cleanup detail 자체는 external repo 공개 히스토리의 본류가 아님
- product-specific path/branch/runtime details

### 8.3 External repo target commit sequence

아래 순서로 replay한다.

| Seq | Replay Unit | Purpose in public history | Representative output scope |
|---|---|---|---|
| 01 | `wp001` | framework bootstrap foundation | repo skeleton, README, license, initial docs skeleton |
| 02 | `adr001` | synchronized change-management rule | docs wording / governance rule baseline |
| 03 | `wp002` | tool-hook enforcement foundation | hook docs + guard/compliance primitives |
| 04 | `wp003` | final-output compliance gate | git/compliance rule strengthening |
| 05 | `wp004` | document structure transition | process catalog / operating docs split |
| 06 | `adr002` | goal alignment process | G0-related process docs |
| 07 | `wp005` | process-based collaboration model | process selection / context / team-mode contract |
| 08 | `adr003` | conditional team activation | team activation policy surface |
| 09 | `wp007` | artifact boundary preparation | framework vs project boundary docs |
| 10 | `adr004` | artifact boundary decision | boundary rule formalization |
| 11 | `wp008` | Codex+OMX alignment | Codex-facing commands/rules/templates |
| 12 | `wp009` | Claude+OMC parity surface | Claude-facing templates/hook/settings guidance |
| 13 | `adr005` | entrypoint ownership / decoupling | adapter ownership wording cleanup |
| 14 | `wp010` | portable bootstrap completion | schema/templates/generate/install/launch/check completeness |

### 8.4 Commit numbering / message convention

public repo에서는 source repo의 날짜형 WP id를 commit subject에 직접 드러내기보다,
아래처럼 **replay sequence prefix**를 사용한다.

#### WP replay
- `feat(ai-ops): replay wp001 bootstrap foundation`
- `feat(ai-ops): replay wp002 tool hook enforcement`

#### ADR replay
- `docs(ai-ops): replay adr001 requirement sync rule`
- `docs(ai-ops): replay adr005 codex entrypoint ownership`

규칙:
1. numbering은 public repo replay sequence 기준의 3자리(`wp001`, `adr001`)를 사용한다.
2. WP/ADR origin mapping은 별도 replay plan 문서(본 WP)와 release notes에 남긴다.
3. commit body에는 필요 시 source reference를 남기되, 공개 히스토리의 주제는 **framework evolution narrative**로 유지한다.

### 8.5 Replay execution mechanics

다음 `P3`에서 아래 방식으로 수행한다.

1. external repo에서 현재 draft history는 보존용 branch/tag로 백업한다.
   - 예: `draft/extraction-c1-c7`
2. public replay용 새 branch를 **orphan root** 또는 fresh clone 기준으로 시작한다.
3. 최종 `HEAD`의 파일 내용을 기준선으로 삼되,
   각 replay step마다 필요한 파일 subset만 staged 하여 commit한다.
4. 각 단계는 "현재 최종 파일 집합에서 해당 시점에 존재했어야 할 최소 snapshot"을 구성한다.
5. 마지막 `wp010` commit 이후에 현재 external repo working tree와 동일한 파일 집합이 되도록 맞춘다.

### 8.6 Snapshot construction rule

각 replay commit은 아래 원칙으로 만든다.

1. **future file leakage 금지**
   - 해당 step 이전에 존재하면 안 되는 파일은 staged 하지 않는다.
2. **framework-only 유지**
   - WP/ADR 원문, source repo control-board, local runtime/state/log는 포함하지 않는다.
3. **narrative-first split**
   - 같은 최종 파일이라도 public story상 나중에 소개해야 맞는 기능은 뒤 commit으로 미룬다.

## 9. Execution Notes

### 9.1 Replay source mapping 메모

- `wp001~wp005`는 source repo의 초기 bootstrap/운영체계 구축 WPs와 ADR 001~003에서 산출된 framework docs/scripts를 기준으로 split
- `wp007 + adr004`는 portability/boundary layer
- `wp008 + wp009 + adr005`는 adapter/tool-specific alignment layer
- `wp010`은 external repo를 self-contained bootstrap repo로 만드는 final consolidation layer

### 9.2 Validation gates for next P3

Replay 완료 후 external repo에서 반드시 통과해야 한다.

1. `git status` clean
2. `python3 scripts/cli.py check --mode none`
3. `python3 scripts/check_compliance.py --mode none`
4. `init -> generate -> generated target compliance` smoke
5. project-specific 문자열(`ncube`, `wafful`, source absolute path, legacy internal path) 미검출
6. public replay final `HEAD` file tree가 current external repo intended surface와 동등

### 9.3 Publish gate

public push는 아래를 만족할 때만 허용한다.

1. replay sequence `wp001..wp010`, `adr001..adr005`가 계획대로 재구성됨
2. excluded unit(`WP-006`)이 public history에 혼입되지 않음
3. final validation pass
4. release note 또는 README에 "framework-only repo이며 source project history를 직접 복제하지 않는다"는 설명 유지

## 10. Deliverables

- replay 대상/비대상 분류표
- external repo target commit sequence
- commit naming convention
- replay execution mechanics
- validation / publish gate checklist

## 11. Review Notes

- 현재 external repo의 `C1~C7` draft chain은 public release 전 백업 branch로 보존하고,
  public-facing history는 새 replay chain으로 대체하는 것이 적절하다.
- public repo는 "마이그레이션 흔적"보다 "framework evolution"이 보여야 한다는 사용자 목적을 우선 반영해야 한다.

## 12. Decisions

| 결정 | 선택 | 이유 |
|---|---|---|
| public history 기준 | framework evolution narrative | 단순 추출 이력보다 사용자가 원한 제품 구축 이력에 부합 |
| replay 단위 | WP/ADR 의미 단위 | 기존 ai-ops evolution trace를 서사 단위로 보존 |
| numbering 방식 | `wp001`, `adr001` | public repo에서 간결하고 순차적인 story 제공 |
| execution base | orphan/fresh replay branch | 현재 C1~C7 초안 history를 깔끔하게 대체하기 쉬움 |
| excluded unit | `WP-006` | product pilot 성격이라 framework public history와 부정합 |
| final consolidation unit | `wp010` | portable bootstrap surface 완성 지점이기 때문 |

## 13. Follow-ups

- `P3`: external `ai-ops` repo replay branch 생성 및 history rewrite 실행
- `S1`: replay history quality / narrative / validation review
- `S4`: public release verdict와 publish trace 기록

## 14. Timeline

- [2026-03-11] 사용자 요구 명확화: external repo는 단순 추출 이력이 아니라, ai-ops를 처음부터 구축한 것처럼 보이는 public history가 필요함
- [2026-03-11] `P1` 시작: replay plan 대상/순서/게이트 정의
