"""Fail-closed binary preflight for canonical character assets, not a render permit."""
from __future__ import annotations
import base64
import binascii
import hashlib
import struct

class ReferenceTransportError(ValueError):
    pass

def verify_repository_png(character_id, repository_path, base64_content, expected_sha256,
                          expected_dimensions=None, expected_git_blob_sha=None):
    """Verify GitHub Contents API bytes against independently approved source hash."""
    prefix = "canon/characters/assets/"
    if not character_id.startswith("CHAR-") or len(character_id) < 6:
        raise ReferenceTransportError("INVALID_CHARACTER_ID")
    if (not repository_path.startswith(prefix)
            or any(part in ("", ".", "..") for part in repository_path.split("/"))):
        raise ReferenceTransportError("INVALID_REPOSITORY_PATH")
    if len(expected_sha256) != 64 or any(x not in "0123456789abcdef" for x in expected_sha256.lower()):
        raise ReferenceTransportError("INVALID_EXPECTED_HASH")
    try:
        data = base64.b64decode(base64_content, validate=False)
    except (binascii.Error, ValueError) as exc:
        raise ReferenceTransportError("INVALID_BASE64") from exc
    if not data:
        raise ReferenceTransportError("EMPTY_IMAGE_BYTES")
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected_sha256.lower():
        raise ReferenceTransportError("SOURCE_HASH_MISMATCH")
    if len(data) < 24 or not data.startswith(b"\x89PNG\r\n\x1a\n") or data[12:16] != b"IHDR":
        raise ReferenceTransportError("INVALID_IMAGE_BYTES")
    width, height = struct.unpack(">II", data[16:24])
    if width <= 0 or height <= 0:
        raise ReferenceTransportError("INVALID_IMAGE_DIMENSIONS")
    if expected_dimensions is not None and (width, height) != tuple(expected_dimensions):
        raise ReferenceTransportError("IMAGE_DIMENSIONS_MISMATCH")
    blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    if expected_git_blob_sha and blob != expected_git_blob_sha.lower():
        raise ReferenceTransportError("GIT_BLOB_HASH_MISMATCH")
    return {"state": "BINARY_RETRIEVAL_VERIFIED", "character_id": character_id,
            "repository_path": repository_path, "sha256": actual, "git_blob_sha": blob,
            "media_type": "image/png", "width": width, "height": height,
            "byte_size": len(data), "renderer_attachment_proven": False,
            "subject_binding_proven": False, "generation_eligible": False}
