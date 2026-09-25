# Schemin Data Gateway

Reliability layer for ESPN fantasy-football data.

Required behavior:
- Primary ESPN fetch
- Bounded retries with backoff
- Payload contract validation
- Atomic last-known-good snapshots
- Configurable mirror/fallback
- Mandatory freshness metadata

No downstream subsystem may imply live verification when the gateway is stale or failed.
