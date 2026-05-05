---
name: apify
description: Run Apify Actors (web scrapers, crawlers, automation tools) and retrieve their results using the Apify REST API with curl. Use when the user wants to scrape a website, extract data from the web, run an Apify Actor, crawl pages, or get results from Apify datasets.
---

# Apify

Run any of the 17,000+ Actors on [Apify Store](https://apify.com/store) and retrieve structured results via the REST API.

Full OpenAPI spec: [openapi.json](openapi.json)

## Authentication

All requests need the `APIFY_API_KEY` env var (loaded from `.env`). Use it as a Bearer token:

```bash
-H "Authorization: Bearer $APIFY_API_KEY"
```

Base URL: `https://api.apify.com`

## Core workflow

### 1. Find the right Actor

Search the Apify Store by keyword:

```bash
curl -s "https://api.apify.com/v2/store?search=web+scraper&limit=5" \
  -H "Authorization: Bearer $APIFY_API_KEY" | jq '.data.items[] | {name: (.username + "/" + .name), title, description}'
```

Actors are identified by `username~name` (tilde) in API paths, e.g. `apify~web-scraper`.

### 2. Get Actor README and input schema

Before running an Actor, fetch its default build to get the README (usage docs) and input schema (expected JSON fields):

```bash
curl -s "https://api.apify.com/v2/acts/apify~web-scraper/builds/default" \
  -H "Authorization: Bearer $APIFY_API_KEY" | jq '.data | {readme, inputSchema}'
```

`inputSchema` is a JSON-stringified object — parse it to see required/optional fields, types, defaults, and descriptions. Use this to construct valid input for the run.

### 3. Run an Actor (async — recommended for most cases)

Start the Actor and get the run object back immediately:

```bash
curl -s -X POST "https://api.apify.com/v2/acts/apify~web-scraper/runs" \
  -H "Authorization: Bearer $APIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"startUrls":[{"url":"https://example.com"}],"maxPagesPerCrawl":10}'
```

Response includes `data.id` (run ID), `data.defaultDatasetId`, `data.status`.

Optional query params: `?timeout=300&memory=4096&maxItems=100&waitForFinish=60`

- `waitForFinish` (0-60): seconds the API waits before returning. Useful to avoid polling for short runs.

### 4. Poll run status

```bash
curl -s "https://api.apify.com/v2/actor-runs/RUN_ID?waitForFinish=60" \
  -H "Authorization: Bearer $APIFY_API_KEY" | jq '.data | {status, defaultDatasetId}'
```

Terminal statuses: `SUCCEEDED`, `FAILED`, `ABORTED`, `TIMED-OUT`.

### 5. Get results

**Dataset items** (most common — structured scraped data):

```bash
curl -s "https://api.apify.com/v2/datasets/DATASET_ID/items?clean=true&limit=100" \
  -H "Authorization: Bearer $APIFY_API_KEY"
```

Or directly from the run (shortcut — same parameters):

```bash
curl -s "https://api.apify.com/v2/actor-runs/RUN_ID/dataset/items?clean=true&limit=100" \
  -H "Authorization: Bearer $APIFY_API_KEY"
```

Params: `format` (`json`|`csv`|`jsonl`|`xml`|`xlsx`|`rss`), `fields`, `omit`, `limit`, `offset`, `clean`, `desc`.

**Key-value store record** (screenshots, HTML, OUTPUT):

```bash
curl -s "https://api.apify.com/v2/key-value-stores/STORE_ID/records/OUTPUT" \
  -H "Authorization: Bearer $APIFY_API_KEY"
```

**Run log:**

```bash
curl -s "https://api.apify.com/v2/logs/RUN_ID" \
  -H "Authorization: Bearer $APIFY_API_KEY"
```

### 6. Run Actor synchronously (short-running Actors only)

For Actors that finish within 300 seconds, get dataset items in one call:

```bash
curl -s -X POST "https://api.apify.com/v2/acts/apify~web-scraper/run-sync-get-dataset-items?timeout=120" \
  -H "Authorization: Bearer $APIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"startUrls":[{"url":"https://example.com"}],"maxPagesPerCrawl":5}'
```

Returns the dataset items array directly (not wrapped in `data`). Returns `408` if the run exceeds 300s.

## Quick recipes

### Long-running Actor (async with polling)

```bash
# 1. Start
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/apify~web-scraper/runs?waitForFinish=60" \
  -H "Authorization: Bearer $APIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"startUrls":[{"url":"https://example.com"}],"maxPagesPerCrawl":500}')
RUN_ID=$(echo "$RUN" | jq -r '.data.id')

# 2. Poll until done
while true; do
  STATUS=$(curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?waitForFinish=60" \
    -H "Authorization: Bearer $APIFY_API_KEY" | jq -r '.data.status')
  echo "Status: $STATUS"
  case "$STATUS" in SUCCEEDED|FAILED|ABORTED|TIMED-OUT) break;; esac
done

# 3. Fetch results
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?clean=true" \
  -H "Authorization: Bearer $APIFY_API_KEY"
```

### Abort a run

```bash
curl -s -X POST "https://api.apify.com/v2/actor-runs/RUN_ID/abort" \
  -H "Authorization: Bearer $APIFY_API_KEY"
```

## Error handling

- **401**: `APIFY_API_KEY` missing or invalid.
- **404 Actor not found**: check `username~name` format (tilde, not slash). Browse https://apify.com/store.
- **400 run-failed**: check `GET /v2/logs/RUN_ID` for details.
- **402/403 payment required**: the Actor likely requires a subscription.
- **408 run-timeout-exceeded**: sync endpoints have a 300s limit. Use async workflow instead.
- **429 rate-limit-exceeded**: retry with exponential backoff.
