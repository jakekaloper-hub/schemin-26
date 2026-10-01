import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
ROUTER_PATH = ROOT / "author_router.py"
spec = importlib.util.spec_from_file_location("author_router", ROUTER_PATH)
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)

class AuthorRouterTests(unittest.TestCase):
    def test_named_author_routes_exactly(self):
        r = router.select_consultants("Bullpen, call Grisham on this chapter.")
        self.assertEqual(r["advisors"], ["john_grisham"])
        self.assertEqual(r["selection_mode"], "EXPLICIT_AUTHORS")

    def test_multiple_named_authors_preserve_request_order_by_registry_scan(self):
        r = router.select_consultants("Have Rowling and Martin challenge chapter architecture.")
        self.assertEqual(set(r["advisors"]), {"jk_rowling", "george_rr_martin"})

    def test_pov_panel_is_canonical(self):
        r = router.select_consultants("Bullpen run the POV panel.")
        self.assertEqual(r["panel"], "pov_character")
        self.assertEqual(r["advisors"], ["ursula_k_le_guin", "joe_abercrombie", "george_rr_martin"])

    def test_full_seven_is_exact_registry_order(self):
        reg = router.load_registry()
        r = router.select_consultants("Convene the full Seven.")
        self.assertEqual(r["consultation_type"], "FULL_COUNCIL")
        self.assertEqual(r["advisors"], reg["author_council"]["core_seven"])

    def test_book_architecture_escalates_full_council(self):
        r = router.select_consultants("Audit the book architecture.")
        self.assertEqual(r["consultation_type"], "FULL_COUNCIL")

    def test_generic_consult_is_small_triage_not_full_seven(self):
        r = router.select_consultants("Bullpen, call the Novel consultants on this chapter.")
        self.assertEqual(r["panel"], "chapter_triage")
        self.assertEqual(len(r["advisors"]), 3)

    def test_engagement_manifest_freezes_selection_and_evidence(self):
        m = router.build_engagement_manifest(
            "Run the pacing panel",
            engagement_id="NOVEL-AUTHOR-CONSULT-2026-10-01-001",
            evidence_commit_sha="abc123",
            temporal_cutoff="2026-10-01T02:00:00-04:00",
            decision_question="Does Chapter 2 move?",
        )
        self.assertEqual(m["status"], "FROZEN")
        self.assertEqual(m["panel"], "pacing_readability")
        self.assertEqual(router.validate_engagement_manifest(m), [])

    def test_manifest_rejects_missing_evidence(self):
        m = router.build_engagement_manifest(
            "Call Tolkien",
            engagement_id="X",
            evidence_commit_sha="",
            temporal_cutoff="",
            decision_question="World depth?",
        )
        errors = router.validate_engagement_manifest(m)
        self.assertIn("MISSING_EVIDENCE_COMMIT", errors)
        self.assertIn("MISSING_TEMPORAL_CUTOFF", errors)

    def test_manifest_rejects_cross_reading_before_lock(self):
        m = router.build_engagement_manifest(
            "Call Le Guin",
            engagement_id="X",
            evidence_commit_sha="abc",
            temporal_cutoff="now",
            decision_question="POV?",
        )
        m["independence"]["cross_reading_before_lock"] = True
        self.assertIn("INDEPENDENCE_VIOLATION", router.validate_engagement_manifest(m))

if __name__ == "__main__":
    unittest.main(verbosity=2)
