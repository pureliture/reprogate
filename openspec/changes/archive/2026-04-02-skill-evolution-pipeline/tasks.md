## 1. Session Observation Capture

- [x] 1.1 `~/.claude/homunculus/instincts/` 디렉토리 자동 초기화 로직 추가 (첫 실행 시 생성)
- [x] 1.2 instinct YAML 스키마 정의 (`id`, `session_id`, `captured_at`, `observations`, `confidence`, `raw_summary`)
- [x] 1.3 `reprogate_hook_stop.py`에 observation extraction 함수 구현 (LLM-assisted, 비동기)
- [x] 1.4 생성된 instinct YAML 파일을 `~/.claude/homunculus/instincts/<session-id>.yaml`로 저장
- [x] 1.5 Stop hook에서 미평가 instinct 수 카운트 후 알림 메시지 출력
- [x] 1.6 observation 추출 오류 시 세션 종료를 차단하지 않는 예외 처리 추가

## 2. Instinct Quality Gate (/learn-eval)

- [x] 2.1 `.claude/commands/learn-eval.md` 슬래시 커맨드 파일 생성
- [x] 2.2 `~/.claude/homunculus/instincts/`에서 미평가 instinct 목록 조회 로직 구현
- [x] 2.3 instinct 선택 및 대화형 리뷰 플로우 구현 (LLM과 함께 품질 평가)
- [x] 2.4 품질 기준 체크: specificity, 재사용 가능성, 명확한 trigger
- [x] 2.5 `confidence: low` instinct 승격 시 명시적 확인 요청 처리
- [x] 2.6 리뷰 완료 시 instinct YAML에 `reviewed: true`, `promoted: true/false` 마킹

## 3. Prose Skill Storage (instinct-quality-gate에 통합)

- [x] 3.1 `~/.claude/homunculus/evolved/skills/` 디렉토리 자동 초기화 로직 추가
- [x] 3.2 prose skill Markdown 생성 함수 구현 (표준 구조: `# name`, `## Trigger`, `## Pattern`, `## Rationale`)
- [x] 3.3 품질 게이트 통과 후 `~/.claude/homunculus/evolved/skills/<name>.md` 저장
- [x] 3.4 동일 이름 파일 존재 시 덮어쓰기 확인 요청 처리
- [x] 3.5 `/learn-eval` 내 prose skill 목록 조회 기능 추가 (이름·생성일 정렬)

## 4. ADR-012 Verification 항목 완료

- [x] 4.1 `SKILL-EVO-01` 요구사항에 "prose instinct까지" 범위 문서화
- [x] 4.2 v2 backlog에 `reprogate evolve-to-rego` 항목 등록
- [x] 4.3 ADR-012 검증 체크리스트 완료 처리

## 5. Tests

- [x] 5.1 observation extraction 함수 단위 테스트 (`scripts/tests/`)
- [x] 5.2 instinct YAML 스키마 유효성 검증 테스트
- [x] 5.3 prose skill 저장 경로 및 구조 테스트
- [x] 5.4 `/learn-eval` quality gate 로직 테스트 (통과/실패/저신뢰도 케이스)
