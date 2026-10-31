"""2023 Week 14 NONCANON Chronicle: archival, substantive fiction, source-time and protected canon tests.
Passing this technical suite does not constitute independent author/Atlas/Umpire review.
"""
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import re
import unittest

ROOT=Path(__file__).resolve().parents[3]
ARCHIVE=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
STORY=ROOT/"living-novel/historical-chronicle/seasons/2023/weeks/W14.md"
PREVIOUS=ROOT/"living-novel/historical-chronicle/seasons/2023/weeks/W13.md"
CONT=ROOT/"living-novel/historical-chronicle/seasons/2023/CONTINUITY.json"
SOURCE_SHA="ded119cde5c660f87f197f269b8d6ddd2a11316a"
PREVIOUS_SHA="819d069735c2f1f72effcd92bc8049fe87fde3df"
PROTECTED={
 "PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
 "CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def git_blob(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def scored(n):
    return f"{Decimal(str(n)):.2f}"

class Test2023FourteenthWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive=json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.rows=next(w["matchups"] for w in cls.archive["weeks"] if w["week"]==14)
        cls.story=STORY.read_text(encoding="utf-8")
        cls.cont=json.loads(CONT.read_text(encoding="utf-8"))
        cls.headers=re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$",cls.story)
        cls.scenes=re.split(r"(?m)^## [IVX]+\. [^\n]+\n",cls.story)[1:]

    def test_pinned_archive_and_upstream_limit(self):
        self.assertEqual(git_blob(ARCHIVE),SOURCE_SHA)
        self.assertEqual(self.archive["source"],"Flaim ESPN 1417621")
        self.assertIn("Raw ESPN SHA unavailable",self.archive["limits"])

    def test_six_disjoint_fixture_rows_and_twelve_slots(self):
        self.assertEqual(len(self.rows),6)
        self.assertEqual(sorted(v for row in self.rows for v in (row["home_id"],row["away_id"])),list(range(1,13)))

    def test_source_exact_winners_margins(self):
        self.assertEqual([r["home_id"] if r["winner"]=="HOME" else r["away_id"] for r in self.rows],[9,12,7,11,5,10])
        self.assertEqual([scored(abs(Decimal(str(r["hp"]))-Decimal(str(r["ap"])))) for r in self.rows],
                         ["26.86","4.68","40.40","28.92","26.46","39.67"])

    def test_six_story_scenes_match_source_in_order(self):
        self.assertEqual([h[0] for h in self.headers],["I","II","III","IV","V","VI"])
        self.assertEqual(len(self.scenes),6)
        for i,(row,scene) in enumerate(zip(self.rows,self.scenes),1):
            with self.subTest(scene=i):
                self.assertIn(f'{row["home"].strip()} (home), {scored(row["hp"])}',scene)
                self.assertIn(f'{row["away"].strip()} (away), {scored(row["ap"])}',scene)
                ishome=row["winner"]=="HOME"
                winner=(row["home"] if ishome else row["away"]).strip()
                slot=row["home_id"] if ishome else row["away_id"]
                self.assertIn(f"Winner: **{winner} (slot {slot})**",scene)
                self.assertIn(f'Margin **{abs(Decimal(str(row["hp"]))-Decimal(str(row["ap"]))):.2f}**',scene)

    def test_full_length_six_substantial_separate_scenes(self):
        self.assertGreaterEqual(len(self.story.split()),5000)
        for i,scene in enumerate(self.scenes[:5],1):
            with self.subTest(scene=i):
                self.assertGreaterEqual(len(scene.split()),580)
                self.assertGreaterEqual(scene.count("\n\n"),8)
        self.assertIn("### After the Fourteenth Reckoning",self.scenes[-1])

    def test_slot_one_final_regular_season_record_5_9(self):
        rows=[next(r for r in week["matchups"] if 1 in (r["home_id"],r["away_id"])) for week in self.archive["weeks"][:14]]
        self.assertEqual(sum(1 for r in rows if (r["home_id"] if r["winner"]=="HOME" else r["away_id"])==1),5)
        self.assertEqual(len(rows),14)
        self.assertIn("5–9",self.story)

    def test_regular_season_is_not_postseason_provenance(self):
        self.assertIn("not any postseason match",self.story)
        self.assertIn("postseason bracket",self.story)
        self.assertIn("No champion appears",self.story)
        self.assertNotIn("2024",self.story)

    def test_only_candidate_jake_principal_pov_and_no_pseudo_people(self):
        self.assertEqual(self.cont["principal_pov_ids"],["CHAR-JAKE-KALOPER"])
        self.assertEqual(self.cont["other_owner_povs"],"NONE")
        self.assertNotRegex(self.story,r"\b(?:Edrin|Edin|Master Oren)\b")
        self.assertNotRegex(self.story,r"(?i)El Niño\s+(?:said|spoke|walked|thought|asked|smiled|decided)")
        self.assertIn("only proposed principal interior POV",self.story)

    def test_benedict_and_owner_unknown_guards(self):
        self.assertIn("The four Benedict banners",self.story)
        self.assertIn("user-attested, not provider-authenticated",self.story)
        self.assertIn("actual historical owner identities",self.story)
        self.assertIn("UNKNOWN",self.story)

    def test_atlas_and_fiction_firewall_retained(self):
        for x in ("PROPOSED FICTION / HISTORICAL ATLAS HOLD","NONCANON",
                  "home/away ordering proves no geographic location","not statements about real owners",
                  "independent Umpire","Founder HOLD"):
            self.assertIn(x.lower(),self.story.lower())

    def test_story_leaves_river_and_civic_costs_unresolved(self):
        for x in ("proper ferry","punt grounded","no passenger crossing",
                  "workers","unpaid","shelter","medicine cart","unheated"):
            self.assertIn(x.lower(),self.story.lower())

    def test_previous_week_thirteen_prose_byte_identical(self):
        self.assertEqual(git_blob(PREVIOUS),PREVIOUS_SHA)
        self.assertIn("The Room Beyond the Map",PREVIOUS.read_text(encoding="utf-8"))

    def test_84_84_competitive_coverage_but_editorial_hold(self):
        c=self.cont
        self.assertEqual(c["phase"],"WEEK_01_14_DRAFT_NONCANON")
        self.assertEqual(c["story_time_cutoff"],"after scoring week 14 only")
        m=c["matchup_coverage"]
        self.assertEqual(m["scoring_weeks_complete"],list(range(1,15)))
        self.assertEqual(m["verified_matchups"],84)
        self.assertEqual(m["prose_entries"],84)
        self.assertEqual(m["regular_season_matchups_covered"],84)
        self.assertEqual(m["regular_season_matchups_total"],84)
        self.assertTrue(m["week14_complete"])
        self.assertEqual(m["postseason"],"NOT_DRAFTED")
        self.assertEqual(c["drafts"]["fourteenth_week"],str(STORY.relative_to(ROOT)))

    def test_historical_and_release_gates_fail_closed(self):
        c=self.cont
        self.assertEqual(c["source"]["blob_sha"],SOURCE_SHA)
        self.assertEqual(c["source"]["raw_provider_sha"],"UNKNOWN")
        self.assertEqual(c["source"]["owner_identity"],"UNVERIFIED")
        self.assertEqual(c["historical_transactions_asserted"],0)
        self.assertEqual(c["world_atlas_status"],"UNAPPROVED_PROPOSED_STAGING")
        self.assertIn("DRAFT_UNREVIEWED",c["literary_status"])
        self.assertEqual(c["ci_week14"]["independent_umpire"],"NOT_OBTAINED")
        self.assertIn(c["ci_week14"]["status"],["PENDING_ACTUAL_CI_READBACK","SUCCESS_AT_TESTED_COMMIT"])

    def test_protected_2026_hard_canon_unchanged_sha1(self):
        for n,sha in PROTECTED.items():
            with self.subTest(protected=n):
                self.assertEqual(git_blob(ROOT/"living-novel/manuscript"/n),sha)

if __name__=="__main__":
    unittest.main()
