import unittest

from canon.characters.runtime.asset_reference import AssetReference
from canon.characters.runtime.asset_resolver import request_state, resolve_assets
from canon.characters.runtime.generation_adapter import governed_generate
from canon.characters.runtime.generation_eligibility import (
    issue_eligibility,
    validate_eligibility,
)
from canon.characters.runtime.reference_mount import CharacterReferenceMount
from canon.characters.runtime.renderer_capabilities import negotiate


CID = "CHAR-ZACH-WILSON"
CID2 = "CHAR-AUSTIN-BYARS"
HASH = "a" * 64
BLOB = "b" * 40
CAP_RECEIPT = "cap-test-1"


def asset(uri="repo://canon/assets/zach.jpg", cid=CID):
    return AssetReference(
        "A1", cid, "ZACH", uri, HASH, "image/jpeg", 100, 100,
        "1", "APPROVED", "HIGH", "commissioner",
    )


def mount(
    *,
    cid=CID,
    owner="ZACH",
    asset_id="A1",
    attached=True,
    bound=True,
    slot="subject-1",
    route="test",
    expected_hash=HASH,
    mounted_hash=HASH,
    mount_receipt_id="mount-1",
    binding_id="bind-1",
    generation_reference_id="ref-1",
    capability_receipt_id=CAP_RECEIPT,
):
    return CharacterReferenceMount(
        cid, owner, asset_id, f"repo://canon/assets/{cid}.jpg", HASH,
        "image/jpeg", (100, 100), "1", "APPROVED",
        True, True, True, attached, route,
        generation_reference_id if attached else None,
        slot,
        bound,
        binding_id if bound else None,
        "now",
        expected_hash,
        mounted_hash,
        f"canon/characters/assets/{cid}/primary/source.jpeg",
        BLOB,
        100,
        mount_receipt_id,
        capability_receipt_id,
    )


CAP = {
    "test": {
        "evidence_state": "PROVEN",
        "capability_receipt_id": CAP_RECEIPT,
        "supports_image_references": True,
        "returns_attachment_receipt": True,
        "returns_mounted_byte_hash_receipt": True,
        "supports_subject_binding": True,
        "returns_subject_binding_receipt": True,
        "max_references": 12,
        "reference_mechanism": "test",
        "subject_binding_mechanism": "slot-map",
    }
}


def execution_receipt(request_id, route, mounts):
    return {
        "request_id": request_id,
        "route": route,
        "mount_receipt_ids": sorted(m.mount_receipt_id for m in mounts),
        "generation_reference_ids": sorted(m.generation_reference_id for m in mounts),
        "subject_binding_ids": sorted(m.subject_binding_id for m in mounts),
    }


def authority_receipt(*ids):
    return {
        "state": "REFERENCE_AUTHORITY_RESOLVED",
        "results": [
            {
                "state": "REFERENCE_AUTHORITY_RESOLVED",
                "character_id": cid,
                "expected_sha256": HASH,
                "source_filename": f"{cid}.jpeg",
            }
            for cid in ids
        ],
    }


