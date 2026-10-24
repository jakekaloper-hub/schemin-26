import tempfile
import json
import unittest
from world.atlas.spatial.historical_constraints import build_historical_constraints
from world.atlas.spatial.reference_scene import export_reference

class HistoricalSpatialConstraints(unittest.TestCase):
    def test_exact_reuse_and_factual_bounds(self):
        p=build_historical_constraints()
        self.assertEqual(p['region_id'],'REG-CENTRAL-BASIN')
        self.assertEqual(len(p['landmark_ids']),5)
        self.assertEqual({x['week'] for x in p['historical_observations']['LOC-PITTSYS-BOOK']},{4,5,6})
        self.assertTrue(all(not x['geometry_approved'] for x in p['route_topology_constraints']))
        self.assertFalse(p['physical_requirements']['metric_scale_and_landmark_footprints_approved'])
    def test_rendered_reference_has_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=export_reference(tmp)
            obj=(p/'central_basin_candidate.obj').read_text()
            meta=json.loads((p/'historical_constraints.json').read_text())
            self.assertTrue(obj.startswith('# SCHEMIN SYNTHETIC / NOT CANON'))
            self.assertEqual(meta['authorization'],'RESEARCH_AND_SIMULATION_ONLY')
            self.assertEqual(meta['status'],'EVIDENCE_CONSTRAINED_CANDIDATE_NOT_CANON')
if __name__=='__main__':unittest.main()
