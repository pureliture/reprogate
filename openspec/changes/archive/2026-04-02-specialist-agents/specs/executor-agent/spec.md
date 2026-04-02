## ADDED Requirements

### Requirement: Executor agent reads PLAN.md and implements tasks in order
executor 에이전트는 PLAN.md를 읽어 태스크를 순서대로 실행하고 각 태스크 완료 후 EXECUTION-LOG.md에 체크포인트를 기록해야 한다(SHALL).

#### Scenario: Executor completes all tasks and logs them
- **WHEN** executor가 PLAN.md를 입력으로 실행되면
- **THEN** 모든 태스크를 순서대로 구현하고 `EXECUTION-LOG.md`에 각 태스크의 완료 상태와 변경 파일 목록을 기록해야 한다

#### Scenario: Executor stops on unrecoverable error
- **WHEN** 구현 중 복구 불가능한 오류(예: 의존성 누락)가 발생하면
- **THEN** executor는 오류를 EXECUTION-LOG.md에 기록하고 이후 태스크 실행을 중단해야 한다(SHALL)

### Requirement: Executor does not rewrite the plan
executor 에이전트는 PLAN.md를 수정해서는 안 된다(SHALL NOT). 계획 변경이 필요하면 EXECUTION-LOG.md에 deviation으로 기록하고 planner를 재호출하도록 요청해야 한다.

#### Scenario: Executor encounters plan deviation
- **WHEN** executor가 계획된 방식이 아닌 다른 접근법을 선택할 때
- **THEN** PLAN.md는 그대로 유지하고 EXECUTION-LOG.md의 deviation 섹션에 이유와 실제 선택을 기록해야 한다

### Requirement: Executor agent is invocable as a Claude Code sub-agent
executor 에이전트는 `.claude/agents/executor.md` 파일로 정의되어 Claude Code `Task` tool로 호출 가능해야 한다(SHALL).

#### Scenario: Executor invoked by orchestrator
- **WHEN** Phase Workflow 커맨드가 executor를 sub-agent로 호출하면
- **THEN** executor는 독립적으로 PLAN.md를 읽어 실행하고 EXECUTION-LOG.md를 남긴 후 종료해야 한다
