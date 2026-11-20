# 2016 Week Nine — source-concordance, fiction and continuity QA receipt

**Status:** NONCANON; PR #243 OPEN/DRAFT; Authors Council, historical Character Canon, Atlas, independent Umpire and Founder approval **HOLD / NOT RECEIVED**. Date: 2026-10-29.

## Concrete literary work

- New 2016 Week Nine narrative [*The Wheel That Learned to Wait*](weeks/W09.md): **5,001 words including metadata**, six independently dramatized archived competitive fixtures, original opening and aftermath.
- A new [ten-component Prologue–W09 partial reading copy](READING_COPY_PROLOGUE_W01_W09_PARTIAL_NONCANON.md): **42,582 words including assembly headers**, with the ten prior/added component bodies reproduced verbatim and source-blob annotated.
- All preceding 2016 source components and earlier reader snapshots preserved. **54 of 78** 2016 regular-season archived pairings now have draft prose across Weeks 1–9; 2016 postseason and epilogue are not contained in this reader.

The fictional story leaves the shelter for an unapproved wheelwright's yard, boot maker, apprentices, measurement disputes and a halted lift. The worker begins independent employment and chooses a boot repair without Jake negotiating on his behalf. His disputed old timber compensation is *not* settled by new work. The machine does not begin operating. No place is promoted as historical/Atlas canon.

## Pinned historical archive (not current upstream authentication)

Retained file: `living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json`, Git blob `6dbec1fe2537139f3a97c6a78250e2bae082a518`; league 1417621, `weeks[week==9].matchups`. The six exact archive rows, including winner and margin, are:

| Scene | Home (ID) | Home score | Away (ID) | Away score | Winning side | Margin |
|---|---|---:|---|---:|---|---:|
| A | The Real Austin's Hyenas (12) | 123.66 | I'M HERE SO I WON'T GET FINED (11) | 71.76 | The Real Austin's Hyenas | 51.90 |
| B | Pittsy's Rhino's (6) | 88.80 | Bavid Dabbs (4) | 81.44 | Pittsy's Rhino's | 7.36 |
| C | All ACL Squad (9) | 122.10 | Scruffy Looking Nerf Herders (1) | 97.32 | All ACL Squad | 24.78 |
| D | Team Hollingshead (10) | 129.26 | Kunt Liquors (3) | 131.42 | Kunt Liquors | 2.16 |
| E | Austin's Hyena's (8) | 94.92 | Hook, Line, and Zeeker (2) | 127.92 | Hook, Line, and Zeeker | 33.00 |
| F | The Gunslingers (7) | 131.08 | Here, Ok I took L's (5) | 113.56 | The Gunslingers | 17.52 |

Exactly twelve IDs participate and slot-one historical defeat is fixture evidence only. Slot 1/Jake owner binding is **NOT PROVIDER-AUTHENTICATED**. Do not conflate similar hyena team IDs 8 and 12, invent owner motives or treat scoring home/away as geographic positions.

## Continuity and restrictions

**Entry from Week Eight:** borrowed canvas term has ended, no permanent shelter built; eastern roof closed; seller's material invoice unpaid; old worker timber credit disputed and open; missing claimant UNKNOWN; message from unfamiliar traveler does not prove relatives; child's bowl returned to original child. Itinerant singer's song is not Jake's property.

**Exit from Week Nine:** proposed worker chooses new short-term employment, possible repaired boot and stay near workyard; neither his old labor credit nor any shelter claim is discharged. Supported test lift is halted when rope frays, so no new working pump or water channel exists. The wheelwright's daughter is an observed actor with a concrete ambition, not a new principal viewpoint. No known identity/outcome for claimant; no new authorized settlement or political border; eastern room still closed and invoice still unpaid.

**Literary challenge for independent review:** The wheel and stopped lift risk an obvious metaphor for institutional patience; the worker's newfound agency must persist beyond a teaching episode. Worldbuilding details such as machine design, artisanship, shops, geography and labour law remain author-room proposals requiring period correctness. The weekly result paragraphs preserve exhaustive Chronicle coverage but should not be promoted mechanically as novel chapters. Avoid a ninth round of Jake experiencing an ethical lesson in every scene.

## Engineering evidence

New `qa/test_2016_ninth_week.py` (12 cases) checks source hash, six team pairings, exact winner/score/margin, story structure and substance, sole eligible principal POV, historical identity limits, W08 immutable blob, older debts and 2026 hard-canon protected blobs. New `qa/test_2016_partial_reader_w09.py` (6 cases) validates ordered ten source-exact components, exact git blobs, noncanon scope and no protected 2026 chapter inclusions. CI has two named new checks. Direct authenticated GitHub file readback confirmed six score headers and ten verbatim reader bodies before this receipt; final-head GitHub Actions status must be checked separately. No independent Umpire approval is implied.

**NEXT:** Verify workflows on final commit, request real independent editorial/Atlas/Umpire challenge, then continue six authoritative Week Ten archive rows and extend reader without altering protected canon. **No merge, promotion or public release.**
