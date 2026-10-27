#!/usr/bin/env python3
"""Read-only publication timeline from derived identity index; no release promotion."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
obj=json.loads((root/"governance/publication-manifest/PUBLICATION_MANIFEST_V1.json").read_text())
rows=[]
for p in obj["publications"]:
 rows.append({k:p.get(k) for k in ["publication_id","family","season","title","release_state","publication_date","canonical_artifact","authority_refs","release_receipt_refs"]})
(root/"docs/visual/publications-data.json").write_text(json.dumps({"role":obj.get("manifest_role"),"authority_warning":obj.get("authority_rule"),"publications":rows},indent=2)+"\n")
print("PUBLICATIONS",len(rows),"BY_STATE", {x:sum(p["release_state"]==x for p in rows) for x in sorted({p["release_state"] for p in rows})})
