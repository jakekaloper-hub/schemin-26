# Schemin Cinema Runtime — audited from selected upstream

Upstream workflow: Filmclusive-ImageRef2VideoRef-WAN2.2 Animate.json.

## Runtime
- current stable ComfyUI
- ComfyUI-WanVideoWrapper (workflow records Kijai wrapper nodes)
- comfyui-kjnodes
- comfyui_controlnet_aux
- any additional node packs reported by ComfyUI when the vendored workflow is loaded

## Models
Per Filmclusive upstream README:
- WAN 2.2 Animate fp8-scaled model set from Kijai/WanVideo_comfy_fp8_scaled (Wan22Animate)
- text encoder: umt5-xxl-enc-bf16.safetensors
- optional Lightx2v LoRA
- optional WanAnimate_relight_lora_fp16.safetensors
- VAE referenced by workflow notes

Expected folders:
ComfyUI/models/diffusion_models
ComfyUI/models/text_encoders
ComfyUI/models/vae
ComfyUI/models/loras

## Important
The vendored JSON is a ComfyUI UI workflow, not automatically an API-format prompt. It must first be loaded successfully in ComfyUI with its node/model dependencies. Export API format after validation for headless use.
