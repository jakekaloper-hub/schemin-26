# EXTERNAL RENDER TRANSPORT SELECTION V1
**Preferred:** Runpod ComfyUI Serverless / dedicated ComfyUI GPU
**Fallback:** generic remote ComfyUI HTTP API
**Reason:** Runpod documentation explicitly supports dedicated ComfyUI generation and ComfyUI workers deployed as Serverless endpoints. Novel OS can therefore preserve the ComfyUI workflow boundary while moving compute outside ChatGPT/local hardware.
## Runtime secrets
Never commit credentials. Required at execution: RUNPOD_API_KEY and RUNPOD_ENDPOINT_ID (or equivalent secret store).
## Gate
Selection does not equal connection. Production state remains TRANSPORT_IMPLEMENTED / REMOTE_RUNTIME_UNBOUND until an authorized endpoint and credential are available to the runtime.
## Security
Secrets stay outside NovelVisualJob, Git history, RenderReceipt and image metadata.
