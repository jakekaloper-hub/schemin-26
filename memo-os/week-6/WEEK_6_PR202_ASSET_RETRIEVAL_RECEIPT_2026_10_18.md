# Week 6 cinematic candidate GitHub ingestion receipt

Date: 2026-10-18. Actual authorized Mac Git checkout and push, not simulation.

Source: Commissioner's previously supplied ZIP in Mac Downloads. The existing fail-closed importer verified all six PNG members, matching SHA-256 fingerprints, image signatures, dimensions 1672x941 and distinct LOC IDs. The importer was rerun in --write candidate-only mode and staged six image files (19,088,501 bytes total) without changing `LOCATION_REFERENCE_REGISTRY.json`.

Commit `2c78205abf71d5d48e65c4256a9633459ef4074e` pushed to GitHub branch `memo/week6-cinematic-asset-ingestion-20261018` and PR #202, based on PR #200.

**Independent repository clean-clone check**: cloned the PR #202 branch into a new temp checkout from GitHub. Read all six PNGs from the actual repository and recomputed SHA-256 values, byte lengths, PNG dimensions against the six-field manifest: **6/6 PASS**. Existing cinematic metadata/structural reference test: **6/6 PASS**. Location Control Plane suite: **15/15 PASS**.

This is evidence of durable candidate bytes and actual Git clean-context retrieval, **not** evidence of renderer/native model reference attachment. Active cinematic approvals remain empty. Character render/compositing with the merged PR #201 owner lineup, spatial metrics, Slob's pickup-truck issue, independent Umpire, Commissioner final approval and integration/main merge remain outstanding.

Safe status: `ASSET_INGESTION = COMPLETE`, `GIT_RETRIEVAL = COMPLETE`, `RUNTIME_RENDERER_REFERENCE_BINDING = HOLD`, `CINEMATIC_CANON_PROMOTION = HOLD`.
