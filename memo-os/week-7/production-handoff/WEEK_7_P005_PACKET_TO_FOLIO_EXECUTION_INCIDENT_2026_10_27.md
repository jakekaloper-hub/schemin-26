# Week 7 P005 — packet-to-folio execution incident and mandatory repair gate

**State:** EXECUTION BLOCKED / REPAIR REQUIRED / NOT A NEW PREPRODUCTION ROUND.
**Authority:** Week 7 executive production handoff V2, existing PR #256, Memo OS V5.5, approved Week 7 P005 packet, exact-copy split, Week 6 published visual standard.
**Founder observation:** A standalone illustration and improvised text overlay were delivered instead of a finished page-native Week 7 folio comparable to Weeks 2–6. Both are rejected as publication candidates.

## Reproduced failure
1. The renderer was invoked with a prose scene description rather than demonstrably attached, hash-verified owner-specific image references.
2. The illustration alone was presented as the page deliverable; afterward an ad hoc composition was attempted without verified Week 6 shell/design-system implementation.
3. P005 V2 explicitly declares creative DNA JSON UNRESOLVED, accepted portrait source UNRESOLVED, text-safe layout pending proof, and technical pre-render HOLD. These were bypassed.
4. Exact manuscript integration, native 1024x1536 composed raster, 390px copyfit, character QA, physical QA and independent Umpire were not demonstrated.
5. Source PNG retrieval through GitHub base64 succeeded for CHAR-PHILLIP-PITTS and CHAR-ZACH-WILSON, but decoded SHA256 and provider-bound subject slots were not verified. Git blob SHA is not image SHA256.

## Required Bullpen execution (existing architecture only)
- Librarian: reconcile P005 exact-copy authority, Oct18 lineup crop hashes, costume precedence and approved Week 6 published visual shell/reference pages. Verify decoded source bytes, not metadata alone.
- Architect/Renderer: trace existing packet schema to actual image request and page composer. Identify exact missing/ignored fields and implement fail-closed validation. Do not create a parallel OS.
- Editorial/Design: locate and reuse existing Weeks 2–6 page-native layout/shell assets, typography rules and composition code; compare real Week 6 page(s) against P005 before any replacement.
- Character/Atlas/Physical: validate two-subject binding, exactly three TDS heads, Duckhook floral bucket hat, waterfall left, landward camera, bag set down, single cup and continuous prop geography.
- Groundskeeper: generate one complete P005 1024x1536 page containing actual approved manuscript copy and controlled typography; inspect real raster and 390px downscale. Never count an isolated illustration as a finished folio.
- Independent Umpire: require actual source/output hashes, attachment proof, per-page visual QA, and external acceptance before certification. No invented receipts.

## Acceptance test
Given approved P005 packet, the existing production entrypoint must output a **single complete page-native PNG** with art and exact source narration, verified design-shell lineage to Week 6, per-subject reference provenance, source/output SHA256, real 390px readability evidence, and explicit disposition. Missing prerequisites MUST fail closed before render. Once repaired, run a negative test for illustration-only and ad hoc text-overlay output. Preserve rejected attempts only as experimental evidence.

## Operational sequencing
Continue PR #256 and branch mission/week7-renderer-gates-20261027. Do not change manuscripts, approved venues or character canon. Do not restart general brainstorming. No merge or publication until all real gates pass.
