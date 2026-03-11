#!/usr/bin/env python3
import argparse
import pathlib
import shutil
import sys
from datetime import date
from typing import Any, Dict, Iterable, List, Sequence, Tuple


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "ai-ops.config.yaml"
TEMPLATES_DIR = ROOT / "templates"

FRAMEWORK_DIRECTORIES = ("docs", "scripts", "config", "templates")


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate adapter files from ai-ops.config.yaml.")
    parser.add_argument("--config", default=str(CONFIG_PATH), help="Path to ai-ops.config.yaml.")
    parser.add_argument(
        "--output-root",
        default=str(ROOT),
        help="Directory where generated files will be written.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite generated files.")
    return parser.parse_args(argv)


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value.startswith(("\"", "'")) and value.endswith(("\"", "'")):
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return value


def load_config(path: pathlib.Path) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "project": {},
        "workspaces": {"primary": {}},
        "processes": {"enabled": []},
        "tools": {"claude": {}, "codex": {}},
        "records": {},
    }
    section: List[str] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if line.startswith("- "):
            if section == ["processes", "enabled"]:
                data["processes"]["enabled"].append(parse_scalar(line[2:]))
            continue

        if line.endswith(":"):
            key = line[:-1]
            if indent == 0:
                section = [key]
            elif indent == 2:
                section = [section[0], key]
            elif indent == 4:
                section = [section[0], section[1], key]
            continue

        key, raw_value = line.split(":", 1)
        value = parse_scalar(raw_value)

        if indent == 0:
            data[key] = value
            section = []
        elif indent == 2 and len(section) == 1:
            data[section[0]][key] = value
        elif indent == 4 and len(section) == 2:
            data[section[0]][section[1]][key] = value
        elif indent == 6 and len(section) == 3:
            data[section[0]][section[1]][section[2]][key] = value

    return data


def render_template(text: str, context: Dict[str, str]) -> str:
    rendered = text
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{ {key} }}}}", value)
    return rendered


def context_from_config(config: Dict[str, Any]) -> Dict[str, str]:
    project = config["project"]
    primary = config["workspaces"]["primary"]
    tools = config["tools"]
    claude = tools.get("claude", {})
    codex = tools.get("codex", {})
    records = config["records"]

    claude_enabled = bool(claude.get("enabled", True))
    claude_hook_enabled = bool(claude.get("hook_enforcement", True))
    codex_enabled = bool(codex.get("enabled", True))
    runtime = str(primary.get("runtime", "")).strip()
    runtime_value = runtime or "Fill in the primary runtime for this repository."

    return {
        "project_name": str(project["name"]),
        "project_description_block": (
            f'  description: "{project.get("description", "")}"' if project.get("description") else ""
        ),
        "primary_workspace_name": str(primary["name"]),
        "primary_branch": str(primary["branch"]),
        "primary_runtime_block": (
            f'    runtime: "{runtime}"' if runtime else ""
        ),
        "primary_runtime_value": runtime_value,
        "today": date.today().isoformat(),
        "today_month": date.today().isoformat()[:7],
        "enabled_process_lines": "\n".join(
            f"    - {process}" for process in config["processes"]["enabled"]
        ),
        "claude_enabled": "true" if claude_enabled else "false",
        "claude_hook_enforcement": "true" if claude_hook_enabled else "false",
        "codex_enabled": "true" if codex_enabled else "false",
        "wp_path": str(records["wp_path"]),
        "adr_path": str(records["adr_path"]),
        "changelog_path": str(records["changelog_path"]),
        "codex_notes_block": (
            "- Follow this file, `AGENTS.md`, and the copied framework docs for Codex or JetBrains AI Assistant work.\n"
            "- If a launch gate is installed, prefer it for new writable sessions."
            if codex_enabled
            else "- Codex adapter generation is disabled in this project configuration."
        ),
        "claude_notes_block": (
            "- Claude adapters should follow the same process flow and use the same tracking artifacts.\n"
            + (
                "- The generated `.claude/settings.json` and hook wrapper already point to `scripts/hooks/claude_pretooluse_guard.py`."
                if claude_hook_enabled
                else "- Claude hook enforcement is disabled in this project configuration."
            )
            if claude_enabled
            else "- Claude adapter generation is disabled in this project configuration."
        ),
        "claude_hook_block": (
            "When Claude hook enforcement is enabled, the generated `.claude/settings.json` and "
            "`.claude/hooks/pretooluse-ai-ops-guard.py` route to `scripts/hooks/claude_pretooluse_guard.py`."
            if claude_hook_enabled
            else "Claude hook enforcement is disabled in this project configuration."
        ),
    }


