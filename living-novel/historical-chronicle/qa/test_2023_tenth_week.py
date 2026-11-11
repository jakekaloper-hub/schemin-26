"""NONCANON 2023 Week 10 six-scene Chronicle: source, POV, temporal, and protected-canon regression.
PASS is only a technical assertion; it is not an independent literary/Umpire/Atlas approval.
"""
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
W09 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W09.md"
W10 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W10.md"
CONT = ROOT / "living-novel/historical-chronicle/seasons/2023/CONTINUITY.json"
SOURCE_SHA = "ded119cde5c660f87f197f269b8d6ddd2a11316a"
W09_SHA = "22ae783dcf13961c70869a7c52a908b18307c7c4"
PROTECTED = {
 "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
 "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def score(value):
    return f"{Decimal(str(value)):.2f}"

class Test2023TenthWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.rows = next(w["matchups"] for w in cls.archive["weeks"] if w["week"] == 10)
        cls.story = W10.read_text(encoding="utf-8")
        cls.cont = json.loads(CONT.read_text(encoding="utf-8"))
        cls.headers = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", cls.story)
        cls.scenes = re.split(r"(?m)^## [IVX]+\. [^\n]+\n", cls.story)[1:]

    def test_archival_evidence_fingerprint_is_pinned(self):
        self.assertEqual(git_blob(ARCHIVE),SOURCE_SHA)
        self.assertEqual(self.archive["year"],2023)
        self.assertEqual(self.archive["source"],"Flaim ESPN 1417621")
        self.assertIn("Raw ESPN SHA unavailable",self.archive["limits"])

    def test_exact_six_disjoint_matchups_twelve_slots(self):
        self.assertEqual(len(self.rows),6)
        ids = [i for row in self.rows for i in (row["home_id"],row["away_id"])]
        self.assertEqual(len(ids),12)
        self.assertEqual(set(ids),set(range(1,13)))

    def test_winner_slots_and_source_score_agree(self):
        winners=[]
        for row in self.rows:
            home=Decimal(str(row["hp"]))>Decimal(str(row["ap"]))
            self.assertEqual(row["winner"],"HOME" if home else "AWAY")
            winners.append(row["home_id"] if home else row["away_id"])
        self.assertEqual(winners,[11,9,2,8,4,5])

    def test_every_scene_has_source_exact_labels_scores_winner_margin(self):
        self.assertEqual(len(self.scenes),6)
        for i,(row,scene) in enumerate(zip(self.rows,self.scenes),1):
            with self.subTest(scene=i):
                self.assertIn(f'{row["home"].strip()} (home), {score(row["hp"])}',scene)
                self.assertIn(f'{row["away"].strip()} (away), {score(row["ap"])}',scene)
                h=row["winner"]=="HOME"
                name=row["home"].strip() if h else row["away"].strip()
                sid=row["home_id"] if h else row["away_id"]
                self.assertIn(f"Winner: **{name} (slot {sid})**",scene)
                margin=abs(Decimal(str(row["hp"]))-Decimal(str(row["ap"])))
                self.assertIn(f"Margin **{margin:.2f}**",scene)

    def test_six_long_scenes_with_a_real_opening_and_afterword(self):
        self.assertEqual([x[0] for x in self.headers],["I","II","III","IV","V","VI"])
        self.assertGreaterEqual(len(self.story.split()),6200)
        self.assertIn("The first plank to break",self.story.split("## I.")[0])
        self.assertIn("### After the Tenth Reckoning",self.scenes[-1])
        for i,scene in enumerate(self.scenes,1):
            with self.subTest(i=i):
                self.assertGreaterEqual(len(scene.split()),700)
                self.assertGreaterEqual(scene.count("\n\n"),14)

    def test_slot_one_week_by_week_is_three_and_seven(self):
        first10=[next(row for row in week["matchups"] if 1 in (row["home_id"],row["away_id"])) for week in self.archive["weeks"][:10]]
        wins=[((row["home_id"] if row["winner"]=="HOME" else row["away_id"])==1) for row in first10]
        self.assertEqual(wins,[False,False,False,False,True,True,True,False,False,False])
        self.assertIn("3–7",self.story)
        self.assertIn("176.96–143.09",self.story)

    def test_provenance_and_owner_uncertainty_are_explicit(self):
        for phrase in ("NONCANON","PROPOSED FICTION / HISTORICAL ATLAS HOLD",
                       "user-attested, not provider-authenticated",
                       "Home/away competition fields do not identify physical venues",
                       "Four distinct Benedict banners","El Niño banner",
                       "sole proposed principal interior viewpoint", "No Week 11+"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase,self.story)

    def test_no_retired_or_out_of_class_principal_pov(self):
        self.assertNotRegex(self.story,r"\b(?:Edrin|Edin|Master Oren)\b")
        self.assertNotRegex(self.story,r"(?i)El Niño\s+(?:said|spoke|walked|thought|asked|smiled|decided)")
        self.assertEqual(self.cont["principal_pov_ids"],["CHAR-JAKE-KALOPER"])
        self.assertEqual(self.cont["other_owner_povs"],"NONE")

    def test_no_week_eleven_future_score_leak(self):
        eleven=next(w["matchups"] for w in self.archive["weeks"] if w["week"]==11)
        for row in eleven:
            with self.subTest(home=row["home"]):
                self.assertNotIn(f'{row["home"].strip()} (home), {score(row["hp"])}',self.story)
                self.assertNotIn(f'{row["away"].strip()} (away), {score(row["ap"])}',self.story)

    def test_previous_week_nine_bytes_intact(self):
        self.assertEqual(git_blob(W09),W09_SHA)
        self.assertIn("The Ash Beneath the Road",W09.read_text(encoding="utf-8"))

    def test_append_only_2023_continuity_sixty_of_eighty_four(self):
        c=self.cont
        self.assertRegex(c["phase"], r"^WEEK_01_(?:0[1-9]|1[0-4])_DRAFT_NONCANON$")
        self.assertGreaterEqual(int(c["phase"].split("_")[2]),10)
        self.assertEqual(c["story_time_cutoff"], f"after scoring week {int(c['phase'].split('_')[2])} only")
        m=c["matchup_coverage"]
        self.assertEqual(m["scoring_weeks_complete"][:10],list(range(1,11)))
        self.assertGreaterEqual(m["verified_matchups"],60)
        self.assertGreaterEqual(m["prose_entries"],60)
        self.assertGreaterEqual(m["regular_season_matchups_covered"],60)
        self.assertEqual(m["regular_season_matchups_total"],84)
        self.assertTrue(m["week10_complete"])
        self.assertEqual(c["drafts"]["tenth_week"],str(W10.relative_to(ROOT)))

    def test_river_and_consent_remain_genuinely_unresolved(self):
        for phrase in ("punt remained grounded","no passage authorized",
                       "no authority to consent","far-bank","not a government",
                       "river's closure","right to stop"):
            self.assertIn(phrase.lower(),self.story.lower())

    def test_provider_facts_and_canon_release_fail_closed(self):
        c=self.cont
        self.assertEqual(c["source"]["blob_sha"],SOURCE_SHA)
        self.assertEqual(c["source"]["raw_provider_sha"],"UNKNOWN")
        self.assertEqual(c["source"]["owner_identity"],"UNVERIFIED")
        self.assertEqual(c["historical_transactions_asserted"],0)
        self.assertEqual(c["world_atlas_status"],"UNAPPROVED_PROPOSED_STAGING")
        self.assertEqual(c["ci_week10"]["independent_umpire"],"NOT_OBTAINED")
        self.assertIn("DRAFT_UNREVIEWED",c["literary_status"])

    def test_four_protected_hard_canon_files_exact_main_bytes(self):
        for name,sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT/"living-novel/manuscript"/name),sha)

if __name__=="__main__":
    unittest.main()
