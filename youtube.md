# YouTube Notes

This file is **reference only**. It does **not** control the live scrape job.

## What actually controls runtime

- `content/research/scrape-topics.env` — active search topics/queries
- `content/research/run-scrape.sh` — runtime orchestration
- OpenClaw cron job — weekly trigger
- `skills/youtube-scraper/scripts/youtube_scraper.py` — actual scraper behavior

## Current runtime usage

The weekly scrape uses YouTube queries defined in `scrape-topics.env` and writes output to:

- `content/research/youtube-trends/YYYY-MM-DD.md`

## Useful command pattern

```bash
python3 ~/.openclaw/workspace/skills/youtube-scraper/scripts/youtube_scraper.py --search "red light therapy fat loss" --limit 15
```

## Notes

- The underlying scraper is Apify-backed through the YouTube scraper skill.
- Use this file only for YouTube-specific strategy notes or future expansion ideas.
- If you want to change the active weekly queries, edit `scrape-topics.env` instead.
