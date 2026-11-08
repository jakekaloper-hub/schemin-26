"""Existing character authority must reach actual Week9 packets; not pixel certification."""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[2]
WEEK = ROOT / 'memo-os/week-9'
ISSUE = 'WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json'
LINEUP = 'canon/characters/APPROVED_LINEUP_2026_10_18.json'
CHILI = 'CHAR-BRANDON-PRYOR'
NINO = 'CHAR-MANNING-WELTY'
MUD = 'CHAR-BOBBY-MITCHELL'

class Week9CharacterApplicationTests(unittest.TestCase):
    def setUp(self):
        self.issue = json.loads((WEEK / ISSUE).read_text())
        self.lineup = json.loads((ROOT / LINEUP).read_text())

    def test_all_twelve_current_appearance_sources_are_resolved(self):
        self.assertIn('resolved_character_appearances', self.issue)
        resolved = self.issue['resolved_character_appearances']
        self.assertEqual(set(resolved), {x['character_id'] for x in self.lineup['individuals']})
        for cid, value in resolved.items():
            source = ROOT / value['appearance_authority_path']
            self.assertTrue(source.is_file(), cid)
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), value['appearance_authority_sha256'])
            self.assertFalse(value['identity_reapproval_required'])
            self.assertFalse(value['renderer_binding_proven'])
            self.assertTrue(value['required_visible_identity'])

    def test_chili_latest_correction_overrides_older_lineup(self):
        resolved = self.issue.get('resolved_character_appearances', {})
        self.assertIn(CHILI, resolved)
        c = resolved[CHILI]
        self.assertTrue(c['appearance_authority_path'].endswith('COMMISSIONER_APPEARANCE_LOCK_2026_10_22.json'))
        self.assertEqual(c['approval_date'], '2026-10-22')
        self.assertFalse(c['preferred_visual_binary_verified'])
        self.assertIn('sunglasses', json.dumps(c).lower())
        for page in self.issue['pages']:
            if CHILI not in page['characters_present']:
                continue
            assets = [a for a in page['reference_assets'] if a['character_id'] == CHILI]
            self.assertEqual(len(assets), 1)
            self.assertEqual(assets[0]['appearance_authority_path'], c['appearance_authority_path'])
            self.assertFalse(assets[0]['older_crop_satisfies_latest_appearance'])

    def test_mud_nino_are_both_explicit_approved_subjects(self):
        pages = [p for p in self.issue['pages'] if p.get('matchup_id') == 'W09-M02']
        self.assertEqual(len(pages), 3)
        for page in pages:
            self.assertEqual(set(page['characters_present']), {MUD, NINO})
            self.assertEqual({a['character_id'] for a in page['reference_assets']}, {MUD, NINO})
            self.assertIn('four', json.dumps(page['scene_identity_application']).lower())
            self.assertIn('humanoid', json.dumps(page['scene_identity_application']).lower())

    def test_false_storm_identity_is_removed_from_active_directions(self):
        files = [ISSUE, 'WEEK_9_SPORTS_STORY_CARDS_2026-11-08.json', 'WEEK_9_SIX_MATCHUP_COMMISSIONER_PREVIS_CANDIDATES_2026-11-08.json', 'WEEK_9_COMMISSIONER_QUESTIONNAIRE_CREATIVE_CONTEXT_2026-11-08.md']
        for name in files:
            text = (WEEK / name).read_text()
            for invalid in ['No humanoid storm adversary appears.', 'El Niño is mobile weather, not humanoid speaking racer', "El Niño's identity is **the storm itself** rather than a person/rider."]:
                self.assertNotIn(invalid, text, name)

    def test_each_cinematic_page_has_exact_cast_not_all_issue_poster(self):
        pages = [p for p in self.issue['pages'] if p.get('matchup_id')]
        self.assertEqual(len(pages), 18)
        for page in pages:
            self.assertIn('page_character_contract', page)
            contract = page['page_character_contract']
            self.assertEqual(len(page['characters_present']), 2)
            self.assertEqual(set(contract['allowed_principal_character_ids']), set(page['characters_present']))
            self.assertEqual(contract['output_page_id'], page['page_id'])
            self.assertEqual(contract['maximum_output_pages'], 1)
            self.assertTrue(contract['reject_all_issue_status_poster'])
            self.assertFalse(page['render_authorized'])
            self.assertIsNone(page['actual_winner_team_id'])

    def test_no_scene_changes_to_identity_or_mistaken_new_approval(self):
        self.assertIn('resolved_character_appearances', self.issue)
        c = self.issue['resolved_character_appearances']
        self.assertIn('duck', json.dumps(c['CHAR-ZACH-WILSON']).lower())
        self.assertIn('four', json.dumps(c['CHAR-WILSON-LOOK']).lower())
        self.assertIn('three', json.dumps(c['CHAR-PHILLIP-PITTS']).lower())
        self.assertIn('red', json.dumps(c['CHAR-KEVIN-ZEEK']).lower())
        for cid in c:
            self.assertFalse(c[cid]['new_canon_approval'])
        ctx = json.loads((WEEK / 'THREAD_CONTINUITY.json').read_text())
        self.assertEqual(set(ctx['character_policy']['focused_exception_ids']), {'CHAR-AUSTIN-BYARS', 'CHAR-WILSON-LOOK'})
        self.assertFalse(ctx['character_policy']['repeat_questionnaire'])
        self.assertFalse(ctx['status']['polished_proofs_complete'])

    def test_correction_is_on_current_read_path_and_ci(self):
        self.assertIn('Current character application', (WEEK / '_INDEX.md').read_text())
        self.assertIn('test_week9_character_application.py', (ROOT / '.github/workflows/weekly-memo-authority-ci.yml').read_text())

if __name__ == '__main__':
    unittest.main()
