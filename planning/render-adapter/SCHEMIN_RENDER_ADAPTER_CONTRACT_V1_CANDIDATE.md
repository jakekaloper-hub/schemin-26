# SCHEMIN '26 — SHARED RENDER ADAPTER CONTRACT V1 (CANDIDATE)

**Status:** RESEARCH_CANDIDATE / NOT ACTIVE  
**Date:** 2026-09-30  
**Scope:** Visual / Data Story / Motion rendering seam only

## Board decision

Schemin does not need another storyboard OS, canon database, world model, historical ledger, or publication state machine.

The repository already owns:
- verified league evidence and freshness;
- Weekly Memo V5.5 Issue Previs + Page Packet production;
- Chronicle/Living Novel history and scene architecture;
- Character Canon and Character Control Plane v2 release-candidate machinery;
- World Engine V1.1 + Location Control Plane;
- renderer-addressable structural environment references;
- publication and world-evolution gates.

External repositories may therefore sit only **downstream** of Schemin authority.

## Candidate seam

```
VERIFIED LEAGUE EVIDENCE
        |
        v
ACTIVE CHARACTER AUTHORITY ---- WORLD / LOCATION PACKET
        |                              |
        +--------------+---------------+
                       |
                       v
             MEMO / NOVEL / PAGE / SCENE PACKET
                       |
                       v
              SCHEMIN RENDER REQUEST
                       |
        +--------------+----------------+
        |              |                |
        v              v                v
 CHARACTER-GROUNDED  DATA STORY       MOTION
 STATIC / ART        ADAPTER          ADAPTER
        |              |                |
        +--------------+----------------+
                       |
                       v
              ARTIFACT + PROVENANCE
                       |
                       v
          EXISTING QA / PUBLICATION GATES
```

## Authority invariants

A renderer:
1. may transform presentation;
2. may not create or supersede league facts;
3. may not promote character identity/version/reference assets;
4. may not create geography or world state;
5. may not silently invent missing deterministic data;
6. may not self-certify publication readiness;
7. may not write World Evolution;
8. must preserve source/provenance receipts;
9. must fail closed when required authority inputs are absent;
10. cannot become ACTIVE merely because an external library can produce an attractive artifact.

## Relationship to Character Control Plane

AIComicBuilder research reinforces the value of mounted multi-view references and reference-first generation.

It does **not** justify:
- a second Schemin character database;
- automatic character extraction as canon;
- generated turnaround sheets self-promoting to authority;
- a parallel storyboard/shot state machine.

The current CCP v2 remains RELEASE_CANDIDATE / NOT ACTIVE. Its existing G1 durable-byte and renderer-injection closure contract remains upstream. The Render Adapter may consume a character packet only from the character authority declared active by Project Control at execution time.

## Profile A — CHARACTER_GROUNDED_STATIC

Required:
- verified evidence receipt;
- active character authority receipt;
- one or more character packets;
- renderer-addressable reference asset for every depicted character;
- `render_ready=true` per depicted character;
- Page/Scene/Visual packet;
- world/location packet when location-bearing.

Research lesson:
- AIComicBuilder reference mounting.

Success metric:
- canonical-reference injection pass rate;
- character regeneration/correction rate.

## Profile B — DATA_STORY

Required:
- verified evidence receipt;
- deterministic, read-only data payload;
- explicit field definitions and units;
- no inference of absent league values;
- provenance preserved into the artifact.

Research lesson:
- Vizzu animated data-story transitions.

Initial Schemin candidate:
- Pittsy's Book receipts or standings progression.

Success metric:
- manual graphic rebuild rate;
- data/artifact divergence rate.

## Profile C — MOTION

Required:
- verified evidence;
- existing storyboard/page/scene packet;
- source artifact list;
- character/world packets where depicted;
- session/revision identity;
- output artifact verification;
- no authority mutation.

Research lessons:
- Remotion: deterministic code-driven composition/rendering.
- OpenStoryline: conversational multi-turn edit session and verified outputs.
- VoiceStudio: possible future local narration/dubbing lane.

These are capability roles, not selected dependencies.

Success metric:
- revision restart rate;
- template reuse rate;
- artifact verification pass rate.

## Deferred profiles

Timeline/chronology and interactive scroll-scene reader are intentionally outside this candidate. Schemin already has Chronicle history and an active read-only Atlas. TimelineJS3 and Albino patterns remain reference material until a user-facing reader need is prioritized.

## Promotion gates

Before any production dependency proposal:
1. current Schemin authority map remains single-source;
2. candidate tests pass;
3. one real Week 4+ unit can be expressed by the contract without duplicating state;
4. license review passes;
5. Warden permission/security review passes;
6. local/runtime cost and failure modes are measured;
7. rollback path exists;
8. chosen renderer proves measurable value over current production;
9. Project Control Registry explicitly promotes the adapter;
10. existing Memo/Novel/World/Character gates remain upstream and independent.
