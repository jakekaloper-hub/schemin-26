"""Source/provenance audit protects original source image, supporting HMB and all 12 crops."""
import hashlib,json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
RECEIPT=ROOT/"canon/characters/lineup_2026_10_18/BINARY_SOURCE_AND_CROP_RECEIPTS.json"

class BinaryReceiptTests(unittest.TestCase):
    def test_all_fourteen_git_blob_hash_and_sha_proofs(self):
        record=json.loads(RECEIPT.read_text())
        self.assertEqual(len(record["items"]),14)
        for x in record["items"]:
            raw=(ROOT/x["repository_path"]).read_bytes()
            self.assertEqual(len(raw),x["size_bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),x["sha256"])
            self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),x["git_blob_sha1"])
        self.assertFalse(record["actual_provider_mount_proven"])
        self.assertEqual(record["independent_umpire_T15"],"HOLD")

    def test_exact_original_and_twelve_distinct_derived_crops(self):
        items=json.loads(RECEIPT.read_text())["items"]
        self.assertEqual(items[0]["sha256"],"24cd6adf9654e598c97a6588afc07603d5adcc40c276eba07e7c86c0d438e7b2")
        self.assertEqual(items[1]["sha256"],"ed65db3f1271e19db54be94d7a09b7910b333cde79dcaa107020cc54015d5ade")
        self.assertEqual(len({x["character_id"] for x in items[2:]}),12)
        self.assertEqual(len({x["sha256"] for x in items[2:]}),12)
