# dpc Adapter Rules for dev-ps-cast

Use the dpc framework as the source of truth for process-driven work in this repository.

## Required References

Read these files before starting substantial work:

1. `WORKSPACE-PROFILE.md`
2. `docs/constitution.md`
3. `docs/operating-model.md`
4. `docs/process-catalog/README.md`
5. `docs/work-packets/index.md`
6. `docs/CHANGELOG.md`

## Operating Rules

1. Start with `G0`, then recommend one process and one or two alternatives.
2. Wait for explicit user process selection before implementation work.
3. Record the selected process with:

```bash
python3 scripts/set_process_context.py --process <PROCESS> --wp <WP-ID> --team-mode auto
```

4. For team-capable processes (`P3`, `P4`, `S3`, optional `S1`), resolve `team` or `single` before code changes.
5. Use `single` fallback only when one worker can still perform `executor -> verifier -> recorder` responsibilities sequentially.
6. Update `docs/work-packets`, `docs/adr`, and `docs/CHANGELOG.md` as required by the selected process.
7. Before ending a process, summarize:
   - `current_process`
   - work performed
   - artifact paths
   - checklist status
   - `next_process`

## Codex / JetBrains / OMX Notes

- Follow this file and the framework docs for Codex or JetBrains AI Assistant work.
- Prefer `scripts/launch_dpc_session.py` for new writable sessions when appropriate.

## Claude Notes

- Claude adapters should follow the same process flow and use the same tracking artifacts.
- The local `.claude/settings.json` and hook wrapper should point to `scripts/hooks/claude_pretooluse_guard.py` when enabled.
