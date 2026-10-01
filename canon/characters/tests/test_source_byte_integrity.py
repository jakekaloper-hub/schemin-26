import copy
import hashlib
import json
import pathlib
import tempfile
import unittest

from canon.characters.runtime.source_byte_integrity import (
    DEFAULT_REGISTRY,
    git_blob_sha,
    verify_source_bytes,
)


class SourceByteIntegrityTests(unittest.TestCase):
    def test_registry_has_exactly_twelve_unique_approved_sources(self):
        registry=json.loads(DEFAULT_REGISTRY.read_text())
        entries=registry["entries"]
        self.assertEqual(len(entries),12)
        self.assertEqual(len({e["character_id"] for e in entries}),12)
        self.assertEqual(len({e["conversation_file_id"] for e in entries}),12)
        self.assertTrue(all(len(e["expected_sha256"])==64 for e in entries))
        self.assertTrue(all(e["approval_state"]=="APPROVED" for e in entries))

    def test_repository_never_false_passes_missing_or_corrupt_bytes(self):
        result=verify_source_bytes()
        self.assertIn(result["state"],{"PASS","SOURCE_BYTES_REQUIRED"})
        self.assertEqual(result["blocked_count"],0)
        if result["state"]=="SOURCE_BYTES_REQUIRED":
            self.assertGreater(result["source_bytes_required_count"],0)
            self.assertLess(result["pass_count"],result["total"])

    def test_tampered_bytes_block(self):
        registry=json.loads(DEFAULT_REGISTRY.read_text())
        one=copy.deepcopy(registry)
        one["entries"]=one["entries"][:1]
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d)
            entry=one["entries"][0]
            p=root/entry["repository_path"]
            p.parent.mkdir(parents=True)
            p.write_bytes(b"tampered")
            result=verify_source_bytes(root,one)
            self.assertEqual(result["state"],"GENERATION_BLOCKED")
            self.assertEqual(result["records"][0]["reason"],"SOURCE_HASH_MISMATCH")

    def test_exact_bytes_can_pass_and_emit_git_blob_sha(self):
        payload=b"exact-approved-test-bytes"
        registry=json.loads(DEFAULT_REGISTRY.read_text())
        one=copy.deepcopy(registry)
        one["entries"]=one["entries"][:1]
        entry=one["entries"][0]
        entry["expected_sha256"]=hashlib.sha256(payload).hexdigest()
        entry["observed_library_size_bytes"]=len(payload)
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d)
            p=root/entry["repository_path"]
            p.parent.mkdir(parents=True)
            p.write_bytes(payload)
            result=verify_source_bytes(root,one)
            self.assertEqual(result["state"],"PASS")
            record=result["records"][0]
            self.assertEqual(record["actual_sha256"],entry["expected_sha256"])
            self.assertEqual(record["git_blob_sha"],git_blob_sha(payload))
            self.assertEqual(len(record["git_blob_sha"]),40)


if __name__=="__main__":
    unittest.main()
