#!/usr/bin/env python3
"""Read-only evidence graph from explicit canonical pointers; not a causal inference engine."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def read(p):return json.loads((R/p).read_text())
publications=read("governance/publication-manifest/PUBLICATION_MANIFEST_V1.json")["publications"]
locations=read("world/data/locations.json")["locations"]
events=read("world/data/world_state_events.json")["events"]
characters=read("canon/characters/APPROVED_LINEUP_2026_10_18.json")["individuals"]
nodes=[];edges=[];unresolved=[]
def add(id,kind,title,path,**other):nodes.append({"id":id,"type":kind,"title":title,"source":path,**other})
def edge(a,b,relation,path):edges.append({"from":a,"to":b,"relation":relation,"source":path,"classification":"EXPLICIT_REFERENCE"})
pub_source="governance/publication-manifest/PUBLICATION_MANIFEST_V1.json"
world_source="world/data/world_state_events.json"
loc_source="world/data/locations.json"
character_source="canon/characters/APPROVED_LINEUP_2026_10_18.json"
for p in publications:add(p["publication_id"],"publication",p["title"],pub_source,status=p["release_state"])
for l in locations:add(l["id"],"location",l["name"],loc_source,status=l.get("canon_status"))
for c in characters:add(c["character_id"],"character",c["display_title"],character_source,status="LINEUP_APPROVED_RENDERER_QA_HOLD")
for e in events:
 add(e["id"],"event",e["id"],world_source,status=e["classification"],week=e["week"],continuity=e.get("continuity_out",[]))
 edge(e["id"],e["location_id"],"RECORDED_AT",world_source)
for l in locations:
 if l.get("owner_character_id"):edge(l["id"],l["owner_character_id"],"OWNER_DOMAIN_ID",loc_source)
for p in publications:
 for rel in p.get("relations",[]):
  if rel.get("publication_id"):
   edge(p["publication_id"],rel["publication_id"],rel["type"],pub_source)
node_ids={n["id"] for n in nodes}
assert len(node_ids)==len(nodes)
assert all(e["from"] in node_ids and e["to"] in node_ids for e in edges)
for e in events:
 unresolved.append({"event":e["id"],"relation":"SPECIFIC_LEAGUE_FACT_TO_EVENT","reason":"No explicit audited event-level league fact edge in these registries."})
 unresolved.append({"event":e["id"],"relation":"SPECIFIC_MEMO_PAGE_OR_NOVEL_PASSAGE","reason":"Shared week and document provenance do not establish direct depiction or causal relation."})
data={"version":1,"scope":"explicit-source-relationships","warning":"This graph preserves explicit references only. No inferred event-to-publication or league causality.","nodes":nodes,"edges":edges,"unresolved":unresolved,"source_files":[pub_source,world_source,loc_source,character_source]}
(R/"docs/visual/evidence-graph.json").write_text(json.dumps(data,indent=2)+"\n")
print("EVIDENCE_GRAPH",len(nodes),"nodes",len(edges),"explicit edges",len(unresolved),"unresolved assertions")
