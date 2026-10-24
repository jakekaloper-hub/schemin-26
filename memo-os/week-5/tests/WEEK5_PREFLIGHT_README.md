# Week 5 Preliminary Manifest Gate — Review Candidate

This additive preflight does **not** supersede Memo OS V5.5, the actual character renderer/source-byte gate, the independent Umpire, or publication acceptance.

## Run
`python3 memo-os/week-5/tests/week5_preflight.py path/to/week5-manifest.json`

The manifest input schema is an **experimental crosswalk** for V5.5 compact page packets. No production pages are certified against it yet. Required properties: `week=5`; `result_state`; `pages[]` with stable `id`, recognized `family`, `narrative_job`, `world_anchor`, `text_safe_zone`, `copy_budget`, `source_refs`; six distinct overtures with matchup IDs. Character-bearing pages must present reference-mount evidence; exact data must be deterministic. Winner POV is blocked until a FACT_LOCK state. Historic banned premises are rejected. Approved pages require a QA receipt.

**Evidence:** eight local smoke checks were executed on 2026-10-11 ET against the equivalent Python gate logic: valid shell and seven known-bad fixtures (wrong week, missing overture, premature winner POV, missing character mount, generated score, superseded sheriff, duplicate IDs); 8/8 behaved as expected. **Not CI; no full-repo regression; no actual renderer/pixel test**. No claim of false-negative-free detection.

## Remaining high-priority gates
1. **Character:** identify all twelve actual source bytes, hashes, registry IDs, renderer mounts and final-raster identities; fail closed until verified.
2. **All-page manifest:** assemble complete issue previs after narrative and facts, then test exact manifest-to-packet counts.
3. **Historical:** replay Week 3/4 real bad and known-good fixtures; verify this gate integrates with existing acceptance machinery rather than introducing a parallel source of truth.
4. **Design:** convert Bible V1.1 into typography and page-family tokens, six-overture coverage, subject-safe zones and phone-size rendered tests.
5. **Assembly:** verify derivative scoreboard portrait sourcing and all-page PDF/HTML export, publication manifest and immutable receipts.

## Source authority
- Existing Week 5 Issue #146, Week 4 incident #131, Memo OS V5.5, six world concept/Atlas packets, winner-POV overture lock, Sunday FLAIM provisional intake.
- Week 4 33-page expansion plan is historical design precedent, **not proof** of audited final 33-page publication bytes.
- Character ID/Atlas acceptance cannot be inferred from prose, team names, or a successful schema test.
