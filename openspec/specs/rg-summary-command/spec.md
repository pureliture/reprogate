## ADDED Requirements

### Requirement: /rg:summary creates tracked phase summary from artifact packet
시스템은 `/rg:summary <phase-name>` 실행 시 `.rg/<phase-name>/`의 artifact들을 읽어 `records/summaries/<YYYY-MM-DD>-<phase-name>.md`를 생성해야 한다(SHALL).

#### Scenario: Developer summarizes completed phase
- **GIVEN** `.rg/my-feature/VERIFICATION.md`가 PASS 또는 FAIL로 존재할 때
- **WHEN** 개발자가 `/rg:summary my-feature`를 실행하면
- **THEN** `records/summaries/<today>-my-feature.md`를 `phase-summary-schema` 스키마에 따라 생성해야 한다
- **THEN** summary 파일은 레포에 커밋 가능한 tracked 파일이어야 한다

### Requirement: /rg:summary fails if VERIFICATION.md is missing
VERIFICATION.md가 없으면 `/rg:summary`는 실행을 중단하고 `/rg:verify`를 먼저 실행하도록 안내해야 한다(SHALL).

#### Scenario: Missing VERIFICATION.md
- **WHEN** `.rg/my-feature/VERIFICATION.md`가 없을 때 `/rg:summary my-feature`를 실행하면
- **THEN** "VERIFICATION.md not found. Run /rg:verify my-feature first." 메시지를 표시해야 한다

### Requirement: /rg:summary includes PASS/FAIL result prominently
생성된 summary는 phase 결과(PASS/FAIL)를 상단에 명시해야 한다(SHALL).

#### Scenario: Summary shows result at top
- **WHEN** summary가 생성되면
- **THEN** `**Result:** PASS ✅` 또는 `**Result:** FAIL ❌`가 상단 메타데이터에 포함되어야 한다
