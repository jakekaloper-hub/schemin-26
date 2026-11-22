# Schemin Bullpen Runtime — Local Model Draft Canary

**Status: narrow live execution proof; not a release acceptance.** 2026-11-22.

## Existing runtime + new adapter

The existing `BullpenRuntime` accepts injected worker functions, stores stage artifacts, and separately invokes independent stage gates. A new `src/model-draft-worker.js` adapter permits a real, explicitly supplied `ModelProvider.generate` function to produce a provenance-bound **UNREVIEWED** text candidate after rehashing its supplied source text.

The adapter never sets `canon_approved`, `publication_eligible` or `character_renderer_eligible` to true; it never supplies an image-generation worker or an independent gate. Invalid/missing source bytes and empty/failing model calls return blocked results instead of fabricated artifacts.

## Local proof

Run on an owner-authorized Mac, using the existing Bullpen `authenticatedChat` provider pointed to a loopback-only, no-paid-API Ollama server (`qwen2.5-coder:7b`). The test source was the current checkout's `SCHEMIN_26_PROJECT_MISSION.md`; no private character image, ESPN credentials, or paid service used.

- Source packet: **PASSED** against a fresh source SHA-256 check.
- Manuscript text draft: **PASSED** its deterministic *draft-contract* gate. Generated text remains unreviewed; the model's claims are not independently fact-certified.
- Art job: **BLOCKED** with `missing worker: visualDevelopment`, as required.
- Actual artifact records: **2**; actual approved images: **0**.
- Exit code: **0**, because the smoke explicitly asserted that the art-stage block was the expected result.
- Local receipt: outside public Git, with source/draft hashes and stage states but no public raw model text.

## Verification

Red-phase import/test failure was observed before implementation. Targeted new tests: **4/4 passed**; full `bullpen-runtime` suite after the change: **28/28 passed**. These are local Mac checks, not hosted CI or independent production acceptance.

## Next binding boundary

Connect a real approved, reference-aware image worker with independent character/visual QA and artifact storage *only after* exact reference-byte custody and renderer subject-binding proofs. Until that happens, the art stage remains BLOCKED. Do not mark the pipeline production-ready from the text-only canary.
