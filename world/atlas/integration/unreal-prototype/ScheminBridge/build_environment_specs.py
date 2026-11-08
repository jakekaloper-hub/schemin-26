"""Compile source-preserving environment specifications for every Atlas location."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def compile_specs(data):
    assert data["kind"]=="UNREAL_WORLD_PREVIEW_NOT_CANON"
    seen=set(); specs=[]
    for item in data["locations"]:
        ident=item["id"]
        if ident in seen: raise ValueError("duplicate ID")
        seen.add(ident)
        landmarks=item.get("landmarks",[])
        if not isinstance(landmarks,list) or any(not isinstance(x,str) for x in landmarks):raise ValueError("invalid landmarks")
        specs.append({"location_id":ident,"source_classification":item["source_classification"],
          "region_id":item["region"],"scene_asset":"/Game/ScheminPreview/Generated/"+item["unreal_map_name"],
          "landmark_proxies":[{"source_label":x,"proxy_index":n,"geometry_status":"PLACEHOLDER_UNSCALED"} for n,x in enumerate(landmarks)],
          "art_direction_status":"NOT_APPROVED","terrain_status":"UNRESOLVED","metric_scale_status":"UNRESOLVED",
          "camera_status":"NOT_REVIEWED","character_assets_allowed":False,"publication_allowed":False})
    return {"schema_version":"schemin.environment-preview.v0.1","source_commit":data["source_commit"],"specifications":specs}
if __name__=="__main__":
    manifest=json.loads((ROOT/"generated/world_preview_manifest.json").read_text())
    out=compile_specs(manifest)
    (ROOT/"generated/environment_specs.json").write_text(json.dumps(out,indent=2)+"\n")
    print("ENVIRONMENT_SPECS_GENERATED",len(out["specifications"]))
