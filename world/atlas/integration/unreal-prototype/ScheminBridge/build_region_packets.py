"""Source-backed region scene descriptors; no fabricated terrain geometry."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def compile_regions(regions,world):
 if regions.get("coordinate_space")!=world.get("coordinate_space"):raise ValueError("coordinate space mismatch")
 locations=world["locations"]
 ids={r["id"] for r in regions["regions"]}
 if len(ids)!=len(regions["regions"]):raise ValueError("duplicate regions")
 if any(x["region"] not in ids for x in locations):raise ValueError("unknown region in Atlas manifest")
 packets=[]
 for region in regions["regions"]:
  env=region["environment"]
  packets.append({"region_id":region["id"],"region_name":region["name"],
    "source_canon_status":region["canon_status"],"terrain_source_terms":env["terrain"],
    "climate_source_terms":env["climate"],"movement_source_terms":env["movement"],
    "neighbor_ids":region["adjacent_region_ids"],
    "location_ids":sorted(x["id"] for x in locations if x["region"]==region["id"]),
    "visual_geometry_status":"NOT_AUTHORED","metric_dimensions":"UNRESOLVED",
    "source_provenance":region["provenance"],"publishable":False})
 return {"schema_version":"schemin.region.preview.v0.1","source_commit":world["source_commit"],"regions":packets}
if __name__=="__main__":
 raw=(ROOT/"canonical_regions_snapshot.json").read_bytes()
 data=json.loads(raw)
 world=json.loads((ROOT/"generated/world_preview_manifest.json").read_text())
 result=compile_regions(data,world)
 result["source_sha256"]=hashlib.sha256(raw).hexdigest()
 (ROOT/"generated/region_environment_packets.json").write_text(json.dumps(result,indent=2)+"\n")
 print("REGION_PACKETS_GENERATED",len(result["regions"]))
