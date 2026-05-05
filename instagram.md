# Instagram Notes

This file is **reference only**. It does **not** control the live scrape job.

## What actually controls runtime

- `content/research/scrape-topics.env` — active hashtags/topics
- `content/research/run-scrape.sh` — runtime orchestration
- OpenClaw cron job — weekly trigger
- `skills/instagram-scraper/scripts/instagram_scraper.py` — actual scraper behavior

## Current runtime usage

The weekly scrape uses Instagram hashtags defined in `scrape-topics.env` and writes output to:

- `content/research/instagram-trends/YYYY-MM-DD.md`

## Useful command pattern

```bash
python3 ~/.openclaw/workspace/skills/instagram-scraper/scripts/instagram_scraper.py --hashtag "redlighttherapy" --limit 20
```

## Notes

- The underlying scraper is Apify-backed through the Instagram scraper skill.
- Instagram is usually the most temperamental source because anti-scraping is stricter.
- Use this file only for Instagram-specific strategy notes or future expansion ideas.
- If you want to change the active weekly hashtags, edit `scrape-topics.env` instead.
