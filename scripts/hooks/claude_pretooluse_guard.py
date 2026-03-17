#!/usr/bin/env python3
import json
import os
import pathlib
import re
import subprocess
import sys
from typing import Dict, Optional, Tuple


ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts" / "check_compliance.py"
PROCESS_CONTEXT = pathlib.Path(
    os.getenv("DPC_CONTEXT_FILE", ROOT / ".dpc" / "process-context.json")
)

GUARDED_TOOLS = {"Write", "Edit", "MultiEdit", "Bash"}
READ_ONLY_PROCESSES = {"G0", "P0", "P1", "P2", "S2", "S4"}
TEAM_ELIGIBLE_PROCESSES = {"P3", "P4", "S3", "S1"}

READONLY_BASH_PATTERNS = [
    re.compile(r"^(pwd|date)$"),
    re.compile(r"^(ls|find|cat|head|tail|wc|grep|rg|cut|sort|uniq|echo)\b"),
    re.compile(r"^sed\s+-n\b"),
    re.compile(r"^git\s+(status|log|show|diff|rev-parse|branch)\b"),
    re.compile(r"^python3\s+scripts/check_compliance.py\b"),
    re.compile(r"^(pytest|python3?\s+-m\s+pytest|python3?\s+-m\s+unittest)\b"),
]


def read_payload() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def tool_name(payload: dict) -> str:
    return payload.get("tool_name") or payload.get("toolName") or payload.get("tool") or ""


def tool_input(payload: dict) -> dict:
    value = payload.get("tool_input") or payload.get("input") or {}
    return value if isinstance(value, dict) else {}


def extract_file_path(payload: dict) -> str:
    item = tool_input(payload)
    return item.get("file_path") or item.get("path") or ""


def extract_command(payload: dict) -> str:
    item = tool_input(payload)
    return item.get("command") or item.get("cmd") or ""


def as_repo_relative(path_str: str) -> Optional[str]:
    if not path_str:
        return None
    path = pathlib.Path(path_str)
    if not path.is_absolute():
        path = (ROOT / path).resolve()
    else:
        path = path.resolve()
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def is_documentation_target(path_str: str) -> bool:
    rel = as_repo_relative(path_str)
    if not rel:
        return False
    return rel.startswith("docs/") or rel.endswith(".md") or rel in {"README.md", "AGENTS.md"}


def load_process_context() -> Dict[str, object]:
    if not PROCESS_CONTEXT.exists():
        return {}
    try:
        data = json.loads(PROCESS_CONTEXT.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:  # noqa: BLE001
        return {}


def selected_process(context: Dict[str, object]) -> str:
    value = str(context.get("selected_process") or context.get("process") or "").strip().upper()
    return value


def team_mode(context: Dict[str, object]) -> str:
    value = str(context.get("team_mode") or "auto").strip().lower()
    return value if value in {"auto", "single", "team", "none"} else "auto"


def tdd_mode_enabled(context: Dict[str, object]) -> bool:
    """Check if TDD mode is enabled in the process context."""
    value = context.get("tdd_mode") or context.get("tdd_enabled")
    if value is None:
        # Default: TDD mode is enabled if process is TDD-related
        process = selected_process(context)
        return process in {"TDD", "P3"}  # P3 is implementation process
    return bool(value)


def is_readonly_bash(command: str) -> bool:
    cmd = (command or "").strip()
    if not cmd:
        return True
    segments = re.split(r"&&|;|\|\|", cmd)
    for segment in segments:
        part = segment.strip()
        if not part:
            continue
        if any(pattern.match(part) for pattern in READONLY_BASH_PATTERNS):
            continue
        return False
    return True


def deny(reason: str) -> int:
    print(json.dumps({"permissionDecision": "deny", "permissionDecisionReason": reason}))
    return 0


def allow() -> int:
    print(json.dumps({"permissionDecision": "allow"}))
    return 0


def run_checker() -> Tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(CHECKER), "--mode", "none"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return True, ""
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    return False, lines[0] if lines else "AI Ops compliance check failed."


# =============================================================================
# TDD Gate Functions
# =============================================================================

# File extensions that are considered code files (requiring TDD enforcement)
CODE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".kt", ".go", ".rs", ".rb", ".swift"}

