# SCHEMIN ’26 — WEEKLY MEMO GOLD-STANDARD PRODUCTION MANUAL

**Version:** 4.0 — Week 2 Quality Standard  
**Status:** Authoritative production runbook for premium weekly issues  
**Applies to:** Pro Schemin’ Football League weekly memo production  
**League:** ESPN 1417621  
**Benchmark:** Approved 2026 Week 2 illustrated memo  
**Primary publishing reality:** phone-first, full-page illustrated magazine PDF

---

# 0. Why this manual exists

This document records the **actual production method that produced the approved Week 2 memo quality**.

It does not replace the existing Weekly Memo Playbook. It upgrades it.

The Week 1 Playbook established the core doctrine correctly: accuracy before entertainment, layout as editorial communication, artwork that tells a story, receipts for claims, and rendered-page QA rather than trusting source files. The Week 2 production cycle then exposed where those principles were still too abstract. Character identity drifted, utility pages occasionally looked disconnected from the issue, factual fields had to be corrected late, and the strongest pages emerged only after Jake supplied personal league context and the production moved **page by page** rather than as a blind batch.

The approved Week 2 issue was therefore created by four layers working together:

1. **Weekly Memo OS** — sequencing, evidence, recurring departments, and release gates.
2. **Specialist subagents / production roles** — source lock, stats, story, continuity, art, design, QA.
3. **Jake as Commissioner-Editor** — league lore, inside jokes, personal context, taste, corrections, and final creative judgment.
4. **ChatGPT orchestration** — research synthesis, story architecture, prompt engineering, creative translation, revision, defect diagnosis, and PDF assembly.

The repeatable production model is:

```text
SYSTEM
  ↓
VERIFIED LEAGUE EVIDENCE
  ↓
EDITORIAL INTERPRETATION
  ↓
COMMISSIONER CONTEXT
  ↓
CHATGPT SYNTHESIS
  ↓
PAGE CONCEPT
  ↓
PAGE GENERATION
  ↓
HUMAN VISUAL REVIEW
  ↓
CORRECTION / REGENERATION
  ↓
FINAL ASSET LOCK
  ↓
PDF ASSEMBLY
  ↓
INDEPENDENT AUDIT
  ↓
RELEASE
```

The goal is **not autonomous content generation**. The goal is a repeatable editorial studio where automation handles mechanics, specialist agents protect quality, ChatGPT synthesizes the moving parts, and human context makes the publication unmistakably Pro Schemin’.

---

# 1. Definition of gold-standard Schemin’ quality

A Pro Schemin’ weekly memo is not a standings report with decorative artwork.

It is a **fictional sports publication built from real fantasy-football evidence**.

The reader should immediately recognize:

- the actual matchup;
- the real score;
- the correct team/franchise identity;
- the established character;
- the league-specific joke;
- the football mechanism;
- the ongoing season arc;
- the same visual world from page to page.

A strong page rewards a league member who already knows the score.

It should still give them at least one of the following:

- a better understanding of why the result mattered;
- a sharper read of the league state;
- a genuinely earned joke;
- a continuity payoff from prior weeks;
- an image worth screenshotting and sharing.

## Core editorial test

> Could these team names be swapped for two random fantasy teams without changing the page?

If yes, the page is too generic.

## Core visual test

> If every word disappeared, would the illustration still communicate who these characters are and what happened?

If no, the art is decorative rather than editorial.

## Core production test

> Does the final rendered PDF look and read correctly on a phone?

If not, the source files do not matter.

---

# 2. Two valid production modes

Week 2 proved that the memo needs two distinct production paths.

## Mode A — Modular Editorial Mode

Separate components are built and assembled conventionally:

```text
approved art
+ live typography
+ verified tables/data
+ designed layout
= final page
```

Use Mode A when:

- data density is high;
- exact selectable text matters;
- a page is likely to receive late factual changes;
- tables must remain easy to patch;
- generated typography would create unacceptable risk.

Best candidates:

- dense standings pages;
- schedule tables;
- transaction ledgers;
- highly numerical appendices.

### Strengths

- easiest to correct;
- best factual control;
- best for live/selectable text.

### Risks

- can look like PowerPoint;
- can drift toward SaaS/dashboard aesthetics;
- can feel visually disconnected from the illustrated features.

---

## Mode B — Premium Illustrated Page Mode

The page is conceived as a **single editorial composition**:

```text
story
+ characters
+ environment
+ props
+ typography hierarchy
+ narration zone
+ jokes
+ physical receipts
= one integrated magazine page
```

This is the quality mode that ultimately defined the approved Week 2 issue.

Use Mode B by default for:

- cover;
- Opening Drive;
- matchup features;
- Power Rankings when the ranking board is visually embedded in the world;
- Pittsy’s Book;
- State of Play;
- Waiver Wire;
- Final Word;
- any recurring department that benefits from a physical in-world environment.

