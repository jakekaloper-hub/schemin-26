# WEEKLY MEMO REGRESSION SUITE V1
Status: POSTMORTEM CANDIDATE SUITE

## Character invariants
- R-CHAR-001 ObiWan: blond human Trade Jedi; green blade; golden retriever when scene packet calls for companion; NO championship belt.
- R-CHAR-002 D0nkey K0ng: human warrior torso + full equine body; Arsenal-red language; never gorilla, ape, horse-headed humanoid substitute or human-only barbarian.
- R-CHAR-003 TDS: exactly one green/gold reptilian humanoid; #3 identity; never three snakes/heads; continuity state must equal current ledger state.
- R-CHAR-004 TDS POST_HAIRCUT state cannot silently regain dreadlocks.
- R-CHAR-005 El Niño remains nonhuman storm/water/lightning elemental.
- R-CHAR-006 Mud Dogs remains huge mud-soaked monstrous canine/wolf creature, not normal dog.
- R-CHAR-007 Dr. Duckhook remains anthropomorphic white duck golfer.
- R-CHAR-008 HMB remains corpse-pale immortal champion with black/rune championship language across renames.
- R-CHAR-009 Chili Outlaw remains western outlaw/pitmaster; Dark Horse association preserved when continuity requires it.
- R-CHAR-010 Red Leopards remains anthropomorphic red leopard with red/black/gold armor.
- R-CHAR-011 LLC remains human corporate raider with dark-suit identity.
- R-CHAR-012 Seven Deadly Chins remains established heavyset bearded human identity with canonical props when scene packet requires them.

## Fact invariants
- R-FACT-001 Every matchup score equals FACT_LOCK.
- R-FACT-002 Every W-L record reconciles with previous record + locked result.
- R-FACT-003 League-wide wins equal league-wide losses.
- R-FACT-004 PF/PA arithmetic reconciles; each weekly score appears once as PF and once as opponent PA.
- R-FACT-005 Standings and editorial Power Rankings are separate data types.
- R-FACT-006 Betting ledger recomputes exactly from transaction/bet inputs.
- R-FACT-007 Commissioner-supplied facts remain provenance-labeled until independently verified.
- R-FACT-008 No play-by-play causality inferred from score deltas.

## Raster / assembly invariants
- R-ASM-001 final PDF page count equals release manifest.
- R-ASM-002 every page master has a durable hash, dimensions and approval state.
- R-ASM-003 no two page slots point to same unintended master hash.
- R-ASM-004 no approved master is regenerated or replaced without explicit reopen event.
- R-ASM-005 final PDF render is visually compared against locked masters.
- R-ASM-006 native portrait ratio and crop are preserved.

## Typography / mobile invariants
- R-TYPE-001 scores, records, standings, rankings, odds, bids and financial ledgers use deterministic typography.
- R-TYPE-002 generated art may contain decorative noncritical lettering only when explicitly approved.
- R-MOB-001 every page receives phone-scale proof before PAGE_LOCK.
- R-MOB-002 no critical copy requires zoom.
- R-MOB-003 safe zones protect headers, footers and edge text.

## Issue invariants
- R-ISSUE-001 all 12 teams appear in league-wide modules when module scope requires all teams.
- R-ISSUE-002 no matchup receives >2 chapter pages without Story Room justification; cover exposure counted separately.
- R-ISSUE-003 no single composition family occupies >35% of issue without explicit Art Director override.
- R-ISSUE-004 opening, consequence section, horizon and closing each have distinct narrative jobs.
- R-ISSUE-005 continuity ledger updates after every page that creates a persistent consequence.

## Gate-integrity invariant
- R-GATE-001 PASS without evidence pointer is invalid. Aesthetic approval does not implicitly waive FACT, CHARACTER, CONTINUITY or MOBILE QA.
