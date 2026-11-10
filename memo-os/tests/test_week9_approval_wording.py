from pathlib import Path
import json
import unittest
W=Path(__file__).resolve().parents[2]/'memo-os/week-9'
class ApprovalWordingTests(unittest.TestCase):
    def test_digit_alias_and_markdown_eof(self):
        a=json.loads((W/'WEEK_9_FINAL_APPROVAL_FOLIOS_2026-11-10.json').read_text())
        f={x['page_id']:x for x in a['folios']}
        self.assertIn('D0nkey K0ng',f['W09-P35']['copy']['deck'])
        self.assertIn('D0nkey K0ng',f['W09-P26']['copy']['deck'])
        self.assertNotIn('D 0 nkey',json.dumps(a['folios']))
        text=(W/'WEEK_9_FINAL_APPROVAL_FOLIOS_2026-11-10.md').read_text()
        self.assertTrue(text.endswith('\n'))
        self.assertFalse(text.endswith('\n\n'))
if __name__=='__main__':
    unittest.main()