### Why Mode B worked

The strongest Week 2 pages did not look like illustrations pasted into a report.

They looked like pages that **existed inside the Pro Schemin’ universe**.

Successful examples included:

- the Red Leopards / Sonic “Special Delivery” world;
- Mud Dogs riding a bicycle through the swamp;
- D0nkey’s Arsenal-themed barbershop;
- the Country Club of Jackson;
- El Niño’s storm-service counter;
- Chins wrecking LLC’s boardroom;
- the commissioner office;
- the sportsbook ledger;
- the evidence room;
- the waiver transaction desk.

### Mode B risk

Integrated generated typography can introduce spelling, score, record, or label errors.

Therefore:

> A beautiful generated page receives **more QA**, not less.

---

# 3. Production roles and domain authority

The memo is not operated by one generic assistant.

Each domain has an owner and veto power.

| Role | Primary authority | May block release? |
|---|---|---:|
| Executive Producer | scope, sequencing, issue architecture, final production state | Yes |
| Source Lock / League Intelligence | scores, records, rosters, schedule, transactions | Yes |
| Statistics Desk | margins, ranks, averages, deltas, derived metrics | Yes |
| Narrative Editor / The Booth | story cards, issue thesis, narration, continuity | Yes |
| Character Librarian | canonical characters, rebrands, franchise continuity | Yes |
| Narrative Art Director | scene concept, visual action, page-world storytelling | Yes |
| Prompt / Generation Operator | executes page/image generation | No self-certification |
| Editorial Designer | hierarchy, composition, issue-level visual rhythm | Yes |
| Mobile UI/UX QA | phone readability and reading path | Yes |
| Copy / Fact QA | names, numbers, repetition, factual text | Yes |
| Independent Release Auditor | final artifact review only | Yes |
| Jake / Commissioner-Editor | league culture, personal context, taste, final creative judgment | Absolute creative veto |

## Separation rule

The same production role may contribute to multiple stages, but the agent/system that **creates** a page may not be the only authority that **certifies** it.

Producer confidence is not QA.

---

# 4. Source hierarchy

The humor may be exaggerated.

The facts may not be.

## Tier 1 — Canonical fantasy-league evidence

Preferred order:

1. ESPN Fantasy API for league `1417621` when accessible.
2. Direct ESPN screenshots supplied by Jake.
3. Validated league schedule documents.
4. League exports or other verified platform records.

Use for:

- final scores;
- records;
- standings;
- rosters;
- schedule;
- transactions;
- ownership;
- lineup data;
- projections when explicitly available.

## Tier 2 — User-supplied league receipts

Examples:

- Pittsy’s Book settlement messages;
- side-bet ledgers;
- waiver screenshots;
- trade confirmations;
- owner-to-owner events;
- commissioner notes;
- league-chat incidents.

These are legitimate primary inputs for editorial storytelling when supplied by Jake.

## Tier 3 — NFL context

Use official/current NFL reporting when it materially explains:

- a fantasy outcome;
- injury-driven waiver urgency;
- a lineup decision;
- role/opportunity change;
- a player’s Week 3 outlook.

NFL news is not filler.

## Tier 4 — Editorial interpretation

Examples:

- “the model finally got a receipt”;
- “the rebellion was complicated”;
- “Mud Dogs keeps winning ugly.”

These are conclusions, not raw facts.

## Tier 5 — Joke / league lore

Examples:

- Sonic chili dogs;
- Country Club of Jackson;
- barbershop humiliation;
- commissioner sayings;
- recurring character props.

These can be stylized, but they must still connect to recognizable league culture.

---

# 5. Fact-state protocol

Every material claim begins in one of four states:

```text
VERIFIED
DERIVED
EDITORIAL
UNVERIFIED
```

### VERIFIED
Directly supported by a trusted source.

### DERIVED
Mathematically calculated from verified facts.

Examples:
- scoring margin;
- two-week points;
- average;
- median;
- week-over-week delta.

### EDITORIAL
Interpretive language based on the evidence.

### UNVERIFIED
Not safe for publication as fact.

Unverified information does not become “close enough” because the page looks good.

---

# 6. Weekly intake package

The issue begins when the fantasy week closes.

The Source Lock team collects the following.

## A. Final results

- six final matchup scores;
- winners and losers;
- margin;
- post-week records;
- divisions.

## B. Player evidence

- displayed top performers;
- key starter contributions;
- injury context where relevant;
- significant bench/start decisions only when verified.

## C. League state

- standings;
- total points;
- division ordering;
- undefeated teams;
- winless teams;
- Week 1 → current-week movement.

## D. Market activity

- waiver claims;
- FAAB;
- failed claims;
- drops;
- trades;
- roster churn.

## E. Pittsy’s Book

- posted lines;
- final results;
- player ledger;
- house P/L;
- special parlays or markets.

## F. Forward state

- next week’s exact matchups;
- relevant divisional stakes;
- rivalry/history context.

