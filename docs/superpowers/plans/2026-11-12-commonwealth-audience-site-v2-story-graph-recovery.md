# Commonwealth Audience Site V2 — Story Graph Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Recover the useful Commonwealth audience-site implementation from `feat/commonwealth-audience-site-20261022` onto a fresh current branch, with Story Production Graph outputs as the read-only memo/timeline source and no parallel publication authority.

**Architecture:** Treat the stale branch as a donor only. Create a fresh branch from the current Story Graph integration base, port the static shell/reader/atlas patterns, and replace the old memo/publication projection with adapters over `generated/2026/web_index.json` and `timeline.json`. Character/world display may continue to read current canonical sources, but the site must not create canon, release state, or renderer eligibility.

**Tech Stack:** Python 3.12 stdlib, Node 22 built-in test runner, static HTML/CSS/ES modules, existing repository data; no new npm/runtime dependencies.

**Spec:** `planning/story-production-graph/AUDIENCE_SITE_BRANCH_RECOVERY_BOARD_2026-11-12.md`

## Global Constraints

- Do not rebase or merge `feat/commonwealth-audience-site-20261022`.
- Do not blindly cherry-pick its two commits.
- Fresh recovery branch: `feat/commonwealth-audience-site-v2-story-graph`.
- Initial base: current Story Graph integration head; retarget/rebase onto `main` only after PR #307 is accepted/merged.
- Story Graph consumer outputs are read-only projections and may not promote canon/publication state.
- `render_queue.json` is informational only; no renderer execution from the audience site.
- Do not import stale `TASK_REGISTRY_V1.json` changes.
- Do not create duplicate character, world, memo, or publication databases.
- Public bundle must exclude Mercer/private analysis, candidate/editorial payloads, credentials, and write controls.
- No new third-party dependencies.
- Merge, deployment, and public release remain separate governance states.

## Review Focus

1. HOLD/BLOCKED or external-only memo records must never become active released-edition links.
2. A stale Story Graph fingerprint must fail the site build rather than silently mixing revisions.
3. Unknown/missing Scene or memo IDs must render an unavailable state, not fall back to a different issue.
4. Deep links and browser history must survive direct load/reload without requiring navigation from home.
5. Mobile/reduced-motion/storage-denied paths must preserve reading/navigation functionality.

---

### Task 1: Fresh branch and donor-file recovery

**Files:**
- Create on fresh branch: `productions/audience-site/README.md`
- Create: `productions/audience-site/src/index.html`
- Create: `productions/audience-site/src/styles.css`
- Create: `productions/audience-site/src/progress.js`
- Create: `productions/audience-site/tests/progress.test.mjs`
- Create: `productions/audience-site/package.json`

**Interfaces:**
- Consumes: donor files from `feat/commonwealth-audience-site-20261022`.
- Produces: current-branch static shell and versioned local progress helper; no data/catalog integration yet.

- [ ] **Step 1: Create the fresh recovery branch from the current Story Graph integration head**

Run:
```bash
git switch story-production-graph-v1
git switch -c feat/commonwealth-audience-site-v2-story-graph
```

Expected: new branch contains current Story Graph files and no stale audience-site branch ancestry.

- [ ] **Step 2: Port only the shell/progress files from the donor branch**

Use file-level checkout/copy from `feat/commonwealth-audience-site-20261022`; do not port old governance/task-registry changes.

- [ ] **Step 3: Run the donor progress tests before modification**

Run:
```bash
npm --prefix productions/audience-site test
```

Expected: PASS for same-publication reload, source-version isolation, corrupt/blocked storage, and normalized range.

- [ ] **Step 4: Add a test that progress keys remain source-fingerprint specific**

Test: two identical publication IDs with different Story Graph fingerprints must not share progress.

Expected before change: FAIL if current helper lacks this binding.

