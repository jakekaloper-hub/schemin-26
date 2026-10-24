# Schemin audience website — Bullpen whole-site audit

Date: October 22, 2026, America/New_York. Audited source: remote1c975c7b96f404a380326e9789838e3e80a333d8, local2e7b5d39 plus unchanged untracked artifacts. Production version4 source mirror af455a0138699d3d25b95ecde0472f67d688032b.

## Decision

NOT ACCEPTED as the founder's completed immersive illustrated publishing experience. A working audience archive and two reviewed environment presentations are delivered. The atlas remains a visibly unfinished block-and-number topology diagram. The public deployment is not evidence of visual acceptance. PR237 remains draft; no merge or full-art completion is claimed.

Review consisted of three independent delegated audits (content, UX/code, visual direction), root browser inspection and a simulated director synthesis. Director names below describe review responsibilities, not claims that real people or authenticated director runtimes attended.

## Simulated board synthesis

- Closer: prior completion language exceeded the evidence. Adopt this defect register and corrected coverage before further completion claims.
- Visual Direction Lead: painted banners do not finish a diagram; art and interface must be composed together for each page family.
- Groundskeeper: use the existing production spatial blueprint,23 location anchors, 18 routes and regional environment constraints. Every painted anchor must match its biome and landmarks. Unknown distances remain unknown.
- Librarian: existing source material is underused; reconcile approved upstream world state and narrative records rather than inventing replacement content.
- GM: discovery must connect world, people and actual publications. A working link that reaches an empty relationship section does not satisfy the journey.
- Architect / Tim Veil: region art slots are not publishable and character commissions have no reviewed-composition integration contract. Repair those deliberate interfaces while retaining identity gates.
- Scout: source-state omissions, raster-only memos and tiny map targets are substantive defects despite passing unit tests.
- Umpire: founder final visual acceptance remains open. Generated, source-reviewed, integrated and browser-verified are distinct states.

## Corrected artwork coverage

Under the founder requirement for a distinct treatment on every current primary route, the inventory covers at least 56 commissions, not 49. Seven region routes were added without adding commissions. The 49 inventory consists of five entrances, 23 locations, 12 profiles, five memo issues and four chapter openings. Seven region pages bring this to 56. Confirm any additional public routes before freezing scope.

| Family | Required compositions | Current evidence |
|---|---:|---|
| Homepage |1| One original environment, independent presentation review, desktop/phone checked; founder final acceptance open |
| Atlas |1| Panorama generated; positional integration rejected; diagram remains unfinished |
| Twelve index and profiles |13| Existing portrait reuse; zero original page-specific index/profile compositions |
| Destinations |23| One original homeland presentation;22 ungenerated |
| Regions |7| Zero; omitted from inventory and rejected by loader |
| Memo archive and issues |6| Original editions intact; zero original website framing compositions |
| Library and chapter readers |5| Text preserved; zero commissioned library/chapter compositions |
| Total |56| Two independently reviewed page-specific environment presentations; atlas panorama is not a completed positional commission |

Three slots have generated compositions.53 slots have no generated composition under the corrected56 scope. Atlas remains unfinished and founder acceptance remains open for all 56. The rejected ridge-only draft does not add a commissioned-route completion.

## Prioritized findings

