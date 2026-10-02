# Source of Truth Policy

## Universal authority rule

Authority is resolved by **domain + time + release state + production eligibility**, not by retrieval convenience.

Historical canonical evidence remains true for its historical interval. It must not silently satisfy a current/latest request. Current semantic authority does not imply production eligibility when required freshness, source-byte, mount/binding, release, or QA evidence is absent.

## League truth priority

1. Live validated ESPN league data when successfully fetched.
2. Validated last-known-good Schemin Data Gateway snapshot with freshness metadata.
3. Commissioner/user-provided primary evidence such as screenshots or exported league data.
4. Canonical Schemin '26 repository documents.
5. Conversation memory/context only as a convenience layer.

Never present stale or remembered league state as freshly verified.

Required freshness fields:
- `stale`
- `fetched_at`
- `snapshot_age_seconds`
- `failure_reason`

## Publication identity

Publication identity is resolved through the Publication Manifest and owning release evidence.

Week 2: `Week 2 memo.pdf` is the canonical 14-page league-shared Week 2 issue and historical gold-standard benchmark.

Week 3: `Pro_Schemin_Week_3_Memo_Final.pdf` is the current released Memo benchmark until a newer released issue is explicitly promoted.

Do not identify similarly named finals, tests, reruns, replays, RC candidates, drafts, or historical benchmarks as current merely because they are retrievable or semantically similar.

Explicit historical requests remain historical. Current/latest requests resolve current authority. Unknown/unreleased requests fail closed.
