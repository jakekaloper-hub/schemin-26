# ESPN Endpoint Permanence Patch v2

## Decision
The ChatGPT/web execution surface is no longer the primary ESPN transport. GitHub Actions is the durable acquisition plane for league 1417621.

## Path
ESPN lm-api-reads -> scheduled GitHub Action -> schema validation -> atomic validated snapshot -> Schemin consumers.

This eliminates repeated dependence on whether an individual chat runtime can resolve or reach ESPN.

## Consumer contract
Consumers read `data/snapshots/1417621/latest.json` and inspect `meta.fetched_at` and `meta.stale`. A chat may attempt direct ESPN as an optimization, but failure there is not a production blocker.

## SLO
- Scheduled refresh: every 30 minutes.
- Game-window target can be tightened later.
- Snapshot promotion occurs only after league ID, team count, schedule, settings, and status validation.
- Failed fetch never overwrites last-known-good.

## Remaining deployment check
The workflow must complete successfully at least once in GitHub Actions. Until that happens, this patch is code-complete but not operationally certified.
