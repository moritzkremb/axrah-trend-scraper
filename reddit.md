# Reddit Notes

This file is **reference only**. It does **not** control the live scrape job.

## What actually controls runtime

- `content/research/scrape-topics.env` — active search topics/queries
- `content/research/run-scrape.sh` — runtime orchestration
- OpenClaw cron job — weekly trigger
- `skills/reddit-scraper/scripts/reddit_scraper.py` — actual scraper behavior

## Current runtime usage

The weekly scrape uses Reddit search queries defined in `scrape-topics.env` and writes output to:

- `content/research/reddit-trends/YYYY-MM-DD.md`

## Useful command pattern

```bash
python3 ~/.openclaw/workspace/skills/reddit-scraper/scripts/reddit_scraper.py --search "red light therapy fat loss" --limit 20 --time week
```

## Notes

- Use this file only for Reddit-specific strategy notes or future expansion ideas.
- If you want to change the active weekly topics, edit `scrape-topics.env` instead.