## G. Commissioner context

This is the information the platform cannot know:

- owner interactions;
- gifts/stunts;
- shared clubs/locations;
- off-platform trash talk;
- league-chat moments;
- personal history;
- exact comedic angle;
- cultural references;
- pages Jake wants emphasized or removed.

This category is not optional.

---

# 7. Commissioner Context Pass

The best Week 2 pages became strong only after Jake supplied context that did not exist in ESPN data.

Examples from the approved cycle:

- Chili delivered Sonic chili dogs to Red before the Game of the Week.
- Mud Dogs should humiliate ObiWan in the swamp while riding a bicycle.
- D0nkey should shave TDS’s dreads in an Arsenal barbershop.
- Slob and Duckhook share Country Club of Jackson.
- El Niño / Thst’s Fantasy should use a recognizable sitcom-style denial gag.
- Seven Deadly Chins should physically destabilize LLC’s polished business world.
- the cover should feature **Red Leopards alone**, while the matchup page shows both characters.
- QB injuries should become the Waiver Wire page’s central visual mechanism.

These directions are not ad hoc chatter.

They are formal editorial inputs.

## Standard Commissioner Context form

```text
PAGE / MATCHUP:
REAL-WORLD CONTEXT:
INSIDE JOKE:
OWNER RELATIONSHIP:
VISUAL REQUEST:
TONE:
MUST INCLUDE:
MUST NOT INCLUDE:
```

ChatGPT is responsible for translating conversational input into this structure.

---

# 8. Issue thesis and Story Budget

Do not write six independent recaps and hope they form an issue.

First determine what the week means.

Week 2 eventually worked because the editorial frame became:

> Week 1 made claims. Week 2 started a correction file.

That allowed recurring issue language such as:

- evidence;
- receipts;
- correction;
- second data point;
- reputation;
- pressure.

## Issue Story Budget

Before writing pages, assign the editorial jobs:

- Cover story
- Opening Drive
- Scoreboard / standings orientation
- Power Rankings
- Pittsy’s Book
- League-wide analytical synthesis
- six matchup stories
- waiver/transaction story
- Final Word

No two pages should have the same editorial job.

---

# 9. Matchup Story Engine

Every matchup must reduce to:

```text
SCENE
→ TENSION
→ MECHANISM
→ TURN
→ CONSEQUENCE
```

## Example — Red vs Chili

**Scene:** Chili sends dinner to Red before kickoff.

**Tension:** Week 1’s 198-point darling vs the preseason/model doubt.

**Mechanism:** Red produces 191.90 while Chili collapses to 100.90.

**Turn:** the taunt becomes Red’s physical receipt.

**Consequence:** Red owns the cover; the food delivery becomes league folklore.

If a matchup cannot answer all five stages, it is not ready for art.

---

# 10. Story Card contract

Create a Story Card before generating each matchup feature.

Required fields:

- matchup;
- final score;
- records;
- division;
- Week 1 prior;
- opening scene;
- tension;
- fantasy mechanism;
- relevant NFL mechanism;
- turning point;
- consequence;
- Commissioner Context;
- humor lane;
- Week 3 hook;
- headline options;
- exact characters;
- visual action;
- emotional state of both characters;
- environment;
- props;
- facts requiring QA;
- prohibited visual substitutions.

The Story Card is the bridge between evidence and art.

---

# 11. Character canon

Character continuity is franchise continuity.

A team can change names.

The character does not automatically change.

## Current 12-team visual canon

### ObiWan Jacoby
- blond human Trade Jedi;
- tan/brown robe language;
- green lightsaber;
- golden retriever companion;
- intelligent/trader identity.

### Mud Dogs
- grotesque blue/orange swamp-dog monster;
- muddy/diseased appearance;
- chains;
- oversized feral silhouette;
- never a normal household dog.

### D0nkey K0ng
- same established character as former Baker Moore Purdy;
- horse-headed centaur warrior;
- Arsenal-red football identity;
- cigar/axe/beer language;
- never a gorilla.

### Three Dreaded Snake
- reptilian snake humanoid;
- dark dreadlocks;
- green/black football styling;
- jungle/rebellion identity.

### Slob on my Dobb
- huge human redneck/frat-bro berserker;
- heavy build;
- beer;
- bat/golf-club chaos when appropriate;
- Beerus dog companion.

### Dr. Duckhook
- anthropomorphic white duck golfer;
- floral/loud golf styling;
- bucket hat;
- cigar;
- golf-driver/prosthetic-arm language.

### Red Leopards
- giant red leopard predator warrior;
- black spots;
- ancient/royal armor;
- amber predator eyes;
- hunter identity.

### Chili Cheesers
- Brandon Pryor / Chili Outlaw;
- human cowboy;
- black hat;
- dark glasses;
- beard;
- red western/chili ammunition styling;
- Dark Horse continuity when useful.

