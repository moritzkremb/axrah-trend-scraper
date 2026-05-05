#!/usr/bin/env python3
"""
TikTok Scraper - Uses Apify CLI to scrape TikTok videos, profiles, and search results.
Default production actor: clockworks/tiktok-scraper

When using --search, results are filtered to the current scrape week (Monday 00:00 UTC onward)
and ranked by popularity so the output reflects this week's strongest videos.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ACTOR = "clockworks/tiktok-scraper"


def run_apify(input_data):
    """Run Apify actor via CLI and return results."""
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
            json_output = "\n".join(lines[json_start:])
            return json.loads(json_output)
    except Exception:
        pass

    print(result.stdout)
    return []


def scrape_username(username, limit=20):
    input_data = {"profiles": [username], "resultsPerPage": limit}
    return run_apify(input_data)


def scrape_search(keyword, limit=20):
    input_data = {"searchQueries": [keyword], "resultsPerPage": max(limit * 3, 20)}
    return run_apify(input_data)


def scrape_url(url, limit=20):
    input_data = {"postURLs": [url], "resultsPerPage": limit}
    return run_apify(input_data)


def week_start_utc(now=None):
    now = now or datetime.now(timezone.utc)
    start = now - timedelta(days=now.weekday())
    return start.replace(hour=0, minute=0, second=0, microsecond=0)


def popularity_score(item):
    return (
        item.get("playCount", 0)
        + item.get("diggCount", 0) * 10
        + item.get("shareCount", 0) * 15
        + item.get("commentCount", 0) * 12
        + item.get("collectCount", 0) * 8
    )


def filter_this_week(items):
    cutoff = week_start_utc()
    filtered = []
    for item in items:
        if not isinstance(item, dict):
            continue
        ts = item.get("createTime")
        if not ts:
            continue
        try:
            created = datetime.fromtimestamp(int(ts), tz=timezone.utc)
        except Exception:
            continue
        if created >= cutoff:
            filtered.append(item)
    filtered.sort(key=popularity_score, reverse=True)
    return filtered


def print_items(items, limit):
    usable = [item for item in items if isinstance(item, dict)]
    if not usable:
        print("No usable results found.")
        return

    for item in usable[:limit]:
        text = (item.get("text") or "Untitled").replace("\n", " ")[:180]
        author = item.get("authorMeta", {}) or {}
        likes = item.get("diggCount", 0)
        comments = item.get("commentCount", 0)
        views = item.get("playCount", 0)
        created = item.get("createTimeISO") or item.get("createTime") or "unknown"
        print(f"📹 {text}")
        print(f"   👤 @{author.get('name', 'unknown')} | 👁️ {views:,} | ❤️ {likes:,} | 💬 {comments:,}")
        print(f"   🗓️ {created}")
        print(f"   🔗 {item.get('webVideoUrl', '')}")
        print()


def main():
    parser = argparse.ArgumentParser(description="TikTok Scraper using Apify CLI")
    parser.add_argument("--username", "-u", help="TikTok username (without @)")
    parser.add_argument("--search", help="TikTok search keyword")
    parser.add_argument("--hashtag", help="Legacy alias; treated as a search keyword")
    parser.add_argument("--start-url", action="append", help="Ignored by Clockworks actor; kept for compatibility")
    parser.add_argument("--url", "-l", help="Direct TikTok URL")
    parser.add_argument("--location", default="US", help="Ignored by Clockworks actor; kept for compatibility")
    parser.add_argument("--sort-type", default="RELEVANCE", help="Ignored by Clockworks actor; kept for compatibility")
    parser.add_argument("--date-range", default="DEFAULT", help="Ignored by Clockworks actor; kept for compatibility")
    parser.add_argument("--include-search-keywords", action="store_true", help="Ignored by Clockworks actor; kept for compatibility")
    parser.add_argument("--limit", "-n", type=int, default=3, help="Number of top items to output")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.username and not args.search and not args.hashtag and not args.url:
        parser.print_help()
        sys.exit(1)

    if args.username:
        data = scrape_username(args.username, args.limit)
    elif args.search or args.hashtag:
        keyword = args.search or args.hashtag
        data = filter_this_week(scrape_search(keyword, args.limit))
    elif args.url:
        data = scrape_url(args.url, args.limit)
    else:
        data = []

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print_items(data, args.limit)


if __name__ == "__main__":
    main()
