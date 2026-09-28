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


    def test_prompt_governance_passes_repo(self):
        self.assertEqual(mod.validate_prompt_governance(ROOT,self.registry),[])

    def test_prompt_governance_rejects_retired_title(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            p=root/"foo/MASTER_PROMPT.md"
            p.parent.mkdir(parents=True)
            p.write_text("Use Frat-Bro Berserker as the current character.")
            errors=mod.validate_prompt_governance(root,self.registry)
            self.assertTrue(any("retired Slob title" in e for e in errors))

    def test_prompt_governance_ignores_archive_history(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            p=root/"archive/legacy/OLD_PROMPT.md"
            p.parent.mkdir(parents=True)
            p.write_text("Use Frat-Bro Berserker")
            self.assertEqual(mod.validate_prompt_governance(root,self.registry),[])


    def test_publication_release_passes_repo(self):
        self.assertEqual(mod.validate_publication_release(ROOT,self.registry),[])

    def test_publication_release_rejects_unregistered_release(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"governance/enforcement").mkdir(parents=True)
            (root/"governance/enforcement/RELEASE_REGISTRY_V1.json").write_text('{"releases":[]}')
            (root/"governance/enforcement/RELEASE_MANIFEST_CONTRACT_V1.md").write_text("contract")
            p=root/"memo-os/week-9/FINAL.md"
            p.parent.mkdir(parents=True)
            p.write_text("**Status:** RELEASED")
            errors=mod.validate_publication_release(root,self.registry)
            self.assertTrue(any("lacks release registry record" in e for e in errors))

    def test_publication_release_accepts_registered_release(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"governance/enforcement").mkdir(parents=True)
            rec={
                "artifact_path":"memo-os/week-9/FINAL.md",
                "status":"RELEASED",
                "source_commit":"abc123",
                "released_at":"2026-09-28T15:00:00Z",
                "authority":"The Closer",
                "qa_gates":["final-artifact-qa"]
            }
            (root/"governance/enforcement/RELEASE_REGISTRY_V1.json").write_text(json.dumps({"releases":[rec]}))
            (root/"governance/enforcement/RELEASE_MANIFEST_CONTRACT_V1.md").write_text("contract")
            p=root/"memo-os/week-9/FINAL.md"
            p.parent.mkdir(parents=True)
            p.write_text("**Status:** RELEASED")
            self.assertEqual(mod.validate_publication_release(root,self.registry),[])


    def test_exception_registry_passes_repo(self):
        self.assertEqual(mod.validate_exceptions(ROOT,self.registry),[])

    def test_exception_rejects_commissioner_policy_without_commissioner(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"governance/enforcement").mkdir(parents=True)
            rec={
                "exception_id":"EX-1",
                "policy_id":"CANON-001",
                "scope_glob":"canon/**",
                "reason":"Temporary controlled canon test",
                "approved_by":["Character QA"],
                "approved_at":"2026-09-28T15:00:00Z",
                "review_trigger":"remove after test",
                "status":"ACTIVE"
            }
            (root/"governance/enforcement/EXCEPTIONS_V1.json").write_text(json.dumps({"exceptions":[rec]}))
            errors=mod.validate_exceptions(root,self.registry)
            self.assertTrue(any("requires Jake / Commissioner approval" in e for e in errors))

    def test_exception_rejects_expired_record(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"governance/enforcement").mkdir(parents=True)
            rec={
                "exception_id":"EX-2",
                "policy_id":"AUTH-001",
                "scope_glob":"foo/**",
                "reason":"Temporary controlled authority migration",
                "approved_by":["Umpire"],
                "approved_at":"2026-09-01T00:00:00Z",
                "expires_at":"2026-09-02T00:00:00Z",
                "status":"ACTIVE"
            }
            (root/"governance/enforcement/EXCEPTIONS_V1.json").write_text(json.dumps({"exceptions":[rec]}))
            errors=mod.validate_exceptions(root,self.registry)
            self.assertTrue(any("is expired" in e for e in errors))

    def test_valid_prompt_exception_is_narrow(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"governance/enforcement").mkdir(parents=True)
            rec={
                "exception_id":"EX-3",
                "policy_id":"PROMPT-001",
                "scope_glob":"foo/MASTER_PROMPT.md",
                "reason":"Historical migration prompt retained for one review",
                "approved_by":["Librarian"],
                "approved_at":"2026-09-28T15:00:00Z",
                "review_trigger":"remove after migration review",
                "status":"ACTIVE"
            }
            (root/"governance/enforcement/EXCEPTIONS_V1.json").write_text(json.dumps({"exceptions":[rec]}))
            p=root/"foo/MASTER_PROMPT.md"
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text("Use Frat-Bro Berserker")
            self.assertEqual(mod.validate_prompt_governance(root,self.registry),[])


    def test_native_character_canon_passes_repo(self):
        self.assertEqual(mod.validate_character_canon(ROOT,self.registry),[])

    def test_native_character_canon_rejects_title_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"governance/enforcement").mkdir(parents=True)
            (root/"canon").mkdir(parents=True)
            (root/"living-novel/os/adapters/flaim").mkdir(parents=True)

            assertions={
                "source_visual_lock":"canon/LOCK.md",
                "source_sha256":"abc",
                "owners":{"Jake Kaloper":{"title":"The Trade Jedi","invariants":["NO CHAMPIONSHIP BELT"]}}
            }
            (root/"governance/enforcement/CANON_ASSERTIONS_V1.json").write_text(json.dumps(assertions))
            (root/"canon/LOCK.md").write_text("abc")
            (root/"living-novel/os/adapters/flaim/PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json").write_text(json.dumps({
                "records":[{"owner":"Jake Kaloper","canonical_character":"Wrong Jedi","hard_invariants":["NO CHAMPIONSHIP BELT"]}]
            }))
            (root/"canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md").write_text("### Jake Kaloper / ObiWan Jacoby\n**Character:** The Trade Jedi.\nNO CHAMPIONSHIP BELT")
            errors=mod.validate_character_canon(root,self.registry)
            self.assertTrue(any("title mismatch" in e for e in errors))


    def test_security_scan_passes_repo(self):
        self.assertEqual(mod.validate_security_scan(ROOT,self.registry),[])

    def test_security_scan_rejects_token_signature(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            p=root/"bad.txt"
            p.write_text("token = ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456")
            errors=mod.validate_security_scan(root,self.registry)
            self.assertTrue(any("GitHub classic token" in e for e in errors))

    def test_historical_identity_passes_repo(self):
        self.assertEqual(mod.validate_historical_identity(ROOT,self.registry),[])

    def test_historical_identity_rejects_retired_current_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            p=root/"world/history/2025/2025_OWNER_TEAM_ALIAS_MAP.md"
            p.parent.mkdir(parents=True)
            p.write_text(
                "HISTORICAL EVIDENCE / IDENTITY RESOLUTION — TO VERIFY WHERE MARKED\n"
                "canon/SCHEMIN_26_MASTER_VISUAL_CANON_REFERENCE_LOCK_V1.md\n"
                "canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md\n"
                "TO VERIFY\n"
                "Frat-Bro Berserker / established Slob"
            )
            errors=mod.validate_historical_identity(root,self.registry)
            self.assertTrue(any("retired current-identity authority" in e for e in errors))

    def test_index_integrity_passes_repo(self):
        self.assertEqual(mod.validate_index_integrity(ROOT,self.registry),[])

    def test_index_integrity_rejects_retired_reference(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for rel in ["archive/_INDEX.md","canon/_INDEX.md","memo-os/_INDEX.md","data-gateway/_INDEX.md","mercer/_INDEX.md"]:
                p=root/rel
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_text("SCHEMIN_26_MASTER_VISUAL_CANON_REFERENCE_LOCK_V1.md")
            (root/"memo-os/_INDEX.md").write_text("XCODE_CHATGPT_HANDOFF.md")
            errors=mod.validate_index_integrity(root,self.registry)
            self.assertTrue(any("retired authority" in e for e in errors))

    def test_data_gateway_dependency_is_auditable(self):
        result=mod.validate_data_gateway_dependency(ROOT,self.registry)
        self.assertIsInstance(result,list)

    def test_release_kernel_runs(self):
        self.assertTrue(mod.run(ROOT,"RELEASE"))

    def test_merge_kernel_runs(self):
        self.assertTrue(mod.run(ROOT,"MERGE"))

if __name__=="__main__":
    unittest.main()
