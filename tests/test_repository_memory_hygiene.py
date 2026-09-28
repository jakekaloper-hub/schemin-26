import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class RepositoryMemoryHygieneTests(unittest.TestCase):
    def test_retired_active_paths_are_absent(self):
        retired = [
            "world/canon/SCHEMIN_26_MASTER_CHARACTER_CANON_V1_1.md",
            "XCODE_CHATGPT_HANDOFF.md",
            "XCODE_HANDOFF_PRO_SCHEMIN_WORLD.md",
            "living-novel/os/adapters/flaim/registries/PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json",
        ]
        for rel in retired:
            self.assertFalse((ROOT / rel).exists(), rel)

    def test_single_active_master_character_canon(self):
        active = [
            p for p in ROOT.rglob("SCHEMIN_26_MASTER_CHARACTER_CANON*.md")
            if "archive" not in p.parts
        ]
        self.assertEqual(
            [p.relative_to(ROOT).as_posix() for p in active],
            ["canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md"],
        )

    def test_single_active_flaim_identity_registry(self):
        active = [
            p for p in ROOT.rglob("PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json")
            if "archive" not in p.parts
        ]
        self.assertEqual(
            [p.relative_to(ROOT).as_posix() for p in active],
            ["living-novel/os/adapters/flaim/PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json"],
        )

    def test_quarantined_markdown_has_historical_banner(self):
        paths = [
            ROOT / "archive/legacy-canon/SCHEMIN_26_MASTER_CHARACTER_CANON_V1_1_HISTORICAL_ONLY.md",
            ROOT / "archive/legacy-handoffs/XCODE_CHATGPT_HANDOFF_2026-09-26_HISTORICAL_ONLY.md",
            ROOT / "archive/legacy-handoffs/XCODE_HANDOFF_PRO_SCHEMIN_WORLD_2026-09-26_HISTORICAL_ONLY.md",
        ]
        for path in paths:
            self.assertTrue(path.exists(), path)
            first = path.read_text().splitlines()[0]
            self.assertEqual(first, "# HISTORICAL ONLY — DO NOT USE AS CURRENT PRODUCTION AUTHORITY")

    def test_quarantined_json_declares_archive_status(self):
        path = ROOT / "archive/identity-history/PRO_SCHEMIN_IDENTITY_RESOLUTION_V1_LEGACY_REGISTRY.json"
        data = json.loads(path.read_text())
        self.assertEqual(data.get("_archive_status"), "ARCHIVE_ONLY")
        self.assertIn("Canonical current registry", data.get("_reason", ""))

    def test_memory_architecture_and_authority_graph_exist(self):
        required = [
            "docs/governance/REPOSITORY_MEMORY_ARCHITECTURE_V1.md",
            "planning/ACTIVE_AUTHORITY_GRAPH_V1.md",
            "planning/DEPRECATION_SUPERSESSION_LEDGER_V1.md",
            "planning/CHARACTER_CONTAMINATION_MATRIX_V1.md",
        ]
        for rel in required:
            self.assertTrue((ROOT / rel).exists(), rel)


    def test_temporal_lineage_contract_is_exposed(self):
        contract = (ROOT / "docs/governance/SUBSYSTEM_TEMPORAL_LINEAGE_CONTRACT_V1.md").read_text()
        self.assertIn("V1 → V2_AUDITED → V3_REBUILD → V4_CONSULTANT_REVISION", contract)
        self.assertIn("Past recommendations belong in the Decision Journal", contract)

        novel = (ROOT / "living-novel/README.md").read_text()
        self.assertIn("V4 Consultant Revision is the current production parent", novel)

        mercer = (ROOT / "mercer/OPERATING_CONTRACT.md").read_text()
        self.assertIn("Historical recommendations are decision-journal evidence, not standing instructions", mercer)


    def test_public_chronicle_evidence_does_not_import_private_mercer_grades(self):
        path = ROOT / "chronicles/proof-of-concept/prologue/PROLOGUE_PRESEASON_EVIDENCE_AND_EMOTIONAL_SPINE.md"
        text = path.read_text()
        forbidden = [
            "Mercer grade",
            "Mercer judged",
            "A+ starting hand in Mercer audit",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, text)
        self.assertIn("private Mercer grades, valuations, recommendations", text)

if __name__ == "__main__":
    unittest.main()
