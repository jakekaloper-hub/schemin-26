import pathlib
import unittest

from canon.characters.cccp_render_contract import compile_render_contract


ROOT = pathlib.Path(__file__).resolve().parents[3]


class ConsumerEnforcement(unittest.TestCase):
    def test_semantic_render_contract_never_authorizes_generation(self):
        result = compile_render_contract(["Dr. Duckhook"])
        self.assertEqual(result["state"], "GENERATION_BLOCKED")
        self.assertIn("SUBJECT_BINDING", result["reason"])

    def test_novel_character_visual_declares_governed_adapter(self):
        text = (ROOT / "living-novel/os/engine/novel_os.py").read_text()
        self.assertIn('"generation_adapter":"canon/characters/runtime/generation_adapter.py"', text)
        self.assertIn('"generation_eligibility_required":character_bearing', text)

    def test_memo_contract_requires_governed_adapter(self):
        text = (ROOT / "memo-os/CCCP_INTEGRATION_CONTRACT_V1.md").read_text()
        self.assertIn("generation_adapter.py", text)
        self.assertIn("SUBJECT_BINDING", text)
        self.assertIn("GENERATION_ELIGIBLE", text)


if __name__ == "__main__":
    unittest.main()
