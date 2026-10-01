# Weekly Memo OS — Renderer-Addressable Asset Contract V1

**Status:** V5.6 RC dependency  
**Purpose:** ensure generated media can be retrieved, inspected, hashed, reused and certified as the exact bytes entering publication.

## Lifecycle

```text
GENERATION
→ DURABLE ASSET ID
→ RENDERER-ADDRESSABLE BYTES
→ APPROVED PERSISTENT LOCATION
→ CONTENT HASH
→ GENERATION INTENT LINK
→ REFERENCE LINEAGE
→ INSPECTION
→ ASSET MANIFEST
```

No asset may receive ART_LOCK when the exact bytes intended for publication cannot be retrieved by independent QA.

## Required record

```yaml
asset_id:
issue_id:
page_id:
generation_intent_id:
storage_location:
content_hash:
dimensions:
mime_type:
created_at:
generator:
reference_assets:
character_packets:
world_packet:
inspection_status:
supersedes:
release_eligible:
```

## Hard rules

- FILE_EXISTS != RELEASE_READY.
- IMAGE_WAS_GENERATED != ART_LOCK.
- broken locator → BLOCKED.
- missing bytes → BLOCKED.
- hash mismatch → BLOCKED.
- superseded asset → BLOCKED.
- missing lineage → BLOCKED.
- final raster must be the same asset identity inspected by QA.
