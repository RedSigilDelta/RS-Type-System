#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Compatibility repair for Bold static font RIBBI style metadata.

Called after fontmake and before WOFF2 conversion. Does not modify outlines,
spacing, kern, features, axes, masters, other weights, or variable binaries.
Refuses unexpected families/styles; rerun --verify to audit the result.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from fontTools.ttLib import TTFont

FAMILIES=('RedSigil Display','RedSigil Everyday','RedSigil Mono')


def _records(font, nid):
    return [n for n in font['name'].names if n.nameID==nid]


def _values(font, nid):
    return {n.toUnicode() for n in _records(font,nid)}


def fix_font(font, family, verify=False):
    if family not in FAMILIES:
        raise ValueError('Unexpected family '+family)
    n=font['name']
    before={k:_values(font,k) for k in (1,2,16,17)}
    if not before[1] or not before[1].issubset({family,f'{family} Bold'}):
        raise ValueError(f'Unexpected nameID1: {before[1]}')
    if before[16] and before[16]!={family}:
        raise ValueError(f'Unexpected typographic family: {before[16]}')
    if before[17] and before[17]!={'Bold'}:
        raise ValueError(f'Unexpected typographic style: {before[17]}')
    if before[2] and not before[2].issubset({'Regular','Bold'}):
        raise ValueError(f'Unexpected nameID2: {before[2]}')
    if not _records(font,1) or not _records(font,2):
        raise ValueError('Legacy naming records missing; manual review required')
    required=(before[1]=={family} and before[2]=={'Bold'}
              and bool(font['OS/2'].fsSelection&0x20)
              and not bool(font['OS/2'].fsSelection&0x40)
              and bool(font['head'].macStyle&1))
    if verify:
        if not required: raise ValueError('Bold RIBBI not yet corrected: '+family)
        return False
    if required: return False
    for nid,new_value in ((1,family),(2,'Bold')):
        for record in _records(font,nid):
            n.setName(new_value,nid,record.platformID,record.platEncID,record.langID)
    # NameID 16/17, if present, retain the authoritative typographic labels.
    font['OS/2'].fsSelection=(font['OS/2'].fsSelection | 0x20)&~0x40
    font['head'].macStyle |= 1
    if not (font['OS/2'].fsSelection & 0x20) or (font['OS/2'].fsSelection & 0x40):
        raise AssertionError('Bold selection flags invalid')
    return True


def execute(directory,verify=False):
    directory=Path(directory)
    fonts=sorted(directory.glob('*-Bold.ttf'))
    if len(fonts)!=1:
        raise ValueError(f'Expected exactly one Bold static font in {directory}; got {len(fonts)}')
    for path in fonts:
        fam=path.stem.removesuffix('-Bold')
        font=TTFont(path,recalcTimestamp=False)
        try:
            changed=fix_font(font,fam,verify=verify)
            if changed:
                font.save(path,reorderTables=False)
            print(f'{"VERIFIED" if verify else "PATCHED" if changed else "UNCHANGED"}: {path.name}')
        finally: font.close()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',help='Build static TTF directory (not UFO sources)')
    p.add_argument('--verify',action='store_true',help='Non-mutating verification')
    a=p.parse_args()
    try: execute(a.directory,verify=a.verify)
    except Exception as exc:
        print('BLOCKED:',exc,file=sys.stderr);return 1
    return 0

if __name__=='__main__':sys.exit(main())
