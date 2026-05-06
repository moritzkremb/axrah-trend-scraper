# CEO Brief — Daily Executive Intelligence for AXRAH

## What this skill does

Produces a concise, actionable executive brief for the AXRAH CEO every morning. It synthesizes trend data, email intelligence, and web research into decisions and directives — not a data dump.

## Inputs

1. **Trend data** — fetched from the scraper repo's consolidated output:
   ```
   https://raw.githubusercontent.com/moritzkremb/axrah-trend-scraper/main/outputs/latest.md
   ```
2. **Gmail** — recent emails via Gmail MCP (check inbox for client comms, partnership inquiries, order notifications, competitor alerts)
3. **Web search** — general search for breaking industry news, competitor moves, regulatory changes in the RLT/PBM space

## Output

A markdown brief written to `ceo-brief/briefs/YYYY-MM-DD.md` and also to `ceo-brief/briefs/latest.md`.

## Brief structure

```markdown
# AXRAH CEO Brief — [Date]

## Urgent / Action Required
[Anything that needs same-day attention — client issues, time-sensitive opportunities, problems]

## Industry & Market
[Key developments in red light therapy, photobiomodulation, wellness tech, regulatory changes]

## Competitor Intelligence
[NovoTHOR, TheraLight, Prism Light Pod, Joovv, Mito Red — any moves, pricing changes, new products, partnerships]

## Content & Social Trends
[What's trending in AXRAH's categories — from the trend scrape. What angles are getting engagement. What people are asking/complaining about]

## Influencer & Creator Signals
[What Huberman, Asprey, Greenfield, Bryan Johnson, etc. are posting. Relevant podcast mentions, collaborations]

## Team Directives

### Marketing
[What to post, respond to, or capitalize on this week]

### Sales
[Leads to prioritize, objections surfacing, market signals to use in outreach]

### Product
[Feature requests surfacing, unmet needs, development priorities]

### Operations
[Supply chain, fulfillment, support issues]

### Business Development
[Partnership opportunities, events, collaborations to pursue]

## Key Links & Sources
[Links to the most important items mentioned above]
```

## How to run

This skill is designed to be invoked by a Claude Code remote routine on a daily schedule. The routine should:

1. Fetch the latest trend data from the raw GitHub URL
2. Check Gmail for relevant emails (last 24h)
3. Run a web search for "red light therapy news", "photobiomodulation industry", and competitor names
4. Synthesize everything into the brief format above
5. Write the output file
6. Commit and push to the repo

## Business context

AXRAH is a red light therapy / photobiomodulation device company. Key facts:

- **Products:** Panel ($449), Panel Pro ($1,999), Grid ($1,999), Pod ($14,999), Pod Ultra ($24,999)
- **Positioning:** Clinical-grade PBM at 1/3 to 1/5 competitor pricing
- **Markets:** USA, Germany, Austria
- **Sales model:** Primarily B2B (clinics, gyms, sports teams, hotels)
- **Key competitors:** NovoTHOR ($65K+), TheraLight ($45-85K+), Prism Light Pod ($35K+), Joovv (panels only)
- **CEO:** Tiger
- **Differentiator:** Pod Ultra has 43,200 LEDs, 5 wavelengths, 6,000W, 129 mW/cm² — matching competitors at 1/3 to 1/5 the price
- **Target ICPs:** Medical spas, gyms, chiropractic/PT clinics, sports teams, hotels/resorts

### Products in development (do NOT mention to prospects):
- Lounger ($34,999) — luxury reclining system
- Halo ($349) — hair loss cap
- SkinIQ ($69) — skin diagnostic device

### Competitor pricing is estimated — always use "approximately" or "estimated"

### Key metrics to watch:
- Consumer interest: 32% of US adults have tried or plan to try RLT
- Med spa growth: 8,899 (2022) → 10,488 (2023)
- Market size: RLT beds $8.21B (2025) → $19.30B by 2032 (13% CAGR)

## Tone

Direct, concise, CEO-level. No fluff. Lead with what matters, what changed, and what to do about it. Tiger is a founder who wants signal, not noise.
