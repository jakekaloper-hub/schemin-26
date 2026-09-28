from __future__ import annotations
import hashlib, json, shutil
from datetime import datetime, timezone
from pathlib import Path
from gradio_client import Client

SPACE = "black-forest-labs/FLUX.1-Kontext-Dev"
OUT = Path("living-novel/os/runtime/smoke")
OUT.mkdir(parents=True, exist_ok=True)

client = Client(SPACE)
print(client.view_api(all_endpoints=True))

result = client.predict(
    None,
    "A simple cinematic still life of one closed plain brown leather notebook on an otherwise empty wooden table, ordinary natural light, no text, no symbols, no glow.",
    424242,
    False,
    2.5,
    8,
    api_name="/infer",
)
print("RAW_RESULT", result)

artifact = result[0] if isinstance(result, (list, tuple)) else result
if isinstance(artifact, dict):
    artifact = artifact.get("path") or artifact.get("url")
src = Path(str(artifact))
if not src.exists():
    raise RuntimeError(f"Returned artifact is not a local retrieved file: {artifact!r}")
dst = OUT / "zerogpu-smoke.png"
shutil.copyfile(src, dst)
digest = hashlib.sha256(dst.read_bytes()).hexdigest()
receipt = {
    "schema": "NovelOSRenderReceipt/v1",
    "job_id": "NOVEL-OS-ZEROGPU-SMOKE-V1",
    "beat_id": None,
    "engine": "FLUX.1-Kontext-dev",
    "provider": "Hugging Face ZeroGPU",
    "transport": "GradioClientZeroGPU",
    "space": SPACE,
    "seed": 424242,
    "generation_parameters": {"guidance_scale": 2.5, "steps": 8},
    "execution_timestamp": datetime.now(timezone.utc).isoformat(),
    "output_artifact": str(dst),
    "output_sha256": digest,
    "status": "RENDERED_UNAPPROVED",
    "purpose": "non-canon external GPU smoke test"
}
(OUT / "zerogpu-smoke-receipt.json").write_text(json.dumps(receipt, indent=2))
print(json.dumps(receipt, indent=2))
