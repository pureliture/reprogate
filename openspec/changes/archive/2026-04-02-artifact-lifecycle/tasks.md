## 1. Phase Summary Schema

- [x] 1.1 `records/summaries/` 디렉토리 생성 및 `.gitkeep` 추가 — tracked 디렉토리
- [x] 1.2 `docs/spec/phase-summary-schema.md` 생성 — summary 스키마 및 컨벤션 문서화
- [x] 1.3 `.claude/commands/.gitignore`에 `rg-summary.md`, `rg-health.md` 예외 추가

## 2. /rg:summary Command

- [x] 2.1 `.claude/commands/rg-summary.md` 생성 — summary 커맨드 정의
- [x] 2.2 `$ARGUMENTS`로 phase 이름 받는 로직: 없으면 `.rg/` 아래 완료된 phase 목록 표시
- [x] 2.3 VERIFICATION.md 존재 확인: 없으면 `/rg:verify` 실행 안내
- [x] 2.4 CONTEXT.md + VERIFICATION.md + EXECUTION-LOG.md 읽기 및 summary 생성 로직
- [x] 2.5 `records/summaries/<YYYY-MM-DD>-<phase>.md` 생성 로직 (today's date 사용)
- [x] 2.6 PASS/FAIL result를 상단에 포함하는 schema 준수 확인

## 3. /rg:health Command

- [x] 3.1 `.claude/commands/rg-health.md` 생성 — health 커맨드 정의
- [x] 3.2 hooks 상태 체크: `scripts/hooks/*.py` 파일 목록 및 수
- [x] 3.3 skills 상태 체크: `skills/` 디렉토리 항목 수
- [x] 3.4 gate failures 체크: `records/gate-failures/` 파일 수 (최근 5개)
- [x] 3.5 ADR 체크: `records/adr/` 파일 수 및 최신 ADR 번호
- [x] 3.6 `/rg:*` 커맨드 존재 체크: 6개 커맨드 (discuss, plan, execute, verify, summary, health)
- [x] 3.7 읽기 전용 보장: 파일 생성/수정 없음 명시
- [x] 3.8 면책 문구 포함: "파일 존재 확인만 수행"

## 4. Tests

- [x] 4.1 `records/summaries/` 디렉토리 존재 및 tracked 테스트
- [x] 4.2 `docs/spec/phase-summary-schema.md` 존재 및 필수 섹션 테스트
- [x] 4.3 `rg-summary.md` 커맨드 존재 및 VERIFICATION.md prerequisite 체크 테스트
- [x] 4.4 `rg-health.md` 커맨드 존재 및 read-only/면책 문구 포함 테스트
- [x] 4.5 `.claude/commands/.gitignore` 업데이트 확인 (rg-summary, rg-health 예외)
