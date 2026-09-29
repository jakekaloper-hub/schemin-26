import re
from models import CharacterRecord,AssetReference
HEX64=re.compile(r"^[0-9a-f]{64}$")
def validate_record(r:CharacterRecord):
 errors=[]
 if r.schema_version!="2.0": errors.append("schema_version")
 if not r.character_id.startswith("CHAR-"): errors.append("character_id")
 for name in ("owner","current_team","identity","species_body","head_face","silhouette","materials"):
  if not getattr(r,name): errors.append(name)
 if len(set(r.aliases))!=len(r.aliases): errors.append("duplicate_alias")
 if set(r.aliases)&set(r.retired_aliases): errors.append("alias_active_retired_collision")
 return errors
def validate_asset(a:AssetReference):
 errors=[]
 if not HEX64.match(a.sha256): errors.append("sha256")
 if a.availability=="AVAILABLE" and not a.uri: errors.append("available_without_uri")
 if a.availability!="AVAILABLE" and a.uri: errors.append("nonavailable_with_uri")
 return errors
