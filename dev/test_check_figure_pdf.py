"""Exercise final-size checks on synthetic vector and raster PDF pages."""
import sys
import unittest
from pathlib import Path

try:
    import pymupdf
except ImportError:
    pymupdf = None

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_figure_pdf import inspect


@unittest.skipUnless(pymupdf, "PyMuPDF is optional")
class FigureSizeTests(unittest.TestCase):
    def setUp(self):
        self.document = pymupdf.open()
        self.addCleanup(self.document.close)
        self.page = self.document.new_page(width=144, height=144)

    def test_text_at_two_placement_widths(self):
        self.page.insert_text((10, 20), "Label", fontsize=10)
        self.page.insert_text((10, 40), "OCR", fontsize=3, render_mode=3)
        full = inspect(self.page, 50.8, 10, 300)
        half = inspect(self.page, 25.4, 10, 300)
        self.assertAlmostEqual(full["smallest_measurable_text_pt"], 10)
        self.assertEqual(full["failures"], [])
        self.assertAlmostEqual(half["smallest_measurable_text_pt"], 5)
        self.assertTrue(half["failures"])

    def test_rotated_raster_uses_the_lower_axis_density(self):
        # 200 x 100 pixels at 90 degrees, displayed in a 1 x 1 inch square.
        bitmap = pymupdf.Pixmap(pymupdf.csGRAY, (0, 0, 200, 100), False)
        bitmap.clear_with(127)
        self.page.insert_image((0, 0, 72, 72), pixmap=bitmap, rotate=90,
                               keep_proportion=False)
        result = inspect(self.page, 50.8, 8, 120)
        self.assertAlmostEqual(result["lowest_measurable_raster_dpi"], 100)
        self.assertTrue(result["unmeasured"])
        self.assertTrue(result["failures"])
        smaller = inspect(self.page, 25.4, None, 180)
        self.assertAlmostEqual(smaller["lowest_measurable_raster_dpi"], 200)
        self.assertEqual(smaller["failures"], [])

    def test_outlined_art_requires_visual_text_review(self):
        self.page.draw_rect((10, 10, 50, 80))
        result = inspect(self.page, 50.8, 8, None)
        self.assertIsNone(result["smallest_measurable_text_pt"])
        self.assertTrue(result["unmeasured"])

    def test_vertically_compressed_label_cannot_pass_at_its_nominal_size(self):
        origin = pymupdf.Point(10, 54)
        self.page.insert_text((10, 25), "Normal", fontsize=10)
        self.page.insert_text(origin, "Flattened", fontsize=12,
                              morph=(origin, pymupdf.Matrix(1, 0.3)))
        result = inspect(self.page, 50.8, 9, None)
        self.assertEqual(result["unmeasurable_text_spans"], 1)
        self.assertAlmostEqual(result["smallest_measurable_text_pt"], 10)
        self.assertTrue(result["unmeasured"])

    def test_rotated_cropped_page_uses_visible_objects_only(self):
        self.page.insert_text((108, 45), "edge", fontsize=10)
        self.page.insert_text((5, 16), "outside", fontsize=2)
        bitmap = pymupdf.Pixmap(pymupdf.csGRAY, (0, 0, 3, 3), False)
        bitmap.clear_with(127)
        self.page.insert_image((0, 2, 35, 30), pixmap=bitmap)
        self.page.set_cropbox((40, 32, 140, 92))
        self.page.set_rotation(90)
        result = inspect(self.page, 60 * 25.4 / 72, 9, 300)
        self.assertEqual(result["failures"], [])
        self.assertEqual(result["unmeasured"], [])
        self.assertAlmostEqual(result["smallest_measurable_text_pt"], 10)
        self.assertEqual(result["raster_placements"], 0)


if __name__ == "__main__":
    unittest.main()
