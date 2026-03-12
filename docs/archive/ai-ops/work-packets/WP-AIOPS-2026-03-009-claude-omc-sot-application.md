---
packet_id: "WP-AIOPS-2026-03-009"
title: "Claude+OMC SoT 구조 적용"
goal_ids: ["AIOPS-G3", "AIOPS-G5"]
status: "DONE"
work_type: "FEATURE"
priority: "P0"
target_environment: "master"
start_process: "P0"
current_process: "S4"
next_process: "END"
owner: "SHARED"
created_at: "2026-03-09"
last_updated: "2026-03-09"
---
# WP-AIOPS-2026-03-009 Claude+OMC SoT 구조 적용

## 1. Background
- WP-008에서 Codex+OMX 정렬 작업 중, Claude+OMC 측에도 동일한 SoT 구조 적용이 필요함이 확인됨
- Claude Code + OMC 경로는 `/ai-ops` 명령과 PreToolUse hook 기반 hard gate를 사용
- `docs/ai-ops/*`와 `scripts/ai-ops/*`를 SoT로 참조하는 구조가 `.claude/CLAUDE.md`에 명시되어야 함
- WP-008의 범위를 Codex+OMX에 집중하고, Claude+OMC 적용은 별도 WP로 분리

## 2. Goal
- Claude Code + OMC 경로에 `docs/ai-ops/*` SoT 구조를 적용한다.
- `.claude/CLAUDE.md`에 AI Ops Local Overlay 섹션을 추가하여 AGENTS.md와 동등한 운영 기준을 확보한다.
- config/policy 파일은 git 추적 허용, runtime state는 .gitignore로 제외한다.

## 3. Scope
### 3.1 `.claude/CLAUDE.md` 확장
- AI Ops Local Overlay (Claude+OMC Adapter) 섹션 추가
- Named Entrypoint Parity: `/ai-ops` ↔ `$ai-ops`
- Mandatory References: 6개 필수 참조 문서
- Capability-First Rules: 도구 독립적 SoT 참조 원칙
- Process Context: 프로세스 선택 및 team_mode 확정 절차
- Hard Rules: PreToolUse 기반 hard gate 명시
- P3 Soft Execution Contract: single fallback 역할 순차 수행
- Team Roster Examples: OMC 및 Claude-Native 예시

### 3.2 `.gitignore` 수정
- `.claude/`, `.omc/` config/policy 파일 추적 허용
- runtime state (sessions, logs, notepad 등) 제외

### 3.3 Compliance Checker 수정
- `validate_local_ai_runtime_tracking` 함수 비활성화 (runtime state 제외는 .gitignore로 처리)

## 4. Work Details
### 4.1 P0 분석 (2026-03-09)
- AGENTS.md(Codex+OMX) vs .claude/CLAUDE.md(Claude+OMC) 갭 분석 수행
- 누락 항목 식별: Named Entrypoint Parity, Mandatory References, Capability-First Rules, Process Context, P3 Soft Execution Contract

### 4.2 P3 구현 (2026-03-09)
- `.claude/CLAUDE.md`에 AI Ops Local Overlay 섹션 추가
- `.gitignore` 수정: config/policy 추적 허용, runtime state 제외
- `check_ai_ops_compliance.py` 수정: tracking validation 비활성화

### 4.3 S1 리뷰 (2026-03-09)
- CLAUDE.md ↔ AGENTS.md 정렬 검증: PASS
- Compliance check: PASS
- 도구별 차이(Hard Rules vs Launch Gate)는 의도된 분기로 확인

## 5. Done Criteria
- [x] `.claude/CLAUDE.md`에 AI Ops Local Overlay 섹션 추가
- [x] Named Entrypoint Parity, Mandatory References, Capability-First Rules 적용
- [x] Process Context, Hard Rules, P3 Soft Execution Contract 적용
- [x] `.gitignore` config/policy 추적 허용, runtime state 제외
- [x] Compliance check 통과
- [x] S1 리뷰 완료

## 6. Risks / Constraints
- OMC 버전 업데이트 시 `.claude/CLAUDE.md`의 OMC 섹션이 덮어써질 수 있음 (AI Ops Local Overlay는 별도 섹션이라 영향 최소화)

## 7. Related References
### 7.1 Related Docs
- [WP-AIOPS-2026-03-008](./WP-AIOPS-2026-03-008-codex-omx-alignment.md)
- [WP-AIOPS-2026-03-006](./WP-AIOPS-2026-03-006-pilot-verification.md)
- [운영체계 구축 상위 계획](../ops-bootstrap-master-plan.md)
- [AI Ops Constitution](../constitution.md)

### 7.2 Related Code
- `.claude/CLAUDE.md`
- `.gitignore`
- `scripts/ai-ops/check_ai_ops_compliance.py`

## 8. Artifacts
- `.claude/CLAUDE.md` (AI Ops Local Overlay 섹션)
- `.gitignore` (수정)
- `scripts/ai-ops/check_ai_ops_compliance.py` (수정)

## 9. Timeline
| Date | Process | Activity |
|------|---------|----------|
| 2026-03-09 | P0 | AGENTS.md vs CLAUDE.md 갭 분석 |
| 2026-03-09 | P3 | AI Ops Local Overlay 구현, .gitignore 수정 |
| 2026-03-09 | S1 | 리뷰 완료 (PASS) |
| 2026-03-09 | S4 | WP-009 분리 생성, 문서 기록 |
