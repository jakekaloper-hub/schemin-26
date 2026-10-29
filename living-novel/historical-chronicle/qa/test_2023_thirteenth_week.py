"""NONCANON 2023 Week 13: source, six scenes, chronology, protected text and draft-only guards.
These checks are technical self-tests, not independent editorial, Atlas or Umpire acceptance.
"""
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import re
import unittest

ROOT=Path(__file__).resolve().parents[3]
ARCHIVE=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
STORY=ROOT/"living-novel/historical-chronicle/seasons/2023/weeks/W13.md"
PREVIOUS=ROOT/"living-novel/historical-chronicle/seasons/2023/weeks/W12.md"
CONT=ROOT/"living-novel/historical-chronicle/seasons/2023/CONTINUITY.json"
SOURCE_SHA="ded119cde5c660f87f197f269b8d6ddd2a11316a"
PREVIOUS_SHA="4b2d1c9b4abb08f043d8ff9aecf56c0ab82ce418"
PROTECTED={
 "PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
 "CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def blob(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\\0"+data).hexdigest()
def fmt(n):
    return f"{Decimal(str(n)):.2f}"

class Test2023ThirteenthWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive=json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.story=STORY.read_text(encoding="utf-8")
        cls.cont=json.loads(CONT.read_text(encoding="utf-8"))
        cls.rows=next(w["matchups"] for w in cls.archive["weeks"] if w["week"]==13)
        cls.headers=re.findall(r"(?m)^## ([IVX]+)\\. ([^\\n]+)$",cls.story)
        cls.scenes=re.split(r"(?m)^## [IVX]+\\. [^\\n]+\\n",cls.story)[1:]

    def test_pinned_source_and_known_limit(self):
        self.assertEqual(blob(ARCHIVE),SOURCE_SHA)
        self.assertEqual(self.archive["source"],"Flaim ESPN 1417621")
        self.assertIn("Raw ESPN SHA unavailable",self.archive["limits"])
        self.assertIn("historical owner assignments",self.story)

    def test_six_distinct_matchups_cover_twelve_slots(self):
        self.assertEqual(len(self.rows),6)
        self.assertEqual(sorted(i for r in self.rows for i in (r["home_id"],r["away_id"])),list(range(1,13)))

    def test_actual_winners_and_margins(self):
        self.assertEqual([(r["home_id"] if r["winner"]=="HOME" else r["away_id"]) for r in self.rows],[2,9,10,4,1,12])
        self.assertEqual([fmt(abs(Decimal(str(r["hp"]))-Decimal(str(r["ap"])))) for r in self.rows],
                         ["7.68","6.02","59.66","40.84","1.04","14.12"])

    def test_six_source_exact_story_anchors_in_source_order(self):
        self.assertEqual([h[0] for h in self.headers],["I","II","III","IV","V","VI"])
        self.assertEqual(len(self.scenes),6)
        for i,(r,scene) in enumerate(zip(self.rows,self.scenes),1):
            with self.subTest(scene=i):
                self.assertIn(f'{r["home"].strip()} (home), {fmt(r["hp"])}',scene)
                self.assertIn(f'{r["away"].strip()} (away), {fmt(r["ap"])}',scene)
                win=r["winner"]=="HOME"
                name=(r["home"] if win else r["away"]).strip()
                slot=r["home_id"] if win else r["away_id"]
                self.assertIn(f'Winner: **{name} (slot {slot})**',scene)
                self.assertIn(f'Margin **{abs(Decimal(str(r["hp"]))-Decimal(str(r["ap"]))):.2f}**',scene)

    def test_substantial_six_scene_prose(self):
        self.assertGreaterEqual(len(self.story.split()),5000)
        for i,scene in enumerate(self.scenes[:5],1):
            with self.subTest(scene=i):
                self.assertGreaterEqual(len(scene.split()),520)
                self.assertGreaterEqual(scene.count("\\n\\n"),8)
        self.assertIn("### After the Thirteenth Reckoning",self.scenes[-1])

    def test_slot_one_winning_record_not_human_owner_claim(self):
        slot_1=[]
        for week in self.archive["weeks"][:13]:
            row=next(r for r in week["matchups"] if 1 in (r["home_id"],r["away_id"]))
            slot_1.append((row["home_id"] if row["winner"]=="HOME" else row["away_id"])==1)
        self.assertEqual(sum(slot_1),5)
        self.assertEqual(len(slot_1)-sum(slot_1),8)
        self.assertIn("5–8",self.story)
        self.assertIn("user-attested, not provider-authenticated",self.story)

    def test_timeline_rejects_later_competitive_rows(self):
        future=next(w["matchups"] for w in self.archive["weeks"] if w["week"]==14)
        for r in future:
            self.assertNotIn(f'{r["home"].strip()} (home), {fmt(r["hp"])}',self.story)
            self.assertNotIn(f'{r["away"].strip()} (away), {fmt(r["ap"])}',self.story)
        self.assertIn("No Week 14 or postseason result is known",self.story)

    def test_pov_and_no_personified_storm(self):
        self.assertEqual(self.cont["principal_pov_ids"],["CHAR-JAKE-KALOPER"])
        self.assertEqual(self.cont["other_owner_povs"],"NONE")
        self.assertNotRegex(self.story,r"\\b(?:Edrin|Edin|Master Oren)\\b")
        self.assertNotRegex(self.story,r"(?i)El Niño\\s+(?:said|spoke|walked|thought|asked|smiled|decided)")

    def test_disclaimers_and_geography_firewalls(self):
        for phrase in ["NONCANON","PROPOSED FICTION / HISTORICAL ATLAS HOLD",
                       "home/away is archival ordering, not geographic proof",
                       "four similarly named Benedict banners",
                       "El Niño is a competitor banner",
                       "UNKNOWN","no independent Author Council"]:
            self.assertIn(phrase.lower(),self.story.lower())

    def test_river_and_shelter_obligations_unresolved(self):
        for phrase in ["proper ferry","punt grounded","no safe operating hearth",
                       "far-bank consent","workers' compensation","unresolved"]:
            self.assertIn(phrase.lower(),self.story.lower())

    def test_prior_week_and_protected_hard_canon_byte_identity(self):
        self.assertEqual(blob(PREVIOUS),PREVIOUS_SHA)
        for n,sha in PROTECTED.items():
            with self.subTest(protected=n):
                self.assertEqual(blob(ROOT/"living-novel/manuscript"/n),sha)

    def test_continuity_exactly_78_noncanonical_fixtures(self):
        c=self.cont
        self.assertEqual(c["phase"],"WEEK_01_13_DRAFT_NONCANON")
        self.assertEqual(c["story_time_cutoff"],"after scoring week 13 only")
        m=c["matchup_coverage"]
        self.assertEqual(m["scoring_weeks_complete"],list(range(1,14)))
        self.assertEqual(m["verified_matchups"],78)
        self.assertEqual(m["prose_entries"],78)
        self.assertEqual(m["regular_season_matchups_covered"],78)
        self.assertEqual(m["regular_season_matchups_total"],84)
        self.assertTrue(m["week13_complete"])
        self.assertEqual(m["postseason"],"NOT_DRAFTED")
        self.assertEqual(c["drafts"]["thirteenth_week"],str(STORY.relative_to(ROOT)))

    def test_no_promotion_or_invented_provider_verification(self):
        c=self.cont
        self.assertEqual(c["source"]["blob_sha"],SOURCE_SHA)
        self.assertEqual(c["source"]["raw_provider_sha"],"UNKNOWN")
        self.assertEqual(c["source"]["owner_identity"],"UNVERIFIED")
        self.assertEqual(c["historical_transactions_asserted"],0)
        self.assertEqual(c["world_atlas_status"],"UNAPPROVED_PROPOSED_STAGING")
        self.assertIn("DRAFT_UNREVIEWED",c["literary_status"])
        self.assertEqual(c["ci_week13"]["independent_umpire"],"NOT_OBTAINED")
        self.assertEqual(c["ci_week13"]["status"],"PENDING_ACTUAL_CI_READBACK")

if __name__=="__main__":
    unittest.main()
