import importlib.util
from pathlib import Path
import unittest

path=Path(__file__).resolve().parents[2]/'scripts/build-observer-site.py'
spec=importlib.util.spec_from_file_location('site_link',path) if path.exists() else None
module=importlib.util.module_from_spec(spec) if spec else None
if module: spec.loader.exec_module(module)

class SiteLinkTests(unittest.TestCase):
    def test_private_world_entry_is_added_to_the_existing_navigation(self):
        self.assertIsNotNone(module, 'existing-site integration helper is required')
        html='<nav id="navigation"><a href="#home">Home</a></nav><main></main>'
        result=module.link_observer(html)
        self.assertIn('href="observer.html"',result)
        self.assertIn('World preview',result)
        self.assertIn('<a href="#home">Home</a>',result)
        self.assertTrue(result.endswith('<main></main>'))
    def test_integration_is_idempotent(self):
        self.assertIsNotNone(module)
        html='<nav id="navigation"></nav>'
        once=module.link_observer(html)
        self.assertEqual(module.link_observer(once),once)
    def test_missing_navigation_is_an_error_not_a_silent_broken_link(self):
        self.assertIsNotNone(module)
        with self.assertRaises(ValueError):module.link_observer('<main></main>')

if __name__=='__main__':unittest.main()
