# Publication Manifest V1 — Index

**Status:** ACTIVE DERIVED INDEX  
**Authority:** Librarian / Release Control consumers  
**Non-authority rule:** this directory does not publish, promote, supersede, or mutate any publication.

## Purpose

Provide one machine-readable index of Schemin publication identity and relationships across:
- Weekly Memo issues;
- Living Novel hard-canon installments;
- future Atlas/special publications;
- season/archive collections;
- release receipts;
- fact/canon/world references;
- world-evolution transaction references when they actually exist.

## Controlling files

1. `PUBLICATION_MANIFEST_V1.json` — derived publication identity registry.
2. `PUBLICATION_MANIFEST_V1.schema.json` — structural schema.
3. `validate_publication_manifest.py` — executable invariants.\n4. `memo_reference_resolver.py` — deterministic Weekly Memo authority resolver.\n5. `test_memo_reference_resolver.py` — explicit-week/current/latest/fail-closed/future-succession regression suite.

## Authority boundary

This registry points to authority. It never becomes authority itself.

Publication state is controlled by the owning system and its existing gates:
- Weekly Memo → Memo OS + release gate + release evidence;
- Living Novel → Novel OS + manuscript/final gates;
- World consequences → World Evolution accepted transactions;
- canon → Character Canon;
- league truth → Data Gateway / verified fact locks.

A manifest entry must not upgrade a blocked/candidate artifact into a release.

## Current seed

The initial registry includes:
- official Week 2 Memo;
- immutable Week 3 Memo;
- blocked Week 4 Memo slot;
- hard-canon Prologue;
- hard-canon Chapter I;
- hard-canon Chapter II;
- Founder-approved hard-canon Chapter III — `THE HILL IS NOT THE KINGDOM`.

Chapter III was added only after independent Novel authority produced `living-novel/qa/CHAPTER_03_FINAL_CANON_GATE_V1.md` and `living-novel/qa/CHAPTER_03_CANON_RELEASE_RECEIPT_V1.md`. The manifest did not create or promote it. Week 3 remains evidence; Chapter III exists because the causal Novel pipeline separately selected, wrote, audited and approved that story unit.

## Acceptance evidence

- `PUBLICATION_MANIFEST_V1_ACCEPTANCE.md` — mission acceptance, audit, learning and rollback receipt.
\n## Weekly Memo benchmark semantics\n\n`CANONICAL_FOR_WEEK` and `CURRENT_BENCHMARK` are distinct. A released Memo remains canonical for its own week indefinitely unless explicitly superseded. Only one released Weekly Memo may carry `metadata.benchmark_status = CURRENT_BENCHMARK`, and it must be the highest released week. Week 2 is historical gold-standard evidence; Week 3 is the current benchmark until a later Memo completes its owning release transaction.\n