# CEO Brief Routine Prompt

Use this as the prompt when creating the scheduled routine on Tiger's Claude Code account.

---

## Prompt

```
You are producing the daily AXRAH CEO brief. Follow the instructions in ceo-brief/SKILL.md exactly.

Steps:
1. Fetch the latest trend data from: https://raw.githubusercontent.com/moritzkremb/axrah-trend-scraper/main/outputs/latest.md
2. Check Gmail for emails from the last 24 hours — look for client inquiries, order notifications, partnership requests, competitor mentions, anything business-relevant
3. Run web searches for: "red light therapy news", "photobiomodulation industry news", "NovoTHOR", "TheraLight", "AXRAH" — look for breaking developments
4. Synthesize everything into the brief format defined in ceo-brief/SKILL.md
5. Write the brief to ceo-brief/briefs/YYYY-MM-DD.md (using today's date)
6. Also write it to ceo-brief/briefs/latest.md (overwrite)
7. Commit and push with message: "Daily CEO brief — YYYY-MM-DD"

Focus on signal, not noise. Tiger wants to know: what changed, what matters, and what to do about it.
```

## Schedule

Daily at 7:30 AM (Tiger's timezone)

## Required MCP connections

- Gmail (for inbox scanning)
- WebSearch / WebFetch (for industry news)

## Repo

This same repo: `moritzkremb/axrah-trend-scraper`
