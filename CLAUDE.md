# Axrah Trend Scraper & CEO Brief

Social media trend research and executive intelligence for AXRAH.

## Repo structure

```
axrah-trend-scraper/
├── run-scrape.sh              — main scrape entry point
├── scrape-topics.env          — centralized topic/query config
├── outputs/latest.md          — consolidated latest scrape (downstream routines read this)
├── reddit-trends/             — raw Reddit outputs (timestamped)
├── tiktok-trends/             — raw TikTok outputs (timestamped)
├── youtube-trends/            — raw YouTube outputs (timestamped)
├── instagram-trends/          — raw Instagram outputs (timestamped)
├── instagram-account-watch/   — influencer IG profile watch
├── youtube-account-watch/     — influencer YT channel watch
├── ceo-brief/
│   ├── SKILL.md               — full instructions for the CEO brief routine
│   └── briefs/                — daily brief outputs
└── .claude/skills/            — scraper scripts
```

## Two routines, two accounts

### 1. Trend Scraper (runs from Moritz's account)

```bash
bash run-scrape.sh
```

Scrapes Reddit (11 relevant subreddits), TikTok, YouTube, Instagram + influencer watchlists. Commits consolidated output to `outputs/latest.md`.

### 2. CEO Brief (runs from Tiger's account)

Reads `outputs/latest.md` via raw GitHub URL, checks Gmail, does web research, and produces an executive brief. See `ceo-brief/SKILL.md` for full instructions.

The brief routine fetches trend data from:
```
https://raw.githubusercontent.com/moritzkremb/axrah-trend-scraper/main/outputs/latest.md
```

## Changing scrape topics

Edit `scrape-topics.env` — not the shell scripts. Changes flow automatically on next run.

## Environment

- Scraper requires `APIFY_API_KEY` in `.env` (not committed to git)
- CEO brief requires Gmail MCP connection on Tiger's account
