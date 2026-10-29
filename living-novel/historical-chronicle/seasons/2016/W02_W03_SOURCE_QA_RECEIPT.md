# 2016 Weeks 2–3 — verified fixture concordance and manuscript acceptance HOLD

**Production date:** 2026-10-29. **PR:** #243 (existing historical saga draft). **State:** NONCANON / NOT MERGED / NO AUTHOR OR UMPIRE ACCEPTANCE.

## Real literary production

- **Week 2 — [The Names That Would Not Buy Bread](weeks/W02.md)**: 4,343 whitespace-separated words including headings, source notes and editorial firewall. Six dramatized fixture encounters; causal arc around shelter admission, the unsafe beam, and an offered victory-derived vote refused.
- **Week 3 — [The Joint That Held](weeks/W03.md)**: 4,026 whitespace-separated words including headings and source notes. Six successive fixture encounters; carries forward the shelter and beam; resolves only the provisional repair while creating a binding **fictional** obligation for Jake and outstanding labor/payment records.
- **Total new authored draft material:** 8,369 whitespace words, including headings, receipts and metadata. This is authored prose, NOT two automatically designated novel chapters; the historical Chronicle week-format satisfies a different completeness contract from the causal epic.
- **Existing baseline preserved:** 2016 Prologue, Week 1 and draft postseason/epilogue not overwritten. Newly drafted 2016 ordinary-week fixture coverage: 12 results across Weeks 2–3; **18 of 78** regular-season results have a first-draft narrative when Week 1 is included (six per week). This is a coverage count, not a maturity or author acceptance claim.

## Competitive provenance

**Source:** `living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json`  
**Git blob:** `6dbec1fe2537139f3a97c6a78250e2bae082a518`  
**Record labels:** `Flaim ESPN 1417621`; year 2016; standard scoring weeks 2–3. Retained archive source, **not a newly authenticated raw upstream ESPN snapshot**. Source explicitly flags unverified historical human identities and possible duplication of postseason multiweek scoring periods.

| Week | Fixture | Home | Away | Verified winner | Margin |
|---:|:---:|---|---|---|---:|
| 2 | A | Kunt Liquors 87.76 | Here, Ok I took L's 120.28 | Here, Ok I took L's | 32.52 |
| 2 | B | I'M HERE SO I WON'T GET FINED 82.56 | Hook, Line, and Zeeker 93.82 | Hook, Line, and Zeeker | 11.26 |
| 2 | C | Bavid Dabbs 85.38 | Scruffy Looking Nerf Herders 102.42 | Scruffy Looking Nerf Herders | 17.04 |
| 2 | D | The Real Austin's Hyenas 108.60 | All ACL Squad 147.00 | All ACL Squad | 38.40 |
| 2 | E | Team Hollingshead 139.76 | Pittsy's Rhino's 124.72 | Team Hollingshead | 15.04 |
| 2 | F | Austin's Hyena's 96.08 | The Gunslingers 133.62 | The Gunslingers | 37.54 |
| 3 | A | I'M HERE SO I WON'T GET FINED 119.88 | Kunt Liquors 113.72 | I'M HERE SO I WON'T GET FINED | 6.16 |
| 3 | B | Here, Ok I took L's 96.76 | Bavid Dabbs 129.24 | Bavid Dabbs | 32.48 |
| 3 | C | Hook, Line, and Zeeker 106.80 | Scruffy Looking Nerf Herders 163.14 | Scruffy Looking Nerf Herders | 56.34 |
| 3 | D | Team Hollingshead 88.68 | The Real Austin's Hyenas 112.10 | The Real Austin's Hyenas | 23.42 |
| 3 | E | All ACL Squad 103.74 | Austin's Hyena's 97.86 | All ACL Squad | 5.88 |
| 3 | F | Pittsy's Rhino's 121.08 | The Gunslingers 117.90 | Pittsy's Rhino's | 3.18 |

**Identity prohibitions:** 2016 Scruffy slot 1 as historical Jake is **NOT PROVIDER-AUTHENTICATED**; its narrative Jake lane is a fictional Author Room proposal, not a real-owner biography. The Real Austin's Hyenas slot 12 and Austin's Hyena's slot 8 must remain distinct scoring IDs; a champion-name change does not prove historical human continuity. El Niño is absent from these archived fixtures and is not personified.

## Technical tests

- `living-novel/historical-chronicle/qa/test_2016_second_week.py` — 14 new deterministic cases. Checks all six source results, uniqueness, narrative length, exclusive proposed POV, uncertainty/Atlas/firewall and handoff.
- `living-novel/historical-chronicle/qa/test_2016_third_week.py` — 14 new deterministic cases. Checks pinned archive blob, all six results, substantial fiction, exact previous-week blob, all four protected 2026 hard manuscript blobs, temporal knowledge, candidate owner firewall and review HOLD.
- Both named steps wired into the existing `.github/workflows/novel-os-ci.yml`. Test commands:
  - `python -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_2016_second_week.py' -v`
  - `python -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_2016_third_week.py' -v`
- Week 2 test passed in GitHub Novel OS CI at SHA `8912a1f86d91582331a3caa93bc2ce7c99453300`, run `40933018949`. A previous failure at `d79ab4a6` arose from a markdown-emphasis mismatch in a negative-guard assertion and was repaired before the passing run. This assertion repair did **not** modify narrative prose. Week 3 combined exact-head CI requires fresh observation; do not infer it from the Week 2 result.
- Independent review and editorial merit **are not established by these tests**.

## Literary self-critique — NOT independent review

**Strengths requiring confirmation:** The story's consequence is not victory itself but the changing conditions of shelter. The inspector and seller have differentiated practical obligations, and the proposed Jake's signature in Week 3 makes the earlier moral refusal expensive. No claim is made about the actual league owners' mental states.

**Material defects:** A six-tablet delivery mechanism repeats across scenes and may become a thin allegory for fantasy results. The proposed Jake POV is unauthenticated for 2016; the hall has no approved Atlas anchor; the supporting people are undernamed, and their agency can be overshadowed by the protagonist's conclusions. The roof metaphor risks becoming a repetitive declaration that outcomes do not equal civic legitimacy; any editorial adaptation into an epic causal chapter must compress the receipts and deepen distinct character desires, material constraints and local culture. The 2016 season cannot inherit 2026 wardrobe, companions, ownership or political canon by assumption.

**Gate status:** historical human-owner binding HOLD; historical Atlas HOLD; independent Author Council review NOT RECEIVED; independent Umpire review NOT RECEIVED; Founder-only canon promotion and publication CLOSED; no merge authorized.

**Next eligible prose:** 2016 Week 4's six archived outcomes and the proposed unpaid obligation, or independent causality-first rewrite of this two-week sequence once owner/Atlas inputs are available. Never infer unseen season transactions, personal motives, venues, or later results.
