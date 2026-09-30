import unittest
from canon.characters.runtime.asset_reference import AssetReference
from canon.characters.runtime.asset_resolver import resolve_assets, request_state
from canon.characters.runtime.reference_mount import CharacterReferenceMount
from canon.characters.runtime.renderer_capabilities import negotiate
from canon.characters.runtime.generation_eligibility import issue_eligibility, validate_eligibility
from canon.characters.runtime.generation_adapter import governed_generate

CID="CHAR-ZACH-WILSON"
def asset(uri="repo://canon/assets/zach.jpg",cid=CID):
    return AssetReference("A1",cid,"ZACH",uri,"abc","image/jpeg",100,100,"1","APPROVED","HIGH","commissioner")
def mount(attached=True):
    return CharacterReferenceMount(CID,"ZACH","A1","repo://x","abc","image/jpeg",(100,100),"1","APPROVED",True,True,True,attached,"test","ref-1" if attached else None,"now")
CAP={"test":{"supports_image_references":True,"returns_attachment_receipt":True,"max_references":4,"reference_mechanism":"test"}}

class Boundary(unittest.TestCase):
    def test_nonportable_blocks(self):
        r=resolve_assets([CID],{CID:asset(None)}); self.assertEqual(request_state(r),"GENERATION_BLOCKED")
    def test_swap_blocks(self):
        r=resolve_assets([CID],{CID:asset(cid="CHAR-AUSTIN-BYARS")}); self.assertEqual(request_state(r),"GENERATION_BLOCKED")
    def test_unsupported_route_blocks(self):
        self.assertEqual(negotiate("bad",{},1)["state"],"GENERATION_ROUTE_REFERENCE_UNSUPPORTED")
    def test_missing_mount_blocks(self):
        e=issue_eligibility("r",[CID],[mount(False)],"test",negotiate("test",CAP,1),now=1); self.assertEqual(e["state"],"GENERATION_BLOCKED")
    def test_eligibility_is_bound(self):
        e=issue_eligibility("r",[CID],[mount()],"test",negotiate("test",CAP,1),now=1)
        self.assertEqual(validate_eligibility(e,"r",[CID],"test",["abc"],now=2),"GENERATION_ELIGIBLE")
        self.assertEqual(validate_eligibility(e,"other",[CID],"test",["abc"],now=2),"GENERATION_BLOCKED")
        self.assertEqual(validate_eligibility(e,"r",[CID],"other",["abc"],now=2),"GENERATION_BLOCKED")
        self.assertEqual(validate_eligibility(e,"r",[CID],"test",["changed"],now=2),"GENERATION_BLOCKED")
        self.assertEqual(validate_eligibility(e,"r",[CID],"test",["abc"],now=999),"GENERATION_BLOCKED")
    def test_adapter_blocks_direct_bypass(self):
        called={"n":0}
        def renderer(payload): called["n"]+=1; return {"state":"RENDERED"}
        out=governed_generate(renderer,{"state":"GENERATION_BLOCKED"},"r",[CID],"test",["abc"],{})
        self.assertEqual(out["state"],"GENERATION_BLOCKED"); self.assertEqual(called["n"],0)

if __name__=="__main__": unittest.main()
