# Week 4 Keeper / Campaign-State Closure — Memo OS

**Status:** ACTIVE WEEK 4 STORY-INTELLIGENCE ADDENDUM / NOT STORY LOCKED  
**Date:** 2026-10-05  
**League:** Pro Schemin' Football League — ESPN 1417621  
**Authority:** ESPN/Flaim keeper metadata + confirmed draft picks + audited Mercer post-draft keeper ledger + current Week 4 rosters + verified external injury reporting + existing Week 3 canon  
**Production effect:** STORY INTELLIGENCE / STORY ROOM / TRANSITION DELTA ONLY  
**No finished art. No final winner language.**

## 1. Closure ruling

Week 4 requires a **foundational-asset consequence** layer in addition to ordinary score / projection / injury / transaction signals.

Working Week 4 field:

`KEEPER / FOUNDATIONAL-ASSET CONSEQUENCE`

This is a Week 4 test, not a new Memo OS subsystem.

Core distinction:

> **A WEEKLY RESULT CHANGES THE SCOREBOARD. A FOUNDATIONAL-ASSET EVENT CAN CHANGE THE CAMPAIGN.**

## 2. Authoritative keeper ledger reconciliation

ESPN league metadata reports a two-keeper league and supplies raw keeper player IDs by team. ESPN's completed 2026 draft marks keeper selections directly and provides confirmed rounds. The provider ledger agrees with the audited Mercer post-draft keeper ledger.

| Team | Owner | Division | Keeper 1 | Cost | Keeper 2 | Cost | Provider check |
|---|---|---|---|---:|---|---:|---|
| ObiWan Jacoby | Jake / Trade Jedi | Burgers | Puka Nacua | R6 | Rashee Rice | **R13** | CONFIRMED |
| D0nkey K0ng | Wilson Look | Burgers | Bijan Robinson | R1 | Breece Hall | R4 | CONFIRMED |
| Three Dreaded Snake | Phillip Pitts | Burgers | Chris Olave | R7 | Javonte Williams | R10 | CONFIRMED |
| Mud Dogs | Bobby Mitchell | Burgers | Saquon Barkley | R1 | Sam LaPorta | R4 | CONFIRMED |
| Red Leopards | Kevin Zeek | Wings | Lamar Jackson | R4 | Kyren Williams | R14 | CONFIRMED |
| Slob on my Dobb | Jordan Hollingshead | Wings | Quinshon Judkins | R8 | Bucky Irving | R14 | CONFIRMED |
| Chili Cheesers | Brandon Pryor | Wings | Malik Nabers | R2 | Brock Bowers | R7 | CONFIRMED |
| Dr. Duckhook | Zach Wilson | Wings | Jahmyr Gibbs | R1 | Drake Maye | R15 | CONFIRMED |
| The LLC | David Babb | Pizza | Omarion Hampton | R2 | Colston Loveland | R9 | CONFIRMED |
| His Majesty's Blood | Austin Byars | Pizza | Jaxon Smith-Njigba | R2 | De'Von Achane | R15 | CONFIRMED |
| El Niño | Manning Welty | Pizza | Nico Collins | R9 | UNKNOWN / no second keeper in ESPN snapshot | — | ONE KEEPER ONLY |
| Seven Deadly Chins | Ben Whipple | Pizza | Emeka Egbuka | R6 | Tyler Warren | R8 | CONFIRMED |

### Rashee Rice round reconciliation

**AUTHORITATIVE ROUND: R13.**

Provider evidence:
- ESPN keeperPlayerIds for ObiWan include Rashee Rice player ID `4428331`.
- ESPN completed 2026 draft marks player `4428331` as `isKeeper: true` at **Round 13, overall pick 154**.
- Audited Mercer report independently records Rashee Rice — R13.

**STALE VALUE TO RETIRE: R14.**

Any Week 4 / Novel / derived context that still labels Rice R14 is superseded by the confirmed ESPN draft result.

## 3. Rashee Rice Week 4 injury verification receipt

### Pre-game state
Kansas City's official Week 4 injury report listed Rice with a **knee** issue but full participation Wednesday/Thursday/Friday and no game-status designation. He was active for Week 4.

