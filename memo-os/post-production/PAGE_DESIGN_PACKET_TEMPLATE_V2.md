# PAGE DESIGN PACKET TEMPLATE V2

PAGE ID:
CHAPTER/MODULE:
NARRATIVE JOB:
STORY BEAT:
CREATIVE DNA PATTERN IDs (from memo-os/creative-dna/COMMISSIONER_CREATIVE_DNA_V1.json):
CREATIVE DNA PACKET JSON REF (for structural validation):
EXEMPLAR PAGE ID + WHAT TO BORROW (composition/story, NOT identity):
ART-LED COPY TREATMENT (integrated / hybrid / minimal; no boilerplate overture):
MATCHUP-WAVE ACCEPTED PORTRAIT SOURCE (when result strip or rankings):
FANTASY EVENT → STORY CONSEQUENCE EVIDENCE:
FACT DEPENDENCIES + classification:
CHARACTERS:
OWNER→CHARACTER RESOLUTION:
MASTER REFERENCE IDs:
IMMUTABLE CHARACTER FEATURES:
CURRENT CONTINUITY OVERLAYS:
FORBIDDEN MUTATIONS:
WORLD REGION/LOCATION:
MAP/ATLAS ID:
ENTERING WORLD STATE:
CONTINUITY-OUT:
TIME / WEATHER / LIGHT:
CAMERA DISTANCE / ANGLE:
FOREGROUND:
MIDGROUND:
BACKGROUND:
CHARACTER SCALE:
ILLUSTRATION:TEXT RATIO:
COPY BUDGET:
IMAGE TELLS:
PROSE TELLS:
DETERMINISTIC TYPOGRAPHY/DATA:
PREVIOUS PAGE RELATIONSHIP:
NEXT PAGE RELATIONSHIP:
MOBILE RISKS:
QA REQUIRED:
APPROVAL/LOCK STATE:

## Creative DNA previsualization integration
Load `../creative-dna/COMMISSIONER_CREATIVE_DNA_V1.md` as a subordinate creative preference under V5.5, not as character/fact/release authority. Every used pattern requires its structured payload in the issue candidate JSON; validate with `python memo-os/creative-dna/validate_creative_dna.py --packet path/to/candidate.json` before image production. Missing/invalid structure is a preproduction HOLD; passing structure does NOT authorize rendering or publication. Prose may be composited directly on illustration if mobile-legible; exact numeric data always remains deterministic.

## Cinematography specialist routing (additive; effective only after PR acceptance)

SPECIALIST DESK: Frank Masi motion-picture unit-stills *reference* — no personal participation or endorsement.
CONSULTATION TIER: 1 if page is a cover, decisive matchup beat, action, character turning point, cinematic climax, or trailer key art; 2 for portraits, dialogue, establishing stills and other promotion art; 3 for tables, scores, and pure typography.
UNIT-STILLS REVIEW STATUS: NOT_RUN until Cinematography Director reviews. For Tier 1, PASS requires the completed review record described in `memo-os/cinematography/FRANK_MASI_UNIT_STILLS_REFERENCE_V1.md`.
DECISIVE INSTANT:
CAMERA POSITION / AXIS:
OPTICAL PERSPECTIVE / SUBJECT SEPARATION:
MOTIVATED LIGHT FROM CAMERA POSITION:
SILHOUETTE / OCCLUSION:
TEXT-SAFE REGION:
ATLAS HORIZON / CHARACTER REFERENCE CHECK:
STILLS REVIEWER / RECEIPT:

Photographic consultation never authorizes missing source reference bytes, absent approval, new geography, fabricated game facts, or overwritten typography. Existing V5.5 character and geography gates control.

## Scene Direction & Cinematic Staging (optional additive block; does not supersede existing required fields)

SCENE INTENT / DRAMATIC CHANGE:
VISUAL INTENSITY: grounded | epic | mythic
SCENE CATEGORY: combat | dialogue | environment | aftermath | motion
CHARACTER INTENTIONS / EYELINES / PERFORMANCE:
BLOCKING POSITIONS / CONTACT / ACTION AXIS / SILHOUETTES:
SCENE-CORRECT COSTUME STATE (identity preserved):
REQUIRED ENVIRONMENT / NON-SALIENT DETAILS:
CAMERA POSITION / SHOT SCALE / MOTIVATED LIGHT / DECISIVE INSTANT:
FOCAL HIERARCHY / TEXT SAFE AREA:
STORYBOARD AND ALTERNATIVE COMPOSITION RECEIPTS:
PUBLISHED-METHOD SPECIALIST REFERENCES (advisory only):
CANONICAL BULLPEN ROUTE + COUNTERWEIGHT RECEIPT:
STAGING PREFLIGHT: BLOCK | HOLD | PREVIS_READY
RASTER ACCEPTANCE: independently assessed under existing PAGE_GENERATION_GATE

Reference implementation: `memo-os/scene_direction.py`.
Previs readiness never implies render eligibility or publication acceptance.
