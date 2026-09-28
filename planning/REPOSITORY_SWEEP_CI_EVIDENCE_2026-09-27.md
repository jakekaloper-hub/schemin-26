# Schemin '26 — Repository Sweep CI Evidence

**Document class:** review  
**Authority / owner:** Groundskeeper + The Umpire  
**Version:** 1.0  
**Status:** ACTIVE EVIDENCE  
**Created:** 2026-09-27  
**Review trigger:** sweep close or material CI change

## Bullpen Runtime CI

Workflow: `.github/workflows/bullpen-runtime-ci.yml`

- Current baseline main SHA `49194258ef60c3d467d6f1cdf9926c1a4cc84cc5`: run **302**, success.
- Sweep branch governance commits triggered runs 304–312 observed during the sweep; all completed runs observed were successful.
- Runtime: Node 22, `npm test`.

## Novel OS CI

Workflow: `.github/workflows/novel-os-ci.yml`

Recent main-branch evidence includes:
- run **73** / id `36371735587` — success
- run **72** / id `36371733358` — success
- run **71** / id `36371592754` — success
- run **70** / id `36368556598` — success

Certification history:
- PR #7 head: Novel OS CI failed.
- PR #8 head: Novel OS CI passed.
- PR #9 head: Novel OS CI passed.
- PRs #7–#9 were certification-only trigger branches and have been closed as superseded/satisfied; Actions history remains evidence.

## ZeroGPU smoke

Workflow: `.github/workflows/novel-os-zerogpu-smoke.yml`

- run **1** / id `36371595027` — success.
- This proves the configured real smoke workflow completed at that commit; it does not certify every future renderer/provider state.

## ESPN League Snapshot

Workflow: `.github/workflows/espn-cold-standby.yml`

Scheduled run id `36362219506` completed successfully and its job log recorded:

`Validated ESPN snapshot 2026-09-28T00:26:22.173918+00:00`

However, the sweep proved that the post-fetch commit gate used `git diff --quiet` before staging the new snapshot directory. Untracked snapshot files were therefore invisible to the diff and the workflow could exit green without persisting `data/snapshots/1417621/latest.json`.

Repair on sweep branch:
- stage `data/snapshots/1417621` first;
- inspect `git diff --cached --quiet` second;
- add required `snapshot_age_seconds` metadata;
- add Data Gateway regression CI.

## Data Gateway CI

Workflow: `.github/workflows/data-gateway-ci.yml`

First sweep-branch run:
- run **1** / id `36373200079` — **success**
- compile gateway — success
- snapshot contract tests — success

The tests cover:
- required freshness fields;
- atomic snapshot write behavior;
- staging-before-diff workflow invariant.

## Remaining CI proof

A post-merge scheduled/manual ESPN run is still required to prove the repaired workflow persists the first durable `latest.json`/manifest on the default branch. Until then, acquisition is proven and the repair is test-proven, but default-branch snapshot persistence is not yet certified.
