#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# RedSigil family production build using fontmake and validated font post-processing.
# Builds static and variable TTFs, then generates matching WOFF2 outputs.
set -euo pipefail
if [ "$#" -ne 2 ]; then echo "usage: $0 <family.designspace> <output-dir>" >&2; exit 2; fi
DESIGNSPACE=$1; OUT=$2
: "${FONTMAKE:=fontmake}"
mkdir -p "$OUT/static" "$OUT/variable" "$OUT/woff2"
"$FONTMAKE" -m "$DESIGNSPACE" -o ttf -i --output-dir "$OUT/static"
"$FONTMAKE" -m "$DESIGNSPACE" -o variable --output-dir "$OUT/variable"
# Resolve only verified Bold static RIBBI compatibility metadata after fontmake.
python3 "$(dirname "$0")/scripts/repair_bold_ribbi.py" "$OUT/static"
python3 "$(dirname "$0")/scripts/repair_bold_ribbi.py" "$OUT/static" --verify
# Retain no-autohint output while enabling TrueType smart-dropout control.
python3 "$(dirname "$0")/scripts/guarded_fix_nonhinting.py" "$OUT/static" "$OUT/variable" --designspace "$DESIGNSPACE"
python3 "$(dirname "$0")/scripts/guarded_fix_nonhinting.py" "$OUT/static" "$OUT/variable" --designspace "$DESIGNSPACE" --verify
python3 "$(dirname "$0")/scripts/make_woff2.py" "$OUT/static" "$OUT/variable" --output "$OUT/woff2"
