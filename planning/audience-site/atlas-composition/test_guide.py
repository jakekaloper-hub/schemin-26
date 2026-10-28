import hashlib
import importlib.util
import json
import subprocess
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('guide', HERE / 'build_guide.py')
guide = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guide)


class GuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = guide.compile_matrix()

    def test_projection_matches_real_site_for_all_anchors(self):
        module = (guide.ROOT / 'productions/audience-site/src/experience.js').as_uri()
        payload = [{'x': a['abstractPosition'][0], 'y': a['abstractPosition'][1]} for a in self.matrix['anchors']]
        result = subprocess.run(['node', '--input-type=module', '-e', f'import {{projectPoint}} from {json.dumps(module)}; console.log(JSON.stringify({json.dumps(payload)}.map(projectPoint)));'], check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout), [a['overlayPoint'] for a in self.matrix['anchors']])

    def test_all_source_anchors_and_route_order_retained(self):
        self.assertEqual(len(self.matrix['anchors']), 23)
        self.assertEqual(len(self.matrix['routes']), 18)
        self.assertEqual(len(self.matrix['regions']), 7)
        source = json.loads((guide.ROOT / 'world/data/locations.json').read_text())['locations']
        self.assertEqual({a['id']: a['abstractPosition'] for a in self.matrix['anchors']}, {l['id']: l['abstract_position'] for l in source})
        self.assertEqual(self.matrix['routes'], json.loads((guide.ROOT / 'world/data/routes.json').read_text())['routes'])

    def test_every_location_receives_its_region_and_landmarks(self):
        regions = {r['id']: r for r in self.matrix['regions']}
        source = {l['id']: l for l in json.loads((guide.ROOT / 'world/data/locations.json').read_text())['locations']}
        for anchor in self.matrix['anchors']:
            self.assertEqual(anchor['regionalEnvironment'], regions[anchor['regionId']]['environment'])
            self.assertEqual(anchor['landmarks'], source[anchor['id']].get('persistent_landmarks', []))
            self.assertTrue(anchor['routeIds'])
            self.assertTrue(all(v == 'PENDING' for v in anchor['review'].values()))

    def test_upstream_contested_state_is_preserved(self):
        hill = next(a for a in self.matrix['anchors'] if a['id'] == 'LOC-DK-MUD-HILL')
        self.assertTrue(any('summit remains unclaimed' in s for s in hill['authoritativeState']))
        self.assertTrue(any('no sovereignty' in s for s in hill['authoritativeState']))

    def test_source_hashes_are_fresh(self):
        for source in self.matrix['sources']:
            self.assertEqual(source['sha256'], hashlib.sha256((guide.ROOT / source['path']).read_bytes()).hexdigest())

    def test_svg_contains_every_registered_layer_and_identity(self):
        root = ET.fromstring(guide.render_svg(self.matrix))
        self.assertEqual(root.attrib['viewBox'], '0 0 2000 1400')
        self.assertEqual({e.attrib['data-location'] for e in root.iter() if 'data-location' in e.attrib}, {a['id'] for a in self.matrix['anchors']})
        self.assertEqual({e.attrib['data-route'] for e in root.iter() if 'data-route' in e.attrib}, {r['id'] for r in self.matrix['routes']})


if __name__ == '__main__':
    unittest.main()
