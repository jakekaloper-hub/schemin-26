from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Literal
import hashlib, json

EvidenceClass=Literal["ESTABLISHED","SUPPORTED","PROPOSED","RETIRED"]
AssetAvailability=Literal["AVAILABLE","MISSING_REFERENCE","PENDING_INGESTION"]
QAStatus=Literal["PASS","REGENERATE","HUMAN_REVIEW_REQUIRED"]

@dataclass(frozen=True)
class AssetReference:
    asset_id:str; role:str; sha256:str; availability:AssetAvailability
    uri:str|None=None; media_type:str|None=None; provenance:str|None=None
    approval_event:str|None=None; supersedes:tuple[str,...]=()

@dataclass(frozen=True)
class POVClaim:
    text:str; evidence_class:EvidenceClass; provenance:tuple[str,...]=()

@dataclass(frozen=True)
class CharacterRecord:
    schema_version:str; character_id:str; owner:str; current_team:str; identity:str
    aliases:tuple[str,...]=(); retired_aliases:tuple[str,...]=()
    active_version:str="1.0"; species_body:str="UNKNOWN"; head_face:str="UNKNOWN"
    silhouette:str="UNKNOWN"; materials:str="UNKNOWN"; wardrobe:tuple[str,...]=()
    signature_objects:tuple[str,...]=(); companions:tuple[str,...]=()
    environment_anchor:str="UNKNOWN"; negative_locks:tuple[str,...]=()
    hard_locks:tuple[str,...]=(); primary_asset_id:str|None=None
    pov:tuple[POVClaim,...]=()

@dataclass(frozen=True)
class Layer:
    kind:Literal["IDENTITY_BASE","APPROVED_CHARACTER_VERSION","CONTINUITY_STATE","WEEKLY_STORY_STATE","SCENE_STATE","EXPLICIT_COMMISSIONER_OVERRIDE"]
    changes:dict[str,Any]; provenance:tuple[str,...]=()

@dataclass(frozen=True)
class QACheck:
    check_id:str; expected:Any; observed:Any; severity:Literal["FATAL","IMPORTANT","ADVISORY"]; evidence:tuple[str,...]=()

IDENTITY_FIELDS={"species_body","head_face","silhouette","materials","wardrobe","negative_locks","hard_locks"}
STORY_FIELDS={"verified_event_ids","pressure","reputation_delta","unresolved_threads","story_notes"}
SCENE_FIELDS={"pose","action","camera","weather","lighting","location","wear","expression"}
LAYER_WRITE_POLICY={
"IDENTITY_BASE":IDENTITY_FIELDS|{"signature_objects","companions","environment_anchor"},
"APPROVED_CHARACTER_VERSION":IDENTITY_FIELDS|{"signature_objects","companions","environment_anchor","primary_asset_id"},
"CONTINUITY_STATE":{"wardrobe","signature_objects"},
"WEEKLY_STORY_STATE":STORY_FIELDS,
"SCENE_STATE":SCENE_FIELDS,
"EXPLICIT_COMMISSIONER_OVERRIDE":IDENTITY_FIELDS|{"signature_objects","companions","environment_anchor","primary_asset_id"},
}
def canonical_hash(value:Any)->str:
    def default(o): return asdict(o) if hasattr(o,"__dataclass_fields__") else list(o) if isinstance(o,tuple) else str(o)
    raw=json.dumps(value,default=default,sort_keys=True,separators=(",",":")).encode()
    return hashlib.sha256(raw).hexdigest()
