import hashlib
import json
import unittest
from pathlib import Path
from validate_preview_schedule import ROOT, check

SOURCE='memo-os/week-9/WEEK_8_FINAL_WEEK_9_PROVIDER_EVIDENCE_2026-11-06.json'
DATA=json.loads((ROOT/SOURCE).read_text())
ROWS=[{'home':x['home']['teamName'], 'away':x['away']['teamName']} for x in DATA['week9_matchups']['matchups']]

def candidate():
    return {'week':8,'season':2026,'publication_state':'RELEASED','preview_week':9,
            'preview_schedule_source':SOURCE,'preview_schedule_source_sha256':hashlib.sha256((ROOT/SOURCE).read_bytes()).hexdigest(),
            'preview_fixture_rows':ROWS,'published_artifact_sha256':'a'*64,'generation_operator_id':'generator',
            'preview_final_raster_review':{'decision':'PASS','reviewer_id':'reviewer','reviewed_at':'2026-11-06T19:00:00Z',
            'pdf_sha256':'a'*64,'fixture_rows_sha256':hashlib.sha256(json.dumps(ROWS,sort_keys=True,ensure_ascii=False,separators=(',', ':')).encode()).hexdigest()}}

class ScheduleGate(unittest.TestCase):
    def test_correct_schedule(self): self.assertEqual(check(candidate()),[])
    def test_recycled_week8_schedule(self):
        x=candidate();x['preview_fixture_rows'][0]={'home':'Mud Dogs','away':'Dr. Duckhook'}
        self.assertTrue(any('do not match' in e for e in check(x)))
    def test_fictional_team(self):
        x=candidate();x['preview_fixture_rows'][0]={'home':'The Place We Once Knew','away':'The Commonwealth'}
        self.assertTrue(check(x))
    def test_missing_rows(self):
        x=candidate();x.pop('preview_fixture_rows');self.assertTrue(check(x))
    def test_wrong_source_hash(self):
        x=candidate();x['preview_schedule_source_sha256']='0'*64;self.assertTrue(check(x))
    def test_wrong_week(self):
        x=candidate();x['preview_week']=10;self.assertTrue(check(x))
    def test_missing_raster_review(self):
        x=candidate();x['preview_final_raster_review']['decision']='HOLD';self.assertTrue(check(x))
    def test_stale_pdf_review(self):
        x=candidate();x['preview_final_raster_review']['pdf_sha256']='b'*64;self.assertTrue(check(x))
    def test_stale_fixture_review(self):
        x=candidate();x['preview_final_raster_review']['fixture_rows_sha256']='b'*64;self.assertTrue(check(x))
    def test_self_review(self):
        x=candidate();x['preview_final_raster_review']['reviewer_id']='generator';self.assertTrue(check(x))
    def test_draft_not_release(self):
        x=candidate();x['publication_state']='REVIEW';self.assertEqual(check(x),[])

if __name__=='__main__': unittest.main()
