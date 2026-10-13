# Week 5 — Dark Wizard Chess: P004–P007 render preflight
**Commissioner instruction:** preflight the existing four-page storyline before generating images. This is a patch to established production controls, not a new storyboard or an authenticated director vote.

## Authority and facts
- Canonical repository: `jakekaloper-hub/schemin-26`; PR #152 working branch.
- Approved venue: `LOC-COMPACT-NEUTRAL-GROUNDS`, `REG-CENTRAL-BASIN`. Temporary monumental living chessboard on the market grounds; the site and stalls survive. **No permanent chess empire, no persistent conquest**, and keep actual vendors safe from falling stone.
- Reader-facing dominant title **His Majesty's Blood at Three Dreaded Snake** on all four PNGs; the literary scene subheads are subordinate. Never reuse dominant `SCHEMIN ’26` masthead.
- ESPN/FLAIM Week 5 now DECIDED: **His Majesty's Blood 113.45 (post-W5 3–2), Three Dreaded Snake 85.34 (post-W5 2–3), winner His Majesty's Blood, margin 28.11**. Avoid writing results into P004–P006 when that would spoil the story.
- Full standalone integrated image `1024×1536` PNG per page. No PDF assembly. Four separate images, **never** a triptych.
- Official Week 4 memo is quality minimum; compare P004 to comparable winner overture and P005–P007 to cinematic staging/action/finale. P007 specifically must use the official Week 4 P008/P012/P016/P020/P024/P028 lower-third payoff banner design standard.
- The existing page packets' manuscripts govern the prose. Their editorial status is candidate, not authenticated author-council approval. No manuscript regeneration or Tolkien/Peter Jackson endorsement claim.

## Owner images / non-negotiable visual continuity
1. **His Majesty's Blood / Austin Byars / `CHAR-AUSTIN-BYARS`:** source SHA-256 `eedfaaf0b2e2dd78a7a32e11aef333cab41278c206b65ec78c4aa4f1fd2c4f76`. Corpse-pale immortal Belt Keeper, long black hair, glowing pale eyes, black rune armor/cloak, massive rune sword and ACTUAL CHAMPIONSHIP BELT. Not a generic king, vampire, wizard, or other owner's face.
2. **Three Dreaded Snake / Phillip Pitts / `CHAR-PHILLIP-PITTS`:** source SHA-256 `31b9d7be295ba662b1332897ef7c33e2f64e92aeefb2d6abe625c08bac914c0c`. ONE anthropomorphic serpentine reptile body with EXACTLY THREE independently visible serpent heads, green/gold scales, glowing eyes, dark #3 football gear. Do not separate heads into three animals, collapse to one head, or substitute a human. Preserve the active hair/extension design as depicted in Commissioner source, never invent a human haircut.
3. Exact source SHA-256 verifies original file identity ONLY. For acceptance confirm the actual renderer conditioned on the intended two specific image originals, inspect depicted owner identity/anatomy, and record independent Umpire artwork verdict. Never claim that GitHub source presence proves in-render source binding.

## Page-specific locked beats and transitions

### P004 — Winner-POV overture
- **Source packet:** `pages/P004-gotw-overture/PAGE_PACKET.md`.
- **Reader title:** His Majesty's Blood at Three Dreaded Snake.
- **Scene:** The Belt Keeper approaches the ordinary market on the eastern road; monumental temporary chessboard barely seen beyond stalls, dense ground fog, torches and dark epic medieval architecture. Prose-forward, approximately 65–75% readable editorial treatment.
- **Manuscript continuity:** The Keeper counts steps; a belt can be carried onto neutral ground but does not make the land a throne. All three serpent heads observe differing paths. The Keeper's POV is verified by actual win, but the scene does NOT announce his victory.
- **Transition to P005:** move camera from human market scale to overwhelming chessboard geometry.
- **Hard reject:** generic conquering king, missing belt, huge triumphant results banner, multi-headed serpent depicted as separate creatures.