### El Niño
- humanoid storm/water elemental;
- glowing blue energy;
- lightning;
- wave/storm motifs;
- staff/surf/weather language.

### Thst’s Fantasy
- same character as former The Immortal;
- Austin Byars / Belt Keeper;
- pale human gothic champion;
- black armor;
- glowing eyes;
- runic sword;
- championship belt.

### Seven Deadly Chins
- very heavy blue-collar/redneck human;
- dirty tank;
- cap;
- 40 oz beer;
- sledgehammer;
- BBQ/truck-stop world.

### The LLC
- human corporate mob boss;
- expensive dark suit;
- sunglasses;
- cigar;
- gold watch;
- LLC briefcase.

---

# 12. Character Packets

Every art prompt should attach a compact Character Packet.

```text
TEAM:
CURRENT NAME:
LEGACY NAME:
CANONICAL IMAGE:
FORM:
FACE / SPECIES:
BODY:
WARDROBE:
SIGNATURE PROP:
PALETTE:
WORLD:
MUST KEEP:
DO NOT:
```

The image reference is authoritative.

Text description supports it.

Text description does not override it.

## Character QA failure conditions

A page automatically fails if:

- species changes;
- human becomes animal or vice versa;
- signature silhouette disappears;
- rebrand creates a new character;
- costume/prop identity is materially lost;
- the character becomes a generic mascot;
- the focal character is too small to recognize;
- a matchup feature fails to show both required characters.

Cover exception:

A cover may intentionally feature only one character when the cover thesis calls for one protagonist.

---

# 13. Approved Week 2 page architecture

The final high-performing structure became:

1. **Cover**
2. **Opening Drive**
3. **Week 2 Scoreboard / Standings**
4. **Power Rankings**
5. **Pittsy’s Book**
6. **State of Play / Evidence / Week 3 bridge**
7. **Red Leopards vs Chili Cheesers**
8. **Mud Dogs vs ObiWan Jacoby**
9. **D0nkey K0ng vs Three Dreaded Snake**
10. **Slob on my Dobb vs Dr. Duckhook**
11. **El Niño vs Thst’s Fantasy**
12. **Seven Deadly Chins vs The LLC**
13. **Waiver Wire / Transaction Desk**
14. **Final Word**

This is a proven rhythm, not a permanent mandate.

The governing rule is:

> The issue gets as many pages as the stories require, but every page must have a distinct job.

---

# 14. Cover standard

The cover carries one clear thesis.

## Hierarchy

1. publication identity;
2. primary character;
3. dominant cover headline;
4. one supporting line;
5. one unmistakable visual receipt;
6. restrained footer/league branding.

## Cover lesson from Week 2

The issue improved when Red Leopards appeared alone as the protagonist.

The matchup page then continued the story with Red **and** Chili.

This establishes a repeatable device:

```text
COVER = protagonist / symbol / thesis
MATCHUP FEATURE = full conflict / both characters / explanation
```

Do not force all participants onto the cover when one protagonist better carries the issue.

---

# 15. Premium Illustrated Page Mode — visual doctrine

## Core visual world

Use recurring physical materials and environments:

- parchment;
- dark steel;
- brass;
- leather;
- dark wood;
- deep burgundy;
- red accents;
- gold hardware;
- warm practical light;
- smoke;
- rain;
- mud;
- receipts;
- ledgers;
- books;
- chalkboards;
- banners;
- framed physical scoreboards.

The publication should feel tactile and lived-in.

## Avoid

- generic PowerPoint geometry;
- white SaaS interfaces;
- floating app cards;
- flat infographic dashboards;
- repeated black backgrounds with no worldbuilding;
- generic stadium wallpaper;
- tiny character cameos;
- pasted mascot portraits;
- the same matchup layout six times.

## Composition

Default to portrait full page.

Recommended balance:

- 50–70% visual action/world;
- 20–35% editorial headline/narration zone;
- 5–15% metadata, quote, folio, small jokes.

Negative space must be intentional.

Never put body copy across the best facial expression or decisive action.

---

# 16. Embedded typography in Premium Illustrated Page Mode

Week 2 proved that page-level generation can deliver a more unified result than modular layout for this project.

Therefore generated/embedded typography is allowed in Premium Illustrated Page Mode.

It creates additional QA obligations.

## Required text inspection

Check every visible:

- team name;
- score;
- record;
- player name;
- division label;
- headline;
- quote;
- page folio;
- table value;
- betting amount;
- FAAB amount;
- next-week matchup.

Also inspect for:

- invented words;
- malformed logos;
- incorrect jersey text;
- accidental substitutions.

## Fix rule

**Patch** when:
- error is isolated;
- the typography can be corrected without looking pasted-on.

**Regenerate** when:
- the error is central;
- several fields are wrong;
- the headline is malformed;
- the visual hierarchy is broken;
- a character is wrong.

---

# 17. Matchup page contract

