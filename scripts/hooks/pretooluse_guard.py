#!/usr/bin/env python3
"""
Stub pretooluse_guard.py for worktree execution.
This is a minimal stub that allows Bash commands to proceed unblocked.
The full implementation lives in the gsd workspace.
"""
import sys

# Read stdin and pass through (no-op guard)
data = sys.stdin.read()
sys.stdout.write(data)
sys.exit(0)
