"""Keep stored Commissioner image candidates byte-correct without changing active canon."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
RECOVERY = ROOT / "canon/characters/recovery"
EVIDENCE = RECOVERY / "GITHUB_REMOTE_ASSET_READBACK_2026_10_17.json"
ACTIVE = ROOT / "canon/characters/reference_sources_v1.json"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify_candidate_assets(root: Path, records: list[dict]) -> bool:
    for entry in records:
        p = root / entry["repository_path"]
        if not p.is_file():
            return False
        data = p.read_bytes()
        if (len(data) != entry["size_bytes"]
                or hashlib.sha256(data).hexdigest() != entry["sha256"]
                or git_blob_sha(data) != entry["git_blob_sha1"]):
            return False
    return True


class CommissionerRepositoryCandidateIntegrityTests(unittest.TestCase):
    def test_twelve_bytes_are_persisted_and_per_character(self):
        receipt = json.loads(EVIDENCE.read_text())
        rows = receipt["items"]
        self.assertEqual(len(rows), 12)
        self.assertEqual(len({x["character_id"] for x in rows}), 12)
        for entry in rows:
            self.assertTrue(entry["repository_path"].startswith(
                "canon/characters/assets/" + entry["character_id"] + "/primary/"))
        self.assertTrue(verify_candidate_assets(ROOT, rows))
        self.assertEqual(sum(x["relation_to_prior"] == "EXACT_MATCH" for x in rows), 2)
        self.assertEqual(sum(x["relation_to_prior"] != "EXACT_MATCH" for x in rows), 10)

    def test_candidate_bytes_never_auto_promote_over_active_canon(self):
        receipt = json.loads(EVIDENCE.read_text())
        active = json.loads(ACTIVE.read_text())
        canonical = {x["character_id"]: x for x in active["entries"]}
        self.assertEqual(len(canonical), 12)
        self.assertFalse(receipt["active_canon_promoted"])
        self.assertFalse(receipt["renderer_subject_binding_verified"])
        self.assertEqual(receipt["t15"], "HOLD")
        for x in receipt["items"]:
            self.assertIn(x["character_id"], canonical)
            if x["relation_to_prior"] != "EXACT_MATCH":
                self.assertNotEqual(x["sha256"], canonical[x["character_id"]]["expected_sha256"])

    def test_modified_candidate_fails_closed(self):
        import tempfile
        receipt = json.loads(EVIDENCE.read_text())
        first = receipt["items"][0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = root / first["repository_path"]
            p.parent.mkdir(parents=True)
            p.write_bytes(b"wrong-character-or-corrupt-content")
            self.assertFalse(verify_candidate_assets(root, [first]))


if __name__ == "__main__":
    unittest.main()
