# Commonwealth Folio Studio — Third Engineering Pass

**Date:** 2026-11-20
**Base examined:** PR #337 at `5367fefec95c586ab6418dcf6bb631c079c4c1aa`
**Scope:** source-bound backend and frontend coding only, no new image generation, deployment or world-canon promotion
**Methodology:** senior engineering workflows applied to existing project code. The disciplines below are review roles, **not claims that named human engineers were consulted**.

## Engineering review disciplines applied

| Discipline | Risk-first workflow | Executed change | Evidence |
|---|---|---|---|
| Principal / staff software architect | Identify true consumers; preserve existing World Engine ownership; avoid introducing a second registry or generator | Added the source-derived production contract compiler and linked it to the existing Folio builder | Deterministic file and current-source tests |
| Senior backend / data engineer | Define a strict contract, write a failing test first, lock source identity and provenance, implement minimum production transform | 23 canonical LOC packets + 7 region packets, 7 event-source candidates and a separate draft-only Island descriptor; explicit render prohibited | Test failed for missing file before implementation, then new contract tests passed |
| Senior frontend / accessibility engineer | Test functional navigation and mobile layouts in a real browser, not JS syntax alone | Seventh Production Packets tab; source-constraint inspector, usable filters, restored SVG-keyboard focus, synchronized filtered inspector | Chrome DevTools test across all seven views |
| Application security engineer | Fail closed on untrusted paths, restrict active client resources, prevent leaks/promotions | Validate each source card's exact path and LOC ID; CSP restricting scripts, connections, images and styles to same origin | Adversarial path traversal tests; browser CSP compatibility |
| QA / reliability engineer | Add regression guard for each observed defect; verify deterministic output and artifact behavior | Contract/unit tests, source SHA, actual download endpoint test, all-tab 390px overflow checks | Exact-content --check, new Python tests, full browser smoke and CI |
| Release / operations owner | Keep private draft and current canon separate; no public release from a passing local build | Existing CI stays on PR #337; production artifacts explicitly CODE_ONLY_SOURCE_INDEX_NO_IMAGE_GENERATION | Zero raster files; draft-only PR; no source World Engine mutations |

## Code changes

1. `production_packets.py` compiles **30 machine-readable, source-only establishing contracts**: 23 governed LOC IDs and 7 governed regions. Each location packet contains current region/owner bindings, approved structural source URI and checksum, source Location Card checksum, known landmarks, access routes, climate and movement, actual source weather relationships, required visual-prohibition rules, and dated recorded historical event IDs.
2. `build_folio.py` now emits and checksum-verifies `site/data/production_packets.json` alongside the established `world.json` dataset, without new dependencies or image APIs. `--check` also catches stale/extra copies of structural SVGs.
3. `site/index.html`, `site/app.js`, and `site/styles.css` contain a seventh searchable **Production Packets** section, a JSON download link, one-source-per-location inspection and seven physical-region overview cards. All candidate asset paths are clearly described as **nonexistent, nonapproved targets**.
4. Fixed keyboard-focus loss on rebuilding SVG map locations and the proposed Island topology. Navigation now restores focus to the appropriate replacement SVG node after activation.
5. Fixed **real browser-discovered 390px horizontal overflow**: the main map grid needed a shrinkable track; production panel metadata/QA control text needed wrapping. Tests now inspect all seven views, not just the default or Source Evidence screen.
6. Fixed filtered inspector drift: when filters show only one LOC or packet, the inspector now matches the visible result instead of showing a different, previously selected site.
7. Added source-card path validation and a restrictive same-origin Content Security Policy for the read-only frontend.
8. Extended browser checks to request the downloadable packet JSON and assert exact 23/7 counts and **render_permitted=false** on every location.

## Data truth and production constraints

- Three nonexclusive divisions of four team slots; twelve owner-character primary homes.
- Seven physical regions, 23 current mainland locations and 18 routes.
- Legacy 48 `CAND-*` and two different unmerged PR #324/#325 expansion sets remain **proposals**, not extra active `LOC-*`.
- The bridge-connected Postseason Island in PR #322 is still an **unmerged, unmeasured candidate network** (23 nodes, 45 edges, 9 venue candidates). Its relationship to main's Central Basin Last Field candidate remains unresolved. No preview may imply a surveyed causeway or final location.
- Current main World Engine state is dated through **end of Week 3, 2026**. The Folio must not present it as a fully verified Week 11 environmental state. Any 2015–2025 source event is a *candidate temporal reference* until verified for its physical implications.
- 23 SVGs included in the UI are copies of **already-approved structural diagrams**, not generated or approved cinematic masters. **0 approved cinematic masters** remain.
- The compiled packet contract explicitly sets `render_permitted: false`; its site export contains no generation prompts or images.

## Red → green evidence

- Before production compiler: targeted new tests failed because `production_packets.json` did not exist.
- After compiler: 23/7 packet identity, source-byte integrity, forbidden-canon promotion and Island separation tests passed.
- Expanded browser tests found two genuine overflow defects at 390px: Atlas width 487px and Production width 455px. CSS grid shrink and long-token wrapping repaired both. Later tested all seven screens at 390px with no horizontal overflow.
- Keyboard focus and source-filter coherence are now functional browser tests, not only static review observations.
- New fail-closed path tests reject malformed or escaping source Location Card paths. CSP remains limited to source-hosted static assets and source-link navigation.

## Verification commands (no user Mac interaction needed)

From the existing authorized GitHub checkout used for execution:

```sh
python3 world/environment-references/cinematic-folio/build_folio.py --check
python3 -m unittest discover -s world/environment-references/cinematic-folio/tests -p 'test_*.py'
python3 world/environment-references/test_environment_references.py
python3 world/location-control-plane/qa/test_location_control_plane.py
python3 world/qa/test_universe_v1_1.py
node --check world/environment-references/cinematic-folio/site/app.js
```

The CI workflow also runs real headless Chrome navigation, keyboard, all-tab mobile-width, export and source-provenance tests using the existing `browser_smoke.mjs`. The local preview requires no user action and was used only for automated validation, not for a deployed site.

## Hosted-CI reliability correction

The first GitHub Actions run for the third-pass commit passed the deterministic compiler, 22 Folio Python tests, and JavaScript syntax. Its real-browser test **failed before reaching application code**, because hosted Chrome did not expose the DevTools HTTP endpoint at 127.0.0.1:9229 (ECONNREFUSED). This was not a passing CI run.

The browser workflow now starts Chrome with safer hosted-Linux flags including `--disable-dev-shm-usage` and `--no-first-run`, verifies Chrome readiness explicitly, retries once with a fresh isolated profile, prints startup logs on failure, and bounds the Node browser test duration. The app's local real-browser test already passed. Do not mark the hosted browser job PASS unless its new exact-commit workflow run completes successfully.

## Review gate and next real dependency

**Backend and frontend changes:** source-bound implementation and local checks complete; exact-commit CI acceptance is recorded separately after pushing.
**No new images, source canon edits or public deployment:** satisfied.
**Independent external review / approved cinematic image bytes:** not performed or claimed.
**Future actual rendering:** continues under source-hydrated location-specific briefs, creative QA, real image inspection and Founder/Umpire release authority. This pass only prepares the code needed to do that correctly later.
