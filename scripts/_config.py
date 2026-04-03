#!/usr/bin/env python3
"""Shared config utilities for ReproGate scripts."""
from typing import Any, Dict


def merge_config_defaults(loaded: Dict[str, Any], defaults: Dict[str, Any]) -> None:
    """Merge defaults into loaded config in-place (one level deep for dict values).

    For each key in defaults:
    - If missing from loaded, copy the default value.
    - If both values are dicts, merge one level deeper (sub-keys only).
    """
    for key, default_value in defaults.items():
        if key not in loaded:
            loaded[key] = default_value
        elif isinstance(default_value, dict) and isinstance(loaded.get(key), dict):
            for sub_key, sub_default in default_value.items():
                if sub_key not in loaded[key]:
                    loaded[key][sub_key] = sub_default
