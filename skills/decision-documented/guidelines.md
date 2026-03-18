---
skill_id: "decision-documented"
name: "의사결정 기록"
version: "0.1.0"
tags: ["core", "stage-1"]
---

# 의사결정 기록 (decision-documented)

## Goal
중요한 기술적 판단에는 반드시 ADR(Architecture Decision Record)을 작성한다.

## Required Records
- `records/adr/` 디렉토리에 Frontmatter가 포함된 ADR `.md` 파일이 존재해야 한다.
- Frontmatter의 `type` 필드가 `"adr"`이어야 한다.

## Workflow Expectations
1. 대안이 2개 이상인 기술적 결정이 발생하면 ADR을 작성한다.
2. Context → Decision → Consequences 순서로 기록한다.
3. 결정이 뒤집히면 새 ADR로 supersede하되, 원본은 삭제하지 않는다.

## Verification
- `gatekeeper.py`가 `records/adr/` 내 ADR 파일의 존재를 검사한다.
- Frontmatter의 `type: "adr"` 필드를 확인한다.
