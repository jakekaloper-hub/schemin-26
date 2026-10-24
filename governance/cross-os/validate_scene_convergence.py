"""Cross-OS scene packet structural compatibility test; NOT art or human approval."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CONTRACT=ROOT/"governance/cross-os/SCENE_CONVERGENCE_CONTRACT_V1.json"
CANONICAL={"memo_os","novel_os","visual_grounding","interactive_atlas","world_evolution","mercer","chronicles"}

def validate_contract(d):
    errors=[]
    if set(d.get("consumers",[]))!=CANONICAL: errors.append("all consumer domains must be covered")
    if len(d.get("consumers",[]))!=len(CANONICAL): errors.append("duplicate consumer domain")
    for x in ["character_id","character_source_ref","location_id","world_state_ref","verified_event_ref"]:
        if x not in d.get("immutable",[]): errors.append("missing immutable field "+x)
    for x in ["camera","composition","lighting","visual_treatment","narrative_purpose"]:
        if x not in d.get("creative_choices",[]): errors.append("missing creative flexibility "+x)
    if d.get("parent")!="world/atlas/integration/ATLAS_PUBLICATION_CONVERGENCE_CONTRACT_V1.json":
        errors.append("must consume existing Atlas publication authority")
    for p in [d.get("parent"),*d.get("sources",{}).values()]:
        if not isinstance(p,str) or not (ROOT/p).is_file(): errors.append("missing actual authority "+str(p))
    return errors

def validate_scene(scene,contract):
    errors=validate_contract(contract)
    if not isinstance(scene,dict): return errors+["missing scene object"]
    for field in contract["immutable"]:
        if not isinstance(scene.get(field),str) or not scene[field].strip():
            errors.append("missing shared authority: "+field)
    views=scene.get("views")
    if not isinstance(views,dict): return errors+["missing consumer views"]
    for name in ("memo_os","novel_os","visual_grounding","interactive_atlas"):
        view=views.get(name)
        if not isinstance(view,dict): errors.append("missing view "+name);continue
        for key in contract["immutable"]:
            if view.get(key)!=scene.get(key): errors.append(name+": divergent "+key)
        if not isinstance(view.get("narrative_purpose"),str) or not view["narrative_purpose"].strip():
            errors.append(name+": missing narrative purpose")
    if scene.get("world_mutation") or scene.get("private_mercer_data") or scene.get("art_claims_canon"):
        errors.append("unapproved mutation or private data in shared scene")
    return errors

if __name__=="__main__":
    c=json.loads(CONTRACT.read_text())
    errors=validate_contract(c)
    for e in errors: print("FAIL:",e)
    if not errors: print("PASS: shared scene consumer contract (structural only)")
    raise SystemExit(bool(errors))
