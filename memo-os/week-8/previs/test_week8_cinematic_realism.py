#!/usr/bin/env python3
"""Week 8 static cinematic realism packet validator. No rendered-art approval."""
import json
import pathlib
import sys
import hashlib
import re

def owner_crop_hash_matches(record):
    crop = ROOT / record["crop"]
    manifest = ROOT / record["manifest"]
    if not crop.is_file() or not manifest.is_file():
        return False
    match = re.search(r'owner_crop_sha256:\s*"?([0-9a-f]{64})', manifest.read_text())
    return bool(match and hashlib.sha256(crop.read_bytes()).hexdigest() == match.group(1))


ROOT = pathlib.Path(__file__).resolve().parents[3]
PACKETS = ROOT / "memo-os/week-8/previs/WEEK_8_29_COMPOSITION_PACKETS_2026-11-02.json"
DATA = json.loads(PACKETS.read_text())
rows = DATA["packets"]
stories = {p["story"] for p in rows}
overtures = [p for p in rows if p["layout"].startswith("shared environmental POV overture")]
ending = [p for p in rows if p.get("ending_selection_status") == "WINNER_SELECTED_COPY_UNLOCKED_NOT_ART_APPROVED"]
fields = ("site", "discovery_path", "visual_location_cues", "inhabited_world_evidence", "lighting", "camera_geometry", "continuity", "forbidden_ui")
checks = {
    "29_compositions": len(rows) == 29,
    "six_stories": len(stories) == 6,
    "six_overtures": len(overtures) == 6,
    "six_decided_ending_branches": len(ending) == 6,
    "1080x1920": all(p["canvas"] == [1080, 1920] for p in rows),
    "cinematic_specs_present": all(all(p.get("cinematic_realism_v1", {}).get(k) for k in fields) for p in rows),
    "no_rendered_visual_claim": all(p["cinematic_realism_v1"].get("review_status") == "SPECIFIED_NOT_VISUALLY_VERIFIED" for p in rows),
    "owner_crop_byte_hashes_match": all(owner_crop_hash_matches(v) for v in DATA["references"].values()),
    "reference_paths_relative": all(not pathlib.PurePath(v["crop"]).is_absolute() and not pathlib.PurePath(v["manifest"]).is_absolute() for v in DATA["references"].values()),
    "six_location_parent_ids": len({p["location_id"] for p in rows}) == 6,
    "decided_winners_not_art_lock": DATA["visual_governance"]["no_outcome_lock"] is False and DATA["week8_result_promotion"]["release"] == "BLOCKED",
    "no_artwork": DATA["visual_governance"]["no_artwork"] is True,
    "all_decided_winners": all(p.get("week8_result_evidence", {}).get("winner") in ("HOME", "AWAY") for p in rows),
    "all_manuscript_links": all(p.get("session_e_v1", {}).get("manuscript_section") == p["packet_id"] for p in rows),
    "all_scene_copy_camera": all(all(p.get("session_c_v1", {}).get(k) for k in ("scene_action", "camera_and_blocking", "provisional_narration")) for p in rows),
    "reference_mount_status_explicit": all(isinstance(v.get("render_mount_proven"), bool) for v in DATA["references"].values()),
}
if len(sys.argv) == 1:
    print(json.dumps({"checks": checks, "passed": sum(checks.values()), "total": len(checks), "status": "STATIC_PREFLIGHT_ONLY"}, indent=2))
    sys.exit(0 if all(checks.values()) else 1)

# Optional actual-art gate. This cannot substitute for independent identity/camera/copy review.
# Usage: python test_week8_cinematic_realism.py --packet W08-02-01 --png FILE --binding-receipt JSON
import argparse
import struct
argp = argparse.ArgumentParser(description="Live Week 8 render gate; never an independent approval.")
argp.add_argument("--packet", required=True)
argp.add_argument("--png", required=True)
argp.add_argument("--binding-receipt", required=True)
args = argp.parse_args()
packet = next((v for v in rows if v["packet_id"] == args.packet), None)
assert packet is not None, "Unknown packet ID"
img = pathlib.Path(args.png)
receipt_path = pathlib.Path(args.binding_receipt)
live_checks = {"static_preflight": all(checks.values())}
try:
    image_bytes = img.read_bytes()
    valid_png = image_bytes.startswith(b"\\x89PNG\\r\\n\\x1a\\n") and image_bytes[12:16] == b"IHDR"
    live_checks["actual_png_exists"] = valid_png
    live_checks["exact_resolution"] = valid_png and struct.unpack(">II", image_bytes[16:24]) == tuple(packet["canvas"])
    actual_sha256 = hashlib.sha256(image_bytes).hexdigest()
except (FileNotFoundError, OSError, ValueError, struct.error):
    actual_sha256 = None
    live_checks["actual_png_exists"] = False
    live_checks["exact_resolution"] = False
try:
    receipt = json.loads(receipt_path.read_text())
except (OSError, json.JSONDecodeError):
    receipt = {}
live_checks["auditable_provider_request"] = bool(receipt.get("provider_request_id") and receipt.get("provider") and receipt.get("submitted_at"))
submitted = receipt.get("renderer_inputs", [])
live_checks["required_character_refs_mounted"] = (
    isinstance(submitted, list)
    and all(any(
        isinstance(e, dict)
        and e.get("character_id") == char
        and e.get("attached_as_image") is True
        and e.get("source_path")
        and e.get("source_sha256")
        for e in submitted
    ) for char in packet["reference_ids"])
)
live_checks["independent_visual_qa_receipt_present"] = bool(
    receipt.get("independent_visual_qa", {}).get("evidence_path")
    and receipt.get("independent_visual_qa", {}).get("result") == "PASS"
)
live_checks["copy_qa_receipt_present"] = bool(
    receipt.get("copy_qa", {}).get("evidence_path")
    and receipt.get("copy_qa", {}).get("result") == "PASS"
)
print(json.dumps({
    "packet": args.packet, "sha256": actual_sha256,
    "checks": live_checks, "status": "PROOF_GATES_PASS_NOT_FOUNDER_APPROVAL" if all(live_checks.values()) else "REJECTED_OR_BLOCKED",
    "warning": "Manual reference identity, scenic camera, source-copy and artistic quality still require actual evidence; a JSON field does not authenticate a reviewer.",
}, indent=2))
sys.exit(0 if all(live_checks.values()) else 1)
