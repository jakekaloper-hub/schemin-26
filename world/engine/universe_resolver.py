#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from collections import deque

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"world"/"data"

def load(name):
    with (DATA/name).open("r",encoding="utf-8") as f:
        return json.load(f)

def _maps():
    locations=load("locations.json")["locations"]
    routes=load("routes.json")["routes"]
    domains=load("owner_domains.json")["domains"]
    memories=load("world_memory.json")["memories"]
    settlements=load("settlements.json")["settlements"]
    institutions=load("institutions.json")["institutions"]
    divisions=load("divisions.json")["divisions"]
    state=load("current_world_state.json")["locations"]
    return {
        "locations":{x["id"]:x for x in locations},
        "routes":routes,
        "domains":{x["character_id"]:x for x in domains},
        "memories":memories,
        "settlements":settlements,
        "institutions":institutions,
        "divisions":{x["id"]:x for x in divisions},
        "state":state,
    }

def where_is(character_id:str):
    m=_maps(); d=m["domains"].get(character_id)
    if not d: return None
    return {"character_id":character_id,"location_id":d["primary_location_id"],"physical_regions":d.get("physical_zone_ids",[]),"division_id":d.get("division_id")}

def who_lives(location_id:str):
    m=_maps()
    out=[]
    for s in m["settlements"]:
        if s.get("anchor_location_id")==location_id:
            out.extend(s.get("population",[]))
    return out

def routes_touch(location_id:str):
    m=_maps(); out=[]
    for r in m["routes"]:
        via=r.get("via_location_ids",[])
        if r.get("via_location_id"): via=via+[r["via_location_id"]]
        if location_id in [r.get("from"),*via,r.get("to")]:
            out.append(r["id"])
    return out

def _graph():
    m=_maps(); g={}
    for r in m["routes"]:
        via=r.get("via_location_ids",[])
        if r.get("via_location_id"): via=via+[r["via_location_id"]]
        chain=[r.get("from"),*via,r.get("to")]
        chain=[x for x in chain if x]
        for a,b in zip(chain,chain[1:]):
            g.setdefault(a,[]).append((b,r["id"]))
            g.setdefault(b,[]).append((a,r["id"]))
    return g

def how_to_travel(a:str,b:str):
    g=_graph()
    if a==b: return {"locations":[a],"routes":[]}
    q=deque([(a,[a],[])])
    seen={a}
    while q:
        node,path,routes=q.popleft()
        for nxt,rid in g.get(node,[]):
            if nxt in seen: continue
            if nxt==b: return {"locations":path+[nxt],"routes":routes+[rid]}
            seen.add(nxt); q.append((nxt,path+[nxt],routes+[rid]))
    return None

def what_happened(location_id:str):
    m=_maps()
    return [x for x in m["memories"] if x.get("location_id")==location_id]

def what_state(location_id:str):
    return _maps()["state"].get(location_id,[])

def institutions_near(location_id:str):
    m=_maps()
    return [x for x in m["institutions"] if x.get("location_id")==location_id]

def region_contains(location_id:str):
    return _maps()["locations"].get(location_id,{}).get("physical_zone_id")

def division_culture(location_id:str):
    m=_maps(); loc=m["locations"].get(location_id,{})
    did=loc.get("division_id")
    return m["divisions"].get(did,{}).get("culture_v2") if did else None

def query(kind,*args):
    table={
        "WHERE_IS":where_is,
        "WHO_LIVES":who_lives,
        "HOW_TO_TRAVEL":how_to_travel,
        "WHAT_ROUTES_TOUCH":routes_touch,
        "WHAT_HAPPENED":what_happened,
        "WHAT_STATE":what_state,
        "WHAT_INSTITUTIONS_NEAR":institutions_near,
        "WHAT_REGION_CONTAINS":region_contains,
        "WHAT_DIVISION_CULTURE":division_culture,
    }
    if kind not in table: raise KeyError(kind)
    return table[kind](*args)

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("args",nargs="*")
    ns=p.parse_args()
    print(json.dumps(query(ns.query,*ns.args),indent=2,ensure_ascii=False))
