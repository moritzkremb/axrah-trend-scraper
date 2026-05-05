# TikTok Notes

This file is **reference only**. It does **not** control the live scrape job.

## What actually controls runtime

- `content/research/scrape-topics.env` — active hashtags/topics
- `content/research/run-scrape.sh` — runtime orchestration
- OpenClaw cron job — weekly trigger
- `skills/tiktok-scraper/scripts/tiktok_scraper.py` — actual scraper behavior

## Current runtime usage

The weekly scrape uses TikTok hashtags defined in `scrape-topics.env` and writes output to:

- `content/research/tiktok-trends/YYYY-MM-DD.md`

## Useful command pattern

```bash
python3 ~/.openclaw/workspace/skills/tiktok-scraper/scripts/tiktok_scraper.py --hashtag "redlighttherapy" --limit 20
```

## Notes

- The underlying scraper is Apify-backed through the TikTok scraper skill.
- Use this file only for TikTok-specific strategy notes or future expansion ideas.
- If you want to change the active weekly hashtags, edit `scrape-topics.env` instead.
