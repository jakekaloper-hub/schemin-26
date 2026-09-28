"""Novel OS v1.0-rc core — dependency-light, repository-native."""
from __future__ import annotations
import json, re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

AUTHORITY_RANK={
"EXPERIMENT":0,"ORACLE":1,"PROPOSED_CANON":2,"INTERPRETATION":3,
"MANUSCRIPT_CANON":4,"WORLD_CANON":5,"VISUAL_CANON":6,"CHARACTER_CANON":7,
"HISTORICAL_RECORD":8,"VERIFIED_LEAGUE_FACT":9,"SOURCE_EVIDENCE":10,
}
WORKFLOW_STATES={"PENDING","RUNNING","PASSED","FAILED","BLOCKED"}

@dataclass
class Finding:
    code:str; severity:str; message:str; evidence:list[str]=field(default_factory=list)

def load_json(path:str|Path)->Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def save_json(path:str|Path,data:Any)->None:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+".tmp")
    tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    tmp.replace(p)

def resolve_assertions(assertions:list[dict])->dict:
    """Return winning assertion; newer never wins solely by recency."""
    if not assertions: raise ValueError("no assertions")
    ranked=sorted(assertions,key=lambda a:(AUTHORITY_RANK.get(a["authority"],-1),a.get("approved",False)),reverse=True)
    top=ranked[0]
    ties=[a for a in ranked if AUTHORITY_RANK.get(a["authority"],-1)==AUTHORITY_RANK.get(top["authority"],-1) and a.get("approved",False)==top.get("approved",False)]
    values={json.dumps(a.get("value"),sort_keys=True) for a in ties}
    if len(values)>1: return {"status":"CONFLICTED","candidates":ties}
    return {"status":"RESOLVED","assertion":top}

def build_context_pack(task:str,records:list[dict],entity_ids:set[str]|None=None,temporal_scope:str|None=None)->dict:
    entity_ids=entity_ids or set()
    chosen=[]
    for r in records:
        ids=set(r.get("entity_ids",[]))
        if entity_ids and not (ids & entity_ids): continue
        if temporal_scope and r.get("temporal_scope") not in (None,temporal_scope): continue
        chosen.append(r)
    chosen.sort(key=lambda r:AUTHORITY_RANK.get(r.get("authority","EXPERIMENT"),-1),reverse=True)
    return {"task":task,"temporal_scope":temporal_scope,"records":chosen,
            "conflicts":[r for r in chosen if r.get("status")=="CONFLICTED"],
            "unknowns":[r for r in chosen if r.get("status")=="UNKNOWN"]}

def validate_character_text(text:str)->list[Finding]:
    f=[]
    low=text.lower()
    if "obiwan jacoby" in low or "jake kaloper" in low or "trade jedi" in low:
        if re.search(r"(his|jake'?s|obiwan'?s).{0,30}championship belt",low):
            f.append(Finding("CHAR-JAKE-BELT","FATAL","Trade Jedi may not possess/wear a championship belt."))
    if "donkey kong" in low and re.search(r"\b(gorilla|ape)\b",low):
        f.append(Finding("CHAR-WILSON-SPECIES","FATAL","Donkey Kong rename must not turn Arsenal Centaur into a gorilla/ape."))
    if "his majesty's blood" in low and re.search(r"\bking\b|\bcrown\b",low):
        f.append(Finding("CHAR-BYARS-ROYAL","IMPORTANT","Team rename must not redefine Belt Keeper as a king/crowned character."))
    return f

def validate_oracle_mutation(record:dict)->list[Finding]:
    if record.get("temporal_layer")=="ORACLE" and record.get("authority") not in ("ORACLE","EXPERIMENT","PROPOSED_CANON"):
        return [Finding("ORACLE-PROMOTION","FATAL","Oracle Time cannot enter established canon without verified event ingestion.")]
    return []

