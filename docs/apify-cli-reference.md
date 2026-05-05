# Apify CLI Reference

Quick reference for the Apify CLI. Full docs: https://docs.apify.com/cli/docs/reference

---

## Authentication

| Command | What it does |
|---|---|
| `apify login -t <TOKEN>` | Authenticate with API token (stored in `~/.apify/auth.json`) |
| `apify login -m console` | Interactive browser-based login |
| `apify logout` | Remove stored credentials |
| `apify info` | Show current authenticated account |

---

## Creating & Running Actors Locally

| Command | What it does |
|---|---|
| `apify create [name] -t <template>` | Scaffold a new Actor project from a template |
| `apify init [name]` | Initialize Actor project in current directory |
| `apify run` | Run Actor locally with simulated Apify env vars |
| `apify run -i '{"key":"val"}'` | Run locally with inline JSON input |
| `apify run --input-file input.json` | Run locally with input from file |
| `apify run --purge` | Run locally and clear previous default stores |
| `apify validate-schema [path]` | Validate Actor input schema |

---

## Deploying & Managing Actors on Apify

| Command | What it does |
|---|---|
| `apify push [actorId]` | Deploy local Actor to Apify platform |
| `apify push --force` | Force deploy (overwrite remote) |
| `apify pull [actorId]` | Download Actor code from platform |
| `apify pull -v <version>` | Pull a specific version |
| `apify actors ls` | List your Actors |
| `apify actors ls --my` | List only Actors you own |
| `apify actors info <actorId>` | Show Actor details |
| `apify actors rm <actorId>` | Delete an Actor |

---

## Running Actors Remotely

| Command | What it does |
|---|---|
| `apify call [actorId]` | Run Actor remotely and wait for finish |
| `apify call [actorId] -i '{"key":"val"}'` | Run with inline input |
| `apify call [actorId] -f input.json` | Run with input file |
| `apify call [actorId] -m 4096 -t 300` | Set memory (MB) and timeout (seconds) |
| `apify call [actorId] -o` | Print output dataset when done |
| `apify actors start [actorId]` | Start Actor remotely, return immediately (don't wait) |

---

## Runs

| Command | What it does |
|---|---|
| `apify runs ls [actorId]` | List runs (optionally filter by Actor) |
| `apify runs info <runId>` | Show run details |
| `apify runs log <runId>` | Print run log output |
| `apify runs abort <runId>` | Abort a running Actor |
| `apify runs abort <runId> -f` | Force abort |
| `apify runs resurrect <runId>` | Resume an aborted/finished run |
| `apify runs rm <runId>` | Delete a run |

---

## Builds

| Command | What it does |
|---|---|
| `apify builds create --tag <tag>` | Create a new build |
| `apify builds ls [actorId]` | List builds |
| `apify builds info <buildId>` | Show build details |
| `apify builds log <buildId>` | Print build log |
| `apify builds rm <buildId>` | Delete a build |

---

## Datasets (Structured Output Storage)

| Command | What it does |
|---|---|
| `apify datasets create [name]` | Create a named dataset |
| `apify datasets ls` | List all datasets |
| `apify datasets info <id>` | Show dataset info |
| `apify datasets get-items <id>` | Get items (default JSON) |
| `apify datasets get-items <id> --format csv` | Get items as CSV (also: jsonl, html, rss, xml, xlsx) |
| `apify datasets get-items <id> --limit 100 --offset 50` | Paginate results |
| `apify datasets push-items <id> '[{"k":"v"}]'` | Push data into a dataset |
| `apify datasets rename <id> <newName>` | Rename a dataset |
| `apify datasets rm <id>` | Delete a dataset |

---

## Key-Value Stores

Shorthand: `apify kvs` works in place of `apify key-value-stores`.

| Command | What it does |
|---|---|
| `apify kvs create [name]` | Create a new store |
| `apify kvs ls` | List all stores |
| `apify kvs info <storeId>` | Show store info |
| `apify kvs keys <storeId>` | List all keys in a store |
| `apify kvs get-value <storeId> <key>` | Get a value |
| `apify kvs set-value <storeId> <key> <value>` | Set a value |
| `apify kvs set-value <storeId> <key> <val> --content-type application/json` | Set with content type |
| `apify kvs delete-value <storeId> <key>` | Delete a value |
| `apify kvs rename <id> <newName>` | Rename a store |
| `apify kvs rm <id>` | Delete a store |

---

## Actor Runtime Helpers (Use Inside Actor Code)

These work during `apify run` or in a running Actor:

| Command | What it does |
|---|---|
| `apify actor get-input` | Get Actor input from default KV store |
| `apify actor get-value <key>` | Read from KV store |
| `apify actor set-value <key> <value>` | Write to KV store |
| `apify actor push-data '{"k":"v"}'` | Push data to default dataset |
| `apify actor get-public-url <key>` | Get public HTTP URL for a KV store item |
| `apify actor charge <event> --count 1` | Charge for pay-per-event runs |

---

## Tasks

| Command | What it does |
|---|---|
| `apify task run <taskId>` | Run a saved task remotely |
| `apify task run <taskId> -m 4096 -t 300` | Run with memory/timeout overrides |

---

## Secrets

| Command | What it does |
|---|---|
| `apify secrets add <name> <value>` | Store a secret env variable |
| `apify secrets rm <name>` | Remove a secret |

---

## Other

| Command | What it does |
|---|---|
| `apify help [command]` | Show help for any command |
| `apify upgrade` | Update the CLI |
| `apify telemetry enable/disable` | Toggle anonymous usage data |

---

## Common Flags (Available on Most Commands)

| Flag | What it does |
|---|---|
| `--json` | Output in JSON format |
| `--limit <n>` | Limit number of results |
| `--offset <n>` | Skip first n results |
| `--desc` | Sort descending |
