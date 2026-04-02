## ADDED Requirements

### Requirement: /rg:plan invokes planner agent via prompt embedding
시스템은 `/rg:plan <phase-name>` 실행 시 `.claude/agents/planner.md`를 읽어 컨텍스트에 임베딩하고, planner agent 역할로 `.rg/<phase-name>/CONTEXT.md`를 읽어 PLAN.md를 생성해야 한다(SHALL).

#### Scenario: Developer runs /rg:plan
- **GIVEN** `.rg/my-feature/CONTEXT.md`가 존재할 때
- **WHEN** 개발자가 `/rg:plan my-feature`를 실행하면
- **THEN** planner agent 규칙에 따라 `.rg/my-feature/PLAN.md`를 생성해야 한다
- **THEN** PLAN.md는 `docs/spec/agent-contract.md`의 PLAN.md 스키마를 따라야 한다

### Requirement: /rg:plan fails if CONTEXT.md is missing
CONTEXT.md가 없으면 `/rg:plan`은 실행을 중단하고 `/rg:discuss`를 먼저 실행하도록 안내해야 한다(SHALL).

#### Scenario: Missing CONTEXT.md
- **WHEN** `.rg/my-feature/CONTEXT.md`가 없을 때 `/rg:plan my-feature`를 실행하면
- **THEN** "CONTEXT.md not found. Run /rg:discuss my-feature first." 메시지를 표시해야 한다

### Requirement: /rg:plan planner guardrails are enforced
planner agent의 "코드 수정 금지" guardrail이 커맨드에서 명시적으로 강조되어야 한다(SHALL).

#### Scenario: Planner stays in planning mode
- **WHEN** planner가 실행되면
- **THEN** 코드 파일을 수정하거나 생성하지 않아야 한다
