# Schemin → KupkaProd adapter

This adapter treats KupkaProd as a renderer/orchestrator, never as league truth.

## Inputs
- official Week 2 page-7 artwork exported as `special-delivery-source.png`
- `special-delivery-brief.txt`
- Schemin Week 2 Story Package

## Recommended upstream settings
- image-to-video/keyframe path enabled
- no dialogue
- one take per scene for first smoke test; increase only after identity QC passes
- 24 fps
- conservative resolution for first run
- resume enabled

## Return contract
Copy/register selected outputs as A01–A05 with:
- upstream repo + commit/version
- model/workflow
- seed
- source artwork checksum
- QC decision
- output checksum
- publication status

Do not mark generated media official until Schemin release approval.
