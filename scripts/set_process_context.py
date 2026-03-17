#!/usr/bin/env python3
import argparse
import json
import pathlib
from datetime import datetime, timezone
from typing import Dict, List


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTEXT_FILE = ROOT / ".dpc" / "process-context.json"

VALID_PROCESSES = {"G0", "P0", "P1", "P2", "P3", "P4", "S1", "S2", "S3", "S4", "NONE"}
TEAM_ELIGIBLE_PROCESSES = {"P3", "P4", "S3", "S1"}

PROFILE_ROLE_MAP: Dict[str, List[str]] = {
    "ANALYSIS_MIN2": ["analyst", "verifier"],
    "DELIVERY_MIN3": ["executor", "verifier", "recorder"],
    "REVIEW_MIN2": ["reviewer", "verifier"],
    "DOC_MIN2": ["recorder", "verifier"],
    "SINGLE_MIN1": ["executor"],
}

PROCESS_PROFILE_MAP = {
    "G0": "ANALYSIS_MIN2",
    "P0": "ANALYSIS_MIN2",
    "P1": "ANALYSIS_MIN2",
    "P2": "ANALYSIS_MIN2",
    "P3": "DELIVERY_MIN3",
    "P4": "DELIVERY_MIN3",
    "S1": "REVIEW_MIN2",
    "S2": "DOC_MIN2",
    "S3": "DELIVERY_MIN3",
    "S4": "DOC_MIN2",
    "NONE": "SINGLE_MIN1",
}

