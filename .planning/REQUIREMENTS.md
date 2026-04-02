# Requirements: ReproGate Delivery Harness

**Defined:** 2026-04-02
**Core Value:** ECC와 GSD의 핵심 기제를 조합해, 1인 개발자가 Claude Code 위에서 재현 가능하고 기록 기반의 AI 보조 개발을 할 수 있게 한다.

---

## v1 Requirements

### Foundation — Phase 1 기술 기반 (완료)

- [x] **FOUND-01**: `reprogate` CLI 통합 진입점 (`scripts/cli.py`) — create, check, validate
- [x] **FOUND-02**: 작업 기록(ADR/RFC) 생성·시퀀셜 ID 부여 (`scripts/create_record.py`)
- [x] **FOUND-03**: OPA/Rego 기반 gatekeeper (`scripts/gatekeeper.py` + `scripts/opa_wrapper.py`)
- [x] **FOUND-04**: Skill 정책 구조 (`skills/*/rules.rego` + `guidelines.md`) — 4개 skill 운영 중
- [x] **FOUND-05**: pre-commit hook으로 gatekeeper 자동 실행 (`.githooks/pre-commit`)

### INIT — 하네스 설치 및 활성화 (ADR-013, ADR-015)

- [ ] **INIT-01**: `reprogate init`이 `.claude/settings.json`에 hook 설정을 주입하고 `.claude/session-data/` 디렉토리를 생성한다.
- [ ] **INIT-02**: `REPROGATE_DISABLED=1` 환경 변수로 hook layer를 임시 비활성화할 수 있다.
- [ ] **INIT-03**: `reprogate disable`이 `.claude/settings.json`에서 hook 설정을 제거한다.
- [ ] **INIT-04**: `reprogate.yaml`의 `record_triggers` 경로 패턴 기반으로 레코드 요구 여부를 판단한다 (ADR-014).
- [ ] **INIT-05**: `generate.py` 스키마 불일치 해소 — `init.py` 출력 스키마와 정렬 (Asset Inventory blocker).
- [ ] **INIT-06**: `AGENTS.md.j2`·`CLAUDE.md.j2` 템플릿의 구버전 정체성("compiler/gatekeeper") 문구를 harness 정체성으로 교체.

### HOOK — Layer 1: 하네스 코어 (ECC 방식, ADR-011, ADR-013)

- [ ] **HOOK-01**: hook 인프라 — `REPROGATE_HOOK_PROFILE=minimal|standard|strict` 프로파일 게이팅. 모든 hook이 이 프로파일을 준수한다.
- [ ] **HOOK-02**: SessionStart hook — `.claude/session-data/current-session.json` 초기화 (프로젝트 로컬).
- [ ] **HOOK-03**: Stop hook — 세션 요약을 `.claude/session-data/`에 저장; session observation YAML 초안 생성.
- [ ] **HOOK-04**: PreCompact hook — `.claude/session-data/pre-compact-state.json` 저장.
- [ ] **HOOK-05**: PreToolUse hook — governance capture (standard 프로파일 이상에서 활성). OPA 평가는 `git commit` 시만 hard gate; 실행 중은 advisory.
- [ ] **HOOK-06**: PostToolUseFailure hook — gate 실패를 `records/gate-failures/`에 자동 기록.

### SKILL-EVO — 스킬 진화 (ECC 방식, ADR-012)

- [ ] **SKILL-EVO-01**: Stop hook에서 session observation → instinct YAML 초안 자동 생성.
- [ ] **SKILL-EVO-02**: `/rg:learn-eval` 커맨드 — instinct 품질 게이트 (Save / Improve / Absorb / Drop 판정).
- [ ] **SKILL-EVO-03**: `/rg:evolve` 커맨드 — instinct 클러스터링 및 prose skill 초안 생성.
- [ ] **SKILL-EVO-04**: prose skill → `.rego` 변환은 개발자가 수동 작성 (v1 범위; 자동 변환은 v2).

### PHASE — Layer 2: Phase 플로우 (GSD 방식)

