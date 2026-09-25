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

## Canonical published-artifact override

For historical publication identity, the Commissioner-designated artifact is authoritative over filenames inferred from prior production runs.

**Week 2 / September 23, 2026:** the official league-shared publication is **`Week 2 memo.pdf`**, the 14-page illustrated issue beginning with the Red Leopards **“SPECIAL DELIVERY”** cover and ending with **“THE FINAL WORD.”**

Do **not** identify `PRO_SCHEMIN_WEEK_2_FINAL_MEMO.pdf`, an Engine Room test, V5.2-RC candidate, rerun, replay, or any later Week 2 artifact as the official published Week 2 memo.

When the official Week 2 memo is used as a gold-standard/regression benchmark, “official,” “published,” and “gold standard” all resolve to `Week 2 memo.pdf` unless the Commissioner explicitly supersedes it.
