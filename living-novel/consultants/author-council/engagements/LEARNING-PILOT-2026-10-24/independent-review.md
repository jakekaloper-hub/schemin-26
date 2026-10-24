# Independent bounded pilot review — 2026-10-24

Reviewer: separate Codex reviewer invocation `/root/pilot_review`, performing Umpire-style technical/editorial analysis. This is an independent agent review, not an actual author, human review, authenticated Bullpen director consultation, manuscript acceptance or canon promotion.

Scope: engagement artifacts, frozen source passage, location card, and three modified existing templates. Full active novel and entire reference books were not read. Reviewed after.md SHA-256: `7da94905c4a475b1824b6bbad43759b790660c2ac543b527b009ce214cbf965d`.

## Findings and revision effects

1. **Initial failure — agency was not causality.** The first candidate said “Wilson waited on the slope until they had dragged the axle out together.” His descent did not cause clearance; the attendant instead obstructed a worker. This failed the existing Martin/Abercrombie dossier question of whether the POV drives a consequence. Reviewer requested a meaningful action or a failed criterion. Revised candidate puts Wilson's hands on the unstable end; a worker's “Toward me” / “Not up” changes his action; together they clear the path. The physical limitation now costs effort, and dialogue performs work. **Resolved within the excerpt.**
2. **Initial failure — retained details lacked local anchors.** Before covers source lines 31–69, but candidate uses axe, split strap/ribs and northern-road context from lines 19, 21 and 29. Full-file hash existed, but that was insufficiently precise for the comparison. `additional_source_anchors` now identifies those passages. **Resolved.**
3. **Initial failure — stale spatial handoff.** First storyboard retained the initial candidate's attendant-beside-path / Wilson-crosses sequence after prose changed. Reviewer required uphill standard custody, axe placement/retrieval and joint drag. Updated storyboard carries these actions. Exact ordering of retrieval versus first wagon movement was also flagged for alignment. See final verification below.
4. **Residual literary limitation — characterization.** Baseline contains sharper explicit relief at unceremonious work (“He liked them immediately”; kingdom contrast). Candidate replaces that with a choice and labor, which supports the same direction indirectly, but does not establish distinctive voice across other POVs. Character specificity is **PARTIAL**, not a solved defect.
5. **Residual scope limitation — dialogue and long arcs.** New worker dialogue changes immediate action, but this short exchange cannot demonstrate sustained dialogue, transmitted historical knowledge, later rediscovery or overlapping multi-year arcs. Those remain **NOT TESTED**. The new three-pass template asks the right questions but is not execution of those manuscript passes.
6. **Comparison limitation — ledger/jargon defects absent in baseline.** Neither selected source slice nor candidate contains production-policy jargon or a ledger/access plot. Their absence after revision is not improvement evidence. Repeated patterns across adjacent scenes and season compression remain **NOT TESTED**.
7. **Authority/access limits correctly retained.** Candidate is NONCANON_EXERCISE; invented blocking/dialogue is labeled; source historical authority is NONE; owner binding remains unverified. Missing approved visual bytes stays HUMAN_REVIEW_REQUIRED. Sources distinguish catalog/partial/public material and application inferences. No full-book reading, author contact, permanent training or human acceptance is claimed.

## Independent checks actually run

- Compared source bytes against `git show 8fcb77191955f413fe970154d47632770f923055:<source_path>`: exact match.
- Recomputed source hash and compared before.md with source lines 31–69: exact match.
- Checked resource IDs unique and all full_book_read values false.
- Ran `python -m unittest discover -s . -p 'test_verify.py' -v` from engagement directory: **12 tests passed** at first verifier review. Negative controls reject missing/changed assembly coverage, declared gaps, inflated book depth, catalog-as-method, unknown reference, missing alternatives, simulated acceptance and unverified-owner/coverage overclaims.

The validator trusts supplied receipt metadata; it cannot prove cognition, authentic human reading, historical identity or literary quality. A structurally complete declared assembly is not evidence that an unwritten saga exists. Initial tests used synthetic receipts; actual pilot receipt integration was requested separately and is reported below when rerun.

## Verdict

Useful bounded application with a documented failed first candidate and targeted correction. Three existing templates integrate source depth, three-to-four reading passes, passage-backed alternatives, handoff uncertainty and authority boundaries without adding an organization. Suitable for draft review: final actual-receipt checks and storyboard alignment are now confirmed. **No production/canon acceptance.** Full-book access, unresolved “Foundations,” approved visual bytes, historical owner binding, full-manuscript passes and long-arc effectiveness remain open.

## Final verification

Re-ran `python verify.py` and the 12-case unittest command against the final artifacts. Both succeeded. The verifier now loads `reading-receipt.json`, recomputes the before/first/final candidate hashes, checks its EXCERPT_ONLY scope, and evaluates both actual handoff packets. It returns PASS_EXCERPT_ONLY, three rejected negative-control errors, UNVERIFIED owner binding, HUMAN_REVIEW_REQUIRED visual production, NOT_PROVEN_BY_SCRIPT literary quality, and zero full-manuscript passes.

Read `EVALUATION.md` and the actual receipt. Both preserve first-candidate failure, recognize untreated defects and distinguish synthetic test cases from actual excerpt evidence. Read final storyboard shot 3: steps onto slope → retrieves axe → wagon moves, matching after.md. No unresolved implementation defect found in this bounded review. The residual literary/access/coverage limits above remain; none are converted to acceptance.
