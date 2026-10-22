import unittest
from world.atlas.spatial.grade_audit import route_grade_report
class GradeAuditTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(route_grade_report(),route_grade_report())
    def test_expected_routes(self):
        r=route_grade_report()
        self.assertEqual({x["route_id"] for x in r["routes"]},{"ROUTE-ARCHIVE-CHAMBER","ROUTE-BASIN-MARKET"})
        self.assertEqual([len(x["segments"]) for x in r["routes"]],[1,3])
    def test_finite_candidate_grades(self):
        for r in route_grade_report()["routes"]:
            for s in r["segments"]:
                self.assertGreater(s["synthetic_length_m"],0)
                self.assertGreaterEqual(s["maximum_sampled_grade"],0)
                self.assertLess(s["maximum_sampled_grade"],1)
    def test_noncanonical_label(self):
        self.assertIn("NOT_ROUTE_CERTIFICATION",route_grade_report()["limits"])
if __name__=="__main__":unittest.main()