Every matchup page must lock the following before generation.

## Data

- both team names;
- final score;
- division;
- current records when shown.

## Headline

Short, visual, physical, joke-compatible.

Week 2 examples:

- SPECIAL DELIVERY
- TAKEN FOR A RIDE
- OFF THE TOP
- MEMBERS ONLY
- NO WIN FOR YOU
- HOSTILE TAKEOVER

These work because they function as both a visual scene and a football conclusion.

## Narration

Target roughly 85–160 words.

The text must answer:

1. what happened;
2. what caused it;
3. what changed;
4. why the league should care.

## Visual
- both canonical characters;
- one decisive action;
- readable emotion;
- one league-specific or owner-specific visual mechanism;
- 3–5 meaningful props;
- no unexplained extra hero character.

## Quote / handwritten line

Use one strong line, not five competing jokes.

## Explicit “do not” list

Every art brief needs matchup-specific prohibitions.

Example:

```text
DO NOT:
- turn D0nkey into a gorilla;
- turn Mud Dogs into a normal brown dog;
- replace Thst’s Belt Keeper with a generic king;
- crop either matchup character out of the visual story.
```

---

# 18. Utility-page design doctrine

The Week 2 cycle proved that utility pages can destroy visual continuity even when their information is correct.

Therefore every recurring department must occupy a physical location inside the same world.

## Scoreboard / Standings

World:
- league hall;
- brass standings board;
- commissioner desk;
- parchment result ledger.

Never paste raw ESPN UI into the publication.

## Power Rankings

World:
- engraved ranking board;
- physical plaques;
- league office/hall;
- canonical miniature character portraits.

Important:

> Wrong character art in a ranking row is a blocking Character QA failure.

## Pittsy’s Book

World:
- sportsbook counter;
- black ledger boards;
- betting receipts;
- whiskey;
- house notes;
- physical bookmaker environment.

Only use actual supplied betting outcomes.

## State of Play

World:
- evidence room;
- wall map;
- pinned cards;
- second-data-point board;
- Week 3 files.

Purpose:
- synthesis, not a second Scoreboard.

## Waiver Wire

World:
- transaction desk;
- claim window;
- emergency roster paperwork;
- bid slips;
- failed-claim receipts.

Week 2’s strongest angle:
- quarterback injuries created roster panic;
- TDS attacked the market;
- Chili bought Bryce Young;
- Thst’s missed both QB claims and pivoted.

Purpose:
- explain market behavior and urgency, not just list transactions.

## Final Word

World:
- commissioner office after hours;
- empty chair;
- physical remains of the issue;
- quieter lighting;
- Week 3 note waiting on the desk.

Purpose:
- close the week;
- do not repeat awards, rankings, or scoreboard content.

---

# 19. Page-at-a-time approval loop

The approved Week 2 quality was achieved **page by page**.

This is now formal production doctrine for high-identity pages.

```text
PAGE BRIEF
  ↓
GENERATE
  ↓
DISPLAY TO JAKE
  ↓
ACCEPT / CORRECT
  ↓
CHARACTER QA
  ↓
FACT QA
  ↓
PAGE LOCK
  ↓
NEXT PAGE
```

## Why batch approval failed

Batch generation amplifies wrong assumptions.

If the first art direction is wrong, the same error can infect:

- six matchup pages;
- utility-page design;
- character form;
- typography hierarchy.

A page-at-a-time loop gives the issue a live editorial feedback system.

---

# 20. What the production team owns vs what Jake owns

Jake should **not** have to catch:

- arithmetic;
- wrong standings;
- wrong records;
- wrong page numbers;
- obvious text overlap;
- wrong rename mapping;
- duplicated teams;
- generic character substitutions.

Those are production failures.

Jake’s highest-value input is:

- “this joke is funnier”;
- “the cover should only show Red”;
- “these owners belong to the same country club”;
- “this page is repetitive”;
- “this does not feel like our magazine”;
- “use the waiver panic as the illustration.”

That is Commissioner-Editor judgment.

---

# 21. ChatGPT’s role in the production system

ChatGPT sits between the OS, the subagents, the raw evidence, and Jake’s live creative direction.

It should perform five functions.

## 1. Orchestration

Translate the production request into:
- tasks;
- dependencies;
- gates;
- page order;
- QA ownership.

## 2. Synthesis

Combine:
- ESPN evidence;
- NFL context;
- Week 1 continuity;
- current standings;
- user context;
- league lore.

## 3. Creative translation

Turn Jake’s raw idea into an executable Page Brief.

Example:

“have Mud Dogs riding a bike and make ObiWan look stupid in the swamp”

becomes:

- exact Mud Dogs character;
- exact ObiWan character;
- low-angle bicycle chase;
- ObiWan stuck/slipping in swamp;
- dog companion reacting;
- humorous humiliation;
- protected narration zone;
- no generic dog replacement.

## 4. Defect diagnosis

