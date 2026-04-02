#!/usr/bin/env python3
"""Stop hook stub — placeholder until Phase 2 (HOOK-03) implementation."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from reprogate_hook_base import check_disabled

if check_disabled():
    sys.exit(0)

# Full implementation in Phase 2 (HOOK-03)
sys.exit(0)
