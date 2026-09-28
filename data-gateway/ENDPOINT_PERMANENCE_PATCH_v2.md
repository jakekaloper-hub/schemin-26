# ESPN Endpoint Permanence Patch v2

## Decision
The ChatGPT/web execution surface is no longer the primary ESPN transport. GitHub Actions is the durable acquisition plane for league 1417621.

## Path
ESPN lm-api-reads -> scheduled GitHub Action -> contract validation -> atomic validated snapshot -> Schemin consumers.

This eliminates repeated dependence on whether an individual chat runtime can resolve or reach ESPN.

## Consumer contract
Consumers read `data/snapshots/1417621/latest.json`, inspect `meta.fetched_at`, `meta.stale`, and `meta.failure_reason`, and **recompute effective snapshot age from `fetched_at` at read time**. Persisted `snapshot_age_seconds` is a receipt/lower bound rather than a perpetual clock.

A chat may attempt direct ESPN or Flaim as an optimization/evidence source, but failure there is not proof that the durable GitHub snapshot is unavailable.

## SLO
- Scheduled refresh: every 30 minutes.
- Game-window consumers should enforce a tighter age threshold.
- Snapshot promotion occurs only after league ID, team count, core objects, roster-settings, and settings-derived roster-capacity validation.
- Failed fetch never replaces last-known-good league data.
- Failed fetch promotes last-known-good metadata to degraded/stale state and the Action remains red.

## Operational certification state

A prior scheduled Action successfully fetched and validated ESPN, but the original workflow failed to persist first-time untracked snapshot files. That green run therefore proved acquisition, not durable cold-standby operation.

The repository-integrity remediation in PR #12 repairs persistence and degraded-state handling. This patch is **not operationally certified** until a post-merge scheduled/manual run produces `data/snapshots/1417621/latest.json` on the approved durable storage path and the repository-native health check passes.
