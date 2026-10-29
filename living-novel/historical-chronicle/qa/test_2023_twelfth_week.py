"""NONCANON 2023 Week 12: source exactness, POV, substantial prose, append-only and hard-canon guards.
Passing code does not independently approve literature, Atlas, Umpire or canon release.
"""
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT=Path(__file__).resolve().parents[3]
ARCHIVE=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
W11=ROOT/"living-novel/historical-chronicle/seasons/2023/weeks/W11.md"
W12=ROOT/"living-novel/historical-chronicle/seasons/2023/weeks/W12.md"
CONT=ROOT/"living-novel/historical-chronicle/seasons/2023/CONTINUITY.json"
SOURCE_SHA="ded119cde5c660f87f197f269b8d6ddd2a11316a"
W11_SHA="2aca8a3f578ba5e73451ea648488c4711979558a"
PROTECTED={
 "PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
 "CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def git_blob(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def score(x):
    return f"{Decimal(str(x)):.2f}"

class Test2023TwelfthWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive=json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.rows=next(w["matchups"] for w in cls.archive["weeks"] if w["week"]==12)
        cls.story=W12.read_text(encoding="utf-8")
        cls.cont=json.loads(CONT.read_text(encoding="utf-8"))
        cls.headers=re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$",cls.story)
        cls.scenes=re.split(r"(?m)^## [IVX]+\. [^\n]+\n",cls.story)[1:]

    def test_pinned_provenance(self):
        self.assertEqual(git_blob(ARCHIVE),SOURCE_SHA)
        self.assertEqual(self.archive["source"],"Flaim ESPN 1417621")
        self.assertIn("Raw ESPN SHA unavailable",self.archive["limits"])

    def test_exact_twelve_disjoint_slots_six_fixtures(self):
        self.assertEqual(len(self.rows),6)
        self.assertEqual(sorted(i for r in self.rows for i in (r["home_id"],r["away_id"])),list(range(1,13)))

    def test_winner_truth_and_expected_slots(self):
        ids=[]
        for r in self.rows:
            h=Decimal(str(r["hp"]))>Decimal(str(r["ap"]))
            self.assertEqual(r["winner"],"HOME" if h else "AWAY")
            ids.append(r["home_id"] if h else r["away_id"])
        self.assertEqual(ids,[10,9,2,5,11,7])

    def test_all_six_scenes_source_identical_scores_and_margins(self):
        self.assertEqual([h[0] for h in self.headers],["I","II","III","IV","V","VI"])
        self.assertEqual(len(self.scenes),6)
        for i,(r,scene) in enumerate(zip(self.rows,self.scenes),1):
            with self.subTest(i=i):
                self.assertIn(f'{r["home"].strip()} (home), {score(r["hp"])}',scene)
                self.assertIn(f'{r["away"].strip()} (away), {score(r["ap"])}',scene)
                h=r["winner"]=="HOME"
                winner=(r["home"] if h else r["away"]).strip()
                sid=r["home_id"] if h else r["away_id"]
                self.assertIn(f"Winner: **{winner} (slot {sid})**",scene)
                margin=abs(Decimal(str(r["hp"]))-Decimal(str(r["ap"])))
                self.assertIn(f"Margin **{margin:.2f}**",scene)

    def test_sustained_prose_six_independent_drama_scenes(self):
        self.assertGreaterEqual(len(self.story.split()),5500)
        self.assertIn("When Jake returned to his room",self.story.split("## I.")[0])
        self.assertIn("### After the Twelfth Reckoning",self.scenes[-1])
        for i,scene in enumerate(self.scenes[:5],1):
            with self.subTest(i=i):
                self.assertGreaterEqual(len(scene.split()),600)
                self.assertGreaterEqual(scene.count("\n\n"),9)

    def test_slot_one_four_wins_eight_losses_at_week12(self):
        found=[next(r for r in w["matchups"] if 1 in (r["home_id"],r["away_id"])) for w in self.archive["weeks"][:12]]
        wins=[(r["home_id"] if r["winner"]=="HOME" else r["away_id"])==1 for r in found]
        self.assertEqual(wins,[False,False,False,False,True,True,True,False,False,False,True,False])
        self.assertIn("4–8",self.story)
        self.assertIn("Benedict Kenobi (away), 123.16",self.story)

    def test_historic_owner_uncertainty_and_release_holds(self):
        for phrase in ("NONCANON","PROPOSED FICTION / HISTORICAL ATLAS HOLD",
                       "user-attested, not provider-authenticated",
                       "archive home/away flags are not physical locations",
                       "four archived Benedict banners","El Niño banner",
                       "sole proposed principal interior POV","No Week 13+"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(),self.story.lower())

    def test_exclusive_proposed_principal_pov(self):
        self.assertNotRegex(self.story,r"\b(?:Edrin|Edin|Master Oren)\b")
        self.assertNotRegex(self.story,r"(?i)El Niño\s+(?:said|spoke|walked|thought|asked|smiled|decided)")
        self.assertEqual(self.cont["principal_pov_ids"],["CHAR-JAKE-KALOPER"])
        self.assertEqual(self.cont["other_owner_povs"],"NONE")

    def test_no_week13_competitive_foreknowledge(self):
        rows=next(w["matchups"] for w in self.archive["weeks"] if w["week"]==13)
        for r in rows:
            self.assertNotIn(f'{r["home"].strip()} (home), {score(r["hp"])}',self.story)
            self.assertNotIn(f'{r["away"].strip()} (away), {score(r["ap"])}',self.story)

    def test_previous_week11_prose_intact(self):
        self.assertEqual(git_blob(W11),W11_SHA)
        self.assertIn("The Orchard That Refused a Name",W11.read_text(encoding="utf-8"))

    def test_continuity_seventy_two_of_eighty_four_with_season_open(self):
        c=self.cont
        self.assertEqual(c["phase"],"WEEK_01_12_DRAFT_NONCANON")
        self.assertEqual(c["story_time_cutoff"],"after scoring week 12 only")
        m=c["matchup_coverage"]
        self.assertEqual(m["scoring_weeks_complete"],list(range(1,13)))
        self.assertEqual(m["verified_matchups"],72)
        self.assertEqual(m["prose_entries"],72)
        self.assertEqual(m["regular_season_matchups_covered"],72)
        self.assertEqual(m["regular_season_matchups_total"],84)
        self.assertTrue(m["week12_complete"])
        self.assertEqual(m["postseason"],"NOT_DRAFTED")
        self.assertEqual(c["drafts"]["twelfth_week"],str(W12.relative_to(ROOT)))

    def test_causal_river_and_warming_room_limits_retained(self):
        for phrase in ("punt grounded","proper ferry","no passenger crossing",
                       "not a safe operating hearth","lender","far bank"):
            self.assertIn(phrase.lower(),self.story.lower())

    def test_no_unverified_provider_fact_or_auto_promotion(self):
        c=self.cont
        self.assertEqual(c["source"]["blob_sha"],SOURCE_SHA)
        self.assertEqual(c["source"]["raw_provider_sha"],"UNKNOWN")
        self.assertEqual(c["source"]["owner_identity"],"UNVERIFIED")
        self.assertEqual(c["historical_transactions_asserted"],0)
        self.assertEqual(c["world_atlas_status"],"UNAPPROVED_PROPOSED_STAGING")
        self.assertEqual(c["ci_week12"]["independent_umpire"],"NOT_OBTAINED")
        self.assertIn("DRAFT_UNREVIEWED",c["literary_status"])

    def test_four_protected_hard_canon_sha1(self):
        for name,sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT/"living-novel/manuscript"/name),sha)

if __name__=="__main__":
    unittest.main()
