#!/usr/bin/env python3
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"world"/"evolution"))
from engine.world_evolution import world_payloads,validate_request,apply_to_payloads

def base_req():
 return {"schema_version":"1.0","transaction_id":"TXN-TEST-W4-001","week":4,"season":2026,"source_release":"TEST_ONLY_RELEASE","release_verified":True,"operations":[],"approvals":{"umpire":True,"closer":True,"commissioner":False}}

class Phase5Tests(unittest.TestCase):
 def setUp(self): self.p=world_payloads()
 def event_op(self,eid="EVT-W4-TEST"):
  return {"op":"APPEND_WORLD_STATE_EVENT","event":{"id":eid,"week":4,"location_id":"LOC-COUNTRY-CLUB-JACKSON","event_type":"cleanup","classification":"TEST_ONLY","entering_state":["dirty"],"continuity_out":["cleanup tested"],"source_provenance":["TEST_ONLY"]}}
 def test_valid_state_transaction_applies_in_memory(self):
  r=base_req();r["operations"]=[self.event_op(),{"op":"SET_LOCATION_STATE","location_id":"LOC-COUNTRY-CLUB-JACKSON","state":["test cleanup"]}]
  p,plan=apply_to_payloads(r,self.p)
  self.assertTrue(plan["state_apply_allowed"]);self.assertEqual(len(p["events"]["events"]),len(self.p["events"]["events"])+1)
  self.assertEqual(p["state"]["as_of"],"end_of_week_4_2026")
  self.assertEqual(len(p["ledger"]["transactions"]),len(self.p["ledger"]["transactions"])+1)
 def test_unverified_release_blocks(self):
  r=base_req();r["release_verified"]=False;r["operations"]=[self.event_op()]
  p=validate_request(r,self.p);self.assertEqual(p["status"],"FATAL")
 def test_duplicate_event_blocks(self):
  existing=self.p["events"]["events"][0]["id"];r=base_req();r["operations"]=[self.event_op(existing)]
  self.assertEqual(validate_request(r,self.p)["status"],"FATAL")
 def test_missing_umpire_blocks_apply_not_plan(self):
  r=base_req();r["approvals"]["umpire"]=False;r["operations"]=[self.event_op()]
  p=validate_request(r,self.p);self.assertTrue(p["valid"]);self.assertFalse(p["state_apply_allowed"])
 def test_candidate_evidence_does_not_promote(self):
  r=base_req();r["operations"]=[{"op":"REGISTER_CANDIDATE_EVIDENCE","candidate_id":"CAND-LANTERN-HOUSE","evidence_reference":"TEST_ONLY"}]
  p=validate_request(r,self.p);self.assertTrue(p["valid"]);self.assertFalse(p["state_apply_allowed"]);self.assertEqual(len(p["candidate_evidence"]),1)
 def test_candidate_promotion_needs_commissioner(self):
  r=base_req();r["operations"]=[{"op":"REQUEST_CANDIDATE_PROMOTION","candidate_id":"CAND-LANTERN-HOUSE","event_class":"NON_MATCHUP","route_resolution":"RESOLVED","proposed_location":{"id":"LOC-TEST-LANTERN","physical_zone_id":"REG-CENTRAL-BASIN"}}]
  p=validate_request(r,self.p);self.assertIn("TRIPLE_APPROVAL_REQUIRED",p["candidate_promotion_plans"][0]["blockers"])
 def test_championship_candidate_locked_before_event(self):
  r=base_req();r["approvals"]["commissioner"]=True;r["operations"]=[{"op":"REQUEST_CANDIDATE_PROMOTION","candidate_id":"CAND-CHAMP-LAST-FIELD","event_class":"PLAYOFF","route_resolution":"RESOLVED","championship_verified":False,"finalists_verified":False,"proposed_location":{"id":"LOC-LAST-FIELD","physical_zone_id":"REG-CENTRAL-BASIN"}}]
  p=validate_request(r,self.p);b=p["candidate_promotion_plans"][0]["blockers"];self.assertIn("CHAMPIONSHIP_EVENT_REQUIRED",b);self.assertIn("FINALISTS_VERIFIED_REQUIRED",b)
 def test_championship_candidate_plan_ready_only_when_verified(self):
  r=base_req();r["approvals"]["commissioner"]=True;r["operations"]=[{"op":"REQUEST_CANDIDATE_PROMOTION","candidate_id":"CAND-CHAMP-LAST-FIELD","event_class":"CHAMPIONSHIP","route_resolution":"RESOLVED","championship_verified":True,"finalists_verified":True,"proposed_location":{"id":"LOC-LAST-FIELD","physical_zone_id":"REG-CENTRAL-BASIN"}}]
  p=validate_request(r,self.p);self.assertTrue(p["candidate_promotion_plans"][0]["ready_for_separate_location_transaction"]);self.assertEqual(p["candidate_promotion_plans"][0]["blockers"],[])
 def test_new_candidate_cannot_start_active(self):
  r=base_req();r["operations"]=[{"op":"REGISTER_NEW_CANDIDATE","candidate":{"id":"CAND-TEST","lifecycle_status":"APPROVED_ACTIVE_CANON"}}]
  self.assertEqual(validate_request(r,self.p)["status"],"FATAL")
 def test_no_real_world_mutation_in_tests(self):
  before=len(self.p["events"]["events"]);r=base_req();r["operations"]=[self.event_op()]
  validate_request(r,self.p);self.assertEqual(len(self.p["events"]["events"]),before)
if __name__=="__main__":unittest.main(verbosity=2)
