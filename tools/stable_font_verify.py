#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Fail-closed, standalone stable font version/shape verifier."""
import argparse
import hashlib
import json
import plistlib
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
if __package__:
    from .greek_delta_check import check_master
else:
    from greek_delta_check import check_master

ROOT = Path(__file__).resolve().parents[1]
MASTERS = (3, 2, 2)
FAMILIES = ('display', 'everyday', 'mono')
EXPECTED_STATIC = {'display': 5, 'everyday': 4, 'mono': 4}


def source_check():
    sources = []
    for family, count in zip(FAMILIES, MASTERS):
        base = ROOT / 'sources' / family
        masters = sorted(base.glob('*.ufo/fontinfo.plist'))
        assert len(masters) == count, f'{family}: expected {count} masters, got {len(masters)}'
        for p in masters:
            with p.open('rb') as f:
                info = plistlib.load(f)
            assert (info.get('versionMajor'), info.get('versionMinor')) == (1, 1), f'{p}: version mismatch'
            check_master(p.parent)
            sources.append(str(p.relative_to(ROOT)))
    print(f'PASS: {len(sources)} UFO masters declare v1.001 and contain independent Greek Delta U+0394')


def same_table_content(tag, left, right):
    """Compare SFNT tables while permitting only documented WOFF2 head changes.

    WOFF2 reconstruction changes the head.checkSumAdjustment (bytes 8:12)
    and sets bit 11 of head.flags to mark a lossless modifying transform.
    All other bytes must agree. The WOFF2 transform bit must be present.
    """
    if tag != 'head':
        return left == right
    if len(left) != len(right) or len(left) < 18:
        return False
    ttf_flags = int.from_bytes(left[16:18], 'big')
    woff_flags = int.from_bytes(right[16:18], 'big')
    if woff_flags != (ttf_flags | 0x0800):
        return False
    return left[:8] == right[:8] and left[12:16] == right[12:16] and left[18:] == right[18:]


def collect(base):
    details = []
    for family in FAMILIES:
        folder = base / family
        static = sorted((folder / 'static').glob('*.ttf'))
        variable = sorted((folder / 'variable').glob('*.ttf'))
        woff = sorted((folder / 'woff2').glob('*.woff2'))
        assert len(static) == EXPECTED_STATIC[family], f'{family}: {len(static)} static fonts, expected {EXPECTED_STATIC[family]}'
        assert len(variable) == 1, f'{family}: expected one variable font, got {len(variable)}'
        assert len(woff) == len(static) + 1, f'{family}: expected {len(static)+1} WOFF2, got {len(woff)}'
        original = {p.stem: p for p in static + variable}
        assert {p.stem for p in woff} == set(original), f'{family}: mismatched TTF/WOFF2 names'
        for file in static + variable + woff:
            with TTFont(file, lazy=False) as font:
                revision = font['head'].fontRevision
                assert abs(revision - 1.001) < 0.00002, f'{file}: head version {revision}'
                versions = {n.toUnicode() for n in font['name'].names if n.nameID == 5}
                assert versions and all(v.startswith('Version 1.001') for v in versions), f'{file}: version strings {versions}'
                assert font['OS/2'].fsType == 0, f'{file}: restricted embedding'
                cmap = font.getBestCmap() or {}
                assert 0x0394 in cmap and 0x2206 in cmap, f'{file}: missing U+0394/U+2206'
                delta_name, increment_name = cmap[0x0394], cmap[0x2206]
                assert delta_name != increment_name, f'{file}: Delta/increment share one compiled glyph'
                assert font['hmtx'][delta_name][0] == font['hmtx'][increment_name][0], f'{file}: Delta/increment width differs'
                glyphset = font.getGlyphSet()
                delta_pen, increment_pen = RecordingPen(), RecordingPen()
                glyphset[delta_name].draw(delta_pen)
                glyphset[increment_name].draw(increment_pen)
                assert delta_pen.value == increment_pen.value, f'{file}: Delta/increment outlines differ'
                assert bool('fvar' in font) == (file.stem in {p.stem for p in variable}), f'{file}: variable classification'
                details.append({'path': str(file.relative_to(base)), 'sha256': hashlib.sha256(file.read_bytes()).hexdigest(), 'version': sorted(versions)})
        for p in woff:
            with TTFont(original[p.stem]) as ttf, TTFont(p) as wf:
                assert set(ttf.keys()) == set(wf.keys()), f'{p}: table set differs'
                for tag in (set(ttf.keys()) - {'GlyphOrder'}):
                    assert same_table_content(tag, ttf.getTableData(tag), wf.getTableData(tag)), f'{p}: table {tag} differs from TTF'
    assert len(details) == 32, f'Expected 32 outputs, got {len(details)}'
    return details


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', action='store_true')
    parser.add_argument('--compiled', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    assert args.sources or args.compiled, 'Choose --sources and/or --compiled'
    if args.sources:
        source_check()
    if args.compiled:
        items = collect(args.compiled)
        print(f'PASS: {len(items)} stable font files, versions, structure and WOFF2/TTF table parity')
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps({'result': 'PASS', 'file_count': len(items), 'files': items}, indent=2) + '\n')


if __name__ == '__main__':
    main()
