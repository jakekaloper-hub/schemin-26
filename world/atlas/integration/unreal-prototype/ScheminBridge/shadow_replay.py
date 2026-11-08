"""Read-only historical world-state replay proposal; never write into canonical data."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
EXPECTED="6612d7c965bf804770b5b60edfa35a381573128f069c4472bf2b7ec168c5aafa"
def replay(event_id, events_path=ROOT/"canonical_events_snapshot.json",locations_path=ROOT/"canonical_locations_snapshot.json"):
    raw=Path(events_path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise ValueError("events snapshot integrity failed")
    events=json.loads(raw).get("events",[])
    match=[x for x in events if x.get("id")==event_id]
    if len(match)!=1:raise ValueError("missing or ambiguous event")
    event=match[0]
    locations=json.loads(Path(locations_path).read_text())["locations"]
    location=next((x for x in locations if x["id"]==event["location_id"]),None)
    if not location:raise ValueError("event location missing from pinned canonical locations")
    if event.get("classification")!="WORLD_CANON":raise ValueError("not a WORLD_CANON event")
    return {"mode":"SHADOW_PREVIEW_ONLY","source_commit":"7afe7ef0fcf24e25d67ca8c85d4e6e36e03a78e3","event_id":event_id,
        "location_id":location["id"],"location_name":location["name"],"event_type":event["event_type"],
        "entering_state":event["entering_state"],"continuity_out":event["continuity_out"],"week":event["week"],
        "mutates_world_state":False,"canon_approved":False}
if __name__=="__main__":
    output=replay("EVT-W3-BRIDGE")
    (ROOT/"examples"/"week3_bridge_shadow.json").write_text(json.dumps(output,indent=2)+"\n")
    print("SHADOW_REPLAY_CREATED",output["event_id"],output["location_id"])
