#!/usr/bin/env python3
import copy,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/"world"/"evolution"))
from engine.world_evolution import world_payloads,apply_to_payloads
from engine.world_reconstruction import make_envelope,reconstruct,digest

def closed_txn():
 return {"schema_version":"1.0","transaction_id":"TXN-RECON-W4-001","week":4,"season":2026,"source_release":"CLOSED_TEST_FIXTURE","release_verified":True,
 "operations":[
  {"op":"APPEND_WORLD_STATE_EVENT","event":{"id":"EVT-W4-RECON-TEST","week":4,"location_id":"LOC-COUNTRY-CLUB-JACKSON","event_type":"cleanup","classification":"TEST_ONLY","entering_state":["cleanup unresolved"],"continuity_out":["reconstruction fixture"],"source_provenance":["TEST_FIXTURE_ONLY"]}},
  {"op":"SET_LOCATION_STATE","location_id":"LOC-COUNTRY-CLUB-JACKSON","state":["cleanup completed in reconstruction fixture"]}
 ],"approvals":{"umpire":True,"closer":True,"commissioner":False}}

class ReconstructionTests(unittest.TestCase):
 def setUp(self): self.base=world_payloads()
 def test_replay_matches_direct_apply(self):
  req=closed_txn(); expected,_=apply_to_payloads(req,self.base)
  env=make_envelope(self.base,[req]); actual=reconstruct(env,self.base)
  for k in ("state","events","ledger"): self.assertEqual(digest(actual[k]),digest(expected[k]))
 def test_replay_is_deterministic(self):
  env=make_envelope(self.base,[closed_txn()])
  a=reconstruct(env,self.base);b=reconstruct(env,self.base)
  for k in ("state","events","ledger"): self.assertEqual(digest(a[k]),digest(b[k]))
 def test_unknown_contract_version_fails_closed(self):
  env=make_envelope(self.base,[]);env["contract_version"]="99.0"
  with self.assertRaisesRegex(ValueError,"UNSUPPORTED_RECONSTRUCTION_CONTRACT_VERSION"): reconstruct(env,self.base)
 def test_unknown_source_version_fails_closed(self):
  env=make_envelope(self.base,[]);env["state_schema_version"]="2.0"
  with self.assertRaisesRegex(ValueError,"UNSUPPORTED_SOURCE_SCHEMA_VERSION"): reconstruct(env,self.base)
 def test_corrupt_base_hash_fails_closed(self):
  env=make_envelope(self.base,[]);env["base_state"]["as_of"]="tampered"
  with self.assertRaisesRegex(ValueError,"SOURCE_HASH_MISMATCH:state"): reconstruct(env,self.base)
 def test_missing_hash_fails_closed(self):
  env=make_envelope(self.base,[]);del env["source_hashes"]["events"]
  with self.assertRaisesRegex(ValueError,"SOURCE_HASH_MISMATCH:events"): reconstruct(env,self.base)
 def test_duplicate_replay_transaction_fails(self):
  req=closed_txn();env=make_envelope(self.base,[req,copy.deepcopy(req)])
  with self.assertRaises(ValueError): reconstruct(env,self.base)
 def test_prototype_does_not_mutate_input(self):
  before={k:digest(self.base[k]) for k in ("state","events","ledger")}
  env=make_envelope(self.base,[closed_txn()]);reconstruct(env,self.base)
  after={k:digest(self.base[k]) for k in ("state","events","ledger")}
  self.assertEqual(before,after)

if __name__=="__main__": unittest.main(verbosity=2)
