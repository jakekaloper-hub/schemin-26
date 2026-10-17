"""Recovery search must be exact-hash scoped and fail on wrong/corrupt bytes."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from canon.characters.recovery.scan_existing_primary_sources import find_exact_sources, stage_results


class RecoveryScannerTests(unittest.TestCase):
    def registry(self, files):
        entries=[]
        for i,data in enumerate(files):
            entries.append({"character_id":f"CHAR-TEST-{i:02d}",
                            "expected_sha256":hashlib.sha256(data).hexdigest(),
                            "observed_library_size_bytes":len(data),
                            "repository_path":f"canon/characters/assets/CHAR-TEST-{i:02d}/primary/ref.jpeg"})
        return {"entries":entries}

    def test_exact_hash_only_and_no_implicit_roots(self):
        samples=[b"\xff\xd8\xff"+bytes([i])*12 for i in range(12)]
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            source=root/"source"; source.mkdir()
            dest=root/"dest"; dest.mkdir()
            (source/"matching-but-noncanonical-name.blob").write_bytes(samples[7])
            (source/"same-size-wrong-image.jpeg").write_bytes(b"\xff\xd8\xff"+b"!"*12)
            reg=self.registry(samples)
            report=find_exact_sources([source],reg,repository_root=dest)
            self.assertEqual(len(report["matches"]),1)
            self.assertEqual(report["matches"][0]["character_id"],"CHAR-TEST-07")
            staged=stage_results(report,dest)
            self.assertEqual(len(staged),1)
            self.assertEqual((dest/reg["entries"][7]["repository_path"]).read_bytes(),samples[7])
            self.assertEqual(stage_results(report,dest),[])

    def test_corrupt_existing_primary_fails_instead_of_skipping(self):
        samples=[b"\xff\xd8\xff"+bytes([i])*12 for i in range(12)]
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp); folder=r/"source";folder.mkdir()
            reg=self.registry(samples)
            p=r/reg["entries"][0]["repository_path"]
            p.parent.mkdir(parents=True)
            p.write_bytes(b"\xff\xd8\xffwrong")
            with self.assertRaisesRegex(ValueError,"corrupt"):
                find_exact_sources([folder],reg,skip_existing=True,repository_root=r)

    def test_missing_authorized_scan_root_is_error(self):
        samples=[b"\xff\xd8\xff"+bytes([i])*12 for i in range(12)]
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                find_exact_sources([Path(tmp)/"not-here"],self.registry(samples))

    def test_registry_rejects_cross_character_hash_reuse(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows=self.registry([b"same" for _ in range(12)])
            with self.assertRaisesRegex(ValueError,"duplicate cross-character"):
                find_exact_sources([Path(tmp)], rows)
