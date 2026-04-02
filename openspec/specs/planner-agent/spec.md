## ADDED Requirements

### Requirement: Planner agent reads CONTEXT.md and requirements to produce PLAN.md
planner 에이전트는 phase CONTEXT.md와 관련 requirements를 읽어 실행 가능한 태스크 목록이 포함된 PLAN.md를 생성해야 한다(SHALL).

#### Scenario: Planner produces a structured PLAN.md
- **WHEN** planner 에이전트가 CONTEXT.md를 입력으로 실행되면
- **THEN** numbered atomic tasks, 각 task의 검증 기준, 예상 산출물이 포함된 PLAN.md를 출력해야 한다

#### Scenario: Planner does not modify any code
- **WHEN** planner 에이전트가 실행되면
- **THEN** 소스 코드, 설정 파일, 기존 문서를 수정해서는 안 된다(SHALL NOT) — PLAN.md 생성만 허용

### Requirement: Planner agent is invocable as a Claude Code sub-agent
planner 에이전트는 `.claude/agents/planner.md` 파일로 정의되어 Claude Code `Task` tool로 호출 가능해야 한다(SHALL).

#### Scenario: Planner invoked by orchestrator
- **WHEN** Phase Workflow 커맨드가 planner를 sub-agent로 호출하면
- **THEN** planner는 독립적으로 실행되어 PLAN.md를 생성하고 종료해야 한다
