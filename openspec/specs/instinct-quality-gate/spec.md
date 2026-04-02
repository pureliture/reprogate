## ADDED Requirements

### Requirement: /learn-eval command lists pending instincts
`/learn-eval` 커맨드 실행 시 시스템은 `~/.claude/homunculus/instincts/`에서 미평가(unreviewed) instinct 목록을 표시해야 한다(SHALL).

#### Scenario: Pending instincts exist
- **WHEN** 개발자가 `/learn-eval`을 실행하고 미평가 instinct가 있으면
- **THEN** 시스템은 instinct 목록(파일명, 캡처 시각, confidence, observations 수)을 표시하고 리뷰할 항목 선택을 요청해야 한다

#### Scenario: No pending instincts
- **WHEN** 개발자가 `/learn-eval`을 실행하고 미평가 instinct가 없으면
- **THEN** 시스템은 "리뷰할 instinct가 없습니다." 메시지를 출력하고 종료해야 한다

### Requirement: /learn-eval evaluates instinct quality interactively
선택된 instinct에 대해 시스템은 LLM과 함께 대화형으로 품질을 평가해야 한다(SHALL).

#### Scenario: Instinct passes quality gate
- **WHEN** instinct가 품질 기준(충분한 specificity, 재사용 가능성, 명확한 trigger)을 충족하면
- **THEN** 시스템은 prose skill 저장을 진행하고 instinct를 `reviewed: true`로 마킹해야 한다

#### Scenario: Instinct fails quality gate
- **WHEN** instinct가 품질 기준을 충족하지 못하면
- **THEN** 시스템은 실패 이유를 설명하고 instinct를 `reviewed: true, promoted: false`로 마킹하되 prose skill을 생성해서는 안 된다(SHALL NOT)

### Requirement: /learn-eval does not promote low-confidence instincts without explicit confirmation
`confidence: low` instinct는 개발자의 명시적 확인 없이 자동 승격되어서는 안 된다(SHALL NOT).

#### Scenario: Low confidence instinct promotion attempt
- **WHEN** `confidence: low` instinct가 quality gate를 통과하려 할 때
- **THEN** 시스템은 "신뢰도가 낮습니다. 그래도 승격하시겠습니까?" 확인을 요청해야 한다

### Requirement: Prose skill is saved to standard path after promotion
품질 게이트를 통과한 instinct는 `~/.claude/homunculus/evolved/skills/<name>.md` 경로에 prose skill Markdown으로 저장되어야 한다(SHALL).

#### Scenario: Successful prose skill creation
- **WHEN** instinct가 `/learn-eval` 품질 게이트를 통과하면
- **THEN** 시스템은 `~/.claude/homunculus/evolved/skills/<suggested_skill_name>.md` 파일을 생성해야 한다

#### Scenario: Name conflict on save
- **WHEN** 동일한 `suggested_skill_name`을 가진 prose skill이 이미 존재하면
- **THEN** 시스템은 기존 파일을 덮어쓰기 전에 개발자에게 확인을 요청해야 한다

### Requirement: Prose skill follows standard Markdown structure
저장된 prose skill은 정해진 헤더 구조(`# <name>`, `## Trigger`, `## Pattern`, `## Rationale`)를 따라야 한다(SHALL).

#### Scenario: Prose skill structure validation
- **WHEN** prose skill이 생성될 때
- **THEN** 파일은 `# <name>`, `## Trigger`, `## Pattern`, `## Rationale` 섹션을 포함해야 한다

### Requirement: Prose skill directory is auto-initialized
`~/.claude/homunculus/evolved/skills/` 디렉토리가 없으면 시스템이 자동으로 생성해야 한다(SHALL).

#### Scenario: First-time prose skill save
- **WHEN** 처음으로 prose skill을 저장하고 디렉토리가 존재하지 않으면
- **THEN** 시스템은 필요한 디렉토리를 자동 생성한 후 파일을 저장해야 한다

### Requirement: Prose skills are listable via /learn-eval
개발자는 `/learn-eval`로 저장된 prose skill 목록을 조회할 수 있어야 한다(SHALL).

#### Scenario: List stored prose skills
- **WHEN** 개발자가 prose skill 목록을 요청하면
- **THEN** 시스템은 `~/.claude/homunculus/evolved/skills/`의 모든 파일을 이름·생성일 기준으로 정렬하여 표시해야 한다
