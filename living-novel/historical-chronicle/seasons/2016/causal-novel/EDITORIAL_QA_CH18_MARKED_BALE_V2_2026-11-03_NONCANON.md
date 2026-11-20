# Chapter XVIII V2 — producer developmental audit, not independent acceptance

2026-11-03 • NONCANON • PR #243 draft only

**Production:** Revised `THE_RIVER_KEPT_NO_PLACE_CHAPTER_18_NONCANON.md` without altering original, introducing approximately 2174 new/changed prose words in a downstream freighting scene and a limited lower-landing receipt confrontation. New Chapter XVIII contains 7514 source words including metadata; 15-part assembled edition contains 98459 chapter-source words, with 14/14 prior component bodies preserved unchanged. Source: original Chapter XVII V2 marked-cloth handoff, blob `0f6644c8ca29787324ee8d4641428b41f8dadae3`. All trade routes, people, cargo rules, damage, and economics are proposed fiction, never reported ESPN facts.

**Causal repair:** The unreceived cloth from Chapter XVI remains aboard and marked at the end of Chapter XVII. Chapter XVIII previously ignored it at the lower landing. V2 adds a minor shifting-return-frame hazard, prevents damage to the *external* evidence mark, and explicitly refuses a false discharge. Aren did not accept cloth; the lower-landing clerk now records only shield crates and packing. No consignee, internal condition verdict, liability, settlement or ownership identification is supplied. Deren retains custody. The earning of fictional wages and Jake's inland walk toward the shelter remain intact; Mara's earlier note remains unconfirmed, Chapter XIX begins after this road departure.

**Editorial challenges:** This is another procedural cargo sequence in a densely procedural book. Does the new movement change Jake's behavior, or merely reiterate his preference for limited claims? Does Pell's near fall and scratched hand plausibly earn a character consequence without becoming an artificial hazard? Are a loose crate frame and shallow-water lateral motion mechanically coherent? Is a clerk empowered to make this limited note? Does the newly extended Chapter XVIII overstay its ending? Historical owner/slot binding remains unverified. Period Atlas, material culture, contract practice and Author Council review needed.

**Verification:** Repository regression code and a named Novel OS CI step are included, but *PASS is not claimed until observed on exact commit*. Byte-source manifest compares all 15 chapter sources with Git blob hashes; previous 14 source segments unchanged. No protected 2026 hard manuscript files are edited.

**Independent reviewers:** NOT OBSERVED (Authors Council, Historical Librarian, Character Canon, Atlas and Umpire). Founder canon/publication authorization NOT GRANTED. No merge, publication or automatic promotion. Next: exact-head CI readback, independent scrutiny of Chapters XVI–XIX continuity, then source-safe Chapter XIX revision only if justified.


## Observed CI failure and repair

At production commit `7ddfb70c695ece1bcac7e0c50aace436f4786ce8`, [Novel OS CI #41605093099](https://github.com/jakekaloper-hub/schemin-26/actions/runs/41605093099) **FAILED** in the new 12-test step: 11 tests passed; one protected-Prologue Git blob assertion failed because the new test had an incorrectly transcribed hash (`5ef240b31a67cf1a6c6d8ee723bf39fc7dfaf0` instead of the independently verified `5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0`). This was a **test-fixture typo**, not a changed manuscript. All four protected 2026 files were fetched on both main and PR branch and their blobs matched. The expected hash was corrected without altering any prose. Re-run status must be independently checked on the corrective commit; no premature PASS claim.

At the failed production commit Cross-Domain Authority, Bullpen Runtime CI and Repository Merge Gate succeeded; independent editorial review remains outstanding.
