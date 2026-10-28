"""Deterministic noncanonical Chapter I V5 source, structure and provenance checks.

This suite cannot certify artistic quality, independent review, Atlas clearance,
current ESPN freshness or Founder-approved canon promotion.
"""
from pathlib import Path
import hashlib
import importlib.util
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "living-novel/production/full-rewrite-2026/2026-10-28-causal-cut"
V4 = P / "CHAPTER_I_THE_FIRST_ANSWER_CAUSAL_READING_CANDIDATE_V4.md"
V5 = P / "CHAPTER_I_THE_FIRST_ANSWER_CAUSAL_READING_CANDIDATE_V5.md"
PART_V = P / "CHAPTER_I_CAUSAL_CUT_PART_V_REVISED_V5_NONCANON.md"
ORIGINAL = ROOT / "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md"
AUDIT = ROOT / "living-novel/os/adapters/flaim/PRO_SCHEMIN_SOURCE_FUSION_AUDIT_W1_W2_V1.md"
GATE = ROOT / "living-novel/os/qa/twelve_owner_rewrite_gate.py"
PROTECTED_SHA = "26a17f05eb0565e7648c29add03ee9580ec933c3"
PAIR_ANCHORS = [
    ("125.36", "120.86"), ("147.32", "145.82"),
    ("142.70", "134.96"), ("175.56", "144.42"),
    ("198.00", "122.01"), ("141.70", "131.26"),
]
IDS = [
    "CHAR-JAKE-KALOPER", "CHAR-BEN-WHIPPLE", "CHAR-AUSTIN-BYARS",
    "CHAR-BEN-WHIPPLE", "CHAR-JAKE-KALOPER",
]
HEADER = re.compile(r"(?m)^## ([IVX]+)\. ([^\n]+)$")


def sections(s):
    marks = list(HEADER.finditer(s))
    assert [m.group(1) for m in marks] == ["I", "II", "III", "IV", "V"]
    return [
        s[m.start(): marks[i + 1].start() if i + 1 < len(marks) else len(s)].strip()
        for i, m in enumerate(marks)
    ]


def load_gate():
    spec = importlib.util.spec_from_file_location("twelve_owner_gate_ch1v5", GATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ChapterICausalCutV5Tests(unittest.TestCase):
    def test_protected_original_and_fused_source_still_match(self):
        raw = ORIGINAL.read_bytes()
        git_blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        self.assertEqual(git_blob, PROTECTED_SHA)
        audit = AUDIT.read_text(encoding="utf-8")
        chapter = V5.read_text(encoding="utf-8")
        self.assertIn("NONCANON", chapter)
        for left, right in PAIR_ANCHORS:
            self.assertIn(left, chapter)
            self.assertIn(right, chapter)
            self.assertIn(left, audit)
            self.assertIn(right, audit)
        self.assertIn("Belt belonged", chapter)
        self.assertNotRegex(chapter, r"(?i)Jake.{0,48}(?:wears|wore|carried|received) the (?:championship )?Belt")

    def test_v5_is_continuous_and_v4_scenes_one_to_four_are_retained(self):
        old = sections(V4.read_text(encoding="utf-8"))
        new = sections(V5.read_text(encoding="utf-8"))
        self.assertEqual(old[:4], new[:4], "Reopen first four scenes explicitly if editing")
        self.assertEqual(len(new), 5)
        self.assertIn("The Position That Stayed Empty", new[4].splitlines()[0])
        self.assertGreater(len(new[4].split()), 2200)
        self.assertGreater(len(V5.read_text(encoding="utf-8").split()), 7000)
        self.assertIn("Three days after the results were certified", new[3])
        self.assertIn("On the third evening after certification", new[4])
        standalone = PART_V.read_text(encoding="utf-8")
        self.assertIn(standalone[standalone.index("## V."):standalone.index("**Status:**")].strip(), new[4])

    def test_revised_closure_has_real_choice_not_just_interpretation(self):
        end = sections(V5.read_text(encoding="utf-8"))[-1]
        for anchor in [
            "Tell them to let the wagons through.",
            "The open strip of bridge began to function again.",
            "Put down that the reserve was available",
            "At the next rehearsal, test the reserve signal",
            "That question doesn't have a number yet.",
            "SIGNIFICANCE",
        ]:
            self.assertIn(anchor, end)
        self.assertNotIn("## V. The Empty Space", end)

    def test_exclusive_principal_pov_and_negative_case(self):
        validator = load_gate()
        chapter = V5.read_text(encoding="utf-8")
        self.assertNotRegex(chapter, r"(?i)\b(?:Edrin|Edin|Master Oren)\b")
        for scene, character in zip(sections(chapter), IDS):
            packet = {
                "pov_character_id": character,
                "pov_class": "PRINCIPAL_CHARACTER",
                "source_event_ids": [
                    "living-novel/os/adapters/flaim/PRO_SCHEMIN_SOURCE_FUSION_AUDIT_W1_W2_V1.md#Week-1"
                ],
                "world_context_id": "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md",
                "story_time_cutoff": "AFTER_2026_W1_CERTIFICATION_BEFORE_W2_RESULT",
                "real_owner_boundary_note": "Private motives belong only to fantasy characters",
                "manuscript_text": scene,
            }
            self.assertEqual(validator.validate_rewrite_scene(packet), [])
            invalid = dict(packet, pov_character_id="CHAR-EDRIN-VALE")
            self.assertIn("NON_OWNER_POV_FORBIDDEN", validator.validate_rewrite_scene(invalid))


if __name__ == "__main__":
    unittest.main()
