#!/usr/bin/env python3
"""Structural/source check for the bounded 2015 connected-account candidate."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "manuscript/2015-jake-week1/SCENE_REGISTER.json"
TEXT = ROOT / "manuscript/2015-jake-week1/THE_FIRST_DEBT_NONCANON.md"
FIXTURES = ROOT / "evidence/2015_FIXTURE_COVERAGE.json"

def main() -> int:
    errors=[]
    register=json.loads(REGISTER.read_text())
    fixtures=json.loads(FIXTURES.read_text())
    event=next((row for row in fixtures["events"] if row["event_id"]=="ESPN1417621-2015-P01-E002"),None)
    if event is None: errors.append("EVENT_MISSING")
    else:
        expected={"home_team_id":event["home_id"],"away_team_id":event["away_id"],"home_score":event["home_score"],"away_score":event["away_score"],"winner":event["winner"]}
        if any(register["source_facts"].get(k)!=v for k,v in expected.items()): errors.append("SOURCE_FACT_MISMATCH")
    scenes=register.get("scenes", [])
    if len(scenes)!=3: errors.append("SCENE_COUNT_INVALID")
    if any(scene.get("pov_character_id")!="CHAR-JAKE-KALOPER" for scene in scenes): errors.append("POV_NOT_JAKE")
    if any(scene.get("pov_class")!="PRINCIPAL_CHARACTER" for scene in scenes): errors.append("POV_CLASS_INVALID")
    if any(scene.get("source_event_ids")!=["ESPN1417621-2015-P01-E002"] for scene in scenes): errors.append("EVENT_SCOPE_INVALID")
    if "user" not in register.get("identity_authority",{}).get("user_attestation","").lower(): errors.append("USER_ATTESTATION_MISSING")
    prose=TEXT.read_text()
    forbidden=["Austin", "Kevin", "Jordan", "Phillip", "2016", "2024", "2025", "champion", "championship"]
    present=[word for word in forbidden if word.lower() in prose.lower()]
    if present: errors.append("FOREKNOWLEDGE_OR_UNBOUND_PRINCIPAL:"+",".join(present))
    payload={"scope":"ONE_2015_EVENT_BOUNDED_CONNECTED_ACCOUNT_CANDIDATE","checked_event":"ESPN1417621-2015-P01-E002","scene_count":len(register["scene_ids"]),"errors":errors,"status":"PASS" if not errors else "FAIL"}
    out=ROOT/"review/2015_JAKE_CONNECTED_ACCOUNT_CHECK.json"
    out.write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps(payload,indent=2))
    return 0 if not errors else 1

if __name__=="__main__": raise SystemExit(main())
