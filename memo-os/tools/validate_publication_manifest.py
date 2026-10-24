#!/usr/bin/env python3
"""Fail-closed validation of Schemin Memo OS publication manifests.
Does not certify visual character fidelity or independent QA.
"""
import argparse
import hashlib
import json
import pathlib
from io import BytesIO
from PIL import Image
import sys

REQUIRED = ("source_folio_id", "publication_position", "asset_path", "sha256", "status")
STATES = {"CANDIDATE", "REVIEWED", "ACCEPTED", "BLOCKED", "SUPERSEDED"}

def verify(manifest_path, root):
    errors = []
    try:
        manifest = json.loads(pathlib.Path(manifest_path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"manifest unreadable: {exc}"]
    if not isinstance(manifest, dict):
        return ["manifest must be an object"]
    pages = manifest.get("pages")
    root = pathlib.Path(root).resolve()
    if not isinstance(pages, list) or not pages:
        return ["pages must be a nonempty list"]
    positions = set()
    for i, page in enumerate(pages, 1):
        label = f"page[{i}]"
        if not isinstance(page, dict):
            errors.append(f"{label}: page must be an object")
            continue
        for field in REQUIRED:
            if field not in page:
                errors.append(f"{label}: missing {field}")
        if any(field not in page for field in REQUIRED):
            continue
        pos = page["publication_position"]
        if type(pos) is not int or pos <= 0 or pos in positions:
            errors.append(f"{label}: invalid or duplicate publication_position")
        else:
            positions.add(pos)
        if not isinstance(page["source_folio_id"], str) or not page["source_folio_id"].strip():
            errors.append(f"{label}: missing source folio identity")
        if not isinstance(page["status"], str) or page["status"] not in STATES:
            errors.append(f"{label}: unknown acceptance status")
        if page["status"] == "ACCEPTED":
            for key in ("editorial_receipt", "raster_receipt", "independent_review_receipt"):
                if not page.get(key):
                    errors.append(f"{label}: ACCEPTED without {key}")
        if not isinstance(page["asset_path"], str) or not page["asset_path"]:
            errors.append(f"{label}: unsafe asset_path")
            continue
        rel = pathlib.PurePosixPath(page["asset_path"])
        if rel.is_absolute() or ".." in rel.parts:
            errors.append(f"{label}: unsafe asset_path")
            continue
        asset = root.joinpath(*rel.parts).resolve()
        if not asset.is_relative_to(root):
            errors.append(f"{label}: unsafe asset_path")
            continue
        if not asset.is_file():
            errors.append(f"{label}: asset missing: {rel}")
            continue
        raw = asset.read_bytes()
        if hashlib.sha256(raw).hexdigest() != page["sha256"]:
            errors.append(f"{label}: SHA-256 mismatch")
        if asset.suffix.lower() == ".png":
            try:
                with Image.open(BytesIO(raw)) as image:
                    if image.format != "PNG":
                        raise ValueError("not PNG")
                    if image.size != (1024, 1536):
                        errors.append(f"{label}: PNG dimensions do not match 1024 x 1536")
                    image.verify()
                # Verify chunk integrity and then decode pixels; neither header
                # dimensions alone nor a fabricated IHDR proves a usable raster.
                with Image.open(BytesIO(raw)) as image:
                    image.load()
            except (OSError, ValueError, SyntaxError):
                errors.append(f"{label}: asset is not a readable PNG")
    if positions != set(range(1, len(pages) + 1)):
        errors.append("physical positions must be consecutive from 1")
    return errors

def main():
    p = argparse.ArgumentParser()
    p.add_argument("manifest")
    p.add_argument("--root", default=".")
    args = p.parse_args()
    errors = verify(args.manifest, args.root)
    for error in errors:
        print("FAIL:", error)
    if not errors:
        print("PASS: publication manifest checks", args.manifest)
    return int(bool(errors))

if __name__ == "__main__":
    sys.exit(main())
