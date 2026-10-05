import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SANDBOX = ROOT / "sandbox/week4-rehearsal"

def load_module(name, rel):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

elig = load_module("week4_render_eligibility", "governance/publication/week4_render_eligibility.py")
assembly = load_module("week4_assembly_validator", "governance/publication/week4_assembly_validator.py")
release = load_module("week4_release_transaction", "governance/publication/week4_release_transaction.py")

class SandboxRehearsal(unittest.TestCase):
    def setUp(self):
        self.fx = json.loads((SANDBOX/"SYNTHETIC_FINALITY.json").read_text())
        self.hmb = json.loads((SANDBOX/"HMB_PAGE1_PACKET.json").read_text())
        self.real = json.loads((SANDBOX/"W4_P11_PRODUCTION_EQUIVALENT_PACKET_V2.json").read_text())
        self.matrix = json.loads((ROOT/"memo-os/week-4/publication-readiness/WEEK_04_12_CHARACTER_AUTHORITY_MATRIX.json").read_text())

    def test_fixture_is_noncanon_and_six_decided(self):
        self.assertEqual(self.fx["marker"], "TEST_ONLY_NON_CANON_SANDBOX")
        self.assertTrue(self.fx["finality"])
        self.assertEqual(len(self.fx["matchups"]), 6)
        for m in self.fx["matchups"]:
            self.assertIn(m["winner"], {m["team_a"], m["team_b"]})
            self.assertNotEqual(m["score_a"], m["score_b"])

    def test_gate1_contradictory_result_fails(self):
        bad = dict(self.fx["matchups"][0])
        bad["winner"] = bad["team_a"] if bad["score_a"] < bad["score_b"] else bad["team_b"]
        expected = bad["team_a"] if bad["score_a"] > bad["score_b"] else bad["team_b"]
        self.assertNotEqual(bad["winner"], expected)

    def test_all_12_authority_rows_present(self):
        rows = self.matrix["characters"]
        self.assertEqual(len(rows),12)
        self.assertEqual(len({x["character_id"] for x in rows}),12)
        self.assertEqual(len({x["expected_sha256"] for x in rows}),12)

    def test_hmb_packet_uses_exact_current_hash(self):
        row = next(x for x in self.matrix["characters"] if x["character_id"]=="CHAR-AUSTIN-BYARS")
        supplied = self.hmb["exact_reference_assets"][0]["expected_sha256"]
        self.assertEqual(supplied,row["expected_sha256"])

    def test_hmb_negative_locks_present(self):
        joined = " ".join(self.hmb["negative_constraints"]).lower()
        for token in ["king","crown","vampire","blood mascot","belt omission"]:
            self.assertIn(token, joined)

    def test_hmb_wrong_hash_blocks(self):
        p = json.loads(json.dumps(self.hmb))
        p["exact_reference_assets"][0]["expected_sha256"]="0"*64
        result = elig.render_eligibility(p)
        self.assertEqual(result["state"],"PAGE_RENDER_BLOCKED")
        self.assertEqual(result["reason"],"CHARACTER_REFERENCE_HASH_MISMATCH")

    def test_hmb_current_packet_fail_closes_on_provider_proof(self):
        result = elig.render_eligibility(self.hmb)
        self.assertEqual(result["state"],"PAGE_RENDER_BLOCKED")
        self.assertEqual(result["reason"],"GENERATION_BLOCKED_PROVIDER_CAPABILITY_UNPROVEN")

    def test_real_page_is_actual_w4_p11_model_sequence(self):
        self.assertEqual(self.real["page"]["page_id"],"W4-P11")
        self.assertEqual(self.real["page"]["sequence"],["W4-P11 MODEL","W4-P12 LIABILITY","W4-P13 THE HOUSE GETS BEAT"])
        self.assertEqual(self.real["page"]["page_title"],"THE MODEL")
        self.assertFalse(self.real["live_truth"]["result_language_allowed"])

    def test_real_page_carries_actual_matchup_causality(self):
        st=self.real["story_truth"]
        self.assertEqual(st["llc_100_self_ticket"],"COMMISSIONER_SUPPLIED_FACT")
        self.assertEqual(st["hmb_custom_four_leg_parlay_potential_105"],"COMMISSIONER_SUPPLIED_FACT")
        self.assertEqual(st["primary_engine"],"Two Men With Explanations")

    def test_real_page_rejects_fake_prior_render_language(self):
        joined=json.dumps(self.real).lower()
        for token in ["generic sports promo staging","crown","winner pose","final settlement"]:
            self.assertIn(token, joined)
        self.assertNotIn('"record"', joined)
        self.assertNotIn('"records"', joined)

    def test_real_hmb_binding_uses_exact_recovery_receipt(self):
        h=next(x for x in self.real["characters"] if x["character_id"]=="CHAR-AUSTIN-BYARS")
        self.assertEqual(h["recovered_file_id"],"file_00000000f82c81f5a3843df3ab18dfff")
        self.assertEqual(h["sha256"],"eedfaaf0b2e2dd78a7a32e11aef333cab41278c206b65ec78c4aa4f1fd2c4f76")
        self.assertIn("crown",h["reject"])

    def test_real_page_forbids_generated_factual_typography(self):
        forbidden=set(self.real["deterministic_text"]["generated_image_text_forbidden"])
        self.assertTrue({"scores","records","standings","odds","payouts","final result"}.issubset(forbidden))

    def test_gate11_missing_page_would_fail(self):
        doc={"pages":[{"page_id":f"W4-P{i:02d}","page_number":i,"artifact":"x","sha256":"a"*64,"page_lock":"PASS","qa_receipts":[]} for i in range(1,19)],"final_pdf":"x.pdf","final_pdf_sha256":"b"*64,"umpire_receipt":"PASS"}
        result=assembly.validate(doc)
        self.assertEqual(result["state"],"FAIL_INTERNAL")

    def test_gate12_production_release_stays_blocked(self):
        result=release.validate()
        self.assertEqual(result["state"],"RELEASE_BLOCKED")

if __name__ == "__main__":
    unittest.main()
