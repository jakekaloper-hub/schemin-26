# Schemin Data Gateway

Reliability layer for ESPN fantasy-football data.

Required behavior:
- Primary ESPN fetch
- Bounded retries with backoff
- Payload contract validation against live league settings
- Atomic last-known-good snapshots
- Configurable mirror/fallback
- Mandatory freshness metadata
- Read-time freshness recomputation from `fetched_at`
- Failed-refresh promotion to degraded/stale metadata without replacing last-good league data

No downstream subsystem may imply live verification when the gateway is stale, failed, or older than that consumer's freshness SLO.

Current production entry points:
- acquisition: `refresh_espn_snapshot.py`
- scheduled persistence: `.github/workflows/espn-cold-standby.yml` → Git ref `data/live`, path `data/snapshots/1417621/`
- regression contract: `../tests/test_data_gateway_snapshot_contract.py`