VALID_LOGICAL_ROLES = {"analyst", "executor", "verifier", "recorder", "reviewer"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set dpc selected process context.")
    parser.add_argument("--process", required=False, help="Selected process id (G0, P0~P4, S1~S4, NONE)")
    parser.add_argument("--wp", required=False, help="Target WP id (optional)")
    parser.add_argument(
        "--team-mode",
        choices=["auto", "single", "team", "none"],
        default="auto",
        help="Execution mode hint",
    )
    parser.add_argument(
        "--profile",
        required=False,
        help="Logical team profile id (ANALYSIS_MIN2, DELIVERY_MIN3, REVIEW_MIN2, DOC_MIN2, SINGLE_MIN1)",
    )
    parser.add_argument(
        "--roles",
        required=False,
        help="Comma-separated logical roles (analyst,executor,verifier,recorder,reviewer)",
    )
    parser.add_argument(
        "--members",
        required=False,
        help="Comma-separated member:role mapping. Example: member-a:executor,member-b:verifier,member-c:recorder",
    )
    parser.add_argument("--print-defaults", action="store_true", help="Print process/profile defaults")
    parser.add_argument("--clear", action="store_true", help="Clear context file")
    return parser.parse_args()


def dedupe_keep_order(values: List[str]) -> List[str]:
    seen = set()
    output: List[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def parse_roles(raw_roles: str) -> List[str]:
    if not raw_roles:
        return []
    values = [item.strip().lower() for item in raw_roles.split(",") if item.strip()]
    values = dedupe_keep_order(values)
    invalid = [role for role in values if role not in VALID_LOGICAL_ROLES]
    if invalid:
        allowed = ", ".join(sorted(VALID_LOGICAL_ROLES))
        raise SystemExit(f"Invalid role(s): {', '.join(invalid)}. Allowed: {allowed}")
    return values


def parse_members(raw_members: str) -> List[Dict[str, str]]:
    if not raw_members:
        return []

    entries = [item.strip() for item in raw_members.split(",") if item.strip()]
    members: List[Dict[str, str]] = []
    seen_names = set()

    for entry in entries:
        if ":" not in entry:
            raise SystemExit(
                "Invalid --members entry. Use member:role format, example: member-a:executor"
            )

        member, role = entry.split(":", 1)
        member = member.strip()
        role = role.strip().lower()

        if not member:
            raise SystemExit("Invalid --members entry: member name cannot be empty.")
        if member in seen_names:
            raise SystemExit(f"Duplicate member name in --members: {member}")
        if role not in VALID_LOGICAL_ROLES:
            allowed = ", ".join(sorted(VALID_LOGICAL_ROLES))
            raise SystemExit(f"Invalid member role '{role}'. Allowed: {allowed}")

        seen_names.add(member)
        members.append({"member": member, "role": role})

    return members


def print_defaults() -> int:
    print("Default process -> profile mapping:")
    for process in sorted(PROCESS_PROFILE_MAP):
        print(f"- {process}: {PROCESS_PROFILE_MAP[process]}")
    print("\nProfile -> logical roles:")
    for profile in sorted(PROFILE_ROLE_MAP):
        roles = ", ".join(PROFILE_ROLE_MAP[profile])
        print(f"- {profile}: {roles}")
    print("\nTeam-eligible processes: " + ", ".join(sorted(TEAM_ELIGIBLE_PROCESSES)))
    print("\nTeam member mapping format:")
    print("- --members member-a:executor,member-b:verifier,member-c:recorder")
    return 0


def main() -> int:
    args = parse_args()

    if args.print_defaults:
        return print_defaults()

    if args.clear:
        if CONTEXT_FILE.exists():
            CONTEXT_FILE.unlink()
            print(f"Cleared context: {CONTEXT_FILE.relative_to(ROOT)}")
        else:
            print("Context already empty.")
        return 0

    process = (args.process or "").strip().upper()
    if process not in VALID_PROCESSES:
        values = ", ".join(sorted(VALID_PROCESSES))
        raise SystemExit(f"Invalid --process value: {process or '<empty>'}. Allowed: {values}")

    profile = (args.profile or "").strip().upper()
    if profile and profile not in PROFILE_ROLE_MAP:
        values = ", ".join(sorted(PROFILE_ROLE_MAP))
        raise SystemExit(f"Invalid --profile value: {profile}. Allowed: {values}")

    required_profile = PROCESS_PROFILE_MAP[process]
    required_roles = PROFILE_ROLE_MAP[required_profile]

    active_roles = parse_roles(args.roles or "")
    assigned_members = parse_members(args.members or "")
    member_roles = dedupe_keep_order([item["role"] for item in assigned_members])

    team_mode = args.team_mode
    active_profile = profile
    if not active_profile:
        if team_mode == "team":
            active_profile = required_profile
        elif team_mode == "single" and process in TEAM_ELIGIBLE_PROCESSES:
            active_profile = required_profile
        elif team_mode in {"single", "none"}:
            active_profile = "SINGLE_MIN1"
        else:
            active_profile = required_profile

    if not active_roles and assigned_members:
        active_roles = member_roles

    if not active_roles and team_mode == "single" and process in TEAM_ELIGIBLE_PROCESSES:
        active_roles = required_roles
    elif not active_roles and team_mode != "team":
        active_roles = PROFILE_ROLE_MAP.get(active_profile, ["executor"])

    missing_required = [role for role in required_roles if role not in active_roles]

    members_required = team_mode == "team" and process in TEAM_ELIGIBLE_PROCESSES
    missing_member_roles: List[str] = []
    if members_required:
        missing_member_roles = [role for role in required_roles if role not in member_roles]

    profile_satisfied = len(missing_required) == 0
    member_profile_satisfied = (not members_required) or (
        len(assigned_members) > 0 and len(missing_member_roles) == 0
    )

    CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "selected_process": process,
        "selected_wp": (args.wp or "").strip(),
        "team_mode": team_mode,
        "team_eligible": process in TEAM_ELIGIBLE_PROCESSES,
        "required_profile_id": required_profile,
        "required_logical_roles": required_roles,
        "active_profile_id": active_profile,
        "active_logical_roles": active_roles,
        "missing_required_roles": missing_required,
        "profile_satisfied": profile_satisfied,
        "assigned_members": assigned_members,
        "member_roles": member_roles,
        "missing_member_roles": missing_member_roles,
        "members_required": members_required,
        "member_profile_satisfied": member_profile_satisfied,
        "updated_at": now_iso(),
    }
    CONTEXT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated context: {CONTEXT_FILE.relative_to(ROOT)}")
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
