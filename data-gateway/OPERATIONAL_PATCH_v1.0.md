# Schemin '26 ESPN Data Gateway — Operational Patch v1.0

Purpose: make ESPN league **1417621** ingestion resilient enough that Jack Mercer, Weekly Memo OS, and the Front Office site do not silently fail or silently analyze stale data.

## Runtime policy

1. Fetch the current ESPN Fantasy read host: `lm-api-reads.fantasy.espn.com`.
2. Retry only transient/network failures with bounded exponential backoff.
3. Validate the payload against league contracts before it becomes canonical.
4. Persist every accepted payload as a last-known-good snapshot using atomic writes.
5. If direct ESPN fails, try configured mirrors (`SCHEMIN_ESPN_MIRRORS`).
6. If all network paths fail, return the last-known-good snapshot with `stale=true`, `failure_reason`, `snapshot_age_seconds`, and the last fetch timestamp.
7. Never label cached data as live.

## League contracts

- League ID: **1417621**
- Season: **2026**
- Teams: **12**
- Roster slots/team: **17**
- Expected rostered entries: **204**
- Core objects required: `teams`, `settings`, `schedule`, `status`

These are validated on every refresh. Contract failures do **not** overwrite the last-good snapshot.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python schemin_gateway.py seed tests/fixture_1417621.json
python -m unittest discover -s tests -v
python schemin_gateway.py refresh
python schemin_gateway.py health
```

## Mirror configuration

Set one or more comma-separated raw JSON/envelope URLs. `{league_id}` and `{season}` placeholders are supported.

```bash
export SCHEMIN_ESPN_MIRRORS='https://your-worker.example/league/1417621,https://raw.githubusercontent.com/YOU/REPO/main/data/snapshots/1417621/latest.json'
```

Recommended order:

- Primary: app/server direct ESPN request.
- Secondary: Cloudflare Worker `/league/1417621` edge gateway backed by KV.
- Tertiary: GitHub Actions cold-standby snapshot.
- Final fallback: process-local last-known-good snapshot.

## Freshness policy

Consumers must inspect `meta.stale` and `meta.snapshot_age_seconds`.

- `stale=false`: current network refresh succeeded.
- `stale=true`: usable fallback; analysis may continue, but any statement requiring current rosters/scores must disclose snapshot time.
- Health exits non-zero once stale age exceeds `SCHEMIN_MAX_STALE_SECONDS` (default 24h).

For game windows, use a much tighter operational SLO, e.g. `SCHEMIN_MAX_STALE_SECONDS=900`.

## Cloudflare Worker

`cloudflare/worker.js` is a deliberately **fixed-target gateway**, not an open proxy. It can only retrieve league 1417621 / season 2026, validates the response, stores last-good state in KV, refreshes on a 5-minute cron, and serves cached data during ESPN failure.

Create a Workers KV namespace, replace the ID in `wrangler.toml`, then deploy with Wrangler.

## GitHub Actions cold standby

`.github/workflows/espn-cold-standby.yml` refreshes every 30 minutes and commits only `latest.json` + `manifest.json` when state changes. This gives agents and web clients a second network surface when ESPN's hostname is inaccessible from their execution environment.

## Consumer rule for Mercer / Memo OS

Every ingestion call must produce both `data` and `meta`. No downstream agent may say "live ESPN" unless `meta.stale == false`. If stale, the agent should continue from the snapshot where appropriate and mark freshness explicitly.