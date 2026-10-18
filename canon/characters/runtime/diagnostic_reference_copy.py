#!/usr/bin/env python3
"""Mac-only deterministic primary-reference raster transport diagnostic.

This is a reference copy/format roundtrip, NOT an AI image generator, not
C1 generated-character acceptance, and not a production renderer. It validates
that the four currently present SHA-approved primary bytes can be individually
opened and routed into exact Character-ID-specific raster output slots.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "canon/characters/reference_sources_v1.json"


def sha(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def diagnostics(root: Path, out: Path, *, render_cmd: str = "sips") -> dict:
    if not shutil.which(render_cmd):
        raise RuntimeError("sips/compatible macOS image converter unavailable: route blocked")
    reg=json.loads((root/"canon/characters/reference_sources_v1.json").read_text())
    out.mkdir(parents=True,exist_ok=True)
    records=[]; blockers=[]
    for a in reg["entries"]:
        cid=a["character_id"]
        p=root/a["repository_path"]
        if not p.is_file():
            blockers.append({"character_id":cid,"reason":"EXACT_PRIMARY_BYTES_NOT_STORED"})
            continue
        if sha(p)!=a["expected_sha256"] or p.stat().st_size!=a["observed_library_size_bytes"]:
            raise ValueError("Primary source hash/size mismatch: "+cid)
        target=out/(cid+".png")
        if target.exists():
            raise FileExistsError("Diagnostic output already exists: "+str(target))
        with tempfile.TemporaryDirectory() as tmp:
            probe=Path(tmp)/(cid+".png")
            for destination in (target,probe):
                subprocess.run([render_cmd,"-s","format","png",str(p),"--out",str(destination)],
                               check=True,capture_output=True,text=True)
                if destination.read_bytes()[:8]!=b"\x89PNG\r\n\x1a\n":
                    raise ValueError("Reference diagnostic output is not PNG")
            if sha(target)!=sha(probe):
                raise ValueError("Reference transport conversion is nondeterministic: "+cid)
        records.append({
            "character_id":cid,
            "input_repository_path":a["repository_path"],
            "input_sha256":a["expected_sha256"],
            "input_size_bytes":a["observed_library_size_bytes"],
            "output_repository_path":str(target.relative_to(root)),
            "output_sha256":sha(target),
            "output_size_bytes":target.stat().st_size,
            "subject_slot":"DIAGNOSTIC_SOURCE_COPY_SLOT_"+cid,
            "source_hash_checked_before_copy":True,
            "repeat_conversion_byte_identical":True,
            "provider_image_generation_binding_proven":False,
            "c1_generated_character_output_pass":False,
        })
    if not records:
        raise RuntimeError("No approved primary source bytes available")
    return {
        "schema_version":"1.0",
        "route":"LOCAL_DETERMINISTIC_REFERENCE_COPY_DIAGNOSTIC_ONLY",
        "production_renderer":False,
        "approval_scope":"PROVES_SOURCED_SOURCE_RASTER_TRANSPORT_NOT_GENERATIVE_CHARACTER_PRESERVATION",
        "total_characters":len(reg["entries"]),
        "tested_primary_count":len(records),
        "unavailable_primary_count":len(blockers),
        "renderer_subject_binding_proven":False,
        "c1_generated_raster_qa_passed":False,
        "t15":"HOLD",
        "t16":"HOLD",
        "outputs":records,
        "missing":blockers,
    }


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=ROOT)
    parser.add_argument("--output-dir",type=Path,required=True)
    parser.add_argument("--receipt",type=Path,required=True)
    args=parser.parse_args()
    root=args.root.resolve()
    out=args.output_dir.resolve()
    if not out.is_relative_to(root):
        raise ValueError("Diagnostic output must remain within explicit existing repository root")
    receipt=args.receipt.resolve()
    if not receipt.is_relative_to(root):
        raise ValueError("Diagnostic receipt must remain within explicit existing repository root")
    result=diagnostics(root,out)
    receipt.parent.mkdir(parents=True,exist_ok=True)
    receipt.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"tested_primary":result["tested_primary_count"],
                      "missing_primary":result["unavailable_primary_count"],
                      "production_ready":False,"t15":"HOLD"}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
