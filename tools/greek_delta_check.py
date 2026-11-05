#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate distinct Greek Delta and increment glyphs in a released UFO master.

The new Delta (U+0394) intentionally starts with the same geometry and width
as increment (U+2206). They remain separate glyphs for later Greek design work.
"""
import plistlib
from pathlib import Path
from xml.etree import ElementTree as ET


class DeltaSourceError(ValueError):
    """A UFO source violates the v1.0.1 Greek Delta design."""


def check_master(ufo: Path) -> None:
    """Fail if Delta differs from increment or either codepoint is misassigned."""
    ufo = Path(ufo)
    glyph_dir = ufo / 'glyphs'
    try:
        contents = plistlib.loads((glyph_dir / 'contents.plist').read_bytes())
        lib = plistlib.loads((ufo / 'lib.plist').read_bytes())
        order = lib['public.glyphOrder']
        if not isinstance(order, list) or len(order) != len(set(order)):
            raise DeltaSourceError('missing or duplicate glyph order entries')
        if len(contents) != len(order) or set(order) != set(contents):
            raise DeltaSourceError('contents.plist and public.glyphOrder do not agree')
        if contents.get('Delta') != 'Delta.glif':
            raise DeltaSourceError('Delta must have its own Delta.glif file')
        if contents.get('increment') == contents['Delta']:
            raise DeltaSourceError('Delta and increment must be separate source glyphs')
        if order.count('Delta') != 1 or order.count('increment') != 1:
            raise DeltaSourceError('Delta and increment must each appear once in glyph order')
        if len(set(contents.values())) != len(contents):
            raise DeltaSourceError('two glyph names reference the same GLIF file')
        glifs = {}
        for name in ('Delta', 'increment'):
            path = glyph_dir / contents[name]
            if path.parent != glyph_dir:
                raise DeltaSourceError(f'{name}: unsafe GLIF path')
            glif = ET.parse(path).getroot()
            if glif.tag != 'glyph' or glif.get('name') != name:
                raise DeltaSourceError(f'{name}: wrong GLIF identity')
            glifs[name] = glif
        for name, code in (('Delta', '0394'), ('increment', '2206')):
            mapped = [node.get('hex', '').upper() for node in glifs[name].findall('unicode')]
            if mapped != [code]:
                raise DeltaSourceError(f'{name}: expected only U+{code}, received {mapped}')
        delta, increment = glifs['Delta'], glifs['increment']
        if delta.find('advance') is None or increment.find('advance') is None:
            raise DeltaSourceError('missing glyph advance')
        if delta.find('advance').get('width') != increment.find('advance').get('width'):
            raise DeltaSourceError('Delta advance differs from increment')
        if delta.find('outline') is None or increment.find('outline') is None:
            raise DeltaSourceError('missing glyph outline')
        if ET.tostring(delta.find('outline')) != ET.tostring(increment.find('outline')):
            raise DeltaSourceError('Delta outline differs from increment')
        # Enforce a unique Unicode owner for each code point across the master.
        for name, filename in contents.items():
            if name in ('Delta', 'increment'):
                continue
            item = ET.parse(glyph_dir / filename).getroot()
            codes = {node.get('hex', '').upper() for node in item.findall('unicode')}
            if '0394' in codes or '2206' in codes:
                raise DeltaSourceError(f'{name}: duplicate Greek Delta or increment Unicode')
    except (OSError, ET.ParseError, plistlib.InvalidFileException, KeyError, TypeError) as exc:
        raise DeltaSourceError(f'{ufo}: invalid source data: {exc}') from exc


def check_sources(root: Path) -> int:
    """Validate all seven production masters, without changing any files."""
    root = Path(root)
    expected = {'display': 3, 'everyday': 2, 'mono': 2}
    total = 0
    for family, count in expected.items():
        masters = sorted((root / 'sources' / family ).glob('*.ufo'))
        if len(masters) != count:
            raise DeltaSourceError(f'{family}: expected {count} UFO masters, got {len(masters)}')
        for master in masters:
            check_master(master)
            total += 1
    return total


if __name__ == '__main__':
    count = check_sources(Path(__file__).resolve().parents[1])
    print(f'PASS: distinct Greek Delta U+0394 in {count} masters; '
          'increment U+2206 and initial outlines/widths preserved')
