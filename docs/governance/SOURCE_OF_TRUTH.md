# Source of Truth Policy

Priority order:

1. Live validated ESPN league data when successfully fetched.
2. Validated last-known-good Schemin Data Gateway snapshot with freshness metadata.
3. Commissioner/user-provided primary evidence such as screenshots or exported league data.
4. Canonical Schemin '26 repository documents.
5. Conversation memory/context only as a convenience layer.

Never present stale or remembered league state as freshly verified.

Required freshness fields for gateway-backed data:
- `stale`
- `fetched_at`
- `snapshot_age_seconds`
- `failure_reason`
