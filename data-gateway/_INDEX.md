# Data Gateway — Index

**Authority:** League Data Platform / Data Gateway

## Load order

1. `OPERATIONAL_PATCH_v1.0.md`
2. `SCHEMIN_26_ESPN_INGESTION_RELIABILITY_PATCH_v1.0.md`
3. `ENDPOINT_PERMANENCE_PATCH_v2.md`
4. `../schemas/freshness.schema.json`
5. `../docs/governance/SOURCE_OF_TRUTH.md`

## Current executable contract

```text
scheduled acquisition
→ direct ESPN
→ bounded retry
→ settings-derived contract validation
→ atomic latest.json + manifest.json
→ repository persistence

failed acquisition
→ preserve last-known-good league data
→ recompute age
→ stale=true + failure_reason
→ persist degraded metadata
→ workflow remains red

consumer read
→ load snapshot
→ recompute effective age from fetched_at
→ apply consumer SLO
→ never infer freshness from file existence
```

Mirror/edge failover is architectural but is **not currently an executable repository capability**. A payload existing does not prove freshness.
