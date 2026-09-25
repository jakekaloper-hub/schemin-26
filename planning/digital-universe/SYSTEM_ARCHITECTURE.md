# Digital Universe — System Architecture

```
ESPN PUBLIC LEAGUE
      ↓
SCHEMIN DATA GATEWAY
validation • retries • LKG • freshness
      ↓
CANONICAL LEAGUE EVENTS
      + CHARACTER CANON
      ↓
WEEKLY MEMO OS / EDITORIAL
      ↓
WEEKLY STORY PACKAGE
      ├── PDF Renderer → immutable original edition
      ├── Web Renderer → interactive Week Hub
      ├── Media Orchestrator
      │      ├── image adapter
      │      ├── motion/video adapter
      │      ├── narration adapter
      │      ├── sound/music adapter
      │      └── editing/composition adapter
      ├── Social Renderer
      └── History Projector
             ├── character arcs
             ├── team timeline
             ├── rivalries
             └── season documentary index
```

## Repository boundaries
Schemin ’26 owns contracts, canon, truth rules, weekly packages and release state. Bullpen/FLA may provide specialist adapters but is not a runtime dependency.

## Media orchestration
Adapters implement a common job contract: input assets + approved story beat + generation settings → candidate asset + provenance. Candidate assets never publish automatically.

## Storage
Separate immutable source/published artifacts from generated candidates. Keep lightweight metadata in Git; large media belongs in durable object storage/CDN once deployment is selected.

## Release states
DRAFT → FACT_CHECKED → CANON_CHECKED → MEDIA_APPROVED → RELEASE_CANDIDATE → PUBLISHED.

## Failure behavior
If live data is unavailable, surface freshness and use validated LKG where policy permits. Never fabricate missing league facts to complete a cinematic sequence.
