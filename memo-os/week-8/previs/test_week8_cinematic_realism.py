#!/usr/bin/env python3
"""Week 8 static cinematic realism packet validator. No rendered-art approval."""
import json
import pathlib
import sys

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
    "reference_paths_relative": all(not pathlib.PurePath(v["crop"]).is_absolute() and not pathlib.PurePath(v["manifest"]).is_absolute() for v in DATA["references"].values()),
    "six_location_parent_ids": len({p["location_id"] for p in rows}) == 6,
    "decided_winners_not_art_lock": DATA["visual_governance"]["no_outcome_lock"] is False and DATA["week8_result_promotion"]["release"] == "BLOCKED",
    "no_artwork": DATA["visual_governance"]["no_artwork"] is True,
    "all_decided_winners": all(p.get("week8_result_evidence", {}).get("winner") in ("HOME", "AWAY") for p in rows),
    "all_manuscript_links": all(p.get("session_e_v1", {}).get("manuscript_section") == p["packet_id"] for p in rows),
    "all_scene_copy_camera": all(all(p.get("session_c_v1", {}).get(k) for k in ("scene_action", "camera_and_blocking", "provisional_narration")) for p in rows),
    "all_reference_mounts_unproven": all(v.get("render_mount_proven") is False for v in DATA["references"].values()),
}
print(json.dumps({"checks": checks, "passed": sum(checks.values()), "total": len(checks), "status": "STATIC_PREFLIGHT_ONLY"}, indent=2))
sys.exit(0 if all(checks.values()) else 1)
