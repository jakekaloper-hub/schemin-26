#!/usr/bin/env python3
"""Verify every remaining 2015 team-1 event is linked only to a bounded Jake scene."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIXTURES=json.loads((ROOT/"evidence/2015_FIXTURE_COVERAGE.json").read_text())
REGISTER=json.loads((ROOT/"manuscript/2015-jake-arc/SCENE_REGISTER.json").read_text())

def main() -> int:
    expected={e["event_id"] for e in FIXTURES["events"] if 1 in (e["home_id"],e["away_id"])}
    expected.remove("ESPN1417621-2015-P01-E002")
    actual={event for scene in REGISTER["scenes"] for event in scene["source_event_ids"]}
    errors=[]
    if expected != actual: errors.append("EVENT_SET_MISMATCH")
    if len(REGISTER["scenes"]) != 6: errors.append("SCENE_COUNT_INVALID")
    if any(s["pov_character_id"]!="CHAR-JAKE-KALOPER" or s["pov_class"]!="PRINCIPAL_CHARACTER" for s in REGISTER["scenes"]): errors.append("POV_SCOPE_INVALID")
    if any(not s["real_owner_boundary_note"] or not s["story_time_cutoff"] for s in REGISTER["scenes"]): errors.append("PACKET_FIELD_MISSING")
    prose="\n".join((ROOT/p).read_text() for p in ["manuscript/2015-jake-arc/THE_COST_OF_RETURN_NONCANON.md","manuscript/2015-jake-arc/THE_RECORD_HE_CANNOT_KEEP_NONCANON.md"])
    forbidden=["Austin", "Kevin", "Jordan", "Phillip", "2016", "2024", "2025", "champion", "championship"]
    present=[x for x in forbidden if x.lower() in prose.lower()]
    if present: errors.append("FOREKNOWLEDGE_OR_UNBOUND_PRINCIPAL:"+",".join(present))
    result={"scope":"ALL_REMAINING_2015_TEAM_1_EVENTS","expected_events":len(expected),"linked_events":len(actual),"scene_count":len(REGISTER["scenes"]),"errors":errors,"status":"PASS" if not errors else "FAIL"}
    (ROOT/"review/2015_JAKE_ARC_CHECK.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2)); return int(bool(errors))

if __name__=="__main__": raise SystemExit(main())
