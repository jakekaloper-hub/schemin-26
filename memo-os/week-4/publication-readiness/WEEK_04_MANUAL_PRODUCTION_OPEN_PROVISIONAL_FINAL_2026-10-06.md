# WEEK 4 MANUAL PRODUCTION OPENING — PROVISIONAL-FINAL AUTHORIZATION

**Status:** ACTIVE / COMMISSIONER-AUTHORIZED MANUAL PRODUCTION
**Issue:** Schemin '26 Week 4 Memo
**Page count:** 27
**Production command:** `generate page N`
**Data state:** PROVISIONAL_FINAL / PROVIDER_DECIDED_PENDING
**Creative state:** LOCKED
**Page-generation gate:** ACTIVE

## Bullpen Director ruling

Manual page production may begin **now**, before ESPN/Flaim performs the overnight `DECIDED` transaction, because:
- MNF is complete;
- all NFL scoring for Week 4 is complete;
- Flaim has refreshed stable completed-football scores;
- the 27-page architecture, story beats, characters, world state, visual concepts, text hierarchy and rejection criteria are already locked;
- the only remaining result authority distinction is provider status and possible stat correction.

This authorization does **not** convert provisional results into immutable official truth.

It opens the art-production lane under a mandatory revalidation contract.

## Production rule

When Jake says:

`generate page N`

Bullpen/production must:
1. retrieve the official page packet;
2. retrieve the provisional-final Flaim snapshot and page-impact register;
3. retrieve all applicable character/world/reference authority;
4. run the full PAGE_GENERATION_GATE preflight;
5. generate a candidate;
6. inspect the candidate under the same gate;
7. reject/repair internally until the candidate passes;
8. deliver only a QA-passed PNG.

## Provisional-result pages

Pages containing result-dependent scores, margins, records, rankings, result language or result-derived world consequence may be generated now using the current completed-football values.

Their production record must carry:

`PROVISIONAL_FINAL_DATA_USED / MORNING_REVALIDATION_REQUIRED`

If the morning ESPN/Flaim `DECIDED` transaction produces **no data change**, the page may be promoted by receipt without art regeneration.

If the morning transaction changes any printed/depicted deterministic fact on a page:
- that page becomes `REVALIDATION_FAIL / REGENERATE_OR_RETYPESET`;
- no other page is reopened unless its own deterministic facts changed;
- story/visual architecture still remains locked.

## No-finality-block pages

Pages whose current manifest state is `NO_FINALITY_BLOCK` may be generated and treated as fully QA-approved now, subject only to normal raster/character/world QA.

## Page 25 exception

W4-P25 Pittsy's Book may begin environmental/art production, but the **final settlement page cannot be accepted as final** until:
- current Flaim result math is verified at DECIDED; and
- Pitts supplies the authoritative booked-ticket ledger.

Until then Page 25 remains:

`ART_READY / SETTLEMENT_DATA_PENDING`

Do not invent stakes, bettors, payouts or Book P/L.

## Page 27 exception

W4-P27 may be generated from the staged World Delta only if its selected objects are explicitly labeled provisional in the production record.

The final page lock must wait for the morning World State Delta transaction.

## Director approvals

- **Closer:** APPROVED — open manual production now; no creative reopening.
- **Groundskeeper:** APPROVED — 27-page sequence and production packets are stable.
- **Scout:** APPROVED WITH MORNING REVALIDATION — current scores are completed-football provisional finals; provider status remains UNDECIDED.
- **Librarian:** APPROVED — authority chain remains intact; provisional data is clearly separated from immutable canon.
- **World / Atlas Director:** APPROVED — no permanent result-driven mutation transacts before official finality.
- **Beat Writer:** APPROVED — no story-room reopening; only deterministic result fields may change.
- **Visual Direction Lead:** APPROVED — page art can proceed from locked compositions.
- **Character QA / Canon:** APPROVED ON SPEC — every candidate still requires raster acceptance before delivery.
- **Publication Design:** APPROVED — deterministic text may use provisional-final values, with morning revalidation receipt.
- **Author Council:** APPROVED — restraint pass remains locked; no new concepts.
- **Umpire:** APPROVED — production may start under provisional-final contract; morning audit is verification, not a rewrite.
- **Architect / CAIO:** APPROVED — control plane may distinguish provisional data acceptance from creative authority.

## Morning promotion transaction

Command:

`/bullpen resume Week 4 from official ESPN/Flaim DECIDED flip`

For each already-produced page:
1. compare every result-derived field against official Fact Lock;
2. PASS if unchanged;
3. regenerate/retypeset only pages with a changed deterministic field;
4. promote unchanged pages from provisional-data receipt to official-data receipt;
5. do not reopen art/story merely because provider status changed.

## Commissioner workflow

Jake's intended workflow is authoritative:

`generate page 1`
→ save approved PNG locally

`generate page 2`
→ save approved PNG locally

Continue through all 27 pages.

After 27 approved PNGs are returned:
- verify 27/27;
- verify order;
- reject duplicates/missing pages;
- normalize portrait mobile/iPhone dimensions;
- compile one PDF;
- run final assembly QA.

## Final production state

**MANUAL PRODUCTION: OPEN**
**CREATIVE PACKET: LOCKED**
**PAGE_GENERATION_GATE: ACTIVE**
**PROVISIONAL-FINAL DATA: AUTHORIZED FOR PRODUCTION**
**MORNING DECIDED REVALIDATION: MANDATORY**
**PITTS LEDGER: STILL REQUIRED FOR FINAL PAGE 25 SETTLEMENT**
