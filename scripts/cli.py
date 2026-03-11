#!/usr/bin/env python3
import argparse
import pathlib
import subprocess
import sys
from typing import List


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent


def run_script(script_name: str, args: List[str]) -> int:
    proc = subprocess.run([sys.executable, str(SCRIPT_DIR / script_name), *args], check=False)
    return proc.returncode


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Ops helper CLI.")
    parser.add_argument("command", choices=["init", "generate", "check"], help="Subcommand to run.")
    parser.add_argument("extra", nargs=argparse.REMAINDER)
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    extra = list(args.extra)
    if extra and extra[0] == "--":
        extra = extra[1:]

    if args.command == "init":
        return run_script("init.py", extra)
    if args.command == "generate":
        return run_script("generate.py", extra)
    if args.command == "check":
        return run_script("check_compliance.py", extra)
    return 1


if __name__ == "__main__":
    sys.exit(main())
