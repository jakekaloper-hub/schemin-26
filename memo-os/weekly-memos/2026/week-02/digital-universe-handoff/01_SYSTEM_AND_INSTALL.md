# System and install

## Preferred stack
- KupkaProd Cinema Pipeline: local production orchestrator
- ComfyUI: execution backend
- LTX/KupkaProd-supported I2V path for primary smoke test
- Schemin Filmclusive WAN 2.2 workflow as alternate experiment
- FFmpeg: deterministic assembly/compositing
- Ollama/local LLM only where the production engine requires it

## Upstream constraints already audited
KupkaProd's repository is licensed for non-commercial use; commercial use requires a separate license. Treat this handoff as non-commercial R&D unless the owner explicitly changes that status.

KupkaProd documents a GPU-oriented local setup. Before installing models, record machine capacity and confirm enough free storage.

## Preflight
Record:
```
OS:
GPU:
VRAM:
RAM:
Free disk:
Python:
FFmpeg:
ComfyUI:
Ollama:
```

Then:
1. Clone the Schemin repo/branch provided by Jake.
2. Clone KupkaProd separately; do not vendor its whole source into Schemin.
3. Follow the upstream install instructions from its current README.
4. Confirm ComfyUI `/system_stats` responds.
5. Confirm FFmpeg executes.
6. Confirm required workflow/model files load.
7. Run a minimal non-Schemin smoke test before consuming production time.
8. Proceed to Special Delivery only after the runtime is healthy.

Never commit model weights, credentials, machine-specific secrets or generated caches to Schemin.