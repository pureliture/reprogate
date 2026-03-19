# ReproGate Adapter Rules for dev-ps-cast

Use the ReproGate framework as the source of truth for all AI-assisted work in this repository.

## Required References

Read these files before starting substantial work:

1. `WORKSPACE-PROFILE.md`
2. `docs/governance/constitution.md`
3. `docs/governance/operating-model.md`
4. `docs/strategy/final-definition.md`

## Operating Rules

ReproGate is an **artifact-driven compiler/gatekeeper**, not a state-tracking orchestrator. Your execution must be record-backed.

1. **Record-First Work**: Before implementing code changes, ensure there is a clear work record (e.g., plan, intent, scope).
2. **Explainable Decisions**: Document any significant technical decisions, alternative approaches discarded, and the reasoning behind them.
3. **Verification over Completion**: Implementation alone is not completion. Always include explicit verification steps and document the results.
4. **Skills and Gates**: Rely on explicitly recorded rules (`rules.rego`) and guidelines (`guidelines.md`) when they exist in the repository to guide your workflow.

## Expected Behavior

- Do not rely solely on conversational memory; if it matters, it should exist as an inspectable artifact.
- Follow the workflow dictated by the presence or absence of required outputs (Artifact-Driven Workflow). If a required artifact (like a design doc) is missing, create or request it before proceeding.
- Before starting code changes, confirm whether the user wants the work performed in an isolated workspace or worktree when branch isolation could matter. If the user prefers isolation, or if concurrent work makes isolation the safer default, use a separate workspace/worktree instead of modifying the current checkout directly.
- When addressing pull request review feedback, reply on each resolved review thread and mark the thread resolved using the platform's available mechanism when possible. Do not treat code changes alone as sufficient closure when review-state evidence can also be recorded in the PR.

## Pull Request Requirements

PR 생성 시 `validate_product_definition.py` CI가 실행되므로 다음 규칙을 **반드시** 준수:

### PR Body 필수 섹션
모든 섹션을 채워야 하며, `TBD`, `N/A`, `todo`, `없음` 또는 빈 `-`는 **금지**:

1. **Related Docs**: `docs/` 또는 `records/`로 시작하는 **실제 존재하는 파일 경로** 기재
   ```
   - docs/strategy/final-definition.md
   - records/adr/007-uv-toolchain.md
   ```
2. **Decision Record**: 관련 ADR/RFC 경로 또는 구체적인 변경 이유 기재
3. **Verification**: 실제 수행한 검증 내용 구체적으로 기재

### 구현 파일 변경 시 문서 동반 필수
`scripts/`, `skills/`, `templates/`, `.github/` 변경 시:
→ `docs/spec/`, `docs/strategy/`, `docs/design/`, `docs/governance/`, `records/adr/`, `records/rfc/` 중 하나를 **반드시 함께 변경/추가**

### 연관 문서 정합성
- `final-definition.md` 변경 시 → `vision.md`, `roadmap.md`, `product-boundary.md` 함께 변경
- `product-boundary.md` 변경 시 → `scenarios.md` 함께 변경

### PR 머지 전 코드 리뷰 처리 (필수)
머지 시도 전 **반드시** 다음 절차 수행:

1. **리뷰 코멘트 확인**: `gh pr view <PR번호> --comments` 또는 `gh api repos/{owner}/{repo}/pulls/{pr}/comments`로 미해결 코멘트 확인
2. **미해결 코멘트 있으면 머지 중단**: 코멘트가 있으면 머지 진행하지 않고 조치 먼저
3. **코멘트 조치**: 코드 수정 또는 설명으로 피드백 반영
4. **대댓글 작성**: 해당 리뷰 코멘트에 조치 내용 대댓글
5. **Resolved 처리**: GraphQL API로 리뷰 스레드 resolved 처리
   ```bash
   gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "THREAD_ID"}) { thread { isResolved } } }'
   ```
6. **모든 코멘트 해결 후 머지**: 미해결 코멘트가 0개일 때만 머지 진행

## Python Execution Standard

This repository uses `uv` as the Python execution standard.

### Required

- Use `uv run python3 <script>` for all Python execution
- Declare persistent dependencies in `pyproject.toml` and lock them in `uv.lock`

### Forbidden

- `python3 -m venv` - Do not create virtual environments manually
- `source venv/bin/activate` - Do not activate virtual environments
- `pip install` / `pip3 install` - Do not use pip directly
- `uv run --with ...` in committed code - Use `pyproject.toml` for persistent dependencies

### Examples

```bash
# Run a script
uv run python3 scripts/validate_product_definition.py --help

# One-liner
uv run python3 -c "print('hello')"

# Install dependencies (CI or first-time setup)
uv sync --frozen
```
