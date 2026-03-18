---
record_id: "RFC-002"
title: "Stage 1 Hardening — ReproGate 자체 적용"
type: "rfc"
status: "Implemented"
created_at: "2026-03-18"
implemented_at: "2026-03-18"
tags: ["stage-1", "hardening", "dogfooding"]
---

# RFC-002: Stage 1 Hardening — ReproGate 자체 적용

## Status
Implemented

## Summary
Stage 0에서 만든 프로토타입을 이 저장소의 개발 워크플로에 실제로 적용한다. 3개의 Skill을 추가하고, gatekeeper를 강화하며, Git Hook으로 강제 루프를 완성한다.

## Motivation
Stage 0은 최소 루프(기록 존재 검사)만 구현했다. 실제 "작업 패턴 강제"를 증명하려면 더 세밀한 검사(의사결정 기록, 검증 기록, 범위 정의)가 필요하다.

## Design / Proposal

### 신규 Skill 3개
1. `decision-documented` — ADR이 존재하는지 검사
2. `verification-present` — RFC/ADR에 Verification 섹션이 있는지 검사
3. `scope-defined` — RFC에 Scope 또는 Design 섹션이 있는지 검사

### Gatekeeper 강화
- Frontmatter 필드 검사 외에 **마크다운 섹션 존재 여부** 검사 추가
- `reprogate.yaml`에서 records_dir, skills_dir을 읽도록 개선

### Git Hook 연동
- `.githooks/pre-commit`에서 `gatekeeper.py` 실행
- `git config core.hooksPath .githooks`로 활성화

## Alternatives Considered
- CI에서만 검사 → 로컬 피드백 루프가 없어서 개발 경험이 떨어짐
- 모든 섹션을 필수로 강제 → 과도한 부담, 점진적 도입이 불가능

## Verification
- [x] 3개 Skill이 skills/에 존재 (decision-documented, verification-present, scope-defined)
- [x] gatekeeper.py가 섹션 누락을 감지하고 fail 반환 (exit code 1 확인)
- [x] pre-commit hook이 `.githooks/pre-commit` → `gatekeeper.py` 연동 완료
