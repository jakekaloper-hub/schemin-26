# CHARACTER INCIDENT AUDIT — Calm Before the Storm First Renderer Proof — 2026-10-01

**Severity:** CRITICAL / STOP ART
**Artifact:** rejected first renderer proof
**Decision:** character lock failed again. Do not retry by merely strengthening prose.

## Executive finding
The renderer accepted reference attachments but did not preserve the twelve canonical character identities. The resulting raster is a semantic ensemble reconstruction: recognizable broad motifs (duck golfer, gorilla, chili outlaw, reptile, etc.) were recomposed into newly invented bodies/faces/outfits. This is the same failure class the Character Control Plane was intended to prevent.

Therefore the previous conclusion “reference attachment works” must be narrowed:
- transport into the generation request: observed;
- identity-conditioned rendering: NOT proven;
- per-reference binding to a specific subject: NOT proven;
- canonical character preservation: FAILED.

A mount receipt is not a Character QA receipt.

## Visual evidence from rejected raster

### Systemic defects
1. **Identity contamination:** supplied visual identities are not reproduced faithfully; the model blends semantic traits into generic fantasy mascots.
2. **Reference-to-subject binding failure:** the generation operation provided a set of references, but there is no evidence each reference was explicitly bound to one named subject/slot.
3. **Ensemble overload:** asking for twelve distinct identities in one generation exceeds the demonstrated preservation reliability of the current path.
4. **Cross-character leakage:** gorilla/reptile/human/animal motifs recur or migrate across figures.
5. **Body-form reconstruction:** several principals are represented as newly invented bodies rather than current canonical silhouettes.
6. **Duplicate/extra-like figures:** the crowded compositions contain figures that cannot be certified as exactly one instance of each of the twelve.
7. **Generated labels create false confidence:** team-name labels under noncanonical figures make the raster appear mapped even when the pictured identity is wrong.
8. **Multi-page collapse:** four narrative beats were generated together, increasing subject count and repeated-character identity drift across panels.
9. **Text rendering distracted model capacity:** extensive titles, captions, scoreboard and speech balloons competed with identity preservation despite the packet's NO_TEXT_IN_ART rule.
10. **No per-character crop acceptance before ensemble use:** the pipeline jumped from mount to 12-person generation without proving each reference could survive a controlled single-subject or low-cardinality render.

## Specific canon failures visible enough to certify
- **TDS:** canonical requirement is one body with three serpent heads. Raster repeatedly shows a single ordinary reptile/crocodilian head/body. FAIL.
- **ObiWan Jacoby:** supplied Trade Jedi identity is not reliably preserved; generic human/Jedi-like figures cannot be certified as Jake's canonical character. FAIL. No-belt rule alone is insufficient.
- **D0nkey K0ng:** gorilla motif appears, but canonical Arsenal Gorilla Warrior identity is not faithfully preserved; generic gorilla reconstruction is not a pass. FAIL.
- **His Majesty's Blood:** Belt Keeper identity is not reliably reproduced as the canonical supplied character. Generic human/royal/warrior-like figures do not qualify. FAIL.
- **Slob on my Dobb:** current supplied identity is not faithfully preserved; generated large human/club-comedy figures cannot be mapped with confidence. FAIL.
- **Seven Deadly Chins:** current supplied identity is not faithfully preserved; generic large human figures are insufficient. FAIL.
- **Red Leopards:** generated red feline/leopard cues are semantic reconstruction rather than proof of the supplied canonical identity. FAIL.
- **Mud Dogs:** generic dog/mascot-like reconstruction is not a certified match to the supplied character. FAIL.
- **The LLC:** Page 3 golfer is a generic suited animal/human-like corporate golfer rather than a certified current LLC identity. FAIL.
- **El Niño:** cloud-headed work-call figure is a semantic weather-personification reconstruction; it cannot be certified as the current approved reference identity. FAIL.
- **Chili Cheesers:** cowboy/red/chili cues appear, but the exact Chili Outlaw identity is not faithfully locked. FAIL.
- **Dr. Duckhook:** duck-golfer semantics are strong, but the raster still reconstructs a generic cartoon duck rather than proving exact canonical Duckhook preservation. FAIL.

Result: **0/12 characters receive Character QA PASS from this raster.** Some have recognizable semantics, but semantic recognizability is explicitly not the acceptance criterion.

## Root cause
Primary root cause is **reference presence being mistaken for reference control**.

The current generation interface can receive references, but the pipeline has not demonstrated:
REFERENCE ID → OWNER/CHARACTER ID → SUBJECT SLOT → BODY/FACE/FORM LOCK → OUTPUT INSTANCE → CROP QA.

Without that binding, a twelve-reference prompt behaves like a mood/reference pool. The model may borrow traits without preserving identities.

Secondary causes:
- 12-subject cardinality in a single pass;
- four scenes in one raster;
- generated typography;
- no staged compositing;
- no per-subject identity confidence gate;
- no deterministic subject placement layer.

## Corrective architecture — mandatory before another 12-character attempt

### Gate C1 — Reference binding proof
For each of 12:
canonical file/hash → character ID → explicit subject slot → one controlled identity-preservation test.
PASS requires the rendered subject to be visually certifiable against the supplied reference. Semantic resemblance is FAIL.

### Gate C2 — Low-cardinality tests
Do not jump directly to 12.
Test:
1 subject → 2 interacting subjects → 3-4 subjects.
At each stage run crop-level Character QA. If identity degrades, stop and use compositing rather than adding subjects.

### Gate C3 — Character cutout / layer strategy
If renderer cannot preserve multiple identities simultaneously, generate or extract each canonical principal as a controlled transparent/isolatable layer, then compose into the Country Club scene. Environment and characters become separate production assets.

### Gate C4 — Deterministic ensemble manifest
Before Page 1 render, declare exactly 12 slots:
slot ID, character ID, source hash, position, scale, occlusion budget, required visible identity markers, prohibited mutations.
No unregistered thirteenth figure; no duplicate character.

### Gate C5 — No text in generative art
All narration, dialogue, labels and scoreboard are deterministic post-generation typography. The image renderer receives no request to spell editorial copy.

### Gate C6 — Scene cardinality
One page = one scene = one generation/composite target. Never ask the renderer to create all four pages at once.

### Gate C7 — Crop audit
After composition, produce 12 labeled QA crops. Character Control compares each crop against its canonical reference. 12/12 PASS is mandatory before Story/World polish can lock.

## Pipeline change
OLD:
12 refs → prompt → ensemble raster → inspect

REQUIRED:
12 canonical refs
→ per-ref binding tests
→ 12/12 identity proof
→ low-cardinality interaction tests
→ decide native ensemble vs compositing
→ deterministic 12-slot ensemble manifest
→ Country Club environment plate
→ character layers / controlled groups
→ composition
→ 12 crop audit
→ Character QA 12/12
→ World QA
→ Story QA
→ deterministic typography
→ mobile QA
→ Page Lock

## Release ruling
- first renderer proof: REJECTED
- Character QA: 0/12 PASS
- art generation: STOPPED pending C1
- no prompt-only retry authorized
- no “close enough” semantic mascot accepted
- R4 transport progress remains valid, but it does not satisfy character control
- V5.6 Gate 8 remains BLOCKED

## Next checkpoint
Execute C1 Reference Binding Proof for the twelve characters individually. Do not produce another Country Club ensemble until individual identity preservation has been demonstrated or the pipeline formally switches to deterministic compositing.
