# Week 11 — All-35 production source audit and clean-PNG restart gate
**Observed November 24, 2026. Scope:** existing Week 11 issue on draft PR #313. **State: COMPLETE SOURCE ASSEMBLY / FINAL RENDER RESET / RELEASE HOLD.**

## Executive finding
The user correctly identified a workflow failure: the generation tool was given a short cinematic image description rather than the mandatory integrated illustrated-memo page request. F15 rendered a good-looking standalone splash with no source-specified headline, matchup, narration or dialogue. The 1080×1920 final-size and 390px mobile proof were also missed. F14 is not an accepted page. Neither may count toward official Week 11. **Do not make more image requests until Jake issues the individual page instruction and the gate below is applied.** No tldraw, no PDF assembly, no unsolicited bulk render.

This audit does NOT invalidate the canonical preproduction: all 35 items have matched **title, reader text, final-result overlay, shot specification, visual ownership, individual commission and location record**. They did not have a single end-to-end render input package: this was created and read back as [the authoritative 35-page integrated handoff](../preproduction/W11_ALL_35_INTEGRATED_RENDER_INPUTS_2026-11-24.json).

## Cross-source inventory and spot-check
| Requirement | Examined evidence | Current result |
| --- | --- | --- |
| 35 reader copy bodies / titles | Nov24 `W11_READER_LETTERING` | 35/35 exact source bodies captured, no blank body; full tables preserved |
| 35 production story overlays | Nov24 `W11_POST_MNF_ALL_35_FOLIO_SELECTED_CUTS` | 35/35; conditional earlier winners must NOT override selected Nov24 outcomes |
| 35 commissioned camera/lighting specs | Nov23 `W11_ALL_35_VISUAL_DIRECTOR_SHOT_SPECS` | 35/35 |
| 35 individual folio brief sections | `OPEN_BOARD_PAGE_REHEARSAL` | 35/35 |
| 35 location records | `WEEK11_LOCATION_DESK.json` | 35/35, not 35 approved cinematic plates |
| 14 full matchup performance scripts | Nov24 six-game director's cut | 14/14 mapped, performance only unless the editor authorizes expanded print copy |
| Working native + phone proof pairs | Nov24 current production desk | 17/35 declared; these remain INTERNAL PROOFS, never accepted finals |
| Accepted art and source locks | independent Umpire / Data Steward | 0/35 finals accepted, SCK still ASSIGNED; FACT_LOCK pending |
| Matchup location photographic plates | pre-render source register | 6/6 missing approved cinematic venue plate |
| Matchup model reference input bindings | pre-render source register | 0 provider-attested bound cast pairs |
| Independent consistency and proof validation | this desk audit | SOURCE JOIN PASS only; NOT render or publication approval |

**Binary access limitation:** the GitHub connector can return empty bytes for some large native files. Presence in the desk inventory is not full independent pixel/hash verification of those native PNGs. Existing desk proof SHA receipts are preserved; later render QA must inspect actual bytes.

## Correction to text authority
**Never equate no folio numbering with no page transcription.**
- On-page include actual issue masthead, story title, matchup deck, reader narration, dialogue, exact scores/tables as applicable. Do not print `F##`, `P##`, production status, hidden IDs, prompts, debugging labels or proof watermarks.
- Reader lettering is the current exact *print* source. The longer director's cut is the source for acting, lighting, scene progression, dramatic motivation and any **proposed** extra printable copy. Where an artist/editor wants a longer paragraph, return it for page-specific approval; do not automatically discard director prose or silently convert all performance notes into print copy.
- Source precedence: official ESPN/House data -> Nov24 selected results -> exact reader lettering -> current director performance -> shot/Atlas/Character controls -> Week10 published composition. Older conditional story workshop is not live outcome authority.
- Replace visual-only generation requests with integrated per-page request carrying both exact print copy and performance treatment in separate explicit fields. Long writing is typeset as page typography, not engraved on an implausibly small physical prop.