def validate_promise(p:dict)->list[Finding]:
    allowed={"OPEN","DEVELOPING","PARTIALLY_PAID","PAID","ABANDONED_WITH_JUSTIFICATION"}
    out=[]
    if p.get("status") not in allowed: out.append(Finding("PROMISE-STATUS","FATAL","Invalid promise status."))
    if p.get("status")=="ABANDONED_WITH_JUSTIFICATION" and not p.get("justification"):
        out.append(Finding("PROMISE-JUSTIFICATION","IMPORTANT","Abandoned promise requires justification."))
    return out

def route(command:str)->list[str]:
    c=command.lower(); roles={"Showrunner","Librarian"}
    if any(x in c for x in ["prologue","chapter","scene","write","manuscript"]): roles|={"Literary Director","Continuity Director","Canon Guardian"}
    if any(x in c for x in ["image","visual","composition","art","reference"]): roles|={"Visual Director","Character Director","Canon Guardian"}
    if any(x in c for x in ["week","espn","league","result","trade","draft"]): roles|={"Data Director","League Historian"}
    if any(x in c for x in ["canon","audit","check","validate"]): roles|={"QA Director","Canon Guardian","Continuity Director"}
    return sorted(roles)

def can_accept(findings:list[Finding])->bool:
    return not any(x.severity in {"FATAL","IMPORTANT"} for x in findings)


# ---- Phase 4 continuity intelligence ----
def validate_timeline(events:list[dict])->list[Finding]:
    out=[]
    by_id={e["id"]:e for e in events if "id" in e}
    for e in events:
        for dep in e.get("after",[]):
            if dep not in by_id:
                out.append(Finding("TIME-MISSING-DEPENDENCY","IMPORTANT",f"{e.get('id')} depends on missing {dep}"))
                continue
            a=e.get("order"); b=by_id[dep].get("order")
            if a is not None and b is not None and a<=b:
                out.append(Finding("TIME-ORDER","FATAL",f"{e.get('id')} must occur after {dep}"))
    return out

def validate_object_state(events:list[dict])->list[Finding]:
    out=[]; holder={}
    for e in sorted(events,key=lambda x:x.get("order",0)):
        obj=e.get("object_id")
        if not obj: continue
        action=e.get("action")
        if action=="ACQUIRE": holder[obj]=e.get("actor")
        elif action=="TRANSFER":
            if holder.get(obj) not in (None,e.get("from")):
                out.append(Finding("OBJECT-POSSESSION","FATAL",f"{obj} transfer source conflicts with current holder"))
            holder[obj]=e.get("to")
        elif action=="USE" and holder.get(obj) not in (None,e.get("actor")):
            out.append(Finding("OBJECT-USE","FATAL",f"{e.get('actor')} uses {obj} held by {holder.get(obj)}"))
    return out

def validate_relationships(records:list[dict])->list[Finding]:
    out=[]; pairs={}
    for r in records:
        if not r.get("symmetric"): continue
        k=(r.get("subject"),r.get("predicate"),r.get("object"))
        pairs[k]=r
    for (s,p,o),r in pairs.items():
        if (o,p,s) not in pairs:
            out.append(Finding("REL-SYMMETRY","IMPORTANT",f"Symmetric relationship {p}: {s} ↔ {o} is incomplete"))
    return out

def validate_knowledge(events:list[dict])->list[Finding]:
    out=[]; known={}
    for e in sorted(events,key=lambda x:x.get("order",0)):
        actor=e.get("actor")
        if e.get("action")=="LEARN": known.setdefault(actor,set()).add(e.get("fact_id"))
        if e.get("action") in {"SAY","ACT_ON"} and e.get("fact_id") and e.get("fact_id") not in known.get(actor,set()):
            out.append(Finding("KNOWLEDGE-LEAK","FATAL",f"{actor} uses {e.get('fact_id')} before learning it"))
    return out

def validate_alias_identity(records:list[dict])->list[Finding]:
    out=[]
    for r in records:
        if r.get("team_name_changed") and r.get("canonical_character_before") != r.get("canonical_character_after"):
            out.append(Finding("ALIAS-IDENTITY-DRIFT","FATAL","Team rename changed canonical character identity"))
    return out

