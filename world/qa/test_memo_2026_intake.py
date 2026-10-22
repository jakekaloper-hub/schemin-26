import copy
import unittest
from world.qa.validate_memo_2026_intake import validate
class IntakeTests(unittest.TestCase):
 def test_intake_is_consistent_and_noncanonical(self):
  self.assertEqual(validate(),[])
 def test_strict_requires_real_archived_pdf_bytes(self):
  self.assertEqual(validate(require_pdf_bytes=True),[])
if __name__=="__main__":unittest.main()