## Go/no-go for EACH individual image
1. **Source packet:** fetch the page from the integrated 35-folio input; confirm headline, masthead, **all exact print copy including dialogue/tables**, plus selected outcome and acting script. Do not submit a one-sentence scene-only prompt.
2. **Identity and Atlas:** use actual active binary source attachments, approved temporal appearance and venue references where required. Current character route does not attest mounted reference hashes or subject bindings; do not assert canonical identity PASS without evidence. Keep architectural/hydrological continuity and previous-page cast/props.
3. **One composite PNG:** typography plus cinematic scene in one deliberately art-directed 9:16 composition. No generic poster, no PDF-looking four-panel, no default header/image/paragraph stack, no internal page labels. If AI lettering drifts, deterministic type must be overlaid from exact source.
4. **Artifact QA:** inspect native 1080×1920 PNG and 390×693 phone proof, verify dimensions, exact text, scoreboard labels, character identity, physical cause/effect, scene continuity and readable hierarchy. Record SHA-256, correction and acceptance separately for every page.
5. **Authority:** owner provides individual page direction. The Closer manages sequence; Setup Man, Beat Writer, visual lead, Librarian and GM review under existing responsibilities. Independent Umpire acceptance and trusted Data Steward's RECEIVED→VALIDATED/FACT_LOCK are separate release prerequisites. Never describe an internal candidate as an accepted final master.
6. **Reset:** P14/P15 chat outputs are REJECTED as full master handoffs; F08 scenic ChatGPT example is only a source study. The 17 desk proofs are comparisons/review assets, not reusable final issue masters without full independent review. Fresh final PNG work begins with the user's designated folio and only after the page gate is satisfied.

## All 35 page-by-page review matrix
| Internal ID (never printed) | Reader page | Existing native+phone | Required gate / design verification |
| --- | --- | --- | --- |
| F01 | One Last Crossing | No qualifying native/phone proof | Cover choice, Wilson appearance, authorized bridge or Chili scene plate, image review |
| F02 | The bottom of the register | Working proof only | Working proof, source and presentation check; two-owner portraits if illustrated |
| F03 | Commissioner’s Note | Working proof only | Commissioner voice, byline and actual signature; unsigned proof only |
| F04 | The Week 11 board | Working proof only | Six finals, decimal alignment and independent data lock |
| F05 | The Twelve · first six | Working proof only | Commissioner rank approval; exact six current character portraits |
| F06 | The Twelve · second six | Working proof only | Commissioner rank approval; exact remaining six portraits; consistent F05 scale |
| F07 | What seventh place means | Working proof only | Official seeding/records and playoff cutoff; independent data lock |
| F08 | The roads between | No qualifying native/phone proof | Hearthroad/Mountain Lake separate sites; cleared atmospheric images; candidate re-render |
| F09 | After you, Austin | No qualifying native/phone proof | Wilson four-hoof authority conflict and Mountain Lake accepted plate |
| F10 | He was here before us | No qualifying native/phone proof | Same bridge axis, correct Wilson/Austin bound references; fall causality |
| F11 | The carter listens | No qualifying native/phone proof | Wilson resurfaces alive; lake hydrology and exact identities |
| F12 | Six. I told her six. | No qualifying native/phone proof | Same Week10 truck geometry, Jordan/Manning references and Hearthroad plate |
| F13 | The radio call | No qualifying native/phone proof | Two keg count, tie physics and loaded-truck route permission |
| F14 | Off the board | No qualifying native/phone proof | Rejected chat candidate; exact OFF BOARD sheet, two bound characters and carnival |
| F15 | The safest seat | No qualifying native/phone proof | Rejected chat candidate; full copy missing, one throw/hinge/underwater scene; Chili look |
| F16 | At the ladder | No qualifying native/phone proof | Jake head to both boots, full-length phone visibility, tank same orientation |
| F17 | Pick a side | No qualifying native/phone proof | Phillip single reptile body three heads, Kevin identity, waterfall visitor side |
| F18 | The dry stone | No qualifying native/phone proof | Same waterfall path/stone; no hunter costume or bag |
| F19 | The wrong turn | No qualifying native/phone proof | Gators & Dawgs sign/stands left/postcard right, truthful source image and cast |
| F20 | The road that comes back | No qualifying native/phone proof | Repeat same sign/ruts; Bobby's deception and safe Ben retreat |
| F21 | The visitor's chair | No qualifying native/phone proof | Jackson office plate, two cast references and wet key/first unsigned paper |
| F22 | The second sheet | No qualifying native/phone proof | LLC corporate document and board succession; no fantasy ownership transfer |
| F23 | What the starters changed | Working proof only | G01–G03 starter values, team labels and result comparison |
| F24 | Who could answer? | Working proof only | G04–G06 starter values, response vs opponent and bench distinction |
| F25 | The cost of Sunday | Working proof only | Separate House Nov19 statement from roster date and positions |
| F26 | The next starting sheet | Working proof only | Chiefs vs Texans D/ST bench/start, margin cannot overturn win |
| F27 | Who made it onto the roster? | Working proof only | 43 events = 32 complete/6 failed/5 canceled; no failed bids called pickups |
| F28 | Three divisions | Working proof only | Four teams per division, official records and conditional Week12 story |
| F29 | The Twelve · scoring form | Working proof only | 70/30 math exact; do not confuse index with editorial rankings |
| F30 | Seven places | Working proof only | TheFFHub odds source/date; possibility vs simulation, no false eliminations |
| F31 | Under a deal we never made? | No qualifying native/phone proof | Private shack not porch, Jake bound look, fictional interview/2023 1.04 margin |
| F32 | The next six | Working proof only | Six Week12 visitor-to-host fixtures and arrow orientation |
| F33 | Next week's feature | No qualifying native/phone proof | Commissioner GOTW selection, Chins/El Niño odds and Storm Bowl plate |
| F34 | Pittsy’s Book | Working proof only | Three-headed Phillip source binding; market lines; Book close-only geography |
| F35 | They know the way home | Working proof only | Storm Coast Road camera and vehicle-access hold; single Final Word line |

