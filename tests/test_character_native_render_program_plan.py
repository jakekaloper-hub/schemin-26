import importlib.util
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
MODULE=ROOT/"planning"/"character-native-render"/"validate_program_plan.py"

spec=importlib.util.spec_from_file_location("program_plan",MODULE)
program_plan=importlib.util.module_from_spec(spec)
spec.loader.exec_module(program_plan)

class CharacterNativeRenderProgramPlanTests(unittest.TestCase):
    def test_plan_is_complete(self):
        self.assertEqual(program_plan.validate(),[])

if __name__=="__main__":
    unittest.main()
