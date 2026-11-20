#!/usr/bin/env python3
"""Verify the bounded 2016 team-1 Jake candidate against its source ledger."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main() -> int:
    fixtures=json.loads((ROOT/"evidence/2016_FIXTURE_COVERAGE.json").read_text())
    register=json.loads((ROOT/"manuscript/2016-jake-arc/SCENE_REGISTER.json").read_text())
    expected={e["event_id"] for e in fixtures["events"] if 1 in (e["home_id"],e["away_id"])}
    actual={event for scene in register["scenes"] for event in scene["source_event_ids"]}
    errors=[]
    if expected!=actual: errors.append("EVENT_SET_MISMATCH")
    if len(register["scenes"])!=10: errors.append("SCENE_COUNT_INVALID")
    if any(s["pov_character_id"]!="CHAR-JAKE-KALOPER" or s["pov_class"]!="PRINCIPAL_CHARACTER" for s in register["scenes"]): errors.append("POV_SCOPE_INVALID")
    prose=(ROOT/"manuscript/2016-jake-arc/THE_MEASURE_OF_REPAIR_NONCANON.md").read_text().lower()
    present=[x for x in ["austin","kevin","jordan","phillip","2017","champion","championship"] if x in prose]
    if present: errors.append("FOREKNOWLEDGE_OR_UNBOUND_PRINCIPAL:"+",".join(present))
    result={"scope":"ALL_2016_TEAM_1_EVENTS","expected_events":len(expected),"linked_events":len(actual),"scene_count":len(register["scenes"]),"errors":errors,"status":"PASS" if not errors else "FAIL"}
    (ROOT/"review/2016_JAKE_ARC_CHECK.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2)); return int(bool(errors))
if __name__=="__main__": raise SystemExit(main())