### P005 — Monumental chessboard setup
- **Source packet:** `pages/P005-gotw-setup/PAGE_PACKET.md`.
- **Camera:** elevated overhead wide of giant grid, foreground shuttered vendor carts, midfield two distinct owner characters opposite each other, background colossal stone rooks, cold blue moonlight against warm torch rims.
- **Manuscript continuity:** Traders shelter their wares behind enormous pieces; the three serpent heads argue over threats; the Keeper notices divided attention. Falling chess stone endangers market vendors who did not consent to the duel.
- **Transition to P006:** begin isolating the central tactical corridor and brittle stone knight.
- **Hard reject:** ordinary tabletop-size game, identical P004 camera, empty arena that erases the market, opponent species drift.

### P006 — Tactical collision
- **Source packet:** `pages/P006-gotw-escalation/PAGE_PACKET.md`.
- **Camera:** dramatic ground-level diagonal tracking, shattered stone knight in foreground, opposing pieces compress middle distance, vulnerable king beyond, hard shadows and sparks/debris.
- **Manuscript continuity:** The first impact shakes the stalls. The Keeper exploits disagreements between the serpent heads and advances a bishop. NFL player touchdowns are *narrative pressures*, not literal physical chess player appearances. Verify player-stat claims independently before embedding numeric callouts.
- **Transition to P007:** lead from the exposed center to the cracked decisive square.
- **Hard reject:** real NFL athletes in arena, 3 standalone serpents, copied branded movie characters, permanent city destruction.

### P007 — Checkmate and consequences / FINAL PAYOFF
- **Source packet:** `pages/P007-gotw-payoff/PAGE_PACKET.md`.
- **Camera:** worm's-eye view of fractured square, raised Belt Keeper and authentic belt, Three Dreaded Snake retreating WITH ALL THREE HEADS INTACT; smoke, debris, broken temporary stone pieces, inhabited market continuing beyond. Triumph dramatic; ground remains neutral. This payoff uses the **verified HMB win**; remove obsolete `UNDECIDED` qualifier without rewriting narrative.
- **Inside THE SAME 1024×1536 PNG:** full-width **distinct illustrated lower-third RESULT BANNER** in the official Week 4 payoff visual language, with side-by-side recognizable actual-character face crops from the same scene, exact visible team names, scores `113.45` and `85.34`, post-week records `3–2` and `2–3`, explicit WINNER `His Majesty's Blood`. No fake logo portraits. At 390px both owner insets and all score text must be legible.
- **Hard reject:** missing footer banner, score hallucination, wrong winner side, emperor-style conquest of neutral market, human or single-head TDS, unrecognizable portrait, anything unlike the prior three pages' style.

## Per-PNG acceptance, stop-and-fix
- Compare the actual generated image against the page before and the official Week 4 relevant sample: same gothic-black/gold/cold-moonlight palette, world geometry, architecture, text hierarchy, size scale, equipment, and character identities, but **a new camera/beat for each page**.
- Verify one page only, 1024×1536, integrated text, exact full team title, factual and narrative consistency, no extraneous banners/slogans, mobile 390px legibility, genuine reference-to-subject identity and portrait continuity.
- Check every visible serpent head count (three on ONE body) and Belt Keeper belt; do not rely only on text/metadata checks.
- P007 has an additional strict machine-data gate `production-evidence/WEEK_5_SIX_PAYOFF_FINAL_RESULT_BANNER_LOCK_2026-10-13.json` and `production-evidence/WEEK_5_PAYOFF_RESULT_BANNER_CONTRACT_2026-10-13.json`.
- Record independent authenticated Umpire acceptance per actual file; no invented Director signoff. Reject and remake a defective page before moving to the next. Passing CI validates instructions, not visual output.

**State:** PREPRODUCTION_BRIEF_RECONCILED. Actual cinematic image-generation reference mount and independent visual-image QA must still be demonstrated on generated images. No art produced by this preflight.
