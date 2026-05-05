#!/bin/bash

# Social Media Trends Scraping Script
# Runs all platform scrapers and saves to trend folders
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

# --- Reddit: subreddit-specific top posts ---
echo "Reddit: Scraping ${#REDDIT_SUBREDDITS[@]} subreddits..."
: > "$reddit_out"
for sub in "${REDDIT_SUBREDDITS[@]}"; do
    echo "  r/$sub"
    python3 "$SCRIPT_DIR/.claude/skills/reddit-scraper/scripts/reddit_scraper.py" \
        --subreddit "$sub" --sort "$REDDIT_SORT" --time "$REDDIT_TIME" --limit "$REDDIT_LIMIT" >> "$reddit_out"
done

# --- TikTok ---
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

# --- YouTube ---
echo "YouTube: Scraping..."
: > "$youtube_out"
for query in "${YOUTUBE_QUERIES[@]}"; do
    python3 "$SCRIPT_DIR/.claude/skills/youtube-scraper/scripts/youtube_scraper.py" --search "$query" --limit 3 >> "$youtube_out"
done

# --- Instagram ---
echo "Instagram: Scraping..."
: > "$instagram_out"
for hashtag in "${INSTAGRAM_HASHTAGS[@]}"; do
    python3 "$SCRIPT_DIR/.claude/skills/instagram-scraper/scripts/instagram_scraper.py" --hashtag "$hashtag" --limit 20 >> "$instagram_out"
done

# --- Account watchlists ---
echo "Instagram Account Watch..."
ig_watch_out="$SCRIPT_DIR/instagram-account-watch/$DATE.md"
bash "$SCRIPT_DIR/run-instagram-account-watch.sh"

echo "YouTube Account Watch..."
yt_watch_out="$SCRIPT_DIR/youtube-account-watch/$DATE.md"
bash "$SCRIPT_DIR/run-youtube-account-watch.sh"

# --- Consolidate latest.md (Reddit + watchlists only) ---
echo "Consolidating latest.md..."
latest="$SCRIPT_DIR/outputs/latest.md"
mkdir -p "$SCRIPT_DIR/outputs"

{
  echo "# Trend Scrape — $RUN_ID"
  echo ""
  echo "## Reddit (top posts this week from relevant subreddits)"
  echo ""
  grep -v "^   📝" "$reddit_out"
  echo ""
  echo "## Instagram Account Watch"
  echo ""
  cat "$ig_watch_out"
  echo ""
  echo "## YouTube Account Watch"
  echo ""
  cat "$yt_watch_out"
} > "$latest"

echo "=== Scrape Complete — outputs/latest.md updated ==="
