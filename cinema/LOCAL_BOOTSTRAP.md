# Local bootstrap

The repository side is wired. The renderer itself must run on a GPU machine.

1. Install current stable ComfyUI.
2. Install ComfyUI Manager.
3. Load `cinema/vendor/filmclusive/wan22-image-ref-video-ref.json`.
4. Use Manager to install missing custom nodes. Audited workflow already identifies ComfyUI-WanVideoWrapper, comfyui-kjnodes, and comfyui_controlnet_aux.
5. Install the WAN 2.2 Animate fp8-scaled model set referenced by Filmclusive/Kijai, UMT5 XXL encoder, required VAE, and optional LoRAs.
6. Put the official Special Delivery source image into ComfyUI input.
7. Confirm the workflow runs interactively once.
8. Export the validated workflow in API format to `cinema/runtime/api/wan22-animate.json`.
9. Run `python cinema/scripts/build_jobs.py`.
10. Submit A01-A05 through the local ComfyUI endpoint and QC outputs before publishing.

This is deliberately the only machine-local boundary. League truth, prompts, shot definitions, provenance and acceptance rules remain versioned in Schemin.
