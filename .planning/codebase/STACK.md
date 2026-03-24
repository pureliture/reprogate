# Technology Stack

**Analysis Date:** 2025-03-24

## Languages

**Primary:**
- Python 3.10+ - Used for all core tooling, scripts, and gatekeeper logic in `scripts/`.

**Secondary:**
- Shell (Bash) - Used for Git hooks and installation scripts in `.githooks/` and `scripts/`.
- Markdown - Used for documentation, records, and skills across `docs/`, `records/`, and `skills/`.

## Runtime

**Environment:**
- Python 3.10+

**Package Manager:**
- uv - Specified in `pyproject.toml` and `reprogate.yaml` as the python toolchain.
- Lockfile: `uv.lock` is present.

## Frameworks

**Core:**
- ReproGate (Custom) - A repository tooling framework defined by `reprogate.yaml`.

**Testing:**
- pytest - Used for testing scripts, located in `scripts/tests/`.

**Build/Dev:**
- uv - Used for dependency management and environment isolation.

## Key Dependencies

**Critical:**
- `PyYAML` (>=6.0) - Used for parsing configuration files and frontmatter in Markdown records.
- `requests` (>=2.28) - Used for external HTTP requests.

**Infrastructure:**
- Git - Used for version control and hook-based enforcement.

## Configuration

**Environment:**
- Configured via `reprogate.yaml` in the project root.
- Python dependencies managed via `pyproject.toml`.

**Build:**
- `pyproject.toml`
- `reprogate.yaml`

## Platform Requirements

**Development:**
- Python 3.10 or higher.
- `uv` toolchain recommended.

**Production:**
- Primarily a development-time tooling suite; runs in local developer environments and CI/CD pipelines.

---

*Stack analysis: 2025-03-24*
