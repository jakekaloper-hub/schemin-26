# Bullpen Board — Commonwealth Audience Site Branch Recovery

**Date:** 2026-11-12  
**Project:** Schemin '26  
**Command:** `/bullpen board --project schemin-26 --topic audience-site-stale-branch-recovery --evidence-required`  
**Decision scope:** how to recover useful work from `feat/commonwealth-audience-site-20261022`, currently 2 commits ahead / 1,249 commits behind `main`.

## Evidence boundary

This is a source-grounded Bullpen board synthesis using canonical Bullpen command/role doctrine and repository evidence. The role names below are domain ownership lenses; this document is not an authenticated live-Director invocation receipt.

## Evidence reviewed

- Bullpen `docs/COMMAND_SYSTEM_V2.md`
- Bullpen `BULLPEN.md`
- Bullpen task-orientation doctrine
- Schemin current `main`
- Story Production Graph branch / PR #307
- stale branch `feat/commonwealth-audience-site-20261022`
- compare result: **2 commits ahead / 1,249 behind / diverged**
- stale branch's audience-site implementation and plan
- current Story Graph downstream feeds:
  - `planning/story-production-graph/generated/2026/web_index.json`
  - `planning/story-production-graph/generated/2026/timeline.json`
  - `planning/story-production-graph/generated/2026/render_queue.json`

## Board question

Should Schemin:
1. rebase/merge the stale audience-site branch onto current main,
2. cherry-pick the old commits,
3. selectively recover the useful audience-site implementation into a fresh current branch?

## Domain positions

### Architect — recommend selective transplant

The old branch contains useful implementation boundaries:
- `productions/audience-site/build_public_catalog.py`
- `productions/audience-site/src/*`
- `productions/audience-site/tests/*`
- `.github/workflows/audience-site.yml`

But its catalog logic predates the Story Production Graph and therefore duplicates publication/content projection responsibilities now owned by the newer graph.

Recommendation: preserve presentation architecture and tested UX patterns; replace its old publication-projection seam with the current Story Graph consumer feeds.

### Setup Man — reject giant rebase/merge

A 1,249-commit catch-up creates a large conflict surface and obscures which two old commits are genuinely valuable.

Recommendation:
- do not rebase stale branch;
- do not merge stale branch;
- do not blindly cherry-pick both commits;
- create a fresh branch from current main / accepted integration base;
- transplant files or individual hunks with tests.

### Librarian — donor branch, not authority branch

The stale branch is historical implementation evidence, not a current authority source.

Keep:
- layout/navigation patterns;
- site build/recovery documentation;
- tests worth preserving;
- public-only projection discipline.

Do not restore:
- stale task registry state;
- stale release assumptions;
- parallel memo/publication truth;
- any old source-selection logic that conflicts with current publication/Story Graph authority.

### GM — preserve the actual audience journeys

The old audience-site plan correctly identified three audience goals:
1. explore the Commonwealth/world,
2. find/read the correct memo,
3. read approved narrative/character material.

The recovery should be judged by those journeys, not by percentage of old code reused.

Recommendation: reuse the shell only where it accelerates those journeys. Avoid a technical transplant that preserves stale UX just because code exists.

### Umpire — conditions for acceptance

Reject recovery if it:
- creates a second publication authority;
- makes HOLD/BLOCKED content appear public-ready;
- imports stale governance state;
- breaks deep links/history;
- exposes editorial/candidate/internal data;
- claims deployment because code merged;
- bypasses independent QA.

Require:
- explicit source feed tests;
- no-authority-promotion tests;
- direct-link/history tests;
- mobile/accessibility checks;
- exact-revision build evidence.

### Warden — public boundary

The audience site must remain read-only.
No credentials, editor controls, private Mercer content, unpublished candidate payloads, or private analysis may enter the public bundle.

### Closer — synthesis

**Approve Approach C: selective donor transplant onto current architecture.**

The stale branch should be treated as a capability donor, then archived/superseded after the current implementation proves equivalent-or-better audience behavior.

## Alternatives considered

### A — Rebase stale branch onto main
**Rejected.**
Pros: preserves exact old branch history.
Cons: 1,249-commit conflict surface; high integration risk; stale architectural assumptions remain embedded.

### B — Cherry-pick both unique commits
**Rejected as default.**
Pros: simple mechanically.
Cons: commits include governance/task-registry/site assumptions as one historical package; cherry-pick can reintroduce parallel authority and stale state.

### C — Fresh branch + selective transplant
**APPROVED / RECOMMENDED.**
Pros:
- current architecture remains authoritative;
- old site UX/code can be reused surgically;
- Story Graph becomes the data source;
- tests can prove behavior incrementally;
- easy rollback and review.

Cons:
- requires deliberate file/hunk reconciliation rather than one command.

## Approved target architecture

```
Current Schemin authorities
        ↓
Story Production Graph
        ↓
generated/2026/
  web_index.json
  timeline.json
  render_queue.json
        ↓
Audience-site public catalog adapter
        ↓
Existing audience-site shell / reader / atlas presentation patterns
        ↓
Static read-only public build
```

The audience site must consume derived Story Graph outputs; it must not rebuild or supersede canon/publication truth.

## Recovery scope

### Port/adapt
- audience-site README/update/rollback pattern
- static shell and navigation
- reader progress behavior
- memo-card/read paths
- public atlas presentation pattern
- deep-link/history logic
- site-specific tests
- CI pattern, rewritten for current paths

### Rebuild against current interfaces
- public catalog builder
- memo indexing
- release/latest resolution
- Story Graph feed ingestion
- source/version fingerprints
- public eligibility filtering

### Do not port blindly
- old `TASK_REGISTRY_V1.json` modifications
- historical release-state assumptions
- stale branch-specific plans as active control
- duplicate location/character/publication databases
- any branch-only canonical claims

## Execution sequence recommended by board

### R1 — Fresh recovery branch
Create from current integration base, not from stale audience branch.

Suggested:
`feat/commonwealth-audience-site-v2-story-graph`

### R2 — Catalog seam first
Port the site shell/tests, but make its public catalog consume:
- `web_index.json`
- `timeline.json`

Do not wire live renderer output yet; `render_queue.json` currently has zero authorized ready requests.

### R3 — Preserve existing current authorities
Character/world data should continue through active canonical sources or existing current adapters where the site genuinely needs richer display data.

### R4 — Reintroduce site tests under current CI
Minimum tests:
- all nine memo issue records represented truthfully;
- HOLD/BLOCKED remains non-promoted;
- Story Graph fingerprint visible in output;
- stale/candidate records excluded;
- direct memo links do not silently fall back;
- deep-link/history survives reload;
- mobile navigation remains usable;
- source URLs resolve to current authority paths.

### R5 — Visual/reader QA
Run the three audience journeys on desktop/mobile before any deployment claim.

### R6 — Supersede stale branch
After the fresh implementation demonstrates parity or improvement:
- mark `feat/commonwealth-audience-site-20261022` historical/superseded;
- retain it as provenance;
- do not delete history unless separately authorized.

## Board recommendation

**Proceed with a fresh current branch and surgical transplant.**

Do not spend effort making the stale branch “caught up.” Its value is the two unique commits and their site patterns, not its branch ancestry.

## Next canonical Bullpen command

`/bullpen plan --project schemin-26 --objective audience-site-v2-story-graph-recovery --source-branch feat/commonwealth-audience-site-20261022 --target current-main --no-parallel-authority --tdd --evidence-required`

The plan should define exact file-by-file transplant decisions and RED→GREEN tests before implementation begins.