| ID | Priority | Verified problem | Owner | Acceptance requirement |
|---|---|---|---|---|
| A01 |P1| Atlas uses overlapping blocks and anonymous numeric dots. Region titles require hover. Separate painting does not create a finished world map. |Visual/Groundskeeper| One coordinated source-backed composition; all 23 anchors reviewed; persistent region/place labels; readable desktop/phone |
| A02 |P1| Region hooks cannot publish: regionPage requests region-* IDs absent from builder allowlist and inventory. |Architect/Librarian| Route inventory reconciled; seven explicit eligible regional slots with byte/hash/review tests |
| A03 |P1| Character compositions have no integration path; CHAR-* rejected and profile has no composition consumer. |Architect/Visual| Explicit independently reviewed composition contract that preserves the separate character eligibility gate |
| A04 |P1| Destination renderer ignores imported worldState/baseState/features/accessRoutes. Pages repeat broad regional lists and landmark names. |Beat Writer/Groundskeeper| Each destination uses eligible specific place life, landmarks, current state and route context as readable editorial content |
| A05 |P1| Derived cards can lag upstream state: Mud Hill omits custodial cleanup,below-summit standard, summit unclaimed, no sovereignty transfer. |Librarian/Groundskeeper| Fresh upstream-state reconciliation; regression verifies contested-state qualifiers survive output |
| A06 |P1| All five memo characterIds arrays are empty. Character-to-memo journey is not delivered. |Librarian/GM| Source-reviewed relationship metadata and complete tested journeys; no inferred image associations presented as fact |
| A07 |P1| Released Weeks 2/3 lack pdf field; latest eligible issue has no original PDF download link. |Architect/Librarian| Exact original durable authorized retrieval path; verifiedbytes and access |
| A08 |P1|110 memo pages are raster images with title/page-onlyalt, no verified text companion. |Architect/Beat Writer| Preserve originals and add verified readable text/contents where supported; do not claim accessibility certification before review |
| A09 |P1| Primary phone map dots are about 9px diameter at 330px map width (radius 14 in a 1000-unit viewBox). Larger index alternatives exist, but map tapping remains poor. |GM/Architect| Adequate hit areas without collisions, readable labels and usable selection at phone widths |
| A10 |P2| Profiles expose morphology/props rather than enduring identity, narrative biography and established relationships. |Author Council/Librarian| Reconcile latest visual locks with eligible character dossiers,POV register and relationship graph |
| A11 |P2| Intermediate route stops link only to from endpoint, omitting onward to. |Architect| Source-ordered route presentation includes both directions/adjacent stops |
| A12 |P2| Character search promises homeland but does not search actual homeland name. |Architect/GM| Query matches actualhome, current team, owner and enduring identity |
| A13 |P2| Selecting a place at retained zoom can leave its marker offscreen. |Architect| Selected point revealed/recentered without corrupting persisted position |
| A14 |P2| Sticky memo Next changes image without returning to page boundary. |Architect| Deliberate page change announces and focuses/scrolls new page start; initial deep link handled separately; browser retest |
| A15 |P2| Memo image dimensions not reserved; replacements can shift layout. |Architect| Source aspect ratio reserved and useful loading/error state |
| A16 |P2| Explicit bookmark button only at reader top; returning to save can overwrite intended position. |GM/Architect| Current-position accessible toolbar; distinguish progress/bookmark if both promised |
| A17 |P2| Most art absent; huge shared mastheads delay primary content. Phone Week 3 initialviewport shows metadata/controls with originalpage below the fold. |Visual/GM| Page-family compositions lead with meaningful content; compact edition notes; actual phone proof |
| A18 |P2| Homepage curation fixed to narrow places andfirst four characters. |GM/Beat Writer| Intentional thematic collections grounded in verified relationships |
| A19 |P2| Atlas manifest usage text is notenforced. |Architect| Allowed usage contract prevents rejected positional use from reappearing |
| A20 |P3| Mobile hero rule targets .hero-footer but DOM uses .hero-index. |Architect| Correct selector and no overlap at narrow/enlarged text layouts |
| A21 |P3| Reader has section headings but no contents interface. |GM/Architect| Collapsible contents and useful within-chapter orientation |

## Source evidence

- productions/audience-site/src/app.js: atlas,regionPage, destination, characters, character, memo, read.
- productions/audience-site/build_public_catalog.py: load_artwork allowlist, location card import,pdf_mentions,recovered released memo projection.
- productions/audience-site/dist/data.json:23 locations, 7 zones, 12 characters, 5 memos, 4 chapters; current memo relationship arrays empty; Weeks 2/3 no pdf.
- world/data/current_world_state.json versus world/location-control-plane/locations/LOC-DK-MUD-HILL/CARD.json.
- world/production/CANONICAL_WORLD_PLATE_SPATIAL_BLUEPRINT_V1.md: existing production geography contract and explicit routes/anchor placement.
- world/production/visual-packets, location/homeland CARDs: richer scene context.
- living-novel/characters/01_JAKE_KALOPER.md and peers, RELATIONSHIP_GRAPH.md, canon/characters/TWELVE_CHARACTER_NARRATIVE_POV_REGISTER_V1.md: richer identity/narrative material requiring authority reconciliation.

## Browser evidence and limits

Twenty route checks: ten page types at 1348px desktop and 375px iframe content width inside a 390px frame. All sampled routes rendered expected heading/page identity and no horizontal overflow. BROWSER_ROUTE_CHECKS.json records observations. Screenshots captured for each view; root visually inspected homepage, atlas, region, destination, index, profile, archive, issue, library and reader across this audit and preceding batch checks. Phone samples confirm oversized mastheads/metadata delay memo art, profile is a reused portrait above technical description, reader retains readable cream surface.

This is page-type sampling, not all 56individualroutes or physical-device testing. No 200% zoom certification, screen-reader audit,full contrast certification or all-image-failure review. MemoNext-scroll, bookmark current position andmenu Escape focus require focused browser reproduction; code-based defects are marked here accordingly. Lazy portraits not loaded below the fold were not treated as broken images.

Prior suites: Node 10/10 and Python 22/22 with recovered release inputs; independent UX review reranNode 10/10. Passing tests do not cover these content/visual gaps. Sound behavior: Week 3 remains latest eligible release; Weeks 4/6 source and Week 5 review distinguished; exact archival text and approved portraits preserved; no unsupported POV menu invented.

## Ordered repair mission

1. Reconcile all routes,56-slot inventory, artusage contracts, regional publishing and gated character composition path.
2. Refresh authoritative source projections, current world state, narrative identity, reviewed publication/world relationships and original PDF access.
3. Build atlas composition guide from existing spatial blueprint:23-anchor matrix, 18 routes, biome/landmark requirements,persistentlabels,mobilehit areas. Generate against guide; repair conflicting areas; review every anchor beforeoverlay acceptance.
4. Prove one complete composition for each page family on desktop and phone, then complete artwork in coherent batches rather than adding painted headers to unchanged catalogs.
5. Repair memo/reader interactions and accessible content; test complete visitor journeys plus keyboard, reduced motion, loading, error and direct links.
6. Independent source/code/visual acceptance; retain founder final visual judgment. No full completion or 100% accuracy claim without corresponding evidence.
