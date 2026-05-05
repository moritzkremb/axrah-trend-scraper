# Social Media Research

This folder contains trend research from Reddit, TikTok, YouTube, and Instagram for AXRAH-relevant social/content intelligence.

## Central topic control

**Single source of truth:** `content/research/scrape-topics.env`

Update that file to change the active topics, search queries, or hashtags. `run-scrape.sh` reads from it at runtime, so changes there automatically flow into the actual scrape job.

## Current target topics

- fat loss
- anti inflammation
- biohacking
- skin regeneration
- muscle recovery
- pain relief
- hair growth

## TikTok strategy note

TikTok is now configured as a **search-first workflow** for `apidojo/tiktok-scraper`.

That means:
- use broader search keywords
- pair them with TikTok search URLs where useful
- do **not** treat hashtag-only input as the main strategy anymore

## Structure

```
axrah_apify_scrapers/
├── .claude/skills/          # installed scraper skills (apify, instagram, reddit, tiktok, youtube)
├── .env                     # APIFY_API_KEY
├── scrape-instructions.md   # human-readable workflow + system map
├── scrape-topics.env        # centralized active topics/queries/hashtags
├── run-scrape.sh            # runtime entry point — runs all 4 platform scrapers
├── run-instagram-account-watch.sh
├── run-youtube-account-watch.sh
├── reddit-trends/           # Reddit markdown outputs
├── tiktok-trends/           # TikTok markdown outputs
├── youtube-trends/          # YouTube markdown outputs
├── instagram-trends/        # Instagram markdown outputs
├── instagram-account-watch/ # Instagram profile watch outputs
├── youtube-account-watch/   # YouTube channel watch outputs
└─�� docs/                    # Apify CLI reference & guide
```

## Runtime flow

1. Cron triggers `run-scrape.sh`
2. `run-scrape.sh` loads `scrape-topics.env`
3. The scraper runs for each platform every time the job is triggered
4. Each run writes to a new unique timestamped markdown file per platform
5. Results are saved in the platform trend folders without overwriting earlier same-day runs

## Platform tools

- **Reddit**: `python3 .claude/skills/reddit-scraper/scripts/reddit_scraper.py`
- **TikTok**: `python3 .claude/skills/tiktok-scraper/scripts/tiktok_scraper.py`
- **YouTube**: `python3 .claude/skills/youtube-scraper/scripts/youtube_scraper.py`
- **Instagram**: `python3 .claude/skills/instagram-scraper/scripts/instagram_scraper.py`

## Rule

If you want to update scrape targets, edit `scrape-topics.env` first — not the hardcoded command lines in `run-scrape.sh`.
