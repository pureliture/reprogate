---
record_id: "ADR-015"
title: "Harness activation model: reprogate.yaml presence + explicit init"
type: "adr"
status: "Draft"
created_at: "2026-04-02"
tags: ["activation", "init", "harness", "hooks", "config"]
---

# ADR-015: Harness activation model: reprogate.yaml presence + explicit init

## Status
Draft

## Context
ADR-009는 "ReproGate 활성화 시 command layer와 hook layer가 모두 강제된다. 비활성화는 명시적 조치 필요"라고 명시했다. 구체적인 활성화·비활성화 메커니즘은 정의되지 않았다(HARNESS-ARCHITECTURE.md Q1).

선택지:
1. `reprogate.yaml` 존재 = 암묵적 활성화 (항상 켜짐)
2. `reprogate init` 명시 실행 후 활성화

## Decision

**2단계 활성화 모델**을 채택한다:

**1단계: 하네스 컨텍스트 선언** — `reprogate.yaml`이 레포에 존재하면 해당 레포는 ReproGate 하네스 컨텍스트다. 그러나 hook layer는 아직 활성화되지 않는다.

**2단계: 하네스 설치** — `reprogate init` 실행 시:
- `.claude/settings.json`에 hook 설정 주입 (ADR-013)
- `.claude/session-data/` 디렉토리 생성 (ADR-011)
- `record_triggers` 기본값을 `reprogate.yaml`에 주입 (ADR-014)
- pre-commit hook 설치 확인

**비활성화**:
- 임시: `REPROGATE_DISABLED=1` 환경 변수 → hook이 no-op으로 동작
- 영구: `reprogate disable` → `.claude/settings.json`에서 hook 설정 제거

**재활성화**: `reprogate init` 재실행.

이 모델은 "harness를 켜면 두 레이어 모두 강제"라는 ADR-009 원칙과 일치하면서, 명시적 설치 단계를 통해 의도하지 않은 활성화를 방지한다.

## Consequences
- Positive: 활성/비활성 상태가 명확하다 — `reprogate init` 여부로 판단 가능.
- Positive: `REPROGATE_DISABLED=1`로 단기 긴급 비활성화가 쉽다.
- Positive: `reprogate.yaml`만 있고 `init`을 안 한 상태(= 컨텍스트만 선언)도 유효한 상태로 정의된다.
- Neutral: 레포 클론 후 `reprogate init`을 실행해야 hook이 활성화됨 — README에 명시 필요.
- Negative: 2단계 모델이므로 처음 사용자가 "hook이 왜 안 걸리지?"를 겪을 수 있다.

## Verification
- [ ] `reprogate init` 실행 후 `.claude/settings.json`에 hook이 등록됨.
- [ ] `REPROGATE_DISABLED=1` 설정 시 PreToolUse hook이 no-op으로 동작함.
- [ ] `reprogate disable` 실행 후 `.claude/settings.json`에서 hook 설정이 제거됨.
- [ ] `reprogate.yaml` 없는 디렉토리에서 `reprogate init` 실행 시 오류 메시지 출력.
