"""2025 thirteen-part, twelve-principal source-exact noncanon reader.

Deterministic integrity guards only, not human-owner authentication,
Atlas/Character approval, editorial acceptance, or Umpire certification.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
NEW = BASE / "READING_COPY_2025_TWELVE_VOICES_THIRTEEN_PARTS_NONCANON.md"
OLD = BASE / "READING_COPY_2025_TWELVE_VOICES_NONCANON.md"
OLD_BLOB = "8c5785bfea6dd48693ad4ff1922396cd2f2a8a84"
CHAPTER = BASE / "THE_MAP_OF_UNPAID_MILES_JAKE_2025_NONCANON.md"
CHAPTER_BLOB = "3821bc1c3a99bcca5b6419e50ebee6e260dc3234"
PILOT = ROOT / "living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md"
PILOT_BLOB = "9737fa9b9832de847ee504ed9b87d5e2c404e481"
EVIDENCE = ROOT / "living-novel/historical-chronicle/evidence/2025_FLAIM_TEAM_SLOT_AND_PODIUM_READBACK_2026-11-01_REVIEW_ONLY.md"
HISTORY = ROOT / "living-novel/history/PLAYOFF_MATCHUP_EVIDENCE_2022_2025.json"
PRIOR_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
PRIOR_2016_BLOB = "8f1dda21ac4962143ba3291cef4d60769197d62f"
WRAPPER = re.compile(r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->")
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(path):
    b = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()

def file_for_source(name):
    return PILOT if name == PILOT.name else BASE / name

class TwelveOwnersThirteenParts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new = NEW.read_text(encoding="utf-8")
        cls.old = OLD.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.pilot = PILOT.read_text(encoding="utf-8")
        cls.parts = list(WRAPPER.finditer(cls.new))
        cls.old_parts = list(WRAPPER.finditer(cls.old))
        cls.scene = cls.chapter.split("\n---\n\n### Source, causality, and continuity handoff")[0]
        cls.evidence = EVIDENCE.read_text(encoding="utf-8")

    def test_01_twelve_owner_thirteen_source_wrappers(self):
        self.assertEqual(len(self.parts), 13)
        self.assertEqual(len(self.old_parts), 12)

    def test_02_previous_reader_exact_blob(self):
        self.assertEqual(blob(OLD), OLD_BLOB)

    def test_03_previous_embedded_parts_exact(self):
        for i in range(12):
            with self.subTest(part=i+1):
                self.assertEqual(self.parts[i].group(0), self.old_parts[i].group(0))

    def test_04_new_chapter_exact_blob(self):
        self.assertEqual(blob(CHAPTER), CHAPTER_BLOB)

    def test_05_new_chapter_exact_wrapper(self):
        p = self.parts[-1]
        self.assertEqual(p.group(1), CHAPTER.name)
        self.assertEqual(p.group(2), CHAPTER_BLOB)
        self.assertEqual(p.group(3), self.chapter.rstrip("\n"))
        self.assertEqual(p.group(4), CHAPTER.name)

    def test_06_every_source_matches_manifest(self):
        for p in self.parts:
            with self.subTest(name=p.group(1)):
                f = file_for_source(p.group(1))
                self.assertEqual(blob(f), p.group(2))
                self.assertEqual(f.read_text(encoding="utf-8").rstrip("\n"), p.group(3))

    def test_07_pilot_preserved(self):
        self.assertEqual(blob(PILOT), PILOT_BLOB)

    def test_08_canonical_opening_preserved(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), sha)

    def test_09_2016_reader_preserved(self):
        self.assertEqual(blob(PRIOR_2016), PRIOR_2016_BLOB)

    def test_10_manifest_orders_thirteen_parts(self):
        manifest = self.new.split("## Source-exact manifest\n",1)[1].split("\n---\n",1)[0]
        self.assertEqual(re.findall(r"^\| (\d+) \|", manifest, re.M), [str(i) for i in range(1,14)])

    def test_11_twelve_exclusive_ids_jake_repeated(self):
        ids = re.findall(r"^\| \d+ \| [^|]+ / (CHAR-[A-Z-]+)", self.new, re.M)
        self.assertEqual(len(ids), 13)
        self.assertEqual(len(set(ids)), 12)
        self.assertEqual(ids.count("CHAR-JAKE-KALOPER"), 2)
        registry = (ROOT / "canon/characters/CHARACTER_REGISTRY.yaml").read_text(encoding="utf-8")
        for id_ in set(ids):
            self.assertIn("id: " + id_, registry)

    def test_12_new_story_substantial_six_movements(self):
        self.assertGreater(len(self.scene.split()), 3800)
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.scene, re.M)), 6)

    def test_13_exact_words_including_metadata(self):
        self.assertEqual(len(self.chapter.split()), 4958)

    def test_14_source_words_total(self):
        self.assertEqual(sum(len(file_for_source(p.group(1)).read_text(encoding="utf-8").split()) for p in self.parts), 65443)
        self.assertIn("65443", self.new)

    def test_15_no_retired_pov_in_scene(self):
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Oren)\b", self.scene))

    def test_16_sole_principal_jake_viewpoint(self):
        self.assertIn("One limited principal viewpoint—fictional Jake", self.chapter)
        self.assertIn("never interior POV", self.chapter)
        self.assertIn("golden retriever", self.chapter)

    def test_17_jake_does_not_reclaim_belt(self):
        self.assertIn("Jake has no championship Belt", self.chapter)
        self.assertIn("Jake neither possesses nor displays a championship Belt", self.chapter)
        self.assertIsNone(re.search(r"(?:wearing|carrying|holding) the (?:championship )?[Bb]elt", self.scene))

    def test_18_verified_2025_slot_not_owner_authentication(self):
        self.assertIn("| 1 | ObiWan Jacoby | 10–4 | 2 | runner_up |", self.evidence)
        self.assertIn("historical manager-account ID remains unavailable", self.chapter)
        self.assertIn("PROVISIONAL FICTIONAL ASSOCIATION", self.chapter)

    def test_19_known_championships_not_new_match_results(self):
        self.assertIn("161.07 to 109.56", self.scene)
        self.assertIn("187.52 to 161.68", self.scene)
        self.assertTrue(HISTORY.is_file())
        self.assertIn("No other league score, matchup, trade", self.chapter)

    def test_20_road_bounded_witness(self):
        self.assertIn("One inspected wagon made one permitted movement", self.scene)
        self.assertIn("A support afterward showed a crack", self.scene)
        self.assertIn("No further passage has been certified", self.scene)

    def test_21_manning_ferry_does_not_reopen(self):
        self.assertIn("a ferry gone from its landing", self.scene)
        self.assertIn("coastal glass stays undelivered", self.chapter)
        self.assertIn("damaged bridge remains uncertified", self.chapter)

    def test_22_real_cost_not_triumphal_shortcut(self):
        for phrase in ("specific flour and lamp oil", "the rest is still owed", "The first-offer right was gone", "both wagons remained behind the yard gate"):
            self.assertIn(phrase, self.scene.lower() if phrase[0].islower() else self.scene)

    def test_23_consortium_decision_unknown(self):
        self.assertIn("has not accepted a public inspection arrangement", self.chapter)
        self.assertIn("That is not a promise that I will win", self.scene)

    def test_24_source_time_and_atlas_firewall(self):
        self.assertIn("not an Atlas-approved geographic road linking sites", self.chapter)
        self.assertIn("not that all sites are adjacent", self.chapter)
        self.assertIn("future 2026 outcome", self.chapter)

    def test_25_no_false_release_or_editorial_green(self):
        for word in ("DRAFT / NONCANON", "INDEPENDENT", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(word, self.chapter)
        self.assertIn("an independent human or Director review", self.chapter)
        self.assertIn("**NOT**", self.chapter)

    def test_26_reader_emphasizes_not_new_owner(self):
        self.assertIn("twelve distinct registered fictional owner-character viewpoints", self.new)
        self.assertIn("Jake returns for Part 13", self.new)

    def test_27_previous_final_wrapper_unchanged(self):
        self.assertEqual(self.parts[11].group(1), "THE_WEATHER_THAT_WOULD_NOT_PROMISE_MANNING_2025_NONCANON.md")

    def test_28_new_reader_final_marker(self):
        self.assertTrue(self.new.rstrip().endswith("<!-- END_2025_TWELVE_VOICES_THIRTEEN_PARTS_NONCANON -->"))

    def test_29_raw_historical_owner_not_invented(self):
        self.assertIn("historical manager-account ID remains unavailable", self.chapter)
        self.assertIn("manager-account", self.chapter)

    def test_30_no_invisible_acceptance(self):
        self.assertIn("INDEPENDENT EDITORIAL AND UMPIRE HOLD", self.chapter)
        self.assertIn("PERIOD ATLAS AND CHARACTER HOLD", self.chapter)

if __name__ == "__main__":
    unittest.main()
