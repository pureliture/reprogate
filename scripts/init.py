#!/usr/bin/env python3
import argparse
import pathlib
import sys
from typing import Dict, List


ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "templates" / "reprogate.yaml.j2"
OUTPUT_PATH = ROOT / "reprogate.yaml"


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a starter reprogate.yaml file.")
    parser.add_argument("--output", default=str(OUTPUT_PATH), help="Output config path.")
    parser.add_argument("--project-name", default=ROOT.name, help="Project name.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing config file.")
    return parser.parse_args(argv)


def render_template(text: str, context: Dict[str, str]) -> str:
    rendered = text
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{ {key} }}}}", value)
    return rendered


def build_context(args: argparse.Namespace) -> Dict[str, str]:
    return {
        "project_name": args.project_name,
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
