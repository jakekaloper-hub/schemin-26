import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[2]
MEMO=ROOT/"memo-os"
EVID=MEMO/"tests"/"V5_6_CURRENT_MAIN_PROMOTION_EVIDENCE.json"
PROJECT=ROOT/"PROJECT_CONTROL_REGISTRY.md"
MANIFEST=ROOT/"governance"/"publication-manifest"/"PUBLICATION_MANIFEST_V1.json"

class V56CurrentMainSalvageTests(unittest.TestCase):
    def test_v55_remains_controlling(self):
        text=PROJECT.read_text()
        self.assertIn("Current controlling build: **V5.5",text)

    def test_salvaged_controls_exist(self):
        names=[
            "PAGE_PRODUCTION_CONTRACT_V1.md",
            "PUBLICATION_FIDELITY_CONTRACT_V1.md",
            "PAGE_FIDELITY_MODEL_V1.md",
            "GENERATION_INTENT_FIREWALL_V1.md",
            "CHARACTER_PACKET_GATE_V1.md",
            "REFERENCE_MOUNT_RECEIPT_V1.md",
            "RENDERER_ADDRESSABLE_ASSET_CONTRACT_V1.md",
            "RUNTIME_BOOTSTRAP_RESOLVER_V1.md",
            "WORLD_ENCOUNTER_BINDING_V1.md",
        ]
        for name in names:
            self.assertTrue((MEMO/name).exists(),name)

    def test_release_registry_is_superseded(self):
        text=(MEMO/"MEMO_RELEASE_REGISTRY_SPEC_V1.md").read_text()
        self.assertIn("SUPERSEDED",text)
        self.assertIn("governance/publication-manifest/PUBLICATION_MANIFEST_V1.json",text)
        self.assertIn("governance/release-evidence/registry.json",text)
        self.assertIn("Do not create or maintain a second active Memo release registry",text)

    def test_fixture_hash_is_fixed(self):
        data=json.loads(EVID.read_text())
        fx=data["week4_fixture_exact_bytes"]
        self.assertEqual(fx["status"],"PASS")
        self.assertEqual(fx["byte_length"],253543)
        self.assertEqual(fx["sha256"],"4aba1fe41e8fc2c1e5ff247d02e7fcc69ffe7a72c7650782f8308fc7c61f654a")

    def test_real_page_fidelity_still_fails(self):
        data=json.loads(EVID.read_text())
        page=data["week4_real_page_acceptance"]
        self.assertEqual(page["technical_acceptance"],"PASS")
        self.assertEqual(page["publication_fidelity"],"FAIL")
        self.assertEqual(page["real_page_acceptance"],"FAIL")

    def test_promotion_remains_hold(self):
        data=json.loads(EVID.read_text())
        self.assertEqual(data["week2_controlled_reconstruction"]["status"],"MISSING")
        self.assertEqual(data["week2_exact_canonical_binary"]["status"],"SOURCE_BYTES_REQUIRED")
        self.assertEqual(data["independent_release_audit"]["status"],"BLOCKED")
        self.assertEqual(data["promotion"]["status"],"HOLD")

    def test_week4_publication_manifest_remains_blocked(self):
        data=json.loads(MANIFEST.read_text())
        w4=next(x for x in data["publications"] if x["publication_id"]=="memo.2026.week-04")
        self.assertEqual(w4["release_state"],"BLOCKED")
        self.assertIsNone(w4["canonical_artifact"])

if __name__=="__main__":
    unittest.main(verbosity=2)
