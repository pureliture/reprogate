#!/usr/bin/env python3
"""Create work records (ADRs, RFCs) with sequential IDs following existing convention."""
import argparse
import pathlib
import re
import sys
from datetime import date, timezone
from typing import Any, Dict, List

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
RECORDS_DIR = ROOT / "records"
CONFIG_PATH = ROOT / "reprogate.yaml"

# Fallback defaults if config file is missing
DEFAULT_RECORD_TYPES: Dict[str, Dict[str, Any]] = {
    "adr": {
        "dir": "adr",
        "prefix": "ADR",
        "required_sections": ["Context", "Decision", "Consequences", "Verification"],
    },
    "rfc": {
        "dir": "rfc",
        "prefix": "RFC",
        "required_sections": ["Summary", "Design / Proposal", "Verification"],
    },
}


def _load_record_types() -> Dict[str, Dict[str, Any]]:
    """Load record_types from reprogate.yaml, falling back to defaults."""
    if CONFIG_PATH.exists():
        try:
            data = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
            if data and "record_types" in data:
                return data["record_types"]
        except Exception:
            pass
    return DEFAULT_RECORD_TYPES


def slugify(title: str) -> str:
    """Convert a title to a URL-friendly slug.

    Lowercase, replace non-alphanumeric with hyphens, strip leading/trailing
    hyphens, collapse consecutive hyphens.
    """
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug


def next_id(record_dir: pathlib.Path, prefix: str) -> str:
    """Determine the next sequential ID for a record type.

    Scans existing files matching ``{prefix}-*.md`` in *record_dir*, extracts
    the numeric part, and returns ``{prefix}-{max+1:03d}``.  Returns
    ``{prefix}-001`` when the directory is empty or does not exist.
    """
    if not record_dir.exists():
        return f"{prefix}-001"

    max_num = 0
    pattern = re.compile(rf"^{re.escape(prefix)}-(\d+)")
    for path in record_dir.iterdir():
        match = pattern.match(path.name)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num

    return f"{prefix}-{max_num + 1:03d}"


def create_record(
    record_type: str,
    title: str,
    output_dir: pathlib.Path | None = None,
) -> pathlib.Path:
    """Create a new work record file with frontmatter and section stubs.

    Args:
        record_type: Record type key (e.g. ``"adr"``, ``"rfc"``).
        title: Human-readable title for the record.
        output_dir: Base directory for records.  Defaults to ``RECORDS_DIR``.

    Returns:
        Path to the newly created file.

    Raises:
        ValueError: If *record_type* is not a recognised type.
    """
    record_types = _load_record_types()

    if record_type not in record_types:
        valid = ", ".join(sorted(record_types.keys()))
        raise ValueError(f"Invalid record type '{record_type}'. Valid types: {valid}")

    type_config = record_types[record_type]
    prefix: str = type_config["prefix"]
    type_dir: str = type_config["dir"]
    required_sections: List[str] = type_config["required_sections"]

    base_dir = output_dir if output_dir is not None else RECORDS_DIR
    target_dir = base_dir / type_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    record_id = next_id(target_dir, prefix)
    slug = slugify(title)
    filename = f"{record_id}-{slug}.md"
    file_path = target_dir / filename

    today_iso = date.today().isoformat()

    frontmatter = {
        "record_id": record_id,
        "title": title,
        "type": record_type,
        "status": "DRAFT",
        "created_at": today_iso,
    }
    yaml_block = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)

    lines: List[str] = ["---", yaml_block.rstrip(), "---", ""]

    for section in required_sections:
        lines.append(f"# {section}")
        lines.append("")
        lines.append(f"<!-- TODO: Fill in {section} -->")
        lines.append("")

    file_path.write_text("\n".join(lines), encoding="utf-8")
    return file_path


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    record_types = _load_record_types()
    parser = argparse.ArgumentParser(
        description="Create a new work record (ADR, RFC).",
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=sorted(record_types.keys()),
        help="Record type to create.",
    )
    parser.add_argument("--title", required=True, help="Title for the new record.")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Base directory for records (default: records/).",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    output_dir = pathlib.Path(args.output_dir) if args.output_dir else None
    try:
        path = create_record(args.type, args.title, output_dir=output_dir)
        print(f"Created {path}")
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
