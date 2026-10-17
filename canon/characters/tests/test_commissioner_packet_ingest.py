"""Regression tests for the existing canonical-reference asset ingestion route."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[3]
MODULE = ROOT / "canon/characters/recovery/ingest_commissioner_packet.py"
spec = importlib.util.spec_from_file_location("commissioner_ingest", MODULE)
ingest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ingest)


class CommissionerPacketIngestTests(unittest.TestCase):
    def build_fixture(self, root: Path):
        assets = []
        receipt = []
        expected_data = {}
        for index in range(12):
            cid = f"CHAR-TEST-{index:02d}"
            ext = "jpeg" if index >= 10 else "png"
            magic = b"\xff\xd8\xff" if ext == "jpeg" else b"\x89PNG\r\n\x1a\n"
            data = magic + f"synthetic-test-byte-data-{index}".encode()
            member = f"canon/characters/assets/{cid}/primary/COMMISSIONER_2026-10-12.{ext}"
            sha = ingest.digest(data)
            assets.append({
                "character_id": cid,
                "archive_member": member,
                "expected_sha256": sha,
                "size_bytes": len(data),
                "hash_relation_to_prior": "EXACT_MATCH" if index >= 10 else "DIFFERENT_VERSION_REQUIRES_CANON_RECONCILIATION",
            })
            receipt.append({"character_id": cid, "target_repository_path": member, "sha256": sha, "bytes": len(data)})
            expected_data[member] = data
        archive = root / "packet.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for member, data in expected_data.items():
                z.writestr(member, data)
            z.writestr("CHARACTER_UPLOAD_RECEIPTS.json", json.dumps({"items": receipt}))
        lock = {"assets": assets, "source_archive_sha256": ingest.digest(archive.read_bytes())}
        return archive, lock, expected_data

    def test_good_packet_verifies_all_twelve_and_exposes_sha1_receipts(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive, lock, samples = self.build_fixture(Path(tmp))
            rows = ingest.verify_packet(archive, lock)
            self.assertEqual(len(rows), 12)
            for row in rows:
                self.assertEqual(row["sha256"], hashlib.sha256(samples[row["repository_path"]]).hexdigest())
                self.assertEqual(len(row["git_blob_sha1"]), 40)
            self.assertEqual(ingest.make_receipt(rows, lock["source_archive_sha256"], False)["t15"], "HOLD")

    def test_mutated_archive_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive, lock, _ = self.build_fixture(Path(tmp))
            with archive.open("ab") as stream:
                stream.write(b"modified")
            with self.assertRaisesRegex(ingest.IntegrityError, "Archive hash differs"):
                ingest.verify_packet(archive, lock)

    def test_unexpected_path_or_duplicate_member_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive, lock, samples = self.build_fixture(Path(tmp))
            rogue = Path(tmp) / "rogue.zip"
            with zipfile.ZipFile(rogue, "w") as z:
                for member, data in samples.items():
                    z.writestr(member, data)
                z.writestr("../intruder", b"x")
                z.writestr("CHARACTER_UPLOAD_RECEIPTS.json", "{}")
            lock["source_archive_sha256"] = ingest.digest(rogue.read_bytes())
            with self.assertRaisesRegex(ingest.IntegrityError, "unexpected members"):
                ingest.verify_packet(rogue, lock)

    def test_staging_is_repeatable_and_never_overwrites_conflicting_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive, lock, samples = self.build_fixture(root)
            rows = ingest.verify_packet(archive, lock)
            ingest.stage_verified(rows, root)
            ingest.stage_verified(rows, root)
            for member, data in samples.items():
                self.assertEqual((root / member).read_bytes(), data)
            conflict = root / rows[0]["repository_path"]
            conflict.write_bytes(b"not original")
            with self.assertRaisesRegex(ingest.IntegrityError, "Refusing to overwrite"):
                ingest.stage_verified(rows, root)


if __name__ == "__main__":
    unittest.main()
