---
name: youtube
description: "Scrape YouTube videos, channels, comments, and search results using Apify. Use for trend research, competitor analysis, and content monitoring."
---

# YouTube Scraper

Scrape YouTube data using Apify actors. Default actor is **apidojo/youtube-scraper**.

## Quick Start

```bash
# Scrape channel videos
python3 .claude/skills/youtube-scraper/scripts/youtube_scraper.py --channel "https://www.youtube.com/@channelname"

# Search and scrape videos
python3 .claude/skills/youtube-scraper/scripts/youtube_scraper.py --search "red light therapy"

# Watch a channel for new uploads
python3 .claude/skills/youtube-scraper/scripts/youtube_channel_watch.py --channel "https://www.youtube.com/@channelname"
```

## Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--channel` | `-c` | YouTube channel URL or handle | - |
| `--search` | `-s` | Search query | - |
| `--url` | `-u` | Direct video URL | - |
| `--limit` | `-n` | Number of items | 20 |
| `--json` | `-j` | Output as JSON | false |

## Available Actors

- **apidojo/youtube-scraper** — Current default actor for channels, videos, and search
- **streamers/youtube-scraper** — Legacy fallback / rollback option
- **streamers/youtube-comments-scraper** — Video comments
- **epctex/youtube-video-downloader** — Video downloads

## Output Fields

- `id`: Video ID
- `url`: Video URL
- `title`: Video title
- `description`: Video description
- `channelId`: Channel ID
- `channelTitle`: Channel name
- `publishedAt`: Upload date
- `viewCount`: View count
- `likeCount`: Like count
- `commentCount`: Comment count
- `duration`: Video duration
- `tags`: Video tags

## Notes

- Requires `APIFY_API_KEY` env var (loaded from `.env`)
- Default actor is apidojo/youtube-scraper
- Legacy fallback remains streamers/youtube-scraper
