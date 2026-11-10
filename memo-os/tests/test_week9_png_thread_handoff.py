"""Verify repository portability, not permission, generated pixels, or publication."""
from pathlib import Path
import hashlib
import importlib.util
import json
import unittest

ROOT=Path(__file__).resolve().parents[2]
WEEK=ROOT/'memo-os/week-9'
NEW=WEEK/'Week_9_Approval_Review_Full_Names.json'
OLD=WEEK/'WEEK_9_FINAL_APPROVAL_FOLIOS_2026-11-10.json'

class PNGThreadHandoffTests(unittest.TestCase):
    def load(self):
        self.assertTrue(NEW.is_file(),'Latest local-only revision has not been synced')
        return json.loads(NEW.read_text())

    def test_current_read_path_resolves_one_png_entrypoint(self):
        f=WEEK/'PNG_PRODUCTION_START_HERE.md'
        self.assertTrue(f.is_file())
        self.assertIn('PNG_PRODUCTION_START_HERE.md',(WEEK/'_INDEX.md').read_text())
        self.assertIn('PNG_PRODUCTION_START_HERE.md',(WEEK/'THREAD_CONTINUITY.md').read_text())
        self.assertIn('Week_9_Approval_Review_Full_Names.json',f.read_text())
        self.assertIn('PDF',f.read_text())

    def test_exact_approved_revision_and_existing_35_positions_survive(self):
        a=self.load();old=json.loads(OLD.read_text())
        self.assertEqual(len(a['folios']),35)
        self.assertEqual([f['page_id'] for f in a['folios']],[f['page_id'] for f in old['folios']])
        for prev,now in zip(old['folios'],a['folios']):
            for key in ['cast','references','data_rows','selected_branch']:
                self.assertEqual(prev[key],now[key],(now['page_id'],key))
        archived=WEEK/'production-evidence/png-handoff-2026-11-10/source-review/clearance/Week_9_Approval_Review_Full_Names.json'
        self.assertEqual(hashlib.sha256(archived.read_bytes()).hexdigest(),'e65b199a5fd5a321177f61b7e1a62f3957b4c6c08fde0d6fef1bda9c258e8b72')
        self.assertEqual(a['folios'],json.loads(archived.read_text())['folios'])
        self.assertTrue(a['clearance']['repository_synced'])

    def test_current_register_uses_revision_while_history_survives(self):
        a=self.load();old=json.loads(OLD.read_text());j=json.loads((WEEK/'WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json').read_text());by={p['page_id']:p for p in j['pages']}
        for before,f in zip(old['folios'],a['folios']):
            self.assertEqual(by[f['page_id']]['approval_folio'],f)
            self.assertEqual(by[f['page_id']]['approval_folio_before_full_names'],before)
        self.assertEqual(j['current_approval_review']['copy_selector'],'pages[page_id].approval_folio.publication_payload')

    def test_full_names_and_selected_scene_only(self):
        a=self.load();script=WEEK/'production-evidence/png-handoff-2026-11-10/source-review/clearance/prepare_clearance.py'
        spec=importlib.util.spec_from_file_location('names_review',script);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        for f in a['folios']:
            self.assertEqual(m.find_aliases(f['publication_payload']),[],f['page_id'])
            self.assertEqual(m.find_aliases(f['scene']),[],f['page_id'])
            if f['is_finale']:
                self.assertTrue(all(b.get('branch') in ['COMMON',f['selected_branch'].upper()] for b in f['scene']['beats']))
                self.assertEqual(len(f['archived_unselected_beats']),1)

    def test_orders_and_source_digest_are_current(self):
        self.load();jfile=WEEK/'WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json';j=json.loads(jfile.read_text());order=json.loads((WEEK/'WEEK_9_READING_AND_PRODUCTION_ORDER_2026-11-09.json').read_text())
        self.assertEqual(order['source_register_sha256'],hashlib.sha256(jfile.read_bytes()).hexdigest())
        self.assertEqual(order['reading_order'],j['reading_order'])
        self.assertEqual(order['production_queue'],j['production_queue'])
        self.assertEqual([q['page_id'] for q in order['production_queue'][:2]],['W09-P05','W09-P20'])

    def test_first_two_scoped_commissions_are_current_not_finales(self):
        self.load();by={f['page_id']:f for f in self.load()['folios']}
        for pid in ['W09-P05','W09-P20']:
            p=WEEK/'png-production'/pid
            self.assertTrue((p/'COMMISSION.md').is_file())
            f=json.loads((p/'FOLIO.json').read_text());self.assertEqual(f,by[pid]);self.assertFalse(f['is_finale'])
            m=json.loads((p/'manifest.json').read_text());self.assertFalse(m['renderer_binding_proven']);self.assertFalse(m['artwork_generated'])
            for asset in m['reference_files']:
                self.assertEqual(hashlib.sha256((p/asset['file']).read_bytes()).hexdigest(),asset['sha256'])
            self.assertEqual(json.loads((p/'layout.json').read_text()),f['layout'])

    def test_no_imaginary_source_or_output_approval(self):
        a=self.load()
        for k in ['independent_source_acceptance','release_approved','render_authorized']:
            self.assertFalse(a['approval'][k])
        for f in a['folios']:
            self.assertFalse(f['render_authorized']);self.assertFalse(f['publication_approved'])
        h=json.loads((WEEK/'PNG_THREAD_HANDOFF.json').read_text())
        self.assertTrue(h['user_requested_png_transition']);self.assertFalse(h['source_acceptance_completed']);self.assertFalse(h['accepted_scene_images_exist'])
        self.assertEqual(h['pdf_role'],'COMPILE_APPROVED_PNGS_ONLY_AT_END')
        self.assertEqual(h['page_count'],35)

    def test_registered_images_and_all_appearance_authorities_are_preserved(self):
        self.load()
        j=json.loads((WEEK/'WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json').read_text())
        sources=j['resolved_character_appearances'];self.assertEqual(len(sources),12)
        checked=0
        for cid,r in sources.items():
            self.assertFalse(r['identity_reapproval_required'])
            auth=ROOT/r['appearance_authority_path'];self.assertTrue(auth.is_file(),cid)
            self.assertEqual(hashlib.sha256(auth.read_bytes()).hexdigest(),r['appearance_authority_sha256'])
            if r.get('approved_visual_path'):
                image=ROOT/r['approved_visual_path'];self.assertTrue(image.is_file(),cid)
                self.assertEqual(hashlib.sha256(image.read_bytes()).hexdigest(),r['approved_visual_sha256'])
                checked+=1
            else:
                self.assertEqual(cid,'CHAR-BRANDON-PRYOR')
                # The later Chili appearance is authoritative; an older crop is not silently promoted.
                self.assertIn('Chili latest appearance correction',json.dumps(json.loads((WEEK/'PNG_THREAD_HANDOFF.json').read_text())))
        self.assertEqual(checked,11)

if __name__=='__main__':unittest.main()
