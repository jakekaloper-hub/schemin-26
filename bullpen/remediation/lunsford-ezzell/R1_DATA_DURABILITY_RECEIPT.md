# R1 — Data Durability Remediation Receipt

**Mission:** Lunsford × Ezzell External Audit Remediation  
**Gate:** R1 — Data Durability  
**Status:** PASS / OPERATIONALLY VERIFIED  
**Merged PR:** #50  
**Main merge SHA:** `cab798a48847c8fa1ede66b26b42c7d3685d81e2`

## Defect

The prior scheduled ESPN workflow could successfully fetch and validate league `1417621` but exit before staging a first untracked snapshot. A green acquisition run therefore did not prove the promised GitHub cold standby existed.

## Implementation

R1 now:
- validates ESPN payload structure and settings-derived roster capacity;
- preserves last-known-good data on acquisition failure and marks it stale;
- stages snapshot files before change detection;
- isolates machine-written snapshot churn on `data/live`;
- verifies exact remote `latest.json` and `manifest.json` bytes after persistence;
- exposes repository-native freshness/health evaluation;
- turns rejected persistence into a red result.

## Test receipt

Data Gateway CI branch run: `36809906061`.

Result: **17/17 PASS**.

Covered:
- first untracked snapshot;
- changed snapshot;
- unchanged no-op;
- rejected push/persistence failure;
- provider/network failure;
- invalid provider payload;
- LKG preservation;
- read-time freshness;
- atomic local writes;
- durable-branch workflow contract.

## Operational proof

Post-merge ESPN run: `36809984290`  
Job: `110202669057`

Observed:
- ESPN fetch/validation — PASS;
- fetched at `2026-10-01T03:19:38.792141+00:00`;
- persistence to `data/live` — PASS;
- exact remote byte verification — PASS;
- workflow conclusion — SUCCESS.

Durable branch after run:
`data/live@2bc195c353ccc3e57a9a300a924597a9243eb700`

The workflow log records:

`Durable remote snapshot verified: 2026-10-01T03:19:38.792141+00:00`

## Umpire ruling

**R1 PASS.**

Successful provider access is no longer conflated with durable ingestion. R2 is authorized.
