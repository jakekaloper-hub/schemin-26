# Cinema Adapter Contract

Every cinema engine implements:
- input source asset
- prompt/direction
- deterministic settings when supported
- output candidate path
- model/version/seed metadata
- QC result
- rights/license metadata

Engines:
1. comfyui-wan — default local engine
2. ltx-video — alternate local engine
3. paid-cloud — optional only, never required

The web app and WSP never call a vendor directly. They reference accepted media-manifest assets.
