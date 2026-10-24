"""Page preflight must use current source authority, not historical receipt hashes."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('week5_active_gate', ROOT/'memo-os/week-5/runtime/production_gate.py')
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)

class CurrentSourceGate(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.canon = self.root/'canon/characters'
        self.canon.mkdir(parents=True)
        self.week = self.root/'memo-os/week-5'
        (self.week/'production-evidence').mkdir(parents=True)
        self.sha = 'a'*64
        self.write(self.canon/'reference_sources_v1.json', {'entries':[{'character_id':'CHAR-A', 'expected_sha256':self.sha, 'approval_state':'APPROVED'}]})
        self.write(self.canon/'VISUAL_REFERENCE_AUTHORITY_V1.json', {})
        self.write(self.week/'PUBLICATION_PAGE_MANIFEST.json', {'pages':[{'page_id':'P001', 'render_eligible':True}]})
        self.write(self.week/'production-evidence/WEEK_5_CHARACTER_AND_TITLE_RENDER_GATES_2026-10-13.json', {'pages':[{'page_id':'P001', 'display_header':'Fixture', 'owner_reference_requirements':[{'character_id':'CHAR-A', 'raw_sha256':self.sha}]}]})
        self.evidence = {'page_id':'P001','visible_primary_header':'Fixture','renderer_capability_state':'CAPABILITY_VERIFIED','references':[{'character_id':'CHAR-A','source_sha256':self.sha,'mounted_sha256':self.sha,'mount_receipt_id':'m','generation_reference_id':'g','subject_binding_id':'s'}], 'trusted_eligibility_state':'GENERATION_ELIGIBLE','eligibility_token_validated_by_adapter':True}
    def write(self, path, data): path.write_text(json.dumps(data))
    def check(self): return gate.check('P001', self.evidence, self.root)
    def test_current_approved_contract_remains_usable_for_preflight(self):
        self.assertEqual(self.check()['state'], 'PREFLIGHT_EVIDENCE_ACCEPTED')
    def test_historical_hash_does_not_override_current_source(self):
        self.write(self.canon/'reference_sources_v1.json', {'entries':[{'character_id':'CHAR-A','expected_sha256':'b'*64,'approval_state':'APPROVED'}]})
        self.assertEqual(self.check()['reason'], 'ACTIVE_SOURCE_CONTRACT_MISMATCH')
    def test_semantic_conflict_blocks_even_matching_approved_hash(self):
        self.write(self.canon/'VISUAL_REFERENCE_AUTHORITY_V1.json', {'source_visual_conflicts':[{'character_id':'CHAR-A','affected_expected_sha256':self.sha,'state':'ACTIVE_CANON_VISUAL_CONFLICT_HOLD'}]})
        self.assertEqual(self.check()['reason'], 'ACTIVE_SOURCE_CONTRACT_MISMATCH')
    def test_missing_current_authority_blocks(self):
        (self.canon/'reference_sources_v1.json').unlink()
        self.assertEqual(self.check()['reason'], 'ACTIVE_SOURCE_CONTRACT_MISMATCH')
    def test_unapproved_current_source_blocks(self):
        self.write(self.canon/'reference_sources_v1.json', {'entries':[{'character_id':'CHAR-A','expected_sha256':self.sha,'approval_state':'CANDIDATE'}]})
        self.assertEqual(self.check()['reason'], 'ACTIVE_SOURCE_CONTRACT_MISMATCH')
