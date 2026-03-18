---
skill_id: "scope-defined"
name: "범위 정의 필수"
version: "0.1.0"
tags: ["core", "stage-1"]
---

# 범위 정의 필수 (scope-defined)

## Goal
모든 RFC에 설계(Design) 또는 제안(Proposal) 섹션이 포함되어 작업 범위가 명확히 정의되어야 한다.

## Required Records
- `type: "rfc"` 기록에 `## Design / Proposal` 또는 `## Design` 섹션이 존재해야 한다.
- `## Summary` 섹션이 존재해야 한다.

## Workflow Expectations
1. RFC 작성 시 Summary에서 한 문단으로 전체 작업을 요약한다.
2. Design / Proposal에서 구체적 구현 방안을 기술한다.
3. 범위를 벗어나는 작업은 별도 RFC로 분리한다.

## Verification
- `gatekeeper.py`가 RFC 타입 기록에 Design 관련 섹션이 존재하는지 검사한다.
