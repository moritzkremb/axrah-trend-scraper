# Axrah Trend Scraper

Social media trend research for AXRAH across Reddit, TikTok, YouTube, and Instagram.

## How to run a scrape

```bash
bash run-scrape.sh
```

This scrapes all 4 platforms using topics from `scrape-topics.env`, writes timestamped per-platform files, and consolidates results into `outputs/latest.md`.

## Output for downstream consumers

`outputs/latest.md` is the canonical output file. It contains the latest scrape results across all platforms in a single consolidated markdown file. Other routines (e.g. CEO brief) should fetch this file via raw GitHub URL:

```
https://raw.githubusercontent.com/moritzkremb/axrah-trend-scraper/main/outputs/latest.md
```

## Changing scrape topics

Edit `scrape-topics.env` — not the shell scripts. Changes flow automatically on next run.

## Structure

- `run-scrape.sh` — main entry point
- `scrape-topics.env` — centralized topic/query config
- `outputs/latest.md` — consolidated latest scrape (what downstream routines read)
- `reddit-trends/` — raw Reddit outputs (timestamped)
- `tiktok-trends/` — raw TikTok outputs (timestamped)
- `youtube-trends/` — raw YouTube outputs (timestamped)
- `instagram-trends/` — raw Instagram outputs (timestamped)
- `.claude/skills/` — scraper scripts (Apify-based for TikTok/YouTube/Instagram, Reddit JSON API)

## Environment

Requires `APIFY_API_KEY` in `.env` (not committed to git).
