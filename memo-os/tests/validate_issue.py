"""Memo publication manifest guard: fail closed on deterministic defects."""
import json,sys,re
from collections import Counter

def validate(d):
    errors=[]; pages=d.get("pages",[]); expected=d.get("expected_pages",0)
    slots=[p.get("slot") for p in pages]
    if type(expected) is not int or expected<1: errors.append("expected_pages invalid")
    if len(pages)!=expected or any(type(x) is not int for x in slots) or sorted(x for x in slots if type(x) is int)!=list(range(1,expected+1)):
        errors.append("page coverage incomplete or duplicated")
    assets=[p.get("asset_sha256") for p in pages]
    if len(set(assets))!=len(assets): errors.append("duplicate page asset")
    for p in pages:
        n=p.get("slot")
        if p.get("printed_page")!=n: errors.append(f"page {n}: printed label mismatch")
        if not isinstance(p.get("asset_sha256"),str) or not re.fullmatch(r"[0-9a-fA-F]{64}",p["asset_sha256"]): errors.append(f"page {n}: missing SHA256")
        if p.get("role") not in {"RESULT","SETUP","ESCALATION","EDITORIAL","COVER"}: errors.append(f"page {n}: unknown page role")
        if p.get("role")=="RESULT":
            fact=d.get("results",{}).get(p.get("matchup_key"))
            if not fact or p.get("final_scores")!=fact: errors.append(f"page {n}: fact lock mismatch")
        if p.get("role")=="SETUP" and p.get("final_scores"): errors.append(f"page {n}: setup duplicates result")
        if p.get("characters") and p.get("character_raster_qa")!="PASS": errors.append(f"page {n}: raster identity unapproved")
        if p.get("mobile_qa")!="PASS": errors.append(f"page {n}: mobile QA unapproved")
        if p.get("technical_acceptance")!="PASS" or p.get("publication_fidelity")!="PASS":
            errors.append(f"page {n}: dual acceptance incomplete")
        if not p.get("narrative_job"): errors.append(f"page {n}: missing narrative function")
    divisions=Counter()
    members=d.get("team_divisions",{})
    for f in d.get("results",{}).values():
        winner=f.get("winner")
        if winner not in members: errors.append(f"winner missing division: {winner}")
        else: divisions[members[winner]]+=1
    highlight=d.get("division_highlight")
    if highlight and divisions:
        if highlight.get("wins")!=divisions.get(highlight.get("name")) or divisions.get(highlight.get("name"),0)!=max(divisions.values()) or sum(1 for count in divisions.values() if count==max(divisions.values()))>1:
            errors.append("division winner claim unsupported")
    if d.get("publication_state") not in ("PLANNED","REVIEW","RELEASED","PUBLISHED"):
        errors.append("unknown publication state")
    if d.get("publication_state") in ("RELEASED","PUBLISHED"):
        if d.get("pdf_page_count")!=expected: errors.append("PDF count mismatch")
        if d.get("independent_umpire_approval")!="PASS": errors.append("Umpire required")
        if not isinstance(d.get("published_artifact_sha256"),str) or not re.fullmatch(r"[0-9a-fA-F]{64}",d["published_artifact_sha256"]): errors.append("release hash missing")
    return errors

if __name__=="__main__":
    data=json.load(open(sys.argv[1],encoding="utf-8"))
    issues=validate(data)
    print(json.dumps({"verdict":"FAIL" if issues else "PASS","errors":issues},indent=2))
    sys.exit(bool(issues))
