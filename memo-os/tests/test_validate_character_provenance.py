import copy, hashlib, tempfile, unittest
from pathlib import Path
from validate_character_provenance import validate_character_provenance


def sha(b): return hashlib.sha256(b).hexdigest()


class RenderProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name)
        (self.root/"source.jpeg").write_bytes(b"synthetic source")
        (self.root/"raster.png").write_bytes(b"synthetic page master")
        self.receipt={
            "character_id":"CHAR-TEST-OWNER","owner_id":"OWNER-TEST",
            "canonical_asset_path":"source.jpeg",
            "expected_sha256":sha(b"synthetic source"),
            "mounted_sha256":sha(b"synthetic source"),
            "generation_reference_id":"native-ref-1",
            "subject_slot":"subject-1",
            "subject_binding_id":"binding-receipt-1",
            "subject_binding_proven":True,
            "renderer_route":"test-renderer",
            "mount_receipt_id":"test-mount",
            "capability_receipt_id":"test-capability",
            "output_instance_id":"test-output",
            "generation_operator_id":"artist",
            "independent_reviewer_id":"auditor",
            "reviewed_raster_path":"raster.png",
            "raster_sha256":sha(b"synthetic page master"),
            "raster_qa_decision":"PASS"}
        self.d={"publication_state":"PUBLISHED","pages":[{"slot":1,"characters":["CHAR-TEST-OWNER"],
                "asset_sha256":sha(b"synthetic page master"),
                "character_generation_receipts":[self.receipt]}]}

    def fails(self,data,needle):
        errs=validate_character_provenance(data,self.root)
        self.assertTrue(any(needle in e for e in errs),errs)

    def test_synthetic_contract_shape_passes_not_identity_proof(self):
        self.assertEqual(validate_character_provenance(self.d,self.root),[])

    def test_no_subject_binding(self):
        d=copy.deepcopy(self.d);d["pages"][0]["character_generation_receipts"][0]["subject_binding_proven"]=False
        self.fails(d,"unproven reference-to-subject")

    def test_missing_mount(self):
        d=copy.deepcopy(self.d);d["pages"][0]["character_generation_receipts"][0]["mount_receipt_id"]=""
        self.fails(d,"missing mount_receipt_id")

    def test_wrong_mounted_source(self):
        d=copy.deepcopy(self.d);d["pages"][0]["character_generation_receipts"][0]["mounted_sha256"]="0"*64
        self.fails(d,"mounted source hash mismatch")

    def test_missing_source_bytes(self):
        d=copy.deepcopy(self.d);d["pages"][0]["character_generation_receipts"][0]["canonical_asset_path"]="absent.jpeg"
        self.fails(d,"missing accessible canonical_asset_path")

    def test_swap_subject(self):
        d=copy.deepcopy(self.d);d["pages"][0]["character_generation_receipts"][0]["character_id"]="CHAR-WRONG"
        self.fails(d,"unexpected or duplicated")

    def test_missing_second_character_receipt(self):
        d=copy.deepcopy(self.d);d["pages"][0]["characters"].append("CHAR-SECOND")
        self.fails(d,"missing generation receipts")

    def test_reviewer_is_creator(self):
        d=copy.deepcopy(self.d);d["pages"][0]["character_generation_receipts"][0]["independent_reviewer_id"]="artist"
        self.fails(d,"not independent")

    def test_missing_generation_operator_cannot_prove_independence(self):
        for value in (None, "", "   "):
            with self.subTest(value=value):
                d=copy.deepcopy(self.d)
                receipt=d["pages"][0]["character_generation_receipts"][0]
                if value is None:
                    receipt.pop("generation_operator_id")
                else:
                    receipt["generation_operator_id"]=value
                self.fails(d,"missing generation_operator_id")

    def test_raster_qa_failed(self):
        d=copy.deepcopy(self.d);d["pages"][0]["character_generation_receipts"][0]["raster_qa_decision"]="HOLD"
        self.fails(d,"failed final-raster")

    def test_raster_swapped(self):
        d=copy.deepcopy(self.d);d["pages"][0]["asset_sha256"]="a"*64
        self.fails(d,"final-raster hash mismatch")

    def test_review_not_proven_by_field(self):
        d=copy.deepcopy(self.d);d["pages"][0]["character_generation_receipts"]=[]
        self.fails(d,"missing generation receipts")

    def test_review_candidate_not_published(self):
        d=copy.deepcopy(self.d);d["publication_state"]="REVIEW"
        d["pages"][0]["character_generation_receipts"]=[]
        self.assertEqual(validate_character_provenance(d,self.root),[])


if __name__=="__main__":unittest.main()
