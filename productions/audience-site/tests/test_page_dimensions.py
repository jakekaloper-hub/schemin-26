"""Exercise measured image geometry with real, differently sized source pages."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('catalog_dimensions', Path(__file__).resolve().parents[1] / 'build_public_catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class PageDimensionsTests(unittest.TestCase):
    def test_portrait_landscape_and_rotated_pages_use_rendered_dimensions(self):
        objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
                   b'<< /Type /Pages /Kids [3 0 R 4 0 R 5 0 R] /Count 3 >>']
        for width, height, rotation in [(200, 300, 0), (400, 200, 0), (400, 200, 90)]:
            objects.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] /Rotate {rotation} /Resources << >> >>'.encode())
        pdf = bytearray(b'%PDF-1.4\n'); offsets = [0]
        for number, obj in enumerate(objects, 1):
            offsets.append(len(pdf)); pdf.extend(f'{number} 0 obj\n'.encode() + obj + b'\nendobj\n')
        xref = len(pdf)
        pdf.extend(f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode())
        for offset in offsets[1:]:
            pdf.extend(f'{offset:010d} 00000 n \n'.encode())
        pdf.extend(f'trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'varying.pdf'; source.write_bytes(pdf)
            for number, expected in enumerate([(800, 1200), (1200, 600), (600, 1200)], 1):
                target = Path(temp) / f'{number}.jpg'
                catalog.render_pdf_page(source, number, target, scale=1200)
                self.assertEqual(catalog.jpeg_dimensions(target), dict(zip(('width', 'height'), expected)))

    def test_invalid_or_truncated_images_cannot_supply_layout_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'broken.jpg'
            for data in (b'not jpeg', b'\xff\xd8\xff\xc0\x00\x08\x08', b'\xff\xd8\xff\xda'):
                with self.subTest(data=data):
                    path.write_bytes(data)
                    with self.assertRaises(ValueError):
                        catalog.jpeg_dimensions(path)
