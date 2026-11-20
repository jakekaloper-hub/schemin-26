# 2025 Commonwealth: measured-service V5 — producer developmental and source audit
**2026-11-02 (America/New_York) · PR #243 · DEVELOPMENTAL / NONCANON · NOT independent Authors Council, period Atlas, Character Canon or Umpire clearance**

## Manuscript work executed
Revised the final six-movement Ben Whipple/David Babb chapter itself, not an outline or appended stand-alone commentary, and assembled a new eleven-part source-exact novel. The preserved V4 reading is 63,935 source words including metadata. The V5 reader is **65,940 source words** over eleven chapters; all twelve approved fictional principal POV IDs remain present. Ten source wrappers are unchanged from V4; only the final Ben–David wrapper is replaced. Revised Part 11 is **7,924 source words** versus original **5,919**, a net increase of **2,005 source words**, of which approximately **1,914** were freshly written scene words; remaining change is title and editorial provenance.

Source-exact GitHub preflight fetched each of eleven original file paths and checked source text, Git blob SHA and manifest word count before the new reader was committed. Relevant pins after the in-run correction:
- `THE_DAY_THE_POT_WENT_COLD_BEN_DAVID_2025_DEVELOPMENTAL_V2_NONCANON.md` — Git blob `f38bc57bdf828a8fa7607b1717448cf283a6ce24`
- `READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_MEASURED_SERVICE_V5_NONCANON.md` — Git blob `3dbf0047e81174b203a63b80797894d2f9ccfbe6`
- Archived original `THE_DAY_THE_POT_WENT_COLD_BEN_DAVID_2025_NONCANON.md` preserved — `862d0a9dab9a546a1e110fbc45c474d174b127c3`
- V4 reading remains preserved — `b3ff6735553912ce4c89b5f825767592d6f6180a`

## Actual literary changes
**Ben's third movement:** Worker election no longer resolves into merely symbolic silence. Maren returns with two buckets, challenges a disputed entry for labor actually completed, and declines to have Ben's substitute water-carrying counted as payment of her hours. Tessa insists on recording the worker's objection beside the unresolved clerk's objection without turning election into instant compensation. Ben deliberately resists rescuing the scene with his purse or reputation. His place is to carry water on terms he did not set. The claim remains open.

**David's sixth movement:** The measured service rule now has physical consequences: a first bowl, a parent dividing a portion, a covered cup set aside but not yet verified as delivered, people leaving when the size of the store becomes visible, and a ledger separating authorized food, food actually served and unserved demand. David is tempted to make a public pledge from reserves already diminished by paying the accepted wood; he declines to promise a sum he has not accounted for. Partial fuel payment remains a real disbursement, not a new subsidy. The workers' labor arrears remain.

**Closing adjustment:** The former ending said the pot's sound was 'not yet a meal' while existing narrative activity already showed portions passing to people. It now states that there is supper for some, while the record of the unserved cannot create another portion. This is a material truth condition rather than a sentimental total resolution.

**Timeline correction found and fixed during production:** The newly inserted service scene originally appeared **before** the preceding source's paragraph showing the fire catching. That would have placed hot serving before heat. The scene was relocated after ignition; reader and test Git blob pins were updated. This is an observed author-side error and correction, not independent review.

## Pacing and cross-chapter critique
The final transition from the troupe's missing chair (Part 10) to the kitchen's empty pot (Part 11) now carries a thematic similarity of **empty provisions and obligations that outlive public performance**. It does **not** establish a physical link, travel time, messenger delivery, shared accounts, confirmed common date or a route from Austin's hall to the kitchen. Those would require source/Atlas approval.

**Craft risks left deliberately open for independent challenge:**
1. Ben's extra dispute over wage bookkeeping may still feel too discursive after the earlier steward vote; an independent editor should weigh Maren's visible injury and bucket action against the added speeches.
2. David's ledger metaphor appears repeatedly across Chapters 3, 4 and 11; an independent editor should identify redundant sentences and preserve distinct material stakes. A ledger is not itself an answer to hunger.
3. The fictional kitchen bylaws (four of six to fill a seventh seat, later five of seven for a measured procedure) are coherent within this draft but **not period-approved Commonwealth constitutional law**.
4. The grain list has an authorized measure and specific observable servings, but **no authoritative final number of served/unserved people**. Do not fabricate one to make a clean outcome.
5. Maren, Tessa and Iva have visible agency but none gains independent interior POV; the twelve-owner limit is preserved. The workmen and the hungry child are not secret new narrators.
6. Future grain nonrenewal does not retroactively remove received grain; the two absent future sacks remain prospective. Separate David/Pell partial payment and wage arrears must not be conflated.

## QA provenance, exactly scoped
A sixteen-test mechanical suite at `living-novel/historical-chronicle/qa/test_2025_measured_service_v5_reader.py` checks source bytes/blobs, eleven wrappers, twelve registered owner IDs, six alternating Ben/David movements, preserved ten source chapters, protected 2026 files, measured serving and contractual/evidence holds. Wired to the existing `.github/workflows/novel-os-ci.yml`. First workflow run `41553749329` FAILED **two source-wording assertions**; the observed CI log showed 16 tests with 2 failures. The initial correction run `41554011251` likewise failed those two uncorrected assertions. Only test wording was amended at commit `b2d8c20a4f031f193573ea62ea36574bfe1ef951`: the source states '*future* grain pledges' with intervening words and 'period Atlas hold' rather than the test's exact unstated phrases. Manuscript prose was not rewritten to satisfy them. **At this producer QA snapshot, final-commit CI has not been declared green without an actual readback.**

Four hard-canon 2026 files were fetched from both current `main` and production branch after the revision. Their Git blob SHAs matched exactly; no protected file was edited.

## Release and continuation
**HOLD:** Independent literary, period Character Canon, Historical Librarian, Atlas and Umpire acceptance remains outstanding. No submitted independent PR review at this snapshot. 2025 manager-account identity joins remain unauthenticated; the historical 2016 two-Austin-slot ambiguity and seventy-two Jake-limited chapters cannot be repaired by guessing other historical owners.
**Next eligible work:** Once the amended exact-commit CI outcome is observed, repair actual failures if any; otherwise request independent critique of kitchen bylaw credibility and ledger saturation. Then pursue source-bounded 2016 chapter consolidation without assigning an owner from display names. No merge, publication, financial action or canon promotion.
