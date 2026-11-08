import json,re,sys
from pathlib import Path
REPO="jakekaloper-hub/schemin-26"
def validate(d):
    if not isinstance(d,dict): return ["manifest object required"]
    e=[]
    checks=[
      (d.get("schema_version")=="0.1.0","invalid schema"),
      (d.get("source_repository")==REPO,"invalid repo"),
      (isinstance(d.get("source_commit"),str) and bool(re.fullmatch("[a-f0-9]{40}",d["source_commit"])),"invalid commit"),
      (all(isinstance(d.get(k),str) and bool(re.fullmatch("[a-zA-Z0-9_.:-]+",d[k])) for k in ("location_id","scene_id")),"invalid ids"),
      (d.get("status")=="PREVIEW","only PREVIEW permitted"),
      (d.get("canon_approved") is False,"canon approval blocked"),
      (d.get("mutates_world_state") is False,"world mutations blocked"),
      (d.get("characters")==[],"character assets blocked"),
      (d.get("espn_event") is None,"ESPN events blocked"),
      (d.get("asset_bindings")==[],"unverified assets blocked"),
    ]
    ev=d.get("location_evidence")
    checks.append((isinstance(ev,dict) and str(ev.get("source_path","")).startswith("world/") and isinstance(ev.get("source_record_id"),str) and bool(ev.get("source_record_id")) and ev.get("validated") is True,"verified world evidence required") if isinstance(ev,dict) else (False,"verified world evidence required"))
    return [msg for ok,msg in checks if not ok]
if __name__=="__main__":
    issues=validate(json.loads(Path(sys.argv[1]).read_text()))
    print("BLOCKED: "+", ".join(issues) if issues else "VALID PREVIEW CONTRACT (not canon approval)")
    sys.exit(2 if issues else 0)
