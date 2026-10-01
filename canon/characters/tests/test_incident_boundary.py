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
HASH = "a" * 64


def asset(uri="repo://canon/assets/zach.jpg", cid=CID):
    return AssetReference(
        "A1", cid, "ZACH", uri, HASH, "image/jpeg", 100, 100,
        "1", "APPROVED", "HIGH", "commissioner",
    )


def mount(*, attached=True, bound=True, slot="subject-1", route="test"):
    return CharacterReferenceMount(
        CID, "ZACH", "A1", "repo://x", HASH, "image/jpeg", (100, 100),
        "1", "APPROVED", True, True, True, attached, route,
        "ref-1" if attached else None,
        slot,
        bound,
        "bind-1" if bound else None,
        "now",
    )


CAP = {
    "test": {
        "supports_image_references": True,
        "returns_attachment_receipt": True,
        "supports_subject_binding": True,
        "returns_subject_binding_receipt": True,
        "max_references": 4,
        "reference_mechanism": "test",
        "subject_binding_mechanism": "slot-map",
    }
}


class Boundary(unittest.TestCase):
    def test_nonportable_blocks(self):
        result = resolve_assets([CID], {CID: asset(None)})
        self.assertEqual(request_state(result), "GENERATION_BLOCKED")

    def test_swap_blocks(self):
        result = resolve_assets([CID], {CID: asset(cid="CHAR-AUSTIN-BYARS")})
        self.assertEqual(request_state(result), "GENERATION_BLOCKED")

    def test_reference_only_route_is_not_enough(self):
        refs_only = {
            "route": {
                "supports_image_references": True,
                "returns_attachment_receipt": True,
                "supports_subject_binding": False,
                "returns_subject_binding_receipt": False,
                "max_references": 4,
            }
        }
        self.assertEqual(
            negotiate("route", refs_only, 1)["state"],
            "GENERATION_ROUTE_SUBJECT_BINDING_UNPROVEN",
        )

    def test_missing_subject_binding_blocks(self):
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], [mount(bound=False)], "test", capability,
            signing_key="test-key", now=1,
        )
        self.assertEqual(eligible["state"], "GENERATION_BLOCKED")

    def test_eligibility_is_request_route_asset_and_subject_bound(self):
        mounts = [mount()]
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], mounts, "test", capability,
            signing_key="test-key", now=1,
        )
        self.assertEqual(
            validate_eligibility(
                eligible, "r", [CID], mounts, "test",
                signing_key="test-key", now=2,
            ),
            "GENERATION_ELIGIBLE",
        )
        self.assertEqual(
            validate_eligibility(
                eligible, "other", [CID], mounts, "test",
                signing_key="test-key", now=2,
            ),
            "GENERATION_BLOCKED",
        )
        self.assertEqual(
            validate_eligibility(
                eligible, "r", [CID], [mount(slot="subject-2")], "test",
                signing_key="test-key", now=2,
            ),
            "GENERATION_BLOCKED",
        )

    def test_nonce_replay_blocks(self):
        mounts = [mount()]
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], mounts, "test", capability,
            signing_key="test-key", now=1, nonce="once",
        )
        used = {"once"}
        self.assertEqual(
            validate_eligibility(
                eligible, "r", [CID], mounts, "test",
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
            [CID], [mount()], "test", {}, signing_key="test-key",
        )
        self.assertEqual(result["state"], "GENERATION_BLOCKED")
        self.assertEqual(called["n"], 0)

    def test_missing_output_receipt_never_becomes_qa_pass(self):
        mounts = [mount()]
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], mounts, "test", capability,
            signing_key="test-key", now=1,
        )
        result = governed_generate(
            lambda payload: {"pixels": "opaque"},
            eligible, "r", [CID], mounts, "test", {},
            signing_key="test-key", consumed_nonces=set(),
        )
        self.assertEqual(result["state"], "GENERATION_OUTPUT_BLOCKED")
        self.assertTrue(result["renderer_invoked"])

    def test_valid_adapter_result_is_pending_character_qa_not_pass(self):
        mounts = [mount()]
        capability = negotiate("test", CAP, 1)
        eligible = issue_eligibility(
            "r", [CID], mounts, "test", capability,
            signing_key="test-key", now=1,
        )
        result = governed_generate(
            lambda payload: {"output_instance_id": "out-1"},
            eligible, "r", [CID], mounts, "test", {},
            signing_key="test-key", consumed_nonces=set(),
        )
        self.assertEqual(result["state"], "GENERATION_EXECUTED_PENDING_CHARACTER_QA")


if __name__ == "__main__":
    unittest.main()
