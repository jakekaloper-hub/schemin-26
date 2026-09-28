# Schemin '26 ESPN Data Gateway — Operational Patch v1.0

Purpose: make ESPN league **1417621** ingestion resilient enough that Jack Mercer, Weekly Memo OS, and the Front Office site do not silently fail or silently analyze stale data.

## Runtime policy

Current executable policy:

1. Fetch the current ESPN Fantasy read host: `lm-api-reads.fantasy.espn.com`.
2. Retry failures with bounded exponential backoff.
3. Validate the payload against league contracts before promotion.
4. Persist accepted state atomically to the dedicated Git ref `data/live`.
5. If direct ESPN fails, preserve the last-known-good payload, promote its metadata to `stale=true` with `failure_reason` and recomputed age, persist that degraded state to `data/live`, and leave the scheduled workflow red.
6. Never label cached data as live.

Mirror/edge routing is an approved architectural extension point but is **not part of the current executable runtime**.

## League contracts

- League ID: **1417621**
- Season: **2026**
- Teams: **12**
- Core objects required: `teams`, `settings`, `schedule`, `status`
- Roster settings must expose `lineupSlotCounts`.
- Every team must expose roster entries.
- A team's current roster entries may not exceed the roster capacity derived from the live league settings.

Do **not** use an exact league-wide roster-entry count as a live hard contract. Reserve/IR occupancy can legitimately make current team entry counts differ. The 2026 league currently has 17 base roster spots plus reserve capacity; validation therefore derives the ceiling from ESPN settings instead of hard-coding `17 × 12 = 204`.

These contracts are validated on every refresh. Contract failures do **not** replace the last-good data payload.

## Repository-native verification

No external Python dependencies are required by the current cold-standby implementation.

```bash
python -m py_compile data-gateway/refresh_espn_snapshot.py data-gateway/check_snapshot_health.py
python -m unittest -v tests/test_data_gateway_snapshot_contract.py
python data-gateway/refresh_espn_snapshot.py
python data-gateway/check_snapshot_health.py
```

To inspect the durable snapshot from a local/code checkout without switching branches:

```bash
git fetch origin refs/heads/data/live:refs/heads/data/live
mkdir -p data/snapshots/1417621
git show data/live:data/snapshots/1417621/latest.json > data/snapshots/1417621/latest.json
git show data/live:data/snapshots/1417621/manifest.json > data/snapshots/1417621/manifest.json
python data-gateway/check_snapshot_health.py
```

For a game-window freshness check:

```bash
SCHEMIN_MAX_STALE_SECONDS=900 python data-gateway/check_snapshot_health.py
```

## Mirror configuration

The controlling reliability architecture permits mirrors, but the current committed cold-standby script does **not** implement `SCHEMIN_ESPN_MIRRORS`. Do not represent mirror failover as operational until a tested adapter is committed and registered.

Current executable path:
- acquisition: direct ESPN with bounded retries;
- persistence: GitHub snapshot;
- degradation: last-known-good data + stale/failure metadata;
- consumer health: read-time freshness recomputation.

## Freshness policy

Consumers must inspect `meta.stale`, `meta.fetched_at`, and `meta.snapshot_age_seconds`.

`snapshot_age_seconds` stored in Git is a persistence-time receipt, not a perpetual clock. **Every consumer must recompute effective age from `fetched_at` at read time** and use the greater of the stored and recomputed age.

- `stale=false`: the most recent persisted acquisition succeeded and effective age is still inside the consumer's SLO.
- `stale=true`: usable fallback/degraded state; analysis may continue, but any statement requiring current rosters/scores must disclose snapshot time.
- A consumer must treat a snapshot as stale once effective age exceeds its SLO even if the persisted `stale` bit has not yet been rewritten.
- A failed scheduled refresh preserves the last-good data payload, rewrites only freshness/failure metadata, persists that degraded state, then leaves the workflow red.

For game windows, use a tight operational SLO such as 900 seconds. Background workflows may use a broader SLO when appropriate.

## Edge mirror status

A Cloudflare Worker/KV mirror remains an architectural option, not a deployed repository capability. There is currently no controlling `cloudflare/worker.js` or `wrangler.toml` in `schemin-26`. Add one only through an explicit implementation/validation path.

## GitHub Actions cold standby

`.github/workflows/espn-cold-standby.yml` refreshes every 30 minutes and persists `latest.json` + `manifest.json` to the dedicated Git ref **`data/live`** whenever durable snapshot/freshness state changes. Operational snapshot churn therefore does not mutate `main`. On acquisition failure, the last-good data remains intact while metadata is promoted to degraded/stale state before the workflow fails. Consumers resolve ref `data/live`, path `data/snapshots/1417621/latest.json`.

## Consumer rule for Mercer / Memo OS

Every ingestion call must produce both `data` and `meta`. No downstream agent may say "live ESPN" unless `meta.stale == false`. If stale, the agent should continue from the snapshot where appropriate and mark freshness explicitly.