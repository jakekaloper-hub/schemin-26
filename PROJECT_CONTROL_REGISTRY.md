# Schemin '26 — Project Control Registry

**Status:** ACTIVE  
**Season:** 2026  
**League:** Pro Schemin' Football League — ESPN `1417621`

This file is the shortest authoritative entry point for substantial Schemin '26 work.

Standing operating contract:
- `docs/governance/SCHEMIN_26_STANDING_OPERATING_CONTRACT_V1.md`

For substantial work, load the standing operating contract before domain-specific execution.

## Canonical publication lock

**Official Week 2 Memo (league-shared September 23, 2026): `Week 2 memo.pdf`.** It is the 14-page illustrated issue beginning with Red Leopards “SPECIAL DELIVERY.” This is the canonical Week 2 published artifact and gold-standard benchmark. No similarly named Week 2 “final,” test, replay, rerun, or RC candidate may replace it without explicit Commissioner supersession.

## Five-plane architecture

```text
JAKE / COMMISSIONER INTENT
          ↓
CONTROL — SCHEMIN COLLABORATION KERNEL (SCK)
          ↓
TRUTH — LEAGUE DATA PLATFORM / DATA GATEWAY
          ↓
PRODUCTION — DOMAIN SYSTEM (MEMO OS / MERCER / CREATIVE)
          ↓
GOVERNANCE — INDEPENDENT QA / RELEASE CONTROL
          ↓
LEARNING — REGRESSION / RESEARCH / VERSIONED MEMORY
```

## Controlling domains

### Weekly Memo
Current controlling production-hardening layer: **V5.4**, with **V5.3** binding beneath it for character/reference enforcement. **V5.2-RC** remains the cross-OS orchestration layer pending its own acceptance criteria.

Read in this order:
1. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_4_ACCEPTANCE_TEST_HARDENING_PATCH.md`
2. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_3_CHARACTER_REFERENCE_ENFORCEMENT_PATCH.md`
3. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_GOLD_STANDARD_STUDIO_PATCH.md`
4. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_2_RC_MUTUAL_IMPLEMENTATION_PATCH.md`
5. `memo-os/SCHEMIN_26_WEEKLY_MEMO_GOLD_STANDARD_PRODUCTION_MANUAL.md`
6. `memo-os/SCHEMIN_26_WEEKLY_MEMO_MASTER_INITIATION_PROMPT.md`
7. `canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md`
8. `chronicles/standards/CHARACTER_VISUAL_LOCK_GATE.md`

V5.2-RC remains an RC architecture until its acceptance criteria are satisfied; do not relabel it permanently certified merely because a strong artifact exists.

### League truth / ESPN
Read:
- `data-gateway/SCHEMIN_26_ESPN_INGESTION_RELIABILITY_PATCH_v1.0.md`
- `data-gateway/OPERATIONAL_PATCH_v1.0.md`
- `schemas/freshness.schema.json`

No downstream system may imply live ESPN verification unless freshness metadata supports that claim.

### Character canon
Read:
- `canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md`

Rule: **OWNER → CANONICAL CHARACTER → CURRENT TEAM NAME**.

A rename changes labels, not character identity.

### Jack Mercer
Read:
- `mercer/JACK_MERCER_FRONT_OFFICE_V2_SPEC.md`
- `mercer/OPERATING_CONTRACT.md`

Mercer owns football decision analysis for ObiWan Jacoby. Mercer does not own Weekly Memo publication or league-data freshness.

### Bullpen / FLA
Read:
- `bullpen/SCHEMIN_26_BULLPEN_FULL_PROJECT_REVIEW.md`
- `bullpen/SCHEMIN_26_SUBAGENT_V5_1_ENGINE_ROOM_RESPONSE.md`
- `docs/architecture/FLA_INTEGRATION.md`

FLA Bullpen is a selective specialist/governance adapter. It is not a sixth Schemin control plane and is not the source of current fantasy league truth.

## Non-negotiable execution rules

- Evidence before inference.
- Stale data never masquerades as live.
- Canon blocks visual publication when unresolved.
- Same-week benchmark material is isolated during blank-canvas originality tests.
- Production agents may not self-certify release.
- File existence is not release readiness.
- A late correction reopens only dependent artifacts when possible.
- Private Mercer intelligence must not leak into public memo production.
- Material operating changes belong in Git history.
