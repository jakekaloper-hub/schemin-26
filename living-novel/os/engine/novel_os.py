"""Novel OS v0.3 core — dependency-light, repository-native."""
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
