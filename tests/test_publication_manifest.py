import copy
import importlib.util
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
MOD_PATH=ROOT/"governance"/"publication-manifest"/"validate_publication_manifest.py"
spec=importlib.util.spec_from_file_location("publication_manifest_validator",MOD_PATH)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PublicationManifestTests(unittest.TestCase):
    def setUp(self):
        self.doc=mod.load_manifest()

    def errors(self,doc=None):
        return mod.validate_manifest(copy.deepcopy(doc or self.doc))

    def test_current_manifest_passes(self):
        self.assertEqual(self.errors(),[])

    def test_week2_identity_is_locked(self):
        doc=copy.deepcopy(self.doc)
        p=next(x for x in doc["publications"] if x["publication_id"]=="memo.2026.week-02")
        p["canonical_artifact"]="PRO_SCHEMIN_WEEK_2_FINAL_MEMO.pdf"
        self.assertTrue(any("Week 2 canonical publication identity drifted" in x for x in self.errors(doc)))

    def test_blocked_week4_cannot_claim_artifact(self):
        doc=copy.deepcopy(self.doc)
        p=next(x for x in doc["publications"] if x["publication_id"]=="memo.2026.week-04")
        p["canonical_artifact"]="week4.pdf"
        self.assertTrue(any("BLOCKED publication cannot claim canonical_artifact" in x for x in self.errors(doc)))

    def test_blocked_week4_cannot_be_promoted(self):
        doc=copy.deepcopy(self.doc)
        p=next(x for x in doc["publications"] if x["publication_id"]=="memo.2026.week-04")
        p["release_state"]="RELEASED"
        p["canonical_artifact"]="week4.pdf"
        p["release_receipt_refs"]=["memo-os/week-4/WEEK_4_RELEASE_GATE_V1.md"]
        self.assertTrue(any("Week 4 publication cannot be promoted" in x for x in self.errors(doc)))

    def test_living_novel_week_is_not_automatic_chapter(self):
        doc=copy.deepcopy(self.doc)
        p=next(x for x in doc["publications"] if x["publication_id"]=="novel.2026.chapter-02")
        p["source_interval"]["kind"]="week"
        self.assertTrue(any("automatic chapter identity" in x for x in self.errors(doc)))

    def test_chapter3_requires_independent_novel_evidence(self):
        doc=copy.deepcopy(self.doc)
        ch3=next(x for x in doc["publications"] if x["publication_id"]=="novel.2026.chapter-03")
        ch3["release_receipt_refs"]=[]
        self.assertTrue(any("Chapter III requires independent Novel canon/release evidence" in x for x in self.errors(doc)))

    def test_chapter3_current_record_is_canon_closed(self):
        ch3=next(x for x in self.doc["publications"] if x["publication_id"]=="novel.2026.chapter-03")
        self.assertEqual(ch3["release_state"],"CANON_CLOSED")
        self.assertEqual(ch3["canonical_artifact"],"living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md")
        self.assertIn("living-novel/qa/CHAPTER_03_FINAL_CANON_GATE_V1.md",ch3["authority_refs"])
        self.assertIn("living-novel/qa/CHAPTER_03_CANON_RELEASE_RECEIPT_V1.md",ch3["release_receipt_refs"])

    def test_relation_target_must_exist(self):
        doc=copy.deepcopy(self.doc)
        p=doc["publications"][0]
        p["relations"].append({"type":"companion","publication_id":"missing"})
        self.assertTrue(any("relation target missing" in x for x in self.errors(doc)))

    def test_symmetric_relationship_must_be_reciprocal(self):
        doc=copy.deepcopy(self.doc)
        ch2=next(x for x in doc["publications"] if x["publication_id"]=="novel.2026.chapter-02")
        ch2["relations"]=[x for x in ch2["relations"] if not (x["type"]=="interprets_same_source_interval" and x["publication_id"]=="memo.2026.week-02")]
        self.assertTrue(any("lacks reciprocal relation" in x for x in self.errors(doc)))

    def test_released_record_requires_receipt(self):
        doc=copy.deepcopy(self.doc)
        p=next(x for x in doc["publications"] if x["publication_id"]=="memo.2026.week-03")
        p["release_receipt_refs"]=[]
        self.assertTrue(any("RELEASED requires release_receipt_refs" in x for x in self.errors(doc)))

    def test_authority_reference_must_exist(self):
        doc=copy.deepcopy(self.doc)
        p=doc["publications"][0]
        p["authority_refs"].append("does/not/exist.md")
        self.assertTrue(any("missing authority ref" in x for x in self.errors(doc)))

if __name__=="__main__":
    unittest.main()
