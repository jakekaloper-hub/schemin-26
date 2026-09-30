"""Per-request asset resolution. No global readiness flag."""
from .asset_reference import AssetReference

def resolve_assets(character_ids, asset_registry):
    results=[]
    for cid in character_ids:
        asset=asset_registry.get(cid)
        if asset is None:
            results.append({"character_id":cid,"state":"GENERATION_BLOCKED","reason":"CHARACTER_REFERENCE_NOT_RESOLVED"})
            continue
        verdict=asset.validate(cid)
        results.append({"character_id":cid,"state":"ASSET_RESOLVED" if verdict=="PASS" else "GENERATION_BLOCKED","reason":None if verdict=="PASS" else verdict,"asset":asset})
    return results

def request_state(results):
    if not results:
        return "HUMAN_REVIEW_REQUIRED"
    return "ASSETS_RESOLVED" if all(x["state"]=="ASSET_RESOLVED" for x in results) else "GENERATION_BLOCKED"
