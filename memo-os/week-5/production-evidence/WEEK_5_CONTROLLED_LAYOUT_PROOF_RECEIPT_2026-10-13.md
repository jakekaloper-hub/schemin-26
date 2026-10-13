# Week 5 — Controlled physical-layout proof receipt (2026-10-13)

**Authority:** Commissioner `CONTROLLED_PRODUCTION_AUTHORIZED`, Issue #146 / PR #152, master packet and 32-ID `PUBLICATION_PAGE_MANIFEST.json`. This is production evidence **within the existing Memo OS**, not a new system. **Publication = HOLD.** **This document does not approve pagination, artwork or copy.**

## Real outputs generated in the production session

1. `SCHEMIN_26_WEEK5_21_PAGE_LAYOUT_PROOF_NONFINAL.pdf` — 21-page complete source-to-physical **test layout**, with 32 source IDs mapped, all six dedicated overtures, 18 setup/escalation/payoff beats, opening/scoreboard/editorial departments, and an explicitly noncanonical Week 6 GOTW candidate insertion. The 24 matchup narrative bodies were drawn from the 2026-10-13 existing P004–P027 manuscript candidates. No new story premises.
   - SHA-256: `f63881e6ecf396d422c97418b74ea793270267c9a010aed3bee08272eb04c2e7`
   - 135,398 bytes; 21/21 extractable nonempty PDF pages
   - Rendered 21 visual previews at 390px, assembled and visually inspected as a contact sheet
2. `SCHEMIN_26_WEEK5_8_PAGE_BASELINE_COMPARISON_NONFINAL.pdf` — eight sample source pages from the uncompressed 32-source-page direction, containing **Dark Wizard Chess (P004–P007)** and **After the Storm (P020–P023)** as the mandatory atmospheric/action comparison.
   - SHA-256: `6a53bdb01c3ad86979b565feade5d45883a953b08170f661ae4a39c4fecda688`
   - 102,384 bytes; 8/8 extractable nonempty PDF pages
   - Rendered each comparison page at 390px and visually inspected

**Storage caveat:** The actual PDF binaries and preview PNGs currently exist as session artifacts provided to the Commissioner; they are **not uploaded to GitHub by this receipt**. Hashes identify those artifacts for subsequent durable ingestion. Do not claim the GitHub repository contains the binaries or that a reproducible CI exporter has been proven.

## Live data reconciliation

- Authenticated connected FLAIM: ESPN league `1417621`, 2026 Week 5. Six matchup `winner` fields remain `UNDECIDED`, `totalPoints=0` as of this production session. `pointsByScoringPeriod[5]` holds all six updated **provisional** totals.
- The 12 standings rows returned represent completed Week 4 records, **not verified Week 5 records**. The compact proof labels the resulting standings presentation as a placeholder rather than falsely promoting it to Power Rankings.
- Week 5 activity returned 22 transactions. Selected completed acquisitions are presented in the proof. No unverified week-6 waiver news.
- Week 5 Pitty's Book stake/line/outcome receipts unavailable, so numerical settlement withheld. No unverified playoff probabilities.
- Mike Ditka's death on 2026-10-09 was independently confirmed through Chicago Bears and Pro Football Hall of Fame primary notices:
  - https://www.chicagobears.com/news/bears-legend-mike-ditka-passes-away-at-86
  - https://www.profootballhof.com/news/pro-football-hall-of-famer-mike-ditka-86-dies
  The Commissioner-locked LLC memorial-first concept was preserved; no owner portrait or fabricated Ditka quote.

## Layout and mobile findings

- **Structural PASS:** 21 physical pages, six overtures, six three-beat pages, all 32 source IDs traced, PDF text extractable, four embedded DejaVu typefaces, no empty PDF pages and no detected manuscript box overflow after controlled font fitting.
- **Mobile QUALITY HOLD:** On a raw 390px page render, several compact three-beat scenes shrink to `12.65–13.35pt` at 612pt source width (approximately `8.1–8.5px` output). This is materially less readable than the uncompressed source-page comparison, `17.2pt` (approximately `11.0px` at 390px). Reject the 21-page mapping for final approval until typography is improved without cutting text or hiding art.
- **Art HONESTY PASS / character release HOLD:** Only abstract noncanonical visual placeholders were drawn. Canon owner-character renders are absent. `canon/characters/renderer_capabilities_v1.json` continues to record `NO_PRODUCTION_ROUTE_PROVEN`. No owner-byte mount hash or deterministic subject-binding receipt has been produced.
- **Content HOLD:** NFL player claims remain inherited editorial source candidates; no new independent per-stat NFL final certification performed here. Several matchup payoffs imply the provisional leader's victory and are unmistakably labeled **conditional** in the proof. They are not certified results.
- **Page 18 governance HOLD:** The Week 6 GOTW reader insert is test-only; no new canonical P033 and no approved GOTW selection.
- **Review HOLD:** No authenticated Bullpen runtime/Director conference or independent Umpire signoff occurred. Layout was manually previewed within the production session. No claim of organizational independence.

## Stop/go — precise current state

| Ledger | State |
| --- | --- |
| IMPLEMENTED | Two real PDF proofs and 390px rendered previews, all existing P004–P027 prose placed, current FLAIM snapshot consulted |
| TESTED | Opened PDFs, counted pages, extractable text, hash/bytes and phone-size visual previews |
| AUDITED | Local visual and structural self-review; independently authenticated Umpire **not obtained** |
| PROMOTED | **This proof receipt to PR #152 only**, if GitHub write succeeds; **no page/canon/publication promotion** |
| BLOCKED | Official ESPN Fact Lock, exact character renderer mount/identity, 21-page mobile acceptance, full NFL source verification, final departments and Pitty receipts, final pagination approval, independent Umpire |
| REMAINING_EXTERNAL_INPUT | Actual renderer-mount capability, official fantasy settlement or Commissioner-authorized final reconciliation, official Pitty receipts, Commissioner final pagination approval after comparing proof artifacts, independent release reviewer |
| NEXT AUTOMATIC ACTION | Preserve original 32-ID manifest; iterate compact typography or choose uncompressed layout as the production-safe fallback, reconcile winner-sensitive prose, verify roster line scores and close source receipts, then perform art binding tests and complete issue assembly |

**No false green.** Proofs are real; release acceptance is not.

## Post-persistence CI / deployment inspection

At commit `c948e04d5e012b92c75bababa7e2e2c00a391334`, seven GitHub Actions jobs completed with success (Week 4 Publication Readiness, Character Lock, Weekly Memo Authority, Repository Merge Gate, Bullpen Runtime, Character Generation Boundary and Cross-Domain Authority). These checks do **not** independently certify the experimental PDF, art mounts, fantasy results or Week 5 release.

The separate Netlify `scheminnovel` PR preview check **failed**. Authenticated Netlify deploy `6acdb37572ee0e568f406096` reports: `Failed during stage 'building site': Deploy directory 'novel/book' does not exist`. It is a distinct novel-site deploy issue, **not evidence of a Week 5 PDF export failure**, but it blocks any claim that every PR status is green. Do not modify Netlify publishing configuration as a side effect of this Memo proof without inspecting the canonical Novel deployment contract.
