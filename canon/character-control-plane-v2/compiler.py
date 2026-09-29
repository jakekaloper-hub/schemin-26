from dataclasses import asdict
from models import canonical_hash,QACheck
from registry import resolve
from assets import resolve_asset
from compose import compose
def compile_contract(query,records,assets,layers=(),scene=None):
    rr=resolve(query,records)
    if rr["status"]!="CURRENT_CANON_RESOLVED": return rr
    r=rr["record"]; ar=resolve_asset(r.primary_asset_id,assets) if r.primary_asset_id else {"status":"HUMAN_REVIEW_REQUIRED","reason":"NO_PRIMARY_ASSET"}
    state,trace=compose(r,list(layers))
    contract={"schema_version":"2.0","character_id":r.character_id,"active_version":r.active_version,"resolved":state,"layer_trace":trace,"asset":asdict(ar["asset"]) if "asset" in ar else None,"asset_status":ar["status"],"scene":scene or {}}
    contract["contract_hash"]=canonical_hash(contract)
    contract["render_ready"]=ar["status"]=="PASS"
    return contract
