---
packet_id: "WP-DPC-2026-03-005"
title: "external ai-ops canonical migration inventory"
goal_ids: ["DPC-G1", "DPC-G4", "DPC-G5"]
status: "IN_REFINEMENT"
work_type: "MIGRATION"
priority: "P0"
target_environment: "master"
start_process: "P0"
current_process: "P1"
next_process: "P3"
owner: "SHARED"
created_at: "2026-03-11"
last_updated: "2026-03-11"
parent: "WP-DPC-2026-03-001"
track: "external canonical migration"
---

# WP-DPC-2026-03-005: external ai-ops canonical migration inventory

## 1. Background

- 사용자 전제가 변경되었다:
  - 앞으로 ai-ops 관련 **모든 작업의 canonical workspace는 external repo** ``ai-ops` (this repository)`
  - `ncube-regression-verify-ai-ops`는 **과거 ai-ops 작업의 archive/source-of-origin** 역할만 한다.
- 이 전제라면, 단순히 framework docs/scripts/templates만 external repo에 있는 것으로는 부족하다.
- external repo가 실제 canonical workspace가 되려면, source repo에만 남아 있는
  **control-board / ADR / changelog / roadmap / repo-local adapter surface** 중 무엇을 옮겨야 하는지 다시 분류해야 한다.

## 2. Goal

- 새로운 전제(external canonical, source archive-only) 아래에서 **이관 대상 전체를 재분류**한다.
- source repo에만 남아 있는 ai-ops 관련 자산 중
  - 반드시 external repo로 옮겨야 하는 것
  - 정제 후 옮겨야 하는 것
  - source archive에만 남겨야 하는 것
  - 옮기면 안 되는 것을 구분한다.
- 다음 `P1`에서 구체적인 migration policy / target structure를 확정할 수 있게 입력값을 만든다.

## 3. Scope

- source repo canonical ai-ops docs/records/adapters inventory
- external repo current coverage 분석
- control-board / ADR / changelog / roadmap / adapter surface gap 식별
- migration target categories 정의

## 4. Out of Scope

- 이번 P0에서 actual file move / copy / commit 수행
- external repo history rewrite/push
- public release execution

## 5. Done Criteria

- [x] source-only ai-ops assets inventory가 정리된다.
- [x] external repo current coverage와 gap이 식별된다.
- [x] must-move / curate-then-move / archive-only / do-not-move 분류가 나온다.
- [x] 다음 `P1`에서 확정해야 할 policy 질문이 정리된다.

## 6. Risks / Constraints

- source repo를 archive-only로 재정의하면, live control-board가 source repo에만 남아 있는 현재 구조는 곧바로 부정합이 된다.
- external repo에는 framework surface는 있지만, **repo가 스스로 ai-ops를 운영하기 위한 control-board/adapters**는 아직 없다.
- raw discussion transcript를 그대로 external public repo로 옮기면 product-history / internal-language 흔적이 그대로 노출될 수 있다.

## 7. Related References

### 7.1 Related Docs
- [WP-DPC-2026-03-001](./WP-DPC-2026-03-001-ai-ops-bootstrap.md)
- [WP-DPC-2026-03-003](./WP-DPC-2026-03-003-framework-extraction.md)
- [WP-DPC-2026-03-004](./WP-DPC-2026-03-004-public-history-replay-plan.md)
- [AI Ops CHANGELOG](../CHANGELOG.md)
- [운영체계 구축 상위 계획](../governance/ops-bootstrap-master-plan.md)
- [future-direction discussion archive](../archive/ai-ops/discussions/future-direction-discussion-2026-03-09.md)

### 7.2 Related Code
- source repo: current `docs/*`, `scripts/*`, `AGENTS.md`, `WORKSPACE-PROFILE.md`
- external repo: ``ai-ops` (this repository)`

## 8. Process Plan

### 8.1 분석 질문

1. external repo가 canonical workspace가 되려면 어떤 **live control-board**가 반드시 있어야 하는가?
2. source repo에 남아 있는 framework-level decision records는 external repo로 이관해야 하는가?
3. future direction / product vision / roadmap 류 논의는 raw transcript를 옮길 것인가, curated public docs로 재작성할 것인가?
4. external repo가 스스로 ai-ops를 사용하려면 어떤 **repo-local adapters**가 필요하며, 현재 무엇이 비어 있는가?

