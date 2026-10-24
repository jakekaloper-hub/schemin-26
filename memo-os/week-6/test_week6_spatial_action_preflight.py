#!/usr/bin/env python3
"""Week 6 previsualization semantic/spatial gate. Does NOT certify physical engineering."""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"world/location-control-plane/compiler"))
from location_control_plane import compile_world_packet
DATA=Path(__file__).with_name("WEEK_6_SPATIAL_ACTION_PREFLIGHT_V1.json")
def check():
    p=json.loads(DATA.read_text())
    rows=p["encounters"]
    assert len(rows)==6 and len({r["id"] for r in rows})==6
    assert rows[0]["id"]=="W6-RED-DK" and rows[0]["commissioner_home_override_required"]
    assert p["source_coordinate_space"].endswith("non-metric")
    for row in rows:
        loc=row["home_loc"]
        ids=[row["home_character"],row["away_character"]]
        sem=compile_world_packet(loc,ids,consumer="MEMO",event_class=row["event_class"])
        assert sem["status"]=="READY_FOR_SEMANTIC_QA",(loc,sem.get("review_blockers"))
        assert [x["relationship"] for x in sem["relationships"]]==["HOME_PRIMARY","AWAY_REACHABLE"],loc
        cinematic=compile_world_packet(loc,ids,consumer="VISUAL",event_class=row["event_class"],reference_requirement="CINEMATIC")
        assert cinematic["status"]=="HUMAN_REVIEW_REQUIRED",loc
        assert "MISSING_APPROVED_CINEMATIC_REFERENCE" in cinematic["review_blockers"],loc
        assert row["feature_candidate"].startswith("SUB::"+loc+"::"),loc
        assert len(row["anchor_sequence"])>=5 and len(row["action_path"])>=4,loc
        assert len(row["camera_axes"])>=2 and len(row["physical_checks"])>=5,loc
        print(f"SEMANTIC_PASS / CINEMATIC_HOLD {row['id']}: {loc}")
    print("6/6 semantic and structural-contract assertions PASS; 6/6 cinematic reference gates HOLD.")
if __name__=="__main__":
    check()
