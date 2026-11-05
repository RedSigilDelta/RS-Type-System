#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Focused regression tests for the independent Greek Delta glyph."""
import plistlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from greek_delta_check import DeltaSourceError, check_master, check_sources

ROOT = Path(__file__).resolve().parents[1]
GLIF_TEMPLATE = ("<?xml version='1.0' encoding='UTF-8'?>\n"
                 '<glyph name="{name}" format="2">'
                 '<advance width="620" /><unicode hex="{code}" />'
                 '<outline><contour><point x="0" y="0" type="line" />'
                 '<point x="300" y="700" type="line" />'
                 '<point x="600" y="0" type="line" />'
                 '</contour></outline></glyph>')


class DeltaSourceTests(unittest.TestCase):
    def test_all_real_masters(self):
        self.assertEqual(check_sources(ROOT), 7)

    def make_fixture(self, directory):
        ufo = Path(directory) / 'Mock.ufo'
        g = ufo / 'glyphs'
        g.mkdir(parents=True)
        for name, code in (('Delta', '0394'), ('increment', '2206')):
            (g / f'{name}.glif').write_text(GLIF_TEMPLATE.format(name=name, code=code))
        (g / 'contents.plist').write_bytes(plistlib.dumps({'Delta': 'Delta.glif',
                                                         'increment': 'increment.glif'}))
        (ufo / 'lib.plist').write_bytes(plistlib.dumps({'public.glyphOrder': ['increment', 'Delta']}))
        return ufo

    def test_good_separate_glyphs(self):
        with tempfile.TemporaryDirectory() as td:
            check_master(self.make_fixture(td))

    def test_missing_delta_mapping_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            ufo = self.make_fixture(td)
            path = ufo / 'glyphs' / 'Delta.glif'
            path.write_text(path.read_text().replace('0394', '2206'))
            with self.assertRaises(DeltaSourceError):
                check_master(ufo)

    def test_changed_width_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            ufo = self.make_fixture(td)
            path = ufo / 'glyphs' / 'Delta.glif'
            path.write_text(path.read_text().replace('width="620"', 'width="630"'))
            with self.assertRaises(DeltaSourceError):
                check_master(ufo)

    def test_changed_outline_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            ufo = self.make_fixture(td)
            path = ufo / 'glyphs' / 'Delta.glif'
            path.write_text(path.read_text().replace('x="300"', 'x="305"'))
            with self.assertRaises(DeltaSourceError):
                check_master(ufo)

    def test_missing_glyphorder_entry_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            ufo = self.make_fixture(td)
            (ufo / 'lib.plist').write_bytes(plistlib.dumps({'public.glyphOrder': ['increment']}))
            with self.assertRaises(DeltaSourceError):
                check_master(ufo)


if __name__ == '__main__':
    unittest.main()
