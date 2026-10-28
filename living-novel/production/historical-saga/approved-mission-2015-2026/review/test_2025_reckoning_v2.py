"""Fail-closed, scoped 2025 historical reading candidate regression.

Only validates repository transcribed results, candidate assembly and owner firewall.
It does NOT establish raw owner identity, historical venue or literary/Umpire approval.
"""
from __future__ import annotations
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "SCHEMIN_26_PROJECT_MISSION.md").exists())
BASE = ROOT / "living-novel/production/historical-saga/approved-mission-2015-2026/manuscript/2025-reckoning"
SOURCE = ROOT / "living-novel/history/PLAYOFF_MATCHUP_EVIDENCE_2022_2025.json"
ORIGINAL = BASE / "THE_PLACE_LEFT_EMPTY.md"
INSERT = BASE / "THE_STANDARD_HE_WOULD_NOT_BURN_PITTS_NONCANON.md"
ASSEMBLED = BASE / "THE_PLACE_LEFT_EMPTY_EXPANDED_V2_NONCANON.md"
HARD_CH1 = ROOT / "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md"
HARD_CH1_BLOB_SHA = "26a17f05eb0565e7648c29add03ee9580ec933c3"
REQUIRED_POVS = ["Jake", "Austin", "Phillip", "Jake", "Austin", "Jake", "Austin", "Jake"]
REQUIRED_IDS = ("HIST-2025-SEMIFINAL-1", "HIST-2025-SEMIFINAL-2", "HIST-2025-CHAMPIONSHIP-1")


def sections(document: str):
    parts = re.split(r"(?=^## [IVX]+\\. )", document, flags=re.M)
    found = []
    for part in parts:
        if part.startswith("## "):
            heading, _, body = part.partition("\n")
            found.append((heading, body.strip()))
    return found


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()


class Historical2025PittsV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = ORIGINAL.read_text()
        cls.insert = INSERT.read_text()
        cls.assembled = ASSEMBLED.read_text()
        cls.old_parts = sections(cls.original)
        cls.new_parts = sections(cls.assembled)
        cls.events = {e["id"]: e for e in json.loads(SOURCE.read_text())["matchups"]}

    def test_eight_owner_scenes_in_order(self):
        self.assertEqual(len(self.new_parts), 8)
        ids = [re.match(r"^## ([IVX]+)\\.", h).group(1) for h, _ in self.new_parts]
        self.assertEqual(ids, ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"])
        povs = [h.rsplit(" — ", 1)[-1] for h, _ in self.new_parts]
        self.assertEqual(povs, REQUIRED_POVS)

    def test_exact_seven_original_scene_bodies_preserved(self):
        self.assertEqual(len(self.old_parts), 7)
        for i, (_, body) in enumerate(self.old_parts):
            with self.subTest(scene=i + 1):
                self.assertEqual(body, self.new_parts[i if i < 2 else i + 1][1])

    def test_new_pitts_prose_is_exact_insert(self):
        self.assertIn("\n---\n", self.insert)
        standalone = self.insert.split("\n---\n", 1)[1].strip()
        self.assertEqual(standalone, self.new_parts[2][1])
        self.assertGreaterEqual(len(standalone.split()), 2300)

    def test_all_result_records_match_source_transcription(self):
        expect = {
            "HIST-2025-SEMIFINAL-1": ("ObiWan Jacoby", 174.38, "Three Dreaded Snake", 153.20),
            "HIST-2025-SEMIFINAL-2": ("The Immortal", 152.20, "Dr. Duckhook", 151.80),
            "HIST-2025-CHAMPIONSHIP-1": ("The Immortal", 161.07, "ObiWan Jacoby", 109.56),
        }
        for key in REQUIRED_IDS:
            with self.subTest(key=key):
                row = self.events[key]
                winner, high, loser, low = expect[key]
                self.assertEqual(row["season"], 2025)
                self.assertEqual(row["winner"], winner)
                self.assertEqual(float(row["winner_score"]), high)
                self.assertEqual(row["loser"], loser)
                self.assertEqual(float(row["loser_score"]), low)
                for point in (high, low):
                    self.assertIn(f"{point:.2f}", self.assembled)

    def test_knowledge_cutoff_and_no_retired_pov(self):
        self.assertNotRegex(self.new_parts[2][1], r"\\b(?:161\\.07|109\\.56)\\b")
        self.assertNotRegex(self.assembled, r"\\b(?:Edrin|Edin|Master Oren)\\b")
        self.assertNotRegex(self.assembled, r"^## [IVX]+\\..*— (?:El Niño|Manning)\\s*$")

    def test_protected_hard_chapter_blob_unchanged(self):
        self.assertEqual(git_blob_sha(HARD_CH1.read_bytes()), HARD_CH1_BLOB_SHA)

    def test_release_and_binding_holds_preserved(self):
        frontmatter = self.assembled.split("\n---\n", 1)[0]
        self.assertIn("NONCANON", frontmatter)
        self.assertIn("UNKNOWN", frontmatter)
        self.assertIn("venue", frontmatter)
        self.assertIn("remain proposed", frontmatter)
        self.assertGreaterEqual(len(self.assembled.split()), 7000)


if __name__ == "__main__":
    unittest.main()
