#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
import argparse
from pathlib import Path
from fontTools.ttLib import TTFont
ap=argparse.ArgumentParser(); ap.add_argument('inputs',nargs='+'); ap.add_argument('--output',required=True); args=ap.parse_args()
out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
for raw in args.inputs:
    p=Path(raw); files=[p] if p.is_file() else sorted(p.glob('*.ttf'))
    for src in files:
        f=TTFont(src,recalcTimestamp=False); f.flavor='woff2'; target=out/(src.stem+'.woff2'); f.save(target,reorderTables=None); print(target)
