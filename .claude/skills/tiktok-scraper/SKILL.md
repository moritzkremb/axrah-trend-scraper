---
name: tiktok
description: "Scrape TikTok videos, users, hashtags, and comments using Apify. Use for trend research, competitor analysis, and content monitoring."
---

# TikTok Scraper

Scrape TikTok data using Apify actors. Default actor is **apidojo/tiktok-scraper**.

## Quick Start

```bash
# Scrape user profile videos
python3 .claude/skills/tiktok-scraper/scripts/tiktok_scraper.py --username bullieyebrow

# Scrape hashtag videos
python3 .claude/skills/tiktok-scraper/scripts/tiktok_scraper.py --hashtag wellness

# Scrape with limit
python3 .claude/skills/tiktok-scraper/scripts/tiktok_scraper.py --hashtag trending --limit 50
```

## Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--username` | `-u` | TikTok username (without @) | - |
| `--hashtag` | - | Hashtag to scrape | - |
| `--url` | `-l` | Direct TikTok URL | - |
| `--limit` | `-n` | Number of items | 20 |
| `--json` | `-j` | Output as JSON | false |

## Available Actors

- **apidojo/tiktok-scraper** — Current default actor
- **clockworks/tiktok-scraper** — Legacy general-purpose fallback
- **clockworks/tiktok-profile-scraper** — Legacy profile-specific option
- **clockworks/tiktok-hashtag-scraper** — Legacy hashtag-specific fallback
- **clockworks/tiktok-comments-scraper** — Legacy comments option

## Output Fields

- `id`: Video/post ID
- `url`: Full URL
- `title`: Video caption
- `author`: Creator username
- `authorId`: Creator ID
- `likeCount`: Number of likes
- `commentCount`: Number of comments
- `shareCount`: Number of shares
- `viewCount`: Number of views
- `hashtags`: Array of hashtags
- `music`: Music/sound used
- `createTime`: Upload timestamp

## Notes

- Requires `APIFY_API_KEY` env var (loaded from `.env`)
- Default actor is apidojo/tiktok-scraper
- Legacy Clockworks actors remain documented for rollback
