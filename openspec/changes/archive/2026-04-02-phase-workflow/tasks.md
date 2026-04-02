## 1. Phase Artifact Packet

- [x] 1.1 `.rg/` 디렉토리를 `.gitignore`에 추가 — phase artifact packet은 gitignored
- [x] 1.2 `docs/spec/agent-contract.md`에 "Phase Workflow" 섹션 추가 — `.rg/<phase-name>/` 경로 컨벤션 및 커맨드 순서 기술 (별도 파일 신규 생성 없이 기존 문서 확장)
- [x] 1.3 ADR-017 업데이트 반영: `.gitignore`에 `/rg:*` 커맨드 파일 예외 항목 추가 (이미 완료)

## 2. /rg:discuss Command

- [x] 2.1 `.claude/commands/rg-discuss.md` 생성 — discuss 커맨드 정의
- [x] 2.2 `$ARGUMENTS`로 phase 이름 받는 로직: 없으면 이름 입력 안내
- [x] 2.3 대화형 질문 흐름: Goal → Requirements → Constraints → References 순서
- [x] 2.4 CONTEXT.md 생성 로직: `agent-contract.md` 스키마 준수
- [x] 2.5 기존 CONTEXT.md 존재 시 덮어쓰기 확인 프롬프트

## 3. /rg:plan Command

- [x] 3.1 `.claude/commands/rg-plan.md` 생성 — plan 커맨드 정의
- [x] 3.2 `.claude/agents/planner.md` 읽기 및 임베딩 패턴 구현
- [x] 3.3 CONTEXT.md 존재 확인: 없으면 `/rg:discuss` 실행 안내
- [x] 3.4 planner guardrail 강조: "코드 수정 금지" 명시

## 4. /rg:execute Command

- [x] 4.1 `.claude/commands/rg-execute.md` 생성 — execute 커맨드 정의
- [x] 4.2 `.claude/agents/executor.md` 읽기 및 임베딩 패턴 구현
- [x] 4.3 PLAN.md 존재 확인: 없으면 `/rg:plan` 실행 안내
- [x] 4.4 deviation 기록 guardrail 강조: "deviation은 EXECUTION-LOG.md에 기록" 명시
- [x] 4.5 PLAN.md 재작성 금지 guardrail 명시

## 5. /rg:verify Command

- [x] 5.1 `.claude/commands/rg-verify.md` 생성 — verify 커맨드 정의
- [x] 5.2 `.claude/agents/verifier.md` 읽기 및 임베딩 패턴 구현
- [x] 5.3 EXECUTION-LOG.md 존재 확인: 없으면 `/rg:execute` 실행 안내
- [x] 5.4 verifier guardrail 강조: "코드 수정 금지" 명시
- [x] 5.5 VERIFICATION.md 생성 후 결과 요약 출력 (PASS/FAIL + blockers 수)

## 6. Tests

- [x] 6.1 `.rg/` gitignore 추가 테스트
- [x] 6.2 4개 커맨드 파일 존재 및 필수 키워드 포함 테스트 (rg-discuss, rg-plan, rg-execute, rg-verify)
- [x] 6.3 각 커맨드가 해당 agent 파일 임베딩 패턴 포함 테스트
- [x] 6.4 각 커맨드가 prerequisite 체크 패턴 포함 테스트 (CONTEXT.md/PLAN.md/EXECUTION-LOG.md)
