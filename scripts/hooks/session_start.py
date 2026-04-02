#!/usr/bin/env python3
"""SessionStart hook stub — placeholder until Phase 2 (HOOK-02) implementation."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from reprogate_hook_base import check_disabled

if check_disabled():
    sys.exit(0)

# Full implementation in Phase 2 (HOOK-02)
sys.exit(0)