# File extensions and patterns that are exempt from TDD enforcement
CONFIG_EXTENSIONS = {".yaml", ".yml", ".json", ".toml", ".ini", ".cfg", ".conf", ".env"}
CONFIG_FILES = {"Makefile", "Dockerfile", ".gitignore", ".dockerignore", "requirements.txt", "package.json", "tsconfig.json", "pyproject.toml"}

# Test file patterns by language
TEST_PATTERNS = {
    "python": [
        re.compile(r"^test_.*\.py$"),      # test_*.py
        re.compile(r".*_test\.py$"),        # *_test.py
    ],
    "javascript": [
        re.compile(r".*\.test\.[jt]sx?$"),  # *.test.js, *.test.ts, *.test.tsx
        re.compile(r".*\.spec\.[jt]sx?$"),  # *.spec.js, *.spec.ts
    ],
    "java": [
        re.compile(r".*Test\.java$"),       # *Test.java
        re.compile(r".*Tests\.java$"),      # *Tests.java
    ],
}


def is_test_file(path_str: str) -> bool:
    """Determine if a file is a test file based on naming conventions.

    Supports:
    - Python: test_*.py, *_test.py
    - JavaScript/TypeScript: *.test.js, *.spec.ts, etc.
    - Java: *Test.java, *Tests.java
    """
    if not path_str:
        return False

    name = pathlib.Path(path_str).name

    # Check all test patterns
    for patterns in TEST_PATTERNS.values():
        for pattern in patterns:
            if pattern.match(name):
                return True

    return False


def get_language_from_extension(path_str: str) -> Optional[str]:
    """Get the language category from file extension."""
    ext = pathlib.Path(path_str).suffix.lower()

    if ext == ".py":
        return "python"
    elif ext in {".js", ".ts", ".tsx", ".jsx"}:
        return "javascript"
    elif ext in {".java", ".kt"}:
        return "java"

    return None


def find_corresponding_test(impl_path: str, root_dir: str) -> Optional[str]:
    """Find a test file corresponding to the implementation file.

    Search strategies:
    1. Same directory: test_<name>.py, <name>_test.py, <name>.test.js
    2. tests/ directory at same level
    3. tests/ directory at project root
    """
    if not impl_path:
        return None

    impl = pathlib.Path(impl_path)
    root = pathlib.Path(root_dir)
    stem = impl.stem  # filename without extension
    language = get_language_from_extension(impl_path)

    if not language:
        return None

    # Generate possible test file names
    test_names = []
    if language == "python":
        test_names = [f"test_{stem}.py", f"{stem}_test.py"]
    elif language == "javascript":
        ext = impl.suffix
        test_names = [f"{stem}.test{ext}", f"{stem}.spec{ext}"]
    elif language == "java":
        test_names = [f"{stem}Test.java", f"{stem}Tests.java"]

    # Search locations
    search_dirs = []

    # 1. Same directory
    if impl.parent.exists():
        search_dirs.append(impl.parent)

    # 2. tests/ at same level as implementation
    tests_sibling = impl.parent / "tests"
    if tests_sibling.exists():
        search_dirs.append(tests_sibling)

    # 3. tests/ at project root
    tests_root = root / "tests"
    if tests_root.exists():
        search_dirs.append(tests_root)

    # 4. scripts/tests/ for scripts
    scripts_tests = root / "scripts" / "tests"
    if scripts_tests.exists():
        search_dirs.append(scripts_tests)

    # Search for test files
    for search_dir in search_dirs:
        for test_name in test_names:
            test_path = search_dir / test_name
            if test_path.exists():
                return str(test_path)

    # Recursive search in tests directories for the test file
    for tests_dir in [tests_root, scripts_tests]:
        if tests_dir.exists():
            for test_name in test_names:
                for found in tests_dir.rglob(test_name):
                    return str(found)

    return None


