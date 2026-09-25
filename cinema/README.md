# Schemin Cinema — local/open pipeline

Schemin Cinema replaces per-shot paid generation as the default path.

## Engine
Primary: ComfyUI + Wan 2.2 image-to-video.
Fallback/benchmark: LTX-Video/LTX-2.

The adapter boundary means either engine can be replaced without changing the Weekly Story Package.

## Why
- runs locally/self-hosted
- source artwork remains under our control
- no per-generation credit gate
- repeatable workflow JSON can be versioned
- verified typography is composited after generation
- rejected generations remain reproducible through seeds/settings

## Week 2 first target
Special Delivery, official Week 2 page 7.

Pipeline:
source art -> local I2V -> QC -> ffmpeg verified overlays -> web encode -> media manifest.

No generated text or score is trusted. Principal character drift fails QC.
