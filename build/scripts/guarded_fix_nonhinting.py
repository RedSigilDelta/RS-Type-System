#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validated gftools nonhinted TrueType post-processing.

Applies to ALL named static instances and the family variable TTF. The expected
instance count comes from the authoritative Designspace, never from glob output.
Guards against source/outline/cmap/advance changes, partial outputs and wrong
font inventory. FontBakery/OTS must still run independently on GitHub.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
from xml.etree import ElementTree
from fontTools.ttLib import TTFont


def source_instance_count(designspace: Path) -> int:
    path = Path(designspace)
    if not path.is_file():
        raise ValueError(f'Missing Designspace: {path}')
    tree = ElementTree.parse(path).getroot()
    group = tree.find('instances')
    n = len(group.findall('instance')) if group is not None else 0
    if n < 1:
        raise ValueError(f'Designspace has no static instances: {path}')
    return n


def gather_fonts(static_dir: Path, variable_dir: Path, expected_static: int) -> list[Path]:
    static_dir, variable_dir = Path(static_dir), Path(variable_dir)
    if not static_dir.is_dir() or not variable_dir.is_dir():
        raise ValueError('Expected static and variable directories both to exist')
    # Restrict to direct children, matching the production fontmake contract.
    static = sorted(static_dir.glob('*.ttf'))
    variable = sorted(variable_dir.glob('*.ttf'))
    if any(p.is_symlink() or not p.is_file() for p in static + variable):
        raise ValueError('Refusing symbolic links or non-files among TTF candidates')
    if len(static) != expected_static or len(variable) != 1:
        raise ValueError(f'Expected {expected_static} static and 1 variable TTF; got {len(static)} static and {len(variable)} variable')
    if not variable[0].stem.endswith('-VF'):
        raise ValueError(f'Expected one -VF variable font, got: {variable[0].name}')
    if len({p.name for p in static}) != len(static):
        raise ValueError('Duplicate static font names')
    # Refuse stale post-processing intermediates or unexpected TTFs in nested paths.
    for parent, expected in ((static_dir, static), (variable_dir, variable)):
        actual = set(parent.rglob('*.ttf'))
        if actual != set(expected):
            raise ValueError(f'Unexpected nested TTFs in {parent}')
        if list(parent.glob('*.nonhinting-tmp.ttf')):
            raise ValueError(f'Stale nonhinting temp in {parent}')
    return static + variable


def signature(font: TTFont):
    glyphs = font['glyf']
    outlines = []
    for glyph_name in font.getGlyphOrder():
        coords, ends, flags = glyphs[glyph_name].getCoordinates(glyphs)
        outlines.append((glyph_name, tuple(map(tuple, coords)), tuple(ends), tuple(flags)))
    return (
        tuple(outlines),
        tuple(sorted(font['hmtx'].metrics.items())),
        tuple(sorted((font.getBestCmap() or {}).items())),
        tuple(font.getGlyphOrder()),
    )


def has_smart_dropout(font: TTFont) -> bool:
    if 'prep' not in font or not hasattr(font['prep'], 'program'):
        return False
    asm = font['prep'].program.getAssembly()
    return any('SCANCTRL' in op for op in asm) and any('SCANTYPE' in op for op in asm)


def verify_postprocessed(path: Path):
    font = TTFont(str(path), recalcTimestamp=False)
    try:
        if not has_smart_dropout(font):
            raise ValueError(f'Missing smart dropout SCANCTRL/SCANTYPE in {path}')
        if 'gasp' not in font:
            raise ValueError(f'Missing gasp table in {path}')
    finally:
        font.close()


def audit(original: Path, patched: Path):
    before = TTFont(str(original), recalcTimestamp=False)
    after = TTFont(str(patched), recalcTimestamp=False)
    try:
        if signature(before) != signature(after):
            raise ValueError(f'Outline/advance/cmap/glyph order changed in {original.name}')
    finally:
        before.close()
        after.close()
    verify_postprocessed(patched)


def execute(static_dir: Path, variable_dir: Path, designspace: Path, verify: bool = False):
    expected_static = source_instance_count(designspace)
    fonts = gather_fonts(static_dir, variable_dir, expected_static)
    if verify:
        for font in fonts:
            verify_postprocessed(font)
            print('VERIFIED:', font.name)
        print(f'OK: verified {len(fonts)} TTFs ({expected_static} static + 1 variable)')
        return 0
    # Stage and audit EVERY output before replacing ANY source candidate.
    # gftools fix-nonhinting creates *-backup-fonttools-prep-gasp.ttf beside
    # its input. Never give gftools a path in a production output directory:
    # the backup would be mistaken for a real static/variable font by glob-based
    # structural tests, FontBakery, OTS, and reproducibility checks.
    with tempfile.TemporaryDirectory(prefix='redsigil-nonhinting-') as temporary:
        staged = []
        sandbox = Path(temporary)
        for index, source in enumerate(fonts):
            # Work on an exact private copy; backups remain inside the sandbox.
            stage_input = sandbox / f'{index:02d}-input.ttf'
            target = sandbox / f'{index:02d}-postprocessed.ttf'
            shutil.copy2(source, stage_input)
            subprocess.run(['gftools', 'fix-nonhinting', str(stage_input), str(target)], check=True)
            if not target.is_file():
                raise ValueError(f'gftools produced no output for {source.name}')
            audit(source, target)
            staged.append((source, target))
        # Refuse unexpected input/output changes before committing staged outputs.
        # This also prevents pre-existing backups being silently ignored.
        gather_fonts(static_dir, variable_dir, expected_static)
        for source, target in staged:
            target.replace(source)
            print('NONHINTED:', source.name)
    print(f'OK: postprocessed {len(fonts)} TTFs ({expected_static} static + 1 variable)')
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('static_dir', type=Path)
    parser.add_argument('variable_dir', type=Path)
    parser.add_argument('--designspace', type=Path, required=True)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    try:
        return execute(args.static_dir, args.variable_dir, args.designspace, verify=args.verify)
    except Exception as exc:
        print('BLOCKED:', exc, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
