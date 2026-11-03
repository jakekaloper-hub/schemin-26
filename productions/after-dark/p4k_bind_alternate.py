#!/usr/bin/env python3
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2]
D=R/"productions/after-dark"
p=D/"fixtures/p4i_six_page_reference_bindings.json"
d=json.loads(p.read_text())
asset=R/"canon/characters/assets/CHAR-DAVID-BABB/primary/COMMISSIONER_2026-10-12.png"
expected="33e70a9208b47692d9d883707236a2b3a670629e0cb3b3f84c61eacff20fea37"
actual=hashlib.sha256(asset.read_bytes()).hexdigest()
assert actual==expected
d["verified_alternate_babb_reference"]={"path":str(asset.relative_to(R)),"sha256":actual,"repository_bytes_verified":True,"source":"memo-os/week-5/production-evidence/WEEK_5_CHARACTER_SOURCE_ASSET_RECEIPTS_2026-10-13.json","identity_use":"CONTROLLED_VISUAL_CANDIDATE","active_primary_supersession":False}
for item in d["pages"]:
 if item["page"]>=2:
  item["alternate_reference_path"]=str(asset.relative_to(R))
  item["alternate_reference_authority"]="HASH_VERIFIED_NOT_ACTIVE_PRIMARY"
  item["final_render_authorized"]=False
d["gates"]["alternate_babb_asset"]="PASS_EXACT_REPOSITORY_BYTES"
d["gates"]["canonical_primary_supersession"]="HOLD"
d["gates"]["final_cinematic_generation"]="BLOCKED"
out=D/"fixtures/p4k_reconciled_reference_bindings.json"
out.write_text(json.dumps(d,indent=2)+"\n")
print("P4K alternate asset verified and bound to pages 2–6; canon hold preserved")
