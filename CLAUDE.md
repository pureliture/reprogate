# Claude Code 전용 규칙

이 파일은 Claude Code에서만 참조됩니다. 툴 중립적 규칙은 `AGENTS.md`를 참고하세요.

## Git Workflow

1. **작업 시작 전 worktree 사용 여부 확인**: 코드 변경이 필요한 작업 시작 전에 사용자에게 worktree로 작업할지 물어볼 것. 사용자가 원하면 `EnterWorktree` 도구 사용.

2. **PR 리뷰 코멘트 처리**: 코드 수정 후 해당 리뷰 코멘트에 대댓글 달고, GraphQL API로 resolved 처리까지 완료.
