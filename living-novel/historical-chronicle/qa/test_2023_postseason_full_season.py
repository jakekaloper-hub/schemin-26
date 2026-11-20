"""Source-concordant NONCANON 2023 postseason and 19-part full-season reader regression.

This technical guard is neither independent literary review nor historical owner,
Atlas, Umpire, Founder or publication authorization. Raw ESPN refetch not done here.
"""
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = Path("living-novel/historical-chronicle/seasons/2023")
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
FINALS = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2015_2025_FLAIM_VERIFIED_CHAMPIONSHIP_ROUNDS.json"
PLAYOFF_EVIDENCE = ROOT / "living-novel/history/PLAYOFF_MATCHUP_EVIDENCE_2022_2025.json"
ASSEMBLED = ROOT / BASE / "READING_COPY_FULL_SEASON_NONCANON.md"
POSTSEASON = [ROOT / BASE / "weeks" / f"W{i}.md" for i in range(15, 18)]
EPILOGUE = ROOT / BASE / "EPILOGUE.md"
EXPECTED = (
    [str(BASE / "PROLOGUE.md")]
    + [str(BASE / "weeks" / f"W{i:02}.md") for i in range(1, 18)]
    + [str(BASE / "EPILOGUE.md")]
)
SOURCE_SHA = "ded119cde5c660f87f197f269b8d6ddd2a11316a"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
SOURCE_TAG = re.compile(
    r"<!-- SOURCE_BEGIN (?P<path>\S+) (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- SOURCE_END (?P=path) -->", re.DOTALL
)

def blob_sha(p):
    data = p.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def score(n):
    return f"{Decimal(str(n)):.2f}"

