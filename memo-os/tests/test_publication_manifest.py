import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest

path = Path(__file__).resolve().parents[1] / "tools" / "validate_publication_manifest.py"
spec = importlib.util.spec_from_file_location("validate_publication_manifest", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def png(width=1024, height=1536):
    return b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", width, height)

class PublicationManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.asset = self.root / "page.png"
        self.asset.write_bytes(png())
        self.page = {
            "source_folio_id": "F04", "publication_position": 1,
            "asset_path": "page.png",
            "sha256": hashlib.sha256(self.asset.read_bytes()).hexdigest(),
            "status": "CANDIDATE"
        }

    def tearDown(self):
        self.tmp.cleanup()

    def errors(self, pages):
        p = self.root / "manifest.json"
        p.write_text(json.dumps({"pages": pages}))
        return str(module.verify(p, self.root))

    def test_valid_candidate(self):
        self.assertEqual("[]", self.errors([self.page]))

    def test_bad_hash(self):
        self.page["sha256"] = "0" * 64
        self.assertIn("SHA-256 mismatch", self.errors([self.page]))

    def test_duplicate_position(self):
        self.assertIn("duplicate publication_position", self.errors([self.page, dict(self.page)]))

    def test_nonconsecutive_positions(self):
        self.page["publication_position"] = 2
        self.assertIn("consecutive", self.errors([self.page]))

    def test_acceptance_requires_receipts(self):
        self.page["status"] = "ACCEPTED"
        self.assertIn("independent_review_receipt", self.errors([self.page]))

    def test_wrong_dimensions(self):
        self.asset.write_bytes(png(800,1200))
        self.page["sha256"] = hashlib.sha256(self.asset.read_bytes()).hexdigest()
        self.assertIn("PNG dimensions", self.errors([self.page]))

    def test_missing_asset(self):
        self.asset.unlink()
        self.assertIn("asset missing", self.errors([self.page]))

    def test_path_traversal(self):
        self.page["asset_path"] = "../secret"
        self.assertIn("unsafe asset_path", self.errors([self.page]))

if __name__ == "__main__":
    unittest.main()
