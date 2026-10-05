# Week 4 Pre-Publication Director Declarations

**Status:** PRE-PRODUCTION CONTROL REVIEW  
**Date:** 2026-10-05  
**Generation:** PROHIBITED until Closer `PASS_TO_PRODUCTION`

## Scout
- Domain owned: league truth / Flaim / records / scoring / standings / player events.
- Controlling source: final Flaim/ESPN result state after MNF.
- Superseded sources: projections and live scoring snapshots once Fact Lock is issued.
- Unresolved ambiguity: provider remains UNDECIDED.
- Enforcement: freshness + contradiction + finality checks.
- Regression: pre-MNF finality must HOLD; contradictory winner/score must fail.
- Cross-reference: Umpire.
- Control verdict: **PASS**
- Execution verdict: **HOLD_EXTERNAL**

## Pitty desk
- Domain owned: Week 4 wager ledger / settlement.
- Controlling source: complete Week 4 submitted ticket ledger + final results.
- Superseded sources: provisional/unsettled wager notes.
- Unresolved ambiguity: final ledger inputs and results.
- Enforcement: deterministic arithmetic + prior-ledger reconciliation.
- Cross-reference: Scout.
- Control verdict: **PASS**
- Execution verdict: **HOLD_EXTERNAL**

## Power Rankings desk
- Domain owned: editorial 1–12 hierarchy.
- Controlling source: current ranking rules + prior published Week 3 baseline + final Week 4 facts.
- Superseded sources: standings-only or projection-driven ordering.
- Unresolved ambiguity: final ordering.
- Enforcement: current story-authority module + final records + movement baseline.
- Cross-reference: Scout + Beat Writer.
- Control verdict: **PASS**
- Execution verdict: **WAITING_ON_FACT_LOCK**

## Beat Writer
- Domain owned: matchup causality / prose purpose / current consequence branch.
- Controlling source: `WEEK_04_STORY_AUTHORITY_REGISTER.json`.
- Superseded sources: any older treatment named by the register.
- Unresolved ambiguity: final-result-dependent endings.
- Enforcement: current story ID/hash/receipt required downstream.
- Regression: LLC×HMB stale three-page branch must fail semantic fidelity.
- Cross-reference: Librarian.
- Control verdict: **PASS**
- Execution verdict: **WAITING_ON_FACT_LOCK**

## Librarian
- Domain owned: story supersession / canon / continuity / authority provenance.
- Controlling source: story-authority register + current canon authority.
- Superseded sources: older general planning when newer specific instructions exist.
- Unresolved ambiguity: none internal; result branches remain external.
- Enforcement: source-blob receipts + newer/more-specific precedence.
- Cross-reference: Beat Writer.
- Control verdict: **PASS**

## World / Atlas Director
- Domain owned: venue / geography / travel / environmental continuity.
- Controlling source: current World/Atlas decisions referenced by each story unit.
- Superseded sources: visually convenient invented geography.
- Unresolved ambiguity: venue sub-resolution where source marks it provisional.
- Enforcement: world dependency fields in current story units/page packets.
- Cross-reference: Librarian.
- Control verdict: **PASS WITH EXPLICIT PROVISIONAL VENUE HOLDS**

## Character Director / CAIO
- Domain owned: Character ID / exact source/hash / negatives / reference routing.
- Controlling source: active 12-character authority matrix and owner-specific canon.
- Superseded sources: stale aliases/assets/semantic reconstruction.
- Unresolved ambiguity: provider mounted-reference/subject-binding proof.
- Enforcement: exact expected SHA + fail-closed character runtime.
- Cross-reference: Visual Direction Lead.
- Control verdict: **PASS**
- Execution verdict: **HOLD_EXTERNAL FOR FINAL RENDER**

## Visual Direction Lead
- Domain owned: composition / visual story / hierarchy / art:text balance.
- Controlling source: current story unit visual_job + current page packet.
- Superseded sources: cinematic-but-semantic-mismatch composition.
- Unresolved ambiguity: none before Story Lock; rendering prohibited.
- Enforcement: no render without current story authority receipt and Closer authorization.
- Cross-reference: Beat Writer.
- Control verdict: **PASS**

## Groundskeeper
- Domain owned: page packets / dependency graph / sequencing.
- Controlling source: story-authority register; active page plan generated only after Story Lock.
- Superseded sources: fixed 19-page pre-lock plan.
- Unresolved ambiguity: final page count.
- Enforcement: page packet schema now requires story authority ID/hash/receipt/state.
- Cross-reference: Architect.
- Control verdict: **PASS**
- Execution verdict: **WAITING_ON_STORY_LOCK**

## Architect
- Domain owned: schemas / manifests / dependency enforcement.
- Controlling source: Week 4 publication controls.
- Superseded sources: hardcoded 19-page assumptions before Story Lock.
- Enforcement: Story-Lock-driven active page/assembly manifests + stale packet blocking.
- Cross-reference: CAIO.
- Control verdict: **PASS**

## Publication Design
- Domain owned: deterministic facts / typography / mobile readability.
- Controlling source: Fact Lock + deterministic data surfaces.
- Superseded sources: rasterized generated scores/records/odds/payouts.
- Enforcement: critical factual text stays deterministic.
- Cross-reference: Scout.
- Control verdict: **PASS**

## Author Council
- Domain owned: restraint / pacing / clarity / consequence.
- Controlling source: current story units, not older architecture.
- Superseded sources: redundant pages / stale jokes / generic spectacle.
- Enforcement: current-page-count challenge and semantic-fidelity review.
- Cross-reference: Beat Writer.
- Control verdict: **PASS**

## Umpire
- Domain owned: independent adversarial QA.
- Controlling source: assembled artifact compared to current story-authority register.
- Cross-reference: independent.
- Enforcement: schema PASS cannot substitute for semantic fidelity.
- Control verdict: **PASS FOR PRE-PRODUCTION CONTROL DESIGN**
- Final issue verdict: **NOT YET APPLICABLE**

## Closer pre-production ruling

The Closer may issue `PASS_TO_PRODUCTION` only after:
1. Story Authority Register PASS;
2. all six matchup story units CURRENT;
3. required editorial modules CURRENT;
4. page packets bind current story authority;
5. semantic-fidelity tests PASS;
6. character authority 12/12 PASS;
7. world dependencies resolved or explicitly held;
8. Director owner + counterweight PASS;
9. Umpire preflight PASS;
10. Fact Lock-dependent fields remain correctly held until finality.

Until then:

**NO ART GENERATION AUTHORIZED**
