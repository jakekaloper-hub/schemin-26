"""Deterministic, NONCANON Chapter I V4 chronology and source contract.

Passing tests cannot certify literary quality, current ESPN freshness, Atlas
location clearance, an independent Umpire ruling, or Founder canon promotion.
"""
import hashlib
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FOLDER = ROOT / "living-novel/production/full-rewrite-2026/2026-10-28-causal-cut"
MANUSCRIPT = FOLDER / "CHAPTER_I_THE_FIRST_ANSWER_CAUSAL_READING_CANDIDATE_V4.md"
AUSTIN_SCENE = FOLDER / "CHAPTER_I_CAUSAL_CUT_PART_III_AUSTIN_REVISED_V4_NONCANON.md"
CANON = ROOT / "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md"
AUDIT = ROOT / "living-novel/os/adapters/flaim/PRO_SCHEMIN_SOURCE_FUSION_AUDIT_W1_W2_V1.md"
GATE = ROOT / "living-novel/os/qa/twelve_owner_rewrite_gate.py"
CANON_BLOB_SHA = "26a17f05eb0565e7648c29add03ee9580ec933c3"
PAIRS = [
    "Mud Dogs 125.36–120.86 Red Leopards",
    "Dr. Duckhook 147.32–145.82 Seven Deadly Chins",
    "D0nkey K0ng 142.70–134.96 Slob on my Dobb",
    "Three Dreaded Snake 175.56–144.42 El Niño",
    "Chili Cheesers 198.00–122.01 The LLC",
    "ObiWan Jacoby 141.70–131.26 His Majesty's Blood",
]
POVS = [
    "CHAR-JAKE-KALOPER", "CHAR-BEN-WHIPPLE",
    "CHAR-AUSTIN-BYARS", "CHAR-BEN-WHIPPLE", "CHAR-JAKE-KALOPER",
]
HEADER = re.compile(r"(?m)^## (I|II|III|IV|V)\. ([^\n]+)$")

def read(path):
    return path.read_text(encoding="utf-8")

def scenes(text):
    marks = list(HEADER.finditer(text))
    if [m.group(1) for m in marks] != ["I", "II", "III", "IV", "V"]:
        raise AssertionError("Five ordered principal POV scenes required")
    return [
        text[m.start():marks[i+1].start() if i+1 < len(marks) else len(text)].strip()
        for i, m in enumerate(marks)
    ]

def gate():
    spec = importlib.util.spec_from_file_location("twelve_owner_rewrite_gate_v4", GATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class ChapterICausalCutV4Tests(unittest.TestCase):
    def test_protected_chapter_i_git_blob_exact(self):
        raw = CANON.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()
        self.assertEqual(digest, CANON_BLOB_SHA)

    def test_fused_score_pairs_and_succession_guard(self):
        chapter, audit = read(MANUSCRIPT), read(AUDIT)
        for pair in PAIRS:
            self.assertIn(pair, audit)
            left, right = re.findall(r"\d+\.\d+", pair)
            self.assertIn(left, chapter)
            self.assertIn(right, chapter)
        self.assertIn("No transfer of succession", chapter)
        self.assertIn("Belt belonged", chapter)
        self.assertIn("NONCANON", chapter)
        self.assertNotRegex(chapter, r"(?i)Jake.{0,48}(?:wears|wore|carried|received) the (?:championship )?Belt")

    def test_five_scene_chronology_and_substantive_edit(self):
        chapter = read(MANUSCRIPT)
        parts = scenes(chapter)
        self.assertGreater(len(chapter.split()), 5800)
        self.assertGreater(len(parts[2].split()), 1500)
        self.assertGreater(len(parts[3].split()), 1100)
        self.assertIn("Three days after the results were certified", parts[3])
        self.assertIn("On the third evening after certification", parts[4])
        self.assertNotIn("Three days after the results were certified", parts[1])
        self.assertIn("The public-notices", chapter.lower().replace("public notices","public-notices"))
        # The standalone Austin scene is incorporated, with frontmatter excluded.
        standalone = read(AUSTIN_SCENE)
        start = standalone.index("## III.")
        end = standalone.rfind("**Status:**")
        self.assertIn(standalone[start:end].strip(), parts[2])
        self.assertIn("The numbers are right", parts[2])
        self.assertIn("I owe you an apology", parts[2])

    def test_owner_only_and_negative_cases(self):
        validator = gate()
        for part, owner in zip(scenes(read(MANUSCRIPT)), POVS):
            packet = {
                "pov_character_id": owner,
                "pov_class": "PRINCIPAL_CHARACTER",
                "source_event_ids": [
                    "living-novel/os/adapters/flaim/PRO_SCHEMIN_SOURCE_FUSION_AUDIT_W1_W2_V1.md#Week-1"
                ],
                "world_context_id": "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md",
                "story_time_cutoff": "AFTER_2026_W1_CERTIFICATION_BEFORE_W2_RESULT",
                "real_owner_boundary_note": "All imagined motives belong solely to fictional characters",
                "manuscript_text": part,
            }
            self.assertEqual(validator.validate_rewrite_scene(packet), [])
            invalid = dict(packet, pov_character_id="CHAR-EDRIN-VALE")
            self.assertIn("NON_OWNER_POV_FORBIDDEN", validator.validate_rewrite_scene(invalid))
        self.assertNotRegex(read(MANUSCRIPT), r"(?i)\b(?:Edrin|Edin|Master Oren)\b")

if __name__ == "__main__":
    unittest.main()
