# Schemin '26 — Cross-Atlas Audit & Hardening Receipt V2

**Date:** 2026-11-20  
**Target:** [PR #324](https://github.com/jakekaloper-hub/schemin-26/pull/324) (`feat/atlas-location-summit-20261120`)  
**Upstream sources:** [Playoff Island PR #322](https://github.com/jakekaloper-hub/schemin-26/pull/322), [Commonwealth Observer PR #314](https://github.com/jakekaloper-hub/schemin-26/pull/314)  
**Acceptance status:** **TECHNICAL / STRUCTURAL PASS, WORLD-CANON / PUBLICATION HOLD.** No claim of independent Umpire, actual external production team participation, or new scene/atlas publication.

## 1. Reopened source evidence and scope

This audit fetched the exact current GitHub files and source PR heads and tested a fresh isolated working copy on the authorized Mac. The focus was the earlier delivered 23 live LOC IDs + 48 legacy candidates + 40 additional candidates, and 44 source handles from PR #322 (the latter include `LOSERS_BEACH`, 23 topology nodes, 9 arena/heritage site IDs, 9 dormant ruin handles and 3 siting hypotheses). Distinct handles are not all distinct geographic properties or approved active sites.

PR #314's visitor source still models the original 23 active locations and does not automatically render the 40 new candidates. PR #322's island remains a Founder-directed **draft geographic proposal**, not automatically part of the active World Engine.

## 2. Findings and implemented repairs

| ID / severity | Verified defect or weakness | Actual remediation in PR #324 | Disposition |
|---|---|---|---|
| HIST-01 / HIGH | Twelve franchise-slot historical matrix contained many `UNKNOWN_NOT_NO` playoff participation values despite 2015–2025 qualification records in PR #322 | Reconciled all **132 slot-year records** with **67 qualifying slot-years / 65 nonqualifiers / 13 byes**, all **56** bracket fixture IDs and **112** reciprocal contestant records; recorded QF/SF/final exit states and corresponding Losers' Beach eligibility *as proposed fiction* | **REPAIRED, source-bound** |
| QA-02 / HIGH | Older viewer excluded new candidates by an editable source-provenance string, so missing/forged provenance could leak an unapproved ID into Phase 4 editorial views | Introduced exact **48-ID Phase 4 display allowlist** in `world/atlas/interactive/FROZEN_EDITORIAL_CANDIDATE_IDS_V1.json`; builder fails closed on duplicates or missing legacy candidates | **REPAIRED** |
| DEPTH-03 / MEDIUM | Legacy location dossiers largely described generic three-stage research checks, not source-specific environmental or civil constraints | Enriched **all 111** live/candidate dossiers with real seven-region terrain/climate/movement, known route restrictions, credible civilian work and supply questions, parent event memory context, technology/neutrality obligations and explicit historical nonattribution | **REPAIRED AS EDITORIAL DEPTH, not new world fact** |
| TEST-04 / HIGH | Existing validation mainly checked nonempty dictionaries and record counts; mirror-score drift, forged owner continuity, fictional venue promotion and false beach admission were weakly covered | Added `postseason_lineage_gates.py` and **16 adversarial unit tests**, plus **16 interactive Atlas viewer tests**; strengthened existing 111-dossier validator with region/route/memory/source-content checks and CI wiring | **REPAIRED** |
| ISSUE-05 / MEDIUM | Playoff Island PR #322 source embeds `checks.edge_count=41` although its full edge array and fixed source tests contain **45** links | Logged exact source mismatch on #322 and retained a hold; no risky parallel write into dependent generated island assets | **OPEN UPSTREAM** |
| ID-06 / BLOCKING | `CAND-CHAMP-LAST-FIELD` currently uses Central Basin; PR #322 also defines island `CAND-POST-LAST-FIELD`/`LAST_FIELD` | Explicit identity bridge and no-dual-location guard retained; no silent LOC or route promotion | **OPEN CANON/SITING GATE** |
| TECH-07 / BLOCKING | Island offshore terrain, monumental causeway engineering, modern broadcast technology exception, memorial chronology and human-owner lineage are not independently ratified | Preserve draft status, memorial protection, no fake owner mapping, no speculative 2026 champion, no private land deeds | **OPEN** |

## 3. Proof of executed tests

**Mac isolated checkout, fresh source pulls:**

- `python3 world/atlas/summits/2026-11-20/validate_location_summit.py` → `PASS_STRUCTURAL_ONLY` / exit **0**.
- `python3 world/atlas/summits/2026-11-20/postseason_lineage_gates.py` → `PASS_SOURCE_BOUND_NOT_CANON` / exit **0**. Asserts 132 slot-years, 67 qualified, 65 excluded, 13 byes, 56 paired fixtures, 112 participant views, zero verified fictional venue attributions, no ESPN refetch performed this session.
- `python3 -m unittest discover -s world/atlas/summits/2026-11-20 -p 'test_postseason_lineage_gates.py'` → **16/16 PASS**, including deliberate corruption of source-qualifier counts, bracket reciprocity, historical owner, final winner, fake fictional venue, byes and beach entry.
- `python3 -m unittest discover -s world/atlas/interactive -p 'test_interactive_atlas.py'` → **16/16 PASS**, including bad/provenance-forged candidate and missing/duplicate frozen catalog mutation tests.
- Previous `test_atlas_summit.py` cross-handle checks remain wired into GitHub Actions.

**GitHub at exact commit `e9c1f5ca144c3bd66cce773f3a36e9c973ab4516`:** `Atlas location summit CI`, `World Engine QA`, `Cross-Domain Authority CI`, `Commonwealth Archivist CI`, `Bullpen Runtime CI`, `Schemin World Engine CI`, and `Repository Merge Gate` each returned **SUCCESS**.

These are real deterministic tests and live workflow results, not a substitute for independent visual, narrative, source-provider or human-canon judgment.

## 4. Historical interpretation boundary

The new matrix transfers existing PR #322 source-labeled Flaim/ESPN brackets and records **rather than independently refetching** each ESPN result in this audit. Team slots are not automatically real-person identities in 2015–2025. Under Founder decisions, a retrospective scene at Crown Stair or Last Field is an original *fictional* placement of a certified competitive result, never evidence that ESPN recorded an island venue. Real-world athlete injuries, owner biographies, years of building destruction, civic wars, actual historic beach admissions and Michael Farrell memorial chronology must not be fabricated.

All 2015–2025 podium facts, 2026 unresolved results, 2026 current character canon, and seven source World Memory event anchors retain their respective evidence classes.

## 4A. Continuation addendum — source discrepancy resolved and pinned

The ISSUE-05 historical finding above was correct at the time of the original V2 audit, but it has since been repaired on Playoff Island PR #322: the live island topology now declares **45 edges, matching its 45 edge records and 23 nodes** (Git blob `2edc3efcb8e50dba35f851a0a861c785680bffad`). PR #324 now contains an exact read-only source snapshot and validates each source node, per-node edge list, road mode, and protected admission. The new 15-case adversarial island test suite passed locally. ISSUE-05 may therefore be closed as a **data-source metadata defect**; the separate geographic engineering, Last Field identity and independent approval gates remain blocked. No proposed route was added to the 18 active routes.

## 5. Release gate / next domain tasks

**PASS for structural accuracy and reversible editorial design**. Every one of the **155** source handles has source-bound three-layer coverage; the 36 nonduplicative proposed sublocations can undergo supervised canon review, while four speculative duplicate island concepts remain explicitly held.

**HOLD for active-world or visitor publication.** Before any promotion: independent source/venue QA and Umpire signoff; Island/mainland geography and hydrology; Last Field versioned supersession; safe causeway and energy communications plan; historical year-of-construction/owner evidence if asserted; approved character/POV/visual packets; exact current 2026 week-result lock; and audience-site render/readback verification. No existing live LOC was newly activated here, and no old forbidden candidate was promoted.

**Disclosure:** Previous Bullpen route invocation selected actual domain owners and counterweights; that is routing, not independent execution by 18 distinct Director models or a human Inklings council. This audit has not inspected all claimed multi-million-line Novel OS prose or received a third-party Tim Veil review. Those remain separately verifiable release gates.