Primary pregame source:
https://www.chiefs.com/news/week-4-injury-report-chiefs-vs-raiders-2026

### In-game event
During the first quarter against Las Vegas on 2026-10-04, Rice pulled up after a short reception with a **hamstring injury**, left the game, and did not return. Contemporary reporting said Kansas City initially listed him questionable, later doubtful.

High-confidence sources:
- Reuters / Field Level Media: https://www.reuters.com/sports/chiefs-wr-rashee-rice-exits-with-hamstring-injury--flm-2026-10-04/
- Yahoo Sports game report: https://sports.yahoo.com/nfl/breaking-news/article/chiefs-wr-rashee-rice-leaves-early-vs-raiders-after-pulling-up-awkwardly-with-hamstring-injury-220141904.html

### Classification
- EVENT: VERIFIED IN-GAME HAMSTRING INJURY / EXIT
- RETURNED TO GAME: NO
- LONG-TERM SEVERITY: **UNKNOWN / PENDING FURTHER MEDICAL UPDATE**
- WEEK 4 CAMPAIGN STATE: **THREATENED**
- DO NOT WRITE: season-ending, multi-week absence, tear/strain grade, or other unsupported prognosis.

This is no longer merely Commissioner context. The in-game injury itself is externally verified.

## 4. Twelve-team Week 4 keeper-state addendum

Campaign vocabulary:
`INTACT / THREATENED / LOST / TRADED / IR / UNKNOWN / SUPERSEDED`

### BURGERS

#### ObiWan Jacoby
- Puka Nacua — R6 — current Week 4 roster: starter.
- Rashee Rice — R13 — current Week 4 roster: starter before in-game injury.
- Puka also returned to action in Week 4 after earlier injury absence, providing a **resource-restoration** counterpoint.
- Rice then exited Week 4 with verified hamstring injury and did not return.
- FOUNDATIONAL_ASSET_EVENT: **YES**
- STATE: Puka = INTACT / RETURNED; Rice = THREATENED.
- MEMO SIGNIFICANCE: HIGH.
- NOVEL SIGNIFICANCE: HIGH if threat persists; at minimum OFF_PAGE_BUT_ACTIVE.
- Story meaning: apparent matchup success can coexist with resource anxiety.

#### D0nkey K0ng
- Bijan Robinson — R1 — rostered / active.
- Breece Hall — R4 — rostered / bench.
- No keeper-specific loss/trade/IR event found in Week 4 evidence.
- STATE: INTACT / INTACT.
- FOUNDATIONAL_ASSET_EVENT: NO MATERIAL KEEPER-STATE CHANGE FOUND.

#### Three Dreaded Snake
- Chris Olave — R7 — **no longer on TDS roster; currently on Dr. Duckhook roster**.
- Javonte Williams — R10 — rostered / active.
- Week 4 provider transaction feed confirms a trade event but structured sides are incomplete; current roster state proves Olave changed teams, while exact package remains governed by commissioner/repo evidence.
- STATE: Olave = TRADED; Javonte = INTACT.
- FOUNDATIONAL_ASSET_EVENT: YES.
- MEMO SIGNIFICANCE: MEDIUM-HIGH as part of reconstruction.
- NOVEL SIGNIFICANCE: HIGH as keeper-resource conversion / campaign transformation.

#### Mud Dogs
- Saquon Barkley — R1 — rostered / starter.
- Sam LaPorta — R4 — rostered / starter.
- Barkley exited his NFL Week 4 game with a hamstring injury; postgame severity remained uncertain, though he was reported walking normally afterward.
- Source: https://www.reuters.com/sports/eagles-rb-saquon-barkley-hamstring-injured-vs-rams--flm-2026-10-04/
- STATE: Barkley = THREATENED; LaPorta = INTACT.
- FOUNDATIONAL_ASSET_EVENT: YES.
- MEMO SIGNIFICANCE: MEDIUM; use only if it clarifies Mud's roster/resource state.
- NOVEL SIGNIFICANCE: OFF_PAGE_BUT_ACTIVE pending medical resolution.

### WINGS

