# Schemin Data Gateway

Reliability and evidence-brokering layer for Pro Schemin' fantasy-football data. Direct ESPN remains the automated primary path; Flaim is a governed read-only corroboration/provider adapter.

Required behavior:
- Primary ESPN fetch
- Bounded retries with backoff
- Payload contract validation
- Atomic last-known-good snapshots
- Configurable mirror/fallback
- Mandatory freshness metadata

No downstream subsystem may imply live verification when the gateway is stale or failed.


## Flaim adapter

See `FLAIM_PROVIDER_ADAPTER_V1.md`.

Flaim connector captures are durable provider observations with explicit timestamp, source and limitations. They do not bypass Schemin validation, freshness or last-known-good rules.
