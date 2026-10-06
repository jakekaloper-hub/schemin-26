# WEEK 4 PAGE GENERATION GATE — QA BEFORE DELIVERY

**Status:** PRODUCTION HOLD / RECOVERY CONTROLS REQUIRED
**Issue:** Schemin '26 Week 4 Memo
**Page count:** 27
**Commissioner workflow after recovery:** "generate page N" → deterministic preflight → reference-bound art path → deterministic composition → acceptance evidence → approved PNG only
**Release blockers:** production-integrity recovery + exact publishable identity enforcement + deterministic composition + renderer reference-binding proof; Flaim finality remains a separate data gate


## PRODUCTION HOLD — 2026-10-06

Live Pages 1–4 exposed release-blocking failures. This gate is CLOSED until `WEEK_04_PRODUCTION_INTEGRITY_RECOVERY_2026-10-06.md` is cleared.

Hard additions:
- retrieve `WEEK_04_PUBLISHABLE_IDENTITY_REGISTRY.json` before every page;
- internal labels such as DK/OBI/TDS/HMB/7DC are never publishable team-name copy;
- exact team names/divisions/GOTW labels/dates/scores/records/rankings/odds are deterministic composition only;
- Page 3 prohibits character icons entirely;
- Pages 4–7 must carry the Week 3-established GAME OF THE WEEK treatment for **D0nkey K0ng vs ObiWan Jacoby**;
- character-bearing generation is blocked unless the current approved visual reference can actually be supplied to the renderer;
- a semantic prompt description is not a reference-mount receipt;
- a visually plausible candidate is not QA evidence;
- Commissioner review is not the first defect-detection layer.

## Commissioner operating rule

For Week 4, "QA before art" and "QA of the art" are treated as **one PAGE_GENERATION_GATE**.

This is not a sequence where a page is casually generated, delivered, and audited later.

A page command means:

1. retrieve the locked page packet;
2. complete all pre-render QA;
3. resolve final deterministic data;
4. render a candidate;
5. inspect that candidate against the same gate;
6. reject/repair internally if it fails;
7. only mark the page APPROVED when the candidate satisfies the packet;
8. only an APPROVED page belongs in Jake's local Week 4 PNG folder.

A failed candidate is not a locked Memo page and cannot be assembled into the final PDF.

## Important implementation distinction

The gate has two checks because visual facts cannot be verified before pixels exist:

### A. PRE-RENDER PREFLIGHT — must PASS before any render request
- correct page number and title;
- correct story beat;
- correct page count/sequence;
- correct character IDs;
- correct approved source/hash authority;
- page-specific character overrides;
- world/venue/geography authority;
- written-material plan;
- deterministic data slots populated or intentionally blank;
- composition;
- camera;
- foreground/midground/background;
- props and continuity objects;
- negative constraints;
- mobile-safe text hierarchy;
- previous/next-page continuity;
- Author Council restraint;
- Umpire preflight.

### B. CANDIDATE ACCEPTANCE — same gate, after candidate exists and before page lock
- character identity visibly correct;
- character count/anatomy correct;
- forbidden props absent;
- venue/world continuity correct;
- visual beat matches the locked page;
- no accidental story rewrite;
- no hallucinated numerical text;
- text hierarchy legible;
- phone/mobile framing safe;
- composition matches packet;
- no cross-character contamination;
- no stale reference identity;
- no unexpected logo/character/object drift.

The page is considered generated for production purposes only after B passes.

## Native renderer visibility note

The production system must distinguish **candidate visibility** from **page acceptance**. A renderer may surface a candidate image as part of generation, but that does not make it an approved Memo PNG. The production record must clearly mark only QA-passed output as APPROVED_FOR_LOCAL_FOLDER.

## Flaim finality is the only remaining editorial/data input

Before Week 4 manual production begins, Bullpen may leave only these fields unresolved:
- official final winner;
- official final score;
- final margin;
- updated record;
- final standings;
- material verified player-level events already called for by a locked page;
- Pittsy's Book settlement arithmetic;
- downstream deterministic summaries derived from those facts.

Flaim finality may not reopen:
- 27-page count;
- page order;
- titles already locked;
- genres;
- visual concepts;
- character identities;
- page-specific character states;
- world/venue plan;
- composition intent;
- written-material purpose;
- bridge-page ban.

## Page command contract

When Jake says **"generate page N"**, the system must not ask for the prompt again.

It must:
- fetch WEEK_04_27_PAGE_DIRECTOR_REVIEW_PACKET.md;
- fetch WEEK_04_OFFICIAL_MANUAL_PRODUCTION_PACKET.md;
- fetch current character authority;
- fetch current world authority;
- fetch final Fact Lock after Flaim refresh;
- fetch page-specific deterministic data;
- run PRE-RENDER PREFLIGHT;
- if any non-Flaim field is unresolved, STOP as INTERNAL_PREPRODUCTION_DEFECT;
- if only required Flaim-derived data is unresolved, STOP as WAITING_ON_FLAIM;
- otherwise generate candidate;
- inspect candidate under CANDIDATE ACCEPTANCE;
- if candidate fails, it is REJECTED_NOT_FOR_FOLDER;
- if candidate passes, mark APPROVED_FOR_LOCAL_FOLDER and return it as the page.

## Character hard locks

All character-bearing pages inherit WEEK_04_12_CHARACTER_AUTHORITY_MATRIX.json and VISUAL_REFERENCE_AUTHORITY_V1.json.

DK, TDS and HMB owner-specific approved source/hash authority outranks the stale master lineup.

## Mobile production target

Every page is authored as a portrait mobile-reading page suitable for final assembly into an iPhone/mobile-friendly PDF.

Before approval:
- essential text must remain readable at phone width;
- important faces/characters/props must remain inside safe crop;
- no critical text near trim/crop edges;
- dense data pages must use deterministic typography, not generated text;
- page composition must remain legible when viewed one page at a time on a phone.

## Final PDF workflow

Jake will save each approved PNG locally.

After all 27 approved PNGs are supplied back for assembly:
- verify 27/27 filenames/order;
- verify no duplicate/missing pages;
- verify each is an approved Week 4 page;
- normalize portrait page dimensions for mobile/iPhone reading;
- preserve image quality;
- compile a single ordered PDF;
- run final assembly QA;
- return final PDF.

The final assembly audit is not a substitute for page QA. Every page must already have passed PAGE_GENERATION_GATE before inclusion.
