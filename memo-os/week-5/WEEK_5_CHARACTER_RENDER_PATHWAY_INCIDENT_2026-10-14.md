# Week 5 Character Drift — Production Pathway Incident & Corrective Gate

**Basis:** Week 5 Memo production retrospective and distributed-edition post-publication audit, October 14, 2026. This is a Week 5 production incident, **not** a repeat of October 1 source acquisition. The Commissioner already supplied the character references; do not request a bulk re-upload.

## Evidence-backed observations
- Week 5 produced and distributed a 19-sheet edition containing six narrative matchups. Distribution is Commissioner-confirmed; this document does not retroactively grant technical certification.
- Twelve registered Library reference handles matched registry metadata during the Week 5 intake. That establishes source identity metadata, not a specific renderer input receipt.
- Seven Deadly Chins and Slob were rendered as human stand-ins in some Week 5 artwork; DK and TDS continuity remained at risk.
- During retry cycles, wrong matchup/page results appeared, and generated factual typography drifted. Those are adjacent, separately controlled Memo fidelity failures.
- Current Week 5 retrospective does **not** preserve complete per-render API/prompt invocation logs, mounted image hashes or subject slot bindings for all candidate raster attempts. We cannot infer exact backend behavior or prove that a specific reference was attached to each failing render.

## Failure chain
1. **Input / source resolution:** canonical references existed; 12 metadata handles checked. This stage is *not* demonstrated to be the failure.
2. **Render invocation:** absence of per-character mount hash, subject slot and capability receipts means `REFERENCE_ATTACH_PROVEN` and `SUBJECT_BINDING_PROVEN` cannot be established. It is an evidence gap; possible semantic regeneration remains a hypothesis, not a proven provider root cause.
3. **Output review:** wrong-body/stand-in raster candidates reached editorial assembly/retries despite explicit canon lock. The absence of durable per-character QA tied to exact output bytes is a defensible control failure.
4. **Release:** the 19-page edition was distributed. Do not rewrite history or recast the release as unpublished; preserve provenance and record technical certification separately.

## Implemented control
- `memo-os/tests/validate_character_provenance.py`: a released character-bearing page now needs a **per-character** receipt tied to the actual master page SHA, canonical source binary hash, mounted hash, generation reference ID, subject slot, explicit binding ID, renderer/capability receipt, output-instance ID and independent reviewer identity.
- Requires actual accessible source bytes and reviewed raster bytes inside the release candidate evidence bundle. Source/raster hash mismatches, missing subjects, missing mounts or self-review fail closed.
- Integrated into existing `memo-os/tests/validate_artifacts.py` real candidate path and `memo-issue-guardrails-ci.yml`. Historical distributed issues are not retroactively invalidated: requirement applies to future **released** candidates.
- These metadata/byte checks **do not independently authenticate** that the renderer really mounted the bytes or that a reviewer actually examined likeness. Such provenance requires actual provider logs/mount receipts and audited visual comparison.

## Still required
1. Collect existing Week 5 attempt artifacts where available, preserving exact request IDs, prompt + image attachment set, render outputs and selected/rejected page hashes. Do not manufacture missing attempt receipts.
2. In a future controlled single-character C1 invocation, prove reference source hash → real renderer mount → subject slot → output image bytes → reviewer-approved QA crop. Provider capability gaps must be named, not hidden with fabricated true flags.
3. Only then run two-character and multiple-character contamination tests; explicitly test Seven Chins/Slob stand-ins and DK/TDS anatomy errors.
4. Independent Umpire checks real asset comparisons and issue PDFs, not only declared `PASS` fields. Human and authenticated reviewer evidence cannot be replaced by this validator.
5. Reconcile any impact on already staged release candidate formats; use normal migration with no false green.

**Production status:** Source identities known; Week 5 generation-pathway failure observed; per-request provider mechanism remains unproven. Future evidence gate implemented, real mount and subject-binding proof still external to the CI fixture.
