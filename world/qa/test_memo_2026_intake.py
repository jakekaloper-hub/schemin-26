import copy
import unittest
from world.qa.validate_memo_2026_intake import validate
class IntakeTests(unittest.TestCase):
 def test_intake_is_consistent_and_noncanonical(self):
  self.assertEqual(validate(),[])
 def test_strict_requires_real_archived_pdf_bytes(self):
  from world.qa.validate_memo_2026_intake import ROOT,INDEX
  import json
  files=json.loads(INDEX.read_text())["files"]
  unresolved=[f"UNRESOLVED_LFS_POINTER_{f['week']}" for f in files if (ROOT/f["archive_path"]).read_bytes().startswith(b"version https://git-lfs.github.com/spec/v1\n")]
  self.assertEqual(validate(require_pdf_bytes=True),sorted(unresolved))
if __name__=="__main__":unittest.main()
