import unittest
from unittest.mock import patch
from world.atlas.spatial.memo_archive_grounding import resolve_central_basin_evidence, resolve_evidence

class MemoGroundingTests(unittest.TestCase):
    def test_week4_5_6_pittsys_provenance(self):
        rows = resolve_evidence('LOC-PITTSYS-BOOK')
        self.assertEqual({r['week'] for r in rows}, {4, 5, 6})
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(r['spatial_inference'] == 'NOT_APPROVED' for r in rows))
    def test_no_automatic_geometry(self):
        packet = resolve_central_basin_evidence()
        self.assertFalse(packet['metric_geometry_approved'])
        self.assertEqual(set(packet['locations']), {'LOC-LEAGUE-CHAMBER','LOC-LEAGUE-ARCHIVE','LOC-PITTSYS-BOOK','LOC-DK-MUD-HILL','LOC-SOUTHERN-SPEEDWAY'})
    def test_missing_edition_has_no_invented_evidence(self):
        self.assertEqual(resolve_evidence('LOC-NONEXISTENT'), [])

if __name__ == '__main__': unittest.main()
