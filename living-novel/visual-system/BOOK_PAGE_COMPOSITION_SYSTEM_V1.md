# SCHEMIN’ ’26 — BOOK PAGE COMPOSITION SYSTEM V1

**Status:** BINDING PREVIS STANDARD  
**Source precedent:** Prologue physical-book architecture + Memo OS V5.5 Page Packets / Visual Rhythm controls.

## Principle
There is **no default page template**.

There are reusable **composition families**. The final family is chosen from the content of each page/spread.

## Composition families
### T0 — Pure Literary
100% prose. No visual. Use for dialogue, argument, suspense and sequences where image would interrupt velocity.

### T1 — Literary + Marginal Mark
85–95% prose; 5–15% map/object/ornament. Use for recurring objects, road symbols, small environmental anchors and memory echoes.

### T2 — Text-Led Illustrated
65–80% prose; 20–35% illustration. Environment or artifact carries information the prose should not repeat.

### T3 — Balanced Narrative Plate
45–65% prose; 35–55% art. Use for character entrances, new locations, consequential aftermath.

### T4 — Image-Led
10–35% prose; 65–90% art. Use for major reveal, landscape orientation, visual silence or material consequence.

### T5 — Full-Bleed / Near-Silent
0–15% prose. Rare. Earned reveal, chapter threshold, major world-memory scar, or atmospheric reset.

### T6 — Two-Page Cinematic Spread
One composition across verso+recto. Used only when geography, scale or simultaneous action requires spread width. Gutter-safe focal design mandatory.

### T7 — Artifact / Evidence Page
Receipt, ledger, notice, map scrap, wager, certification, object study. Factual text is typeset externally and sourced.

### T8 — Cartographic Page
Map is primary. Physical Atlas is base; optional civil/domain/route/state overlays are visually separated.

### T9 — Character Plate
Environmental portrait, not mascot card. Hard-blocked for final principal-character render until reference binding + raster QA pass.

### T10 — World-Memory Overlay
Stable map/environment with temporal scar/repair/reputation overlay. Base geography remains visually distinguishable from memory layer.

### T11 — Diagram / Institutional Cutaway
Record House, Hall of Keeping, League Chamber, fortress, route system, etc. Must explain function; avoid decorative pseudo-blueprints.

### T12 — Transition / Vignette
Sparse art, strong negative space, page-turn control; useful after dense sequences.

## Selection logic
For every manuscript anchor:
1. What must the reader understand on this page?
2. Does space matter? → T8/T10/T11.
3. Does material evidence matter? → T7.
4. Does character recognition matter? → T3/T9 only if identity gate permits.
5. Does atmosphere/scale matter more than event detail? → T4/T5/T6.
6. Would art repeat the prose? → T0/T1.
7. Does the next page contain a reveal? Preserve page-turn surprise.

## Page Design Packet — book extension
Required fields:
- PAGE/SPREAD ID
- MANUSCRIPT ANCHOR
- CHAPTER / MOVEMENT
- NARRATIVE JOB
- WORD RANGE / TEXT DENSITY
- COMPOSITION FAMILY
- RECTO / VERSO / SPREAD
- PAGE-TURN FUNCTION
- CHARACTERS / OWNER RESOLUTION
- ACTIVE REFERENCE IDS / GATE STATE
- LOCATION ID
- ATLAS LAYERS USED
- ENTERING WORLD STATE
- WORLD MEMORY OVERLAYS
- CAMERA / VIEWPOINT
- FOREGROUND / MIDGROUND / BACKGROUND
- ART:TEXT RATIO
- COPY BUDGET
- IMAGE TELLS
- PROSE TELLS
- EXACT TYPESET DATA
- BLEED / GUTTER / TRIM SAFETY
- PREVIOUS-PAGE GRAMMAR
- NEXT-PAGE GRAMMAR
- PRINT RISK
- DIGITAL / MOBILE ADAPTATION
- QA REQUIRED
- LOCK STATE

## Visual-rhythm constraints
- Never repeat the same dominant composition family on three consecutive pages unless the repetition is itself narrative.
- Adjacent major character portraits are avoided.
- After T5/T6, prefer decompression via T0/T1/T7/T12.
- Two consecutive maps must answer different spatial questions.
- A chapter opener should not be followed immediately by another full-bleed unless intentionally creating a visual prologue.
- Artifact pages require a return to lived world within 1–2 page turns unless the artifact sequence is the story.
- Character art cannot consume space merely to “show the character.”

## Page-specific planning rule
**Visual assignment happens after a provisional typography pass but before final pagination lock.**

Process:
MANUSCRIPT ANCHOR → PROVISIONAL TYPE FLOW → PAGE/SPREAD JOB → TEMPLATE FAMILY → ART/MAP BRIEF → COMPOSITION → REFLOW → FINAL PAGINATION → PAGE QA.

This avoids designing to the temporary 110-page Word export.

## Reader-facing design language
Typography remains literary and quiet. Images can touch trim when earned; text never sits on uncontrolled high-detail regions. Maps may use linework, relief, ink, wash and limited accent coding, but no modern dashboard legend aesthetic.

## Acceptance
A page passes only when:
- it has a unique narrative job;
- image and prose are complementary;
- its geometry helps the reading experience;
- it is legible at print size;
- its map/character/world inputs are governed;
- its relationship to adjacent pages is intentional.
