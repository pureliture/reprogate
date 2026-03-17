# ADR-DPC-004: AI 도구 산출물 경계 분리 (Remote-managed vs Local-only)

## Status

**Accepted** (2026-03-08)

## Context

`master`와 `wafful4(java8)`에서 AI 도구 파일(`.claude/.codex/.omc`)의 추적 기준이 일치하지 않아,
동일 프로젝트 내에서도 로컬 실행 스펙이 원격에 혼입되는 문제가 발생했다.

또한 ai-ops를 별도 공개 레포로 분리하려면 아래 경계가 선행 확정되어야 한다.

1. ai-ops 프레임워크 공통 자산
2. 타겟 프로젝트 특화 어댑터 자산
3. 로컬 실행 중 생성/변경되는 런타임 자산

## Decision

### 1) 숨김 AI 도구 디렉토리는 Local-only로 고정

- `.claude/`, `.codex/`, `.omc/`는 원격 추적 대상에서 제외한다.
- 커밋 단계에서 해당 경로 변경이 감지되면 하드 차단한다.

### 2) 정책/지침은 비숨김 문서 경로에서 관리

- 원격 관리가 필요한 정책 문서와 가이드는 `docs/...` 및 `scripts/...`에서 관리한다.
- 숨김 디렉토리는 로컬 실행 진입점/실행 결과 저장소로만 사용한다.

### 3) 포팅 경계 모델

- ai-ops 레포: 프로젝트 무방 공통 정책/프로세스/훅 원본
- 타겟 프로젝트: 프로젝트 특화 어댑터 문서(예: `AGENTS.md`, branch-specific guide)
- 로컬 환경: 툴 런타임 파일(state/log/replay/cooldown/settings)

## Consequences

### 긍정적

- 워크스페이스 간 기준 불일치가 줄어든다.
- ai-ops 공개 레포 분리 시 경계가 명확해진다.
- 로컬 툴 상태가 원격 이력에 오염되는 위험을 낮춘다.

### 부정적

- 로컬 숨김 디렉토리 초기화/동기화 절차를 별도로 안내해야 한다.
- 기존에 숨김 경로에 저장되던 정책성 문서를 이관해야 한다.

## Related

- [WP-DPC-2026-03-007](../work-packets/WP-DPC-2026-03-007-ai-tool-artifact-separation.md)
- [WP-DPC-2026-03-005](../work-packets/WP-DPC-2026-03-005-process-based-collaboration.md)
- [ops-bootstrap-master-plan.md](../ops-bootstrap-master-plan.md)
