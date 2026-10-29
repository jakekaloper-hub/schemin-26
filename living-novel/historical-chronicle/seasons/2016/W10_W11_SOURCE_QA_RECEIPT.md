# 2016 Weeks Ten–Eleven — literary production, source concordance and QA receipt

**2026-10-29 | PR #243 OPEN / DRAFT | NONCANON / independent editorial HOLD.** This is a repository-authenticated engineering/authoring work receipt, **not** a claim of an authenticated Bullpen Director meeting, independent Author Council acceptance, historical owner verification, Atlas approval, canon promotion or publication.

## Actual authored prose and assembled reading copy

| Component | Title | Whitespace words incl. notes | Git blob |
|---|---|---:|---|
| [W10](weeks/W10.md) | *The Door That Opened Outward* | 5,789 | `1b30e4e36fa9e3cca585a5f43d3e96ca422d79d1` |
| [W11](weeks/W11.md) | *The Places Rain Could Find* | 5,132 | `7b7c53091e1dec4c253b271677468b8256bb8f75` |
| [PROLOGUE–W11 reader](READING_COPY_PROLOGUE_W01_W11_PARTIAL_NONCANON.md) | 12 exact source components | 53,549 including assembly | source-exact readback verified |

**New Week 10–11 fiction:** 10,921 whitespace-delimited words including metadata. The 2016 regular-season Chronicle now includes six independently dramatized fixtures per Week 1–11: **66 / 78** archived regular-season results, with Weeks 12–13 remaining. The twelve-component reading copy reproduces all component bodies **verbatim** between Git-blob markers. Previous editions remain on the branch; these are not newly edited causal-novel chapters. Separate historical postseason and epilogue files are not included in the reading copy.

## Archive provenance and exact scores

**Authoritative retained evidence:** `living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json`, Git blob `6dbec1fe2537139f3a97c6a78250e2bae082a518`, `source=Flaim ESPN 1417621`, `year=2016`. Source limits explicitly state **historical identity unverified** and that multiweek scoring may duplicate matchup periods. These are archived rows, **not a fresh authenticated upstream ESPN read**. All twelve entries per pair of weeks are anchored to specific period and scoring identifiers. Team titles are not real-person identity evidence; historical scoring home/away does not establish venue.

| Week / scene | Home scoring team (ID) | Home points | Away scoring team (ID) | Away points | Archive winner | Margin |
|---|---|---:|---|---:|---|---:|
| 10 A | Bavid Dabbs (4) | 111.48 | The Real Austin's Hyenas (12) | 127.58 | The Real Austin's Hyenas | 16.10 |
| 10 B | Scruffy Looking Nerf Herders (1) | 82.12 | Pittsy's Rhino's (6) | 125.84 | Pittsy's Rhino's | 43.72 |
| 10 C | Kunt Liquors (3) | 111.50 | All ACL Squad (9) | 114.74 | All ACL Squad | 3.24 |
| 10 D | Hook, Line, and Zeeker (2) | 132.10 | Team Hollingshead (10) | 103.22 | Hook, Line, and Zeeker | 28.88 |
| 10 E | Here, Ok I took L's (5) | 76.70 | Austin's Hyena's (8) | 102.14 | Austin's Hyena's | 25.44 |
| 10 F | I'M HERE SO I WON'T GET FINED (11) | 117.34 | The Gunslingers (7) | 120.64 | The Gunslingers | 3.30 |
| 11 A | The Real Austin's Hyenas (12) | 114.72 | Scruffy Looking Nerf Herders (1) | 100.10 | The Real Austin's Hyenas | 14.62 |
| 11 B | Pittsy's Rhino's (6) | 64.48 | Kunt Liquors (3) | 128.10 | Kunt Liquors | 63.62 |
| 11 C | All ACL Squad (9) | 93.64 | Hook, Line, and Zeeker (2) | 96.68 | Hook, Line, and Zeeker | 3.04 |
| 11 D | Team Hollingshead (10) | 104.18 | Here, Ok I took L's (5) | 78.54 | Team Hollingshead | 25.64 |
| 11 E | Austin's Hyena's (8) | 119.90 | I'M HERE SO I WON'T GET FINED (11) | 91.78 | Austin's Hyena's | 28.12 |
| 11 F | The Gunslingers (7) | 146.54 | Bavid Dabbs (4) | 100.38 | The Gunslingers | 46.16 |

**Identity separation:** The Real Austin's Hyenas = **ID 12**; Austin's Hyena's = **ID 8**. Historical slot 1 as proposed fictional Jake remains **NOT PROVIDER-AUTHENTICATED**. No owner genealogy, private real-world motive, historical venue or future result is asserted.

## Continuity entry and exit

