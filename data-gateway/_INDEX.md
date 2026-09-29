# Data Gateway — Index

**Authority:** League Data Platform / Data Gateway

## Load order

1. `OPERATIONAL_PATCH_v1.0.md`
2. `SCHEMIN_26_ESPN_INGESTION_RELIABILITY_PATCH_v1.0.md`
3. `FLAIM_PROVIDER_ADAPTER_V1.md`
4. `flaim_adapter.py`
5. `../schemas/freshness.schema.json`
6. `../docs/governance/SOURCE_OF_TRUTH.md`

## Core contract

```text
direct ESPN automated path
→ bounded retry
→ validate
→ promote canonical snapshot
→ persist last-known-good

authorized Flaim provider receipt
→ validate receipt contract
→ preserve provenance + limitations
→ corroborate / reconcile
→ never bypass freshness or source hierarchy

direct ESPN failure
→ corroborating provider evidence where available
→ mirror / cold standby
→ last-known-good
→ stale=true + provenance
```

A payload existing does not prove freshness. Consumers must propagate freshness metadata.


## Flaim rule

Flaim is a read-only provider adapter, not a second source of truth.

Authorized connector captures are stored as provenance-stamped provider receipts and validated by `flaim_adapter.py`. Consumers must preserve provider limitations and recompute freshness from the capture timestamp.