### 8.2 현재 coverage 분석

#### 이미 external repo에 있는 것

- framework docs:
  - `docs/constitution.md`
  - `docs/operating-model.md`
  - `docs/process-catalog/*`
  - `docs/tool-hooks/*`
  - `docs/commands/*`
  - `docs/portability/*`
  - `docs/omc-config/*`
  - `docs/work-packet-spec.md`
  - `docs/goal-alignment-checklist.md`
- framework scripts:
  - `scripts/check_compliance.py`
  - `scripts/set_process_context.py`
  - `scripts/launch_ai_ops_session.py`
  - `scripts/install_git_hooks.sh`
  - `scripts/sync_omc_policy.sh`
  - `scripts/cli.py`, `scripts/init.py`, `scripts/generate.py`
- templates:
  - `templates/AGENTS.md.j2`
  - `templates/WORKSPACE-PROFILE.md.j2`
  - `templates/claude/*`
  - `templates/codex/*`
  - `templates/project-ops/*`

#### external repo에 아직 없는 것

- live control-board:
  - `docs/work-packets/index.md`
  - `docs/CHANGELOG.md`
  - `docs/adr/`
  - `docs/ops-bootstrap-master-plan.md`
- repo-local tracked adapter surface:
  - `AGENTS.md`
  - `WORKSPACE-PROFILE.md`
- public-facing strategy/vision layer:
  - future direction / vision / roadmap / positioning docs

### 8.3 재분류 결과

#### A. 반드시 external repo로 이관해야 하는 것 (Must Move)

1. **live AI Ops control-board**
   - `docs/work-packets/index.md`
   - active/future ai-ops WP namespace
   - `docs/CHANGELOG.md`
   - `docs/adr/*`
2. **program-level operating plan**
   - `docs/ops-bootstrap-master-plan.md`
3. **external repo self-hosting adapters**
   - tracked `AGENTS.md`
   - tracked `WORKSPACE-PROFILE.md`

이유:
- external repo가 canonical workspace라면, 앞으로의 ai-ops 의사결정/작업/상태 전이는 external repo에서 기록되어야 한다.

#### B. 정제 후 external repo로 옮겨야 하는 것 (Curate Then Move)

1. **future direction / product vision / roadmap**
   - source raw material:
     - `docs/archive/ai-ops/discussions/future-direction-discussion-2026-03-09.md`
   - target shape:
     - `docs/vision.md`
     - `docs/roadmap.md`
     - `docs/why-ai-ops.md` 또는 `docs/positioning.md`
2. **replay-history plan의 external-facing subset**
   - source raw material:
     - `docs/work-packets/WP-DPC-2026-03-004-public-history-replay-plan.md`
   - target shape:
     - release note / history note / maintainers doc

이유:
- raw transcript / source-internal WP를 그대로 public canonical repo에 두는 것보다, public-facing 문서로 재작성하는 편이 적절하다.

#### C. source archive에만 남겨야 하는 것 (Archive Only)

1. source repo 내부 migration history 자체
   - `WP-DPC-2026-03-003` source cleanup detail
   - old legacy sunset review traces
2. raw discussion transcript
   - `docs/archive/ai-ops/discussions/future-direction-discussion-2026-03-09.md`
3. 이전 external draft history planning trace
   - source repo control-board에서만 필요한 migration/audit narrative

이유:
- canonical external repo에는 결과물과 정제된 narrative만 필요하고, source-side migration trace 전체는 archive에 두는 편이 맞다.

#### D. external repo로 옮기면 안 되는 것 (Do Not Move)

1. runtime/local state
   - `.omc/*`
   - `.omx/*`
   - local hook state/log
2. ncube/product-specific assets
   - `docs/project-ops/*`
   - java8/backport/workspace-specific product traces
3. source repo 전용 local environment overlays
   - source repo 전용 hidden local adapter/runtime artifacts

## 9. Analysis Findings

### 9.1 가장 큰 갭

