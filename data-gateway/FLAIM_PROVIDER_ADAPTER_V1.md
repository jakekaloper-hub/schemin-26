# Flaim Provider Adapter V1

**Authority:** League Data Platform / Librarian  
**Status:** ACTIVE PROVIDER ADAPTER  
**Effective date:** 2026-09-29  
**Canonical league:** ESPN 1417621 / 2026

## Purpose

Flaim gives Schemin a second governed read path into the ESPN league.

It does **not** replace the Schemin Data Gateway and does not become an alternate project truth.

## Architecture

```text
Direct ESPN automated path ───────────┐
                                     │
Flaim authorized connector capture ──┼─> Schemin validation / discrepancy layer
                                     │
Commissioner primary evidence ───────┘
                                              ↓
                                      durable receipts
                                              ↓
                                downstream Memo / Novel / Mercer
```

### Direct ESPN

Preferred automated acquisition path where healthy.

### Flaim

Read-only normalized provider adapter useful for:
- current league settings;
- standings;
- weekly matchups and provider projections;
- all-team roster snapshots;
- transactions;
- waiver/FAAB evidence;
- player ownership and available-player research;
- completed draft results;
- historical season lookup.

The ChatGPT Flaim connector is not available inside GitHub Actions. Therefore Flaim evidence enters GitHub as an **authorized, provenance-stamped provider receipt** and is validated by `flaim_adapter.py`.

## Source-of-truth rule

A Flaim receipt is a **PROVIDER OBSERVATION**.

Schemin may promote a fact to stronger status only after applicable validation/reconciliation.

Do not call a Flaim capture perpetually live. Consumers recompute age from `captured_at`.

## Transaction rule

Flaim exposes its ESPN transaction source and limitation metadata.

If:
`structured_details_incomplete=true`

then:
- adds/drops/waiver rows may still be used as provider observations;
- FAAB bids may be used when present;
- exact trade assets remain unresolved unless directional `trade_sides` or independent evidence confirms them;
- no downstream module may silently claim trade completeness.

## Medical/injury rule

Roster slot placement such as IR is **not** medical-status verification.

Flaim roster evidence can prove current fantasy-roster placement. It cannot, by itself, prove current player health/status for Memo injury prose.

## Freshness rule

`flaim_adapter.py` computes:
- `snapshot_age_seconds`
- `stale`
- `freshness_slo_seconds`

at consumption time.

Recommended defaults:
- active game/waiver window: <= 1 hour;
- background preproduction: a broader explicitly stated SLO may be used;
- historical analysis: temporal scope replaces a live SLO.

## Current Week 4 receipt

`../data/provider-receipts/flaim/1417621/2026/week-4/2026-09-29T175654Z.json`

This receipt contains 12 standings rows, 6 Week 4 matchups, all 12 current rosters and 47 recent ESPN transactions.
