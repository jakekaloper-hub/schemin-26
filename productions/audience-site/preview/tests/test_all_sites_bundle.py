"""The offline build must actually mount the all-sites factory, not just ship dead code."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('all_site_build',BASE/'build_preview.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
class AllSiteBundleTests(unittest.TestCase):
 def test_offline_bundle_includes_and_passes_the_additive_site_factory(self):
  data={'sourceRevision':'8894ad191cae8b61d05d6f970a5bd97c0e01ef60','stateAsOf':'end_of_week_3_2026','authority':'DERIVED_PRESENTATION_ONLY','publicationAuthorized':False,'locations':[{'id':'LOC-LEAGUE-ARCHIVE'}]}
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'in.json').write_text(json.dumps(data));receipt=b.build(p/'in.json',p/'out.html');html=(p/'out.html').read_text()
  self.assertIn('const AtlasSites=',html)
  self.assertIn('buildAtlasSiteAssets:AtlasSites.buildAtlasSiteAssets',html)
  self.assertIn('atlasSiteIds:AtlasSites.supportedAtlasSiteIds()',html)
  self.assertIn('LOC-LEAGUE-ARCHIVE',html)
  self.assertFalse(receipt['publicationAuthorized'])
  self.assertEqual(receipt['originalJPEGs'],0)
 def test_no_candidate_location_store_is_embedded_in_the_render_bundle(self):
  source=(BASE/'build_preview.py').read_text()
  self.assertNotIn('atlas_location_candidates.json',source)
if __name__=='__main__': unittest.main()
