import importlib.util
import tempfile
import unittest
from pathlib import Path

P = Path(__file__).with_name('week6_candidate_image_resolver.py')
spec = importlib.util.spec_from_file_location('week6_candidate_image_resolver', P)
mod = importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class CandidatePreviewTests(unittest.TestCase):
    def test_six_exact_refs(self):
        for loc in ('LOC-RED-RUINS','LOC-COUNTRY-CLUB-JACKSON','LOC-SLOB-FOOTHILL-CAMP','LOC-CHILI-STABLE','LOC-MUD-DOGS-SWAMP','LOC-TDS-WATERFALL-TEMPLE'):
            with self.subTest(loc=loc):
                r=mod.resolve(loc);self.assertEqual(r['location_id'],loc);self.assertIn('/'+loc+'/',r['uri']);self.assertFalse(r['canonical_approved'])
    def test_canonical_mode_denied(self):
        with self.assertRaisesRegex(mod.CandidateReferenceError,'CANONICAL_REFERENCE_UNAPPROVED'):
            mod.resolve('LOC-RED-RUINS',mode='canonical')
    def test_wrong_location_denied(self):
        with self.assertRaisesRegex(mod.CandidateReferenceError,'UNKNOWN_OR_DUPLICATE_LOCATION_ID'):
            mod.resolve('LOC-NOT-REAL')
    def test_wrong_location_file_rejected(self):
        original=mod.ROOT
        with tempfile.TemporaryDirectory() as t:
            mod.ROOT=Path(t)
            try:
                with self.assertRaisesRegex(mod.CandidateReferenceError,'LOCATION_ASSET_MISSING_OR_MISMAPPED'):mod.resolve('LOC-RED-RUINS')
            finally:mod.ROOT=original
    def test_mismatched_file_fingerprint_rejected(self):
        import json,shutil
        original=mod.ROOT
        with tempfile.TemporaryDirectory() as t:
            base=Path(t)
            manifest=json.loads(mod.MANIFEST.read_text()); registry=json.loads(mod.REGISTRY.read_text())
            (base/'memo-os/week-6').mkdir(parents=True)
            (base/'world/location-control-plane/registries').mkdir(parents=True)
            (base/'memo-os/week-6/WEEK_6_EXACT_PNG_INGESTION_MANIFEST.json').write_text(json.dumps(manifest))
            (base/'world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json').write_text(json.dumps(registry))
            asset=manifest['assets'][0]; dest=base/asset['candidate_uri'];dest.parent.mkdir(parents=True);dest.write_bytes(b'not a png')
            mod.ROOT=base
            try:
                with self.assertRaisesRegex(mod.CandidateReferenceError,'INVALID_PNG'):mod.resolve(asset['location_id'])
            finally:mod.ROOT=original

if __name__=='__main__': unittest.main()
