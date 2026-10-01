"""Machine-verifiable reference mount + subject-binding contract."""
from dataclasses import dataclass


@dataclass(frozen=True)
class CharacterReferenceMount:
    character_id: str
    owner_id: str
    asset_id: str
    canonical_uri: str
    sha256: str
    media_type: str
    dimensions: tuple[int, int] | None
    canon_version: str
    approval_state: str
    asset_resolved: bool
    hash_verified: bool
    asset_loaded: bool
    asset_attached_to_generation: bool
    renderer_route: str
    generation_reference_id: str | None
    subject_slot: str | None
    subject_binding_proven: bool
    subject_binding_id: str | None
    verified_at: str

    def renderable(self, route=None):
        if route is not None and self.renderer_route != route:
            return False
        return all((
            self.approval_state == "APPROVED",
            bool(self.canonical_uri),
            bool(self.sha256) and len(self.sha256) == 64,
            self.asset_resolved,
            self.hash_verified,
            self.asset_loaded,
            self.asset_attached_to_generation,
            bool(self.generation_reference_id),
            bool(self.subject_slot),
            self.subject_binding_proven,
            bool(self.subject_binding_id),
        ))