def validate_manuscript_anchor(anchor:dict,current_blob_sha:str)->list[Finding]:
    out=[]
    if anchor.get("pinned_blob_sha") and anchor["pinned_blob_sha"]!=current_blob_sha:
        out.append(Finding("MANUSCRIPT-SHA-DRIFT","FATAL","Production anchor no longer matches pinned manuscript blob SHA"))
    if not anchor.get("anchor_text"):
        out.append(Finding("MANUSCRIPT-ANCHOR-MISSING","IMPORTANT","Production record lacks manuscript anchor text"))
    return out

def validate_visual_reference(packet:dict)->list[Finding]:
    out=[]
    if packet.get("character_bearing") and not packet.get("master_canon_resolved"):
        out.append(Finding("VISUAL-CANON-UNRESOLVED","FATAL","Character-bearing visual lacks Master Canon resolution"))
    if packet.get("generated_reference") and not packet.get("approved_visual_canon"):
        out.append(Finding("VISUAL-BOOTSTRAP","FATAL","Generated image cannot bootstrap itself into Visual Canon"))
    return out

def run_deterministic_gate(candidate:dict)->list[Finding]:
    out=[]
    if "text" in candidate: out += validate_character_text(candidate["text"])
    if "oracle_record" in candidate: out += validate_oracle_mutation(candidate["oracle_record"])
    if "promise" in candidate: out += validate_promise(candidate["promise"])
    if "timeline" in candidate: out += validate_timeline(candidate["timeline"])
    if "object_events" in candidate: out += validate_object_state(candidate["object_events"])
    if "relationships" in candidate: out += validate_relationships(candidate["relationships"])
    if "knowledge_events" in candidate: out += validate_knowledge(candidate["knowledge_events"])
    if "aliases" in candidate: out += validate_alias_identity(candidate["aliases"])
    if "visual_packet" in candidate: out += validate_visual_reference(candidate["visual_packet"])
    if "temporal_record" in candidate: out += validate_temporal_firewall(candidate["temporal_record"])
    if "travel_events" in candidate: out += validate_geography(candidate["travel_events"],candidate.get("geography",{}))
    return out

# ---- Phase 5 literary workflow ----
LITERARY_PIPELINE=["RESEARCH","ARCHITECT","CHARACTER_INTENT","SCENE_DESIGN","SCRIBE",
"LITERARY_EDITOR","CONTINUITY_GUARDIAN","STYLE_GUARDIAN","LORE_GUARDIAN",
"READER_SIMULATION","ADVERSARIAL_REVIEW","REVISION","CLOSER","HUMAN_CANON_GATE"]

def literary_workflow(manuscript_id:str,mode:str="AUDIT")->dict:
    return {"workflow":"LITERARY","manuscript_id":manuscript_id,"mode":mode,
            "stages":[{"name":s,"state":"PENDING"} for s in LITERARY_PIPELINE],
            "mutation_policy":"PROPOSE_ONLY_UNTIL_FINAL_GATE"}

# ---- Phase 6 visual workflow ----
VISUAL_PIPELINE=["MANUSCRIPT_ANCHOR","BEAT","VISUAL_VALUE","VISUAL_INTENT","CANON_RETRIEVAL",
"REFERENCE_PACKET","ART_BRIEF","COMPOSITION","GENERATION","VISUAL_QA","CONTINUITY_QA","APPROVAL"]

def visual_workflow(beat_id:str,character_bearing:bool=False)->dict:
    return {"workflow":"VISUAL","beat_id":beat_id,"character_bearing":character_bearing,
            "stages":[{"name":s,"state":"PENDING"} for s in VISUAL_PIPELINE],
            "reference_gate_required":character_bearing}

# ---- Phase 7 live-season transaction ----
LIVE_PIPELINE=["SOURCE_INGESTION","VERIFICATION","SIGNIFICANCE_GRADING","HISTORICAL_CONTEXT",
"CHARACTER_CONSEQUENCE","WORLD_TRANSLATION","STORY_ARCHITECTURE","SCENE_BEAT_DESIGN",
"MANUSCRIPT","EDITORIAL","CONTINUITY_AUDIT","CANON_PROPOSAL","APPROVAL","STATE_UPDATE"]

