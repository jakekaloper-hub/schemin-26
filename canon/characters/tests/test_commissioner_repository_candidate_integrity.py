"""Authoritative source bytes cannot masquerade as active primary identity."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
RECOVERY = ROOT / "canon/characters/recovery"
STAGED = RECOVERY / "COMMISSIONER_2026_10_12_INGEST_RECEIPT.json"
ROLES = RECOVERY / "COMMISSIONER_2026_10_17_ROLE_RECONCILIATION.json"
ACTIVE = ROOT / "canon/characters/reference_sources_v1.json"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify_candidate_assets(root: Path, records: list[dict]) -> bool:
    for item in records:
        p = root / item["repository_path"]
        if not p.is_file():
            return False
        data = p.read_bytes()
        if (len(data) != item["size_bytes"]
                or hashlib.sha256(data).hexdigest() != item["sha256"]
                or git_blob_sha(data) != item["git_blob_sha1"]):
            return False
    return True


class CommissionerRepositoryCandidateIntegrityTests(unittest.TestCase):
    def test_twelve_exact_recovered_bytes_are_role_scoped(self):
        rows = json.loads(STAGED.read_text())["items"]
        self.assertEqual(len(rows), 12)
        self.assertEqual(len({x["character_id"] for x in rows}), 12)
        folder = {
            "PRIMARY_EXACT_MATCH_SOURCE": "primary",
            "SUPPLEMENTARY_REGISTERED_SPOTLIGHT_ORIGINAL": "supplementary",
            "NONACTIVE_VISUAL_CANDIDATE": "candidate",
        }
        for x in rows:
            self.assertTrue(x["repository_path"].startswith(
                f"canon/characters/assets/{x['character_id']}/{folder[x['asset_role']]}/"))
        self.assertTrue(verify_candidate_assets(ROOT, rows))
        roles = [x["asset_role"] for x in rows]
        self.assertEqual(roles.count("PRIMARY_EXACT_MATCH_SOURCE"), 2)
        self.assertEqual(roles.count("SUPPLEMENTARY_REGISTERED_SPOTLIGHT_ORIGINAL"), 9)
        self.assertEqual(roles.count("NONACTIVE_VISUAL_CANDIDATE"), 1)

    def test_all_nine_spotlights_are_explicitly_supplementary_with_receipts(self):
        rows = json.loads(STAGED.read_text())["items"]
        for x in rows:
            if x["asset_role"] != "SUPPLEMENTARY_REGISTERED_SPOTLIGHT_ORIGINAL":
                continue
            receipt = ROOT / f"canon/characters/{x['character_id']}/OWNER_SPOTLIGHT_2026_RECEIPT.json"
            r = json.loads(receipt.read_text())
            self.assertEqual(r["classification"], "COMMISSIONER_RESHARED_SUPPLEMENTARY_OWNER_SPOTLIGHT")
            self.assertFalse(r["supersedes_primary_identity"])
            self.assertEqual(r["user_upload_sha256"], x["sha256"])
            self.assertTrue(r["bytes_differ_but_pixels_identical"])
            self.assertEqual(r["uploaded_rgba_pixel_sha256"], r["stored_rgba_pixel_sha256"])
            self.assertTrue((ROOT / r["stored_repository_path"]).is_file())
            self.assertFalse(r["renderer_binding_proven"])
            self.assertFalse(r["final_raster_qa_passed"])

    def test_no_candidate_or_supplementary_promotes_active_primary(self):
        receipt = json.loads(STAGED.read_text())
        classification = json.loads(ROLES.read_text())
        registry = json.loads(ACTIVE.read_text())
        active = {a["character_id"]: a for a in registry["entries"]}
        self.assertEqual(len(active), 12)
        self.assertTrue(classification["primary_canon_unchanged"])
        self.assertFalse(classification["renderer_binding_proven"])
        self.assertEqual(classification["t15"], "HOLD")
        self.assertEqual(receipt["n_versions_requiring_reconciliation"], 1)
        for x in receipt["items"]:
            if x["asset_role"] == "PRIMARY_EXACT_MATCH_SOURCE":
                self.assertEqual(x["sha256"], active[x["character_id"]]["expected_sha256"])
            else:
                self.assertNotEqual(x["sha256"], active[x["character_id"]]["expected_sha256"])

    def test_supplementary_or_candidate_cannot_seed_primary_render_even_if_mislabeled(self):
        from canon.characters.runtime.reference_authority import validate_reference_candidate
        rows = json.loads(STAGED.read_text())["items"]
        for x in rows:
            candidate = {
                "asset_id": "COMMISSIONER-" + x["character_id"],
                "filename": Path(x["repository_path"]).name,
                "sha256": x["sha256"],
                "source_kind": "ORIGINAL",
            }
            verdict = validate_reference_candidate(x["character_id"], candidate)
            if x["asset_role"] != "PRIMARY_EXACT_MATCH_SOURCE":
                self.assertEqual(verdict["state"], "GENERATION_BLOCKED")
                self.assertEqual(verdict["reason"], "REFERENCE_SOURCE_HASH_MISMATCH")

    def test_modified_or_missing_bytes_fail_closed(self):
        x = json.loads(STAGED.read_text())["items"][0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertFalse(verify_candidate_assets(root, [x]))
            p = root / x["repository_path"]
            p.parent.mkdir(parents=True)
            p.write_bytes(b"wrong-character")
            self.assertFalse(verify_candidate_assets(root, [x]))


if __name__ == "__main__":
    unittest.main()