#### Red Leopards
- Lamar Jackson — R4 — rostered / starter.
- Kyren Williams — R14 — rostered / starter.
- Jackson exited NFL Week 4 with a left ankle injury and did not return; current reporting describes him as day-to-day.
- Source: https://www.reuters.com/sports/nfl-injury-roundup-lamar-jackson-hurts-ankle-star-wrs-go-down--flm-2026-10-05/
- STATE: Lamar = THREATENED; Kyren = INTACT.
- FOUNDATIONAL_ASSET_EVENT: YES.
- MEMO SIGNIFICANCE: MEDIUM-HIGH because Red's apparent strong fantasy week can coexist with keeper-resource uncertainty.
- NOVEL SIGNIFICANCE: OFF_PAGE_BUT_ACTIVE pending resolution.

#### Slob on my Dobb
- Quinshon Judkins — R8 — rostered / bench.
- Bucky Irving — R14 — rostered / starter/FLEX.
- No material Week 4 keeper-state loss, trade or IR change established.
- STATE: INTACT / INTACT.
- FOUNDATIONAL_ASSET_EVENT: NO MATERIAL KEEPER-STATE CHANGE FOUND.

#### Chili Cheesers
- Malik Nabers — R2 — rostered / starter.
- Brock Bowers — R7 — rostered / starter.
- Bowers entered Week 4 with availability noise but was active and produced in the game; no foundational loss is established.
- STATE: INTACT / INTACT.
- FOUNDATIONAL_ASSET_EVENT: NO MATERIAL KEEPER-STATE CHANGE FOUND.

#### Dr. Duckhook
- Jahmyr Gibbs — R1 — rostered / starter.
- Drake Maye — R15 — rostered / starter.
- No keeper loss / threat discovered in current Week 4 evidence.
- STATE: INTACT / INTACT.
- FOUNDATIONAL_ASSET_EVENT: NO MATERIAL KEEPER-STATE CHANGE FOUND.
- Additional campaign note: Duckhook acquired former TDS keeper Chris Olave, increasing current roster capital even while matchup performance may disappoint.

### PIZZA

#### The LLC
- Omarion Hampton — R2 — rostered / starter.
- Colston Loveland — R9 — rostered / bench.
- No material Week 4 keeper-state loss/trade/IR change established.
- STATE: INTACT / INTACT.
- FOUNDATIONAL_ASSET_EVENT: NO MATERIAL KEEPER-STATE CHANGE FOUND.

#### His Majesty's Blood
- Jaxon Smith-Njigba — R2 — rostered / active.
- De'Von Achane — R15 — rostered on IR.
- Week 3 canon establishes Achane's season-ending keeper loss.
- STATE: JSN = INTACT; Achane = LOST / IR.
- FOUNDATIONAL_ASSET_EVENT: PERSISTENT WEEK 3 CONSEQUENCE.
- MEMO SIGNIFICANCE: HIGH entering Week 4.
- NOVEL SIGNIFICANCE: HARD campaign-state consequence.
- Week 4 success must not narratively restore the lost keeper resource.

#### El Niño
- Nico Collins — R9 — only keeper exposed by ESPN keeper metadata.
- Current Week 4 roster: starter.
- External Week 4 game reporting shows Collins returned from injury and produced 7 catches, 118 yards and 2 touchdowns.
- Source: https://www.reuters.com/sports/nfl/cowboys-stun-texans-34-30-behind-ceedee-lamb-huge-second-half--flm-2026-10-04/
- STATE: INTACT / RETURNED.
- FOUNDATIONAL_ASSET_EVENT: POSITIVE RESOURCE RESTORATION.
- MEMO SIGNIFICANCE: LOW-MEDIUM; do not force into already-strong El Niño storm story unless it improves causality.
- NOVEL SIGNIFICANCE: OFF_PAGE_BUT_ACTIVE if prior absence mattered.
- Second keeper remains UNKNOWN; do not invent one.

#### Seven Deadly Chins
- Emeka Egbuka — R6 — rostered / starter.
- Tyler Warren — R8 — rostered / starter.
- No material Week 4 keeper-state loss/trade/IR change established.
- STATE: INTACT / INTACT.
- FOUNDATIONAL_ASSET_EVENT: NO MATERIAL KEEPER-STATE CHANGE FOUND.

