"""2016 noncanonical causal Chapter V and five-source-component reader checks.

Deterministic evidence/structure checks are neither literary acceptance nor
historic owner authentication, Atlas approval, Umpire independence, or canon.
"""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
G01 = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
G01_BLOB = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
FILES = [
    "THE_DEBT_BEFORE_THE_DOOR_CHAPTER_01_NONCANON.md",
    "THE_NAMES_BEYOND_THE_WALL_CHAPTER_02_NONCANON.md",
    "THE_WORK_OF_UNTURNED_THINGS_CHAPTER_03_NONCANON.md",
    "WHAT_THE_WALL_KEPT_CHAPTER_04_NONCANON.md",
    "THE_WEIGHT_OF_DRY_GRAIN_CHAPTER_05_NONCANON.md",
]
BLOBS = [
    "d93505009d7dda7acc010ce1a6e5ec2bacf65ec2",
    "756126cb4e151a0bd78ece39ab59a4c54ef2aa43",
    "f9bf0721c989d30bfd09189388b93293ba3a8ce0",
    "8994f9e443a6313dee217dfd5f92aedeff7bd88c",
    "40d12860e93d9393b18d7771c427061c82e46c8c",
]
READING = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_05_NONCANON.md"
SECTIONS = re.compile(
    r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \| git_blob (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- END 2016_CAUSAL (?P=name) -->", re.S
)

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def pts(number):
    return Decimal(str(number)).quantize(Decimal("0.01"))

class Test2016CausalChapterFive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g01 = json.loads(G01.read_text(encoding="utf-8"))
        cls.chapter = (BASE / FILES[-1]).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("---\n\n*Editorial handoff")[0]
        cls.reading = READING.read_text(encoding="utf-8")
        cls.sections = list(SECTIONS.finditer(cls.reading))

    def test_flaim_transcription_pinned_not_fresh_provider(self):
        self.assertEqual(git_blob(G01), G01_BLOB)
        self.assertEqual(self.g01["year"], 2016)
        self.assertIn("not provider-authenticated", self.chapter)

    def test_week_twelve_gunslingers_result_exact_and_correct_time(self):
        week = next(x for x in self.g01["weeks"] if x["week"] == 12)
        games = [m for m in week["matchups"] if 1 in (m["home_id"], m["away_id"])]
        self.assertEqual(len(games), 1)
        game = games[0]
        self.assertEqual((game["home_id"], game["away_id"], game["winner"]), (7, 1, "AWAY"))
        self.assertEqual((pts(game["hp"]), pts(game["ap"])), (Decimal("86.72"), Decimal("112.20")))
        self.assertIn("112.20 to 86.72", self.prose)
        self.assertIn("The Gunslingers", self.prose)

    def test_no_later_week_source_claim_or_fake_identity(self):
        self.assertNotIn("103.86", self.prose)
        self.assertNotIn("81.44", self.prose)
        self.assertNotIn("214.02", self.prose)
        self.assertNotIn("real-world owner Jake", self.prose)
        self.assertIn("slot-one owner is not provider-authenticated", self.chapter)

    def test_substantial_five_part_causal_not_weekly_schedule(self):
        self.assertGreaterEqual(len(self.chapter.split()), 4500)
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\. ", self.chapter), ["I", "II", "III", "IV", "V"])
        self.assertNotIn("## Week Twelve", self.prose)
        self.assertIn("The weighing yard", self.prose)
        self.assertIn("A cart-owner", self.prose)

    def test_single_principal_owner_and_only_noncanon_world(self):
        for word in ("CHAR-JAKE-KALOPER", "PRINCIPAL_CHARACTER", "NONCANON", "HOLD", "Atlas"):
            self.assertIn(word, self.chapter)
        self.assertNotRegex(self.prose, r"(?m)^### (Edrin|Edin|Oren)\b")
        self.assertIn("All mills, markets", self.chapter)
        self.assertIn("not historical facts or approved geography", self.prose)

    def test_borrowed_awning_not_permanently_assigned(self):
        self.assertIn("The young man took his cart down the road", self.prose)
        self.assertIn("The owner of the awning arrived", self.prose)
        self.assertIn("Chapter IV's distinct short market awning is reclaimed", self.chapter)
        self.assertIn("original three-night canvas was returned", self.chapter)

    def test_suspect_food_not_declared_safe(self):
        self.assertIn("No conclusion could be bought from urgency", self.prose)
        self.assertIn("nothing milled", self.prose)
        self.assertIn("remain closed and separate", self.prose)
        self.assertIn("Grain is not certified safe", self.chapter)

    def test_nonowner_characters_do_not_need_jakes_permission(self):
        for term in ("not under him", "The shed owner", "The wrapped-hand woman",
                     "She had not sought Jake's permission"):
            self.assertIn(term, self.prose)

    def test_unresolved_claims_remain_separate(self):
        lower = self.chapter.lower()
        for phrase in ("chest unretrieved", "reaching frame unbuilt", "supplier invoice",
                       "timber-worker debt", "sealed message unopened", "wheel unturned",
                       "unknown claimant unidentified"):
            self.assertIn(phrase, lower)
        self.assertNotIn("missing claimant was found", self.prose.lower())

    def test_exact_source_reader_has_five_original_full_chapters(self):
        self.assertEqual(len(self.sections), 5)
        self.assertEqual([m.group("name") for m in self.sections], FILES)
        for i, match in enumerate(self.sections):
            with self.subTest(file=FILES[i]):
                self.assertEqual(git_blob(BASE / FILES[i]), BLOBS[i])
                self.assertEqual(match.group("sha"), BLOBS[i])
                self.assertEqual(match.group("body"), (BASE / FILES[i]).read_text(encoding="utf-8").rstrip())
                self.assertIn("| `" + FILES[i] + "` | `" + BLOBS[i] + "` |", self.reading)

    def test_reader_release_holds_and_wordcount(self):
        self.assertGreaterEqual(len(self.reading.split()), 21500)
        self.assertIn("Chapters I–V (NONCANON)", self.reading)
        self.assertIn("independent Authors Council/Umpire", self.reading)
        self.assertIn("Founder-only canon/publication", self.reading)
        self.assertEqual(self.reading.count("<!-- BEGIN 2016_CAUSAL"), 5)
        self.assertEqual(self.reading.count("<!-- END 2016_CAUSAL"), 5)
        self.assertIn("<!-- END_CAUSAL_READING_COPY -->", self.reading)
        self.assertTrue(all("living-novel/manuscript/" not in f for f in FILES))

if __name__ == "__main__":
    unittest.main()
