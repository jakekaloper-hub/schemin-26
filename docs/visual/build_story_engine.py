#!/usr/bin/env python3
"""Read-only canonical Schemin storytelling lifecycle projection."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]
steps=[
("Verified league event","data-gateway/SCHEMIN_26_ESPN_INGESTION_RELIABILITY_PATCH_v1.0.md","Truth","League events must be fact-locked."),
("Freshness evidence","schemas/freshness.schema.json","Truth","Evidence freshness qualifies claims."),
("Character consequence","canon/characters/APPROVED_LINEUP_2026_10_18.json","Canon","Owner IDs and visual presentation stay fixed; renderer hold remains."),
("Geographic translation","world/data/locations.json","World","Venues and physical geography resolve from the World Engine."),
("Story architecture","memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_5_INTEGRATED_PREPRODUCTION_PATCH.md","Production","Creative interpretations depend on verified evidence."),
("Weekly Memo","governance/publication-manifest/PUBLICATION_MANIFEST_V1.json","Publication","Memo releases retain explicit status."),
("Living Novel","living-novel/NOVEL_OS.md","Production","Novel continuity uses the same world."),
("Visual production","canon/characters/T12_VISUAL_CONSUMER_ROUTING_CONTRACT.md","Production","Character rendering requires reference binding and QA."),
("World evolution","world/data/world_state_events.json","World","Recorded consequences have explicit classification."),
("Future continuity","world/data/current_world_state.json","World","The last approved world-state snapshot persists."),
]
for _,p,_,_ in steps:
 assert (R/p).is_file(),p
pub=json.loads((R/"governance/publication-manifest/PUBLICATION_MANIFEST_V1.json").read_text())
events=json.loads((R/"world/data/world_state_events.json").read_text())
state=json.loads((R/"world/data/current_world_state.json").read_text())
data={"warning":"Architecture stages are not proof that any one event completed the entire pipeline.","steps":[{"number":i+1,"title":name,"source":p,"lane":lane,"description":desc} for i,(name,p,lane,desc) in enumerate(steps)],"memos":[{"id":x["publication_id"],"status":x["release_state"]} for x in pub["publications"] if x["family"]=="weekly_memo"],"events":[{"id":x["id"],"week":x["week"],"classification":x["classification"]} for x in events["events"]],"world_state_as_of":state["as_of"]}
(R/"docs/visual/story-engine-data.json").write_text(json.dumps(data,indent=2)+"\n")
print("PASS",len(data["steps"]),"stages",len(data["memos"]),"memo identities",len(data["events"]),"events")
