# 2016 Weeks 12–13 — archived-results concordance and Chronicle production QA

**Status 2026-10-29:** Authenticated GitHub draft PR #243, NONCANON / independent Author Council, historical Character/Atlas, Umpire and Founder-only release HOLD. This receipt documents sourced writing and local construction checks. It does **not** impersonate an autonomous Bullpen agent, an independent review, or an approved manuscript.

## New literary material

| Component | Work | Whitespace-delimited words including notes | Pinned Git blob |
|---|---|---:|---|
| [Week 12](weeks/W12.md) | *The Names We Would Not Move* | **5,069** | `311957166b974f30fff5d615bf8a1072bf936e5e` |
| [Week 13](weeks/W13.md) | *The Table That Kept Its Place* | **3,874** | `eeb336261d44bc92fe688a84e094462f89916581` |
| [Regular-season reader](READING_COPY_REGULAR_SEASON_W01_W13_NONCANON.md) | Original Prologue + 13 source-exact weekly components | **62,518** including assembly | Verbatim assembly of 14 original components |

**New authored prose:** 8,943 whitespace-delimited words, including headings, evidence boundaries and author notes, in **twelve** individually dramatized archived encounters. The 2016 regular-season Chronicle now has draft narrative coverage for **78/78** archived fixtures (13 × 6). The 2016 postseason and epilogue already have **earlier short provisional drafts** but need substantial source-aware fiction and independent review before any claim of a completed causal novel.

## Pin and limits

Authoritative retained evidence file: `living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json`, exact Git blob `6dbec1fe2537139f3a97c6a78250e2bae082a518`. `year=2016`, `source=Flaim ESPN 1417621`, weeks 12 and 13 each contain six rows with scoring periods 12 and 13, respectively.

The source itself warns **historical identity unverified** and **multiweek scoring may duplicate matchup periods**. These rows are archive reconstructions, **not new authenticated ESPN calls**. Scoring IDs are not proof of historical human owner, fictional political identity or geographic homelands; home/away are competition positions. ID 12 `The Real Austin's Hyenas` and ID 8 `Austin's Hyena's` are distinct.

## Row-by-row provenance

| Week / scene | Scoring home (ID) | Home | Scoring away (ID) | Away | Archived winner | Margin |
|---|---|---:|---|---:|---|---:|
| 12 A | The Real Austin's Hyenas (12) | 96.56 | Kunt Liquors (3) | 159.24 | Kunt Liquors | 62.68 |
| 12 B | Pittsy's Rhino's (6) | 86.74 | Hook, Line, and Zeeker (2) | 76.30 | Pittsy's Rhino's | 10.44 |
| 12 C | All ACL Squad (9) | 101.58 | Here, Ok I took L's (5) | 114.94 | Here, Ok I took L's | 13.36 |
| 12 D | Team Hollingshead (10) | 131.64 | I'M HERE SO I WON'T GET FINED (11) | 108.06 | Team Hollingshead | 23.58 |
| 12 E | Austin's Hyena's (8) | 167.54 | Bavid Dabbs (4) | 93.10 | Austin's Hyena's | 74.44 |
| 12 F | The Gunslingers (7) | 86.72 | Scruffy Looking Nerf Herders (1) | 112.20 | Scruffy Looking Nerf Herders | 25.48 |
| 13 A | Hook, Line, and Zeeker (2) | 120.06 | The Real Austin's Hyenas (12) | 129.18 | The Real Austin's Hyenas | 9.12 |
| 13 B | Here, Ok I took L's (5) | 73.24 | Pittsy's Rhino's (6) | 95.88 | Pittsy's Rhino's | 22.64 |
| 13 C | I'M HERE SO I WON'T GET FINED (11) | 132.60 | All ACL Squad (9) | 86.70 | I'M HERE SO I WON'T GET FINED | 45.90 |
| 13 D | Bavid Dabbs (4) | 75.84 | Team Hollingshead (10) | 132.26 | Team Hollingshead | 56.42 |
| 13 E | Scruffy Looking Nerf Herders (1) | 81.44 | Austin's Hyena's (8) | 103.86 | Austin's Hyena's | 22.42 |
| 13 F | Kunt Liquors (3) | 100.48 | The Gunslingers (7) | 102.36 | The Gunslingers | 1.88 |

