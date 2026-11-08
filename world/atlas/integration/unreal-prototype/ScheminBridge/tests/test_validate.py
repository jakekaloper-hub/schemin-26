import copy,unittest
from ScheminBridge.validate import validate
BASE={"schema_version":"0.1.0","source_repository":"jakekaloper-hub/schemin-26","source_commit":"a"*40,"scene_id":"preview.test","location_id":"test_001","status":"PREVIEW","canon_approved":False,"mutates_world_state":False,"characters":[],"espn_event":None,"asset_bindings":[],"location_evidence":{"source_path":"world/test.json","source_record_id":"test_001","validated":True}}
class Tests(unittest.TestCase):
 def test_fixture_contract(self): self.assertEqual(validate(BASE),[])
 def test_fail_closed(self):
  changes=[("source_commit","bad"),("source_repository","other/repo"),("location_id",None),("status","APPROVED"),("canon_approved",True),("mutates_world_state",True),("characters",["character"]),("espn_event",{"id":"fake"}),("asset_bindings",[{"path":"none"}]),("location_evidence",{})]
  for k,v in changes:
   with self.subTest(k=k):
    d=copy.deepcopy(BASE);d[k]=v;self.assertTrue(validate(d))
if __name__=="__main__":unittest.main()
