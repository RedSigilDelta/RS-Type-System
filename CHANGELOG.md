# Changelog — RedSigil Type System

**🔥 Forged for Expression. ⚙️ Engineered for Precision.**

This changelog distinguishes the original **v1.0.0 stable engineering milestone** from **v1.0.1, the first public release**. The initial three-family design, Unicode coverage, OpenType layout and 32-font output set were already present in v1.0.0; they are not represented as new v1.0.1 work.

## [1.0.1] — First public release

### Typography and Unicode

- Added independently encoded **Greek capital Delta Δ (U+0394)** to all seven UFO masters, without replacing **mathematical increment ∆ (U+2206)** or **white up-pointing triangle △ (U+25B3)**.
- Preserved three distinct glyph identities. Delta and increment share equal initial outlines and advances, but remain independently encoded and addressable.
- Updated all seven editable master versions and compiled font metadata to **Version 1.001**. Full Greek-language coverage is **not** claimed.

### Public source and build infrastructure

- Organized the public editable source layout into `sources/display/`, `sources/everyday/`, and `sources/mono/`, preserving original functional glyph identifiers and case-sensitive names.
- Curated a standalone release repository with independently verifiable source and build history.
- Supplied the production build frontend, pinned direct build dependencies, Unicode/source/compiled-font checks, a manual GitHub Actions workflow, and release packaging scripts.
- Built the reorganized release sources at commit **`c956f7fc483a8a2d5bf6af8b35a643e8d3147a24`** using successful [GitHub Actions run **42104786087**](https://github.com/RedSigilDelta/RS-Type-System/actions/runs/42104786087). Verified **32/32** compiled fonts, TTF/WOFF2 table parity, source Delta identities, and downloaded-file SHA-256 checksums.

### First-public-release documentation and distribution

- Added README descriptions of each family, actual static and variable weight ranges, download links, licensing, build instructions, provenance, and character-support limitations.
- Added **five ornate Crimson Mirage type-specimen PNGs** combining reserved decorative artwork with typography rendered from the genuine verified v1.0.1 static TTF files: hero, Display, Everyday, Mono, and a symbols/coverage sheet. The generator verifies real weights, glyph support, source-font hashes and image hashes; no AI-simulated lettering is distributed.
- Prepared four numbered packages: **Stable Fonts**, **Editable Sources**, **Complete**, and **Release Verification**, plus a package-level SHA-256 sidecar.
- Kept **SIL OFL 1.1** for Font Software and editable type sources, with the Reserved Font Name **RedSigil**; assigned **MIT** to original public documentation and standalone tooling for this project only. Third-party license terms remain separate.

## [1.0.0] — Original stable foundation (October 2026)

### Initial font families

- Established three complementary families: **RedSigil Display** for prominent titles and expressive headlines; **RedSigil Everyday** for reading, documents and user interfaces; **RedSigil Mono** for fixed-width technical text, terminals and aligned material.
- Developed **seven editable UFO masters** and **three Designspace documents**: three masters for Display, two for Everyday and two for Mono.
- Built **13 static TTFs** spanning the supported weights:
  - **Display:** Regular 400, Medium 500, Semibold 600, Bold 700, ExtraBold 800.
  - **Everyday:** Regular 400, Medium 500, Semibold 600, Bold 700.
  - **Mono:** Regular 400, Medium 500, Semibold 600, Bold 700.
- Built a **variable TTF per family**, with `wght` axes of **400–800** for Display and **400–700** for Everyday and Mono.
- Produced **16 WOFF2 files** (13 static plus three variable). In total, the original stable build delivered **32 compiled fonts**.

### Character repertoire and typography

- Established extended **Latin-letter and accented-character coverage**, punctuation, numerals, selected currency signs, publishing marks, arrows, triangles and mathematical symbols. The original compilation contained independent **∆ (U+2206)** and **△ (U+25B3)**; **Δ (U+0394)** was added later in v1.0.1.
- Confirmed from the preserved v1.0.0 TTF binaries that each Display and Everyday style/variable font mapped **372 Unicode code points**, while each Mono style/variable font mapped **532**. These are counts of mappings, **not** complete-language or entire-Unicode-block coverage claims.
- Included selected Latin/Central-European diacritic forms such as **Č, Ž, ď, ľ, ť**, in addition to characters such as **Á, É, Ñ, Æ, Œ, µ**. Character availability should always be checked in the actual font before assuming comprehensive language support.
- Included mathematical examples **± × ÷ ≠ ≤ ≥ ≈ ∞ √ ∑ ∏ ∂ ∫**, arrows including **← → ↑ ↓ ↔ ↗ ↘**, plus monetary and publishing marks across all three families.
- Added a larger code-and-terminal-oriented repertoire to **Mono**, including actual mapped **box-drawing and block elements** such as `─ │ ┌ ┐ █ ░`; did not imply these blocks were present in Display or Everyday.

### OpenType layout and mono features

- Shipped **GSUB `ccmp` and `locl`** and **GPOS `mark`/`mkmk`** in all three families for character composition, localized forms, and mark positioning.
- Included **GPOS `kern`** in Display and Everyday; Mono deliberately has no listed `kern` positioning feature in the preserved stable TTFs.
- Included the additional Mono GSUB features **`ss01`** and **`zero`**, alongside `ccmp` and `locl`. Availability of features depends on the consuming application and its OpenType support.
- Maintained Mono's fixed-width design: for example, the v1.0.0 Mono Regular sample glyphs `A`, `B`, `0`, `1` and `─` each have a **620-unit advance**. This sample does not replace a complete every-glyph width audit.

### Build, licensing and release verification

- Established a production pipeline using editable UFO and Designspace inputs, with static/variable TTF and WOFF2 outputs, source/build checks and preserved artifact-level integrity evidence.
- Completed the original v1.0.0 stable production verification: **32/32 PASS**, `Version 1.000` metadata and SHA-256 font inventories. Historical engineering identifiers remain in the private project records.
- Preserved the four-part historical package arrangement of compiled fonts, editable sources, complete sources-and-fonts, and verification evidence; **v1.0.0 had no public release from this repository**.
- Applied **SIL Open Font License 1.1** to the original Font Software, with **RedSigil** as its Reserved Font Name.

The v1.0.0 facts above were cross-checked against archived stable-font binaries and verification reports. They document the original foundation without claiming that v1.0.0 was released publicly, that every glyph or language was tested, or that old and new compiled binaries are byte-for-byte identical.
