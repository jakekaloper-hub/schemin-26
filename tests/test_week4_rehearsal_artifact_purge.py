import importlib.util
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
DENY=ROOT/"memo-os/week-4/publication-readiness/WEEK_04_REJECTED_REHEARSAL_ARTIFACT_DENYLIST.json"

spec=importlib.util.spec_from_file_location("assembly",ROOT/"governance/publication/week4_assembly_validator.py")
assembly=importlib.util.module_from_spec(spec)
spec.loader.exec_module(assembly)

class RehearsalArtifactPurgeTests(unittest.TestCase):
    def test_exact_two_failed_rehearsal_hashes_are_hard_denied(self):
        doc=json.loads(DENY.read_text())
        hashes={x["sha256"] for x in doc["rejected_artifacts"]}
        self.assertEqual(hashes,{
            "ebe961bccad20c0facf2005c5dad6f612bf540239f57c1996ae2ef81f11b28c1",
            "e894abfe327c1dd4af7e369e988ac24c5c560136a14b4441014271bd72ecb592"
        })

    def test_denied_hash_cannot_pass_assembly(self):
        bad_hash="ebe961bccad20c0facf2005c5dad6f612bf540239f57c1996ae2ef81f11b28c1"
        doc={
            "page_plan_state":"LOCKED",
            "pages":[{"page_id":"W4-P01","page_number":1,"artifact":"bad.png","sha256":bad_hash,"page_lock":"PASS"}],
            "final_pdf":"week4.pdf",
            "final_pdf_sha256":"a"*64,
            "umpire_receipt":"PASS"
        }
        result=assembly.validate(doc)
        self.assertEqual(result["state"],"FAIL_INTERNAL")
        self.assertTrue(any("REJECTED_REHEARSAL_ARTIFACT" in e for e in result["errors"]))

    def test_sandbox_rehearsal_directory_is_not_in_production_tree(self):
        self.assertFalse((ROOT/"sandbox/week4-rehearsal").exists())

if __name__=="__main__":
    unittest.main()