external repo는 현재 **framework product surface**로는 꽤 완성됐지만,
**ai-ops가 스스로 ai-ops를 운영하는 canonical repo**로는 아직 미완성이다.

그 이유는:
- control-board 부재
- ADR/changelog 부재
- external repo 자체를 위한 tracked adapter 부재
- vision/roadmap 계층 부재

### 9.2 현재 external repo 상태 해석

- framework docs/scripts/templates 이관 → **완료**
- public history replay branch 구성 → **진행 중**
- canonical workspace 운영 surface 이관 → **미완료**

## 10. P1 policy refinement - external canonical migration target (2026-03-12)

### 10.1 핵심 정책

1. **2026-03-12부터 external repo가 ai-ops canonical workspace다**
   - 대상: ``ai-ops` (this repository)`
   - source repo `ncube-regression-verify-ai-ops`는 ai-ops 관련 **archive/source-of-origin only** 로 간주한다.
2. **이 날짜 이후 ai-ops live control-board는 source repo에 추가하지 않는다**
   - source repo의 `docs/work-packets/*`, `docs/adr/*`, `docs/CHANGELOG.md`는 ai-ops live 기록면으로 더 이상 사용하지 않는다.
   - source repo에는 archive note 또는 migration trace만 남길 수 있다.
3. **external repo는 framework product surface + self-hosting control-board를 모두 가져야 한다**
   - framework docs/scripts/templates만 있는 상태로는 canonical workspace로 충분하지 않다.
   - external repo 자체가 ai-ops를 운영하는 주체가 되도록 control-board/adapters를 함께 갖춰야 한다.

### 10.2 External repo target structure (최종 목표)

external repo는 아래 구조를 가져야 한다.

#### A. 이미 존재하는 framework surface

- `docs/constitution.md`
- `docs/operating-model.md`
- `docs/process-catalog/*`
- `docs/tool-hooks/*`
- `docs/commands/*`
- `docs/portability/*`
- `docs/omc-config/*`
- `docs/work-packet-spec.md`
- `docs/goal-alignment-checklist.md`
- `scripts/*`
- `templates/*`

#### B. 추가되어야 하는 live control-board

- `docs/work-packets/index.md`
- `docs/work-packets/WP-DPC-*.md` (external canonical live packets)
- `docs/adr/ADR-DPC-*.md`
- `docs/CHANGELOG.md`
- `docs/ops-bootstrap-master-plan.md`

#### C. external repo self-hosting adapter surface

- tracked `AGENTS.md`
- tracked `WORKSPACE-PROFILE.md`

#### D. public-facing strategy layer

- `docs/vision.md`
- `docs/roadmap.md`
- `docs/why-ai-ops.md` 또는 `docs/positioning.md`

### 10.3 Must Move set (구체화)

다음은 다음 P3에서 **반드시 external repo로 이관/생성**해야 한다.

#### Live control-board
- `docs/work-packets/index.md`
- active/future AI Ops WP files
  - `WP-DPC-2026-03-001`
  - `WP-DPC-2026-03-002`
  - `WP-DPC-2026-03-004`
  - `WP-DPC-2026-03-005`
- `docs/CHANGELOG.md`
- `docs/adr/ADR-DPC-001..005`
- `docs/ops-bootstrap-master-plan.md`

#### Repo-local adapters
- `AGENTS.md`
- `WORKSPACE-PROFILE.md`

이유:
- 앞으로의 ai-ops live work, 상태 전이, 정책 업데이트, replay/publicization 후속 작업이 external repo에서 수행돼야 하기 때문이다.

### 10.4 Curate Then Move set (구체화)

다음은 **raw file을 그대로 복사하지 말고 public-facing 문서로 재작성**해야 한다.

#### Strategy / vision
- source material:
  - `docs/archive/ai-ops/discussions/future-direction-discussion-2026-03-09.md`
- target docs:
  - `docs/vision.md`
  - `docs/roadmap.md`
  - `docs/why-ai-ops.md` 또는 `docs/positioning.md`

#### Replay/public history explanation
- source material:
  - `docs/work-packets/WP-DPC-2026-03-004-public-history-replay-plan.md`
