"""Read-only Atlas travel graph; visual links are schematic, never metric paths."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def compile_graph(routes,world):
 nodes={x["id"] for x in world["locations"]}
 edges=[];seen=set()
 for route in routes["routes"]:
  rid=route["id"]
  if rid in seen:raise ValueError("duplicate route")
  seen.add(rid)
  sequence=[route["from"],*route.get("via_location_ids",[]),route["to"]]
  if any(node not in nodes for node in sequence):
   raise ValueError("route references unknown location "+rid)
  edges.append({"route_id":rid,"location_sequence":sequence,"travel_modes":route.get("travel_modes",[]),
    "constraints":route.get("constraints",[]),"canon_status":route["canon_status"],
    "source_provenance":route.get("source_provenance",[]),"physical_distance":None,
    "travel_duration":None,"approved_for_navigation":False})
 return {"schema_version":"schemin.unreal.travel-preview.v0.1","source_commit":world["source_commit"],
  "metric_navigation":False,"routes":edges}
if __name__=="__main__":
 raw=(ROOT/"canonical_routes_snapshot.json").read_bytes()
 graph=compile_graph(json.loads(raw),json.loads((ROOT/"generated/world_preview_manifest.json").read_text()))
 graph["source_sha256"]=hashlib.sha256(raw).hexdigest()
 (ROOT/"generated/travel_graph_preview.json").write_text(json.dumps(graph,indent=2)+"\n")
 print("TRAVEL_GRAPH_GENERATED",len(graph["routes"]))
