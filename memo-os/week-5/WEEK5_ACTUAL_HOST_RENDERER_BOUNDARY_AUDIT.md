# Week 5 — Actual Host Renderer Boundary Audit
**Status: GATE 2 PROVIDER_CAPABILITY_BLOCKED / NOT PRODUCTION CERTIFIED**
**Basis:** existing canonical renderer modules, explicit prior portability audit, isolated Mac tests.

## Verified source observations
- `canon/characters/runtime/generation_adapter.py` implements the existing `governed_generate()` eligibility, execution-receipt, and pending-Character-QA contract; PR #151 patches native input `referenced_image_ids` to match approved mounts at the function boundary.
- `canon/characters/runtime/reference_mount.py` requires `mounted_sha256`, Git blob, actual attachment, unique subject-binding proof and capability receipt to mark a mount renderable.
- `canon/characters/missions/2026-09-30-reference-portability/AUDIT_REPORT.md` expressly reports `PROVIDER_CAPABILITY_BLOCKED` because available ChatGPT image generation lacks mounted-byte-hash and deterministic per-subject binding receipts.
- `canon/characters/CCCP_TASK_LEDGER_V1.md` repeats the provider boundary limitation.
- `canon/characters/NATIVE_RENDER_REFERENCE_BINDING_V1.json` records twelve active Library handles but explicitly does not claim fresh source hash computation or host attachment proof.
- Source code search found `governed_generate(` calls in `canon/characters/tests/test_incident_boundary.py`, not a real Week 5 host invocation. A grep audit is *not* proof no host adapter exists elsewhere; host linkage remains unproven.

## Local test evidence
- `python3 -m unittest discover -s canon/characters/tests -p 'test_*.py'`: 46/46 PASS.
- `python3 -m unittest discover -s memo-os/week-5/tests -p 'test_*.py'`: 13/13 PASS.
- Controlled mock-renderer integration confirms exact native reference-ID transport and expected receipt response, but **not** actual provider source attachment or genuine subject binding.
- Novel OS `living-novel/os/transports/renderer_transport.py` supports Comfy/Runpod job submission; its SUBMITTED receipt is not an accepted character identity or output-hash receipt, and it must not be incorrectly promoted into Memo production.

## Gate decision and next minimal repair
**Do not claim host-certified character generation or launch full 12-character production.** Preserve existing CCCP, V5.5 and the new reference-ID input guard.

Choose ONE authorized provider path:
A. Verify a real renderer/provider route that emits actual mounted hash, per-subject binding, capability and output receipts; integrate into existing `generation_adapter.py` contract and test.
B. If using ChatGPT native image generation, obtain an explicit approved authority decision defining a different evidence standard based on exact native Library handle plus final-raster QA. This is a **policy change**, not an engineering workaround, and requires independent acceptance.

Then: one bounded real reference-backed render → verify receipts → inspect final pixels → ConsultEngine per-stage review → independent Umpire before character/Page Lock. Never fabricate host receipts from request metadata.

**Unfinished:** actual native provider invocation, real mount/subject-binding proof, 12/12 character render QA, independent Umpire, and production promotion.
