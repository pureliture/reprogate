---
record_id: "ADR-014"
title: "Record trigger scope: path-pattern based change categorization"
type: "adr"
status: "Draft"
created_at: "2026-04-02"
tags: ["gate", "records", "gatekeeper", "scope", "policy"]
---

# ADR-014: Record trigger scope: path-pattern based change categorization

## Status
Draft

## Context
`record-required` skill(Phase 1)은 레코드 존재를 검사하지만, 어떤 변경이 레코드를 요구하는지에 대한 범위 필터가 정의되어 있지 않다(HARNESS-ARCHITECTURE.md Q2). 범위가 너무 넓으면 모든 커밋에서 ADR을 요구해 마찰이 극심해지고, 너무 좁으면 게이트가 의미를 잃는다.

## Decision

`reprogate.yaml`에 `record_triggers` 섹션을 추가해 레코드를 요구하는 변경 범주를 파일 경로 패턴으로 정의한다.

**기본값 (하네스 피벗 이후):**

```yaml
record_triggers:
  - pattern: "scripts/**"
    record_type: "adr"
    reason: "핵심 스크립트 변경은 의사결정 기록 필요"
  - pattern: "skills/**"
    record_type: "adr"
    reason: "Skill 정책 변경은 의사결정 기록 필요"
  - pattern: "templates/**"
    record_type: "adr"
    reason: "템플릿 변경은 생성 산출물에 영향"
  - pattern: ".github/**"
    record_type: "adr"
    reason: "워크플로우 및 에이전트 설정 변경"
  - pattern: "docs/strategy/**"
    record_type: "adr"
    reason: "전략 문서 변경은 제품 방향 결정"
```

레코드가 **필요 없는** 범주: `docs/spec/**`, `docs/design/**`, `records/**` (레코드 자체), `.planning/**`, README 수정, 일반 산문 문서 업데이트.

`gatekeeper.py`는 커밋 diff에서 변경된 파일 목록을 추출하고 `record_triggers` 패턴과 매칭해 레코드 요구 여부를 판단한다.

## Consequences
- Positive: 마찰이 예측 가능해진다 — 어떤 변경이 레코드를 요구하는지 개발자가 사전에 알 수 있다.
- Positive: `reprogate.yaml`에서 패턴을 추가/제거해 범위를 조정할 수 있다.
- Neutral: 초기 기본값이 잘못 설정되면 불필요한 마찰이 생긴다 — 실사용 후 조정 예상.
- Negative: 경로 패턴 매칭이 `gatekeeper.py`에 추가 로직을 요구한다.

## Verification
- [ ] `reprogate.yaml`에 `record_triggers` 섹션이 스키마에 추가됨.
- [ ] `gatekeeper.py`가 `record_triggers` 패턴을 읽어 레코드 요구 여부를 판단함.
- [ ] 트리거 대상 경로 변경 시 레코드 없이 커밋하면 pre-commit hook이 차단함.
- [ ] 트리거 비대상 경로 변경 시 레코드 없어도 커밋 통과함.
