# Weekly Memo OS — Memo Release Registry Spec V1

**Status:** V5.6 RC dependency

## Purpose
Prevent draft/test/replay artifacts from being mistaken for published issues.

## Record schema

```yaml
release_id:
season:
week:
title:
status: DRAFT | CANDIDATE | RELEASED | SUPERSEDED
publication_timestamp:
canonical_artifact:
artifact_digest:
page_count:
benchmark_status: NONE | GOLD_STANDARD | HISTORICAL_REFERENCE
source_manifest:
fact_snapshot:
canon_snapshot:
world_snapshot:
qa_receipt:
blind_release_audit:
supersedes:
superseded_by:
commissioner_approval:
notes:
```

## Invariants
- one active RELEASED record per season/week unless explicit Commissioner supersession;
- a CANDIDATE cannot overwrite a RELEASED record;
- a replay/test is never promoted implicitly;
- benchmark designation requires explicit registry state;
- artifact digest or equivalent immutable identity is required for RELEASED status;
- changing canonical artifact creates a new release/supersession event.

## Week 2 seed rule
The official league-shared Week 2 illustrated memo is the canonical Week 2 release and gold-standard benchmark. Any later Week 2 test/replay remains non-canonical unless explicitly superseded.