- [ ] **PHASE-01**: `/rg:discuss-phase N` — 인터랙티브 논의로 `CONTEXT.md` 생성.
- [ ] **PHASE-02**: `/rg:plan-phase N` — `gsd-planner` 스폰 → `{N}-{M}-PLAN.md` 생성. `must_haves` frontmatter 필수 (truths / artifacts / key_links).
- [ ] **PHASE-03**: `/rg:execute-phase N` — `gsd-executor` 스폰 → `{N}-{M}-SUMMARY.md` 생성. 순차 실행 (solo dev, worktree 불필요).
- [ ] **PHASE-04**: `/rg:verify-phase N` — `gsd-verifier` 스폰 → `VERIFICATION.md` 생성. Goal-backward 검증: must_haves 기준.
- [ ] **PHASE-05**: `/rg:next` — STATE.md 기반 상태 감지로 다음 단계 자동 라우팅.
- [ ] **PHASE-06**: phase artifact packet 구조 — `.planning/phases/{NN}-{slug}/` 내 CONTEXT + PLAN(s) + SUMMARY(s) + VERIFICATION.

### AGENT — 전문 에이전트 (GSD 방식, MVP 3종)

- [ ] **AGENT-01**: `gsd-executor` — 계획 실행, atomic commit, deviation 처리.
- [ ] **AGENT-02**: `gsd-verifier` — goal-backward 검증, VERIFICATION.md 작성.
- [ ] **AGENT-03**: `gsd-planner` — 태스크 분해, must_haves 도출, PLAN.md 작성.

### LIFECYCLE — Layer 3: ReproGate 고유 아티팩트 라이프사이클

- [ ] **LIFECYCLE-01**: `/rg:phase-summary` — 완료된 phase 산출물 요약·공유 문서 생성 (report/share).
- [ ] **LIFECYCLE-02**: `/rg:harness-check` — 하네스 상태 점검 (hook 활성화 여부, skill 정책 유효성, 미해결 gate 실패 목록) (operate/maintain).

---

## v2 Requirements (Deferred)

### 스킬 진화 자동화
- **SKILL-EVO-AUTO-01**: `reprogate evolve-to-rego` — prose instinct에서 `.rego` 초안 자동 생성 (ADR-012 v2 defer).

### 가시성
- **VIS-01**: 터미널 기반 HUD — gate 상태·phase 진행 실시간 표시 (Textual).

### 통합
- **INTEG-01**: MCP 서버 — `records/`·`skills/` 를 AI 에이전트에 리소스로 노출.
- **INTEG-02**: `notesmd-cli` 심화 통합 — `reprogate search` 커맨드가 notesmd-cli를 백엔드로 사용.

### 팀 확장
- **SCALE-01**: 팀 단위 Skill 공유 및 원격 정책 동기화.

---

## Out of Scope

| Feature | Reason |
|---------|--------|
| OMC | ADR-009 — 현재 참조 범위 제외 |
| 서버 측 중앙 상태 추적 | 로컬·Git 기반 상태만 허용 |
| 정의된 스크립트 외 임의 코드 실행 | 하네스 범위 외 |
| Worktree 기반 병렬 실행 | 팀 기능 — solo dev 불필요 |
| gsd-nyquist-auditor, gsd-ui-auditor 등 20+ GSD 에이전트 | 범용 도구 — ReproGate MVP 3종 에이전트로 충분 |
| ECC2 Rust daemon | 너무 무거움; `risk_score` 개념만 차용 |

---

## Traceability

| REQ-ID | Phase | Status |
|--------|-------|--------|
| FOUND-01 ~ FOUND-05 | Phase 1 | Complete |
| INIT-01 ~ INIT-06 | Phase 2 | Pending |
| HOOK-01 ~ HOOK-06 | Phase 2 | Pending |
| SKILL-EVO-01 ~ SKILL-EVO-04 | Phase 3 | Pending |
| PHASE-01 ~ PHASE-06 | Phase 3 | Pending |
| AGENT-01 ~ AGENT-03 | Phase 3 | Pending |
| LIFECYCLE-01 ~ LIFECYCLE-02 | Phase 4 | Pending |
| SKILL-EVO-AUTO-01 | v2 | Deferred |
| VIS-01 | v2 | Deferred |
| INTEG-01 ~ INTEG-02 | v2 | Deferred |
| SCALE-01 | v2 | Deferred |

**Coverage:**
- v1 requirements: 29개 (FOUND 5 완료 + 미완 24개)
- Mapped to phases: 29
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-02*
*Last updated: 2026-04-02 after harness pivot research (ADR-009 ~ ADR-015)*
