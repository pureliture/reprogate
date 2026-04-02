## ADDED Requirements

### Requirement: Verifier agent validates implementation against requirements and produces VERIFICATION.md
verifier 에이전트는 EXECUTION-LOG.md와 구현된 코드를 phase requirements에 대해 검증하고 PASS/FAIL 결과가 포함된 VERIFICATION.md를 생성해야 한다(SHALL).

#### Scenario: Verification passes all requirements
- **WHEN** 구현이 모든 requirements를 충족하면
- **THEN** verifier는 `status: PASS`와 각 requirement별 검증 근거가 포함된 VERIFICATION.md를 생성해야 한다

#### Scenario: Verification fails one or more requirements
- **WHEN** 구현이 하나 이상의 requirement를 충족하지 못하면
- **THEN** verifier는 `status: FAIL`과 실패한 requirement 목록, 실패 이유를 포함한 VERIFICATION.md를 생성해야 한다

#### Scenario: Verifier does not modify source code
- **WHEN** verifier가 실행되면
- **THEN** 소스 코드나 PLAN.md를 수정해서는 안 된다(SHALL NOT) — VERIFICATION.md 생성만 허용

### Requirement: Verifier includes deviation review in its assessment
verifier는 EXECUTION-LOG.md의 deviation 항목을 검토하고 deviation이 요구사항에 미치는 영향을 VERIFICATION.md에 포함시켜야 한다(SHALL).

#### Scenario: Deviation exists in execution log
- **WHEN** EXECUTION-LOG.md에 deviation 항목이 있으면
- **THEN** verifier는 해당 deviation이 허용 가능한지, requirements를 여전히 충족하는지 평가하여 VERIFICATION.md에 기록해야 한다

### Requirement: Verifier agent is invocable as a Claude Code sub-agent
verifier 에이전트는 `.claude/agents/verifier.md` 파일로 정의되어 Claude Code `Task` tool로 호출 가능해야 한다(SHALL).

#### Scenario: Verifier invoked by orchestrator
- **WHEN** Phase Workflow 커맨드가 verifier를 sub-agent로 호출하면
- **THEN** verifier는 독립적으로 실행되어 VERIFICATION.md를 생성하고 종료해야 한다
