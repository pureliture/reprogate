#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
    import requests
except ImportError:
    print("Please install required packages: pip install pyyaml requests")
    sys.exit(1)


def get_github_api_headers() -> Dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    return {}


def fetch_github_state_cli(repo: str, kind: str, number: int) -> str:
    """Fallback to gh cli if no token is available."""
    try:
        cmd = ["gh", kind, "view", str(number), "--repo", repo, "--json", "state", "-q", ".state"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().lower()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "not_found"


def fetch_github_state(repo: str, kind: str, number: int) -> str:
    """Fetch state of an issue or PR. Return 'open', 'closed', 'merged', or 'not_found'."""
    headers = get_github_api_headers()
    if not headers:
        return fetch_github_state_cli(repo, kind, number)

    url = f"https://api.github.com/repos/{repo}/{'pulls' if kind == 'pr' else 'issues'}/{number}"
    resp = requests.get(url, headers=headers)
    
    if resp.status_code != 200:
        return "not_found"
    
    data = resp.json()
    state = data.get("state", "closed").lower()
    
    if kind == "pr" and data.get("merged_at") is not None:
        return "merged"
    
    return state


def evaluate_file(item: Dict[str, Any], repo_root: Path) -> float:
    path = repo_root / item.get("path", "")
    if not path.exists() or not path.is_file():
        return 0.0

    content = path.read_text(encoding="utf-8")
    substantive = item.get("substantive", {})
    
    if not substantive:
        return 1.0  # Just existence is enough

    if len(content) < substantive.get("min_chars", 0):
        return 0.25

    forbidden = substantive.get("forbidden", [])
    for word in forbidden:
        if word in content:
            return 0.25

    return 1.0


def calculate_item_score(item: Dict[str, Any], repo: str, repo_root: Path) -> float:
    kind = item.get("kind")
    
    if kind == "issue":
        state = fetch_github_state(repo, "issue", item["number"])
        if state == "open": return 0.35
        if state == "closed": return 1.0
        return 0.0
        
    elif kind == "pr":
        state = fetch_github_state(repo, "pr", item["number"])
        if state == "open": return 0.60
        if state == "merged": return 1.0
        if state == "closed": return 0.0 # closed without merge
        return 0.0
        
    elif kind == "file":
        return evaluate_file(item, repo_root)
        
    elif kind == "manual_placeholder":
        return float(item.get("score", 0.0))
        
    return 0.0


def generate_progress_bar(percent: float, width: int = 10) -> str:
    filled = int((percent / 100) * width)
    return "█" * filled + "░" * (width - filled)


def get_status_label(percent: float) -> str:
    if percent <= 0: return "Not started"
    if percent < 40: return "Seeded"
    if percent < 70: return "Drafted"
    if percent < 100: return "In progress"
    return "Closed"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    repo_root = Path.cwd()
    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    repo = config.get("repo")
    
    stages_result = []
    total_weighted_score = 0.0
    total_weight = 0.0
    
    print(f"Building progress report for {repo}...")

    for stage in config.get("stages", []):
        stage_weight = stage.get("weight", 1)
        item_total_weight = 0.0
        item_weighted_score = 0.0
        
        for item in stage.get("items", []):
            weight = item.get("weight", 1)
            score = calculate_item_score(item, repo, repo_root)
            item_total_weight += weight
            item_weighted_score += score * weight
            print(f"  [{stage['id']}] {item['kind']} {item.get('number', item.get('path', item['id']))}: score={score:.2f}")

        stage_score = item_weighted_score / item_total_weight if item_total_weight > 0 else 0.0
        stage_percent = round(stage_score * 100)
        
        stages_result.append({
            "id": stage["id"],
            "title": stage["title"],
            "score": stage_score,
            "percent": stage_percent,
            "status": get_status_label(stage_percent)
        })
        
        total_weighted_score += stage_score * stage_weight
        total_weight += stage_weight

    overall_score = total_weighted_score / total_weight if total_weight > 0 else 0.0
    overall_percent = round(overall_score * 100)
    overall_status = get_status_label(overall_percent)

    # 1. Output JSON
    payload = {
        "overall_percent": overall_percent,
        "overall_status": overall_status,
        "stages": stages_result
    }
    
    # Meaningful hash (without timestamp) could be just the dump of payload
    with open(args.output_json, "w", encoding="utf-8") as f:
        full_json = {**payload, "generated_at": datetime.now(timezone.utc).isoformat()}
        json.dump(full_json, f, indent=2, ensure_ascii=False)

    # 2. Output Markdown
    md_lines = [
        "# ReproGate Progress Report\n",
        "> Generated from roadmap + issue/PR/file state.",
        "> Do not edit manually.\n",
        "## Snapshot\n",
        f"- Overall: **{overall_percent}%**",
        f"- Status: **{overall_status}**",
        f"- Last updated: `{datetime.now(timezone.utc).isoformat()}`\n",
        "```mermaid",
        "pie showData",
        "    title Roadmap Progress"
    ]
    
    for s in stages_result:
        md_lines.append(f'    "{s["title"]}" : {s["percent"]}')
    
    md_lines.extend([
        "```\n",
        "## Stage Board\n",
        "| Area | Status | Progress | Bar |",
        "| ---- | ------ | -------: | --- |"
    ])
    
    for s in stages_result:
        bar = generate_progress_bar(s["percent"])
        md_lines.append(f'| {s["title"]} | {s["status"]} | {s["percent"]}% | `{bar}` |')

    with open(args.output_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

    print(f"Report generated successfully. Overall: {overall_percent}%")


if __name__ == "__main__":
    main()
