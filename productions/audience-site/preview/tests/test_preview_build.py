"""Behavioral tests for the repository's private, offline observer build."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('preview_build', BASE/'build_preview.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
ROOT = BASE.parents[2]


def catalog():
    locations = json.loads((ROOT/'world/data/locations.json').read_text())['locations']
    return {
        'sourceRevision': 'e78b76fc16766afd350b6266edb1c07d10f5cd41',
        'stateAsOf': 'end_of_week_3_2026',
        'authority': 'DERIVED_PRESENTATION_ONLY',
        'publicationAuthorized': False,
        'locations': locations,
    }


class PreviewBuildTests(unittest.TestCase):
    def run_build(self, data=None, **options):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root/'catalog.json'
            source.write_text(json.dumps(catalog() if data is None else data))
            before = source.read_bytes()
            report = builder.build(source, root/'observer.html', **options)
            html = (root/'observer.html').read_text()
            self.assertEqual(source.read_bytes(), before)
            return report, html

    def test_no_editions_is_the_default_even_when_private_art_is_present(self):
        # A flag-order regression must never publish a mounted private asset folder.
        with tempfile.TemporaryDirectory() as td:
            art = Path(td)
            (art/'edition-memory.json').write_text(json.dumps({'memories': [], 'PRIVATE_SENTINEL': True}))
            report, html = self.run_build(art_path=art)
        self.assertEqual(report['originalJPEGs'], 0)
        self.assertFalse('PRIVATE_SENTINEL' in html)
        self.assertIn('id="memoryIndex" type="application/json">null</script>', html)

    def test_absent_private_folder_does_not_block_default_build(self):
        report, _ = self.run_build(art_path='/missing-private-assets')
        self.assertEqual(report['originalJPEGs'], 0)

    def test_build_is_byte_deterministic_and_retains_the_source_date(self):
        a, first = self.run_build(no_editions=True)
        b, second = self.run_build(no_editions=True)
        self.assertEqual(first, second)
        self.assertEqual(a['sha256'], b['sha256'])
        self.assertEqual(a['sourceStateAsOf'], 'end_of_week_3_2026')
        self.assertFalse(a['publicationAuthorized'])

    def test_incomplete_or_nonhex_source_revision_is_rejected(self):
        for value in ['main', 'f'*39, 'g'*40, '']:
            with self.subTest(value=value):
                data = catalog(); data['sourceRevision'] = value
                with self.assertRaisesRegex(ValueError, 'SOURCE_REVISION'):
                    self.run_build(data, no_editions=True)

    def test_missing_source_state_date_is_rejected(self):
        data = catalog(); data.pop('stateAsOf')
        with self.assertRaisesRegex(ValueError, 'SOURCE_STATE'):
            self.run_build(data, no_editions=True)

    def test_presentation_catalog_cannot_claim_publication_authority(self):
        data = catalog(); data['publicationAuthorized'] = True
        with self.assertRaisesRegex(ValueError, 'PUBLICATION_AUTHORITY'):
            self.run_build(data, no_editions=True)

    def test_json_script_breakout_is_escaped(self):
        data = catalog(); data['note'] = '</script><script>window.INJECTED=1</script>'
        _, html = self.run_build(data, no_editions=True)
        self.assertNotIn(data['note'], html)
        self.assertIn('\\u003c/script>', html)

    def test_no_editions_build_does_not_advertise_six_private_image_sequences(self):
        _, html = self.run_build(no_editions=True)
        self.assertFalse('Six locations also open historical artwork' in html)
        self.assertIn('No private edition artwork is included', html)

    def test_renderer_bytes_are_checked_not_only_the_version_string(self):
        original = Path.read_bytes
        def read(path):
            result = original(path)
            return result+b'\n// unexpected alteration' if path.name == 'three.module.js' else result
        with patch.object(Path, 'read_bytes', read):
            with self.assertRaisesRegex(ValueError, 'DEPENDENCY_HASH'):
                self.run_build(no_editions=True)

    def test_explicit_private_mode_requires_an_explicit_asset_directory(self):
        with self.assertRaisesRegex(ValueError, 'EXPLICIT_PRIVATE_ART'):
            self.run_build(no_editions=False)

    def test_explicit_private_assets_still_require_matching_hashes(self):
        with tempfile.TemporaryDirectory() as td:
            art = Path(td); (art/'a.jpg').write_bytes(b'not-the-approved-image')
            (art/'edition-memory.json').write_text(json.dumps({'memories':[{'pages':[
                {'path':'a.jpg','id':'PAGE-1','sha256':'0'*64}]}]}))
            with self.assertRaisesRegex(ValueError, 'ORIGINAL_ART_HASH'):
                self.run_build(no_editions=False, art_path=art)

    def test_output_preserves_the_current_renderer_license_and_no_network_bootstrap(self):
        _, html = self.run_build(no_editions=True)
        self.assertIn('The MIT License', html)
        self.assertIn('id="third-party-license"', html)
        self.assertNotIn('src="https://', html)
        self.assertNotIn('src="http://', html)
        self.assertNotIn('__BUNDLE__', html)


if __name__ == '__main__': unittest.main()
