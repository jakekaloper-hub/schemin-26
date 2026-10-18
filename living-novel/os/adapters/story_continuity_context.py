"""Read-only proposed relationship and promise overlays; never elevate proposals to canon."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
GRAPH=ROOT/"living-novel/production/full-rewrite-2026/R40_TWELVE_OWNER_CROSS_CAUSAL_MAP_V1.json"
PROMISES=ROOT/"living-novel/os/promises/STORY_PROMISE_LEDGER_V1.json"
OWNERS=ROOT/"world/data/owner_domains.json"
def asof(*, character_id, scene_year, scene_week):
    if not isinstance(scene_year,int) or not isinstance(scene_week,int) or not (2015<=scene_year<=2026 and 1<=scene_week<=19):
        raise ValueError("invalid scene time")
    owners=json.loads(OWNERS.read_text())["domains"]
    selected=[o for o in owners if o["character_id"]==character_id]
    if len(selected)!=1:raise ValueError("unknown character")
    name=selected[0]["owner"].split()[0]
    graph=json.loads(GRAPH.read_text())
    facts=[];options=[];withheld=[]
    for e in graph["edges"]:
        if name not in (e["source"],e["target"]):continue
        anchor=e.get("temporal_anchor","")
        match=re.fullmatch(r"(20\\d{2}) W(\\d{1,2})(?: onward)?",anchor)
        # Annual and multiyear anchors do not certify a particular scene-week.
        if not match:
            withheld.append({"id":e["id"],"reason":"ANCHOR_NOT_WEEK_SPECIFIC"});continue
        when=(int(match.group(1)),int(match.group(2)))
        if when>(scene_year,scene_week):
            withheld.append({"id":e["id"],"reason":"FUTURE_SCENE"});continue
        row={"id":e["id"],"from":e["source"],"to":e["target"],
             "anchor":anchor,"interpretation":e.get("causal_interpretation"),
             "source_register":str(GRAPH.relative_to(ROOT)),
             "canon_transaction":False}
        if e.get("status")=="FACT":facts.append(row)
        else:options.append({**row,"status":"UNAPPROVED_PROPOSAL"})
    ledger=json.loads(PROMISES.read_text())
    return {"character_id":character_id,"scene":[scene_year,scene_week],
      "register_assertions_not_independently_verified":facts,
      "proposed_relationship_options":options,"withheld_edges":withheld,
      "story_promises":ledger["records"],"promise_register_empty":not bool(ledger["records"]),
      "relationship_to_personal_memory":"NOT_AUTOMATIC","canon_promoted":False}
