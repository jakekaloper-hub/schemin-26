import hashlib
import importlib.util
import json
from pathlib import Path
from io import BytesIO
from PIL import Image
import tempfile
import unittest

path = Path(__file__).resolve().parents[1] / "tools" / "validate_publication_manifest.py"
spec = importlib.util.spec_from_file_location("validate_publication_manifest", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def png(width=1024, height=1536):
    output = BytesIO()
    Image.new("RGB", (width, height)).save(output, "PNG")
    return output.getvalue()

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

    def test_truncated_png_is_not_an_artifact(self):
        self.asset.write_bytes(self.asset.read_bytes()[:24])
        self.page["sha256"] = hashlib.sha256(self.asset.read_bytes()).hexdigest()
        self.assertIn("readable PNG", self.errors([self.page]))

    def test_nonobject_page_is_diagnostic(self):
        self.assertIn("page must be an object", self.errors([None]))

    def test_unhashable_position_and_status_are_diagnostics(self):
        self.page["publication_position"] = []
        self.page["status"] = {}
        result = self.errors([self.page])
        self.assertIn("publication_position", result)
        self.assertIn("unknown acceptance status", result)

    def test_nonstring_path_is_diagnostic(self):
        self.page["asset_path"] = []
        self.assertIn("unsafe asset_path", self.errors([self.page]))

    def test_symlink_cannot_escape_artifact_root(self):
        with tempfile.TemporaryDirectory() as outside:
            source = Path(outside) / "page.png"
            source.write_bytes(self.asset.read_bytes())
            self.asset.unlink()
            self.asset.symlink_to(source)
            self.assertIn("unsafe asset_path", self.errors([self.page]))

    def test_nonobject_manifest_is_diagnostic(self):
        path = self.root / "manifest.json"
        path.write_text("[]")
        self.assertIn("manifest must be an object", str(module.verify(path, self.root)))

    def test_path_traversal(self):
        self.page["asset_path"] = "../secret"
        self.assertIn("unsafe asset_path", self.errors([self.page]))

if __name__ == "__main__":
    unittest.main()