## Continuity and editorial record

Week 12 preserves the unsafe eastern-room/wider exterior-wall cordon, returns the separate borrowed market awning, continues the missing-claimant uncertainty and introduces an explicit external-custody/refusal-of-retrieval record. The young worker remains independently employed; his earlier timber claim and the shelter's accepted-material invoice are not settled. The wheel is unturned and no retrieval frame approved. Week 13 brings a **fiction-only** limited visual wall observation, not safety certification. The resident's right to decline disclosure, the girl's path-only diagram and the conditional daylight use of the table are distinct from approved historical Atlas or property canon.

**POV:** Sole proposed fictional `CHAR-JAKE-KALOPER` `PRINCIPAL_CHARACTER` viewpoint, subject to the **exclusive twelve-owner** law. Historical ID 1 ↔ Jake remains **NOT PROVIDER-AUTHENTICATED**. No Edrin/Edin/Oren narratorial viewpoint, no humanized El Niño, no claim to a real owner's private thoughts.

**Reader integrity:** Existing Prologue–W11 reading copy preserved; W12 assembly appended the exact W12 Git-blob body; W13 final reader appended the exact W13 Git-blob body. New deterministic tests assert **14** ordered, pinned, verbatim source components. 2026 hard-canon Prologue and Chapters I–III match their current `main` Git blobs in authenticated comparisons.

**Automated tests added:** `qa/test_2016_twelfth_week.py` (12 methods), `qa/test_2016_partial_reader_w12.py` (6), `qa/test_2016_thirteenth_week.py` (12), `qa/test_2016_regular_season_reader.py` (6). All four are wired to named Novel OS CI steps. At an initial Week 13 run, two brittle wording assertions failed; they were corrected to match *unchanged* fiction. **Final patched-head CI results must be independently observed before claiming full technical success.**

## Challenge review / hard gates

The repeated evidence notices risk a ledger-driven story rather than a cohesive epic novel; the woman with chest, the registrar, young worker, girl and displaced residents need greater independent drives across a causal novel. The 2016 Prologue already references later outcomes and needs an authorial spoiler/foreshadowing pass. The separate short postseason and epilogue drafts are not a substitute for substantial historical fiction; do not automatically convert Week 1–13 into novel chapters. Historical house engineering, temporary land use, shelter recordkeeping and inspection capacities must be checked against period-specific Character and Atlas authority, not silently canonized. A routine automated test run cannot constitute independent Umpire approval.

**HOLD:** provider-authenticated historical owner mapping; period Character Canon; historical Atlas; independent literary acceptance; independent Umpire; Founder-only canon promotion; merge; publication. No approval, merger or deployment is inferred by this receipt.


## Observed CI on final tested code head

At exact patched code commit `dfba365309bfee85678ba5a611be2cb428aeec10`, GitHub returned **COMPLETED / SUCCESS** for all four workflows:

- [Novel OS CI #40974764881](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40974764881) — the named Week 12 manuscript, W12 source-exact reader, Week 13 manuscript, and fourteen-component regular-season reader steps each **SUCCESS**.
- [Cross-Domain Authority CI #40974764999](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40974764999) — SUCCESS.
- [Bullpen Runtime CI #40974765179](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40974765179) — SUCCESS.
- [Repository Merge Gate #40974765064](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40974765064) — SUCCESS.

The first Week 13 workflow on prior commit `a0e448c652c5edff1f3daec1f33362e6391c8daf` **FAILED** two literal-text assertions: it expected old Week 12 headings and the words `found key`. Both tests were repaired by `dfba3653` to check actual Week 13 material and `leaf-shaped key`; the manuscript was **not modified** to satisfy them. The successfully tested code SHA precedes this receipt-only edit. A receipt-inclusive commit requires its own CI readback; do not assume a new final head is green.

No test pass implies historical owner authentication, independent literary approval, Atlas validation, Umpire signoff, Founder canon promotion or a merge.