**Entering W10:** eastern room unsafe and closed; door still hinged when W10 begins; private woman's chest and letters inaccessible. Material invoice unpaid; younger worker retains unverified old timber credit and independent new wheelwright-yard work; the unturned wheel's failed rope halted the prior lift. Previous borrowed three-night canvas returned; claimant remains UNKNOWN and stranger's message unanswered.

**Exiting W10:** door removed from eastern-room hinges by unauthorized informal effort, inspected and safely blocked, not rehung; chest still inaccessible; carpenter proposes an unpriced freestanding retrieval frame pending footing check and consent. A messenger receives an honest custody description but no delivery receipt. Younger worker continues paid work; old credit remains open; a possible witness declines to give sworn testimony.

**Exiting W11:** water reaches a separate proposed storeroom and independent measurements find potential movement in an adjoining exterior post, leading to a **precautionary wider cordon**; no collapse or inferred catastrophic loss. Market assistant grants a new **one-night small awning loan**, explicitly distinct from the expired older canvas arrangement. Woman with chest preserves her agency and key to box; room remains sealed, letters not recovered, proposed retrieval frame not built and specialist inspection pending. Missing claimant unknown; separate messenger's rumor of a hidden person unsupported; sealed original message unopened and undelivered; grain moved to tested trestles; old timber credit and unpaid invoice remain open. Worker's new employment remains independent and wheel does not operate.

All locations, social arrangements, geography, technology, injuries and events in these scenes are **PROPOSED FICTION**, requiring period-specific Character Canon/Atlas review. Jake is the sole eligible twelve-owner interior **PRINCIPAL_CHARACTER**; supporting people remain external. No Edrin/Edin/Oren POV; no personified El Niño.

## Executable validation and readbacks

On existing PR branch, new regression files:
- `qa/test_2016_tenth_week.py` — 12 methods checking pinned source blob, IDs, winners, exact six fixture headers, ~5.8k-word narrative, sole eligible POV, identity/Atlas restrictions, open-loop continuity, immutable prior W09 and four protected 2026 hard-canon files.
- `qa/test_2016_partial_reader_w10.py` — 6 source-exact component and negative-scope tests.
- `qa/test_2016_eleventh_week.py` — 12 equivalent source/POV/safety/continuity tests for W11, with W10 blob protected.
- `qa/test_2016_partial_reader_w11.py` — 6 reader assembly/source-exact/negative-scope tests.

**36 added test methods**, explicitly included as four distinct `novel-os-ci.yml` workflow steps. At **code head `de04c2650859200e873d8ea03814b2cf1804423c`** the following GitHub Action runs were **observed COMPLETED / SUCCESS**:

- Novel OS CI **#40968320547** — Week 10 and Week 11 manuscript+reader individual steps **SUCCESS** in the same passing job.
- Cross-Domain Authority CI **#40968320553** — SUCCESS.
- Bullpen Runtime CI **#40968320646** — SUCCESS.
- Repository Merge Gate **#40968320472** — SUCCESS.

Direct authenticated GitHub readback compared 12 beginning/end source markers and content bodies against their exact twelve component files; **12/12 byte-exact** (UTF-8 text and pinned Git blob identity). Four protected hard-canon files on the branch **match main Git blobs exactly**, independently of the tests: Prologue `5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0`, Chapter I `26a17f05eb0565e7648c29add03ee9580ec933c3`, Chapter II `30fcf23a3eb8872fa0fb4dff029fe30044141121`, Chapter III `49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc`.

This receipt may be committed after the tested code head; **do not assume final receipt-inclusive commit CI is green until checked**.

## Adversarial review request and unresolved gates

**Self-review, not independent acceptance.** Developmental editor: test whether serial episodes remain a series of Jake's moral awakenings instead of intensifying causality, and whether the woman with chest, worker and registrar hold independent dramatic goals. Character Canon: check historical eligibility and date-specific expression. Atlas: audit roof/store geometry, travel and weather, without treating invented premises as established sites. Librarian: ensure two similarly titled teams remain distinct and archive limits survive publicity. Umpire: audit all tests, source claims, noncanonical status, Founder-only gates, and whether the compilation is a chronological anthology rather than an edited novel.

**Gates HELD:** historical human-owner/slot authentication; historical Character Canon and Atlas; independent literary/editorial acceptance; independent Umpire; Founder-only canon promotion; merge and publication. Comments requesting independent reviews are not approvals.

**NEXT:** inspect final exact-head Actions checks and any actual independent review; write source-anchored 2016 Week 12 six-fixture Chronicle and extend reader; maintain old open loops and its source-time cutoff. Move to Week 13 afterward, then examine existing historical postseason/epilogue files for editorial reconstruction. No automatic week-to-chapter conversion.