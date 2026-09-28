import unittest
from living_novel_os import *

class NovelOSTests(unittest.TestCase):
    def test_authority_beats_recency(self):
        r=resolve_assertions([
          {"authority":"PROPOSED_CANON","approved":True,"value":"new"},
          {"authority":"CHARACTER_CANON","approved":True,"value":"locked"}])
        self.assertEqual(r["assertion"]["value"],"locked")
    def test_equal_authority_conflict(self):
        r=resolve_assertions([
          {"authority":"CHARACTER_CANON","approved":True,"value":"a"},
          {"authority":"CHARACTER_CANON","approved":True,"value":"b"}])
        self.assertEqual(r["status"],"CONFLICTED")
    def test_trade_jedi_belt_drift(self):
        self.assertFalse(can_accept(validate_character_text("ObiWan Jacoby wore his championship belt.")))
    def test_donkey_kong_species_drift(self):
        self.assertFalse(can_accept(validate_character_text("Donkey Kong, a giant gorilla, entered.")))
    def test_oracle_guard(self):
        self.assertFalse(can_accept(validate_oracle_mutation({"temporal_layer":"ORACLE","authority":"WORLD_CANON"})))
    def test_promise_abandon_requires_reason(self):
        self.assertFalse(can_accept(validate_promise({"status":"ABANDONED_WITH_JUSTIFICATION"})))
    def test_router_visual_prologue(self):
        roles=route("produce next Prologue composition")
        self.assertIn("Visual Director",roles); self.assertIn("Canon Guardian",roles)



class Phase4to7Tests(unittest.TestCase):
    def test_timeline_impossible_order(self):
        f=validate_timeline([{"id":"a","order":2,"after":["b"]},{"id":"b","order":3}])
        self.assertFalse(can_accept(f))
    def test_object_possession(self):
        f=validate_object_state([{"order":1,"object_id":"belt","action":"ACQUIRE","actor":"byars"},{"order":2,"object_id":"belt","action":"USE","actor":"jake"}])
        self.assertFalse(can_accept(f))
    def test_knowledge_leak(self):
        f=validate_knowledge([{"order":1,"actor":"x","action":"ACT_ON","fact_id":"secret"}])
        self.assertFalse(can_accept(f))
    def test_alias_identity(self):
        f=validate_alias_identity([{"team_name_changed":True,"canonical_character_before":"Arsenal Centaur","canonical_character_after":"Gorilla"}])
        self.assertFalse(can_accept(f))
    def test_visual_bootstrap(self):
        f=validate_visual_reference({"character_bearing":True,"master_canon_resolved":True,"generated_reference":True,"approved_visual_canon":False})
        self.assertFalse(can_accept(f))
    def test_unverified_live_event_blocks(self):
        self.assertEqual(live_event_transaction({"id":"w3","verified":False})["state"],"BLOCKED")
    def test_verified_live_event_ready(self):
        self.assertEqual(live_event_transaction({"id":"w1","verified":True})["state"],"READY")
    def test_literary_pipeline_ends_gate(self):
        self.assertEqual(literary_workflow("V4")["stages"][-1]["name"],"HUMAN_CANON_GATE")
    def test_visual_pipeline_reference_gate(self):
        self.assertTrue(visual_workflow("P-BEAT",True)["reference_gate_required"])



class Phase9AdversarialTests(unittest.TestCase):
    def test_future_week1_leak_into_prologue(self):
        f=validate_temporal_firewall({"temporal_lock":"AFTER_2026_DRAFT_BEFORE_WEEK_1_RESULTS","facts":[{"season":2026,"week":1,"kind":"RESULT"}]})
        self.assertFalse(can_accept(f))
    def test_byars_crown_corruption(self):
        self.assertFalse(can_accept(validate_character_text("His Majesty's Blood entered as a crowned king.")))
    def test_missing_visual_master_resolution(self):
        self.assertFalse(can_accept(validate_visual_reference({"character_bearing":True,"master_canon_resolved":False})))
    def test_bad_manuscript_sha(self):
        self.assertFalse(can_accept(validate_manuscript_anchor({"pinned_blob_sha":"bad","anchor_text":"x"},"real")))
    def test_impossible_travel(self):
        f=validate_geography([{"action":"TRAVEL","from":"A","to":"B","elapsed_hours":1}],{"A":{"B":{"min_hours":5}}})
        self.assertFalse(can_accept(f))
    def test_unapproved_generated_visual(self):
        self.assertFalse(can_accept(validate_visual_reference({"character_bearing":False,"generated_reference":True,"approved_visual_canon":False})))
    def test_approval_blocks_findings(self):
        r=approval_transaction({"id":"x"},[Finding("X","FATAL","bad")],"Closer")
        self.assertEqual(r["state"],"BLOCKED")
    def test_approval_requires_approver(self):
        r=approval_transaction({"id":"x"},[],None)
        self.assertEqual(r["state"],"PENDING_APPROVAL")
    def test_release_gate_requires_all(self):
        self.assertEqual(release_gate({"regression_tests":True})["state"],"BLOCKED")
    def test_release_gate_pass(self):
        checks={k:True for k in ["regression_tests","adversarial_campaign","prologue_integration","artifact_registry","approval_gate","recovery_runbook","ci"]}
        self.assertEqual(release_gate(checks)["state"],"PASS")



class FlaimEvidenceTests(unittest.TestCase):
    def test_source_authority_lock(self):
        x={"canon_authority":"MANUSCRIPT_CANON","verification":"VERIFIED","downstream_eligible":True,"observed_fact":"result"}
        self.assertFalse(can_accept(validate_flaim_event(x)))
    def test_live_not_final(self):
        x={"canon_authority":"SOURCE_EVIDENCE","verification":"LIVE_UNFINALIZED","downstream_eligible":True,"observed_fact":"current score"}
        self.assertFalse(can_accept(validate_flaim_event(x)))
    def test_unknown_not_eligible(self):
        x={"canon_authority":"SOURCE_EVIDENCE","verification":"UNKNOWN","downstream_eligible":True,"observed_fact":"unknown"}
        self.assertFalse(can_accept(validate_flaim_event(x)))
    def test_verified_source_passes(self):
        x={"canon_authority":"SOURCE_EVIDENCE","verification":"VERIFIED","downstream_eligible":True,"observed_fact":"verified result"}
        self.assertTrue(can_accept(validate_flaim_event(x)))
    def test_significance_advisory(self):
        self.assertIn(grade_significance({"championship":True,"historical_echo":True}),SIGNIFICANCE_LEVELS)
if __name__=="__main__": unittest.main()
