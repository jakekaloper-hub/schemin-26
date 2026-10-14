import json
import unittest
from pathlib import Path
from validate_twelve_pov import validate

REGISTRY = json.loads((Path(__file__).parent / "TWELVE_PRINCIPAL_REGISTRY_CANDIDATE_V1.json").read_text())

class TestPOV(unittest.TestCase):
    def test_owner_bindings_match_master_canon(self):
        canon = (Path(__file__).resolve().parents[2] / "canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md").read_text(encoding="utf-8")
        owners = [p.get("owner_name") for p in REGISTRY["principals"]]
        self.assertEqual(len(set(owners)), 12)
        for owner in owners:
            with self.subTest(owner=owner):
                self.assertIn("### " + owner + " /", canon)

    def test_accept(self):
        self.assertEqual([], validate(REGISTRY, [{"scene_id":"a","story_time":"w3","principal_pov_id":"obiwan_jacoby"}]))

    def test_reject_outsider(self):
        self.assertTrue(validate(REGISTRY, [{"scene_id":"a","story_time":"w3","principal_pov_id":"edrin"}]))

    def test_reject_missing(self):
        self.assertTrue(validate(REGISTRY, [{"scene_id":"a","story_time":"w3"}]))

    def test_elemental_receipt(self):
        self.assertTrue(validate(REGISTRY, [{"scene_id":"a","story_time":"w3","principal_pov_id":"el_nino"}]))

    def test_arbitrary_elemental_receipt_is_rejected(self):
        scene = {"scene_id":"e1","story_time":"w3","principal_pov_id":"el_nino","elemental_pov_canon_receipt":"ANY_STRING"}
        self.assertTrue(validate(REGISTRY, [scene]))

    def test_elemental_receipt_requires_registry_approval(self):
        scene = {"scene_id":"e1","story_time":"w3","principal_pov_id":"el_nino","elemental_pov_canon_receipt":"R1"}
        candidate = {**REGISTRY, "elemental_pov_approval":{"status":"PENDING", "receipt_id":"R1"}}
        self.assertTrue(validate(candidate, [scene]))

    def test_malformed_pov_type(self):
        for value in ([], {}, 7):
            self.assertTrue(validate(REGISTRY, [{"scene_id":"a","story_time":"w3","principal_pov_id":value}]))

    def test_invalid_registry_type(self):
        self.assertTrue(validate([], []))

    def test_twelve_count(self):
        self.assertTrue(validate({**REGISTRY, "principals":REGISTRY["principals"][:11]}, []))

    def test_chapter_one_two_source_scene_coverage(self):
        path = Path(__file__).parent / "CHAPTER_01_02_TWELVE_POV_SCENE_MIGRATION_PLAN_2026-10-14.json"
        packet = json.loads(path.read_text(encoding="utf-8"))
        scenes = packet["sections"]
        self.assertEqual(len(scenes), 19)
        self.assertEqual(len({s["scene_id"] for s in scenes}), 19)
        self.assertEqual(validate(REGISTRY, scenes), [])
        root = Path(__file__).resolve().parents[2]
        for chapter in packet["chapters"]:
            prose = (root / chapter["main_path"]).read_text(encoding="utf-8")
            headings = [line[3:] for line in prose.splitlines() if line.startswith("## ")]
            actual = [x["source_heading"] for x in scenes if x["source_chapter"] == chapter["chapter"]]
            self.assertEqual(actual, headings)
            self.assertEqual(len(actual), chapter["source_section_count"])
        self.assertTrue(all(s["hard_manuscript_replacement_status"] == "PROPOSED_NOT_WRITTEN_OR_ACCEPTED" for s in scenes))

    def test_early_chapter_candidate_fails_closed_on_unlicensed_narrator(self):
        path = Path(__file__).parent / "CHAPTER_01_02_TWELVE_POV_SCENE_MIGRATION_PLAN_2026-10-14.json"
        scenes = json.loads(path.read_text(encoding="utf-8"))["sections"]
        invalid = [dict(s) for s in scenes]
        invalid[0]["principal_pov_id"] = "edrin"
        self.assertTrue(validate(REGISTRY, invalid))
        elemental = [dict(s) for s in scenes]
        elemental[0]["principal_pov_id"] = "el_nino"
        self.assertTrue(validate(REGISTRY, elemental))

    def test_two_scene_prose_pilot_is_explicitly_noncanonical(self):
        path = Path(__file__).parent / "CHAPTER_01_02_TWELVE_POV_PROSE_PILOT_NONCANON_2026-10-14.md"
        prose = path.read_text(encoding="utf-8")
        self.assertIn("NOT hard canon", prose)
        self.assertIn("## CHAPTER_01_S01", prose)
        self.assertIn("## CHAPTER_02_S01", prose)
        self.assertNotIn("Edrin", prose)
        self.assertNotIn("Edin", prose)
        self.assertIn("141.70", prose)
        self.assertIn("131.26", prose)
        self.assertIn("191.90", prose)
        self.assertIn("100.90", prose)
        self.assertIn("other 17 remain mapped", prose)

if __name__ == "__main__":
    unittest.main()
