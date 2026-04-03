---
record_id: "ADR-013"
title: "Hook delivery via repo-local .claude/settings.json written by reprogate init"
type: "adr"
status: "Draft"
created_at: "2026-04-02"
tags: ["hooks", "activation", "init", "claude-code", "settings"]
---

# ADR-013: Hook delivery via repo-local .claude/settings.json written by reprogate init

## Status
Draft

## Context
ReproGate 활성화 시 hook layer와 command layer가 모두 강제된다(ADR-009). Claude Code는 `.claude/settings.json`을 통해 hooks를 로드한다.

Hook 배포 방식에 두 가지 선택지가 있다:
- **전역**: `~/.claude/settings.json` — 모든 CC 세션에 적용
- **레포 로컬**: `.claude/settings.json` — 해당 레포의 CC 세션에만 적용

HARNESS-ARCHITECTURE.md Q3에서 이 결정이 오픈 이슈로 플래그되었다.

## Decision

Hook을 **레포 로컬** `.claude/settings.json`에 배포한다. `reprogate init` 커맨드가 이 파일을 생성·갱신한다.

- **활성화**: `reprogate init` 실행 → `.claude/settings.json`에 ReproGate hook 설정 주입
- **비활성화**: `REPROGATE_DISABLED=1` 환경 변수 또는 `reprogate disable` 커맨드로 `.claude/settings.json`에서 hook 제거
- **프로파일 게이팅**: ECC의 `run-with-flags.js` 패턴을 차용해 `REPROGATE_HOOK_PROFILE=minimal|standard|strict` 환경 변수로 hook 강도를 조정

`.claude/settings.json`은 **개발자 로컬 환경 전용 설정**으로 취급하며 `.gitignore`에 포함된다(ADR-017).
따라서 레포를 클론한 후 각 개발자가 `reprogate init`을 실행하여 본인 환경에 hook을 주입해야 한다.

## Consequences
- Positive: ReproGate를 사용하는 레포에서만 hook이 활성화된다 — 다른 CC 프로젝트에 영향 없음.
- Positive: 레포 클론 후 `reprogate init` 한 번으로 전체 hook 환경 복원.
- Positive: `.claude/settings.json`을 gitignore하므로 민감한 로컬 설정이 레포에 노출되지 않는다(ADR-017).
- Neutral: `reprogate init`을 실행하지 않으면 hook이 없는 상태로 동작한다 — 문서화 필요.
- Negative: 레포마다 각 개발자가 `reprogate init`을 직접 실행해야 한다 — 자동화 불가.

## Verification
- [ ] `reprogate init` 커맨드가 `.claude/settings.json`을 생성·갱신함.
- [ ] `REPROGATE_DISABLED=1` 환경 변수로 hook을 비활성화할 수 있음.
- [ ] `REPROGATE_HOOK_PROFILE` 환경 변수로 hook 강도를 조정할 수 있음.
- [ ] `.claude/settings.json`이 `.gitignore`에 포함됨 (로컬 전용, 커밋 제외, ADR-017).
