"""Explicitly billed, fail-closed OpenAI image route for Schemin Memo OS.

Generates a 9:16 1152x2048 source via Images API, then uniformly resamples
to the 1080x1920 publication master. Never claims direct 1080px model output,
source character binding, visual QA, or publication approval.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

API_URL = "https://api.openai.com/v1/images/generations"
SOURCE = (1152, 2048)
TARGET = (1080, 1920)
MODEL = "gpt-image-2.5-flare"

def request_body(prompt, model=MODEL):
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("PROMPT_REQUIRED")
    return {"model": model, "prompt": prompt, "size": "1152x2048", "quality": "medium",
            "output_format": "png", "n": 1}

def create_master(source_bytes, destination):
    from io import BytesIO
    from PIL import Image
    from native_png_contract import validate_png
    with Image.open(BytesIO(source_bytes)) as source:
        source.load()
        if source.format != "PNG" or source.size != SOURCE:
            raise ValueError(f"OPENAI_SOURCE_DIMENSIONS_UNEXPECTED:{source.size}")
        output = source.convert("RGB").resize(TARGET, Image.Resampling.LANCZOS)
        output.save(destination, format="PNG")
    return validate_png(destination)

def generate(prompt, destination, model=MODEL, allow_billed=False):
    if not allow_billed:
        raise PermissionError("BILLED_GENERATION_NOT_AUTHORIZED")
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY_NOT_CONFIGURED")
    body = json.dumps(request_body(prompt, model)).encode("utf-8")
    request = urllib.request.Request(API_URL, data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(request, timeout=180) as response:
        payload = json.load(response)
    source = base64.b64decode(payload["data"][0]["b64_json"], validate=True)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    check = create_master(source, destination)
    receipt = {"provider": "OPENAI_IMAGES_API", "model": model,
        "source_dimensions": list(SOURCE), "final_dimensions": list(TARGET),
        "geometry_method": "uniform_lanczos_resample_no_crop",
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "final_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        "structural": check["status"], "source_character_binding": "UNVERIFIED",
        "visual_review": "REQUIRED", "publication_eligible": False}
    destination.with_suffix(".receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
    return receipt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--execute-billed", action="store_true")
    args = parser.parse_args()
    prompt = Path(args.prompt_file).read_text()
    if not args.execute_billed:
        print(json.dumps({"state": "DRY_RUN_NO_API_CALL", "request": request_body(prompt, args.model),
                          "target": list(TARGET), "requires": ["OPENAI_API_KEY", "--execute-billed"]}, indent=2))
        return
    print(json.dumps(generate(prompt, args.output, args.model, allow_billed=True), indent=2))

if __name__ == "__main__":
    main()