When a page fails, identify whether the problem is:
- source;
- story;
- character;
- art;
- typography;
- layout;
- duplication;
- issue-level rhythm.

## 5. Artifact production

After assets are locked:
- build the manifest;
- assemble the PDF;
- preserve aspect ratio;
- inspect output;
- produce the release package.

---

# 22. Error taxonomy

## A. Factual defect

Examples:
- wrong score;
- wrong standings;
- wrong Week 3 opponent;
- bad derived margin.

Response:
- patch if isolated and visually safe;
- rebuild if the fact drives the page.

## B. Character defect

Examples:
- Mud Dogs becomes a normal dog;
- D0nkey becomes a gorilla;
- Thst’s becomes a generic king;
- LLC becomes a logo-headed mascot.

Response:
- regenerate.

Character failures are rarely patchable.

## C. Narrative defect

Examples:
- page is mostly score restatement;
- repeats State of Play;
- joke could fit any team;
- causality is invented.

Response:
- rewrite Story Card before regenerating.

## D. Editorial-design defect

Examples:
- Power Rankings looks like SaaS;
- scoreboard feels like a dashboard;
- body copy covers characters;
- page has no visual world.

Response:
- rebuild page architecture.

## E. Redundancy defect

Examples:
- awards page repeats Evidence Room;
- Week 3 preview repeats State of Play;
- six-matchup collage duplicates the six feature pages inside the same PDF.

Response:
- merge;
- delete;
- or move to social/supplemental asset.

## F. Generated-text defect

Examples:
- misspelling;
- malformed stat;
- wrong record;
- nonsense prop label.

Response:
- patch if small;
- regenerate if central.

---

# 23. Patch vs regenerate vs rebuild

## Patch

Use when:
- one number is wrong;
- folio is wrong;
- small board label needs correction;
- a single table field changed.

## Regenerate

Use when:
- character is wrong;
- emotional relationship is wrong;
- scene does not communicate the result;
- headline typography breaks;
- too many embedded-text errors exist.

## Rebuild from Story Card

Use when:
- the concept is generic;
- the page duplicates another page’s job;
- art and narration repeat each other;
- the page has no reason to exist.

---

# 24. Narrative anti-duplication rule

Every page must perform a unique editorial function.

The same fact may appear more than once only when its function changes.

Example:

- Scoreboard: `Red 191.90 — Chili 100.90`
- Matchup page: the Sonic stunt, football mechanism, and reversal.
- State of Play: Red as evidence of league-wide volatility.
- Final Word: do **not** repeat the score again.

Before release ask:

> If this page disappeared, what unique information, joke, or feeling would the reader lose?

If the answer is “nothing,” the page is redundant.

---

# 25. Asset Manifest

Approved assets must be explicitly named and locked.

Example:

```text
01_COVER_APPROVED.png
02_OPENING_DRIVE_APPROVED.png
03_SCOREBOARD_APPROVED.png
04_POWER_RANKINGS_APPROVED.png
05_PITTSYS_BOOK_APPROVED.png
06_STATE_OF_PLAY_APPROVED.png
07_RED_CHILI_APPROVED.png
08_MUD_OBIWAN_APPROVED.png
09_DONKEY_TDS_APPROVED.png
10_SLOB_DUCKHOOK_APPROVED.png
11_ELNINO_THSTS_APPROVED.png
12_CHINS_LLC_APPROVED.png
13_WAIVER_WIRE_APPROVED.png
14_FINAL_WORD_APPROVED.png
```

When a page is replaced:

```text
old → REJECTED
new → APPROVED
```

Do not assemble from “whatever file looks newest.”

---

# 26. Final PDF assembly

Only approved page assets enter the issue.

## Requirements

- preserve original page ratio;
- no crop;
- no stretch;
- no auto-fit clipping;
- no duplicate pages;
- use manifest order;
- keep social/Instagram collages outside the memo unless intentionally assigned a page role.

The final PDF must be generated from the exact approved page images.

---

# 27. Full release audit

The artifact under review is the **final PDF**.

Not the source images.

Not the prompts.

Not the producer’s description.

## Audit 1 — factual

Verify every visible:

- score;
- record;
- team name;
- player name;
- margin;
- ranking;
- FAAB bid;
- Pittsy amount;
- schedule matchup;
- rebrand.

## Audit 2 — character

Inspect every appearance, including small utility-page portraits.

Pay special attention to:

- Power Rankings;
- scoreboard icons;
- waiver-page cameos;
- evidence-room miniatures.

Small placements are where character drift hides.

## Audit 3 — visual rhythm

Review the issue as a 14-page sequence.

Check:

- repetitive layouts;
- abrupt visual-style shifts;
- excessive black or parchment;
- utility pages that feel separate from the matchup pages;
- whether action pages and quieter pages alternate effectively.

## Audit 4 — phone width

Review each page at approximately a 390px viewport.

