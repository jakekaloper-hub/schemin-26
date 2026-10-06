# WEEK 4 — MANDATORY BULLPEN + CLOSER PAGE APPROVAL PROTOCOL

**Status:** ACTIVE / RELEASE-BLOCKING
**Scope:** every Week 4 page-generation transaction
**Commissioner command:** `generate page N`

## Operating doctrine

The production agent is an **operator/compiler**, not the sole creative authority.

For every page, the production agent must convene the applicable Bullpen domains from the locked repository evidence, reconcile their requirements, and obtain **The Closer's explicit approval before any image-generation call**.

No Closer approval = no render.

## Mandatory Bullpen pre-render board

Every page preflight must include the applicable domains:

- **Groundskeeper** — page number, sequence, composition, production packet completeness.
- **Beat Writer** — exact manuscript copy, narrative function, no improvised prose.
- **Librarian** — canon, callbacks, continuity, prior-week precedent.
- **Scout** — scores, records, player evidence, result-state classification.
- **World / Atlas** — venue, geography, objects, persistent-world consequences.
- **Character QA** — Character IDs, exact canonical references, page-specific character state.
- **Visual Direction Lead** — camera, scale, visual hierarchy, genre, continuity from adjacent pages.
- **Publication Design** — deterministic text layer, mobile hierarchy, image:text balance.
- **Author Council** — restraint, specificity, no generic AI narration or visual cliché.
- **Umpire** — adversarial rejection review.

Only domains relevant to a page need substantive commentary, but none may be silently bypassed when its authority is implicated.

## Required pre-render synthesis

Before rendering, the production agent must internally compile one page-specific production decision containing:

1. exact publishable page title / eyebrow / matchup label;
2. exact reader-facing prose from the locked manuscript;
3. deterministic data fields and current authority state;
4. exact Character IDs;
5. exact native renderer reference handles;
6. world / venue / geography;
7. composition and camera;
8. props / story objects;
9. previous-page continuity;
10. next-page continuity;
11. forbidden elements;
12. mobile hierarchy;
13. Umpire objections and disposition.

The production agent may not add a new story beat merely because it appears aesthetically useful.

## The Closer — PRE-RENDER APPROVAL

The Closer must issue exactly one of:

### `CLOSER_PRE_RENDER_PASS`

Meaning:
- Bullpen authorities reconcile;
- packet is complete;
- manuscript is resolved;
- character references are resolved;
- deterministic data is resolved or intentionally provisional under the active rule;
- no authority conflict remains;
- Umpire objections are cleared;
- page is ready for one controlled renderer invocation.

### `CLOSER_PRE_RENDER_HOLD`

Meaning:
- at least one release-blocking issue remains;
- image generation MUST NOT be invoked.

The production agent cannot override a HOLD.

## Render invocation rule

Only after `CLOSER_PRE_RENDER_PASS` may the production agent invoke image generation.

For character-bearing pages:
- every required canonical `renderer_reference_id` must be passed;
- prose-only identity conditioning is prohibited.

For critical text:
- image generation is not authoritative;
- exact text is controlled by deterministic composition/manuscript authority.

## Candidate review board

After a candidate is visible, the production agent must evaluate it against:
- Character QA;
- World / continuity QA;
- Visual Direction;
- Publication Design;
- manuscript/copy fidelity;
- page-specific rejection conditions;
- Umpire challenge.

## The Closer — POST-RENDER VERDICT

Every surfaced candidate receives exactly one of:

### `CLOSER_PAGE_ACCEPT`
Candidate meets the production packet and may be marked:
`APPROVED_FOR_LOCAL_FOLDER`

### `CLOSER_PAGE_REJECT`
Candidate fails one or more release-blocking checks and is:
`REJECTED_NOT_FOR_FOLDER`

A Commissioner-visible candidate is **not automatically accepted** merely because the renderer returned it.

## Commissioner interaction

Jake should only need to say:

`generate page N`

Bullpen reasoning and Closer approval are internal production responsibilities.

Jake is not the first QA layer and is not required to:
- restate the prompt;
- remind the system of team names;
- remind the system of canon;
- remind the system of the manuscript;
- remind the system of Week 3 precedent;
- perform Director reconciliation.

## Fail-closed rule

If any required authority cannot be retrieved, or Bullpen cannot reconcile a conflict:

`CLOSER_PRE_RENDER_HOLD / DO NOT GENERATE`

The page remains unrendered until the authority defect is repaired.

## Production North Star

**Bullpen thinks.  
The production agent compiles.  
The Umpire challenges.  
The Closer decides.  
Only then does the renderer run.**


## Commissioner-facing delivery contract

For every accepted Week 4 page:

- the user-facing response is the produced page image only;
- do not append a sandbox/download link;
- do not attach a second duplicate file artifact;
- do not add explanatory prose after an accepted render;
- do not switch delivery mechanisms page-to-page merely because the page is data-heavy;
- Pages 1–27 must use one consistent presentation contract.

If a page is rejected or held before acceptance, a concise Bullpen/Closer explanation is allowed.

Once `CLOSER_PAGE_ACCEPT` is issued, delivery must be visually consistent with the accepted Page 1/Page 2 interaction: image only.

A deterministic-data requirement changes how the page is produced internally, not how it is presented to Jake.