- [ ] **Step 5: Implement the minimum progress-key adjustment and rerun Node tests**

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add productions/audience-site
git commit -m "feat: recover audience site shell on current Story Graph base"
```

---

### Task 2: Story Graph public catalog adapter

**Files:**
- Create: `productions/audience-site/build_public_catalog.py`
- Create: `productions/audience-site/tests/test_public_catalog.py`
- Consume: `planning/story-production-graph/generated/2026/web_index.json`
- Consume: `planning/story-production-graph/generated/2026/timeline.json`
- Consume current canonical character/world files already used by the donor builder where needed.

**Interfaces:**
- Consumes:
  - `build_catalog(output: Path, render: bool=False) -> dict`
  - Story Graph `web_index.json`, `timeline.json`
  - current character/world sources.
- Produces: `dist/data.json` with site-only public projection.

- [ ] **Step 1: Write failing test `test_story_graph_fingerprint_is_preserved`**

Assert:
- catalog metadata contains the exact Story Graph `source_fingerprint_sha256`;
- memo records originate from Story Graph issue IDs.

Expected: FAIL because V2 catalog builder does not exist.

- [ ] **Step 2: Write failing test `test_all_nine_memo_records_project_without_release_promotion`**

Assert:
- weeks 1–9 all exist;
- W1 unresolved stays unavailable;
- HOLD/BLOCKED records are not marked released/current;
- no silent fallback to another week.

Expected: FAIL.

- [ ] **Step 3: Write failing test `test_story_graph_timeline_projects_42_events_without_authority_change`**

Assert each projected timeline entry preserves `evidence_status` and `canon_status`.

Expected: FAIL.

- [ ] **Step 4: Implement `build_catalog(output: Path, render: bool=False) -> dict`**

Use Story Graph outputs for memo/timeline truth. Reuse current canonical character/world source adapters only for richer public display fields.

- [ ] **Step 5: Add stale-fingerprint negative test**

Provide mismatched `web_index` and compiler/source fingerprint fixture; builder raises `ValueError`.

- [ ] **Step 6: Run catalog tests**

Run:
```bash
python3 productions/audience-site/tests/test_public_catalog.py
```

Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
git add productions/audience-site/build_public_catalog.py productions/audience-site/tests/test_public_catalog.py
git commit -m "feat: bind audience catalog to Story Graph"
```

---

### Task 3: Port the audience UI against the new catalog contract

**Files:**
- Create/adapt: `productions/audience-site/src/app.js`
- Modify: `productions/audience-site/src/index.html`
- Modify: `productions/audience-site/src/styles.css`
- Test: `productions/audience-site/tests/routes.test.mjs` or equivalent dependency-free route tests.

**Interfaces:**
- Consumes: generated `dist/data.json`.
- Produces: read-only routes for home, atlas, characters, memo archive/issue, library/timeline.

- [ ] **Step 1: Write failing route tests**

Cover:
- direct `#memo/week-9`;
- direct unavailable memo;
- unknown ID returns unavailable/not-found state;
- no fallback to another memo;
- back/forward route parsing remains stable.

- [ ] **Step 2: Port donor `app.js` presentation primitives**

Keep:
- shell/navigation;
- atlas/character layouts;
- memo cards;
- reader-progress behavior.

Remove/rewrite:
- stale assumptions about “latest released memo”;
- direct old-catalog release logic.

- [ ] **Step 3: Add visible state treatment for Story Graph authority**

Memo cards/details must display source state such as Released / Hold / Blocked / Authority unresolved without turning those states into editorial copy that implies promotion.

- [ ] **Step 4: Run Node tests**

Run:
```bash
npm --prefix productions/audience-site test
```

Expected: PASS.

- [ ] **Step 5: Build no-render catalog and smoke-check generated static files**

Run:
```bash
python3 productions/audience-site/build_public_catalog.py --no-render
```

Expected: `dist/data.json`, HTML/CSS/JS exist; no private/candidate payload keys.

- [ ] **Step 6: Commit**

```bash
git add productions/audience-site/src productions/audience-site/tests
git commit -m "feat: adapt Commonwealth reader to Story Graph catalog"
```

---

### Task 4: Public-boundary and provenance hardening

**Files:**
- Modify: `productions/audience-site/tests/test_public_catalog.py`
- Modify: `productions/audience-site/build_public_catalog.py`
- Optional create: `productions/audience-site/tests/test_public_bundle.py`

**Interfaces:**
- Consumes: built catalog and static bundle.
- Produces: fail-closed public eligibility proof.

- [ ] **Step 1: Add failing test for prohibited internal payloads**

Reject any catalog key/value containing:
- Mercer-private strategy;
- candidate/editorial records;
- credential/token fields;
- private repository-only analysis pointers that are not public-safe sources.

- [ ] **Step 2: Add failing test that every source link is revision-pinned or explicitly external-authority labeled**

