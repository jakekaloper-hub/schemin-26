# Weekly Story Package v0.1

The Weekly Story Package (WSP) is the canonical interface between league truth, editorial production and media renderers.

```json
{
  "season": 2026,
  "week": 2,
  "edition_status": "published",
  "published_at": null,
  "truth": {
    "fetched_at": null,
    "stale": null,
    "snapshot_age_seconds": null,
    "sources": []
  },
  "cold_open": {},
  "cover": {},
  "game_of_week": {},
  "matchups": [],
  "standings": [],
  "power_rankings": [],
  "waivers": [],
  "pittys_book": {},
  "state_of_play": {},
  "upcoming": [],
  "character_updates": [],
  "rivalry_updates": [],
  "story_beats": [],
  "media_manifest": [],
  "original_edition": {},
  "approvals": {}
}
```

## Story beat contract
Each beat carries:
- id
- factual_basis[]
- editorial_copy
- classification: FACT | EDITORIAL | FICTIONALIZED_PRESENTATION
- characters[]
- visual_direction
- motion_direction
- narration
- sound_direction
- continuity_refs[]
- approval_status

## Media manifest
Every generated derivative records:
- asset_id / story_beat_id
- type
- source_assets
- generator/provider adapter
- model/version when available
- prompt/version
- created_at
- rights/consent notes
- approval status
- final URI
- checksum where practical

## Renderers
A WSP may be rendered to PDF, immersive web, short video, social cut, archive/timeline and future formats without changing its factual substrate.