def live_event_transaction(event:dict)->dict:
    if not event.get("verified"):
        return {"state":"BLOCKED","reason":"UNVERIFIED_EVENT","event_id":event.get("id")}
    return {"state":"READY","event_id":event.get("id"),"temporal_layer":"BOOK_TIME",
            "stages":[{"name":s,"state":"PENDING"} for s in LIVE_PIPELINE],
            "rule":"RESULT_DETERMINES_EVENT_WRITERS_DETERMINE_MEANING"}


# ---- Phase 9/10 hardening ----
def validate_temporal_firewall(record:dict)->list[Finding]:
    lock=record.get("temporal_lock")
    facts=record.get("facts",[])
    out=[]
    if lock=="AFTER_2026_DRAFT_BEFORE_WEEK_1_RESULTS":
        for fact in facts:
            if fact.get("season")==2026 and fact.get("week",0)>=1 and fact.get("kind") in {"RESULT","STANDING","SCORE","OUTCOME"}:
                out.append(Finding("TEMPORAL-FUTURE-LEAK","FATAL","Week 1+ result leaked into pre-Week-1 Prologue context."))
    return out

def validate_geography(events:list[dict],graph:dict)->list[Finding]:
    out=[]
    for e in events:
        if e.get("action")!="TRAVEL": continue
        a,b=e.get("from"),e.get("to")
        if not a or not b: continue
        edge=graph.get(a,{}).get(b)
        if edge is None:
            out.append(Finding("GEO-UNKNOWN-ROUTE","IMPORTANT",f"No approved route {a} → {b}."))
            continue
        if e.get("elapsed_hours") is not None and edge.get("min_hours") is not None and e["elapsed_hours"]<edge["min_hours"]:
            out.append(Finding("GEO-IMPOSSIBLE-TRAVEL","FATAL",f"{a} → {b} requires at least {edge['min_hours']}h."))
    return out

def approval_transaction(proposal:dict,findings:list[Finding],approver:str|None=None)->dict:
    if not can_accept(findings):
        return {"state":"BLOCKED","proposal_id":proposal.get("id"),"finding_codes":[f.code for f in findings]}
    if not approver:
        return {"state":"PENDING_APPROVAL","proposal_id":proposal.get("id")}
    return {"state":"APPROVED","proposal_id":proposal.get("id"),"approver":approver,
            "authority":proposal.get("proposed_authority","PROPOSED_CANON")}

def validate_artifact_record(r:dict)->list[Finding]:
    out=[]
    for key in ("id","path","domain","authority","status"):
        if not r.get(key): out.append(Finding("ARTIFACT-REQUIRED","IMPORTANT",f"Artifact missing {key}."))
    if r.get("authority") not in AUTHORITY_RANK and r.get("authority") not in {"BINDING","PRODUCTION_AUTHORITY","BENCHMARK","HISTORICAL_BASELINE"}:
        out.append(Finding("ARTIFACT-AUTHORITY","IMPORTANT","Unknown artifact authority class."))
    return out

def semantic_guardian_request(task:str,context_pack:dict,candidate_text:str)->dict:
    return {"task":task,"context_pack":context_pack,"candidate_text":candidate_text,
            "required_checks":["motive_attribution","voice_drift","theme_contradiction","world_rule_contradiction",
                               "unsupported_specificity","future_knowledge"],
            "state":"REQUIRES_MODEL_REVIEW","canon_mutation":False}

def release_gate(checks:dict)->dict:
    required={"regression_tests","adversarial_campaign","prologue_integration","artifact_registry",
              "approval_gate","recovery_runbook","ci"}
    missing=sorted(required-set(checks))
    failed=sorted(k for k,v in checks.items() if k in required and v is not True)
    return {"state":"PASS" if not missing and not failed else "BLOCKED","missing":missing,"failed":failed}