## 5. Matchup impact delta

### DK × Obi
**MATERIAL UPDATE.**
The story now holds two simultaneous resource facts:
1. Puka Nacua's Week 4 return restores one premium keeper resource.
2. Rashee Rice's in-game hamstring injury threatens the other.

If the fantasy result continues to favor Obi, the emotional consequence is not simple triumph. The stronger formulation is:

**victory pressure relieved / keeper-resource uncertainty introduced.**

Do not let Rice replace the primary matchup story. It is a second-order consequence that becomes more important if medical updates worsen.

### Mud × TDS
**MATERIAL UPDATE.**
TDS's reconstruction is now explicitly a keeper-resource transformation story because Olave was a retained asset and has been moved off the roster. Mud simultaneously experienced a new Barkley keeper threat.

This makes the existing **breaking / rebuilding** transition more evidence-rich, but does not justify an extra page.

### Red × Duckhook
**MATERIAL UPDATE.**
Red's current matchup strength can coexist with Lamar Jackson keeper uncertainty. Duckhook, meanwhile, has absorbed former TDS keeper Chris Olave.

Use selectively; do not overwhelm the social/vacation story.

### Slob × Chili
**NO MATERIAL KEEPER STORY DELTA.**

### LLC × HMB
**CONFIRMED PERSISTENCE.**
Achane's Week 3 keeper loss remains active. Any HMB Week 4 stabilization happens from a permanently changed resource base.

### El Niño × 7DC
**MINOR POSITIVE DELTA.**
Nico Collins' return is a resource-restoration fact. It need not be foregrounded unless it helps explain El Niño's Week 4 scoring shape.

## 6. Story Room signal

Add this Week 4-only diagnostic beside existing live signals:

`FOUNDATIONAL_ASSET_STATE`

Questions:
- Was a keeper or equivalent structural resource threatened, lost, traded, restored or materially devalued?
- Did the event alter current capability?
- Did the event alter future control?
- Does it change the emotional meaning of the weekly result?
- Is the consequence verified, or only provisional?

This is a **signal**, not a new Keeper OS.

## 7. Transition architecture delta

No transition page is added.

### DK → TDS bridge
Existing repair / reconstruction bridge is **strengthened**, not redesigned:
- DK's repair state remains his own Week 3/Week 4 burden.
- Obi's Rice threat belongs primarily inside the DK/Obi aftermath.
- TDS's keeper conversion strengthens the reconstruction side.
- Mud's Barkley threat may remain a small data/prose signal rather than another object.

### Final Word
If unresolved at publication time, foundational-resource threats may become quiet carry-forward lines:
- Rice;
- Barkley;
- Lamar;
- Achane as persistent loss.

Do not stack all four visually.

### State of the Realm
Do not add keeper clutter unless a keeper event changes an actual divisional consequence or post-Week 4 strategic state.

## 8. QA

- [x] All 12 teams audited.
- [x] Provider keeper IDs reconciled with draft rounds.
- [x] El Niño's missing second keeper preserved as UNKNOWN.
- [x] Rashee Rice round conflict resolved to R13.
- [x] Rice hamstring exit verified; long-term severity left UNKNOWN.
- [x] Achane Week 3 consequence preserved.
- [x] TDS keeper conversion identified.
- [x] Additional keeper threats found: Saquon Barkley, Lamar Jackson.
- [x] Positive resource-restoration cases found: Puka Nacua, Nico Collins.
- [x] No final Week 4 fantasy winners asserted.
- [x] No new transition page created.
- [x] No new Keeper OS created.

## 9. Closer ruling

**PASS WITH DOCUMENTED LIMITATION — WEEK 4 KEEPER / CAMPAIGN-STATE CLOSURE.**

Limitation:
medical duration / Week 5 availability for Rice, Barkley and Lamar remains unresolved as of this receipt and must be refreshed before final Week 4 publication / Week 5 handoff if still material.

The keeper baseline itself is reconciled and ready for Week 4 planning.
