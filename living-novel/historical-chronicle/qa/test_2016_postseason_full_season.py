"""2016 source-reconciled postseason and 16-component full-season NONCANON reader.

Technical file checks are not a substitute for independent Authors Council,
Character Canon, Atlas, Umpire, Founder, or authenticated ESPN owner approval.
"""
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = Path("living-novel/historical-chronicle/seasons/2016")
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
POST = ROOT / BASE / "POSTSEASON.md"
EPILOGUE = ROOT / BASE / "EPILOGUE.md"
READER = ROOT / BASE / "READING_COPY_FULL_SEASON_NONCANON.md"
PARTS = (
    [str(BASE / "PROLOGUE.md")]
    + [str(BASE / "weeks" / f"W{i:02}.md") for i in range(1, 14)]
    + [str(BASE / "POSTSEASON.md"), str(BASE / "EPILOGUE.md")]
)
SOURCE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
SECTION = re.compile(
    r"<!-- BEGIN 2016 (?P<path>\S+) \| git_blob (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- END 2016 (?P=path) -->", re.S
)
SCENE = re.compile(r"(?m)^### (?P<roman>I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII) — .+$")


def blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def exact_score(n):
    return f"{Decimal(str(n)):.2f}"


class Test2016PostseasonFullSeason(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.post = POST.read_text(encoding="utf-8")
        cls.epilogue = EPILOGUE.read_text(encoding="utf-8")
        cls.reader = READER.read_text(encoding="utf-8")
        cls.weeks = {w["week"]: w["matchups"] for w in cls.archive["weeks"]}
        cls.sections = list(SECTION.finditer(cls.reader))

    def test_source_sha_and_archive_limit(self):
        self.assertEqual(blob(ARCHIVE), SOURCE_SHA)
        self.assertEqual(self.archive["year"], 2016)
        self.assertEqual(self.archive["source"], "Flaim ESPN 1417621")
        self.assertIn("historical identity unverified", self.archive["limits"])

    def test_thirteen_regular_weeks_seventy_eight_fixtures(self):
        self.assertEqual(len(self.archive["weeks"]), 17)
        self.assertEqual(sum(len(self.weeks[w]) for w in range(1, 14)), 78)

    def test_duplicate_two_week_scoring_periods_are_not_new_games(self):
        self.assertEqual(self.weeks[14], self.weeks[15])
        self.assertEqual(self.weeks[16], self.weeks[17])
        self.assertEqual(len(self.weeks[14]), 6)
        self.assertEqual(len(self.weeks[16]), 6)
        self.assertEqual({r["period"] for r in self.weeks[14]}, {14})
        self.assertEqual({r["period"] for r in self.weeks[16]}, {15})
        self.assertEqual(sum(len(self.weeks[w]) for w in range(14, 18)), 24)
        distinct = {
            (r["period"], r["home_id"], r["away_id"], r["tier"])
            for w in range(14, 18) for r in self.weeks[w]
        }
        self.assertEqual(len(distinct), 12)

    def test_twelve_separate_postseason_scenes_and_scores(self):
        markers = list(SCENE.finditer(self.post))
        self.assertEqual([x.group("roman") for x in markers],
                         ["I", "II", "III", "IV", "V", "VI",
                          "VII", "VIII", "IX", "X", "XI", "XII"])
        rows = self.weeks[14] + self.weeks[16]
        self.assertEqual(len(rows), len(markers))
        for i, row in enumerate(rows):
            scene = self.post[markers[i].start():markers[i + 1].start()
                              if i + 1 < len(markers) else len(self.post)]
            with self.subTest(period=row["period"], home=row["home"]):
                self.assertIn(row["home"].strip(), scene)
                self.assertIn(row["away"].strip(), scene)
                self.assertIn(f"(ID {row['home_id']})", scene)
                self.assertIn(f"(ID {row['away_id']})", scene)
                self.assertIn(exact_score(row["hp"]), scene)
                self.assertIn(exact_score(row["ap"]), scene)
                self.assertIn(exact_score(abs(row["hp"] - row["ap"])), scene)
                self.assertIn("defeated", scene)
                self.assertEqual(row["winner"],
                                 "HOME" if row["hp"] > row["ap"] else "AWAY")

    def test_semifinal_and_championship_are_distinct(self):
        self.assertEqual(sum(r["tier"] == "WINNERS_BRACKET"
                             for r in self.weeks[14]), 2)
        self.assertEqual(sum(r["tier"] == "WINNERS_BRACKET"
                             for r in self.weeks[16]), 1)
        final = next(r for r in self.weeks[16] if r["tier"] == "WINNERS_BRACKET")
        self.assertEqual((final["home_id"], final["away_id"], final["winner"]),
                         (8, 7, "HOME"))
        self.assertEqual((exact_score(final["hp"]), exact_score(final["ap"])),
                         ("217.70", "206.88"))
        self.assertIn("verified 2016 champion", self.post)
        self.assertIn("not the championship final", self.post.lower().replace("*", ""))

    def test_reader_has_sixteen_source_exact_components(self):
        self.assertEqual(len(PARTS), 16)
        self.assertEqual(len(self.sections), 16)
        self.assertEqual([x.group("path") for x in self.sections], PARTS)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016 "), 16)
        self.assertEqual(self.reader.count("<!-- END 2016 "), 16)
        self.assertEqual(self.reader.count("<!-- BEGIN_COMPILED_MANUSCRIPT -->"), 1)
        self.assertEqual(self.reader.count("<!-- END_COMPILED_MANUSCRIPT -->"), 1)
        for section in self.sections:
            path = section.group("path")
            with self.subTest(path=path):
                source = (ROOT / path).read_text(encoding="utf-8")
                self.assertEqual(blob(ROOT / path), section.group("sha"))
                self.assertEqual(section.group("body"), source.rstrip())
                self.assertIn(f"| {path} | {section.group('sha')} |", self.reader)

    def test_substantive_assembled_prose_not_an_outline(self):
        self.assertGreaterEqual(len(self.post.split()), 5400)
        self.assertGreaterEqual(len(self.epilogue.split()), 2300)
        self.assertGreaterEqual(len(self.reader.split()), 70000)
        self.assertIn("The Gate That Would Not Crown a King", self.post)
        self.assertIn("The Year the Table Went Home", self.epilogue)
        self.assertIn("12 unique postseason pairings", self.reader.replace("*", ""))

    def test_reader_is_noncanon_without_false_approval(self):
        for part in (self.post, self.epilogue, self.reader):
            lower = part.lower()
            for term in ("noncanon", "atlas", "umpire", "historical", "founder"):
                self.assertIn(term, lower)
            self.assertTrue(any(term in lower for term in
                                ("not provider-authenticated", "unverified")))
        self.assertIn("NOT PUBLISHED", self.reader)
        self.assertIn("Founder HOLD", self.reader)

    def test_exclusive_twelve_owner_firewall(self):
        for part in (self.post, self.epilogue):
            self.assertIn("CHAR-JAKE-KALOPER", part)
            self.assertIn("PRINCIPAL_CHARACTER", part)
            self.assertNotRegex(part, r"(?im)^## (?:Edrin|Edin|Oren)\b")
            self.assertNotRegex(part, r"(?i)El Niño\s+(?:thought|said|walked|smiled)")
        self.assertIn("not verified as scoring slot 1", self.post)

    def test_unresolved_world_obligations_preserved(self):
        for term in ("cordon", "unpaid", "unopened", "frame", "key", "wheel"):
            self.assertIn(term, self.post.lower())
            self.assertIn(term, self.epilogue.lower())

    def test_protected_2026_manuscript_hashes_unchanged(self):
        for filename, expected in PROTECTED.items():
            with self.subTest(filename=filename):
                self.assertEqual(blob(ROOT / "living-novel/manuscript" / filename), expected)


if __name__ == "__main__":
    unittest.main()
