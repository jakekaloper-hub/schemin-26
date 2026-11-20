"""Twelve-owner 2025 noncanonical reading copy: byte provenance and negative guards.

This suite does NOT authenticate historical human owners, approve period visual
anatomy, test hydrology, certify literary quality or substitute for Umpire review.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
READER = BASE / "READING_COPY_2025_TWELVE_VOICES_NONCANON.md"
PREVIOUS = BASE / "READING_COPY_2025_ELEVEN_VOICES_NONCANON.md"
PREVIOUS_BLOB = "d3cd39a5ffc79bd7d728f35615c1bc155718d161"
CHAPTER = BASE / "THE_WEATHER_THAT_WOULD_NOT_PROMISE_MANNING_2025_NONCANON.md"
CHAPTER_BLOB = "7661cad6a12fd53bbda30faae82809cdee5f7b09"
EVIDENCE = ROOT / "living-novel/historical-chronicle/evidence/2025_FLAIM_TEAM_SLOT_AND_PODIUM_READBACK_2026-11-01_REVIEW_ONLY.md"
PRIOR_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
PRIOR_2016_BLOB = "8f1dda21ac4962143ba3291cef4d60769197d62f"
OTHER_SOURCE = ROOT / "living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md"
WRAPPER = re.compile(r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->")
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def gitblob(path):
    body = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(body)).encode() + b"\x00" + body).hexdigest()

def source_path(filename):
    if filename == OTHER_SOURCE.name:
        return OTHER_SOURCE
    return BASE / filename

class TwelveVoiceReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = READER.read_text(encoding="utf-8")
        cls.previous = PREVIOUS.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE.read_text(encoding="utf-8")
        cls.parts = list(WRAPPER.finditer(cls.reader))
        cls.old_parts = list(WRAPPER.finditer(cls.previous))
        cls.scene = cls.chapter.split("\n---\n\n### Source, causality, and continuity handoff")[0]

    def test_01_twelve_source_wrappers(self):
        self.assertEqual(len(self.parts), 12)

    def test_02_unchanged_eleven_voice_reader(self):
        self.assertEqual(gitblob(PREVIOUS), PREVIOUS_BLOB)

    def test_03_prior_eleven_embedded_sources_unchanged(self):
        self.assertEqual(len(self.old_parts), 11)
        for i in range(11):
            with self.subTest(i=i):
                self.assertEqual(self.parts[i].group(0), self.old_parts[i].group(0))

    def test_04_chapter_git_blob(self):
        self.assertEqual(gitblob(CHAPTER), CHAPTER_BLOB)

    def test_05_chapter_embedded_exact(self):
        final = self.parts[-1]
        self.assertEqual(final.group(1), CHAPTER.name)
        self.assertEqual(final.group(2), CHAPTER_BLOB)
        self.assertEqual(final.group(3), self.chapter.rstrip("\n"))
        self.assertEqual(final.group(4), CHAPTER.name)

    def test_06_all_previous_source_blobs_and_bodies(self):
        for part in self.parts[:11]:
            with self.subTest(file=part.group(1)):
                source = source_path(part.group(1))
                self.assertEqual(gitblob(source), part.group(2))
                self.assertEqual(source.read_text(encoding="utf-8").rstrip("\n"), part.group(3))

    def test_07_twelve_ordered_manifest_rows(self):
        manifest = self.reader.split("## Source-exact manifest\n", 1)[1].split("\n---\n", 1)[0]
        self.assertEqual(re.findall(r"^\| (\d+) \|", manifest, re.M),
                         [str(i) for i in range(1, 13)])

    def test_08_new_chapter_word_count(self):
        self.assertEqual(len(self.chapter.split()), 6222)

    def test_09_all_original_source_word_count(self):
        total = sum(len(source_path(p.group(1)).read_text(encoding="utf-8").split())
                    for p in self.parts)
        self.assertEqual(total, 60485)
        self.assertIn("60485", self.reader)

    def test_10_reader_includes_non_source_wrappers(self):
        self.assertGreater(len(self.reader.split()), 60485)

    def test_11_twelve_distinct_owner_characters(self):
        ids = re.findall(r"^\| \d+ \| [^|]+ / (CHAR-[A-Z-]+) \|",
                         self.reader, re.M)
        self.assertEqual(len(ids), 12)
        self.assertEqual(len(set(ids)), 12)
        registry = (ROOT / "canon/characters/CHARACTER_REGISTRY.yaml").read_text(encoding="utf-8")
        for char_id in ids:
            with self.subTest(char_id=char_id):
                self.assertIn("id: " + char_id, registry)

    def test_12_previous_order_preserved_new_end_marker(self):
        self.assertLess(self.reader.index("## Part 11 — Wilson"),
                        self.reader.index("## Part 12 — Manning"))
        self.assertTrue(self.reader.rstrip().endswith("<!-- END_2025_TWELVE_VOICES_NONCANON -->"))

    def test_13_noncanonical_reader_title(self):
        self.assertIn("Twelve Voices", self.reader.splitlines()[0])
        self.assertIn("DRAFT / NONCANON", self.reader)

    def test_14_substantial_six_movement_scene(self):
        self.assertGreater(len(self.scene.split()), 5000)
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.scene, re.M)), 6)

    def test_15_manning_sole_interior(self):
        self.assertIn("Only the fictional storm-elemental Manning possesses interior access", self.chapter)
        self.assertIn("sole principal viewpoint is fictional Manning Welty", self.chapter)

    def test_16_embodied_singular_weather_not_human(self):
        for phrase in ("singular embodied Weather System", "ocean spray", "electric-blue eyes", "lightning",
                       "not an ordinary human", "not a human wizard"):
            self.assertIn(phrase, self.chapter)

    def test_17_season_slot_facts_source_supported(self):
        self.assertIn("| 9 | El Niño | 4–10 | 12 | missed_playoffs |", self.evidence)
        for phrase in ("team slot 9", "El Niño", "4–10", "finalRank 12", "missed_playoffs"):
            self.assertIn(phrase, self.chapter)

    def test_18_human_owner_authentication_guard(self):
        self.assertIn("does not authenticate Manning", self.chapter)
        self.assertIn("PROVISIONAL FICTIONAL ASSOCIATION", self.chapter)
        self.assertIn("not twelve independently verified historical human owner accounts", self.reader)

    def test_19_no_retired_narrator(self):
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Oren)\b", self.scene))

    def test_20_no_claimed_canon_or_final_approval(self):
        self.assertIn("PERIOD CHARACTER AND ATLAS HOLD", self.chapter)
        self.assertIn("INDEPENDENT", self.chapter)
        self.assertIn("FOUNDER-ONLY", self.chapter)
        for phrase in ("NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(phrase, self.chapter)

    def test_21_empty_ferry_trial_not_passenger_launch(self):
        self.assertIn("The empty ferry entered the channel", self.scene)
        self.assertIn("No person was on board", self.scene)
        self.assertIn("exposes a damaged cleat", self.chapter)

    def test_22_actual_people_rescued_without_full_ferry_recovery(self):
        self.assertIn("Two men stood shaking on the landing", self.scene)
        self.assertIn("The ferry was no longer in view", self.scene)
        self.assertIn("ferry remains missing", self.chapter)

    def test_23_costs_paid_in_material_consequence(self):
        self.assertIn("The salt yard answered", self.scene)
        self.assertIn("Then the brace failed", self.scene)
        self.assertIn("warning link cannot be assumed functional", self.chapter)

    def test_24_road_kinetics_not_automatically_closed(self):
        self.assertIn("Kevin's lost elevated watch remains unrepaired", self.chapter)
        self.assertIn("The sealed signal-glass shipment does not reach", self.chapter)
        self.assertIn("a cracked support", self.chapter)

    def test_25_no_proven_atlas_join_or_meteorology(self):
        self.assertIn("No fixed canonical road, channel, ferry or maritime network", self.chapter)
        self.assertIn("rather than historical meteorology or league records", self.chapter)
        self.assertIn("no meteorological claim about the actual world", self.chapter)

    def test_26_no_future_competition_history(self):
        self.assertIn("No characters know 2026 results", self.chapter)
        self.assertIn("No imagined matchup", self.chapter)

    def test_27_retain_2016_original_reader(self):
        self.assertEqual(gitblob(PRIOR_2016), PRIOR_2016_BLOB)

    def test_28_protected_opening_four_blobs(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(gitblob(ROOT / path), sha)

    def test_29_all_twelve_wrapper_end_names_match(self):
        for match in self.parts:
            with self.subTest(part=match.group(1)):
                self.assertEqual(match.group(1), match.group(4))

    def test_30_no_false_independent_acceptance_claim(self):
        self.assertIn("This author-side handoff is **NOT** independent acceptance", self.chapter)

if __name__ == "__main__":
    unittest.main()
