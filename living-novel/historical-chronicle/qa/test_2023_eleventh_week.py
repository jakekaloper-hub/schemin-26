"""2023 W11 Chronicle: source-exact fixtures, substantial prose, continuity, POV, and canon HOLD.
PASS is deterministic technical evidence only, NOT independent editorial/Atlas/Umpire acceptance.
"""
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
W10 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W10.md"
W11 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W11.md"
CONT = ROOT / "living-novel/historical-chronicle/seasons/2023/CONTINUITY.json"
SOURCE_SHA = "ded119cde5c660f87f197f269b8d6ddd2a11316a"
W10_SHA = "18d43a58d240646322ab0245f82d688bc535a125"
PROTECTED = {
 "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
 "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(p):
    data=p.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def score(number):
    return f"{Decimal(str(number)):.2f}"

class Test2023EleventhWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive=json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.rows=next(w["matchups"] for w in cls.archive["weeks"] if w["week"]==11)
        cls.story=W11.read_text(encoding="utf-8")
        cls.cont=json.loads(CONT.read_text(encoding="utf-8"))
        cls.headers=re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$",cls.story)
        cls.scenes=re.split(r"(?m)^## [IVX]+\. [^\n]+\n",cls.story)[1:]

    def test_source_fingerprint_provenance(self):
        self.assertEqual(git_blob(ARCHIVE),SOURCE_SHA)
        self.assertEqual(self.archive["year"],2023)
        self.assertEqual(self.archive["source"],"Flaim ESPN 1417621")
        self.assertIn("Raw ESPN SHA unavailable",self.archive["limits"])

    def test_six_matchups_each_historical_slot_once(self):
        self.assertEqual(len(self.rows),6)
        ids=[i for row in self.rows for i in (row["home_id"],row["away_id"])]
        self.assertEqual(sorted(ids),list(range(1,13)))

    def test_six_winners_and_precise_source_scores(self):
        winner_slots=[]
        for row in self.rows:
            self.assertEqual(row["winner"],"HOME" if Decimal(str(row["hp"]))>Decimal(str(row["ap"])) else "AWAY")
            winner_slots.append(row["home_id"] if row["winner"]=="HOME" else row["away_id"])
        self.assertEqual(winner_slots,[8,12,5,1,9,2])

    def test_all_scenes_exactly_joined_to_matchup_rows(self):
        self.assertEqual(len(self.scenes),6)
        self.assertEqual([h[0] for h in self.headers],["I","II","III","IV","V","VI"])
        for i,(row,scene) in enumerate(zip(self.rows,self.scenes),1):
            with self.subTest(scene=i):
                self.assertIn(f'{row["home"].strip()} (home), {score(row["hp"])}',scene)
                self.assertIn(f'{row["away"].strip()} (away), {score(row["ap"])}',scene)
                home=row["winner"]=="HOME"
                name=(row["home"] if home else row["away"]).strip()
                sid=row["home_id"] if home else row["away_id"]
                self.assertIn(f"Winner: **{name} (slot {sid})**",scene)
                margin=abs(Decimal(str(row["hp"]))-Decimal(str(row["ap"])))
                self.assertIn(f"Margin **{margin:.2f}**",scene)

    def test_substantial_prose_scenes_opening_and_aftermath(self):
        self.assertGreaterEqual(len(self.story.split()),5500)
        self.assertIn("The orchard had been planted",self.story.split("## I.")[0])
        self.assertIn("### After the Eleventh Reckoning",self.scenes[-1])
        for i,scene in enumerate(self.scenes[:5],1):
            with self.subTest(scene=i):
                self.assertGreaterEqual(len(scene.split()),550)
                self.assertGreaterEqual(scene.count("\n\n"),10)

    def test_slot_one_four_and_seven_not_recast_as_person_authenticated(self):
        rows=[next(row for row in w["matchups"] if 1 in (row["home_id"],row["away_id"])) for w in self.archive["weeks"][:11]]
        wins=[(row["home_id"] if row["winner"]=="HOME" else row["away_id"])==1 for row in rows]
        self.assertEqual(wins,[False,False,False,False,True,True,True,False,False,False,True])
        self.assertIn("4–7",self.story)
        self.assertIn("160.79",self.story)
        self.assertIn("user-attested, not provider-authenticated",self.story)

    def test_provenance_and_editorial_holds_are_explicit(self):
        for phrase in ("NONCANON","PROPOSED FICTION / HISTORICAL ATLAS HOLD",
                       "Home/away competition fields do not identify physical venues",
                       "four distinct Benedict banners","The El Niño banner",
                       "sole proposed principal interior viewpoint","No Week 12+"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(),self.story.lower())

    def test_no_retired_pov_or_speaking_el_nino(self):
        self.assertNotRegex(self.story,r"\b(?:Edrin|Edin|Master Oren)\b")
        self.assertNotRegex(self.story,r"(?i)El Niño\s+(?:said|spoke|walked|thought|asked|smiled|decided)")
        self.assertEqual(self.cont["principal_pov_ids"],["CHAR-JAKE-KALOPER"])
        self.assertEqual(self.cont["other_owner_povs"],"NONE")

    def test_no_week_twelve_future_results_in_story(self):
        rows=next(w["matchups"] for w in self.archive["weeks"] if w["week"]==12)
        for row in rows:
            with self.subTest(home=row["home"]):
                self.assertNotIn(f'{row["home"].strip()} (home), {score(row["hp"])}',self.story)
                self.assertNotIn(f'{row["away"].strip()} (away), {score(row["ap"])}',self.story)

    def test_previous_week_ten_manuscript_bytes_remain_intact(self):
        self.assertEqual(git_blob(W10),W10_SHA)
        self.assertIn("The Timber That Did Not Float",W10.read_text(encoding="utf-8"))

    def test_append_only_2023_continuity_sixty_six_of_eighty_four(self):
        c=self.cont
        self.assertRegex(c["phase"], r"^WEEK_01_(?:0[1-9]|1[0-4])_DRAFT_NONCANON$")
        self.assertGreaterEqual(int(c["phase"].split("_")[2]),11)
        self.assertEqual(c["story_time_cutoff"], f"after scoring week {int(c['phase'].split('_')[2])} only")
        m=c["matchup_coverage"]
        self.assertEqual(m["scoring_weeks_complete"][:11],list(range(1,12)))
        self.assertGreaterEqual(m["verified_matchups"],66)
        self.assertGreaterEqual(m["prose_entries"],66)
        self.assertGreaterEqual(m["regular_season_matchups_covered"],66)
        self.assertEqual(m["regular_season_matchups_total"],84)
        self.assertTrue(m["week11_complete"])
        self.assertEqual(c["drafts"]["eleventh_week"],str(W11.relative_to(ROOT)))
        self.assertEqual(m["postseason"],"NOT_DRAFTED")

    def test_end_of_week_eleven_retains_unresolved_world_consequences(self):
        for phrase in ("punt remained grounded","proper ferry was still lost",
                       "no passage authorized","far bank","unresolved","workers"):
            self.assertIn(phrase.lower(),self.story.lower())

    def test_source_world_and_promotion_fail_closed(self):
        c=self.cont
        self.assertEqual(c["source"]["blob_sha"],SOURCE_SHA)
        self.assertEqual(c["source"]["raw_provider_sha"],"UNKNOWN")
        self.assertEqual(c["source"]["owner_identity"],"UNVERIFIED")
        self.assertEqual(c["historical_transactions_asserted"],0)
        self.assertEqual(c["world_atlas_status"],"UNAPPROVED_PROPOSED_STAGING")
        self.assertEqual(c["ci_week11"]["independent_umpire"],"NOT_OBTAINED")
        self.assertIn("DRAFT_UNREVIEWED",c["literary_status"])

    def test_protected_hard_canon_digests(self):
        for name,sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT/"living-novel/manuscript"/name),sha)

if __name__=="__main__":
    unittest.main()
