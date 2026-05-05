---
name: instagram
description: "Scrape Instagram profiles, posts, hashtags, and comments using Apify. Use for trend research, competitor analysis, and content monitoring."
---

# Instagram Scraper

Scrape Instagram data using Apify actors. Default actor is **apidojo/instagram-scraper**.

## Quick Start

```bash
# Scrape user profile posts
python3 .claude/skills/instagram-scraper/scripts/instagram_scraper.py --username wellnessbrand

# Scrape hashtag posts
python3 .claude/skills/instagram-scraper/scripts/instagram_scraper.py --hashtag wellness

# Watch a profile for new posts
python3 .claude/skills/instagram-scraper/scripts/instagram_profile_watch.py --username targetuser
```

## Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--username` | `-u` | Instagram username (without @) | - |
| `--hashtag` | - | Hashtag to scrape | - |
| `--url` | `-l` | Direct post URL | - |
| `--limit` | `-n` | Number of items | 20 |
| `--json` | `-j` | Output as JSON | false |

## Available Actors

- **apidojo/instagram-scraper** — Current default actor
- **apify/instagram-scraper** — Legacy general-purpose fallback
- **apify/instagram-profile-scraper** — Legacy profile-specific option
- **apify/instagram-hashtag-scraper** — Legacy hashtag-specific fallback
- **apify/instagram-comment-scraper** — Legacy comments option

## Output Fields

- `id`: Post ID
- `shortCode`: Post shortcode
- `url`: Post URL
- `caption`: Post caption
- `ownerUsername`: Creator username
- `ownerId`: Creator ID
- `likesCount`: Like count
- `commentsCount`: Comment count
- `takenAt`: Upload timestamp
- `mediaType`: Image, Video, or Album
- `displayUrl`: Main image URL
- `hashtags`: Array of hashtags
- `mentions`: Tagged users

## Notes

- Requires `APIFY_API_KEY` env var (loaded from `.env`)
- Default actor is apidojo/instagram-scraper
- Legacy Apify Instagram actors remain documented for rollback
