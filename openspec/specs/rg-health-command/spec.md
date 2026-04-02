## ADDED Requirements

### Requirement: /rg:health reports harness component status
시스템은 `/rg:health` 실행 시 하네스 컴포넌트(hooks, skills, gate failures, observations, ADRs, commands)의 파일 기반 상태를 점검하고 요약 리포트를 출력해야 한다(SHALL).

#### Scenario: Developer checks harness health
- **WHEN** 개발자가 `/rg:health`를 실행하면
- **THEN** hooks, skills, gate failures, ADRs, `/rg:*` 커맨드 각각의 상태를 확인하여 대시보드 형태로 출력해야 한다

### Requirement: /rg:health is read-only
`/rg:health`는 어떤 파일도 생성, 수정, 삭제해서는 안 된다(SHALL NOT).

#### Scenario: Health check has no side effects
- **WHEN** `/rg:health`가 실행되면
- **THEN** 레포나 파일시스템에 어떤 변경도 발생하지 않아야 한다

### Requirement: /rg:health explicitly notes file-existence-only caveat
리포트는 "파일 존재 확인 (동작 보장 아님)" 면책 문구를 포함해야 한다(SHALL).

#### Scenario: Health report shows caveat
- **WHEN** health 리포트가 출력되면
- **THEN** 파일 존재만 확인하며 실제 동작을 보장하지 않음을 명시해야 한다