## Authority and unresolved dependencies
- **Commissioner:** F03 note signature and voice, F05–F06 editorial rankings, F33 proposed next feature, and final cover selection F01 from actual image candidates.
- **Character/Librarian:** resolve Wilson Look competing visual source; exact published October 22 preferred Brandon Chili Outlaw reference was not present at its registered repository target; Jake and Brandon's lineup crop files exist but are NOT validated renderer attachment receipts. Other named cast face references require scene-specific bindings.
- **Atlas:** six cinematic venue pictures remain unapproved; F13 loaded-truck through-route, F31 private shack depiction, F34 Book-wide exterior, F35 motor-vehicle camera/route, and F01 bridge cover remain source-constrained. No false location promotion from generated imagery.
- **Data Release Steward:** `ECS-DATA-STEWARD-1417621-20261124` assigned but no authenticated signed RECEIVED/VALIDATED; `CANONICAL_SNAPSHOT_LOCK` and `FACT_LOCK` blocked. Final sports facts have ESPN direct comparison but this is not independent acceptance.
- **Umpire:** 0/35 accepted final native PNGs; images and phone proofs require independent pixel review.
- **System:** current image renderer supports contextual image references but its documented capabilities do not return binding/mounted-byte attestations, so governed identity certification remains unproven. Noncanonical candidate studies may be produced with explicit status; they must not be relabeled as published canon.

## Production disposition
**State: DO NOT CLAIM ALL GREEN.** Exact source-packet assembly is now complete for all 35. Blockers requiring actual authoritative human or provider decisions remain. The correct repair is a clean **final-art generation reset** with each folio sourced from the compiled pack, not another manuscript rebuild or additional tldraw planning. Keep previous Week 10/Week 11 visual studies only as references. Changes are documented on the existing draft PR #313, not on a parallel production branch.
