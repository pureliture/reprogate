#!/usr/bin/env python3
"""dpc document search - lightweight, no external dependencies."""
import argparse
import json
import pathlib
import re
import sys
from typing import List, Dict, Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"


def search_content(term: str, format_json: bool = False) -> List[Dict[str, Any]]:
    """Search document content for a term."""
    results = []
    pattern = re.compile(re.escape(term), re.IGNORECASE)

    for md in sorted(DOCS_DIR.rglob("*.md")):
        if ".obsidian" in md.parts:
            continue
        try:
            content = md.read_text(encoding="utf-8")
        except Exception:
            continue

        matches = []
        for i, line in enumerate(content.splitlines(), 1):
            if pattern.search(line):
                matches.append({"line": i, "text": line.strip()[:100]})

        if matches:
            rel_path = md.relative_to(DOCS_DIR).as_posix()
            results.append({
                "path": rel_path,
                "matches": matches[:5],  # limit matches per file
                "count": len(matches),
            })

    return results


def search_files(term: str) -> List[str]:
    """Fuzzy search file names."""
    pattern = re.compile(".*".join(re.escape(c) for c in term.lower()))
    results = []

    for md in sorted(DOCS_DIR.rglob("*.md")):
        if ".obsidian" in md.parts:
            continue
        rel_path = md.relative_to(DOCS_DIR).as_posix()
        if pattern.search(rel_path.lower()):
            results.append(rel_path)

    return results


def print_doc(name: str) -> str | None:
    """Print document content by name (partial match)."""
    name_lower = name.lower()
    for md in DOCS_DIR.rglob("*.md"):
        if name_lower in md.stem.lower() or name_lower in md.as_posix().lower():
            return md.read_text(encoding="utf-8")
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="dpc document search")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # search-content
    sc = subparsers.add_parser("search-content", aliases=["sc"], help="Search content")
    sc.add_argument("term", help="Search term")
    sc.add_argument("--format", choices=["text", "json"], default="text")

    # search (file names)
    sf = subparsers.add_parser("search", aliases=["s"], help="Search file names")
    sf.add_argument("term", help="Search term")

    # print
    pr = subparsers.add_parser("print", aliases=["p"], help="Print document")
    pr.add_argument("name", help="Document name (partial match)")

    args = parser.parse_args()

    if args.command in ("search-content", "sc"):
        results = search_content(args.term)
        if args.format == "json":
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for r in results:
                print(f"\n{r['path']} ({r['count']} matches)")
                for m in r["matches"]:
                    print(f"  L{m['line']}: {m['text']}")
        return 0

    if args.command in ("search", "s"):
        for path in search_files(args.term):
            print(path)
        return 0

    if args.command in ("print", "p"):
        content = print_doc(args.name)
        if content:
            print(content)
            return 0
        print(f"Document not found: {args.name}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