Ask:

- is the headline instantly legible?
- can the score be found quickly?
- is the narration readable?
- are characters recognizable?
- does the page still feel intentional?

## Audit 5 — duplication

Search for:

- repeated facts;
- repeated jokes;
- repeated taglines;
- two pages serving the same function.

## Audit 6 — pagination

Check visible page numbers and sequence.

---

# 28. Independent Release Auditor

The Release Auditor should receive only:

- final PDF;
- Fact Lock;
- Character Manifest;
- acceptance checklist.

The reviewer should not receive the producer’s argument for why the issue should pass.

Allowed decisions:

```text
PASS
PASS WITH NON-BLOCKING NOTES
FAIL — CORRECTION REQUIRED
```

Any blocking defect returns to its owning department.

---

# 29. Release definition

The issue is complete only when:

- all pages are individually approved;
- all critical factual errors are resolved;
- character continuity passes;
- page order passes;
- no critical crop/overlap issue remains;
- no major redundancy remains;
- the final PDF opens correctly;
- the exact saved PDF is the PDF that passed audit.

A PDF existing is not completion.

---

# 30. Permanent Week 2 lessons

## Lesson 1 — Character continuity must be blocking

A good scene with the wrong character is not a good page.

**Permanent change:** Character Librarian has veto authority.

## Lesson 2 — Full-page story composition beats generic image + text panel

The early landscape-art approach weakened the magazine.

**Permanent change:** flagship matchup pages use portrait, full-page story compositions.

## Lesson 3 — Utility pages need art direction too

Correct information can still break the issue if it looks like a dashboard.

**Permanent change:** every recurring department lives inside a physical editorial world.

## Lesson 4 — Personal context is a production input

The best visual concepts came from owner-specific information.

**Permanent change:** Commissioner Context Pass occurs before creative lock.

## Lesson 5 — Batch production is risky for identity-heavy pages

Wrong assumptions replicate quickly.

**Permanent change:** flagship pages are generated and approved one at a time.

## Lesson 6 — More pages does not mean more value

Several planned pages became repetitive.

**Permanent change:** merge or delete duplicate editorial functions.

## Lesson 7 — Premium Illustrated Page Mode is now legitimate

The successful Week 2 pages integrated image, typography, props, narration, and worldbuilding.

**Permanent change:** Mode B is officially supported, with stricter post-generation QA.

---

# 31. Weekly production cadence

## Tuesday night — close the football week

- final score intake;
- results reconciliation;
- standings update;
- Pittsy settlement;
- first story hypotheses.

## Wednesday morning — market reaction

- waiver results;
- FAAB;
- failed bids;
- injury fallout;
- transactions;
- Week 3 schedule confirmation.

## Wednesday production block

- final Fact Lock;
- Commissioner Context Pass;
- issue thesis;
- Story Cards;
- page architecture;
- page-at-a-time production.

## Wednesday release block

- Asset Manifest;
- PDF assembly;
- rendered audit;
- corrections;
- reassembly;
- release audit;
- publication.

The exact clock can move.

The dependency order should not.

---

# 32. Golden-path workflow

```text
01. INTAKE
02. SOURCE LOCK
03. FACT LOCK
04. COMMISSIONER CONTEXT PASS
05. ISSUE THESIS
06. STORY BUDGET
07. SIX STORY CARDS
08. PAGE ARCHITECTURE
09. CHARACTER PACKETS
10. PAGE BRIEFS
11. GENERATE ONE PAGE
12. USER REVIEW
13. CHARACTER QA
14. FACT QA
15. LOCK PAGE
16. REPEAT UNTIL ISSUE COMPLETE
17. UTILITY-PAGE VISUAL HARMONIZATION
18. ASSET MANIFEST
19. PDF ASSEMBLY
20. FULL-ARTIFACT AUDIT
21. DEFECT LOG
22. FIX / REGENERATE / REBUILD
23. REASSEMBLE
24. INDEPENDENT RELEASE AUDIT
25. PUBLICATION
26. RETROSPECTIVE / OS UPDATE
```

No downstream stage may wave through an upstream blocking failure.

---

# 33. Weekly kickoff checklist

## Data

- [ ] six final scores
- [ ] records
- [ ] standings
- [ ] top performers
- [ ] next-week schedule
- [ ] waiver results
- [ ] FAAB
- [ ] failed claims
- [ ] Pittsy results
- [ ] relevant injuries
- [ ] team rename check

## Narrative

- [ ] issue thesis
- [ ] cover thesis
- [ ] six unique matchup theses
- [ ] league-wide analytical angle
- [ ] waiver/transaction angle
- [ ] no unsupported causal claims
- [ ] no duplicate page purpose

## Commissioner context

- [ ] owner jokes
- [ ] real-world gestures
- [ ] shared history/locations
- [ ] requested cultural references
- [ ] exact visual must-haves
- [ ] exact visual prohibitions

