#!/usr/bin/env python3
import argparse
import pathlib
import sys
from typing import Dict, List


ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "templates" / "ai-ops.config.yaml.j2"
OUTPUT_PATH = ROOT / "ai-ops.config.yaml"
DEFAULT_PROCESSES = ["P0", "P1", "P3", "P4", "S1", "S2", "S4"]


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a starter ai-ops.config.yaml file.")
    parser.add_argument("--output", default=str(OUTPUT_PATH), help="Output config path.")
    parser.add_argument("--project-name", default=ROOT.name, help="Project name.")
    parser.add_argument("--project-description", default="", help="Optional project description.")
    parser.add_argument("--primary-workspace-name", default="main", help="Primary workspace name.")
    parser.add_argument("--primary-branch", default="main", help="Primary branch name.")
    parser.add_argument("--primary-runtime", default="", help="Optional runtime description.")
    parser.add_argument(
        "--enabled-processes",
        default=",".join(DEFAULT_PROCESSES),
        help="Comma-separated process ids.",
    )
    parser.add_argument("--disable-claude", action="store_true", help="Disable Claude adapter generation.")
    parser.add_argument(
        "--disable-claude-hook-enforcement",
        action="store_true",
        help="Disable Claude hook enforcement guidance.",
    )
    parser.add_argument("--disable-codex", action="store_true", help="Disable Codex adapter generation.")
    parser.add_argument("--wp-path", default="docs/work-packets", help="Work packet path.")
    parser.add_argument("--adr-path", default="docs/adr", help="ADR path.")
    parser.add_argument("--changelog-path", default="docs/CHANGELOG.md", help="Changelog path.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing config file.")
    return parser.parse_args(argv)


def render_template(text: str, context: Dict[str, str]) -> str:
    rendered = text
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{ {key} }}}}", value)
    return rendered


def build_context(args: argparse.Namespace) -> Dict[str, str]:
    processes = [item.strip() for item in args.enabled_processes.split(",") if item.strip()]
    return {
        "project_name": args.project_name,
        "project_description_block": (
            f'  description: "{args.project_description}"' if args.project_description else ""
        ),
        "primary_workspace_name": args.primary_workspace_name,
        "primary_branch": args.primary_branch,
        "primary_runtime_block": (
            f'    runtime: "{args.primary_runtime}"' if args.primary_runtime else ""
        ),
        "enabled_process_lines": "\n".join(f"    - {process}" for process in processes),
        "claude_enabled": "false" if args.disable_claude else "true",
        "claude_hook_enforcement": "false" if args.disable_claude_hook_enforcement else "true",
        "codex_enabled": "false" if args.disable_codex else "true",
        "wp_path": args.wp_path,
        "adr_path": args.adr_path,
        "changelog_path": args.changelog_path,
    }


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    output_path = pathlib.Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path

    if output_path.exists() and not args.force:
        print(f"Refusing to overwrite existing file without --force: {output_path}", file=sys.stderr)
        return 1

    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    rendered = render_template(template_text, build_context(args))
    output_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")
    try:
        shown = output_path.relative_to(ROOT)
    except ValueError:
        shown = output_path
    print(f"Created {shown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
