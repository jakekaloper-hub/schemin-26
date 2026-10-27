#!/usr/bin/env python3
"""Derived historical explorer. Week association is temporal, not causal proof."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[2]
load=lambda p:json.loads((R/p).read_text())
pub=load("governance/publication-manifest/PUBLICATION_MANIFEST_V1.json")["publications"]
events=load("world/data/world_state_events.json")["events"]
locs={l["id"]:l for l in load("world/data/locations.json")["locations"]}
weeks=sorted({e["week"] for e in events}|{w for p in pub for w in p.get("source_interval",{}).get("weeks",[])})
out=[]
for week in weeks:
 entries=[p for p in pub if week in p.get("source_interval",{}).get("weeks",[])]
 incidents=[]
 for e in events:
  if e["week"]!=week:continue
  loc=locs.get(e["location_id"])
  assert loc, e["location_id"]
  incidents.append({"id":e["id"],"classification":e["classification"],"location_id":e["location_id"],"location_name":loc["name"],"event_type":e.get("event_type"),"continuity":e.get("continuity_out",[]),"provenance":e.get("source_provenance",[])})
 out.append({"week":week,"publications":[{"id":p["publication_id"],"title":p["title"],"family":p["family"],"status":p["release_state"],"relations":p.get("relations",[]),"authority":p.get("authority_refs",[])} for p in entries],"events":incidents})
dest=R/"docs/visual/history-data.json"
dest.write_text(json.dumps({"scope":"Source-indexed 2026 weeks; not an event-level causal linkage ledger","warning":"Week co-occurrence does not establish that an event caused or appears in a specific publication. Interpretive events are not automatically physical canon.","weeks":out,"sources":["governance/publication-manifest/PUBLICATION_MANIFEST_V1.json","world/data/world_state_events.json","world/data/locations.json"]},indent=2)+"\n")
print("HISTORY",len(weeks),"weeks",len(events),"events",len(pub),"total publications")
