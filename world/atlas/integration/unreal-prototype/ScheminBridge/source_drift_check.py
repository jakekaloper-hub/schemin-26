"""Read-only canonical source drift report. Does not update pinned build automatically."""
import datetime,hashlib,json,urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE="https://raw.githubusercontent.com/jakekaloper-hub/schemin-26/main/"
SOURCES={"world/data/locations.json":"canonical_locations_snapshot.json","world/data/physical_zones.json":"canonical_regions_snapshot.json","world/data/world_state_events.json":"canonical_events_snapshot.json"}
def main():
    report={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"state":"PASS","sources":[]}
    for remote,local in SOURCES.items():
        local_bytes=(HERE/local).read_bytes()
        item={"source":remote,"pinned_sha256":hashlib.sha256(local_bytes).hexdigest()}
        try:
            latest=urllib.request.urlopen(BASE+remote,timeout=12).read()
            item["main_sha256"]=hashlib.sha256(latest).hexdigest()
            item["drift"]=item["pinned_sha256"]!=item["main_sha256"]
        except Exception as ex:
            item["error"]=str(ex);report["state"]="BLOCKED"
        report["sources"].append(item)
    p=HERE/"generated/source_drift_report.json"
    p.write_text(json.dumps(report,indent=2)+"\n")
    print("SOURCE_DRIFT_REPORT",report["state"],sum(x.get("drift",False) for x in report["sources"]),"changed")
if __name__=="__main__":main()
