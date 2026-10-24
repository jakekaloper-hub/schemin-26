"""Presentation artwork publication boundary tests; no delivered art is fabricated."""
import hashlib
import importlib.util
import json
import pathlib
import tempfile
import unittest

BASE = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('art_catalog', BASE / 'build_public_catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class ArtworkCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.source = self.root / 'source'
        self.output = self.root / 'output'
        self.source.mkdir()
        # Byte receipt fixture only. Never part of published site assets.
        (self.source / 'home.webp').write_bytes(b'artwork-byte-receipt-fixture')
        self.record = {'file': 'home.webp', 'alt': 'Commissioned empty ridge.',
                       'status': 'REVIEWED_PRESENTATION', 'subjectClass': 'environment',
                       'sha256': hashlib.sha256(b'artwork-byte-receipt-fixture').hexdigest()}

    def manifest(self, assets):
        (self.source / 'manifest.json').write_text(json.dumps({'schemaVersion': 1, 'assets': assets}))

    def test_reviewed_asset_is_verified_and_copied(self):
        self.manifest({'home': self.record})
        result = catalog.load_artwork(self.output, self.source)
        self.assertEqual(result['assets']['home']['sha256'], self.record['sha256'])
        self.assertEqual((self.output / 'artwork/home.webp').read_bytes(), (self.source / 'home.webp').read_bytes())

    def test_drafts_are_excluded_and_stale_public_assets_are_removed(self):
        self.manifest({'home': self.record})
        catalog.load_artwork(self.output, self.source)
        self.record['status'] = 'GENERATED_UNREVIEWED'
        self.manifest({'home': self.record})
        self.assertEqual(catalog.load_artwork(self.output, self.source)['assets'], {})
        self.assertFalse((self.output / 'artwork/home.webp').exists())

    def test_absent_manifest_removes_previous_artwork(self):
        self.manifest({'home': self.record})
        catalog.load_artwork(self.output, self.source)
        (self.source / 'manifest.json').unlink()
        self.assertEqual(catalog.load_artwork(self.output, self.source)['assets'], {})
        self.assertFalse((self.output / 'artwork').exists())

    def test_known_regional_artwork_can_publish(self):
        self.manifest({'region-REG-UPPER-VALLEYS': self.record})
        result = catalog.load_artwork(self.output, self.source)
        self.assertIn('region-REG-UPPER-VALLEYS', result['assets'])

    def test_unknown_regional_slot_is_rejected(self):
        self.manifest({'region-REG-INVENTED': self.record})
        with self.assertRaisesRegex(ValueError, 'Unsupported'):
            catalog.load_artwork(self.output, self.source)

    def test_unreviewed_atlas_cannot_claim_positional_use(self):
        self.record['allowedUses'] = ['positional']
        self.manifest({'atlas': self.record})
        with self.assertRaisesRegex(ValueError, 'Atlas'):
            catalog.load_artwork(self.output, self.source)

    def test_wrong_hash_fails_closed(self):
        self.record['sha256'] = '0' * 64
        self.manifest({'home': self.record})
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            catalog.load_artwork(self.output, self.source)

    def test_parent_path_escape_is_rejected(self):
        self.record['file'] = '../outside.webp'
        self.manifest({'home': self.record})
        with self.assertRaisesRegex(ValueError, 'Invalid artwork file'):
            catalog.load_artwork(self.output, self.source)

    def test_character_slot_cannot_be_activated_by_status_string(self):
        self.manifest({'CHAR-JAKE-KALOPER': self.record})
        with self.assertRaisesRegex(ValueError, 'character-gated'):
            catalog.load_artwork(self.output, self.source)

    def test_character_subject_in_environment_slot_is_rejected(self):
        self.record['subjectClass'] = 'character'
        self.manifest({'home': self.record})
        with self.assertRaisesRegex(ValueError, 'subject class'):
            catalog.load_artwork(self.output, self.source)

    def test_output_cannot_destroy_source(self):
        self.manifest({'home': self.record})
        with self.assertRaisesRegex(ValueError, 'separate'):
            catalog.load_artwork(self.root, self.root / 'artwork')


if __name__ == '__main__':
    unittest.main()
