import importlib.util
import pathlib
import tempfile
import unittest
import json
import os

BASE = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog', BASE / 'build_public_catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = pathlib.Path(cls.temp.name)
        cls.data = catalog.build_catalog(cls.output, render=False)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_canonical_population_and_positions(self):
        self.assertEqual(len(self.data['characters']), 12)
        self.assertEqual(len(self.data['locations']), 23)
        source = json.loads((catalog.ROOT / 'world/data/locations.json').read_text())['locations']
        self.assertEqual({x['id']: [x['x'], x['y']] for x in self.data['locations']},
                         {x['id']: x['abstract_position'] for x in source})

    def test_destination_environments_match_derived_location_cards(self):
        for location in self.data['locations']:
            path = catalog.ROOT / f"world/location-control-plane/locations/{location['id']}/CARD.json"
            if path.is_file():
                card = json.loads(path.read_text())
                self.assertEqual(location['environment'], card['physical_zone'])
                self.assertEqual(location['accessRoutes'], card['access_routes'])
                self.assertEqual(location['features'], card['addressable_feature_handles'])

    def test_latest_world_state_retains_contested_hill_qualifiers(self):
        source = json.loads((catalog.ROOT / 'world/data/current_world_state.json').read_text())
        hill = next(x for x in self.data['locations'] if x['id'] == 'LOC-DK-MUD-HILL')
        self.assertEqual(hill['worldState'], source['locations'][hill['id']])
        self.assertEqual(hill['worldStateAsOf'], source['as_of'])

    def test_living_homeland_activity_is_projected_from_source_packet(self):
        source = json.loads((catalog.ROOT / 'world/production/visual-packets/LOC-TRADE-JEDI-MOUNTAIN-BASE.json').read_text())
        home = next(x for x in self.data['locations'] if x['id'] == 'LOC-TRADE-JEDI-MOUNTAIN-BASE')
        self.assertEqual(home['ordinaryActivities'], source['world']['ordinary_inhabitants'])

    def test_relationships_resolve(self):
        locations = {x['id'] for x in self.data['locations']}
        self.assertTrue(all(x['locationId'] in locations for x in self.data['characters']))
        self.assertTrue(all(x['from'] in locations and x['to'] in locations for x in self.data['routes']))

    def test_approved_character_bytes_are_unchanged(self):
        for character in self.data['characters']:
            self.assertEqual(catalog.sha256(self.output / character['image']), character['sha256'])

    def test_sources_are_not_silently_promoted(self):
        memos = {x['week']: x for x in self.data['memos']}
        self.assertEqual(set(memos), {4, 5, 6})
        self.assertEqual(memos[5]['status'], 'Artwork review edition')
        self.assertTrue(all(x['releaseState'] != 'RELEASED' for x in memos.values()))
        self.assertTrue(all(not x.get('currentBenchmark') for x in memos.values()))
        self.assertEqual(sum(len(x['pageImages']) for x in memos.values()), 75)
        self.assertTrue(all(len(x['pageImages']) == x['pages'] for x in memos.values()))
        self.assertTrue(all('/main/' not in x['sourceUrl'] for x in memos.values()))

    def test_manuscripts_preserve_exact_source_and_archive_status(self):
        self.assertEqual(len(self.data['chapters']), 4)
        for chapter in self.data['chapters']:
            self.assertEqual(chapter['text'], (catalog.ROOT / chapter['source']).read_text())
            self.assertEqual(chapter['status'], 'Archive edition · rewrite commissioned')
            self.assertNotIn('CANDIDATE', chapter['source'])

    def test_hash_mismatch_fails_closed(self):
        with self.assertRaises(ValueError):
            catalog.verify_file(catalog.ROOT / 'README.md', '0' * 64)

    def test_all_public_record_sources_are_revision_pinned(self):
        for record in self.data['characters'] + self.data['locations'] + self.data['memos'] + self.data['chapters']:
            self.assertIn('/blob/' + catalog.REVISION + '/', record.get('sourceUrl', ''))

    def test_receipts_and_warnings_exist(self):
        self.assertTrue(self.data['meta']['sources'])
        self.assertTrue(self.data['meta']['warnings'])
        self.assertTrue((self.output / 'data.json').exists())

    @unittest.skipUnless(os.environ.get('CATALOG_RELEASED_SOURCE_DIR'), 'Optional recovered source integration')
    def test_recovered_released_editions_and_current_resolver(self):
        with tempfile.TemporaryDirectory() as temp:
            data = catalog.build_catalog(temp, render=False,
                                         released_source_dir=os.environ['CATALOG_RELEASED_SOURCE_DIR'])
            memos = {x['week']: x for x in data['memos']}
            self.assertEqual(set(memos), {2, 3, 4, 5, 6})
            self.assertEqual(sum(len(x['pageImages']) for x in memos.values()), 110)
            self.assertEqual(data['meta']['currentReleasedMemoId'], 'week-3')
            self.assertEqual(memos[3]['status'], 'Released edition')
            self.assertTrue(memos[3]['currentBenchmark'])
            self.assertFalse(memos[2]['currentBenchmark'])
            self.assertNotIn('pdf', memos[2])
            self.assertTrue(memos[2]['libraryFileId'].startswith('libfile_'))


if __name__ == '__main__':
    unittest.main()
