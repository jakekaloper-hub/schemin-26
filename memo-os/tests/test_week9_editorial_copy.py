"""Check written copy coverage; these tests do not accept images or final results."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
WEEK = ROOT / 'memo-os/week-9'
REGISTRY = WEEK / 'WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json'

def count_words(text):
    return len(re.findall(r"\S+", text))

class Week9EditorialCopyTests(unittest.TestCase):
    def pages(self):
        return json.loads(REGISTRY.read_text())['pages']

    def require_copy(self, page):
        self.assertIn('editorial_copy', page, page['page_id'] + ' has no page-specific copy')
        return page['editorial_copy']

    def test_all_existing_pages_have_labeled_copy(self):
        pages = self.pages()
        self.assertEqual(len(pages), 28)
        for p in pages:
            c = self.require_copy(p)
            self.assertEqual(c['state'], 'DRAFT_COPY_NOT_FINAL_PUBLICATION')
            self.assertTrue(c['body'].strip())
            self.assertTrue(c['source_paths'])
            self.assertFalse(c['approved_for_release'])

    def test_eighteen_cinematic_pages_and_twelve_separate_endings(self):
        pages = [p for p in self.pages() if p.get('matchup_id')]
        self.assertEqual(len(pages), 18)
        finales = [p for p in pages if p['page_role'] == 'matchup_payoff']
        self.assertEqual(len(finales), 6)
        for p in finales:
            c = self.require_copy(p)
            self.assertEqual(set(c['conditional_narratives']), {'home_win','away_win'})
            self.assertIsNone(c['selected_branch'])
            self.assertIsNone(p['actual_winner_team_id'])
            for text in c['conditional_narratives'].values():
                self.assertGreater(count_words(text), 40)

    def test_narrative_fits_existing_budgets(self):
        for p in self.pages():
            c = self.require_copy(p)
            for text in [c['body'], *c.get('conditional_narratives',{}).values()]:
                self.assertLessEqual(count_words(text), p['copy_budget']['body_words_max'], p['page_id'])
            self.assertLessEqual(count_words(c['headline']), p['copy_budget']['headline_words_max'])

    def test_pending_departments_not_fabricated(self):
        pages = {p['page_id']:p for p in self.pages()}
        ranks = self.require_copy(pages['W09-P25'])
        book = self.require_copy(pages['W09-P27'])
        self.assertEqual(ranks['source_status'],'FINAL_RANKING_NOT_SUPPLIED')
        self.assertEqual(ranks['data_rows'],[])
        self.assertEqual(book['source_status'],'COMMISSIONER_CONFIRMED_WEEK9_CLOSED')
        self.assertEqual(pages['W09-P27']['book_operating_state'],'CLOSED_WEEK9_FOUNDER_CONFIRMED')
        self.assertEqual(book['settled_wagers'],[])

    def test_sports_and_fiction_remain_separate(self):
        for p in self.pages():
            c = self.require_copy(p)
            self.assertFalse(p['render_authorized'])
            self.assertIsNone(p['actual_winner_team_id'])
            if p.get('matchup_id'):
                self.assertEqual(c['body_classification'],'FICTIONAL_SCENE_NARRATION')
                self.assertEqual(c['sports_inset']['classification'],'PRE_MNF_OBSERVED_NOT_FINAL')
                self.assertIn('2026-11-09',c['sports_inset']['as_of'])

    def test_readable_proof_and_entrypoint_exist(self):
        proof = WEEK/'WEEK_9_EDITORIAL_COPY_PROOF_2026-11-09.html'
        self.assertTrue(proof.is_file())
        text=proof.read_text()
        self.assertEqual(text.count('data-folio='),28)
        self.assertEqual(text.count('data-ending='),12)
        self.assertIn('READING PROOF — NOT THE ILLUSTRATED MEMO',text)
        self.assertIn(proof.name,(WEEK/'_INDEX.md').read_text())
        ci=(ROOT/'.github/workflows/weekly-memo-authority-ci.yml').read_text()
        self.assertIn('test_week9_editorial_copy.py',ci)

if __name__=='__main__':
    unittest.main()
