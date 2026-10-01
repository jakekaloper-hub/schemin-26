import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "world" / "contracts" / "WORLD_NARRATIVE_HYDRATION_CONTRACT_V1.md"
RECEIPT = ROOT / "memo-os" / "week-4" / "WEEK_4_WORLD_NARRATIVE_HYDRATION_RECEIPT_V1.md"

class WorldNarrativeHydrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = CONTRACT.read_text()
        cls.receipt = RECEIPT.read_text()

    def test_shared_contract_exists_and_has_required_fields(self):
        for field in [
            "LOC_ID", "REGION_ZONE", "ARRIVAL_ROUTE", "ENTERING_WORLD_STATE",
            "PRIOR_MEMORY", "ORDINARY_WORLD_LIFE", "MATERIAL_CONSTRAINTS",
            "PUBLIC_KNOWLEDGE", "POV_KNOWLEDGE", "EVENT_DELTA",
            "DEPARTURE_STATE", "IMAGE_TELLS", "PROSE_TELLS",
            "UNKNOWN_FORBIDDEN_INVENTIONS",
        ]:
            self.assertIn(field, self.contract)

    def test_failure_modes_are_executable_contract_terms(self):
        for code in [
            "WORLD_AS_BACKDROP", "WORLD_LOADED_BUT_UNUSED",
            "GENERIC_FANTASY_SCENERY", "LORE_DUMP_PROSE",
            "UNAUTHORIZED_GEOGRAPHY", "ROUTELESS_RELOCATION",
            "WORLD_STATE_RESET", "PUBLIC_KNOWLEDGE_LEAK",
            "POV_KNOWLEDGE_LEAK", "VISUAL_PROSE_REDUNDANCY",
            "CONSEQUENCE_WITHOUT_PERSISTENCE", "MATCHUP_AS_ISOLATED_DIORAMA",
        ]:
            self.assertIn(code, self.contract)

    def test_cross_publication_anti_fork(self):
        self.assertIn("Weekly Memo and Living Novel", self.contract)
        self.assertIn("same location/world-state identity", self.contract)
        self.assertIn("may not publish incompatible geography or persistent state", self.contract)

    def test_generated_scenery_and_unknowns_cannot_become_canon(self):
        self.assertIn("Generated jokes and scenery remain non-canon", self.contract)
        self.assertIn("Unknown geography remains UNKNOWN", self.contract)

    def test_week4_all_six_reservoirs_are_hydrated_without_story_lock(self):
        for matchup in [
            "D0nkey K0ng × ObiWan Jacoby",
            "Mud Dogs × TDS",
            "Red Leopards × Dr. Duckhook",
            "Slob × Chili",
            "LLC × HMB",
            "El Niño × Seven Deadly Chins",
        ]:
            self.assertIn(matchup, self.receipt)
        self.assertIn("FINAL STORY LOCK BLOCKED", self.receipt)
        self.assertIn("Finished art: BLOCKED", self.receipt)
        self.assertIn("NOT DECLARED", self.receipt)

    def test_trade_is_not_automatically_literalized(self):
        self.assertIn("Chris Olave + Jadarian Price", self.receipt)
        self.assertIn("A.J. Brown + Bhayshul Tuten", self.receipt)
        self.assertIn("does **not** automatically create wagons, contracts, territorial exchange or physical player movement", self.receipt)

    def test_no_premature_world_mutation_or_venue_claim(self):
        self.assertIn("Final encounter venues: unresolved", self.receipt)
        self.assertIn("New Week 4 world mutations: none authorized", self.receipt)
        self.assertIn("Hydration strengthens interpretation; it does not advance maturity by itself.", self.receipt)

if __name__ == "__main__":
    unittest.main()
