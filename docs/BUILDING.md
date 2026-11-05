# Building RedSigilΔ Type System from source

**Public source working-copy instructions — draft, not yet independently production-tested after path cleanup.**

## Prerequisites

The production workflow uses **Ubuntu 24.04** with **Python 3.11** and the pinned dependencies in `build/requirements-direct.txt`. The scripts require Python, a POSIX shell/Bash, and executables from fontmake, fontTools, gftools and related dependencies. These instructions describe the upstream production environment; they are not Termux installation instructions.

Install pinned direct dependencies in your preferred isolated Python build environment:

```bash
python -m pip install -r build/requirements-direct.txt
```

## Source-only validation

```bash
python tools/stable_font_verify.py --sources
```

```bash
python -m unittest tools/test_greek_delta_check.py
```

## Build each family

```bash
bash build/build_family_with_fontmake.sh sources/display/RedSigilDisplay.designspace ./build-output/display
```

```bash
bash build/build_family_with_fontmake.sh sources/everyday/RedSigilEveryday.designspace ./build-output/everyday
```

```bash
bash build/build_family_with_fontmake.sh sources/mono/RedSigilMono.designspace ./build-output/mono
```

## Validate compiled fonts

```bash
python tools/stable_font_verify.py --compiled ./build-output
```

Expected layout: `build-output/{display,everyday,mono}/{static,variable,woff2}/`. Font counts: **13 static TTF**, **3 variable TTF**, **16 WOFF2**. Each WOFF2 should match its TTF counterpart under the verifier's documented table equivalence checks.

Always use the build tools and source paths from the same release snapshot.