- target docs:
  - `docs/history.md` 또는 maintainer-facing replay note

정책:
- raw discussion transcript는 external canonical repo의 live docs로 두지 않는다.
- 공개용 문서는 framework vision/positioning 기준으로 정제한다.

### 10.5 Archive Only set (구체화)

다음은 source repo archive에만 남긴다.

- `WP-DPC-2026-03-003` source cleanup / legacy sunset 상세 trace
- raw discussion transcript 원본
- source repo 내부에서만 의미 있는 migration review detail
- legacy namespace sunset review/decision trace 원본

정책:
- external repo에는 결과물/정제 문서만 두고,
- source-side migration trace 원본은 source archive에 남긴다.

### 10.6 Do Not Move set (구체화)

- `.omc/*`
- `.omx/*`
- local logs / state / hook runtime files
- `docs/project-ops/*`
- product-specific backport / java8 / branch-specific traces
- source repo 전용 local overlay/runtime files

### 10.7 Source repo archive-only cutoff rule

**Cutoff date: 2026-03-12**

이 날짜 이후:

1. source repo에서는 ai-ops live WP/ADR/changelog를 새로 생성/갱신하지 않는다.
2. source repo는 external canonical 전환 사실을 설명하는 archive note만 남길 수 있다.
3. ongoing ai-ops live task는 external repo control-board로 이관한다.

### 10.8 Next P3 implementation target

다음 P3에서는 최소한 아래를 수행해야 한다.

1. external repo에 live control-board 신설
2. active WP 4건 이관
3. ADR-DPC-001..005 이관
4. external `docs/CHANGELOG.md` / `docs/ops-bootstrap-master-plan.md` 생성
5. external tracked `AGENTS.md` / `WORKSPACE-PROFILE.md` 추가
6. source repo archive-only cutoff note 반영

### 10.9 다음 권장 프로세스

- `P3`
  - external repo로 must-move set 실제 이관
  - control-board/adapters bootstrap
  - source repo archive-only cutoff 적용
## 11. Deliverables

- source-only asset inventory
- external current coverage gap list
- migration target classification
- next `P1` policy questions

## 12. Review Notes

- 앞으로 ai-ops 관련 모든 작업을 external repo에서만 한다면,
  source repo의 `docs/work-packets`, `docs/adr`, `docs/CHANGELOG.md`는 더 이상 canonical live surface로 남아 있으면 안 된다.
- 다음 단계는 “무엇을 옮길지”를 넘어서 “external repo에서 canonical control-board를 어떤 구조로 운영할지”를 결정해야 한다.

## 13. Decisions

| 결정 | 선택 | 이유 |
|---|---|---|
| external canonical assumption | 채택 | 사용자 명시 전제 |
| source repo 역할 | archive/source-of-origin only | future ai-ops work는 external repo에서만 수행 |
| raw discussion 처리 | curate-then-move | public repo에는 정제된 vision/roadmap 문서가 더 적합 |
| live control-board 처리 | must move | canonical workspace면 상태/ADR/changelog도 함께 있어야 함 |
| source migration trace 처리 | archive-only | 결과 repo에는 과거 이관 trace 전체가 필요하지 않음 |
| active AI Ops packets 처리 | external live migration | source repo archive-only 전제와 일관 |
| ADR-DPC-001..005 처리 | external live migration | framework 정책은 canonical repo에도 live로 존재해야 함 |
| source repo cutoff date | 2026-03-12 | canonical workspace 전환 시점 명시 |

## 14. Follow-ups

- `P1`: external canonical migration policy 확정
  - external repo의 control-board 구조
  - source repo archive-only cutoff rule
  - vision/roadmap 문서 target shape
- `P3`: selected assets를 external repo로 실제 이동/재작성

## 15. Timeline

- [2026-03-11] 사용자 전제 변경: 앞으로 ai-ops 관련 모든 작업은 external repo에서 수행, source repo는 archive-only로 취급
- [2026-03-11] `P0` 시작: 이 전제 아래 migration target inventory 재분석
- [2026-03-12] `P1` 시작: must-move / curate-then-move / archive-only / do-not-move 정책 확정
