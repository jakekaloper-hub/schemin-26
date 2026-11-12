#!/usr/bin/env python3
"""Bullpen season adapter: all nine 2026 Schemin memo cycles.

This adapter never reconstructs missing PDF binaries. W1/W2 are issue nodes with
explicit external-binary gaps. W3-W9 matchup facts are adapted from the strongest
repo-native source listed in season_2026_memo_registry.json.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"planning/story-production-graph"
REGISTRY=BASE/"season_2026_memo_registry.json"
sys.path.insert(0,str(BASE))

TEAM={
 "ObiWan Jacoby":(1,"CHAR-JAKE-KALOPER"),
 "Red Leopards":(2,"CHAR-KEVIN-ZEEK"),
 "Slob on my Dobb":(3,"CHAR-JORDAN-HOLLINGSHEAD"),
 "The LLC":(4,"CHAR-DAVID-BABB"),
 "The LLC.":(4,"CHAR-DAVID-BABB"),
 "D0nkey K0ng":(5,"CHAR-WILSON-LOOK"),
 "Donkey Kong":(5,"CHAR-WILSON-LOOK"),
 "Three Dreaded Snake":(6,"CHAR-PHILLIP-PITTS"),
 "The Chili Cheesers":(7,"CHAR-BRANDON-PRYOR"),
 "The Chili Cheesers ":(7,"CHAR-BRANDON-PRYOR"),
 "Chili Cheesers":(7,"CHAR-BRANDON-PRYOR"),
 "His Majesty's Blood":(8,"CHAR-AUSTIN-BYARS"),
 "El Niño":(9,"CHAR-MANNING-WELTY"),
 "Mud Dogs":(10,"CHAR-BOBBY-MITCHELL"),
 "Seven Deadly Chins":(11,"CHAR-BEN-WHIPPLE"),
 "Dr. Duckhook":(12,"CHAR-ZACH-WILSON"),
}
CANON_NAME={v[0]:k.rstrip(". ") for k,v in TEAM.items()}
CANON_NAME.update({4:"The LLC",5:"D0nkey K0ng",7:"The Chili Cheesers"})

def read_json(path): return json.loads((ROOT/path).read_text())
def read_text(path): return (ROOT/path).read_text()

def issue_nodes():
    reg=json.loads(REGISTRY.read_text())
    return [{
      "schema_version":"1.0",
      "issue_id":w["issue_id"],"season":2026,"week":w["week"],
      "source_class":w["source_class"],"publication_state":w["publication_state"],
      "canonical_artifact":w["canonical_artifact"],"page_count":w["page_count"],
      "authority_refs":w["authority_refs"],"coverage_state":w["coverage_state"],
      "binary_in_repo":w["binary_in_repo"],
    } for w in reg["weeks"]]

def event(week,idx,home,away,home_score,away_score,winner_side,source,status="PROVISIONAL",canon="BRANCHABLE",extra=None):
    hid,hchar=TEAM[home]; aid,achar=TEAM[away]
    winner=home if winner_side=="HOME" else away
    out={
      "schema_version":"1.0",
      "event_id":f"EVT-2026-W{week:02d}-M{idx:02d}",
      "event_type":"MATCHUP",
      "league_time":{"season":2026,"week":week,"occurred_at":None},
      "authority":{"evidence_status":status,"source_receipts":[source],"canon_status":canon},
      "participants":[
        {"entity_type":"CHARACTER","entity_id":hchar},
        {"entity_type":"CHARACTER","entity_id":achar},
        {"entity_type":"TEAM","entity_id":str(hid)},
        {"entity_type":"TEAM","entity_id":str(aid)},
      ],
      "result":{"home_team_id":hid,"home_name":home,"home_score":float(home_score),"away_team_id":aid,"away_name":away,"away_score":float(away_score),"winner_side":winner_side,"winner":winner},
      "state":{"branch_state":"SETTLED" if canon=="ACCEPTED" else ("HOME_WIN" if winner_side=="HOME" else "AWAY_WIN"),"knowledge_cutoff":f"2026-W{week:02d}-source","world_writeback_allowed":False},
      "dependencies":[source],
      "notes":[],
    }
    if extra: out["notes"].extend(extra)
    return out

def week3_events():
    path="memo-os/week-3/WEEK_3_FACT_LOCK_V1.md"
    text=read_text(path)
    pat=re.compile(r"^- (.+?) (\d+\.\d+) def (.+?) (\d+\.\d+)\.$",re.M)
    rows=[]
    for i,m in enumerate(pat.finditer(text),1):
        winner,ws,loser,ls=m.groups()
        # Fact-lock prose is winner-first, not home/away. Preserve as home=winner for envelope only.
        rows.append(event(3,i,winner,loser,ws,ls,"HOME",path,"VERIFIED","ACCEPTED",["Source line is winner-first; home/away venue semantics not asserted by this adapter."]))
    return rows

def week4_events():
    path="memo-os/week-4/publication-readiness/WEEK_04_FINAL_WRITTEN_MANUSCRIPT.md"
    text=read_text(path)
    pat=re.compile(r"\*\*Deterministic result line:\*\* (.+?) (\d+\.\d+) — (.+?) (\d+\.\d+)")
    rows=[]
    for i,m in enumerate(pat.finditer(text),1):
        winner,ws,loser,ls=m.groups()
        rows.append(event(4,i,winner,loser,ws,ls,"HOME",path,"PROVISIONAL","BRANCHABLE",["Deterministic final-manuscript result line; Week 4 publication remains BLOCKED in Publication Manifest."]))
    return rows

def week5_events():
    path="memo-os/week-5/production-evidence/WEEK_5_SIX_PAYOFF_FINAL_RESULT_BANNER_LOCK_2026-10-13.json"
    d=read_json(path); rows=[]
    for i,p in enumerate(d["pages"],1):
        home=p["home"]; away=p["away"]; winner=p["winner"].rstrip(".")
        hname=home["name"].rstrip(); aname=away["name"].rstrip()
        side="HOME" if winner.rstrip(".")==hname.rstrip(".") else "AWAY"
        rows.append(event(5,i,hname,aname,home["score"],away["score"],side,path,"VERIFIED","ACCEPTED",[p["evidence_state"]]))
    return rows

def corroborated_events(week):
    path="memo-os/week-7/WEEK_7_ESPN_PRIMARY_CORROBORATION_2026-10-27.json"
    d=read_json(path)
    block=next(x for x in d["weekly_matchup_comparisons"] if x["week"]==week)
    rows=[]
    for i,r in enumerate(block["rows"],1):
        rows.append(event(week,i,r["home_name"].rstrip(),r["away_name"].rstrip(),r["home_points"],r["away_points"],r["provider_winner"],path,"PROVISIONAL","BRANCHABLE",[d["classification"]["evidence_status"],f"fact_lock={d['classification']['fact_lock']}"]))
    return rows

def week8_events():
    path="memo-os/week-8/WEEK_8_FINAL_WEEK_9_PROVIDER_EVIDENCE_2026-11-03.json"
    d=read_json(path); rows=[]
    for i,r in enumerate(d["week8_matchups"]["matchups"],1):
        h=r["home"]; a=r["away"]
        rows.append(event(8,i,h["teamName"].rstrip(),a["teamName"].rstrip(),h["totalPoints"],a["totalPoints"],r["winner"],path,"PROVISIONAL","BRANCHABLE",["Provider-final result; repo publication/fact-release authority remains separate."]))
    return rows

def week9_events():
    from adapt_week9_matchups import compile_week9
    native=compile_week9(False)["events"]
    rows=[]
    for i,e in enumerate(native,1):
        e=dict(e)
        e["event_id"]=f"EVT-2026-W09-M{i:02d}"
        e["league_time"]={"season":2026,"week":9,"occurred_at":None}
        return_ids=[]
        # normalize participant TEAM rows are absent in Week9 adapter; keep its character/location participants
        e["dependencies"]=list(dict.fromkeys(e.get("dependencies",[])+["memo-os/week-9/WEEK_9_FINAL_SPORTS_DESK_EVIDENCE_2026-11-10.json"]))
        rows.append(e)
    return rows

def all_events():
    return week3_events()+week4_events()+week5_events()+corroborated_events(6)+corroborated_events(7)+week8_events()+week9_events()

def week6_encounters(events):
    path="memo-os/week-6/WEEK_6_SPATIAL_ACTION_PREFLIGHT_V1.json"
    d=read_json(path)
    evs=[e for e in events if e["league_time"]["week"]==6]
    out=[]
    for n,x in enumerate(d["encounters"],1):
        chars={x["home_character"],x["away_character"]}
        match=next((e for e in evs if chars.issubset({p["entity_id"] for p in e["participants"] if p["entity_type"]=="CHARACTER"})),None)
        if not match: continue
        out.append({
          "schema_version":"1.0","encounter_id":f"ENC-2026-W06-{n:02d}","event_id":match["event_id"],
          "authority":{"source_receipts":[path],"world_authority":"World Engine/Atlas active authority at build time","character_authority":"active Character Canon authority at build time"},
          "participants":[x["home_character"],x["away_character"]],
          "location":{"location_id":x["home_loc"],"entering_state_receipt":path},
          "persistent_scene_anchors":list(x["anchor_sequence"]),
          "shared_conditions":{"props":[]},
          "scene_ids":[],
          "branch_policy":{"supports_outcome_branches":False,"settled_branch":"NOT_APPLICABLE"},
          "notes":[x["activity"],*x["physical_checks"]],
        })
    return out


def week5_scenes(events):
    page_root=ROOT/"memo-os/week-5/pages"
    evs=[e for e in events if e["league_time"]["week"]==5]
    role_map={"overture":"SETUP","setup":"SETUP","escalation":"ESCALATION","payoff":"RESOLUTION"}
    out=[]
    for d in sorted(page_root.iterdir()):
        if not d.is_dir() or not re.match(r"P0(0[4-9]|1\d|2[0-7])-",d.name):
            continue
        packet=d/"PAGE_PACKET.md"
        if not packet.is_file(): continue
        text=packet.read_text()
        chars=sorted(set(re.findall(r"CHAR-[A-Z0-9-]+",text)))
        locs=re.findall(r"LOC-[A-Z0-9-]+",text)
        if len(chars)<2 or not locs: continue
        match=next((e for e in evs if set(chars[:2]).issubset({p["entity_id"] for p in e["participants"] if p["entity_type"]=="CHARACTER"})),None)
        if not match: continue
        slug=d.name.split("-",2)[-1]
        role=next((v for k,v in role_map.items() if k in slug),"TURN")
        beat_m=re.search(r"Scene beat:\s*\*\*(.+?)\*\*",text)
        beat=beat_m.group(1) if beat_m else f"Source-controlled Week 5 page packet {d.name}; adapter adds no new action."
        sid=f"SCN-2026-W05-{d.name.split('-')[0]}"
        deps=[f"{match['event_id']}::BASE",f"LOC::{locs[0]}",*[f"CHAR::{x}" for x in chars[:2]],str(packet.relative_to(ROOT))]
        if role=="RESOLUTION": deps.append(f"{match['event_id']}::RESULT")
        out.append({
          "schema_version":"1.0","scene_id":sid,"event_id":match["event_id"],"encounter_id":f"ENC-2026-W05-{match['event_id'].split('-')[-1]}",
          "scene_role":role,"branch":"SETTLED" if role=="RESOLUTION" else "COMMON",
          "authority":{"character_authority":"active Character Canon authority at build time","world_authority":"World Engine/Atlas active authority at build time","source_receipts":[str(packet.relative_to(ROOT))]},
          "cast":[{"character_id":x,"role":"PRIMARY","reference_receipts":[]} for x in chars[:2]],
          "location":{"location_id":locs[0],"entering_state_receipt":str(packet.relative_to(ROOT)),"persistent_anchors":[]},
          "continuity":{"in":[],"out":[]},
          "narrative":{"objective":beat,"emotional_objective":"","action_beats":[beat],"dialogue":[]},
          "visual":{"camera":"Source page packet controls camera/composition; unresolved fields remain upstream.","blocking":[],"foreground":[],"midground":[],"background":[],"lighting":"","weather":"","time_of_day":""},
          "state_delta":{"persistent":[],"ephemeral":[]},
          "dependencies":deps,"outputs":["PNG","MOTION","WEB","NOVEL_CONTEXT"],
          "qa":{"required_gates":["FACT","CHARACTER","WORLD","COMPOSITION","PUBLICATION"],"publication_state":"PLANNED","revision":1},
          "source_mapping":{"source_beat_ids":[d.name],"source_classifications":["WEEK5_PAGE_PACKET"],"branch_variants":["COMMON"]},
        })
    return out

def week6_scenes(events,encounters):
    ev_by={e["event_id"]:e for e in events}
    path="memo-os/week-6/WEEK_6_SPATIAL_ACTION_PREFLIGHT_V1.json"
    d=read_json(path)
    enc_by={x["event_id"]:x for x in encounters if x["encounter_id"].startswith("ENC-2026-W06-")}
    out=[]
    for i,x in enumerate(d["encounters"],1):
        chars={x["home_character"],x["away_character"]}
        match=next((e for e in events if e["league_time"]["week"]==6 and chars.issubset({p["entity_id"] for p in e["participants"] if p["entity_type"]=="CHARACTER"})),None)
        if not match: continue
        enc=enc_by.get(match["event_id"])
        sid=f"SCN-2026-W06-M{i:02d}-SPATIAL"
        out.append({
          "schema_version":"1.0","scene_id":sid,"event_id":match["event_id"],"encounter_id":enc["encounter_id"] if enc else f"ENC-2026-W06-{i:02d}",
          "scene_role":"SETUP","branch":"COMMON",
          "authority":{"character_authority":"active Character Canon authority at build time","world_authority":"World Engine/Atlas active authority at build time","source_receipts":[path]},
          "cast":[{"character_id":x["home_character"],"role":"PRIMARY","reference_receipts":[]},{"character_id":x["away_character"],"role":"PRIMARY","reference_receipts":[]}],
          "location":{"location_id":x["home_loc"],"entering_state_receipt":path,"persistent_anchors":list(x["anchor_sequence"])},
          "continuity":{"in":[],"out":[]},
          "narrative":{"objective":x["activity"],"emotional_objective":"","action_beats":list(x["action_path"]),"dialogue":[]},
          "visual":{"camera":" | ".join(x["camera_axes"]),"blocking":list(x["action_path"]),"foreground":[],"midground":[],"background":list(x["anchor_sequence"]),"lighting":"","weather":"","time_of_day":""},
          "state_delta":{"persistent":[],"ephemeral":[]},
          "dependencies":[f"{match['event_id']}::BASE",f"CHAR::{x['home_character']}",f"CHAR::{x['away_character']}",f"LOC::{x['home_loc']}",path],
          "outputs":["PNG","MOTION","WEB","NOVEL_CONTEXT"],
          "qa":{"required_gates":["FACT","CHARACTER","WORLD","COMPOSITION","PUBLICATION"],"publication_state":"PLANNED","revision":1},
          "source_mapping":{"source_beat_ids":[x["id"]],"source_classifications":["WEEK6_SPATIAL_PREFLIGHT"],"branch_variants":["COMMON"]},
        })
    return out

def week9_graph():
    from adapt_week9_matchups import compile_week9
    from adapt_week9_scenes import compile_scenes
    g=compile_week9(False)
    # map old Week9 event ids to season ids deterministically by matchup number
    mapping={f"EVT-W09-W09-M{i:02d}":f"EVT-2026-W09-M{i:02d}" for i in range(1,7)}
    enc=[]
    for x in g["encounters"]:
        y=json.loads(json.dumps(x)); y["event_id"]=mapping.get(y["event_id"],y["event_id"]); y["encounter_id"]=y["encounter_id"].replace("ENC-W09-M","ENC-2026-W09-M")
        y["scene_ids"]=[s.replace("SCN-W09-M","SCN-2026-W09-M") for s in y["scene_ids"]]
        enc.append(y)
    scenes=[]
    for x in compile_scenes():
        y=json.loads(json.dumps(x)); y["event_id"]=mapping.get(y["event_id"],y["event_id"]); y["encounter_id"]=y["encounter_id"].replace("ENC-W09-M","ENC-2026-W09-M"); y["scene_id"]=y["scene_id"].replace("SCN-W09-M","SCN-2026-W09-M")
        deps=[]
        for dep in y.get("dependencies",[]):
            for old,new in mapping.items(): dep=dep.replace(old,new)
            deps.append(dep)
        y["dependencies"]=deps
        scenes.append(y)
    return enc,scenes

def compile_season():
    events=all_events()
    w9enc,w9scenes=week9_graph()
    w6enc=week6_encounters(events)
    encounters=w6enc+w9enc
    scenes=week5_scenes(events)+week6_scenes(events,w6enc)+w9scenes
    issues=issue_nodes()
    return {
      "schema_version":"1.0",
      "season":2026,
      "issues":issues,
      "events":events,
      "encounters":encounters,
      "scenes":scenes,
      "coverage":{
        "memo_weeks":sorted(i["week"] for i in issues),
        "issue_count":len(issues),
        "matchup_event_count":len(events),
        "event_weeks":sorted(set(e["league_time"]["week"] for e in events)),
        "encounter_weeks":sorted(set(int(e["encounter_id"].split("-W")[1][:2]) for e in encounters)),
        "scene_weeks":sorted(set(s["event_id"].split("-W")[1][:2] for s in scenes)),
        "scene_count":len(scenes),
        "external_binary_gap_weeks":[i["week"] for i in issues if not i["binary_in_repo"] and i["week"] in {1,2}],
      }
    }

if __name__=="__main__":
    print(json.dumps(compile_season(),indent=2,ensure_ascii=False))
