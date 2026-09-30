import unittest
from canon.characters.runtime.generation_adapter import governed_generate

class WaiverIncidentSimulation(unittest.TestCase):
 def test_missing_canonical_bytes_means_zero_renderer_calls(self):
  calls=[]
  renderer=lambda payload: calls.append(payload)
  blocked={"state":"GENERATION_BLOCKED","reason":"CHARACTER_REFERENCE_NOT_MOUNTED"}
  result=governed_generate(renderer,blocked,"waiver-4",["CHAR-ZACH-WILSON","CHAR-AUSTIN-BYARS","CHAR-PHILLIP-PITTS"],"test-route",[],{},signing_key="test",consumed_nonces=set())
  self.assertEqual(result["state"],"GENERATION_BLOCKED")
  self.assertFalse(result["renderer_invoked"])
  self.assertEqual(calls,[])
 def test_semantic_only_fallback_cannot_impersonate_eligibility(self):
  calls=[]
  fake={"state":"GENERATION_ELIGIBLE","claims":{"request_id":"waiver-4","character_ids":["CHAR-AUSTIN-BYARS","CHAR-PHILLIP-PITTS","CHAR-ZACH-WILSON"],"asset_hashes":[],"route":"test-route","expires_at":9999999999,"nonce":"x"},"token":"semantic-only"}
  r=governed_generate(lambda p:calls.append(p),fake,"waiver-4",["CHAR-ZACH-WILSON","CHAR-AUSTIN-BYARS","CHAR-PHILLIP-PITTS"],"test-route",[],{},signing_key="test",consumed_nonces=set())
  self.assertFalse(r["renderer_invoked"]); self.assertEqual(calls,[])
if __name__=="__main__": unittest.main()
