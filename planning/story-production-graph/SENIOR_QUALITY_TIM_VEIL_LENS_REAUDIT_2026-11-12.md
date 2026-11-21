# Story Production Graph V1 — Senior Quality Re-Audit + Tim Veil Published-Method Lens

**Date:** 2026-11-12  
**PR:** #307  
**Exact reviewed HEAD:** `2e792b1a57eaf498471b713b8ff1fe19772f4f93`  
**Related audit:** #308

## Evidence boundary

This review is a senior engineering re-audit performed against the repository implementation and CI evidence.

The Tim Veil portion is **not a live human consultation and not a statement from Tim Veil**. It applies the canonical Bullpen `PUBLISHED_METHOD_LENS` documented in:
- `jakekaloper-hub/bullpen/docs/advisors/TIM_VEIL_ADVISORY_LENS_V1.md`
- `jakekaloper-hub/bullpen/research/advisors/TIM_VEIL_INTEGRATION_DOMAIN_DECISIONS_2026-10-10.md`
- `jakekaloper-hub/bullpen/audits/TIM_VEIL_IMPLEMENTATION_RECEIPT_2026-10-10.md`

Canonical Bullpen doctrine explicitly requires `humanVerified=false` for modeled external-advisor output and prohibits attributing generated opinions to the named person.

## Senior engineering review criteria

The re-audit challenged the implementation on:
1. authority preservation / no silent promotion;
2. deterministic repeated builds;
3. stable cryptographic provenance;
4. mutation-sensitive source fingerprints;
5. referential integrity;
6. ID uniqueness;
7. graph acyclicity;
8. fail-closed job readiness;
9. schema conformance;
10. source receipt completeness at render boundaries;
11. persisted read-model drift;
12. negative/blocked execution behavior;
13. selective invalidation precision;
14. cross-domain authority boundaries;
15. no false renderer/publication claims.

## Tim Veil lens applied

The canonical Tim Veil source program prioritizes:
- repeatable benchmark workloads;
- deterministic fixtures;
- referential integrity and schema-aware data;
- failure injection and negative tests;
- bounded, observable failure behavior;
- source/provenance discipline;
- architecture/API fitness;
- independent acceptance after implementation.

The following senior tests were added specifically to operationalize that lens:

- `test_repeated_build_is_byte_deterministic`
- `test_all_primary_ids_are_unique`
- `test_all_graph_references_resolve`
- `test_dependency_graph_is_acyclic`
- `test_compiler_fingerprint_is_sha256_and_stable`
- `test_input_mutation_changes_compiler_fingerprint`
- `test_event_source_receipts_are_in_render_request_provenance_contract`

The stricter tests found two additional defects after the earlier #308 remediation:
- Week 5 Scenes referenced Encounter IDs that did not exist.
- Week 5 Encounter source packets did not expose separate persistent anchor strings required by Encounter V1.

Both were corrected without inventing canon:
- six Week 5 Encounter objects are now materialized from exact source-backed page packets;
- their minimum persistent anchor falls back to the already-resolved `LOC-*` identifier rather than invented scenery.

## Architecture improvements made in this re-audit

### Graph integrity
Added `graph_integrity.py` with:
- duplicate-ID rejection;
- Event/Encounter/Scene/Job referential-integrity validation;
- typed virtual dependency-root checks;
- cycle detection using a deterministic topological traversal.

### Cryptographic source fingerprint
The production compiler now records:
`source_fingerprint_sha256`

The fingerprint is derived deterministically from canonical serialized:
- Events;
- Scenes;
- Memo Issue nodes.

A synthetic source mutation must change the fingerprint.

### Render provenance
Render requests now preserve the union of:
- Event evidence receipts;
- Scene evidence receipts.

The renderer boundary therefore cannot discard upstream fact provenance.

### Week 5 graph completeness
Week 5 now has:
- source-backed Events;
- source-backed Scenes;
- materialized Encounter objects;
- Encounter→Scene referential integrity.

### Compiler contract consistency
Both base compiler manifests and season manifests now satisfy the fingerprint contract.

## Fresh exact-HEAD evidence

On `2e792b1a57eaf498471b713b8ff1fe19772f4f93`:

- Repository Merge Gate #3078 — **PASS**
- Story Production Graph suite — **50 tests PASS**
- Persisted corpus — **PASS: 49 Scenes / 12 character timelines**
- Selective invalidation — **PASS**
- Tim-lens determinism test — **PASS**
- Tim-lens stable SHA-256 fingerprint — **PASS**
- Tim-lens mutation-sensitive fingerprint — **PASS**
- Tim-lens unique IDs — **PASS**
- Tim-lens reference resolution — **PASS**
- Tim-lens dependency DAG — **PASS**
- Tim-lens complete render provenance — **PASS**
- Bullpen Runtime CI #9911 — **PASS**
- Cross-Domain Authority CI #3018 — **PASS**

## Senior-quality disposition

**IMPLEMENTATION QUALITY: PASS at senior-engineering candidate level.**

The code is now internally consistent, fail-closed, deterministic, provenance-aware, schema-validated, graph-integrity checked, and regression protected.

This statement is intentionally narrower than “production release complete.”

## Remaining gates / limitations

1. **Independent Umpire/code review remains pending.** The implementing runtime cannot self-certify that gate.
2. **No live Tim Veil human review occurred.** This is the canonical published-method lens only.
3. **No real renderer execution is claimed.** The no-render proof validates authority transfer and lineage, not image/video generation quality.
4. **W1/W2 raw publication binaries remain external/unavailable in this repo.**
5. **Scene hydration remains source-bounded:** W5/W6/W9 have reusable Scene coverage; W3/W4/W7/W8 do not invent scene geometry to fill gaps.
6. **Project Control promotion and merge remain separate governance decisions.**

## Recommendation

PR #307 is technically ready for **independent review**. Do not weaken the remaining independent gate merely because automated evidence is now green.
