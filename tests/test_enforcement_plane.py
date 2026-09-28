import copy, json, tempfile, unittest
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("enforcement_validate",ROOT/"governance/enforcement/validate.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class EnforcementKernelTests(unittest.TestCase):
    def setUp(self):
        self.registry=mod.load_registry(ROOT)

    def test_registry_is_valid(self):
        mod.validate_registry(ROOT,self.registry)

    def test_policy_ids_are_unique(self):
        ids=[p["policy_id"] for p in self.registry["policies"]]
        self.assertEqual(len(ids),len(set(ids)))

    def test_duplicate_policy_id_fails(self):
        reg=copy.deepcopy(self.registry)
        reg["policies"].append(copy.deepcopy(reg["policies"][0]))
        with self.assertRaises(mod.EnforcementFailure):
            mod.validate_registry(ROOT,reg)

    def test_invalid_severity_fails(self):
        reg=copy.deepcopy(self.registry)
        reg["policies"][0]["severity"]="NUCLEAR"
        with self.assertRaises(mod.EnforcementFailure):
            mod.validate_registry(ROOT,reg)

    def test_missing_validator_fails(self):
        reg=copy.deepcopy(self.registry)
        reg["policies"][0]["validator"]="does_not_exist"
        with self.assertRaises(mod.EnforcementFailure):
            mod.validate_registry(ROOT,reg)


    def test_authority_validator_passes_repo(self):
        self.assertEqual(mod.validate_authority_uniqueness(ROOT,self.registry),[])

    def test_authority_validator_rejects_duplicate_master(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"canon").mkdir(parents=True)
            (root/"living-novel/os/adapters/flaim").mkdir(parents=True)
            (root/"canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md").write_text("x")
            (root/"SCHEMIN_26_MASTER_CHARACTER_CANON_COPY.md").write_text("x")
            (root/"living-novel/os/adapters/flaim/PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json").write_text("{}")
            errors=mod.validate_authority_uniqueness(root,self.registry)
            self.assertTrue(any("active master character canon set invalid" in e for e in errors))

    def test_authority_validator_rejects_resurrected_handoff(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"canon").mkdir(parents=True)
            (root/"living-novel/os/adapters/flaim").mkdir(parents=True)
            (root/"canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md").write_text("x")
            (root/"living-novel/os/adapters/flaim/PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json").write_text("{}")
            (root/"XCODE_CHATGPT_HANDOFF.md").write_text("ACTIVE")
            errors=mod.validate_authority_uniqueness(root,self.registry)
            self.assertTrue(any("retired active path resurrected" in e for e in errors))


    def test_temporal_validator_passes_repo(self):
        self.assertEqual(mod.validate_temporal_state(ROOT,self.registry),[])

    def test_temporal_validator_rejects_unsuperseded_v1(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"docs/governance").mkdir(parents=True)
            (root/"docs/governance/SUBSYSTEM_TEMPORAL_LINEAGE_CONTRACT_V1.md").write_text("ACTIVE")
            p=root/"chronicles/proof-of-concept/prologue"
            p.mkdir(parents=True)
            (p/"PROLOGUE_MANUSCRIPT_V1.md").write_text("old")
            (p/"PROLOGUE_MANUSCRIPT_V2_AUDITED.md").write_text("SUPERSEDED HISTORICAL MANUSCRIPT\nDO NOT USE AS CURRENT PRODUCTION PARENT")
            (p/"PROLOGUE_MANUSCRIPT_V3_REBUILD.md").write_text("SUPERSEDED HISTORICAL MANUSCRIPT\nDO NOT USE AS CURRENT PRODUCTION PARENT")
            (p/"PROLOGUE_MANUSCRIPT_V4_CONSULTANT_REVISION.md").write_text("CURRENT PRODUCTION PARENT\ncurrent production parent does not mean final published manuscript")
            (root/"mercer").mkdir()
            (root/"mercer/OPERATING_CONTRACT.md").write_text("Historical recommendations are decision-journal evidence, not standing instructions\ncurrent-state evidence is freshly resolved through the Data Gateway / controlling ledger")
            errors=mod.validate_temporal_state(root,self.registry)
            self.assertTrue(any("V1" in e or "PROLOGUE_MANUSCRIPT_V1" in e for e in errors))


    def test_mercer_firewall_passes_repo(self):
        self.assertEqual(mod.validate_mercer_firewall(ROOT,self.registry),[])

    def test_mercer_firewall_rejects_public_grade(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            p=root/"chronicles/chapter.md"
            p.parent.mkdir(parents=True)
            p.write_text("Post-draft evidence: Mercer grade A+.")
            errors=mod.validate_mercer_firewall(root,self.registry)
            self.assertTrue(any("Mercer grade" in e for e in errors))

    def test_mercer_firewall_allows_explicit_firewall_warning(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            p=root/"chronicles/proof-of-concept/prologue/PROLOGUE_PRESEASON_EVIDENCE_AND_EMOTIONAL_SPINE.md"
            p.parent.mkdir(parents=True)
            p.write_text("private Mercer grades, valuations, recommendations are not public evidence")
            self.assertEqual(mod.validate_mercer_firewall(root,self.registry),[])

    def test_merge_kernel_runs(self):
        self.assertTrue(mod.run(ROOT,"MERGE"))

if __name__=="__main__":
    unittest.main()
