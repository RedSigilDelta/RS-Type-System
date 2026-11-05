# RedSigilΔ Type System v1.0.1 — First Public Release Notes (DRAFT)

**Release status:** Under review. This file does not announce an available public repository or public download.

## Introducing RedSigilΔ Type System

This is the Type System's **first planned public distribution**. It introduces the complete original v1.0.0 stable foundation alongside the focused v1.0.1 Greek Delta enhancement. The original stable version was developed and released privately; it has not been overwritten or relabeled.

### What the original v1.0.0 foundation delivered

- Three related font families: **Display**, **Everyday** and **Mono**.
- Seven editable UFO masters and three Designspace files.
- A distribution of 32 compiled fonts: 13 static TrueType, 3 variable TrueType and 16 WOFF2.
- A production build process supported by source and compiled-font verification.
- SIL OFL 1.1 licensing for the Font Software, with Reserved Font Name **RedSigil**.

Original stable build evidence: Actions run **38093292620** and source revision **d5f28d1105b4ab0c1c405c88bf653c0afd454802**.

### What changed in v1.0.1

- Added Greek capital Delta **Δ** (U+0394) to every production master as an independent glyph.
- Kept mathematical increment **∆** (U+2206) and white up-pointing triangle **△** (U+25B3).
- Delta and increment remain separate glyphs with identical initial outlines and advance widths.
- Updated source and compiled font version metadata to **1.001**.
- Verified all 32 fonts in successful Actions run **42083737306**, including the Unicode mappings and TTF/WOFF2 checks.

**Important scope note:** This does **not** add complete Greek-alphabet support.

### Public-source preparation

A separate, review-only source copy simplifies family source paths, removes obsolete internal phase/status text from reader-facing documents and nonfunctional source notes, includes MIT-licensed standalone build/verification scripts, and preserves historic private engineering materials separately. Original font glyph identities, outlines, metrics and Unicode mappings have not been intentionally altered by this cleanup; a fresh production build from curated paths is still required before claiming reproduction of the previous binary outputs.

### Release packaging (planned)

The intended distribution retains four numbered archives: **01 Stable Fonts**, **02 Editable Sources**, **03 Complete**, **04 Release Verification**. Public package checksums, publication location and final provenance will be established at release approval.

### Licenses

Font Software: SIL Open Font License 1.1 and Reserved Font Name **RedSigil**. Original standalone build and verification scripts: MIT. Third-party tools have their own licenses. Refer to `LICENSES.md` and the license text files.
