## Change Type
- Bug Fix (CI/CD Workflow)

## Why
- PR #12에서 추가된 워크플로우 로직의 세부 결함(Codex 봇이 지적한 사항)을 보완합니다.

## Linked Issue
- N/A

## Product Layer
- CI/CD Workflow

## Related Docs
- docs/governance/ops-bootstrap-master-plan.md

## Decision Record
- PR 브랜치 대상 푸시 로직 분기 처리(`github.event.pull_request.head.ref`) 및 Closed 이벤트 대응.
- `gh` CLI 예외 처리 강화.
- `progress.md`의 의미 있는 변경 감지 로직 추가.

## Verification
- 로컬 스크립트(`validate_product_definition.py`) 및 Gatekeeper 검증 완료.
