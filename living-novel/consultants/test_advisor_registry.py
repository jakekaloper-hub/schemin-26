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


    def test_author_council_has_exact_core_seven(self):
        council = self.advisors.get("author_council", {})
        expected = {
            "jrr_tolkien",
            "george_rr_martin",
            "jk_rowling",
            "john_grisham",
            "ursula_k_le_guin",
            "brandon_sanderson",
            "joe_abercrombie",
        }
        self.assertEqual(set(council.get("core_seven", [])), expected)

    def test_core_seven_are_published_method_lenses_with_dossiers(self):
        by_id = {a["id"]: a for a in self.advisors["advisors"]}
        for advisor_id in self.advisors["author_council"]["core_seven"]:
            advisor = by_id[advisor_id]
            self.assertEqual(advisor["mode"], "PUBLISHED_METHOD_LENS")
            dossier = advisor.get("dossier_path")
            self.assertTrue(dossier)
            dossier_path = ROOT.parents[1] / pathlib.Path(dossier).relative_to("living-novel")
            self.assertTrue(dossier_path.exists(), dossier)
            text = dossier_path.read_text()
            self.assertIn("## Four-round responsibility", text)
            self.assertIn("## Preservation rule", text)

    def test_core_seven_have_registered_public_sources(self):
        by_id = {a["id"]: a for a in self.advisors["advisors"]}
        for advisor_id in self.advisors["author_council"]["core_seven"]:
            for source_id in by_id[advisor_id]["source_ids"]:
                self.assertIn(source_id, self.source_ids)

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
