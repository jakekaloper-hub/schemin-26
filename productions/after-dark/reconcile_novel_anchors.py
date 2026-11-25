#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
manifest=json.loads((ROOT/"governance/publication-manifest/PUBLICATION_MANIFEST_V1.json").read_text())
releases={x["publication_id"]:x["release_state"] for x in manifest["publications"]}
approved=[x for x in manifest["publications"] if x["family"]=="living_novel" and x["release_state"] in ("CANON_CLOSED","RELEASED")]
# Family may differ in legacy records; recognize by publication identifier instead.
approved=[x for x in manifest["publications"] if x["publication_id"].startswith("novel.") and x["release_state"]=="CANON_CLOSED"]
cards=json.loads((ROOT/"productions/after-dark/fixtures/p3c_week7_week8_editorial_cards.json").read_text())
for c in cards["cards"]:
 c["approved_novel_context"]={"available_canonical_manuscripts":[{"publication_id":x["publication_id"],"artifact":x["canonical_artifact"]} for x in approved],
 "status":"APPROVED_TEXT_AVAILABLE_NOT_CHARACTER_APPEARANCE_PROOF","knowledge_boundary":"No first-person thought, itinerary or future event asserted from an unpublished proposal"}
 c["week7_result_authority"]="PROVISIONAL_2026_10_27_SOURCE_NOT_RELEASED_MEMO"
 c["week8_outcome"]="UNDECIDED"
out=ROOT/"productions/after-dark/fixtures/p3c_week7_week8_authority_reconciled_cards.json"
out.write_text(json.dumps({"status":"NONCANON_REHEARSAL_CONTEXT","release_states":releases,"cards":cards["cards"]},indent=2)+"\n")
assert len(approved)==4 and len(cards["cards"])==12
print("reconciled 12 cards with",len(approved),"approved novel anchors")
