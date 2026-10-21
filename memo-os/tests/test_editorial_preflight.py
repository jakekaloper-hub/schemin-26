import importlib.util
import unittest
from pathlib import Path

file=Path(__file__).resolve().parents[1]/"tools"/"validate_editorial_preflight.py"
spec=importlib.util.spec_from_file_location("editorial_preflight",file)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
STAMP="2026-10-21T12:00:00-04:00"
CLAIM={"claim_id":"W7-1","kind":"WAIVER_CLAIM","source_provider":"ESPN via FLAIM",
"source_reference":"fixture:w7-1","source_sha256":"a"*64,"event_at":STAMP,
"retrieved_at":STAMP,"transaction_status":"COMPLETED","text":"Completed waiver claim (synthetic fixture)"}
STORY={"status":"EDITORIAL_LOCKED","matchup_id":"week-6-duckhook-el-nino",
"home_team_id":"duckhook","away_team_id":"el-nino","location_id":"LOC-COUNTRY-CLUB-JACKSON",
"premise":"Country club against weather","setup":"Elegant clubhouse","escalation":"Storm arrives",
"payoff":"Duckhook wins","camera_axis":"veranda to green","environment_continuity":"clubhouse and green",
"manuscript_sha256":"a"*64,"location_authority":"ESTABLISHED","result_status":"FINAL",
"character_reference_status":"VERIFIED"}

class SportsPreflight(unittest.TestCase):
    def good(self):return {"editorial_cutoff":STAMP,"claims":[dict(CLAIM)]}
    def test_valid_claim_metadata(self):self.assertEqual([],m.validate_sports(self.good()))
    def test_pending_waiver_fails(self):
        x=self.good();x["claims"][0]["transaction_status"]="PENDING"
        self.assertIn("transaction not completed",str(m.validate_sports(x)))
    def test_after_cutoff_fails(self):
        x=self.good();x["claims"][0]["retrieved_at"]="2026-10-22T12:00:00-04:00"
        self.assertIn("after editorial cutoff",str(m.validate_sports(x)))
    def test_missing_provenance_fails(self):
        x=self.good();x["claims"][0]["source_sha256"]=""
        self.assertIn("missing source SHA256",str(m.validate_sports(x)))
    def test_bench_result_requires_eligibility(self):
        x=self.good();x["claims"][0].update(kind="BENCH_COMPARISON",lineup_placement="BENCH",changes_result=True,eligibility_verified=False)
        self.assertIn("requires eligibility",str(m.validate_sports(x)))
    def test_medical_news_requires_contemporary_source(self):
        x=self.good();x["claims"][0].update(kind="NFL_NEWS",medical_claim=True,news_verification="UNKNOWN")
        self.assertIn("contemporary source",str(m.validate_sports(x)))
    def test_duplicate_id_fails(self):
        x=self.good();x["claims"].append(dict(x["claims"][0]))
        self.assertIn("duplicate claim ID",str(m.validate_sports(x)))

class StoryPreflight(unittest.TestCase):
    def test_valid_contract(self):self.assertEqual([],m.validate_story(STORY))
    def test_character_pipeline_hold(self):
        x=dict(STORY,character_reference_status="UNVERIFIED")
        self.assertIn("BLOCKED_BY_CHARACTER_REFERENCE_PIPELINE",m.validate_story(x))
    def test_no_invented_result(self):
        x=dict(STORY,result_status="UNDECIDED")
        self.assertIn("story factual result not final",m.validate_story(x))
    def test_missing_camera(self):
        x=dict(STORY,camera_axis="")
        self.assertIn("story missing camera_axis",m.validate_story(x))
class AtlasPreflight(unittest.TestCase):
    def packet(self):
        return {"location_id":"LOC-COMMONWEALTH-PRESS-GALLERY-CANDIDATE",
                "physical_zone":"Central River Basin",
                "camera_viewpoint":"35mm three-quarter",
                "environment_notes":"stone and dark walnut press gallery",
                "location_authority":"CANDIDATE",
                "permanent_canon_claim":False}
    def test_candidate_remains_candidate(self):
        self.assertEqual([],m.validate_atlas(self.packet()))
    def test_cannot_self_promote_candidate(self):
        x=self.packet();x["permanent_canon_claim"]=True
        self.assertIn("cannot self-promote",str(m.validate_atlas(x)))
    def test_rejects_unsupported_spatial_certification(self):
        x=self.packet();x["spatial_verification"]="VERIFIED"
        self.assertIn("requires independent spatial evidence",str(m.validate_atlas(x)))
    def test_rejects_invented_route_distance(self):
        x=self.packet();x["route_distance"]=13.4
        self.assertIn("unsupported precise route distance",str(m.validate_atlas(x)))

if __name__=="__main__":unittest.main()