def should_enforce_tdd_gate(path_str: str) -> bool:
    """Determine if TDD gate should be enforced for this file.

    TDD gate is enforced for:
    - Code files (Python, JS, TS, Java, etc.)

    TDD gate is NOT enforced for:
    - Test files themselves
    - Documentation files (*.md)
    - Configuration files (*.yaml, *.json, etc.)
    - __init__.py files
    """
    if not path_str:
        return False

    path = pathlib.Path(path_str)
    name = path.name
    ext = path.suffix.lower()

    # Skip test files
    if is_test_file(path_str):
        return False

    # Skip documentation
    if ext == ".md":
        return False

    # Skip config files
    if ext in CONFIG_EXTENSIONS or name in CONFIG_FILES:
        return False

    # Skip __init__.py
    if name == "__init__.py":
        return False

    # Skip dot files
    if name.startswith("."):
        return False

    # Only enforce for known code extensions
    if ext not in CODE_EXTENSIONS:
        return False

    return True


def check_tdd_gate(file_path: str, root_dir: str, tdd_enabled: bool = True) -> Tuple[bool, str]:
    """Check if the file passes the TDD gate.

    Returns:
        (allowed, reason): allowed is True if the file can be written,
                          reason is the denial message if not allowed.
    """
    # If TDD mode is disabled, always allow
    if not tdd_enabled:
        return True, ""

    # If this file doesn't require TDD enforcement, allow
    if not should_enforce_tdd_gate(file_path):
        return True, ""

    # Check if corresponding test exists
    test_path = find_corresponding_test(file_path, root_dir)
    if test_path:
        return True, ""

    # No test found - deny
    file_name = pathlib.Path(file_path).name
    return False, (
        f"TDD Gate: Cannot write implementation file '{file_name}' without a corresponding test. "
        f"Write the test first (e.g., test_{pathlib.Path(file_path).stem}.py), then implement."
    )


def main() -> int:
    payload = read_payload()
    name = tool_name(payload)
    if name and name not in GUARDED_TOOLS:
        return allow()

    context = load_process_context()
    process = selected_process(context)

    if name in {"Write", "Edit", "MultiEdit"}:
        if not process:
            return deny("Select a process before using write/edit tools.")
        if process in TEAM_ELIGIBLE_PROCESSES and team_mode(context) == "auto":
            return deny("Resolve team_mode to team or single before implementation on a team-capable process.")
        if process in READ_ONLY_PROCESSES and not is_documentation_target(extract_file_path(payload)):
            return deny(f"{process} only allows documentation or record updates.")

        # TDD Gate check: ensure test exists before writing implementation
        file_path = extract_file_path(payload)
        if tdd_mode_enabled(context):
            tdd_ok, tdd_reason = check_tdd_gate(file_path, str(ROOT), tdd_enabled=True)
            if not tdd_ok:
                return deny(tdd_reason)

    if name == "Bash":
        command = extract_command(payload)
        readonly = is_readonly_bash(command)
        if not process and not readonly:
            return deny("Select a process before running mutating shell commands.")
        if process in TEAM_ELIGIBLE_PROCESSES and not readonly and team_mode(context) == "auto":
            return deny("Resolve team_mode to team or single before mutating shell commands.")
        if process in READ_ONLY_PROCESSES and not readonly:
            return deny(f"{process} only allows read-only shell commands.")

    ok, reason = run_checker()
    if not ok:
        return deny(reason)
    return allow()


# Legacy alias for backward compatibility
AI_OPS_CONTEXT_FILE = os.getenv("AI_OPS_CONTEXT_FILE")
if AI_OPS_CONTEXT_FILE:
    PROCESS_CONTEXT = pathlib.Path(AI_OPS_CONTEXT_FILE)


if __name__ == "__main__":
    sys.exit(main())