## Art

- [ ] exact character refs
- [ ] page concept
- [ ] decisive action
- [ ] readable emotion
- [ ] props
- [ ] typography hierarchy
- [ ] safe narration zone
- [ ] phone-readable composition

## QA

- [ ] scores
- [ ] records
- [ ] names
- [ ] schedule
- [ ] character continuity
- [ ] page number
- [ ] visual rhythm
- [ ] duplication
- [ ] phone width
- [ ] final PDF review
- [ ] independent release signoff

---

# 34. Reusable Story Card template

```markdown
# MATCHUP STORY CARD

## Matchup
TEAM A vs TEAM B

## Final
TEAM A XX.XX — TEAM B XX.XX

## Records
A:
B:

## Week 1 prior

## Scene

## Tension

## Fantasy mechanism

## Relevant NFL mechanism

## Turn

## Consequence

## Commissioner context

## Humor lane

## Headline options

## Exact character references

## Character A action

## Character B action

## Emotional read

## Environment

## Props

## Narration facts requiring QA

## Do not
```

---

# 35. Reusable Page Brief template

```markdown
# PAGE BRIEF

PAGE:
ROLE IN ISSUE:
MODE: Modular / Premium Illustrated

EDITORIAL JOB:
ONE-SENTENCE THESIS:

HEADLINE:
SUBHEAD:
SCORE / RECORD LINE:

NARRATION:
[final copy or copy budget]

CANONICAL CHARACTERS:
[references]

DECISIVE VISUAL MOMENT:

COMPOSITION:
- top:
- left:
- right:
- bottom:
- protected copy zone:

PROPS:
1.
2.
3.

VISUAL WORLD:
LIGHTING:
TEXTURE:
PALETTE:

MUST INCLUDE:
MUST NOT INCLUDE:

FACTS TO VERIFY:
CHARACTER QA:
MOBILE QA:
```

---

# 36. Reusable defect ledger

```markdown
| Page | Defect | Type | Severity | Owner | Fix | Reaudit |
|---|---|---|---|---|---|---|
| 04 | Wrong character portrait | Character | BLOCKING | Character / Art | regenerate | pending |
| 06 | Wrong record | Fact | BLOCKING | Data / Design | patch | pending |
| 13 | Copy too small | Mobile UX | BLOCKING | Design | rebuild | pending |
```

No blocking defect may remain open at release.

---

# 37. Master weekly kickoff prompt

Use this at the beginning of each future memo cycle:

> Activate the full Schemin ’26 Weekly Memo production system in **Gold-Standard Illustrated Page Mode**.
>
> Use the current `SCHEMIN_26_WEEKLY_MEMO_GOLD_STANDARD_PRODUCTION_MANUAL.md` as controlling doctrine, together with the canonical character references, current league evidence, and this week’s Commissioner Context.
>
> Begin with Source Lock and Fact Lock. Do not write around missing data.
>
> Then produce:
> 1. issue thesis;
> 2. cover story;
> 3. Story Budget;
> 4. six matchup Story Cards;
> 5. proposed page architecture;
> 6. Character Packets;
> 7. page briefs.
>
> Incorporate Jake’s personal league context as a formal Commissioner Context Pass before creative lock.
>
> For flagship pages, work **one page at a time**:
>
> `BRIEF → GENERATE → DISPLAY → REVIEW → CORRECT → QA → LOCK → NEXT PAGE`
>
> Default visual standard:
> - premium full-page portrait magazine composition;
> - tactile Pro Schemin’ world;
> - parchment / black / red / gold hierarchy;
> - cinematic practical-feeling environments;
> - exact canonical characters;
> - owner-specific visual jokes;
> - phone-first readability;
> - art and narration that complement rather than repeat each other.
>
> Utility pages must remain inside the same physical editorial world and must not collapse into generic dashboards.
>
> Treat ESPN league evidence and verified screenshots as factual authority. Never fabricate unavailable results, transactions, schedule fields, or betting records.
>
> Character continuity is blocking. A rename never creates a new character.
>
> The producing system may not self-certify release.
>
> Once all pages are individually approved, build the Asset Manifest, assemble the final PDF without crop/stretch, perform full fact/character/UI/duplication/mobile QA, log and fix defects, rerender, and submit the exact final PDF to an independent Release Audit.
>
> Do not declare completion because a draft or PDF exists.
>
> The assignment is complete only when the final rendered publication meets or exceeds the approved Week 2 quality floor.

---

# 38. Final doctrine

The Pro Schemin’ memo is strongest when the system does not try to remove people from the process.
The OS supplies discipline.

The subagents supply specialized expertise.

ChatGPT supplies synthesis, creative translation, and production leverage.

Jake supplies the league’s lived context and final taste.

The point is not to automate a newsletter.

The point is to operate a repeatable editorial studio that can turn one week of fantasy football into a piece of league culture.

That is the Week 2 quality standard.