"""Read-only export from an exact-byte pinned canonical locations snapshot."""
import argparse, hashlib, json
from pathlib import Path
from ScheminBridge.validate import validate
SOURCE_COMMIT="7afe7ef0fcf24e25d67ca8c85d4e6e36e03a78e3"
SOURCE_SHA256="d3aa0d5fca9bf120ad8f1ecc6267f0cbce54bdf83b8117c0328c8d13cd0aeaeb"
HERE=Path(__file__).resolve().parent
SNAPSHOT=HERE/"canonical_locations_snapshot.json"
def export_location(location_id,snapshot=SNAPSHOT):
    raw=Path(snapshot).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:
        raise ValueError("pinned snapshot integrity mismatch")
    document=json.loads(raw)
    locations=document.get("locations",[])
    matches=[x for x in locations if x.get("id")==location_id]
    if len(matches)!=1:raise ValueError("location ID missing or ambiguous")
    item=matches[0]
    if item.get("canon_status")!="PERMANENT_CANON":
        raise ValueError("provisional location not allowed")
    if document.get("coordinate_space")!="schemin-local-v1 (abstract, non-metric)":
        raise ValueError("unrecognized coordinate space")
    scene={"schema_version":"0.1.0","source_repository":"jakekaloper-hub/schemin-26",
        "source_commit":SOURCE_COMMIT,"scene_id":"preview."+location_id.lower(),
        "location_id":location_id,"status":"PREVIEW","canon_approved":False,
        "mutates_world_state":False,"characters":[],"espn_event":None,"asset_bindings":[],
        "location_evidence":{"source_path":"world/data/locations.json",
            "source_record_id":location_id,"validated":True,
            "snapshot_sha256":SOURCE_SHA256},
        "source_location":{"name":item["name"],"zone_id":item["physical_zone_id"],
            "division_id":item["division_id"],"owner_character_id":item["owner_character_id"],
            "landmarks":item.get("persistent_landmarks",[]),
            "abstract_position":item.get("abstract_position",[]),
            "coordinate_space":document["coordinate_space"]}}
    errors=validate(scene)
    if errors:raise ValueError("; ".join(errors))
    return scene
def main():
    p=argparse.ArgumentParser()
    p.add_argument("location_id")
    p.add_argument("--output",type=Path,default=HERE/"examples/trade_jedi_preview.json")
    a=p.parse_args()
    scene=export_location(a.location_id)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(scene,indent=2)+"\n")
    print("PINNED_PREVIEW_EXPORTED",a.output,scene["location_id"])
if __name__=="__main__":main()
