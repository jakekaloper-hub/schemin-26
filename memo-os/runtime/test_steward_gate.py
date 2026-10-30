import unittest
from steward_gate import *

def packet():
    h={k:[] for k in REQUIRED}
    h.update(run_id="r",assignment_id="a",artifact="x",artifact_version=1,source_authority="ESPN",source_snapshot="s",status="ASSIGNED",confidence="provisional",next_required_action="review",next_gate="CANONICAL_SNAPSHOT_LOCK")
    h["from"]="ECS";h["to"]="STEWARD"
    return h

class TestSteward(unittest.TestCase):
    def test_contract(self): self.assertTrue(validate(packet()))
    def test_missing_field(self):
        h=packet();del h["source_authority"]
        self.assertRaises(GateRejected,validate,h)
    def test_no_fake_ack(self): self.assertRaises(GateRejected,transition,packet(),"ACKNOWLEDGED","STEWARD")
    def test_ack(self): self.assertEqual(transition(packet(),"ACKNOWLEDGED","STEWARD",{"id":"receipt"})["status"],"ACKNOWLEDGED")
    def test_no_skip(self): self.assertRaises(GateRejected,transition,packet(),"VALIDATED","STEWARD",{})
    def test_no_self_receipt(self):
        h=packet();h["status"]="HANDOFF_READY"
        self.assertRaises(GateRejected,transition,h,"RECEIVED","ECS",{"id":"r"})
    def test_unresolved_blocks(self):
        h=packet();h["status"]="RECEIVED";h["unresolved"]=["native provenance"]
        self.assertRaises(GateRejected,transition,h,"VALIDATED","STEWARD",{"source_receipt":1,"semantic_qa":1,"freshness":1,"independent_reviewer":1})
    def test_mercer(self):
        h=packet();h["verified_facts"]=["Mercer"]
        self.assertRaises(GateRejected,validate,h)
    def test_fact_blocked(self): self.assertEqual(gate_status(packet())["FACT_LOCK"],"BLOCKED")
    def test_work_key(self): self.assertEqual(work_key(1417621,2026,8,"a","x"),work_key(1417621,2026,8,"a","x"))

if __name__=="__main__": unittest.main()
