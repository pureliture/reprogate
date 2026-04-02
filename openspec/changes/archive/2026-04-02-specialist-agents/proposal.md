## Why

Phase 03 (Skill Evolution)이 완료되어 ReproGate의 ECC 코어 레이어가 갖춰졌다. 다음 단계는 GSD 플로우(`discuss → plan → execute → verify`)를 실제로 구동할 **Specialist Agents**다. 현재 `/rg:*` 커맨드가 없어 개발자는 ReproGate의 단계별 워크플로우를 실행할 수 없고, 하네스가 단순 hook/record 도구에 머물고 있다. Phase 04는 executor, verifier, planner 에이전트를 Claude Code sub-process로 정의하여 Phase 05 (Phase Workflow)의 토대를 만든다.

## What Changes

- `planner` agent 정의: phase context(CONTEXT.md)를 읽어 실행 가능한 PLAN.md를 생성하는 CC sub-process
- `executor` agent 정의: PLAN.md의 태스크를 순서대로 실행하고 변경 이력을 기록하는 CC sub-process
- `verifier` agent 정의: 구현된 변경사항을 requirements에 대해 검증하고 VERIFICATION.md를 생성하는 CC sub-process
- 세 에이전트의 공통 입출력 계약(artifact contract) 스키마 정의
- 에이전트 정의 파일을 `.claude/agents/` 경로에 배치

## Capabilities

### New Capabilities

- `planner-agent`: phase CONTEXT.md와 requirements를 읽어 atomic task 단위의 PLAN.md를 생성하는 전문 에이전트
- `executor-agent`: PLAN.md를 읽어 task를 순서대로 실행하고 각 task 완료 후 체크포인트를 기록하는 전문 에이전트
- `verifier-agent`: 구현 결과물을 phase requirements 및 UAT 기준과 대조하여 PASS/FAIL 검증 리포트를 생성하는 전문 에이전트
### Modified Capabilities

<!-- 기존 spec-level 요구사항 변경 없음 -->

## Impact

- `.claude/agents/planner.md` (신규): planner agent 정의 (gitignored per current policy)
- `.claude/agents/executor.md` (신규): executor agent 정의
- `.claude/agents/verifier.md` (신규): verifier agent 정의
- `docs/spec/agent-contract.md` (신규): artifact contract 스키마 공식 문서화
- Phase 05 (Phase Workflow)의 `/rg:plan`, `/rg:execute`, `/rg:verify` 커맨드가 이 에이전트들을 호출
