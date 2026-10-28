import importlib.util,pathlib,unittest
p=pathlib.Path(__file__).resolve().parents[1]/'build_public_catalog.py'
s=importlib.util.spec_from_file_location('site_catalog',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Mentions(unittest.TestCase):
 def test_only_explicit_canonical_names_create_links(self):
  people=[{'id':'a','name':'Mud Dogs','team':'Mud Dogs'},{'id':'b','name':'El Niño','team':'El Niño'}]
  self.assertEqual(m.character_mentions('Mud Dogs withdrew. Rain followed.',people),['a'])
 def test_word_boundaries_prevent_partial_name_matches(self):
  self.assertEqual(m.character_mentions('Mud Dogsville', [{'id':'a','name':'Mud Dogs','team':'Mud Dogs'}]),[])
if __name__=='__main__':unittest.main()
