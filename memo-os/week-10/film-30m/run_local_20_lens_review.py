#!/usr/bin/env python3
"""Run 20 bounded, isolated *model-assisted* craft-discipline reviews via local Ollama.

Uses the existing Inklings methodological registry and 12 production reference disciplines.
Does NOT contact, impersonate or claim participation by the people named in those registries.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import time
import urllib.request
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
AUTHOR_REG=ROOT/"living-novel/consultants/ADVISOR_REGISTRY_V1.json"
SPECIALISTS=ROOT/"memo-os/cinematography/PRODUCTION_SPECIALIST_REFERENCE_BENCH_V1.json"
COUNCIL_CODE=ROOT/"living-novel/consultants/author-council/inklings_workshop.py"
SCREENPLAY=json.loads((HERE/"SCREENPLAY_CANDIDATE_V1.json").read_text())
STORYBOARD=json.loads((HERE/"film_storyboard_v1.json").read_text())
authors=json.loads(AUTHOR_REG.read_text())
bench=json.loads(SPECIALISTS.read_text())
scene_by_page={x["source_folio"]:x for x in SCREENPLAY["scene_scripts"]}
board_by_page={x["folio"]:x for x in STORYBOARD["scenes"]}
MODEL="qwen3:8b"
API="http://127.0.0.1:11434/api/generate"
TAGS="http://127.0.0.1:11434/api/tags"
model_tags=json.load(urllib.request.urlopen(TAGS,timeout=5))["models"]
digest=next((m["digest"] for m in model_tags if m["name"]==MODEL),None)
if not digest:raise RuntimeError("Expected installed local model unavailable; no remote fallback")

# Assign narrow, non-overlapping evidence. These names label recorded craft domains, not active personal consultants.
specialist_focus={
"Doug Chiang":("W10-P22","production design: one field throne set, stairs, chair, surviving battery"),
"Dylan Cole":("W10-P11","environment: spatially differentiated storm regions"),
"Joe Letteri":("W10-P12","character VFX: three heads on exactly one body"),
"Ngila Dickson":("W10-P10","costume continuity: travel and mud across distinct sets"),
"Andy Serkis":("W10-P07","performance: wounded pride after a publicly visible capture"),
"Rob Alonzo":("W10-P06","stunt mechanics: rope on torso, sliding boot, manual knot after fall"),
"James Baxter":("W10-P15","character silhouette: four legs, dog and truck separated"),
"Frank Masi":("W10-P19","unit stills: practical warm birthday light and eyeline continuity"),
"John Knoll":("W10-P24","VFX chain: first disabled battery, second surviving battery and hand signal"),
"Jill Bogdanowicz":("W10-P09","color: coast vs Central Basin temporal exposures"),
"Thelma Schoonmaker":("W10-P13","editing: true pause and comic choice"),
"Randy Thom":("W10-P14","sound: independent compressor, waterfall, speaker and drill stems")
}
author_focus=[
("jrr_tolkien","W10-P11","lived-in world; topology and historical materiality"),
("cs_lewis","W10-P23","moral choice, temptation and cost"),
("george_rr_martin","W10-P04","ensemble consequences and opposing perspectives"),
("jk_rowling","W10-P20","setup/payoff and delayed prop reveal"),
("john_grisham","W10-P27","narrative propulsion through documentary data"),
("ursula_k_le_guin","W10-P03","institutional voice and ordinary life"),
("brandon_sanderson","W10-P24","clear power rules and causal consequences"),
("joe_abercrombie","W10-P10","human-scale emotion and ambiguous next choice")
]
lens=[]
for name,(page,focus) in specialist_focus.items():
    lens.append({"advisor":name,"page":page,"focus":focus,"kind":"production_method"})
for aid,page,focus in author_focus:
    assert aid in authors["author_council"]["core_eight"]
    lens.append({"advisor":aid,"page":page,"focus":focus,"kind":"author_method"})
assert len(lens)==20 and len({x["advisor"] for x in lens})==20
assert len(bench["profiles"])==12
assert set(specialist_focus)=={p["name"] for p in bench["profiles"]}

def query(data):
    request=urllib.request.Request(API,data=json.dumps(data).encode("utf-8"),headers={"Content-Type":"application/json"})
    return json.load(urllib.request.urlopen(request,timeout=100))

raw=HERE/"LOCAL_MODEL_20_LENS_RAW.jsonl"
raw.write_text("")
findings=[]
failures=[]
for i,l in enumerate(lens,1):
    p=l["page"]
    s=scene_by_page[p]; b=board_by_page[p]
    compact=[{"shot":sh["id"],"action":sh["blocking"][:240]} for sh in b["shots"] if sh["source_kind"]=="source"]
    review_context={
        "page":p,"title":b["title"],"official_source_text":s["source_unchanged_body"],
        "film_vo_candidate":s["narrator_film_candidate"],
        "audition_only_fictional_dialogue":s["dialogue_proposal"],
        "source_beats":compact,
        "time_logic":b["time_logic"],
        "forbidden_changes":b["forbidden_mutations"],
        "planned_picture_seconds":b["duration_s"],
        "rights_and_appearance_status":"Film unrendered; personal/character references are source-locked but not approved for model output.",
        "site":b["setting"]
    }
    system=("You are a bounded technical and editorial film reviewer applying one registered published-method craft domain. "
            "You are NOT the named real person, not connected to that person, not a fictional character, and not an authorized Bullpen Director. "
            "Preserve all given canon and factual outcomes. Review only the frozen source scene and film supplement. "
            "One practical intervention, no invented league result, no claim a render already exists, no change to canon. "
            "Return strictly JSON with fields observation, proposal, decision, rationale, acceptance_test. "
            "decision must be ACCEPT, ADAPT, HOLD, or REJECT. Keep the other four fields concise.")
    prompt=("Reviewer discipline: "+l["focus"]+"\n"
            "Please identify a specific quality risk or improvement for this screenplay/film storyboard scene, with concrete action and a test. "
            "If appearance, simulation, audio, CGI or rights have not been tested, choose HOLD where those specific outputs are required. "
            "Do not claim real-person review or signoff.\n"
            "EVIDENCE:\n"+json.dumps(review_context,ensure_ascii=False))
    args={
      "model":MODEL,
      "system":system,
      "prompt":prompt,
      "stream":False,
      "think":False,
      "format":"json",
      "options":{"temperature":0.15,"num_predict":240,"seed":1000+i,"top_p":0.8}
    }
    try:
        st=time.monotonic();out=query(args)
        text=out.get("response","").strip()
        result=json.loads(text)
        keys=("observation","proposal","decision","rationale","acceptance_test")
        if not all(isinstance(result.get(k),str) and result[k].strip() for k in keys):
            raise ValueError("Incomplete structured review")
        if result["decision"] not in ("ACCEPT","ADAPT","HOLD","REJECT"):
            raise ValueError("Invalid decision")
        finding={
          "id":f"W10-SCRIPT-MODEL-{i:02d}",
          "advisor":l["advisor"],
          "observation":result["observation"],
          "source_anchor":s["source_request"],
          "proposal":result["proposal"],
          "decision":result["decision"],
          "rationale":result["rationale"],
          "acceptance_test":result["acceptance_test"]
        }
        findings.append(finding)
        receipt={
          "lens":l,
          "source_sha256":s["source_sha256"],
          "model":MODEL,"model_digest":digest,
          "prompt_sha256":hashlib.sha256((system+prompt).encode()).hexdigest(),
          "duration_ms":round((time.monotonic()-st)*1000),
          "eval_tokens":out.get("eval_count"),
          "output":result,
          "status":"LOCAL_MODEL_REVIEW_COMPLETED_NOT_HUMAN"
        }
        print(f"[{i:02d}/20] {l['advisor']}: {result['decision']} ({receipt['duration_ms']}ms)",flush=True)
    except Exception as exc:
        failures.append({"advisor":l["advisor"],"reason":str(exc)})
        receipt={"lens":l,"source_sha256":s["source_sha256"],"model":MODEL,
                 "status":"REVIEW_FAILED_UNRESOLVED","error":str(exc)}
        print(f"[{i:02d}/20] {l['advisor']}: FAILED {str(exc)[:100]}",flush=True)
    with raw.open("a") as file:file.write(json.dumps(receipt,ensure_ascii=False)+"\n")

if not findings:raise RuntimeError("No live model outputs; do not fabricate council session")
workshop={
 "assignment_id":"S26-W10-FILM-LIVE-LOCAL-MODEL-DISCIPLINE-20261122",
 "production":"memo-os",
 "evidence_sha":hashlib.sha256((ROOT/"memo-os/week-10/preproduction/render-inputs/manifest.json").read_bytes()).hexdigest(),
 "decision_question":"Can the proposed Week 10 film screenplay and 42-second M01 stunt proof be advanced without violating source truth, physical blocking and soundtrack requirements?",
 "synthesis":"Keep independent source-level storyline, distinguish sports fact VO from fictional in-world lines, hold expensive action/character/VFX approval until actual pixel/sound QA, use the simplest existing runtime and preserve the original memo.",
 "findings":findings,
 "provenance":"Actual isolated Qwen3:8b local inference calls using twenty published-method *lenses*, not direct consultation with any named person."
}
(HERE/"LOCAL_MODEL_20_LENS_INPUT.json").write_text(json.dumps(workshop,ensure_ascii=False,indent=2)+"\n")
spec=importlib.util.spec_from_file_location("inklings_workshop",ROOT/"living-novel/consultants/author-council/inklings_workshop.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
try:
    result=m.reconcile(workshop,authors,bench)
except Exception as exc:
    result={"status":"BLOCKED","reason":str(exc),"umpire":"PENDING","canon_promoted":False}
result["execution_note"]="Twenty local Qwen3 model queries were run independently where successful. The named authors and production professionals did not participate. Umpire remains pending."
result["failed_reviews"]=failures
result["model"]=MODEL
result["model_digest"]=digest
result["source_of_truth"]="frozen project source files"
(HERE/"LOCAL_MODEL_20_LENS_RECONCILIATION.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
summary={"status":result["status"],"requested":20,"completed":len(findings),"failed":len(failures),
  "decisions":{k:sum(x["decision"]==k for x in findings) for k in ("ACCEPT","ADAPT","HOLD","REJECT")},
  "actual_model":MODEL,"digest":digest,"umpire":"PENDING",
  "real_human_consultation":False,
  "full_film_review_approved":False}
(HERE/"LOCAL_MODEL_REVIEW_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2),flush=True)
