# Weekly Memo OS

Canonical home of the Schemin '26 Weekly Memo production system.

## Benchmark authority

**Current Memo benchmark is resolved dynamically, never hard-coded from historical prominence.**

Use `governance/publication-manifest/memo_reference_resolver.py` + `PUBLICATION_MANIFEST_V1.json`.

Current state:
- Week 2 `Week 2 memo.pdf` — canonical for Week 2; **HISTORICAL_GOLD_STANDARD**.
- Week 3 `Pro_Schemin_Week_3_Memo_Final.pdf` — **CURRENT_BENCHMARK**.
- Week 4 — unreleased/blocked and ineligible to satisfy latest/current until its release gate passes and benchmark promotion is transacted.

A historical gold standard remains useful for regression and craft comparison. It is not the default current reference. Search similarity, filename friendliness, prior prompt frequency, or an old “gold standard” label cannot override release authority.

## Fail-closed rule

Explicit week → exact released week only.  
latest/current/benchmark → highest released CURRENT_BENCHMARK.  
unreleased/unknown week → no substitution.

## Production lifecycle
1. Intake
2. Data verification/freeze
3. Rename + canon reconciliation
4. Pre-production
5. Page architecture
6. Copy
7. Art direction
8. Page production
9. Page-by-page QA
10. Final assembly
11. Mobile-readability audit
12. Publication package
13. Postmortem / OS patch

Historical outputs are regression evidence, not current-state defaults or templates to copy verbatim.


## Release-candidate artifact gate (Week 5 learning patch)

**Historical Week 5:** User-confirmed distributed 19-page issue is archived as shipped; do not rewrite or backfill with invented pages. Its visible numbering and provenance issues become future-production regression fixtures.

**New candidate checks:** `memo-os/tests/validate_issue.py` checks the structured release manifest (fact parity, pagination, identity/mobility QA status and dual acceptance). `memo-os/tests/validate_artifacts.py` independently opens the proposed PDF and page-master image files, recomputes SHA-256 values from disk, verifies PDF page count, decodes images and renders all PDF pages at 390px width.

Use the *existing* Memo OS release candidate and manifest; do not start a second registry. A candidate manifest uses `pdf_path`, `published_artifact_sha256`, `expected_pages`, and for each page `slot`, `asset_path`, `asset_sha256`, alongside the existing validator fields. Paths resolve relative to the manifest and cannot escape its directory. Examples may be preflighted in review state, but **actual release requires independent, evidence-backed character, mobile, editorial, Scout and Umpire sign-offs**.

Run on a real staged candidate before approving it:

```bash
python3 -m pip install pymupdf pillow
python3 memo-os/tests/validate_artifacts.py path/to/actual/issue-manifest.json
```

The new CI executes synthetic positive/negative artifact regression fixtures. **CI success by itself does not prove the current weekly PDF passed the candidate gate.** Ensure the actual candidate command has run with archived outputs and reviewer receipts before release. The validator detects render failures but does **not** certify human-readability, character likeness, printed numbers embedded inside raster images, FLAIM source authenticity, or canonical geography. Those remain existing independent desks' responsibilities; a literal `PASS` field alone is not proof.



## Native page geometry — forward-only amendment (2026-10-28)

Newly produced weekly memo page PNGs (including unapproved Week 7 commissions and Week 8 onward) use **1080 × 1920 pixels, exact 9:16** as their native composition master. The authoritative fields and lock conditions are in [`PAGE_PRODUCTION_CONTRACT_V1.md`](PAGE_PRODUCTION_CONTRACT_V1.md). Validate actual bytes with `python memo-os/native_png_contract.py <page.png>`; the `test_native_png_contract.py` regression checks run in the Memo Issue Guardrail workflow. Legacy historical page packets and published images are evidence, not forward raster defaults. Changing the documented target is not proof that every generator/assembler has switched; runtime integration and visual acceptance remain independent gates.

## OpenAI API raster adapter (candidate; not yet live-proven)

The opt-in `memo-os/openai_image_route.py` uses the OpenAI Images API, model `gpt-image-2.5-flare`, and requests a 1152×2048 native 9:16 PNG. The 1080-pixel target width is not divisible by 16, so the adapter uniformly resamples the 9:16 source to the final 1080×1920 master without cropping. It records source and final hashes, rejects wrong source dimensions, and runs the Memo native PNG validator. A command without `--execute-billed` produces only a dry-run request plan; a billable call requires `OPENAI_API_KEY` in the environment plus the explicit flag. Reference-conditioned character likeness and editorial correctness are NOT proven by this adapter; human/independent QA and official provider capabilities remain separate acceptance gates.
