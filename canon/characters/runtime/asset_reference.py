"""Character asset authority. Asset records are identity-bound and fail closed."""
from dataclasses import dataclass

@dataclass(frozen=True)
class AssetReference:
    asset_id: str
    character_id: str
    owner_id: str
    canonical_uri: str | None
    sha256: str
    media_type: str
    width: int | None
    height: int | None
    canon_version: str
    approval_state: str
    render_quality: str
    provenance: str

    @property
    def portable(self):
        return bool(self.canonical_uri and self.canonical_uri.startswith(("repo://","asset://","https://")))

    def validate(self, requested_character_id):
        if self.character_id != requested_character_id:
            return "ASSET_CHARACTER_MISMATCH"
        if self.media_type not in {"image/jpeg","image/png","image/webp"}:
            return "ASSET_MEDIA_UNSUPPORTED"
        if self.approval_state != "APPROVED":
            return "ASSET_NOT_APPROVED"
        if not self.portable:
            return "ASSET_NOT_PORTABLE"
        return "PASS"
