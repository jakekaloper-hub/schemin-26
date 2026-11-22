# SCHEMIN ’26 — WEEK 10 / THE COMMONWEALTH CUT
## Thirty-minute film production bible and storyboard summit

**Status:** PREPRODUCTION CANDIDATE / NOT ART-LOCKED / NO PUBLICATION APPROVAL
**Date:** 2026-11-22
**Authoritative editorial source:** `memo-os/week-10/preproduction/` on branch `memo-week10-preproduction-20261116` (PR #315)
**Adaptation assets:** `film_storyboard_v1.json`, `storyboard_viewer.html`, their generators, and the 20-lens workshop reconciliation
**Mandate:** One coherent film whose six Week 10 encounters and shared world matter more than merely turning thirty-four pictures into thirty-four title cards.

## 1. The film's argument

Week 10 is the week that *two teams cross 200 points* and every character sees the aftermath differently. The film begins with public record, visits six intensely individual encounters in the Commonwealth, returns to the record to see the consequences, and ends with next week's unresolved bridge and weather. There is no invented champion, playoff clinch, future result or generalized town where all twelve have met. The twelve protagonists remain twelve enduring perspectives, not a montage of NFL players.

The master has **exactly 30:00** of planned picture time, including held images, source narration, observed action, document graphics, pauses, and closing unresolved beats. The existing 34-page reader order remains intact, including **W10-P34 as the nineteenth scene, W10-P35 as scene 33 and W10-P33 as the final scene**. Optional **W10-P32** is not resurrected. Every film scene carries its source page ID, camera-action anchors and original reference-image paths and hashes.

**Narrative form:** cinematic ensemble fiction interleaved with a clearly distinguished factual sports-documentary voice. A memo is *the source*, not a literal screenplay. Avoid reciting league spreadsheets over random landscapes or making visual actions contradict source outcomes.

## 2. Ten movement structure / picture timeline

| Movement | Runtime | Underlying folios | Story function |
|---|---:|---|---|
| Opening / Public Memory | **00:00–03:16** (3:16) | P01–P04 | 200-point figures juxtaposed, inhabited Opening Drive, commissioner civic voice, verified scoreboard |
| Highland Rodeo | **03:16–06:15** (2:59) | P05–P07 | Chili's imitation → DK's lasso → controlled fall → deliberate binding → gallery cost |
| Storm and the Forgotten Court | **06:15–09:18** (3:03) | P08–P10 | Sandbag repair → runoff follows rut → later court collapse → Red's intimate aftermath |
| The Roads Between | **09:18–10:04** (0:46) | P11 | Coast, Upper Basin bridge and delayed wetland runoff separated in space/time |
| Temple / The Pause | **10:04–13:08** (3:04) | P12–P14 | Jackhammer → father's request → silence/hope → conscious volume increase → renewed drill |
| The Swamp Route | **13:08–16:07** (2:59) | P15–P17 | Mud Dogs barks at a raised service road → steady truck passes → empty road remains |
| Consequence Ledger | **16:07–17:46** (1:39) | P18, P34 | Week's verified fantasy performances, documentary causality and cost of Sunday |
| The Birthday | **17:46–20:38** (2:52) | P19–P21 | Duckhook/HMB greeting → burger box reveal → separate cake contact |
| Field Throne | **20:38–23:57** (3:19) | P22–P24 | ObiWan disables initial battery → LLC offers surrender/protection → refusal → remaining lightning |
| Aftershock / The Next Crossing | **23:57–30:00** (6:03) | P25–P31, P35, P33 | Readable lineups, moves, standings/divisions/playoff witnesses; Week 11 unresolved bridge and weather homecoming |

This is a **timing hypothesis** disciplined by original copy length, action and moment-to-moment causality; not an approved locked edit. The 2,278 source words occupy about 15:43 at 145 words/minute; the remainder is authored action, reaction, regional atmosphere, silent decisions, graphics and transitions. Character dialogue is a distinct *script-writing/ADR gate*, not magically contained in those 2,278 words.

## 3. Existing storyboards determine blocking

The primary read is `VISUAL_STORYTELLING_PASS_2026-11-17.md` and every page's `render-inputs/W10-Pxx/request.json#scene.visual_storytelling`. The prior visual benchmarks cited by that pass include Week 9 physical pages 12, 13, 17, 18 and 24 and Week 7 physical page 8. They supply *camera grammar*, not new faces, props, weather, titles or story facts.

Six non-negotiable continuity engines:

1. **Rodeo:** one geographically continuous Highland ring; rear-left service gate established; four-hoofed centaur controls his rope; lasso wraps *torso*, never neck; boots slip before deliberate manual hogtie. Sound is the knot's cause-and-effect.
2. **Storm:** repair on Storm Coast soccer field is followed by a *later* journey to the separate Central Basin Forgotten Court. Storm front is graded geographically. Falling limb strikes the existing right-wall backboard, not a fictional arena elsewhere.
3. **Temple:** Three Dreaded Snake has exactly **three heads on one torso** at a protected household balcony. Seven Deadly Chins stops the tool to adjust a speaker and only then resumes drilling; unreviewed relatives stay offscreen.
4. **Swamp:** raised firm road remains navigable. Truck remains loaded and at routine speed, hound never collides with wheels; no beer-keg battle, no elimination stamp.
5. **Birthday:** gift reveal and cake contact are separate actions, each set up by the previous shot. His Majesty's Blood's established costume and belt identity do not change.
6. **Throne:** same chair, steps and surviving battery across three pages. ObiWan's first disablement precedes LLC's offer; after the refusal, the LLC's hand signal triggers *remaining* battery lightning. Do not imply a new sovereign result.

Cross-page visual continuity is more important than generic blockbuster movement. Every approved POV within the source is retained; the 186 boards comprise **66 source-specific visual beats plus proposed coverage** (establishing, details, reactions and sound bridges). The extra 120 panels do **not** introduce an additional fictional event.

## 4. Advisory summit: how the teams are involved

The 20-entry `METHOD_LENS_WORKSHOP_INPUT.json` is a **modeled, source-anchored desk review**, not actual contact with the named professionals, a live Inklings gathering or authenticated Bullpen Director voting. The *existing* `inklings_workshop.py` reconciliation code was executed. Its output is `CANDIDATE_PENDING_INDEPENDENT_REVIEW`, with **17 accepted/adapted method findings**, **3 held counterarguments**, and **Umpire PENDING**. The complete per-person observation and assigned source page are in `METHOD_LENS_RECONCILIATION.json`.

The twelve discipline lenses each have an individual review question and proposed action:

| Published-method reference lens | Discipline | Shotboard decision |
|---|---|---|
| Doug Chiang | Production design | One physical field-throne set / reusable stairs, chair and battery placements (P22–P24) |
| Dylan Cole | Environment design | Regionally distinct weather and coherent bridge connector (P11) |
| Joe Letteri | Character/VFX | Three-headed single-body topology, cross-shot identity checks (P12) |
| Ngila Dickson | Costume | Carry Red's wet mud and material state from soccer field to later court (P08–P10) |
| Andy Serkis | Performance | Chili's eyes toward gallery after binding, no invented injuries (P07) |
| Rob Alonzo | Stunt/blocking | **HOLD:** torso lasso, slip mechanics and safe physical action proof before animated motion (P06) |
| James Baxter | Silhouette/pose | Truck and hound scales separated by usable raised road (P15–P16) |
| Frank Masi | Unit stills | Lens/eyeline/identity discipline for Duckhook/HMB guest reveal (P19) |
| John Knoll | VFX pipeline | **HOLD:** model/seed/reference/shot hashes and proper compositable motion/light plan (P24) |
| Jill Bogdanowicz | Color finishing | Different regional looks for exposed coast and cold inland court, readable faces (P10) |
| Thelma Schoonmaker | Editing | Give audible real silence before the temple's deliberate escalation (P13) |
| Randy Thom | Sound | **HOLD:** separate speaker/music, water, compressor and drill stems; clearance/original score (P14) |

The eight Inklings/author method lenses are routed to targeted issues instead of eight stylistic rewrites: **Tolkien** for lived geography; **Lewis** for refusal and moral stakes; **Martin** for twelve-sided consequences; **Rowling** for birthday setup/payoff; **Grisham** for sports-desk propulsion; **Le Guin** for the civic voice; **Sanderson** for consistent battery/energy rules; **Abercrombie** for intimate loss at the broken hoop. These are craft-analysis categories, **not imitations of those authors' prose or approvals from them**.

**Bullpen ownership proposal** under the canonical 18-Director constitution: Beat Writer leads story and screenplay; Pitching Coach audits models and free/quota assumptions; Architect and Setup Man validate media pipeline; Groundskeeper manages production operations; Librarian freezes source references; Scout/Analyst certify result copy; Commissioner reviews audience readability; Umpire independently vetoes canon/rights/regression failures; Closer reconciles only after the gates. Supporting project-specific Visual Director, Character Director, Atlas/World and Memo OS desks remain project roles, not new Bullpen Directors. This is the narrowest competent production set, not an invented nineteenth director. A real Bullpen command/counterweight receipt is required before claiming actual routing execution.

## 5. Video execution architecture

**Current proof (separate folder):** The earlier `W10-P11` tech demo on Jake's desktop demonstrated hosted Qwen image production, two Wan 2.2 short I2V clips, two independent Chatterbox voice stems, local atmospheric bed and a **14.25s** assembled MP4. It repeated two unique shots for mux testing and did not prove character lip-sync or scene approval. Subsequent Qwen requests hit **ZeroGPU quota exceeded**. It is a **noncanonical technical proof**, not a film asset candidate.

**Safe production tiers:**

- **Animatic:** Build 30:00 from existing approved imagery, 186 timed board panels, camera pans/parallax, voiceover, sparse actor ADR, original atmospheres/Foley and exact typeset league data. This uses much less hosted generative-video inference but is *not a fully moving film*.
- **Hybrid cinematic:** Full 30:00 editorial soundtrack plus selected Wan/other model motion for every high-value action, reaction and establishing beat. Keep held art/editorial insert only where narratively justified.
- **Full-motion film:** Source enough distinct moving footage to cover 1,800 seconds, plus retakes, performance continuity, character references, editorial sound and color finishing. At the demonstrated **3.563-second** clip length, uninterrupted coverage alone implies roughly **506 clips** before alternate takes; not free-tier-credible without confirmed compute entitlement.

**Never promise free unlimited compute, source-accurate faces or commercial rights merely because the models are open-weight.** Model access, Space access, hosted runtime quota and output license are four distinct checks. No paid job is authorized by this storyboard.

**Render pass data contract per shot:** immutable source page / beat ID; cast/reference SHA256; Atlas venue and weather state; camera/lens/movement; shot seconds; continuity in/out; source environment plate; approved input raster provenance; adapter and checkpoint revision; deterministic seed; render ID and output SHA256; rights/consent status; QC verdict. Save no credentials into prompts or Git history.

## 6. Lighting, color, sound, actor performance

- **Lighting:** produce one shared physically plausible set-lighting document per location before generation. Lighting physically baked into AI footage is not an adjustable 3D light rig. Preserve source layers, masks or depth passes when tool allows; color grades and relighting need separate test and cannot fix inconsistent illumination across cuts.
- **Color:** coastal pewter and wet stone ≠ inland court diffuse squall ≠ sheltered lantern-lit Highland ring ≠ warm birthday hall ≠ mountain throne lightning. One film palette, regionally differentiated exposure/mood.
- **Original score:** recurrent music motifs can bind six stories, but no copyrighted commercial track or recognizable melody is licensed by default. Keep music lower than readable dialogue.
- **Sound buses:** `DX` character dialogue/ADR, `VO` institutional narrator, `FX` impacts and physical interaction, `AMB` location/space/weather, `MX` original score. Export isolated stems plus full stereo mix; propose 48 kHz/24-bit PCM WAV and 24fps picture, and a 1080p review MP4 before 4K claims.
- **Dialogue:** Memo copy is documentary narration, not automatic in-world speech. New character dialogue requires a script lock, casting and performance approval. No invented official owner quotes; the temple page expressly avoids unsourced private lines and identifiable songs.
- **Editing:** uphold true causal geography, match eyelines, lens continuity, shot-to-shot exposure and readable official numbers. Avoid AI-generated lettering for fact tables; author those graphics as native vector/type assets in edit.
- **Accessibility:** captions for dialogue/VO, separate full transcript, descriptive audio notes, and titles legible at normal screen sizes.

## 7. Production backlog and acceptance gates

| Gate | Required evidence | Owner / verdict |
|---|---|---|
| **G0 Source freeze** | All 34 request SHA256 values match, original approved 1080×1920 folio reference paths recoverable, all results fixed | Librarian + Scout / source checks implemented |
| **G1 Story + lens review** | 186 shots indexed, complete transitions, screenplay/ADR plan, three held method objections dispositioned | Beat Writer + Inklings method review / current status candidate |
| **G2 Atlas + casting** | Each intended source character image available, species/costume/environment locks and inter-scene look bible | Atlas + Character Director / PENDING |
| **G3 Previs + look development** | Six hero set masters, human-reviewed camera/reference plates, motion/timing preview, action mechanical QA | Production / PENDING |
| **G4 Compute authorization** | Provider model/revision, rights, actual token/GPU cap, retry policy, no-cost proof or spending approval | Pitching Coach + Bookkeeper / PENDING |
| **G5 Motion & sound dailies** | Frame stability, dialogue/sync, safe blocking, lighting/identity continuity, 5 separate audio buses | Visual + Editorial + Audio / PENDING |
| **G6 Offline edit** | Exact 30-minute cut, no false scoreboard data, accurate subtitles, editable source project and clean handoffs | Beat Writer + publication desk / PENDING |
| **G7 Independent close** | Check tests, review of actual media, legal/commercial rights, Commissioner approval and Umpire + Closer signoff | Umpire/Closer/Founder / PENDING |

Editorial *must not* treat the deterministic storyboard contract test as clearance of pixels, real audio, named director participation, actual render quality or publication. Use reviewed canonical character images before any "locked appearance" claim.

## 8. Post-production handoff contract

Deliver a complete scene/shot manifest with source IDs and hashes; source footage by scene; image and reference plates; exact sports result graphic source values; subtitle cue list; voice/casting consent evidence; five unflattened audio stem families; original soundtrack rights note; metadata on model revision/seed; editor relink paths; versioned NLE timeline (Final Cut Pro, DaVinci Resolve or equivalent) with picture and sound aligned; high-resolution review render; and a QC/rights decision ledger.

The resulting storyboard JSON can drive an EDL or FCPXML adapter, but no automatic NLE project or full dialogue screenplay has been certified in this pass. Avoid dropping the entire 186-shot plan into an editor as if every AI frame already existed.

### Next executable film-production unit
Start with **W10-P05–P07** as the first *character-led* scene: approved Chili and D0nkey reference images, continuous Highland geography, non-neck lasso, controlled fall, manual knot, audible action and reaction, no unsourced dialogue. This is more representative of a movie than the earlier anonymous bridge proof. G2–G5 are therefore the first real critical path, not merely another model lookup.
