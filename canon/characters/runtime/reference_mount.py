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
    expected_sha256: str | None = None
    mounted_sha256: str | None = None
    repository_path: str | None = None
    git_blob_sha: str | None = None
    byte_size: int | None = None
    mount_receipt_id: str | None = None
    capability_receipt_id: str | None = None

    def renderable(self, route=None):
        expected = self.expected_sha256 or self.sha256
        if route is not None and self.renderer_route != route:
            return False
        return all((
            self.approval_state == "APPROVED",
            bool(self.canonical_uri),
            bool(self.sha256) and len(self.sha256) == 64,
            bool(expected) and len(expected) == 64,
            self.sha256 == expected,
            bool(self.mounted_sha256) and self.mounted_sha256 == expected,
            self.asset_resolved,
            self.hash_verified,
            self.asset_loaded,
            self.asset_attached_to_generation,
            bool(self.generation_reference_id),
            bool(self.subject_slot),
            self.subject_binding_proven,
            bool(self.subject_binding_id),
            bool(self.repository_path),
            bool(self.git_blob_sha) and len(self.git_blob_sha) == 40,
            isinstance(self.byte_size, int) and self.byte_size > 0,
            bool(self.mount_receipt_id),
            bool(self.capability_receipt_id),
        ))
