#!/usr/bin/env python3
"""ReproGate hook base helpers.

All Phase 2 ReproGate hook scripts must import and call check_disabled()
at the top of their main() function to honour REPROGATE_DISABLED=1.

Convention (INIT-02):
    import sys
    from scripts.hooks.reprogate_hook_base import check_disabled

    def main() -> int:
        check_disabled()
        # ... actual hook logic
"""
import os
import sys


def check_disabled() -> None:
    """Exit 0 (no-op) if REPROGATE_DISABLED=1 is set in the environment.

    Called by every ReproGate hook script at startup. Allows developers
    to temporarily disable all harness hook behavior without uninstalling.
    """
    if os.environ.get("REPROGATE_DISABLED") == "1":
        sys.exit(0)
