"""Bounded, deterministic safety checks for NONCANON Chapter I causal cut V2.

This is a structural/provenance guard, not independent editorial acceptance or
a proof of canonical Atlas location IDs. Protected Chapter I remains unchanged.
"""
import hashlib
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CANDIDATE = ROOT / "living-novel/production/full-rewrite-2026/2026-10-28-causal-cut/CHAPTER_I_THE_FIRST_ANSWER_CAUSAL_READING_CANDIDATE_V2.md"
CANON = ROOT / "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md"
AUDIT = ROOT / "living-novel/os/adapters/flaim/PRO_SCHEMIN_SOURCE_FUSION_AUDIT_W1_W2_V1.md"
GATE = ROOT / "living-novel/os/qa/twelve_owner_rewrite_gate.py"
EXPECTED_CANON_GIT_BLOB = "26a17f05eb0565e7648c29add03ee9580ec933c3"
SOURCE_PATH = "living-novel/os/adapters/flaim/PRO_SCHEMIN_SOURCE_FUSION_AUDIT_W1_W2_V1.md#Week-1"
POVS = [
    "CHAR-JAKE-KALOPER",
    "CHAR-BEN-WHIPPLE",
    "CHAR-AUSTIN-BYARS",
    "CHAR-JAKE-KALOPER",
]
PAIRS = [
    ("Mud Dogs 125.36–120.86 Red Leopards", ("125.36", "120.86")),
    ("Dr. Duckhook 147.32–145.82 Seven Deadly Chins", ("147.32", "145.82")),
    ("D0nkey K0ng 142.70–134.96 Slob on my Dobb", ("142.70", "134.96")),
    ("Three Dreaded Snake 175.56–144.42 El Niño", ("175.56", "144.42")),
    ("Chili Cheesers 198.00–122.01 The LLC", ("198.00", "122.01")),
    ("ObiWan Jacoby 141.70–131.26 His Majesty's Blood", ("141.70", "131.26")),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def scene_bodies() -> list[str]:
    text = read(CANDIDATE)
    positions = list(re.finditer(r"(?m)^## (?:I|II|III|IV)\. [^\n]+$", text))
    if len(positions) != 4:
        raise AssertionError(f"expected 4 scene headings; found {len(positions)}")
    return [text[m.start(): positions[i + 1].start() if i + 1 < len(positions) else len(text)].strip()
            for i, m in enumerate(positions)]


def gate():
    spec = importlib.util.spec_from_file_location("twelve_owner_rewrite_gate", GATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ChapterICausalCutV2Tests(unittest.TestCase):
    def test_protected_chapter_i_blob_is_unchanged(self):
        raw = CANON.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        self.assertEqual(blob, EXPECTED_CANON_GIT_BLOB)

    def test_six_source_correlated_scores_retained(self):
        src = read(AUDIT)
        candidate = read(CANDIDATE)
        for exact_source_phrase, nums in PAIRS:
            self.assertIn(exact_source_phrase, src)
            for score in nums:
                self.assertIn(score, candidate)
        self.assertIn("Belt belonged", candidate)
        self.assertIn("No transfer of succession", candidate)

    def test_only_canonical_principal_povs_in_scene_packets(self):
        module = gate()
        for idx, (body, owner_id) in enumerate(zip(scene_bodies(), POVS)):
            packet = {
                "pov_character_id": owner_id,
                "pov_class": "PRINCIPAL_CHARACTER",
                "source_event_ids": [SOURCE_PATH],
                # Existing named Hall setting from protected Chapter I.
                # This is a source-context pointer, NOT an Atlas LOC-ID approval.
                "world_context_id": str(CANON.relative_to(ROOT)),
                "story_time_cutoff": "AFTER_2026_W1_CERTIFICATION_BEFORE_W2_RESULT",
                "real_owner_boundary_note": "Fictional interiority; no real-owner motive claims",
                "manuscript_text": body,
            }
            self.assertEqual(module.validate_rewrite_scene(packet), [], f"scene {idx + 1}")
        self.assertGreater(len(read(CANDIDATE).split()), 3500)

    def test_negative_owner_and_retired_narrator_fail_closed(self):
        module = gate()
        example = {
            "pov_character_id": "CHAR-EDRIN-VALE",
            "pov_class": "PRINCIPAL_CHARACTER",
            "source_event_ids": [SOURCE_PATH],
            "world_context_id": str(CANON.relative_to(ROOT)),
            "story_time_cutoff": "AFTER_2026_W1_CERTIFICATION_BEFORE_W2_RESULT",
            "real_owner_boundary_note": "Fictional interiority",
            "manuscript_text": "A proposed scene, nonempty.",
        }
        self.assertIn("NON_OWNER_POV_FORBIDDEN", module.validate_rewrite_scene(example))
        example["pov_character_id"] = "CHAR-JAKE-KALOPER"
        example["manuscript_text"] = "Master Oren was granted private narration."
        self.assertIn("RETIRED_INSTITUTIONAL_CHARACTER_IN_MANUSCRIPT",
                      module.validate_rewrite_scene(example))


if __name__ == "__main__":
    unittest.main()
