---
record_id: "ADR-003"
title: "ADR 템플릿 표준"
type: "adr"
status: "Accepted"
created_at: "2026-03-18"
tags: ["template", "adr", "stage-1"]
---

# ADR-003: ADR 템플릿 표준

## Status
Accepted

## Context
ReproGate는 의사결정 기록으로 ADR(Architecture Decision Record)을 채택했다(RFC-001). ADR 작성 시 일관된 포맷을 유지하기 위해 Michael Nygard의 원본 ADR 템플릿을 표준으로 고정해야 한다.

## Decision
We will use Michael Nygard's original ADR template with the addition of YAML Frontmatter for notesmd-cli compatibility. All new ADRs will follow this format and be stored in `records/adr/`.

## Consequences
- 긍정: 업계 표준을 따르므로 외부 기여자도 즉시 이해 가능
- 긍정: Frontmatter를 통해 gatekeeper가 기계적으로 검사 가능
- 중립: 레거시 ADR(ADR-DPC-006, 007)은 ADR-001, ADR-002로 이관 완료

## Verification
- [x] ADR-001, ADR-002가 새 포맷으로 이관됨
- [x] 모든 ADR에 YAML Frontmatter 포함
