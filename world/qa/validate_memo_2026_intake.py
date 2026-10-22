"""Fail-closed integrity checks for Commissioner-supplied memo intake.
Metadata verification does not imply GitHub stores PDF bytes.
"""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
INDEX=ROOT/"governance/publication-manifest/WEEKS_04_06_COMMISSIONER_SOURCE_INTAKE_2026_10_22.json"
ATLAS=ROOT/"world/atlas/foundation/WEEKS_04_06_PUBLISHED_VISUAL_GEOGRAPHY_INTAKE_V1.json"
def validate():
    a=json.loads(INDEX.read_text())
    b=json.loads(ATLAS.read_text())
    errors=[]
    docs={x["week"]:x for x in a["files"]}
    if set(docs)!={4,5,6}:errors.append("MISSING_WEEK")
    for week,item in docs.items():
        if item.get("archive_status")!="BYTES_PENDING":errors.append(f"UNVERIFIED_ARCHIVE_PROMOTION_{week}")
        if not re.fullmatch(r"[a-f0-9]{64}",item.get("sha256","")):errors.append(f"INVALID_SHA256_{week}")
        if item.get("pages",0)<1 or item.get("size_bytes",0)<1:errors.append(f"INVALID_FILE_METADATA_{week}")
    for record in b["records"]:
        d=docs.get(record.get("week"))
        if not d:errors.append("UNKNOWN_WEEK");continue
        parts=record["pdf_pages"].split("-")
        lo=int(parts[0]);hi=int(parts[-1])
        if lo<1 or hi>d["pages"] or lo>hi:errors.append("PAGE_OUT_OF_BOUNDS")
        if record.get("canon_effect")!="NONE_AUTOMATIC" or record.get("coordinate_authority") is not False:
            errors.append("UNAUTHORIZED_CANON_PROMOTION")
    return sorted(set(errors))
if __name__=="__main__":
    problems=validate()
    if problems:raise SystemExit(";".join(problems))
    print("Memo Week 4-6 intake metadata/provenance validated; PDF bytes remain unarchived")
