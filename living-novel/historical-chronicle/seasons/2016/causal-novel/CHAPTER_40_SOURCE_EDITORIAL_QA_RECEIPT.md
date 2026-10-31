# Chapter XL — source and author-side editorial QA (NONCANON / independent HOLD)

**Candidate:** *The House Made from a Road*; 2016 Commonwealth historical causal novel; sole proposed fictional Jake limited POV (CHAR-JAKE-KALOPER).
**Existing production branch/PR:** `novel/historical-epic-2015-2026` / #243; continuation of Chapter XXXIX, not restart.
**Main authority readback:** `ec941811d6334d70015ec97b2ac68a2d8a26eec6` (schemin-26) and `86889a59efb0e7dcdc37eef639981944dc77ed67` (bullpen).
**Authoritative sources:** Whole-Book Source Authority Matrix V1; Novel OS Session Context / Causal Chapter Architecture; Twelve-Character POV Register; 2016 Flaim/ESPN transcription (read only, no new event inserted); PR #243 and Chapter XXXIX checkpoint.
**Original chapter writing commit:** `e3c71a016bf1039c0ec2cd58ee6b2e0df2478eaa`; subsequent pre-commit editorial cleanup replaces an awkward self-correction about cart wheels, without changing the story's outcome.
**Chapter Git blob:** `d5a4e6778c705b5f3e655071e04a67892ef22b95`; **6,534 whitespace-separated words** including frontmatter and editorial handoff, six prose movements.
**Previous reader blob (39 chapters):** `15165b0e6e98f1a0d274a02fa2d613ad1ea048ac`; **assembled reader blob (40 chapters):** `ecc93dfe2100ed68f9aa49e59c0427fc2dbf6295`; **229,709 words** including source notes and the assembly manifest.

## Observed local verification

- **PASS:** 17/17 chapter-specific regression tests after two genuine manifest-wordcount failures were diagnosed and repaired. The failures were caused by a stale 6,535-word manifest entry after a one-word editorial change; the reader manifest was repaired to 6,534 and its hash pinned in the regression.
- **PASS:** 932/932 local Python tests with `python3 -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_*.py' -q`. No broader cross-repo suite is claimed here.
- **PASS:** forty chapter manifest rows, 40 pairs of source sentinels, each embedded chapter text source-exact, all 40 embedded sources matching pinned Git blob hashes, previous 39-chapter reader unchanged, protected 2026 Prologue/Chapters I–III matching pinned blobs, original 2016 score archive unchanged.
- **GitHub CI:** PENDING exact-commit readback at time of this author-side receipt. A local pass does not constitute CI or independent reviewer acceptance.

## Literary consequence

The former dye-workshop dry room becomes bounded shelter during Ina's wet-work suspension. Hessa and five traveling companions negotiate the conditions as a group, removing one side of their cart for fitted sleeping platforms but retaining the axle and wheels; thus a practical ability to leave is made more costly without a claim of permanent settlement. Ina admits that the decision hurts her apprentice's prospects; the apprentice independently negotiates limited drywork labor. Fara refuses unspoken food debt. A passing carter mistakenly assumes the room has become public lodging, exposing the wider political consequence of a private agreement.

**Independent editorial objections:** (1) Forty chapters in this strand still use Jake as the only limited focalizer: the exclusive twelve-owner rule is formally preserved, but literary polyphony remains unfulfilled. (2) The proposed room/capacity, roof, timber, safety of infant sleeping, storage and water arrangements must not be treated as inspected or Atlas-approved. (3) The fictive twenty-one-night private arrangement may anachronistically suggest civic rules or tenancy rights never approved in period canon. (4) The rhetorical dialogue is sometimes too thesis-forward, especially on work, obligation and entitlement. (5) The late carter question risks reprising earlier false-rumor beats. (6) Labor and displacement ought to produce continuing contradictions in later chapters rather than moral closure. (7) None of Hessa, Ina, Fara, Eren, the maker or apprentice has authorized owner POV; their independent decisions are shown only as externally observable conduct.

## Evidence and approval firewall

The connection between Jake and any 2016 scoring slot is **NOT AUTHENTICATED**. No invented settlement, health/safety condition, water system, financial contract, route, institutional rule or historical-owner motive is canon. Eight travelers' safety, Hessa's sister, distant ash/fire, Mael/Pell freight loss, local blue-water fate and Jake/Esi matters remain unresolved. The 2016 competitive facts remain only in preserved evidence, not rewritten as prose history.

**Independent Authors Council, Historical Librarian, period Character Canon/Atlas and Umpire acceptance: NOT RECEIVED.** Founder-only canon/publishing authority: NOT GRANTED. **DRAFT ONLY. NO MERGE. NO CANON PROMOTION. NO PUBLICATION.**

**Next substantive candidate:** A Chapter XLI consequence driven by the rumor of general lodging and the real limits of the workshop, with direct choices that cannot be solved by another repaired object. Do not overstate historical owner coverage; continue the separate full-season Chronicle obligations.
