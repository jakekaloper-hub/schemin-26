# Open Cinema Adapter — Wan2.2 + ComfyUI

## Decision
Use **Wan-Video/Wan2.2** as the open-source video model family and **Comfy-Org/ComfyUI** as the local/API orchestration layer for Schemin cinematic generation.

This becomes the default no-per-generation-credit path for experiments when suitable GPU compute is available. Commercial providers remain optional adapters, not the core.

## Special Delivery pipeline
Input: official Week 2 page 7 artwork.
1. Load approved source image.
2. Wan2.2 I2V generates a short restrained-motion plate.
3. Preserve character identity/composition; environmental motion only.
4. Post-process/interpolate if required.
5. Composite all factual scores/titles outside the generative model.
6. Register output + workflow hash + model/checkpoint + seed in WSP media_manifest.
7. Human QA against character canon and official still.

## Prompt
Animate this approved fantasy-football magazine artwork as a restrained cinematic establishing shot. Preserve principal character faces, clothing, proportions, pose hierarchy, scene composition, food props and delivery motif. No new characters and no generated typography. Add subtle food steam, distant stadium crowd movement, paper flutter, practical light flicker, atmospheric haze and a slow controlled camera push with mild depth parallax. No morphing, face drift, extra limbs or object replacement.

## Adapter contract
```
render({
  sourceAsset,
  storyBeatId,
  prompt,
  width,
  height,
  frames,
  fps,
  seed,
  workflow
}) -> {
  output,
  model,
  checkpoint,
  workflowHash,
  seed,
  runtime,
  provenance
}
```

## Reproducibility
Store the ComfyUI API workflow JSON in-repo. Pin model/workflow versions. Never bake verified league text into generated frames. A failed identity/canon check is rejected, not patched into history.

## Compute note
Open source removes per-generation vendor credits, not compute cost. Wan2.2 14B is GPU-heavy; TI2V-5B is the practical lower-footprint first benchmark. Local hardware, a self-hosted GPU runner, or a replaceable cloud GPU can execute the same workflow.
