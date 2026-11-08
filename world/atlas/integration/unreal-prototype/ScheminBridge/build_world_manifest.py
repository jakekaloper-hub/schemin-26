"""Generate a deterministic, non-canonical Unreal world preview manifest."""
import json,hashlib
from pathlib import Path
from ScheminBridge.export_location import SOURCE_SHA256,SOURCE_COMMIT,SNAPSHOT
HERE=Path(__file__).resolve().parent
STATUS={"PERMANENT_CANON":"CANON_SOURCE_PREVIEW","PROVISIONAL_CANON":"PROVISIONAL_PREVIEW","INTERPRETIVE_CANON":"INTERPRETIVE_PREVIEW"}
def build(snapshot=SNAPSHOT):
 raw=Path(snapshot).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError("canonical snapshot mismatch")
 source=json.loads(raw)
 if source.get("coordinate_space")!="schemin-local-v1 (abstract, non-metric)":raise ValueError("unexpected coordinate space")
 output=[];seen=set()
 for loc in sorted(source["locations"],key=lambda x:x["id"]):
  key=loc["id"];status=loc["canon_status"]
  if key in seen or status not in STATUS:raise ValueError("duplicate or unknown location classification")
  seen.add(key)
  p=loc.get("abstract_position")
  if not isinstance(p,list) or len(p)!=2 or not all(isinstance(n,(int,float)) for n in p):raise ValueError("abstract position missing")
  output.append({"id":key,"name":loc["name"],"source_classification":status,"render_classification":STATUS[status],
    "region":loc["physical_zone_id"],"owner_character_id":loc.get("owner_character_id"),
    "atlas_position_abstract":p,"landmarks":loc.get("persistent_landmarks",[]),
    "unreal_map_name":"Atlas_"+key.replace("-","_"),"characters_allowed":False,
    "spatial_scale_approved":False,"world_state_writeback":False})
 return {"schema_version":"0.1","kind":"UNREAL_WORLD_PREVIEW_NOT_CANON","source_repository":"jakekaloper-hub/schemin-26",
 "source_commit":SOURCE_COMMIT,"source_sha256":SOURCE_SHA256,"coordinate_space":source["coordinate_space"],
 "locations":output,"regions":sorted(set(x["region"] for x in output))}
if __name__=="__main__":
 result=build()
 folder=HERE/"generated";folder.mkdir(exist_ok=True)
 (folder/"world_preview_manifest.json").write_text(json.dumps(result,indent=2)+"\n")
 print("WORLD_MANIFEST_CREATED",len(result["locations"]),"locations",len(result["regions"]),"regions")