def write_file(path: pathlib.Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite without --force: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def copy_file(source: pathlib.Path, destination: pathlib.Path, force: bool) -> None:
    if source.resolve() == destination.resolve():
        return
    if destination.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite without --force: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def iter_framework_files(directory: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        if any(part == "__pycache__" for part in path.parts):
            continue
        if path.suffix == ".pyc":
            continue
        if path.name == ".gitkeep":
            continue
        yield path


def copy_framework_tree(output_root: pathlib.Path, force: bool) -> None:
    for directory_name in FRAMEWORK_DIRECTORIES:
        source_root = ROOT / directory_name
        for source_path in iter_framework_files(source_root):
            destination = output_root / source_path.relative_to(ROOT)
            copy_file(source_path, destination, force=force)


def render_outputs(
    output_root: pathlib.Path,
    config_path: pathlib.Path,
    config: Dict[str, Any],
    context: Dict[str, str],
    force: bool,
) -> Sequence[pathlib.Path]:
    rendered_outputs: List[Tuple[pathlib.Path, pathlib.Path]] = [
        (output_root / "ai-ops.config.yaml", config_path),
        (output_root / "AGENTS.md", TEMPLATES_DIR / "AGENTS.md.j2"),
        (output_root / "WORKSPACE-PROFILE.md", TEMPLATES_DIR / "WORKSPACE-PROFILE.md.j2"),
        (output_root / ".ai-ops" / "README.md", TEMPLATES_DIR / "project-ops" / "README.md.j2"),
        (output_root / pathlib.Path(config["records"]["changelog_path"]), TEMPLATES_DIR / "project-ops" / "CHANGELOG.md.j2"),
        (
            output_root / pathlib.Path(config["records"]["wp_path"]) / "index.md",
            TEMPLATES_DIR / "project-ops" / "work-packets" / "index.md.j2",
        ),
        (
            output_root / pathlib.Path(config["records"]["adr_path"]) / "README.md",
            TEMPLATES_DIR / "project-ops" / "adr" / "README.md.j2",
        ),
    ]

    if bool(config["tools"].get("codex", {}).get("enabled", True)):
        rendered_outputs.append((output_root / ".codex" / "README.md", TEMPLATES_DIR / "codex" / "README.md.j2"))

    if bool(config["tools"].get("claude", {}).get("enabled", True)):
        rendered_outputs.extend(
            [
                (output_root / ".claude" / "CLAUDE.md", TEMPLATES_DIR / "claude" / "CLAUDE.md.j2"),
                (output_root / ".claude" / "commands" / "ai-ops.md", TEMPLATES_DIR / "claude" / "commands" / "ai-ops.md.j2"),
                (output_root / ".claude" / "settings.json", TEMPLATES_DIR / "claude" / "settings.json.j2"),
            ]
        )
        if bool(config["tools"].get("claude", {}).get("hook_enforcement", True)):
            rendered_outputs.append(
                (
                    output_root / ".claude" / "hooks" / "pretooluse-ai-ops-guard.py",
                    TEMPLATES_DIR / "claude" / "hooks" / "pretooluse-ai-ops-guard.py.j2",
                )
            )

    rendered_paths: List[pathlib.Path] = []
    for output_path, template_path in rendered_outputs:
        if template_path.name.endswith(".yaml") and template_path == config_path:
            text = template_path.read_text(encoding="utf-8")
        else:
            text = render_template(template_path.read_text(encoding="utf-8"), context)
        write_file(output_path, text, force=force)
        rendered_paths.append(output_path)
    return rendered_paths


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    config_path = pathlib.Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    if not config_path.exists():
        print(f"Config file not found: {config_path}", file=sys.stderr)
        return 1
    output_root = pathlib.Path(args.output_root)
    if not output_root.is_absolute():
        output_root = ROOT / output_root

    config = load_config(config_path)
    context = context_from_config(config)

    copy_framework_tree(output_root, force=args.force)
    print("Copied framework directories: docs/, scripts/, config/, templates/")

    for output_path in render_outputs(output_root, config_path, config, context, force=args.force):
        try:
            shown = output_path.relative_to(output_root)
        except ValueError:
            shown = output_path
        print(f"Generated {shown}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
