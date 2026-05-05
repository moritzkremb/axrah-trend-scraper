#!/usr/bin/env python3
"""
YouTube trend scraper using the working production actor: streamers/youtube-scraper

Trend mode:
- uses searchQueries
- filters to this week
- sorts by view count
- outputs only the strongest few videos per topic
"""

import argparse
import json
import subprocess
import sys

ACTOR = "streamers/youtube-scraper"


def run_apify(input_data):
    result = subprocess.run(
        ["apify", "call", ACTOR, "-i", json.dumps(input_data), "-o"],
        capture_output=True,
        text=True,
    )
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


def usable_items(items):
    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("error") or item.get("note") == "NO_RESULTS":
            continue
        if item.get("type") not in (None, "video"):
            continue
        out.append(item)
    return out


def popularity_score(item):
    return item.get("viewCount", 0) + item.get("likes", 0) * 10 + item.get("commentsCount", 0) * 12


def scrape_search(query, limit=3):
    data = run_apify({
        "searchQueries": [query],
        "maxResults": max(limit * 4, 12),
        "maxResultsShorts": 0,
        "maxResultStreams": 0,
        "sortingOrder": "views",
        "dateFilter": "week",
        "videoType": "video",
    })
    items = usable_items(data)
    items.sort(key=popularity_score, reverse=True)
    return items[:limit]


def main():
    parser = argparse.ArgumentParser(description="YouTube trend scraper")
    parser.add_argument("--search", required=True, help="Search query")
    parser.add_argument("--limit", "-n", type=int, default=3, help="Top items to output")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON")
    args = parser.parse_args()

    data = scrape_search(args.search, args.limit)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    if not data:
        print("No results found.")
        return

    for item in data:
        title = (item.get("title") or "Untitled").replace("\n", " ")[:180]
        print(f"▶️ {title}")
        print(f"   📺 {item.get('channelName', 'unknown')} | 👁️ {item.get('viewCount', 0):,} | 💬 {item.get('commentsCount', 0):,}")
        print(f"   🗓️ {item.get('date', 'unknown')}")
        print(f"   🔗 {item.get('url', '')}")
        print()


if __name__ == "__main__":
    main()
