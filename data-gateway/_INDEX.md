# Data Gateway — Index

**Authority:** League Data Platform / Data Gateway

## Load order

1. `OPERATIONAL_PATCH_v1.0.md`
2. `SCHEMIN_26_ESPN_INGESTION_RELIABILITY_PATCH_v1.0.md`
3. `../schemas/freshness.schema.json`
4. `../docs/governance/SOURCE_OF_TRUTH.md`

## Core contract

```text
direct ESPN
→ bounded retry
→ validate
→ promote canonical snapshot
→ persist last-known-good

failure
→ mirror
→ cold standby
→ last-known-good
→ stale=true + provenance
```

A payload existing does not prove freshness. Consumers must propagate freshness metadata.
