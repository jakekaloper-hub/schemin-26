"""Machine-verifiable reference mount contract."""
from dataclasses import dataclass

@dataclass(frozen=True)
class CharacterReferenceMount:
    character_id: str
    owner_id: str
    asset_id: str
    canonical_uri: str
    sha256: str
    media_type: str
    dimensions: tuple[int,int] | None
    canon_version: str
    approval_state: str
    asset_resolved: bool
    hash_verified: bool
    asset_loaded: bool
    asset_attached_to_generation: bool
    renderer_route: str
    generation_reference_id: str | None
    verified_at: str

    def renderable(self):
        return all((self.asset_resolved,self.hash_verified,self.asset_loaded,
                    self.asset_attached_to_generation,self.generation_reference_id))
