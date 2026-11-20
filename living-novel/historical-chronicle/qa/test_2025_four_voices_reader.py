"""2025 four-owner source-exact companion reader QA — technical integrity only.

Does NOT assert independent Authors Council, historical-owner authentication,
Atlas approval, live ESPN verification, Umpire acceptance, canon or publication.
"""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"

SOURCES = (
    ("living-novel/historical-chronicle/seasons/2025/causal-novel/THE_NARROWEST_DOOR_AUSTIN_2025_NONCANON.md", "ae5d50aca6c1ac4da20fb8ead28554baa5e70613", "CHAR-AUSTIN-BYARS", 5001),
    ("living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md", "9737fa9b9832de847ee504ed9b87d5e2c404e481", "CHAR-JAKE-KALOPER", 983),
    ("living-novel/historical-chronicle/seasons/2025/causal-novel/THE_COURSE_BENEATH_THE_COURSE_ZACH_2025_NONCANON.md", "112b3890173cbf11879b139bff966cdff83884d4", "CHAR-ZACH-WILSON", 5310),
    ("living-novel/historical-chronicle/seasons/2025/causal-novel/THE_MASKS_THAT_REMAINED_PHILLIP_2025_NONCANON.md", "f96832d3bd23840d2fb1853d17940ac54774531d", "CHAR-PHILLIP-PITTS", 4777),
)
READER = BASE / "READING_COPY_2025_FOUR_VOICES_NONCANON.md"
READER_SHA = "d51c78949c6461b78e62f1e408bafd0c3812f793"
PREVIOUS = BASE / "READING_COPY_2025_THREE_VOICES_NONCANON.md"
PREVIOUS_SHA = "c09df3abe7233b2a1eb7edd84274d5550ed759cb"
PREVIOUS_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
PREVIOUS_2016_SHA = "8f1dda21ac4962143ba3291cef4d60769197d62f"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
WRAPPER = re.compile(
    r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n"
    r"([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->"
)
MANIFEST = re.compile(r"^\| ([1-4]) \| ([^|]+) \| \x60([^\n]+?)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$", re.M)


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


