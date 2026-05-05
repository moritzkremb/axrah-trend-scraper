#!/bin/bash

# Social Media Trends Scraping Script
# Runs all 4 platform scrapers and saves to trend folders
# Topic targeting is centralized in scrape-topics.env

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

set -a
source "$SCRIPT_DIR/scrape-topics.env"
set +a

DATE=$(date +%Y-%m-%d)
STAMP=$(date +%H%M%S)
RUN_ID="${DATE}-${STAMP}"

reddit_out="$SCRIPT_DIR/reddit-trends/$RUN_ID.md"
tiktok_out="$SCRIPT_DIR/tiktok-trends/$RUN_ID.md"
youtube_out="$SCRIPT_DIR/youtube-trends/$RUN_ID.md"
instagram_out="$SCRIPT_DIR/instagram-trends/$RUN_ID.md"

echo "=== Starting Social Trends Scrape - $RUN_ID ==="
echo "Topics: ${TOPIC_LABELS[*]}"
echo "Mode: always scrape current week and create a new unique file per run"

echo "Reddit: Scraping..."
: > "$reddit_out"
for query in "${REDDIT_QUERIES[@]}"; do
    python3 "$SCRIPT_DIR/.claude/skills/reddit-scraper/scripts/reddit_scraper.py" --search "$query" --limit 20 --time week >> "$reddit_out"
done

echo "TikTok: Scraping..."
: > "$tiktok_out"
for i in "${!TIKTOK_KEYWORDS[@]}"; do
    keyword="${TIKTOK_KEYWORDS[$i]}"
    start_url="${TIKTOK_START_URLS[$i]}"
    python3 "$SCRIPT_DIR/.claude/skills/tiktok-scraper/scripts/tiktok_scraper.py" \
        --search "$keyword" \
        --start-url "$start_url" \
        --location "$TIKTOK_LOCATION" \
        --sort-type "$TIKTOK_SORT_TYPE" \
        --date-range "$TIKTOK_DATE_RANGE" \
        $( [ "$TIKTOK_INCLUDE_SEARCH_KEYWORDS" = true ] && printf '%s' '--include-search-keywords' ) \
        --limit "$TIKTOK_MAX_ITEMS" >> "$tiktok_out"
done

echo "YouTube: Scraping..."
: > "$youtube_out"
for query in "${YOUTUBE_QUERIES[@]}"; do
    python3 "$SCRIPT_DIR/.claude/skills/youtube-scraper/scripts/youtube_scraper.py" --search "$query" --limit 3 >> "$youtube_out"
done

echo "Instagram: Scraping..."
: > "$instagram_out"
for hashtag in "${INSTAGRAM_HASHTAGS[@]}"; do
    python3 "$SCRIPT_DIR/.claude/skills/instagram-scraper/scripts/instagram_scraper.py" --hashtag "$hashtag" --limit 20 >> "$instagram_out"
done

echo "Consolidating latest.md..."
latest="$SCRIPT_DIR/outputs/latest.md"
mkdir -p "$SCRIPT_DIR/outputs"

{
  echo "# Trend Scrape — $RUN_ID"
  echo ""
  echo "## Reddit"
  echo ""
  # Strip long post bodies (📝 lines) to keep it concise
  grep -v "^   📝" "$reddit_out"
  echo ""
  echo "## TikTok"
  echo ""
  cat "$tiktok_out"
  echo ""
  echo "## YouTube"
  echo ""
  cat "$youtube_out"
  echo ""
  echo "## Instagram"
  echo ""
  cat "$instagram_out"
} > "$latest"

echo "=== Scrape Complete — outputs/latest.md updated ==="