class Boundary(unittest.TestCase):
    def test_nonportable_blocks(self):
        result = resolve_assets([CID], {CID: asset(None)})
        self.assertEqual(request_state(result), "GENERATION_BLOCKED")

    def test_swap_blocks(self):
        result = resolve_assets([CID], {CID: asset(cid="CHAR-AUSTIN-BYARS")})
        self.assertEqual(request_state(result), "GENERATION_BLOCKED")

    def test_unproven_capability_evidence_blocks(self):
        unproven = {"route": dict(CAP["test"], evidence_state="UNPROVEN")}
        self.assertEqual(
            negotiate("route", unproven, 1)["reason"],
            "CAPABILITY_EVIDENCE_UNPROVEN",
        )

    def test_reference_only_route_is_not_enough(self):
        refs_only = {
            "route": {
                "evidence_state": "PROVEN",
                "capability_receipt_id": "cap",
                "supports_image_references": True,
                "returns_attachment_receipt": True,
                "returns_mounted_byte_hash_receipt": True,
                "supports_subject_binding": False,
                "returns_subject_binding_receipt": False,
                "max_references": 4,
            }
        }
        self.assertEqual(
            negotiate("route", refs_only, 1)["state"],
            "GENERATION_ROUTE_SUBJECT_BINDING_UNPROVEN",
        )

    def test_missing_mounted_byte_hash_blocks(self):
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], [mount(mounted_hash=None)], "test", capability,
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", now=1,
        )
        self.assertEqual(eligible["state"], "GENERATION_BLOCKED")

    def test_mounted_hash_mismatch_blocks(self):
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], [mount(mounted_hash="c" * 64)], "test", capability,
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", now=1,
        )
        self.assertEqual(eligible["state"], "GENERATION_BLOCKED")

    def test_missing_subject_binding_blocks(self):
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], [mount(bound=False)], "test", capability,
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", now=1,
        )
        self.assertEqual(eligible["state"], "GENERATION_BLOCKED")

    def test_capability_receipt_mismatch_blocks(self):
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], [mount(capability_receipt_id="wrong")],
            "test", capability, authority_receipt=authority_receipt(CID), signing_key="test-key", now=1,
        )
        self.assertEqual(eligible["reason"], "CAPABILITY_RECEIPT_MISMATCH")

    def test_eligibility_is_request_route_asset_and_subject_bound(self):
        mounts = [mount()]
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], mounts, "test", capability,
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", now=1,
        )
        self.assertEqual(
            validate_eligibility(
                eligible, "r", [CID], mounts, "test",
                authority_receipt=authority_receipt(CID),
                signing_key="test-key", now=2,
            ),
            "GENERATION_ELIGIBLE",
        )
        self.assertEqual(
            validate_eligibility(
                eligible, "other", [CID], mounts, "test",
                authority_receipt=authority_receipt(CID),
                signing_key="test-key", now=2,
            ),
            "GENERATION_BLOCKED",
        )
        self.assertEqual(
            validate_eligibility(
                eligible, "r", [CID], [mount(slot="subject-2")], "test",
                authority_receipt=authority_receipt(CID),
                signing_key="test-key", now=2,
            ),
            "GENERATION_BLOCKED",
        )

    def test_multi_character_order_does_not_change_binding(self):
        m1 = mount()
        m2 = mount(
            cid=CID2, owner="AUSTIN", asset_id="A2",
            slot="subject-2", mount_receipt_id="mount-2",
            binding_id="bind-2", generation_reference_id="ref-2",
        )
        capability = negotiate("test", CAP, 2)
        eligible = issue_eligibility(
            "r2", [CID2, CID], [m1, m2], "test", capability,
            authority_receipt=authority_receipt(CID2, CID),
            signing_key="test-key", now=1,
        )
        self.assertEqual(eligible["state"], "GENERATION_ELIGIBLE")
        self.assertEqual(
            validate_eligibility(
                eligible, "r2", [CID, CID2], [m2, m1], "test",
                authority_receipt=authority_receipt(CID, CID2),
                signing_key="test-key", now=2,
            ),
            "GENERATION_ELIGIBLE",
        )

    def test_duplicate_subject_slot_blocks_multi_character(self):
        m1 = mount()
        m2 = mount(
            cid=CID2, owner="AUSTIN", asset_id="A2",
            slot="subject-1", mount_receipt_id="mount-2",
            binding_id="bind-2", generation_reference_id="ref-2",
        )
        capability = negotiate("test", CAP, 2)
        eligible = issue_eligibility(
            "r2", [CID, CID2], [m1, m2], "test", capability,
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", now=1,
        )
        self.assertEqual(eligible["state"], "GENERATION_BLOCKED")

    def test_duplicate_mount_receipt_blocks_multi_character(self):
        m1 = mount()
        m2 = mount(
            cid=CID2, owner="AUSTIN", asset_id="A2",
            slot="subject-2", mount_receipt_id="mount-1",
            binding_id="bind-2", generation_reference_id="ref-2",
        )
        capability = negotiate("test", CAP, 2)
        eligible = issue_eligibility(
            "r2", [CID, CID2], [m1, m2], "test", capability,
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", now=1,
        )
        self.assertEqual(eligible["state"], "GENERATION_BLOCKED")

    def test_nonce_replay_blocks(self):
        mounts = [mount()]
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], mounts, "test", capability,
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", now=1, nonce="once",
        )
        used = {"once"}
        self.assertEqual(
            validate_eligibility(
                eligible, "r", [CID], mounts, "test",
                authority_receipt=authority_receipt(CID),
                signing_key="test-key", now=2, consumed_nonces=used,
            ),
            "GENERATION_BLOCKED",
        )

    def test_adapter_blocks_direct_bypass(self):
        called = {"n": 0}

        def renderer(payload):
            called["n"] += 1
            return {"output_instance_id": "out-1"}

        result = governed_generate(
            renderer, {"state": "GENERATION_BLOCKED"}, "r",
            [CID], [mount()], "test", {}, authority_receipt=authority_receipt(CID), signing_key="test-key",
        )
        self.assertEqual(result["state"], "GENERATION_BLOCKED")
        self.assertEqual(called["n"], 0)

    def test_missing_output_receipt_never_becomes_qa_pass(self):
        mounts = [mount()]
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], mounts, "test", capability,
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", now=1,
        )
        result = governed_generate(
            lambda payload: {"pixels": "opaque"},
            eligible, "r", [CID], mounts, "test", {},
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", consumed_nonces=set(), now=2,
        )
        self.assertEqual(result["state"], "GENERATION_OUTPUT_BLOCKED")
        self.assertTrue(result["renderer_invoked"])

    def test_output_without_reference_execution_receipt_blocks(self):
        mounts = [mount()]
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], mounts, "test", capability,
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", now=1,
        )
        result = governed_generate(
            lambda payload: {"output_instance_id": "out-1"},
            eligible, "r", [CID], mounts, "test", {},
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", consumed_nonces=set(), now=2,
        )
        self.assertEqual(result["state"], "GENERATION_OUTPUT_BLOCKED")
        self.assertIn("REFERENCE_EXECUTION_RECEIPT", result["reason"])

    def test_valid_adapter_result_is_pending_character_qa_not_pass(self):
        mounts = [mount()]
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], mounts, "test", capability,
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", now=1,
        )
        receipt = execution_receipt("r", "test", mounts)
        result = governed_generate(
            lambda payload: {
                "output_instance_id": "out-1",
                "execution_receipt": receipt,
            },
            eligible, "r", [CID], mounts, "test", {},
            authority_receipt=authority_receipt(CID),
            signing_key="test-key", consumed_nonces=set(), now=2,
        )
        self.assertEqual(result["state"], "GENERATION_EXECUTED_PENDING_CHARACTER_QA")
        self.assertEqual(result["execution_receipt"], receipt)


if __name__ == "__main__":
    unittest.main()
