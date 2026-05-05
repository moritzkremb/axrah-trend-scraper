#!/usr/bin/env python3
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
        if item.get("error"):
            continue
        if item.get("type") not in (None, "video"):
            continue
        out.append(item)
    return out


def popularity_score(item):
    return item.get("viewCount", 0) + item.get("likes", 0) * 10 + item.get("commentsCount", 0) * 12


def scrape_channel(channel_url, limit=3):
    data = run_apify({
        "startUrls": [{"url": channel_url}],
        "maxResults": 12,
        "maxResultsShorts": 0,
        "maxResultStreams": 0,
        "oldestPostDate": "7 days",
        "sortVideosBy": "POPULAR",
    })
    items = usable_items(data)
    items.sort(key=popularity_score, reverse=True)
    return items[:limit]


def main():
    parser = argparse.ArgumentParser(description="YouTube account watch scraper")
    parser.add_argument("--channel-url", required=True, help="Channel URL like https://www.youtube.com/@hubermanlab")
    parser.add_argument("--limit", type=int, default=3, help="Top recent videos to print")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    data = scrape_channel(args.channel_url, args.limit)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    if not data:
        print("No recent videos found.")
        return

    for item in data:
        title = (item.get("title") or "Untitled").replace("\n", " ")[:180]
        print(f"▶️ {title}")
        print(f"   👁️ {item.get('viewCount', 0):,} | 💬 {item.get('commentsCount', 0):,}")
        print(f"   🗓️ {item.get('date', 'unknown')}")
        print(f"   🔗 {item.get('url', '')}")
        print()


if __name__ == "__main__":
    main()
