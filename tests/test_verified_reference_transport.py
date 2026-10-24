"""Synthetic binary preflight tests; not renderer certification."""
import base64
import hashlib
import struct
import unittest
from canon.characters.runtime.verified_reference_transport import verify_repository_png, ReferenceTransportError

class TestReferencePreflight(unittest.TestCase):
    def setUp(self):
        self.data = b"\x89PNG\r\n\x1a\n" + b"\0\0\0\rIHDR" + struct.pack(">II", 12, 15) + b"\x08\x02\0\0\0"
        self.args = {"character_id": "CHAR-WILSON-LOOK",
            "repository_path": "canon/characters/assets/lineups/2026-10-18-crops/CHAR-WILSON-LOOK.png",
            "base64_content": base64.b64encode(self.data).decode(),
            "expected_sha256": hashlib.sha256(self.data).hexdigest(), "expected_dimensions": (12, 15)}
    def rejects(self, args, reason):
        with self.assertRaisesRegex(ReferenceTransportError, reason):
            verify_repository_png(**args)
    def test_verified_does_not_grant_renderer_access(self):
        result = verify_repository_png(**self.args)
        self.assertEqual(result["state"], "BINARY_RETRIEVAL_VERIFIED")
        self.assertFalse(result["generation_eligible"])
        self.assertFalse(result["renderer_attachment_proven"])
    def test_modified_bytes(self):
        self.rejects(dict(self.args, base64_content=base64.b64encode(self.data+b"x").decode()), "SOURCE_HASH_MISMATCH")
    def test_bad_path(self):
        self.rejects(dict(self.args, repository_path="canon/characters/assets/../secret"), "INVALID_REPOSITORY_PATH")
    def test_dimensions(self):
        self.rejects(dict(self.args, expected_dimensions=(3, 4)), "IMAGE_DIMENSIONS_MISMATCH")
    def test_blob_mismatch(self):
        self.rejects(dict(self.args, expected_git_blob_sha="0"*40), "GIT_BLOB_HASH_MISMATCH")
    def test_nonimage(self):
        data=b"not an image"
        self.rejects(dict(self.args, base64_content=base64.b64encode(data).decode(),
                          expected_sha256=hashlib.sha256(data).hexdigest()), "INVALID_IMAGE_BYTES")

if __name__ == "__main__":
    unittest.main()
