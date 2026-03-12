---
packet_id: "WP-AIOPS-2026-03-007"
title: "AI 도구 산출물 원격/로컬 분리 및 포팅 경계 정립"
goal_ids: ["AIOPS-G3", "AIOPS-G5"]
status: "DONE"
work_type: "REFACTOR"
priority: "P0"
target_environment: "master+wafful4"
start_process: "P0"
current_process: "S4"
next_process: "END"
owner: "SHARED"
created_at: "2026-03-08"
last_updated: "2026-03-08"
---
# WP-AIOPS-2026-03-007 AI 도구 산출물 원격/로컬 분리 및 포팅 경계 정립

## 1. Background
- `master`는 `.claude/.codex/.omc`를 로컬 전용으로 관리하지만 `wafful4(java8)`는 일부 `.claude/.codex` 파일이 원격 추적되어 기준이 불일치한다.
- ai-ops를 프로젝트에서 분리/공개 레포로 전환하려면, "프레임워크 공통 자산"과 "프로젝트/로컬 전용 자산"의 경계를 먼저 고정해야 한다.
- 포팅 자동화 지시(`ai-ops를 현재 프로젝트에 포팅`)가 가능하려면 ai-ops 자체는 프로젝트 무방해야 하며, 프로젝트 특화 값은 타겟 프로젝트에만 남아야 한다.

## 2. Goal
- AI 도구 파일을 `원격 관리 대상`과 `로컬 전용`으로 명확히 분리한다.
- `master`와 `wafful4(java8)`의 기준을 동일 정책으로 정렬한다.
- ai-ops 분리 이전에 포팅 가능한 경계(Framework vs Project Adapter)를 문서/가드로 고정한다.

## 3. Scope
### 3.1 정책/문서
- 원격/로컬 분리 정책 문서 추가
- ai-ops 프레임워크와 타겟 프로젝트 어댑터의 경계 문서화

### 3.2 규칙/가드
- `check_ai_ops_compliance.py`에 숨김 AI 도구 디렉토리 커밋 금지 규칙 추가
- 관련 AGENTS/명령 문서와 동기화

### 3.3 저장소 정합성
- `wafful4(java8)`에서 추적 중인 `.claude/.codex`를 비추적으로 전환
- 정책성 내용은 `docs/branch-specific/` 하위의 도구 무방 문서로 이관

## 4. Out of Scope
- ai-ops를 별도 공개 레포로 실제 분리/이전
- 포팅 자동화 스크립트의 완전 구현

## 5. Done Criteria
- [x] 원격/로컬/포팅 경계 정책 문서가 생성됨
- [x] `master` compliance가 `.claude/.codex/.omc` staged 변경을 하드 차단함
- [x] `wafful4(java8)`의 `.claude/.codex` 추적 파일이 인덱스에서 제거됨
- [x] `wafful4(java8)` 정책성 가이드가 `docs/branch-specific/ai-tooling/`로 이관됨
- [x] `master`/`wafful4` 모두 로컬 전용 숨김 디렉토리 기준이 일치함

## 6. Risks / Constraints
- 기존 로컬 실행 환경은 숨김 디렉토리를 계속 사용하므로 이관 중 경로 혼동 위험이 있다.
- java8 워크스페이스의 빌드 가드 동작은 유지되어야 한다.

## 7. Related References
### 7.1 Related Docs
- [ops-bootstrap-master-plan.md](../ops-bootstrap-master-plan.md)
- [WP-AIOPS-2026-03-005](./WP-AIOPS-2026-03-005-process-based-collaboration.md)

### 7.2 Related Code
- `scripts/ai-ops/check_ai_ops_compliance.py`
- `AGENTS.md`

## 8. Process Plan
- P0: master/java8 추적 현황 및 ignore 규칙 인벤토리
- P1: 분리 정책 및 경계 설계
- P3: 규칙/문서/저장소 정합성 반영
- S1: 두 워크스페이스 정합성 점검
- S4: 변경 이력 및 후속 분리 작업 연결

## 9. Execution Notes
### P0 Findings (2026-03-08)
- master: `.gitignore`에서 `.claude/.codex/.omc` 로컬 전용 제외
- java8: `.claude/.codex` 추적 파일 존재 (`CLAUDE.md`, `settings.json`, `rules.md` 등)
- 결론: 로컬 실행 스펙 원격 추적 기준 불일치 확인

### P1 Design (2026-03-08)
- 정책 결론: 숨김 도구 디렉토리는 Local-only, 정책/지침은 비숨김 경로(`docs/`, `scripts/`)에서 원격 관리
- 경계 모델: Framework(ai-ops) / Project Adapter(프로젝트 문서) / Local Runtime(숨김 디렉토리)
- ADR 반영: `ADR-AIOPS-004`

### P3 Implementation (2026-03-08)
- master 반영:
  - `check_ai_ops_compliance.py`에 `.claude/.codex/.omc` staged 변경 하드 차단 추가
  - `docs/ai-ops/portability/ai-tool-artifact-boundary.md` 추가
  - `AGENTS.md`, `commands/ai-ops.md`, `process-enforcement-matrix.md` 동기화
- java8 반영:
  - `.gitignore`에 `.claude/`, `.codex/` 추가
  - `.claude/.codex` 추적 해제(`git rm --cached`)
  - 정책 문서 이관: `docs/branch-specific/ai-tooling/`
  - 로컬 스펙 동기화 스크립트 추가: `scripts/ai-tooling/sync-local-ai-specs.sh`

### S1 Verification (2026-03-08)
- master compliance(`--mode working_tree`) 통과
- java8에서 `.claude/.codex` 추적 파일 제거 상태 확인
- java8 로컬 스펙 동기화 스크립트 실행 확인

## 10. Deliverables
- 분리 정책 문서
- 하드 가드 코드 반영
- java8 저장소 정리 커밋

## 11. Review Notes
- 정책 문서가 "프로젝트 무방 프레임워크" 목표와 충돌하지 않는지 확인 필요

## 12. Decisions
| 결정 | 선택 | 이유 |
|------|------|------|
| 숨김 도구 디렉토리 정책 | 원격 비추적(Local-only) | master와 기준 일치 + 포팅/분리 단순화 |
| 정책 공유 위치 | `docs/...` 비숨김 경로 | 툴 런타임 파일과 정책 문서 분리 |

## 13. Follow-ups
- ai-ops 공개 레포 분리 시 공통 자산/어댑터 자산 매핑표를 기준으로 이관

## 14. Timeline
- [2026-03-08] WP 생성 및 P0 현황 확정
- [2026-03-08] P1 설계: Remote-managed / Local-only / Project Adapter 경계 고정
- [2026-03-08] P3 구현: master 가드 + java8 추적 해제/문서 이관 반영
- [2026-03-08] S1 검증 후 S4 완료: WP DONE 전이
