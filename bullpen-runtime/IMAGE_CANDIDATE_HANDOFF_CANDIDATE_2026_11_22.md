# Bullpen Image Candidate Handoff — source-bound implementation checkpoint

**Date:** 2026-11-22
**State:** TESTED CANDIDATE / NOT A PRODUCTION RENDERER / NOT APPROVED FOR PUBLICATION
**Parent:** Draft PR #346 `feat/gap-remediation-canary-20261122`
**Current target:** existing `bullpen-runtime` `art_job` stage, not a new OS or workflow.

## Delivered

`src/image-candidate-worker.js` is an injectable, provider-neutral candidate-artwork adapter. It deliberately does **not** choose or install an image model, read private character originals on its own, or approve art. It requires two distinct external services:

- **`referenceCustodian.verify(request)`**: an independently sourced custody and reference-binding check, with an exact per-character source hash, mount hash, subject slot and binding reference;
- **`renderer.render({request,custody_receipt_id})`**: an actual authorized renderer invocation, returning an output-instance receipt and per-character echoes of the binding fields.

The worker rejects malformed/duplicate character claims, missing independent custody, mismatched mount/reference/subject slots, swapped page/request identifiers, missing output-instance IDs, custody-receipt mismatches and altered/missing PNG bytes. It reuses the existing `raster-preflight.js` from PR #346 to check an exact `1080×1920` PNG and its caller-supplied SHA-256. Successful adapter output is **`RENDERED_UNAPPROVED`** and explicitly says that reference echoes are not authenticated proof that the provider actually mounted images.

The canonical pipeline and independent `characterVisionGate`, `renderGate`, `final_qa` and publication gates remain unchanged. A candidate without an independent visual-QA gate is a blocked production stage; a model cannot approve its own work.

## Test-first and actual-source evidence

- Initial eight tests were run before implementation: **RED** (module absent).
- A targeted negative test for swapped source/custody receipts was run before strengthening the adapter: **RED**, then **GREEN** after requiring both exact echoes.
- **8/8 focused worker tests PASS**. Coverage includes unavailable adapters, malformed/duplicate subjects, custody failures, per-subject echo mismatch, swapped render identity/custody, corrupted/missing PNG, candidate-only output, and independent-gate absence.
- **41/41 full `bullpen-runtime` tests PASS**, including the parent PR's text-model and raster-preflight regressions.
- Read-only `scripts/image-handoff-canary.js` was run against the actual three local Week 10 `render-inputs/W10-P05..P07/request.json` inputs from the existing recovery checkout. P05, P06 and P07 each contained **two distinct character IDs, three character image-reference entries and zero complete generation binding receipts**. Each returned `BLOCKED / UNVERIFIED_RENDER_PACKET`; **zero images generated**.
- The canary prints only page IDs, request digests, character IDs and status. It does not copy reference binaries or fabricate source-attachment receipts.

## What this checkpoint does NOT prove

- It has no certified live image renderer or independently authenticated source-custody provider attached.
- It does not prove the renderer actually used the intended image source, nor inspect facial/morphology consistency or the final copy.
- The synthetic positive test demonstrates only the adapter contract, not production-grade provider integrity.
- A render-result hash echoed by the provider confirms local output-byte consistency, not independent provider/source authenticity.
- The missing 8/12 original character source custody items documented by PR #346 remain unresolved. In particular, this code does not turn a lineup crop or a Library record into a qualifying primary source.
- No story, character canon, world state, draft PR, release or original Week 10 folio is promoted or overwritten.

## Reproduce

```sh
cd bullpen-runtime
npm test
node scripts/image-handoff-canary.js \
  /path/to/memo-os/week-10/preproduction/render-inputs/W10-P05/request.json \
  /path/to/memo-os/week-10/preproduction/render-inputs/W10-P06/request.json \
  /path/to/memo-os/week-10/preproduction/render-inputs/W10-P07/request.json
```

## Next genuine production gate

Complete and independently validate current primary-source byte custody and exact per-subject renderer mount/binding receipts; integrate a real authorized image-rendering adapter and separate visual inspector; then run a **single-character canary** with human/independent visual QA against the actual output raster. Do not activate batch Weekly Memo character generation or publish a scored image until that evidence passes.

The weekly Memo release validator at `memo-os/tests/validate_character_provenance.py` remains separately binding. This work consumes its required evidence **concepts**; it does not replace that release validator.
