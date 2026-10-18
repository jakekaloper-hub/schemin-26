"""Seven original spotlight PNGs and DK candidate are real bytes, never auto-promoted."""
import json,hashlib,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
PROPOSAL=ROOT/"canon/characters/recovery/EXISTING_BYTES_VERSION_MIGRATION_REVIEW_2026_10_18.json"
SOURCE=ROOT/"canon/characters/reference_sources_v1.json"

class ExistingBytesMigrationReviewTests(unittest.TestCase):
    def test_exact_eight_candidate_bytes_and_previous_canon_untouched(self):
        d=json.loads(PROPOSAL.read_text())
        reg={x['character_id']:x for x in json.loads(SOURCE.read_text())['entries']}
        self.assertEqual(len(d['items']),8)
        self.assertEqual(d['supplementary_poster_candidates'],7)
        self.assertEqual(d['current_quadruped_dk_candidate'],1)
        self.assertEqual(len({x['character_id'] for x in d['items']}),8)
        for x in d['items']:
            a=reg[x['character_id']]
            path=ROOT/x['candidate_path']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),x['candidate_sha256'])
            self.assertEqual(path.stat().st_size,x['candidate_bytes'])
            self.assertEqual(x['historical_primary_sha256'],a['expected_sha256'])
            self.assertEqual(x['historical_primary_file_id'],a['conversation_file_id'])
            self.assertNotEqual(x['candidate_sha256'],a['expected_sha256'])
            self.assertFalse(x['new_primary_commissioner_approved'])
            self.assertFalse(x['current_primary_metadata_changed'])
            self.assertFalse(x['generation_production_eligible'])
            self.assertIsNone(x['proposed_new_primary_version'])

    def test_seven_oct12_spotlights_match_supplementary_receipts_only(self):
        doc=json.loads(PROPOSAL.read_text())
        for x in doc['items']:
            if x['character_id']=='CHAR-WILSON-LOOK':
                self.assertIn('/candidate/',x['candidate_path'])
                continue
            self.assertIn('/supplementary/',x['candidate_path'])
            receipt=json.loads((ROOT/f"canon/characters/{x['character_id']}/OWNER_SPOTLIGHT_2026_RECEIPT.json").read_text())
            self.assertEqual(receipt['user_upload_sha256'],x['candidate_sha256'])
            self.assertFalse(receipt['supersedes_primary_identity'])
            self.assertEqual(receipt['uploaded_rgba_pixel_sha256'],receipt['stored_rgba_pixel_sha256'])

    def test_proposal_can_never_be_read_as_release_or_source_supersession(self):
        doc=json.loads(PROPOSAL.read_text())
        self.assertEqual(doc['status'],'COMMISSIONER_VERSION_DECISION_REQUIRED__NO_AUTO_PROMOTION')
        self.assertFalse(doc['source_pixel_identity_proven_against_sept29_jpeg'])
        self.assertFalse(doc['historical_owner_stats_in_cards_authoritative_for_current_memo'])
