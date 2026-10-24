"""Export an integrity-checked local bundle for an authorized renderer adapter.

Never treats approved lineup crops as primary-source replacements or as a
provider mount. The bundle is useful only for integration staging/inspection.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = "canon/characters/APPROVED_LINEUP_2026_10_18.json"

def prepare_local_reference_bundle(character_ids, root=ROOT):
    root = Path(root).resolve()
    manifest = json.loads((root / MANIFEST).read_text())
    entries = {e["character_id"]: e for e in manifest["individuals"]}
    if not character_ids or len(character_ids) != len(set(character_ids)):
        raise ValueError("CHARACTER_SET_INVALID")
    if any(cid not in entries for cid in character_ids):
        raise ValueError("UNKNOWN_CHARACTER_ID")
    result = []
    for cid in character_ids:
        entry = entries[cid]
        path = (root / entry["crop"]).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError("REFERENCE_UNAVAILABLE")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != entry["crop_sha256"]:
            raise ValueError("REFERENCE_HASH_MISMATCH")
        result.append({
            "character_id": cid,
            "repository_path": entry["crop"],
            "verified_sha256": actual,
            "authority_role": "COMMISSIONER_APPROVED_LINEUP_SUPPLEMENTARY_PRESENTATION",
            "original_primary_supersession": False,
            "local_verified_path": str(path),
            "provider_attachment_id": None,
            "provider_binding_proven": False
        })
    return {
        "state": "LOCAL_SUPPLEMENTARY_REFERENCE_BUNDLE_VERIFIED",
        "lineup_sha256": manifest["sha256"],
        "renderer_eligible": False,
        "records": result,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characters", required=True, nargs="+")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    try:
        result = prepare_local_reference_bundle(args.characters)
    except (ValueError, OSError, KeyError) as exc:
        print(json.dumps({"state":"GENERATION_BLOCKED","reason":str(exc)}))
        return 2
    data = json.dumps(result, indent=2)
    if args.json_output:
        Path(args.json_output).write_text(data + "\n")
    else:
        print(data)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
