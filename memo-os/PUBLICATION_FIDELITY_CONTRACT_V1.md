# Weekly Memo OS — Publication Fidelity Contract V1

**Status:** V5.6 RC REQUIRED GATE  
**Authority:** Weekly Memo OS / Independent Art + Publication QA  
**Benchmarks:** Official Week 2 Memo + Official Week 3 Memo

## Incident

The first V5.6 real Week 4 acceptance page proved technical wiring but did not meet the publication quality demonstrated by the official Week 2 and Week 3 releases.

Technical correctness is therefore insufficient for page acceptance.

A page may pass:
- fact provenance;
- character reference mounting;
- deterministic text;
- mobile legibility;
- artifact identity;

and still fail publication fidelity.

## Benchmark doctrine

Week 2 and Week 3 are not templates to clone. They define the quality floor and publication family.

Their recurring characteristics include:
- bespoke full-page illustrated composition;
- story-specific physical environments;
- characters at meaningful narrative scale;
- integrated editorial typography;
- environmental props and jokes carrying story information;
- page-specific visual grammar rather than a repeated generic card;
- foreground / midground / background depth;
- text and illustration designed together;
- strong visual hierarchy at phone scale;
- recurring league-world identity without flattening every page into the same layout.

## Required fidelity dimensions

Every flagship narrative page is independently scored PASS/FAIL on:

1. **Scene Specificity**
   - Would the composition still work if unrelated team names were substituted?
   - If yes, FAIL.

2. **Character Narrative Presence**
   - Required characters must participate in the story action, not exist as decorative cameos.

3. **Environmental Storytelling**
   - Location, props, weather, aftermath, receipts, jokes or historical callbacks must communicate story before body copy is read.

4. **Integrated Editorial Design**
   - Headline, dek, score/fact treatment and illustration must feel designed as one page.
   - Generic hero-image + lower-third/report-card composition fails flagship fidelity.

5. **Depth & Cinematic Construction**
   - Foreground, midground and background must carry intentional visual information where the concept permits.

6. **Page Archetype Diversity**
   - Matchup pages may share publication DNA but cannot repeat one template mechanically.

7. **Text / Image Complementarity**
   - Illustration and prose should add different information.
   - Art that merely decorates already-written copy fails.

8. **World Believability**
   - The scene must feel physically located inside the persistent Schemin universe.

9. **Benchmark Family Resemblance**
   - After originality-safe generation, compare against Week 2 and Week 3 for ambition, density, finish and editorial confidence.
   - Similarity of quality is required; similarity of exact composition is prohibited.

10. **390px Editorial Readability**
   - Major story, score/fact information and page hierarchy must survive phone scale without reducing the page to tiny report text.

## Auto-fail patterns

- generic black information panel under a hero image;
- dashboard/report/social-card composition for a flagship narrative page;
- isolated character portrait with story pasted beneath it;
- large dead zones without narrative purpose;
- typography treated as an afterthought;
- required opponent missing from a matchup feature unless the story concept explicitly justifies absence;
- visually interchangeable page after team-name substitution;
- page that requires body text to explain why the scene matters;
- technically legible but materially less ambitious than the benchmark publication family.

## Acceptance classes

A real page receives two separate outcomes:

### TECHNICAL_ACCEPTANCE
Fact/canon/world/reference/render/mobile plumbing.

### PUBLICATION_FIDELITY
Premium editorial/art/story quality.

Only:

`TECHNICAL_ACCEPTANCE = PASS`
AND
`PUBLICATION_FIDELITY = PASS`

may produce:

`REAL_PAGE_ACCEPTANCE = PASS`

## Week 4 first-page incident disposition

The initial ObiWan Week 4 acceptance page is reclassified:

- TECHNICAL_ACCEPTANCE: PASS
- PUBLICATION_FIDELITY: FAIL
- REAL_PAGE_ACCEPTANCE: FAIL

Reason:
The page demonstrates correct reference mounting, deterministic typography and 390px legibility, but its generic hero-image + lower information architecture is materially below the bespoke full-page illustrated publication standard established by Week 2 and Week 3.

It remains useful as a pipeline fixture and must not be deleted or retroactively misrepresented as publication-grade.

## Release rule

No V5.6 promotion until at least one real current-week page passes both technical and publication-fidelity gates and the controlled Week 2 reconstruction passes issue-level fidelity review.
