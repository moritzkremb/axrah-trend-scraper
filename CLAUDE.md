# Axrah Trend Scraper

Social media trend research for AXRAH across Reddit, TikTok, YouTube, and Instagram.

## How to run a scrape

```bash
bash run-scrape.sh
```

Scrapes Reddit (11 relevant subreddits), TikTok, YouTube, Instagram + influencer watchlists. Commits consolidated output to `outputs/latest.md`.

## Output for downstream consumers

`outputs/latest.md` is the canonical output file. It contains the latest scrape results in a single consolidated markdown file. The CEO brief routine (separate repo: `axrah-ceo-brief`) fetches this via raw GitHub URL:

```
https://raw.githubusercontent.com/moritzkremb/axrah-trend-scraper/main/outputs/latest.md
```

## Changing scrape topics

Edit `scrape-topics.env` — not the shell scripts. Changes flow automatically on next run.

## Structure

- `run-scrape.sh` — main entry point (runs all scrapers + watchlists)
- `scrape-topics.env` — centralized topic/query config
- `outputs/latest.md` — consolidated latest scrape (Reddit + watchlists)
- `reddit-trends/` — raw Reddit outputs (timestamped)
- `tiktok-trends/` — raw TikTok outputs (timestamped)
- `youtube-trends/` — raw YouTube outputs (timestamped)
- `instagram-trends/` — raw Instagram outputs (timestamped)
- `instagram-account-watch/` — influencer IG profile watch
- `youtube-account-watch/` — influencer YT channel watch
- `.claude/skills/` — scraper scripts (Apify-based for TikTok/YouTube/Instagram, Reddit JSON API)

## Environment

Requires `APIFY_API_KEY` in `.env` (not committed to git).
