#!/bin/bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WATCHLIST="$SCRIPT_DIR/instagram-account-watchlist.txt"
OUT_DIR="$SCRIPT_DIR/instagram-account-watch"
DATE=$(date +%Y-%m-%d)
OUT_FILE="$OUT_DIR/$DATE.md"

mkdir -p "$OUT_DIR"
: > "$OUT_FILE"

echo "# Instagram Account Watch — $DATE" >> "$OUT_FILE"
echo >> "$OUT_FILE"

while IFS= read -r handle; do
  [[ -z "$handle" ]] && continue
  [[ "$handle" =~ ^# ]] && continue
  echo "## @$handle" >> "$OUT_FILE"
  if python3 "$SCRIPT_DIR/.claude/skills/instagram-scraper/scripts/instagram_profile_watch.py" --username "$handle" --limit 3 < /dev/null >> "$OUT_FILE" 2>&1; then
    :
  else
    echo "Profile scrape failed for @$handle" >> "$OUT_FILE"
  fi
  echo >> "$OUT_FILE"
done < "$WATCHLIST"

echo "$OUT_FILE"
