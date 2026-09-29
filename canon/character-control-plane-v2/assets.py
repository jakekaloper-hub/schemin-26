from models import AssetReference
def resolve_asset(asset_id:str,assets:dict[str,AssetReference]):
    a=assets.get(asset_id)
    if not a: return {"status":"HUMAN_REVIEW_REQUIRED","reason":"UNKNOWN_ASSET"}
    if a.availability!="AVAILABLE" or not a.uri: return {"status":"HUMAN_REVIEW_REQUIRED","reason":"MISSING_REFERENCE","asset":a}
    return {"status":"PASS","asset":a}
