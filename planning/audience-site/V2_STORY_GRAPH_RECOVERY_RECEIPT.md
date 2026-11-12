# Commonwealth Audience Site V2 — Story Graph Recovery Receipt

**Date:** 2026-11-12  
**Recovery branch:** `feat/commonwealth-audience-site-v2-story-graph`  
**Draft PR:** #309  
**Current base:** `story-production-graph-v1` (retarget to `main` after PR #307 is accepted/merged)  
**Donor branch:** `feat/commonwealth-audience-site-20261022`

## Recovery decision

The stale donor branch was **not rebased, merged, or blindly cherry-picked**.

Repository comparison at recovery start:
- donor ahead of current main: **2 commits**
- donor behind current main: **1,249 commits**
- status: **diverged**

Bullpen board decision: use the stale branch only as a capability donor and rebuild the audience-site data seam against the current Story Production Graph.

## What was recovered

Presentation patterns selectively ported:
- `productions/audience-site/src/index.html`
- `productions/audience-site/src/styles.css`
- `productions/audience-site/src/progress.js`
- donor reader/atlas/navigation patterns in `src/app.js`
- Node progress tests
- site README/reproduction discipline
- path-scoped audience-site CI concept

New/current implementation:
- `src/routes.js` — deterministic hash routing
- Story Graph-backed `build_public_catalog.py`
- Chronicle route using the 42-event Story Graph timeline
- explicit unavailable memo treatment with no fallback
- current Character Canon + World projection
- CANON_CLOSED manuscript projection only
- public-boundary allowlists
- exact-revision source URLs
- audience-site merge-gate suite
- accessibility contract tests

## What was deliberately not recovered

- stale `TASK_REGISTRY_V1.json` changes
- stale publication/release assumptions
- donor branch ancestry
- old catalog authority model
- duplicate character/world/publication databases
- old “latest memo” fallback behavior
- any automatic renderer execution
- deployment claims or hosting mutations

## Current data architecture

```
Current Character / World / Publication authorities
                   +
Story Production Graph generated feeds
  - web_index.json
  - timeline.json
  - render_queue.json
                   ↓
productions/audience-site/build_public_catalog.py
                   ↓
read-only dist/data.json
                   ↓
static Commonwealth reader / atlas / dispatch archive / Chronicle
```

The site remains presentation-only and cannot promote canon, publication state, world state, or render eligibility.

## Story Graph input receipt

Current Story Graph source fingerprint observed by the site build:

`4d0895c2399c61e401aa506dee23d78158e51a7614e8de62541960801ab3728d`

Catalog build output:
- memo issue records: **9**
- timeline events: **42**
- current characters: **12**
- CANON_CLOSED manuscript chapters: **4**
- renderer execution from audience site: **none**

## Fail-closed behavior

Verified:
- W1 unresolved authority remains unavailable.
- HOLD/BLOCKED memo states remain non-promoted.
- unavailable memo artifacts show their exact issue and never substitute another week.
- a synthetic RELEASED record with a missing artifact path remains unavailable.
- mismatched Story Graph consumer fingerprint fails catalog construction.
- internal `open_questions` fields are excluded from the public location projection.
- source links are pinned to exact repository revisions rather than `main`.
- Story Graph evidence/canon states survive timeline projection unchanged.
- public site code exposes no edit/publish/credential controls.

## Route / reader behavior

Verified by dependency-free Node tests:
- direct `#memo/week-9` route resolves exactly;
- unknown memo IDs remain exact and reach unavailable/missing handling;
- malformed URL encoding fails closed;
- progress cannot cross publication/source-fingerprint boundaries;
- corrupt or denied browser storage does not prevent reading;
- app and route modules pass `node --check`.

## Accessibility contract

Static WCAG-oriented checks currently pass for:
- skip navigation;
- labeled/expandable mobile navigation;
- focus-visible styling;
- reduced-motion handling;
- mobile breakpoint;
- keyboard Enter/Space on map points;
- Escape handling for mobile menu;
- 44px minimum target floor for primary interactive controls;
- no credential/edit/publish controls in the public shell.

**Limit:** this is not a full assistive-technology or rendered-browser accessibility audit. Screen-reader, zoom/reflow, real focus order, contrast in rendered states, and pointer/touch behavior still require actual browser/AT verification.

## Automated proof on recovery branch

Latest green technical head before this receipt: `619a8522b432146a93eeea734b860d9d8a468a40`.

Observed:
- Audience Website V2 workflow — **PASS**
- Repository Merge Gate — **PASS**
- Cross-Domain Authority CI — **PASS**
- Python public-catalog suite — **10 tests PASS**
- Node route/progress/accessibility suite — **15 tests PASS / 0 fail**
- Story Graph downstream consumer drift check — **PASS**
- Publication manifest validation — **PASS**
- Repository architecture validation — **PASS**
- One World model contract — **PASS**

A fresh exact-head run is required after this receipt commit before final review state is claimed.

## Stale branch disposition

`feat/commonwealth-audience-site-20261022` is now **superseded as active implementation** by the V2 recovery branch.

It remains valuable historical provenance and should not be deleted without separate authorization.

## Deployment state

**NOT DEPLOYED.**

No hosting project was changed and no public-site release is claimed by this recovery.

## Remaining gates

1. Fresh exact-head CI after receipt/README changes.
2. Independent code review on PR #309.
3. PR #307 must be accepted/merged before #309 is retargeted to `main`.
4. Real browser journey QA at mobile and desktop sizes.
5. Founder visual/experience acceptance.
6. Deployment, rollback rehearsal and public smoke verification only under separate release authorization.