class Test2023PostseasonAndFullSeason(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.story = {w: (ROOT / BASE / "weeks" / f"W{w}.md").read_text(encoding="utf-8")
                     for w in range(15, 18)}
        cls.rows = {w: next(t["matchups"] for t in cls.archive["weeks"] if t["week"] == w)
                    for w in range(15, 18)}
        cls.reading = ASSEMBLED.read_text(encoding="utf-8")
        cls.sections = list(SOURCE_TAG.finditer(cls.reading))

    def test_primary_archival_input_pinned_and_limited(self):
        self.assertEqual(blob_sha(ARCHIVE), SOURCE_SHA)
        self.assertEqual(self.archive["source"], "Flaim ESPN 1417621")
        self.assertIn("Historical owner identity unknown", self.archive["limits"])
        self.assertIn("Raw ESPN SHA unavailable", self.archive["limits"])

    def test_seventeen_scoring_weeks_and_105_rows_not_miscounted(self):
        self.assertEqual([w["week"] for w in self.archive["weeks"]], list(range(1, 18)))
        self.assertEqual(sum(len(w["matchups"]) for w in self.archive["weeks"][:14]), 84)
        self.assertEqual(sum(len(w["matchups"]) for w in self.archive["weeks"][14:]), 21)
        self.assertEqual(sum(len(w["matchups"]) for w in self.archive["weeks"]), 105)

    def test_fifteen_decided_postseason_contests_six_unpaired_rows(self):
        rows = [r for w in range(15,18) for r in self.rows[w]]
        self.assertEqual(len(rows), 21)
        self.assertEqual(sum(r["winner"] != "UNDECIDED" for r in rows), 15)
        self.assertEqual(sum(r["winner"] == "UNDECIDED" for r in rows), 6)
        for w in range(15,18):
            self.assertEqual(len(self.rows[w]), 7)
            self.assertEqual(sum(r["winner"] != "UNDECIDED" for r in self.rows[w]), 5)
            self.assertEqual(sum(r["winner"] == "UNDECIDED" for r in self.rows[w]), 2)

    def test_all_postseason_archival_scores_and_winner_margins_in_written_prose(self):
        for w in range(15,18):
            text = self.story[w]
            for row in self.rows[w]:
                with self.subTest(week=w,home=row["home"]):
                    if row["winner"] == "UNDECIDED":
                        self.assertIn(f'{row["home"].strip()} (slot {row["home_id"]}), {score(row["hp"])}', text)
                        continue
                    self.assertIn(f'{row["home"].strip()} (home), {score(row["hp"])}', text)
                    self.assertIn(f'{row["away"].strip()} (away), {score(row["ap"])}', text)
                    home_won = row["winner"] == "HOME"
                    winner = (row["home"] if home_won else row["away"]).strip()
                    winner_slot = row["home_id"] if home_won else row["away_id"]
                    self.assertIn(f"Winner: **{winner} (slot {winner_slot})**", text)
                    self.assertIn(f'Margin **{abs(Decimal(str(row["hp"]))-Decimal(str(row["ap"]))):.2f}**', text)

    def test_each_postseason_part_has_seven_distinct_narrative_encounters(self):
        for week in range(15,18):
            with self.subTest(week=week):
                scene_markers = re.findall(r"(?m)^## ([IVX]+)\. ", self.story[week])
                self.assertEqual(scene_markers, ["I","II","III","IV","V","VI","VII"])
                self.assertGreaterEqual(len(self.story[week].split()), 3300)
                self.assertIn("NONCANON", self.story[week])

    def test_unpaired_scores_never_get_fabricated_winners(self):
        for w in range(15,18):
            text = self.story[w].lower()
            self.assertIn("winner undecided", text)
            self.assertIn("unpaired", text)
            self.assertTrue(any(term in text for term in ("no opponent", "without an opponent", "no opposing side")),
                            f"Unpaired row narrative missing in W{w}")

    def test_w15_does_not_know_w16_or_w17_scores(self):
        for future in ("214.52","192.88","159.52","140.76","181.20"):
            self.assertNotIn(future,self.story[15])

    def test_w16_does_not_know_w17_scores(self):
        for future in ("192.88","169.60","140.76","118.98","150.36"):
            self.assertNotIn(future,self.story[16])

    def test_champion_final_and_semifinals_match_independent_ledgers(self):
        rounds=json.loads(FINALS.read_text(encoding="utf-8"))["finals"]
        final=next(x for x in rounds if x["season"]==2023)
        self.assertEqual((final["winner_team_id"],final["runnerup_team_id"]),(12,11))
        self.assertEqual((score(final["winner_points"]),score(final["runnerup_points"])),("192.88","140.76"))
        self.assertIn("verified **2023 league champion Eggs Benedict (team slot 12)**",self.story[17])
        self.assertIn("runner-up Arm Chair GM (slot 11)",self.story[17])
        evidence=json.loads(PLAYOFF_EVIDENCE.read_text(encoding="utf-8"))["matchups"]
        two=[x for x in evidence if x["season"]==2023 and x["round"]=="semifinal"]
        self.assertEqual(len(two),2)
        for x in two:
            self.assertIn(f'{x["winner"]}',self.story[16])
            self.assertIn(score(x["winner_score"]),self.story[16])
            self.assertIn(score(x["loser_score"]),self.story[16])

    def test_nineteen_original_source_components_in_order(self):
        self.assertEqual(len(EXPECTED),19)
        self.assertEqual(len(self.sections),19)
        self.assertEqual([x.group("path") for x in self.sections],EXPECTED)
        self.assertEqual(self.reading.count("<!-- SOURCE_BEGIN "),19)
        self.assertEqual(self.reading.count("<!-- SOURCE_END "),19)
        self.assertEqual(self.reading.count("<!-- BEGIN_COMPILED_MANUSCRIPT -->"),1)
        self.assertEqual(self.reading.count("<!-- END_COMPILED_MANUSCRIPT -->"),1)

    def test_full_reading_copy_source_byte_integrity(self):
        for section in self.sections:
            with self.subTest(path=section.group("path")):
                source=(ROOT/section.group("path")).read_text(encoding="utf-8")
                self.assertEqual(section.group("sha"),blob_sha(ROOT/section.group("path")))
                self.assertEqual(section.group("body"),source.rstrip())
                self.assertIn(f"| {section.group('path')} | {section.group('sha')} |",self.reading)

    def test_real_assembled_length_not_skeleton(self):
        self.assertGreater(len(self.reading.split()),85000)
        self.assertGreater(len(self.reading),490000)
        self.assertGreater(len(EPILOGUE.read_text(encoding="utf-8").split()),2000)

    def test_sole_candidate_pov_and_no_anthropomorphism(self):
        for w in range(15,18):
            x=self.story[w]
            self.assertIn("CHAR-JAKE-KALOPER",x)
            self.assertNotRegex(x,r"\b(?:Edrin|Edin|Master Oren)\s+(?:said|thought|decided|believed)")
            self.assertNotRegex(x,r"(?i)El Niño\s+(?:said|thought|walked|smiled|asked|spoke)")
        self.assertIn("CHAR-JAKE-KALOPER",EPILOGUE.read_text(encoding="utf-8"))

    def test_hist_owner_and_atlas_promotion_held(self):
        for p in [*POSTSEASON,EPILOGUE]:
            t=p.read_text(encoding="utf-8").lower()
            self.assertIn("noncanon",t)
            self.assertIn("atlas",t)
            self.assertIn("umpire",t)
            self.assertTrue(any(term in t for term in ("unverified", "not authenticated", "unknown", "does not authenticate")),
                            f"Historical owner identity must remain unproven in {p.name}")
        self.assertIn("NOT PUBLISHED",self.reading)
        self.assertIn("Founder HOLD",self.reading)
        self.assertIn("not an automatically released",self.reading)

    def test_protected_2026_prologue_and_chapters_unchanged(self):
        for name,expected in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob_sha(ROOT/"living-novel/manuscript"/name),expected)

if __name__ == "__main__":
    unittest.main()