class FourVoices2025ReaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = READER.read_text(encoding="utf-8")
        cls.bodies = [(ROOT / path).read_text(encoding="utf-8") for path, _, _, _ in SOURCES]
        cls.phillip = cls.bodies[-1]
        cls.wrappers = list(WRAPPER.finditer(cls.reader))
        cls.manifest = list(MANIFEST.finditer(cls.reader))

    def test_01_sources_are_exact_pinned_blobs(self):
        for path, sha, _, _ in SOURCES:
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_02_reader_is_exact_pinned_blob(self):
        self.assertEqual(git_blob(READER), READER_SHA)

    def test_03_four_wrappers(self):
        self.assertEqual(len(self.wrappers), 4)

    def test_04_four_manifest_entries(self):
        self.assertEqual(len(self.manifest), 4)

    def test_05_each_assembly_body_source_exact(self):
        for i, (path, sha, _, _) in enumerate(SOURCES):
            start, declared_sha, body, end = self.wrappers[i].groups()
            self.assertEqual(start, Path(path).name)
            self.assertEqual(end, Path(path).name)
            self.assertEqual(declared_sha, sha)
            self.assertEqual(body.strip("\n"), self.bodies[i].rstrip("\n"))

    def test_06_manifest_paths_hashes_owners_words(self):
        for i, (path, sha, owner, count) in enumerate(SOURCES):
            row = self.manifest[i]
            self.assertEqual(int(row.group(1)), i + 1)
            self.assertIn(owner, row.group(2))
            self.assertEqual(row.group(3), path)
            self.assertEqual(row.group(4), sha)
            self.assertEqual(int(row.group(5)), count)

    def test_07_phillip_prose_substantial(self):
        self.assertGreater(len(self.phillip.split()), 4500)

    def test_08_six_literary_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.phillip, re.M)), 6)

    def test_09_four_distinct_registered_interior_owners(self):
        self.assertEqual(len({owner for _, _, owner, _ in SOURCES}), 4)
        for _, _, owner, _ in SOURCES:
            self.assertIn(owner, self.reader)

    def test_10_no_restricted_institutional_viewpoint(self):
        narrative = self.phillip.split("\n---\n\n### Source and narrative handoff")[0]
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Master Oren)\b", narrative, re.I))

    def test_11_historical_semifinal_anchor(self):
        self.assertIn("ObiWan Jacoby 174.38 over Three Dreaded Snake 153.20", self.phillip)
        self.assertIn("174.38 to 153.20", self.phillip)
        evidence = json.loads((ROOT / "living-novel/history/PLAYOFF_MATCHUP_EVIDENCE_2022_2025.json").read_text())
        event = next(m for m in evidence["matchups"] if m["id"] == "HIST-2025-SEMIFINAL-1")
        self.assertEqual((event["winner"], event["loser"], event["winner_score"], event["loser_score"]), ("ObiWan Jacoby", "Three Dreaded Snake", 174.38, 153.2))

    def test_12_historical_final_anchor(self):
        self.assertIn("The Immortal 161.07 over ObiWan Jacoby 109.56", self.phillip)
        evidence = json.loads((ROOT / "living-novel/history/PLAYOFF_MATCHUP_EVIDENCE_2022_2025.json").read_text())
        final = next(m for m in evidence["matchups"] if m["id"] == "HIST-2025-CHAMPIONSHIP-1")
        self.assertEqual((final["winner_score"], final["loser_score"]), (161.07, 109.56))

    def test_13_third_place_ledger_anchor(self):
        ledger = (ROOT / "world/history/2025/2025_FACT_LEDGER.md").read_text()
        self.assertIn("Three Dreaded Snake", ledger)
        self.assertIn("finalRank=3", ledger)
        self.assertIn("third-place finish", self.reader)

    def test_14_2023_record_from_character_dossier(self):
        dossier = (ROOT / "living-novel/characters/06_PHILLIP_PITTS.md").read_text()
        self.assertIn("1-13", dossier)
        self.assertIn("10-4", dossier)
        self.assertIn("2023 1–13", self.phillip)

    def test_15_single_serpent_body_guard(self):
        self.assertIn("single three-headed, one-bodied fictional serpent", self.phillip)
        self.assertIn("one shadow cast from a single body", self.phillip)

    def test_16_no_extraneous_espy_claim_or_owner_linkage(self):
        self.assertIn("account binding remains UNKNOWN", self.phillip)
        self.assertIn("not 2025 ESPN facts", self.phillip)
        self.assertIn("no newly verified 2025 alias", self.phillip)

    def test_17_all_new_world_details_remain_proposed(self):
        self.assertIn("PROPOSED_UNAPPROVED", self.phillip)
        self.assertIn("no approved 2025 Atlas location", self.phillip)
        self.assertIn("no land grant", self.phillip)

    def test_18_prose_temporal_boundary(self):
        self.assertIn("Set after the 2025 championship is certified", self.phillip)
        self.assertIn("no 2026 result knowledge", self.phillip)
        self.assertIn("At dawn he would still be third", self.phillip)

    def test_19_dramatic_choice_and_consequence(self):
        for phrase in ("Someone has taken the masks.", "I gave him reason to think so.", "It is not mine to finish.", "The play was performed"):
            self.assertIn(phrase, self.phillip)

    def test_20_old_three_voice_reader_unchanged(self):
        self.assertEqual(git_blob(PREVIOUS), PREVIOUS_SHA)

    def test_21_2016_seventy_two_chapter_reader_unchanged(self):
        self.assertEqual(git_blob(PREVIOUS_2016), PREVIOUS_2016_SHA)

    def test_22_protected_2026_hard_canon_unchanged(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_23_holds_no_canon_promotion(self):
        for term in ("DRAFT / NONCANON", "historical human-owner account mapping remains UNKNOWN",
                     "Founder acceptance remain outstanding", "No merge/publication/canon promotion"):
            self.assertIn(term, self.reader)

    def test_24_reader_has_exact_closing_marker(self):
        self.assertTrue(self.reader.rstrip().endswith("<!-- END_2025_FOUR_VOICES_NONCANON -->"))


if __name__ == "__main__":
    unittest.main()
