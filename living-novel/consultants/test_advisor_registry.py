import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent

class AdvisorRegistryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.advisors = json.loads((ROOT / "ADVISOR_REGISTRY_V1.json").read_text())
        cls.sources = json.loads((ROOT / "SOURCE_REGISTRY_V1.json").read_text())
        cls.source_ids = {s["id"] for s in cls.sources["sources"]}

    def test_registry_is_advisory_only(self):
        self.assertEqual(self.advisors["authority"], "advisory_only")

    def test_advisor_ids_are_unique(self):
        ids = [a["id"] for a in self.advisors["advisors"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_modes_are_known(self):
        allowed = {"PUBLISHED_METHOD_LENS", "COMPOSITE_SPECIALIST", "HUMAN_VERIFIED"}
        for advisor in self.advisors["advisors"]:
            self.assertIn(advisor["mode"], allowed)

    def test_published_method_lenses_have_registered_sources(self):
        for advisor in self.advisors["advisors"]:
            if advisor["mode"] == "PUBLISHED_METHOD_LENS":
                self.assertTrue(advisor.get("source_ids"))
                for source_id in advisor["source_ids"]:
                    self.assertIn(source_id, self.source_ids)

    def test_composites_require_engagement_source_packet(self):
        for advisor in self.advisors["advisors"]:
            if advisor["mode"] == "COMPOSITE_SPECIALIST":
                self.assertTrue(advisor.get("requires_engagement_source_packet"))

    def test_no_current_human_verified_advisor_without_evidence(self):
        for advisor in self.advisors["advisors"]:
            if advisor["mode"] == "HUMAN_VERIFIED":
                self.assertTrue(advisor.get("verification_evidence"))

    def test_all_advisors_cannot_promote_canon(self):
        for advisor in self.advisors["advisors"]:
            self.assertIn("promote_canon", advisor.get("cannot", []))

    def test_source_ids_declared_by_registry_exist(self):
        for source_id in self.advisors["source_ids"]:
            self.assertIn(source_id, self.source_ids)

    def test_sources_have_nonempty_provenance(self):
        for source in self.sources["sources"]:
            self.assertTrue(source["title"])
            self.assertTrue(source["publisher"])
            self.assertTrue(source["url"].startswith("https://"))
            self.assertTrue(source["supports"])
            self.assertIn("live_consultation", source["does_not_establish"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
