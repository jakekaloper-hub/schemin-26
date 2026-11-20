"""Historical 2016 NONCANON causal Chapter VI and exact six-chapter reading copy.

These deterministic tests do not confer human owner identity, approved geography,
literary acceptance, independent Umpire review or Founder canon/publication.
"""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
NAMES = [
    "THE_DEBT_BEFORE_THE_DOOR_CHAPTER_01_NONCANON.md",
    "THE_NAMES_BEYOND_THE_WALL_CHAPTER_02_NONCANON.md",
    "THE_WORK_OF_UNTURNED_THINGS_CHAPTER_03_NONCANON.md",
    "WHAT_THE_WALL_KEPT_CHAPTER_04_NONCANON.md",
    "THE_WEIGHT_OF_DRY_GRAIN_CHAPTER_05_NONCANON.md",
    "THE_SILENCE_IN_THE_SECOND_PRINTING_CHAPTER_06_NONCANON.md",
]
BLOBS = [
    "d93505009d7dda7acc010ce1a6e5ec2bacf65ec2",
    "756126cb4e151a0bd78ece39ab59a4c54ef2aa43",
    "f9bf0721c989d30bfd09189388b93293ba3a8ce0",
    "8994f9e443a6313dee217dfd5f92aedeff7bd88c",
    "40d12860e93d9393b18d7771c427061c82e46c8c",
    "4e3d655895847e9910b7e8c69349fb2b09c94b4b",
]
READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_06_NONCANON.md"
SECTIONS = re.compile(
    r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \| git_blob (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- END 2016_CAUSAL (?P=name) -->", re.S
)

def blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def score(value):
    return Decimal(str(value)).quantize(Decimal("0.01"))

class Test2016CausalChapterSix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.chapter = (BASE / NAMES[-1]).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("---\n\n*Editorial handoff")[0]
        cls.reader = READER.read_text(encoding="utf-8")
        cls.sections = list(SECTIONS.finditer(cls.reader))

    def test_retained_source_pinned_no_fresh_espn_pretence(self):
        self.assertEqual(blob(ARCHIVE), ARCHIVE_SHA)
        self.assertEqual(self.archive["year"], 2016)
        self.assertIn("NOT provider-authenticated", self.chapter)

    def test_week_13_loss_exact_and_hyenas_id_disambiguation(self):
        games = next(w["matchups"] for w in self.archive["weeks"] if w["week"] == 13)
        selected = [g for g in games if 1 in (g["home_id"], g["away_id"])]
        self.assertEqual(len(selected), 1)
        row = selected[0]
        self.assertEqual((row["home_id"], row["away_id"], row["winner"]), (1, 8, "AWAY"))
        self.assertEqual((score(row["hp"]), score(row["ap"])), (Decimal("81.44"), Decimal("103.86")))
        self.assertIn("81.44 to 103.86", self.prose)
        self.assertIn("Austin's Hyena's", self.prose)
        self.assertIn("The Real Austin's Hyenas", self.prose)
        self.assertIn("distinct ID 12", self.prose)

    def test_postseason_future_not_foregrounded(self):
        for future_score in ("204.84", "214.02", "167.74", "209.82"):
            self.assertNotIn(future_score, self.prose)
        self.assertIn("all postseason outcomes stay off-page", self.chapter.lower())

    def test_full_five_movement_dramatic_chapter(self):
        self.assertGreaterEqual(len(self.chapter.split()), 4200)
        self.assertEqual(
            re.findall(r"(?m)^### ([IVX]+)\. ", self.prose),
            ["I", "II", "III", "IV", "V"]
        )
        self.assertNotIn("## Week Thirteen", self.prose)
        self.assertIn("The printer's shop", self.prose)
        self.assertIn("The second printing", self.prose)

    def test_singer_consent_and_independent_refusal(self):
        for phrase in ("I told you no", "I will not sing your performance",
                       "You never had it", "She named no destination"):
            self.assertIn(phrase, self.prose)
        self.assertNotIn("She agreed to perform at the shelter", self.prose)

    def test_press_correction_does_not_pretend_recall(self):
        self.assertIn("no performance was contracted", self.prose.lower())
        self.assertIn("purchases could be returned", self.prose.lower())
        self.assertIn("A correction to a sheet could not know everyone", self.prose)
        self.assertIn("no shelter authority had consented", self.prose)

    def test_apprentices_have_independent_wage_agency(self):
        self.assertIn("The apprentices discussed it among themselves", self.prose)
        self.assertIn("They agreed to the resetting fee", self.prose)
        self.assertIn("He had not bought the paper", self.prose)

    def test_exclusive_owner_pov_and_era_firewall(self):
        for token in ("CHAR-JAKE-KALOPER", "PRINCIPAL_CHARACTER", "NONCANON", "HOLD"):
            self.assertIn(token, self.chapter)
        self.assertNotRegex(self.prose, r"(?m)^### (Edrin|Edin|Oren)\b")
        self.assertNotIn("human Jake's actual 2016 motives", self.prose)
        self.assertIn("invented secondary-world candidates", self.chapter)

    def test_missing_claimant_not_assigned_unauthorized_ink_name(self):
        self.assertIn("not the woman's private chest", self.prose)
        self.assertIn("unopened sealed message", self.prose)
        self.assertIn("unidentified claimant", self.prose)
        self.assertNotIn("the name belonged to the missing claimant", self.prose.lower())

    def test_prior_chapters_and_source_blobs_unchanged(self):
        for i in range(5):
            with self.subTest(path=NAMES[i]):
                self.assertEqual(blob(BASE / NAMES[i]), BLOBS[i])

    def test_exact_six_full_chapter_assembly_and_manifest(self):
        self.assertEqual(len(self.sections), 6)
        self.assertEqual([m.group("name") for m in self.sections], NAMES)
        for idx, match in enumerate(self.sections):
            with self.subTest(file=NAMES[idx]):
                self.assertEqual(match.group("sha"), BLOBS[idx])
                self.assertEqual(blob(BASE / NAMES[idx]), BLOBS[idx])
                self.assertEqual(match.group("body"), (BASE / NAMES[idx]).read_text(encoding="utf-8").rstrip())
                self.assertIn("| `" + NAMES[idx] + "` | `" + BLOBS[idx] + "` |", self.reader)

    def test_reader_substantial_and_all_release_holds_explicit(self):
        self.assertGreaterEqual(len(self.reader.split()), 26000)
        self.assertIn("Chapters I–VI (NONCANON)", self.reader)
        self.assertIn("independent Authors Council/Umpire review", self.reader)
        self.assertIn("Founder-only canon/publication", self.reader)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL"), 6)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL"), 6)
        self.assertIn("<!-- END_CAUSAL_READING_COPY -->", self.reader)
        self.assertTrue(all("living-novel/manuscript/" not in name for name in NAMES))

if __name__ == "__main__":
    unittest.main()
