"""Deterministic guard for the NONCANON Chapter I causal revision V3.

The test checks structural/provenance contracts, not literary acceptance, world
location signoff, actual ESPN freshness, or real owner intentions.
"""
import hashlib
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FOLDER = ROOT / "living-novel/production/full-rewrite-2026/2026-10-28-causal-cut"
MANUSCRIPT = FOLDER / "CHAPTER_I_THE_FIRST_ANSWER_CAUSAL_READING_CANDIDATE_V3.md"
SCENE_II = FOLDER / "CHAPTER_I_CAUSAL_CUT_PART_II_REVISED_V3_NONCANON.md"
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
EXPECTED_POVS = [
    "CHAR-JAKE-KALOPER", "CHAR-BEN-WHIPPLE",
    "CHAR-AUSTIN-BYARS", "CHAR-JAKE-KALOPER",
]
HEADER = re.compile(r"(?m)^## (I|II|III|IV)\\. ([^\\n]+)$")

def read(path):
    return path.read_text(encoding="utf-8")

def scenes(text):
    hits = list(HEADER.finditer(text))
    if [h.group(1) for h in hits] != ["I", "II", "III", "IV"]:
        raise AssertionError("V3 requires exactly four Roman-numbered causal scenes")
    return [
        text[h.start() : hits[i + 1].start() if i < 3 else len(text)].strip()
        for i, h in enumerate(hits)
    ]

def owner_gate():
    spec = importlib.util.spec_from_file_location("twelve_owner_rewrite_gate_v3", GATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class ChapterICausalCutV3Tests(unittest.TestCase):
    def test_original_hard_canon_byte_guard(self):
        raw = CANON.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()
        self.assertEqual(blob, CANON_BLOB_SHA)

    def test_fused_scores_and_belt_succession(self):
        text, audit = read(MANUSCRIPT), read(AUDIT)
        for pair in PAIRS:
            self.assertIn(pair, audit)
            left, right = re.findall(r"\\d+\\.\\d+", pair)
            self.assertIn(left, text)
            self.assertIn(right, text)
        self.assertIn("No transfer of succession", text)
        self.assertIn("Belt belonged", text)
        self.assertNotRegex(text, r"(?i)Jake.{0,48}(?:wears|wore|carried|received) the (?:championship )?Belt")
        self.assertIn("**NONCANON", text)

    def test_scene_replacement_is_exact_and_substantive(self):
        candidate = read(MANUSCRIPT)
        components = scenes(candidate)
        self.assertIn(read(SCENE_II).strip(), components[1])
        self.assertIn("the broken peg", components[1])
        self.assertIn("road office", components[1])
        self.assertGreater(len(components[1].split()), 1500)
        self.assertGreater(len(candidate.split()), 4800)

    def test_owner_only_gate_and_negative_protection(self):
        gate = owner_gate()
        for section, owner_id in zip(scenes(read(MANUSCRIPT)), EXPECTED_POVS):
            packet = {
                "pov_character_id": owner_id,
                "pov_class": "PRINCIPAL_CHARACTER",
                "source_event_ids": [
                    "living-novel/os/adapters/flaim/PRO_SCHEMIN_SOURCE_FUSION_AUDIT_W1_W2_V1.md#Week-1"
                ],
                "world_context_id": "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md",
                "story_time_cutoff": "AFTER_2026_W1_CERTIFICATION_BEFORE_W2_RESULT",
                "real_owner_boundary_note": "Imagined motivations belong to fictional characters only",
                "manuscript_text": section,
            }
            self.assertEqual(gate.validate_rewrite_scene(packet), [])
            adversarial = dict(packet, pov_character_id="CHAR-EDRIN-VALE")
            self.assertIn("NON_OWNER_POV_FORBIDDEN", gate.validate_rewrite_scene(adversarial))
        self.assertNotRegex(read(MANUSCRIPT), r"(?i)\\b(?:Edrin|Edin|Master Oren)\\b")

if __name__ == "__main__":
    unittest.main()
