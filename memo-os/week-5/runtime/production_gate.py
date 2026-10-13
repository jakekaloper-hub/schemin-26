"""Week 5 mandatory preflight. No renderer invocation from a failed manifest or missing receipts.

Usage:
    python -m memo_os.week5.runtime.production_gate   # not applicable: hyphen paths
    python memo-os/week-5/runtime/production_gate.py P004 --repo-root .
    python memo-os/week-5/runtime/production_gate.py P004 --repo-root . --evidence path.json

This is a CLI access gate. It deliberately does not claim to control ChatGPT's
built-in image-generation endpoint; only registered callers which invoke this
entrypoint before generation are governed.
"""
import argparse
import hashlib
import json
from pathlib import Path

WEEK_DIR = Path(__file__).resolve().parents[1]
MANIFEST = WEEK_DIR / "PUBLICATION_PAGE_MANIFEST.json"
CHARACTERS = WEEK_DIR / "production-evidence" / "WEEK_5_CHARACTER_SOURCE_ASSET_RECEIPTS_2026-10-13.json"
TITLE = WEEK_DIR / "production-evidence" / "WEEK_5_CHARACTER_AND_TITLE_RENDER_GATES_2026-10-13.json"

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def check(page_id, evidence=None, repo_root=None):
    root = Path(repo_root) if repo_root else WEEK_DIR.parents[1]
    manifest = read_json(MANIFEST)
    page = next((p for p in manifest["pages"] if p["page_id"] == page_id), None)
    if not page:
        return {"state":"GENERATION_BLOCKED","reason":"UNKNOWN_PAGE","page_id":page_id}
    if not page.get("render_eligible", False):
        return {"state":"GENERATION_BLOCKED","reason":"MANIFEST_RENDER_INELIGIBLE","page_id":page_id}
    if not isinstance(evidence, dict):
        return {"state":"GENERATION_BLOCKED","reason":"RENDER_EVIDENCE_MISSING","page_id":page_id}
    titles = read_json(TITLE)
    row = next(x for x in titles["pages"] if x["page_id"] == page_id)
    if evidence.get("page_id") != page_id or evidence.get("visible_primary_header") != row["display_header"]:
        return {"state":"GENERATION_BLOCKED","reason":"PAGE_TITLE_OR_ID_MISMATCH","page_id":page_id}
    if evidence.get("renderer_capability_state") != "CAPABILITY_VERIFIED":
        return {"state":"GENERATION_BLOCKED","reason":"RENDERER_CAPABILITY_NOT_VERIFIED","page_id":page_id}
    refs = evidence.get("references")
    if not isinstance(refs,list):
        return {"state":"GENERATION_BLOCKED","reason":"MOUNT_RECEIPTS_MISSING","page_id":page_id}
    expected = {x["character_id"]:x["raw_sha256"] for x in row["owner_reference_requirements"]}
    actual = {x.get("character_id"):x for x in refs if isinstance(x,dict)}
    if set(actual)!=set(expected) or len(refs)!=len(expected):
        return {"state":"GENERATION_BLOCKED","reason":"REFERENCE_SET_MISMATCH","page_id":page_id}
    for cid,sha in expected.items():
        e=actual[cid]
        if e.get("source_sha256")!=sha or e.get("mounted_sha256")!=sha:
            return {"state":"GENERATION_BLOCKED","reason":"REFERENCE_HASH_MISMATCH","page_id":page_id}
        if not all(isinstance(e.get(k),str) and e.get(k) for k in ("mount_receipt_id","generation_reference_id","subject_binding_id")):
            return {"state":"GENERATION_BLOCKED","reason":"REFERENCE_BINDING_MISSING","page_id":page_id}
    for k in ("mount_receipt_id","generation_reference_id","subject_binding_id"):
        if len(set(actual[c][k] for c in actual))!=len(actual):
            return {"state":"GENERATION_BLOCKED","reason":"REPEATED_SUBJECT_OR_MOUNT","page_id":page_id}
    if evidence.get("trusted_eligibility_state")!="GENERATION_ELIGIBLE" or not evidence.get("eligibility_token_validated_by_adapter"):
        return {"state":"GENERATION_BLOCKED","reason":"TRUSTED_ADAPTER_ELIGIBILITY_MISSING","page_id":page_id}
    return {"state":"PREFLIGHT_EVIDENCE_ACCEPTED","page_id":page_id,
            "note":"Not a QA or release acceptance. Renderer must still return execution receipts and independent pixel verdict."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("page_id")
    p.add_argument("--evidence")
    p.add_argument("--repo-root")
    args=p.parse_args()
    evidence=read_json(args.evidence) if args.evidence else None
    result=check(args.page_id,evidence,args.repo_root)
    print(json.dumps(result,sort_keys=True))
    return 0 if result["state"]=="PREFLIGHT_EVIDENCE_ACCEPTED" else 2

if __name__=="__main__":
    raise SystemExit(main())
