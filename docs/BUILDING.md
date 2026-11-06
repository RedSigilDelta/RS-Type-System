# Build RedSigilΔ Type System from source

The production build uses Ubuntu 24.04, Python 3.11 and the pinned direct requirements in `build/requirements-direct.txt`. The curated sources were successfully compiled and verified in [GitHub Actions run 42104786087](https://github.com/RedSigilDelta/RS-Type-System/actions/runs/42104786087) from commit `c956f7fc483a8a2d5bf6af8b35a643e8d3147a24`.

The commands below describe the production environment. The project does not require a Termux-specific build, PRoot, or a modified Android installation.

## Prerequisites

Use a case-sensitive filesystem with Python 3.11, Bash and the pinned packages. Fonts are built using the same `fontmake`, `fontTools` and related dependencies as the workflow.

```bash
python -m pip install -r build/requirements-direct.txt
```

## Source verification

```bash
python tools/stable_font_verify.py --sources
```

```bash
python -m unittest tools/test_greek_delta_check.py
```

## Build the three families

```bash
bash build/build_family_with_fontmake.sh sources/display/RedSigilDisplay.designspace ./build-output/display
```

```bash
bash build/build_family_with_fontmake.sh sources/everyday/RedSigilEveryday.designspace ./build-output/everyday
```

```bash
bash build/build_family_with_fontmake.sh sources/mono/RedSigilMono.designspace ./build-output/mono
```

## Validate the outputs

```bash
python tools/stable_font_verify.py --compiled ./build-output --report ./build-output/QA_REPORT.json
```

The expected layout is `build-output/{display,everyday,mono}/{static,variable,woff2}/` containing **13 static TTF**, **3 variable TTF** and **16 WOFF2**. For GitHub Actions downloads made with `gh run download --dir`, point `--compiled` at the inner artifact folder that directly contains `display/`, `everyday/` and `mono/`.

The `.github/workflows/stable-font-build.yml` workflow can be triggered manually from `master` to reproduce the production build. New source or build-tool changes should be independently validated before distributing revised binaries.