No hard-coded `/blob/main/` links for content claims.

- [ ] **Step 3: Add broken-source test**

If an active CTA points to a missing artifact/source, the builder must mark it unavailable instead of producing a broken active link.

- [ ] **Step 4: Implement minimal filtering/eligibility helpers**

Do not add a new authority database; consume the existing Story Graph/publication evidence.

- [ ] **Step 5: Run Python + Node suites**

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add productions/audience-site
git commit -m "test: harden Commonwealth public data boundary"
```

---

### Task 5: Current CI integration

**Files:**
- Create/adapt: `.github/workflows/audience-site.yml`
- Modify if needed: `governance/repository-protection/merge_gate.py`
- Test: `governance/repository-protection/test_merge_gate.py`

**Interfaces:**
- Consumes: audience-site paths plus Story Graph generated feeds.
- Produces: path-scoped CI proof.

- [ ] **Step 1: Add failing merge-gate planner test**

Any change under:
- `productions/audience-site/**`
- Story Graph public consumer JSONs
must schedule audience-site verification.

- [ ] **Step 2: Adapt the donor workflow**

Required commands:
```bash
python3 productions/audience-site/tests/test_public_catalog.py
npm --prefix productions/audience-site test
python3 productions/audience-site/build_public_catalog.py --no-render
python3 planning/story-production-graph/build_downstream_consumers.py --check
python3 governance/publication-manifest/validate_publication_manifest.py
python3 governance/repository-architecture/validate_repository_architecture.py
python3 world/qa/test_one_world_model_contract.py
```

Do not add deployment steps.

- [ ] **Step 3: Run merge-gate planner test**

Expected: PASS.

- [ ] **Step 4: Trigger full PR CI and inspect exact-head results**

Expected:
- Story Graph suite PASS;
- audience-site suite PASS;
- Cross-Domain Authority CI PASS;
- Bullpen Runtime CI PASS.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/audience-site.yml governance/repository-protection
git commit -m "ci: verify Story Graph-backed audience site"
```

---

### Task 6: Audience journey QA and stale-branch supersession packet

**Files:**
- Create: `planning/audience-site/V2_STORY_GRAPH_RECOVERY_RECEIPT.md`
- Modify: `productions/audience-site/README.md`
- Do not delete stale branch.

**Interfaces:**
- Consumes: exact current commit, generated site build, CI receipts.
- Produces: technical recovery receipt and supersession recommendation.

- [ ] **Step 1: Exercise the three canonical journeys**

1. Home → Atlas/location → character.
2. Home → Dispatches → explicit memo week.
3. Home → Library/timeline → source-linked historical item.

Test at minimum:
- 390px/mobile layout;
- 1440px/desktop layout;
- keyboard navigation;
- reduced-motion;
- reload/deep-link;
- unavailable content.

- [ ] **Step 2: Record actual defects and repair P0/P1/P2 failures**

No founder-experience approval is inferred from technical QA.

- [ ] **Step 3: Build exact-revision recovery receipt**

Record:
- donor branch and compare state;
- files/patterns ported;
- files deliberately rejected;
- current Story Graph fingerprint;
- test commands/results;
- deployment state = NOT_DEPLOYED unless separately executed.

- [ ] **Step 4: Mark stale branch as superseded in documentation only**

State:
`feat/commonwealth-audience-site-20261022` remains historical provenance and is not the active implementation.

Do not delete branch without separate authorization.

- [ ] **Step 5: Run complete current suites one final time**

Expected: all green on exact HEAD.

- [ ] **Step 6: Commit**

```bash
git add planning/audience-site productions/audience-site
git commit -m "docs: close audience-site V2 recovery"
```

## Self-Review

- Spec coverage: board-approved selective-transplant strategy is covered by Tasks 1–6.
- Authority boundary: Story Graph/publication/world/character authorities remain upstream; site is presentation-only.
- Type/interface consistency: `build_catalog(...)->dict` is the single site data seam; UI consumes only generated catalog.
- Review-focus failures are each assigned explicit tests.
- No implementation task depends on stale branch governance state.
- No deployment or founder visual acceptance is implied by build/test success.

## Execution handoff

Recommended execution mode: **Native / inline TDD**, because the six tasks share a tight catalog→UI→CI interface and the current Story Graph branch already contains the required evidence/test harness. A fresh independent review should still gate merge at the end.
