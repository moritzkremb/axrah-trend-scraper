#!/usr/bin/env python3
"""
Instagram Scraper - Uses Apify CLI to scrape Instagram hashtags.
Default production actor: apify/instagram-hashtag-scraper

For trend scraping, results are filtered to the current scrape week and ranked by engagement
so the output reflects this week's strongest Instagram posts.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ACTOR = "apify/instagram-hashtag-scraper"


def run_apify(input_data):
    import os
    import urllib.request

    token = os.environ.get("APIFY_API_KEY", "")
    actor_id = ACTOR.replace("/", "~")
    url = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={token}"
    body = json.dumps(input_data).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error calling Apify: {e}", file=sys.stderr)
        return []


def week_start_utc(now=None):
    now = now or datetime.now(timezone.utc)
    start = now - timedelta(days=now.weekday())
    return start.replace(hour=0, minute=0, second=0, microsecond=0)


def popularity_score(item):
    likes = item.get("likesCount", item.get("likeCount", 0)) or 0
    comments = item.get("commentsCount", item.get("commentCount", 0)) or 0
    views = item.get("videoViewCount", 0) or 0
    return likes + comments * 12 + views


def parse_created(item):
    for key in ("timestamp", "takenAtTimestamp", "createdAt"):
        value = item.get(key)
        if not value:
            continue
        try:
            if isinstance(value, (int, float)):
                return datetime.fromtimestamp(int(value), tz=timezone.utc)
            if isinstance(value, str) and value.endswith("Z"):
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            if isinstance(value, str):
                return datetime.fromisoformat(value)
        except Exception:
            continue
    return None


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


def scrape_hashtag(hashtag, limit=20):
    clean = hashtag.lstrip("#").replace(" ", "")
    input_data = {"hashtags": [clean], "resultsLimit": max(limit * 3, 20)}
    return run_apify(input_data)


def main():
    parser = argparse.ArgumentParser(description="Instagram Scraper using Apify CLI")
    parser.add_argument("--hashtag", help="Instagram hashtag (with or without #)")
    parser.add_argument("--search", help="Legacy alias; treated as hashtag/topic")
    parser.add_argument("--limit", "-n", type=int, default=3, help="Number of top items to output")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.hashtag and not args.search:
        parser.print_help()
        sys.exit(1)

    topic = args.hashtag or args.search
    data = filter_this_week(scrape_hashtag(topic, args.limit))

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        if not data:
            print("No results found.")
            return

        for item in data[:args.limit]:
            caption = (item.get("caption") or "Untitled").replace("\n", " ")[:180]
            owner = item.get("ownerUsername") or item.get("owner", {}).get("username") or "unknown"
            likes = item.get("likesCount", item.get("likeCount", 0)) or 0
            comments = item.get("commentsCount", item.get("commentCount", 0)) or 0
            created = parse_created(item)
            created_str = created.isoformat() if created else "unknown"
            url = item.get("url") or item.get("displayUrl") or ""
            print(f"📸 {caption}")
            print(f"   👤 @{owner} | ❤️ {likes:,} | 💬 {comments:,}")
            print(f"   🗓️ {created_str}")
            print(f"   🔗 {url}")
            print()


if __name__ == "__main__":
    main()
