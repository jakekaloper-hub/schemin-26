"""Reader/commission identity and source-selection tests, not image approval."""
from pathlib import Path
import copy, hashlib, importlib.util, json, tempfile, unittest
ROOT=Path(__file__).resolve().parents[2]; W=ROOT/'memo-os/week-9'
REG='WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json'
APR='WEEK_9_FINAL_APPROVAL_FOLIOS_2026-11-10.json'

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class FullNameClearanceTests(unittest.TestCase):
    def naming(self):
        p=W/'approval_naming.py';self.assertTrue(p.is_file(),'No current full-name compiler')
        return module(p,'approval_naming_test')
    def load(self):return json.loads((W/APR).read_text())
    def test_names_expand_without_double_expansion_or_geography_changes(self):
        m=self.naming();s="Duckhook and ObiWan. HMB vs Chili; DK vs the LLC. Slob vs TDS. Red vs Chins."
        out=m.full_names(s)
        for name in ['Dr. Duckhook','ObiWan Jacoby',"His Majesty's Blood",'The Chili Cheesers','D0nkey K0ng','The LLC','Slob on my Dobb','Three Dreaded Snake','Red Leopards','Seven Deadly Chins']:self.assertIn(name,out)
        self.assertEqual(out,m.full_names(out))
        self.assertEqual(m.full_names('Chili Stable, Red Leopard Ruins; chili spills.'),'Chili Stable, Red Leopard Ruins; chili spills.')
        self.assertEqual(m.full_names('The LLC and D0nkey K0ng'),'The LLC and D0nkey K0ng')
    def test_material_colors_and_card_title_are_not_character_aliases(self):
        m=self.naming();self.assertEqual(m.full_names('Red sauce. The Red Card. Red retained the lead.'),'Red sauce. The Red Card. Red Leopards retained the lead.')

    def test_every_folio_has_explicit_character_name_id_and_authority(self):
        a=self.load();self.assertIn('full_name_clearance',a)
        for f in a['folios']:
            self.assertEqual({x['character_id'] for x in f['character_identity']},set(f['cast']))
            for c in f['character_identity']:
                self.assertTrue(c['full_name']);p=ROOT/c['appearance_source'];self.assertTrue(p.is_file())
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),c['appearance_sha256'])
                self.assertFalse(c['identity_reapproval_required'])
    def test_current_text_has_no_unexpanded_character_aliases(self):
        m=self.naming();a=self.load()
        for f in a['folios']:
            self.assertEqual(m.unresolved_aliases(f['copy']),[],f['page_id'])
            for field in ['scene','report_cards','final_visual_direction','sports_note','performance_edit','cover_teasers']:
                self.assertEqual(m.unresolved_aliases(f.get(field)),[],(f['page_id'],field))
    def test_six_finales_preserve_story_after_name_expansion(self):
        m=self.naming();issue=json.loads((W/REG).read_text());ps={p['page_id']:p for p in issue['pages']}
        for f in self.load()['folios']:
            if f['is_finale']:
                original=ps[f['page_id']]['editorial_copy']['conditional_narratives'][f['selected_branch']]
                self.assertEqual(f['copy']['body'],m.full_names(original))
                self.assertTrue(f['selected_ending_source_sha256'])
    def test_only_selected_finale_storyboard_branch_reaches_the_commission(self):
        for f in self.load()['folios']:
            if f['is_finale']:
                self.assertTrue(all(b['branch'] in ['COMMON',f['selected_branch'].upper()] for b in f['scene']['beats']),f['page_id'])
                self.assertTrue(f['archived_opposite_beat_ids'])

    def test_reporting_scope_and_overture_copy_are_not_ambiguous(self):
        fs={f['page_id']:f for f in self.load()['folios']}
        self.assertIn('Scoring-Form',fs['W09-P25']['copy']['headline'])
        self.assertIn('Reserve',fs['W09-P37']['copy']['headline'])
        self.assertFalse(fs['W09-P37']['official_injury_news_verified'])
        self.assertEqual(len(fs['W09-P37']['data_rows']),17)
        for f in fs.values():
            if f['page_role']=='two_character_pov_overture':
                self.assertEqual(f['publication_text_policy']['body'],'POV_HALVES_ONLY_NO_DUPLICATE_JOINED_BODY')
    def test_approval_kit_uses_current_full_names_and_rejects_stale_folio(self):
        self.naming();prep=module(W/'prepare_production_inputs.py','prep_clearance_test');issue=json.loads((W/REG).read_text())
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'review';d=prep.export_page_kit(ROOT,issue,'W09-P05',out,edition='approval-review')
            self.assertEqual(d['copy_selector'],'approval_folio.copy');self.assertFalse(d['render_authorized'])
            text=(out/'COPY.txt').read_text();f=next(p['approval_folio'] for p in issue['pages'] if p['page_id']=='W09-P05')
            self.assertIn(f['copy']['body'],text);self.assertIn('Dr. Duckhook',text);self.assertIn('ObiWan Jacoby',text)
            self.assertIn('Dr. Duckhook',(out/'COMMISSION.md').read_text());self.assertEqual(len(d['reference_files']),2)
            changed=copy.deepcopy(issue);p=next(p for p in changed['pages'] if p['page_id']=='W09-P05');p['approval_folio']['copy']['body']='Unreviewed replacement.'
            with self.assertRaises(ValueError):prep.export_page_kit(ROOT,changed,'W09-P05',Path(td)/'bad',edition='approval-review')
            self.assertFalse((Path(td)/'bad').exists())
    def test_neutral_and_approval_inputs_remain_distinct(self):
        self.naming();prep=module(W/'prepare_production_inputs.py','prep_neutral_test');issue=json.loads((W/REG).read_text())
        with tempfile.TemporaryDirectory() as td:
            d=prep.export_page_kit(ROOT,issue,'W09-P05',Path(td)/'neutral')
            self.assertFalse(d['actual_result_selected']);self.assertFalse(d['contains_final_scores'])
    def test_readable_review_and_all_authorization_holds_exist(self):
        a=self.load();self.assertIn('review_digest',a['full_name_clearance'])
        for k in ['founder_approved','independent_source_acceptance','render_authorized','release_approved']:self.assertFalse(a['approval'][k])
        text=(W/'WEEK_9_FINAL_APPROVAL_FOLIOS_2026-11-10.md').read_text()
        self.assertNotIn('**Home POV:**',text);self.assertIn('Home perspective',text)
        self.assertTrue((W/'production-evidence/clearance-2026-11-10/APPROVAL_SUMMARY.md').is_file())

if __name__=='__main__':unittest.main()
