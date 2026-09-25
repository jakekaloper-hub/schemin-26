# Bullpen decision — Cinema production engine

Date: 2026-09-25
Status: ADOPT AS OPTIONAL LOCAL PRODUCTION ENGINE / DO NOT FORK INTO SCHEMIN

## Decision
Use KupkaProd Cinema Pipeline as the preferred end-to-end local production runner for the Week 2 proof of concept, behind a Schemin adapter. Keep Filmclusive/WAN as a secondary renderer experiment.

## Why
KupkaProd already supplies the orchestration layer Schemin was beginning to rebuild: scene planning, storyboard review, ComfyUI API client, image-to-video support, multiple takes, resume state, review, FFmpeg assembly, and a browser UI.

## Boundary
Schemin remains authoritative for league truth, characters, published artwork, story beats, provenance and release approval. KupkaProd receives a constrained production brief. Its LLM must not rewrite scores, identities, history, or approved story facts.

## License gate
Upstream is non-commercial only unless separately licensed. Personal/non-commercial Schemin experimentation is compatible with the published license; do not use it for commercial/revenue-generating output without a separate license review.

## Hardware gate
Upstream documents NVIDIA 12GB+ VRAM, 32GB+ RAM recommended, roughly 50GB model storage, Python 3.10+, ComfyUI, Ollama and FFmpeg. This remains a machine-runtime dependency.

## Acceptance test
Special Delivery is the canary. Success means:
1. official page-7 art enters the I2V path;
2. five constrained shots render;
3. no factual text is generated as truth;
4. character identity survives QC;
5. selected takes assemble;
6. outputs can be registered back into the Week 2 Story Package and Schemin Studio.
