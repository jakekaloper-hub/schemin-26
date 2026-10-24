> **Historical candidate record (October 12–13):** Preserved for provenance, not current source or release authority. Current approved character registry, visual-reference authority and October 18 lineup prevail; older source supersession and 32-page planning claims below are not reactivated. Current release status resolves through `governance/publication-manifest/PUBLICATION_MANIFEST_V1.json`.

# Week 5 P011 — Final Result Banner failure, factual closure and corrected PNG candidate

**Commissioner issue:** P011 did not meet the proven Week 4 payoff-page visual standard and lacked a full scoring/record/owner portrait result bar. The lack of result-bar visual QA across all six final matchup pages was a production system defect, not a Commissioner input gap.

## Official Week 4 acceptance comparator

The Commissioner-uploaded 33-page **official Week 4 memo** was inspected at P008 / P012 / P016 / P020 / P024 / P028. Its completed matchup pages contain an **integrated low result strip** with two team names, two illustrated character close-up portraits, real final scores, visible records, and winner direction. P011's prior scene did not include any strip or records. This 2026-10-13 finding adds a required physical-artifact component; image-PNG metadata CI alone is insufficient.

## Authoritative new Week 5 result

Connected FLAIM read of ESPN league `1417621`, 2026 Week 5 now reports **official winner `AWAY`**, current matchup period 6, completed season standings reflecting Week 5:
- Visitor **The LLC. — 193.73** points; **2–3** record **after Week 5**.
- Host **Mud Dogs — 127.09** points; **2–3** record **after Week 5**.
- Margin **66.64** fantasy points. Both fantasy score and W/L were obtained from the provider, not inferred from old provisional packets.
- The earlier **`UNDECIDED`** branch remains a historical snapshot and is now superseded for this matchup's final result.

All six payoff source pages now have official result, both post-Week 5 records, owner-portrait requirements and physical banner hard-reject gates in `production-evidence/WEEK_5_SIX_PAYOFF_FINAL_RESULT_BANNER_LOCK_2026-10-13.json`: P007, P011, P015, P019, P023, P027.

## Corrected P011 actual image proof

**Base scene preserved:** session artifact `SCHEMIN26_W05_P011_LLC_MUD_PAYOFF.png`, original SHA-256 `0f805b4497f743fd66067bfd844f656cb545a344dc52bf3dc32dfd4053c70479`, 1024×1536. Its recognizable David Babb/Bobby Mitchell figures and the bounded industrial aftermath were preserved. Original scene's top `The LLC. at Mud Dogs` header and narrative remain.

**Image-model edit rejection:** A newly generated candidate fabricated `147.43` and `126.86`, `1–4`, and an unauthorized golden retriever. It was **REJECTED**, not accepted for the official memo. Generative rendering must **not** typeset unverifiable numerical results or invent background owner-character companions.

**Revised deterministic composite:** `SCHEMIN26_W05_P011_LLC_MUD_PAYOFF_REVISED_FINAL_BANNER_CANDIDATE.png` at **1024×1536**, **2,543,056 bytes**, raw SHA-256 `3c0090de7da5176fb53572d528d715762464b0fd8072a9d073fa51f65da15d24`.
- Added dark black/bronze/amber illustrated lower result panel with the verified exact `193.73`, `127.09`, `WINNER`, `2–3`, `2–3`, and a `66.64`-point winning margin.
- The two genuine portrait insets were **cropped from the actual existing P011 illustrated characters**, not fabricated by an image model, not taken from a stock human/dog and not linked to another fantasy owner.
- Re-rendered an actual 390×585 PNG preview and opened both full-size and 390px output for human operator self-review. The banner shows both face insets and main scores at phone width; body narration remains a relatively small typography risk inherited from the original.
- Output and 390px image are session artifacts. **Their raw bytes have not been committed to GitHub** by this Markdown receipt.

## Authority / handoff

**STRUCTURAL PASS:** banner exists, scores/records/winner correct, character source crops correct, 1024×1536 PNG, 390px visual preview, original scenic content maintained. **Not an independent Umpire pass**: authenticated separate Umpire/Director review and renderer mounted-original source receipts are still missing; do not mark `ACCEPTED_FINAL` merely because a page proof now includes its result panel. The Commissioner need not re-enter any Week 5 scores or records.

**Release rule:** Every payoff page must fail if its rendered result strip lacks either exact score, both post-Week 5 records, two correctly bound character-face insets, proper result direction, or 390px readability. The payoff-strip acceptance test is now added to `tests/test_week5_artwork_first_output_contract.py`; production packet, manifest and master authority must refer to this rule.
