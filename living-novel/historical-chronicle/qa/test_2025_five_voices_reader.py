"""Technical integrity for source-exact 2025 five-owner companion, NONCANON.

This suite does not prove independent author acceptance, connected historical
manager-account identity, Atlas geography, Umpire review or Founder approval.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
READER = BASE / "READING_COPY_2025_FIVE_VOICES_NONCANON.md"
READER_SHA = "e6bb7db5d9293f846a2a3149f32ca1d9905d366a"
SOURCES = (
    ("living-novel/historical-chronicle/seasons/2025/causal-novel/THE_NARROWEST_DOOR_AUSTIN_2025_NONCANON.md", "ae5d50aca6c1ac4da20fb8ead28554baa5e70613", "CHAR-AUSTIN-BYARS", 5001),
    ("living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md", "9737fa9b9832de847ee504ed9b87d5e2c404e481", "CHAR-JAKE-KALOPER", 983),
    ("living-novel/historical-chronicle/seasons/2025/causal-novel/THE_COURSE_BENEATH_THE_COURSE_ZACH_2025_NONCANON.md", "112b3890173cbf11879b139bff966cdff83884d4", "CHAR-ZACH-WILSON", 5310),
    ("living-novel/historical-chronicle/seasons/2025/causal-novel/THE_MASKS_THAT_REMAINED_PHILLIP_2025_NONCANON.md", "f96832d3bd23840d2fb1853d17940ac54774531d", "CHAR-PHILLIP-PITTS", 4777),
    ("living-novel/historical-chronicle/seasons/2025/causal-novel/THE_SIXTH_PLACE_AT_THE_TABLE_BEN_2025_NONCANON.md", "54b6b5f89ae5e33bb05de002fa57b05f9774618b", "CHAR-BEN-WHIPPLE", 4498),
)
OLD_2025 = BASE / "READING_COPY_2025_FOUR_VOICES_NONCANON.md"
OLD_2025_SHA = "d51c78949c6461b78e62f1e408bafd0c3812f793"
OLD_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
OLD_2016_SHA = "8f1dda21ac4962143ba3291cef4d60769197d62f"
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
MANIFEST = re.compile(r"^\| ([1-5]) \| ([^|]+) \| \x60([^\n]+?)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$", re.M)


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


class FiveVoicesReaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = READER.read_text(encoding="utf-8")
        cls.bodies = [(ROOT / p).read_text(encoding="utf-8") for p, _, _, _ in SOURCES]
        cls.ben = cls.bodies[-1]
        cls.wrappers = list(WRAPPER.finditer(cls.text))
        cls.manifest = list(MANIFEST.finditer(cls.text))
        cls.evidence = (
            ROOT / "living-novel/historical-chronicle/evidence/2025_FLAIM_TEAM_SLOT_AND_PODIUM_READBACK_2026-11-01_REVIEW_ONLY.md"
        ).read_text(encoding="utf-8")

    def test_01_pinned_source_blobs(self):
        for p, sha, _, _ in SOURCES:
            with self.subTest(path=p):
                self.assertEqual(git_blob(ROOT / p), sha)

    def test_02_pinned_assembled_reader_blob(self):
        self.assertEqual(git_blob(READER), READER_SHA)

    def test_03_five_source_wrappers(self):
        self.assertEqual(len(self.wrappers), 5)

    def test_04_five_manifest_rows(self):
        self.assertEqual(len(self.manifest), 5)

    def test_05_manifest_path_owner_sha_words(self):
        for index, (p, sha, owner, words) in enumerate(SOURCES):
            row = self.manifest[index]
            self.assertEqual(int(row.group(1)), index + 1)
            self.assertIn(owner, row.group(2))
            self.assertEqual(row.group(3), p)
            self.assertEqual(row.group(4), sha)
            self.assertEqual(int(row.group(5)), words)

    def test_06_all_five_embedded_bodies_source_exact(self):
        for index, (p, sha, _, _) in enumerate(SOURCES):
            marker, manifest_sha, body, end = self.wrappers[index].groups()
            self.assertEqual(marker, Path(p).name)
            self.assertEqual(end, marker)
            self.assertEqual(manifest_sha, sha)
            self.assertEqual(body.strip("\n"), self.bodies[index].rstrip("\n"))

    def test_07_component_counts_are_exact(self):
        self.assertEqual(sum(int(m.group(5)) for m in self.manifest), 20569)
        for body, (_, _, _, count) in zip(self.bodies, SOURCES):
            self.assertEqual(len(body.split()), count)

    def test_08_five_distinct_registered_owner_ids(self):
        self.assertEqual(len({row[2] for row in SOURCES}), 5)
        for _, _, owner, _ in SOURCES:
            self.assertIn(owner, self.text)

    def test_09_ben_substantial(self):
        self.assertGreaterEqual(len(self.ben.split()), 4000)

    def test_10_ben_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.ben, re.M)), 6)

    def test_11_only_ben_owns_fifth_interior(self):
        self.assertIn("sole limited canonical-owner viewpoint", self.ben)
        self.assertIn("no nonowner has interior POV", self.ben)

    def test_12_retired_institutional_pov_not_introduced(self):
        narrative = self.ben.split("\n---\n\n### Source and narrative handoff")[0]
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Master Oren)\b", narrative, re.I))

    def test_13_historical_team_id_and_name_source(self):
        self.assertIn("| 11 | Seven Deadly Chins | 6–8 | 6 | eliminated |", self.evidence)

    def test_14_ben_competitive_anchor_follows_source(self):
        for fact in ("team slot 11", "Seven Deadly Chins", "6–8", "finalRank 6", "postseason eliminated"):
            self.assertIn(fact, self.ben)

    def test_15_missing_manager_identity_explicit(self):
        for phrase in ("manager-account identification remains UNKNOWN", "PROVISIONAL NONCANON FICTIONAL ASSOCIATION"):
            self.assertIn(phrase, self.ben)

    def test_16_no_unverified_score_claim_in_new_narrative(self):
        self.assertIsNone(re.search(r"\b\d{2,3}\.\d{2}\b", self.ben))

    def test_17_no_unapproved_location_claim(self):
        self.assertIn("No approved 2025 Atlas location", self.ben)
        self.assertIn("PROPOSED UNAPPROVED", self.ben)

    def test_18_no_retroactive_props(self):
        self.assertIn("Historical possession of the 2026 hammer, cap, bottle or raccoon companion is not assumed", self.ben)

    def test_19_no_future_results_or_corrupt_belt(self):
        self.assertIn("no knowledge of any 2026 outcome", self.ben)
        self.assertIn("The first place belonged elsewhere, as did the Belt", self.ben)

    def test_20_specific_cost_and_unresolved_rule(self):
        for phrase in ("Four stewards favored the old rule", "Pell still expected payment", "the old serving order stood", "For the moment, he had wood to repay"):
            self.assertIn(phrase, self.ben)

    def test_21_four_voice_reader_still_byte_exact(self):
        self.assertEqual(git_blob(OLD_2025), OLD_2025_SHA)

    def test_22_unified_2016_72_chapters_still_byte_exact(self):
        self.assertEqual(git_blob(OLD_2016), OLD_2016_SHA)

    def test_23_protected_2026_opening_unchanged(self):
        for p, sha in PROTECTED.items():
            with self.subTest(path=p):
                self.assertEqual(git_blob(ROOT / p), sha)

    def test_24_release_and_external_holds_explicit(self):
        for phrase in ("DRAFT / NONCANON", "historical manager-account identity remains UNKNOWN", "No merge, deployment, publication or canon promotion"):
            self.assertIn(phrase, self.text)

    def test_25_reader_five_part_closing_marker(self):
        self.assertTrue(self.text.rstrip().endswith("<!-- END_2025_FIVE_VOICES_NONCANON -->"))


if __name__ == "__main__":
    unittest.main()
