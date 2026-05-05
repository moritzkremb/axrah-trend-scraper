---
name: reddit
description: "Read and search Reddit posts via web scraping. Use for trend research, topic monitoring, and community analysis. Read-only access."
---

# Reddit Scraper

Read and search Reddit posts using the public JSON API. No API key required.

## Quick Start

```bash
# Read top posts from a subreddit
python3 .claude/skills/reddit-scraper/scripts/reddit_scraper.py --subreddit LocalLLaMA --limit 5

# Search for posts
python3 .claude/skills/reddit-scraper/scripts/reddit_scraper.py --search "trending topic" --limit 5

# Read newest posts
python3 .claude/skills/reddit-scraper/scripts/reddit_scraper.py --subreddit ClaudeAI --sort new --limit 5
```

## Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--subreddit` | `-s` | Subreddit name (without r/) | - |
| `--search` | `-q` | Search query | - |
| `--sort` | - | Sort: hot, new, top, rising | top |
| `--time` | `-t` | Time filter: hour, day, week, month, year, all | day |
| `--limit` | `-n` | Number of posts (max 100) | 25 |
| `--json` | `-j` | Output as JSON | false |
| `--verbose` | `-v` | Show post preview text | false |

## Output Fields (JSON)

- `title`: Post title
- `author`: Username
- `score`: Upvotes (net)
- `num_comments`: Comment count
- `url`: Link URL
- `permalink`: Reddit discussion URL
- `subreddit`: Subreddit name
- `created_utc`: Unix timestamp
- `selftext`: Post text (first 200 chars)
- `upvote_ratio`: Upvote percentage (0-1)

## Notes

- No API key required — uses Reddit's public JSON API
- Read-only: cannot post, comment, or vote
- Rate limits may apply for high-frequency requests

## Technical Details

See [references/TECHNICAL.md](references/TECHNICAL.md) for implementation details.
