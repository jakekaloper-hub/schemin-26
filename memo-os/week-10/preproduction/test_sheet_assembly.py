import json,tempfile,unittest
from pathlib import Path
from PIL import Image
from assemble_review_sheets import assemble,validate_master
P=Path(__file__).resolve().parent
class AssemblyTests(unittest.TestCase):
 def test_missing_master_rejected(self):
  with self.assertRaises(FileNotFoundError):validate_master(Path('/nonexistent/W10-P01.png'))
 def test_wrong_geometry_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'wrong.png';Image.new('L',(540,960)).save(f)
   with self.assertRaises(ValueError):validate_master(f)
 def test_color_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'color.png';Image.new('RGB',(1080,1920),(4,20,7)).save(f)
   with self.assertRaises(ValueError):validate_master(f)
 def test_exact_scaled_master_pixels_and_empty_slots(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);masters=root/'fixtures';masters.mkdir();manifest=json.loads((P/'render-inputs/manifest.json').read_text())
   for p in manifest['pages']:Image.new('L',(1080,1920),p['reading_position']*6).save(masters/(p['page_id']+'.png'))
   result=assemble(masters,root/'sheets',manifest);self.assertEqual([len(s['inputs']) for s in result['sheets']],[6,6,6,6,6,4]);self.assertTrue(result['masters_unchanged'])
   with Image.open(root/'sheets/W10-SHEET-06.png') as im:
    self.assertEqual(im.getpixel((24+564+100,92+24+1018+100)),(28,28,28))
    self.assertEqual(im.getpixel((24+100,92+24+1018+100)),(204,204,204))
   self.assertEqual(result['sheets'][-1]['empty_slots'],[5,6])
if __name__=='__main__':unittest.main(verbosity=2)
