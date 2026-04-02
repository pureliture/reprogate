#!/usr/bin/env python3
"""reprogate disable — removes ReproGate hook entries from .claude/settings.json.

Only removes hook entries tagged with _reprogate: true.
Non-ReproGate hooks (e.g., GSD hooks) are preserved.
"""
import argparse
import json
import pathlib
import sys
from typing import Any, Dict, List


ROOT = pathlib.Path(__file__).resolve().parents[1]


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove ReproGate hook configuration from .claude/settings.json."
    )
    parser.add_argument(
        "--settings",
        default=str(ROOT / ".claude" / "settings.json"),
        help="Path to settings.json.",
    )
    return parser.parse_args(argv)


def remove_reprogate_hooks(settings_path: pathlib.Path) -> None:
    """Remove all hook entries tagged with _reprogate: true from settings.json.

    Leaves all non-ReproGate entries intact.
    Removes entire event key if no hooks remain after filtering.
    """
    if not settings_path.exists():
        return
    data: Dict[str, Any] = json.loads(settings_path.read_text(encoding="utf-8"))
    hooks = data.get("hooks", {})
    for event in list(hooks.keys()):
        filtered_groups = []
        for group in hooks[event]:
            remaining_hooks = [
                h for h in group.get("hooks", [])
                if not h.get("_reprogate")
            ]
            if remaining_hooks:
                # Rebuild group with non-reprogate hooks only
                new_group = {k: v for k, v in group.items() if k != "hooks"}
                new_group["hooks"] = remaining_hooks
                filtered_groups.append(new_group)
        if filtered_groups:
            hooks[event] = filtered_groups
        else:
            del hooks[event]
    settings_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    settings_path = pathlib.Path(args.settings)
    if not settings_path.is_absolute():
        settings_path = ROOT / settings_path
    remove_reprogate_hooks(settings_path)
    print(f"Removed ReproGate hooks from {settings_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
