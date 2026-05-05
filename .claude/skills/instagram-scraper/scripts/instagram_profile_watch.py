#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ACTOR = "apify/instagram-scraper"


def run_apify(input_data):
    input_json = json.dumps(input_data)
    cmd = ["apify", "call", ACTOR, "-i", input_json, "-o"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    try:
        lines = result.stdout.split("\n")
        json_start = -1
        for i, line in enumerate(lines):
            if line.strip().startswith("["):
                json_start = i
                break
        if json_start >= 0:
            return json.loads("\n".join(lines[json_start:]))
    except Exception:
        pass
    print(result.stdout)
    return []


def week_start_utc(now=None):
    now = now or datetime.now(timezone.utc)
    start = now - timedelta(days=now.weekday())
    return start.replace(hour=0, minute=0, second=0, microsecond=0)


def parse_created(item):
    value = item.get("timestamp")
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def popularity_score(item):
    return (
        item.get("likesCount", 0)
        + item.get("commentsCount", 0) * 12
        + item.get("videoViewCount", 0)
    )


def filter_this_week(items):
    cutoff = week_start_utc()
    filtered = []
    for item in items:
        if not isinstance(item, dict):
            continue
        created = parse_created(item)
        if created and created >= cutoff:
            filtered.append(item)
    filtered.sort(key=popularity_score, reverse=True)
    return filtered


def scrape_profile(username, limit=3):
    input_data = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "posts",
        "resultsLimit": 30,
        "onlyPostsNewerThan": week_start_utc().date().isoformat(),
    }
    return filter_this_week(run_apify(input_data))[:limit]


def main():
    parser = argparse.ArgumentParser(description="Instagram profile watch scraper")
    parser.add_argument("--username", required=True, help="Instagram username without @")
    parser.add_argument("--limit", type=int, default=3, help="Top recent posts to print")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    data = scrape_profile(args.username, args.limit)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    if not data:
        print("No recent posts found.")
        return

    for item in data:
        caption = (item.get("caption") or "Untitled").replace("\n", " ")[:180]
        likes = item.get("likesCount", 0)
        comments = item.get("commentsCount", 0)
        views = item.get("videoViewCount", 0)
        created = parse_created(item)
        created_str = created.isoformat() if created else "unknown"
        print(f"📸 {caption}")
        print(f"   👁️ {views:,} | ❤️ {likes:,} | 💬 {comments:,}")
        print(f"   🗓️ {created_str}")
        print(f"   🔗 {item.get('url', '')}")
        print()


if __name__ == "__main__":
    main()
