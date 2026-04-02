## 1. Agent Artifact Contract

- [x] 1.1 `docs/spec/agent-contract.md` 생성 — CONTEXT.md → PLAN.md → EXECUTION-LOG.md → VERIFICATION.md 핸드오프 스키마 공식 문서화
- [x] 1.2 PLAN.md 표준 구조 정의 (numbered tasks, verification criteria, expected outputs)
- [x] 1.3 EXECUTION-LOG.md 표준 구조 정의 (task checkpoints, deviations, completed files)
- [x] 1.4 VERIFICATION.md 표준 구조 정의 (status: PASS/FAIL, per-requirement evidence, deviation review)

## 2. Planner Agent

- [x] 2.1 `.claude/agents/planner.md` 생성 — planner agent definition (로컬 전용)
- [x] 2.2 planner 입력 계약 명세: CONTEXT.md 경로, requirements 참조 방법
- [x] 2.3 planner 출력 계약 명세: PLAN.md 표준 포맷 준수 확인
- [x] 2.4 planner가 코드를 수정하지 않는 guardrail 추가

## 3. Executor Agent

- [x] 3.1 `.claude/agents/executor.md` 생성 — executor agent definition (로컬 전용)
- [x] 3.2 executor 입력 계약 명세: PLAN.md 경로
- [x] 3.3 executor 출력 계약 명세: EXECUTION-LOG.md 생성 및 체크포인트 기록
- [x] 3.4 deviation 발생 시 EXECUTION-LOG.md 기록 로직 명세
- [x] 3.5 복구 불가능한 오류 시 중단 및 EXECUTION-LOG.md 기록 명세

## 4. Verifier Agent

- [x] 4.1 `.claude/agents/verifier.md` 생성 — verifier agent definition (로컬 전용)
- [x] 4.2 verifier 입력 계약 명세: EXECUTION-LOG.md + 코드 + requirements
- [x] 4.3 verifier 출력 계약 명세: VERIFICATION.md (PASS/FAIL + per-requirement evidence)
- [x] 4.4 deviation 검토 섹션 포함 명세
- [x] 4.5 verifier가 코드를 수정하지 않는 guardrail 추가

## 5. Tests

- [x] 5.1 `docs/spec/agent-contract.md` 존재 및 필수 섹션 포함 테스트
- [x] 5.2 planner agent 파일 존재 및 입출력 계약 키워드 포함 테스트
- [x] 5.3 executor agent 파일 존재 및 deviation 처리 명세 포함 테스트
- [x] 5.4 verifier agent 파일 존재 및 PASS/FAIL 구조 포함 테스트
