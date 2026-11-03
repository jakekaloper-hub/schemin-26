#!/usr/bin/env python3
"""Fail-closed P4I source and six-page render binding, no art generation."""
import json,hashlib,re
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/"productions/after-dark"
old=json.loads((D/"fixtures/p4h_reference_status.json").read_text())
primary=R/old["primary"]["path"]
crop=R/old["supplementary"]["path"]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
primary_ok=sha(primary)==old["primary"]["expected_sha256"]
crop_ok=sha(crop)==old["supplementary"]["expected_sha256"]
script=(D/"P4D_LLC_LIVE_INTERVIEW_FULL_SCRIPT.md").read_text()
folio=(D/"P4E_LLC_INTERVIEW_SIX_FOLIOS.md").read_text()
pages=re.split(r"(?=^## Page \d{2} — )",folio,flags=re.M)[1:]
assert len(pages)==6
payload={"schema":"after-dark.p4i.v1","status":"NONCANON_PREPRODUCTION","reference_results":{"babb_primary":{"expected":old["primary"]["expected_sha256"],"observed":sha(primary),"verified":primary_ok},"babb_supplementary":{"expected":old["supplementary"]["expected_sha256"],"observed":sha(crop),"verified":crop_ok,"may_supersede_primary":False},"host":{"identity_lock":"PENDING_REVIEW","source":"P4A candidate brief"},"manager":{"identity_lock":"PENDING_REVIEW","source":"P4A candidate brief"}},"studio":{"candidate_id":"CAND-AFTER-DARK-BROADCAST-HOUSE","region":"REG-CENTRAL-BASIN","exact_site":"UNKNOWN","horizon":"UNKNOWN","arrival_connector":"UNKNOWN","status":"FUTURE_UNLOCK_CANDIDATE"},"proposed_guest_movement":{"origin":"UNKNOWN","destination":"CAND-AFTER-DARK-BROADCAST-HOUSE","arrival_timing":"UNKNOWN","approved_route":False,"exit_destination":"UNKNOWN","canon_promotion":False},"pages":[]}
for i,p in enumerate(pages,1):
 lines=re.findall(r'^(?:HOST|BABB|MANAGER|PRODUCTION MANAGER): “(.+)”$',p,re.M)
 assert all(x in script for x in lines)
 payload["pages"].append({"page":i,"dimensions":[1080,1920],"script_line_matches":len(lines),"babb_on_stage":i>1,"babb_reference":"PRIMARY_REQUIRED" if i>1 else "NOT_SHOWN","host_reference":"CANDIDATE_NOT_LOCKED","manager_reference":"CANDIDATE_NOT_LOCKED","studio_reference":"CANDIDATE_NO_HORIZON","final_render_authorized":False})
assert sum(x["script_line_matches"] for x in payload["pages"])==29
payload["gates"]={"script_copy":"PASS_29_OF_29","primary_babb":"PASS" if primary_ok else "BLOCKED_MISSING_OR_HASH_MISMATCH","supplementary_crop":"PASS_NONPRIMARY" if crop_ok else "BLOCKED","host":"BLOCKED","manager":"BLOCKED","arrival_exit":"BLOCKED","studio":"BLOCKED","final_cinematic_generation":"BLOCKED"}
(D/"fixtures/p4i_six_page_reference_bindings.json").write_text(json.dumps(payload,indent=2)+"\n")
print(json.dumps(payload["gates"],indent=2))
