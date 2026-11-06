# RedSigil Type System v1.0.1 — First Public Release

**🔥 Forged for Expression. ⚙️ Engineered for Precision.**

The public README showcases real-font Crimson Mirage specimens for all three families, with accurate static weights, symbol coverage, and a local owner-controlled specimen renderer. These previews are generated from the verified compiled TTF files, not invented letterforms.

RedSigil Type System brings three purpose-built font families together in one open-source release: **Display** for expressive headings, **Everyday** for readable general text, and **Mono** for fixed-width text and technical work.

## Included in v1.0.1

- **32 compiled fonts:** 13 static TTF, 3 variable TTF and 16 WOFF2, spanning Display, Everyday and Mono.
- **Editable sources:** seven UFO masters and three Designspace documents.
- **Build and verification tooling:** the production scripts, pinned direct requirements, Unicode checks and manual GitHub Actions workflow.
- **Four numbered distributions:** Stable Fonts, Editable Sources, Complete, and Release Verification.

## From the stable foundation to the first public release

The original **v1.0.0** private stable engineering milestone established the complete three-family foundation in October 2026: **7 editable UFO masters**, **3 Designspaces**, **13 static TTFs**, **3 variable TTFs**, and **16 WOFF2 files**. Display offered five static weights (400–800); Everyday and Mono each offered four (400–700). Every family included OpenType `ccmp`, `locl`, `mark`, and `mkmk`; Display and Everyday also supplied kerning, while Mono supplied `ss01`, `zero`, and additional box/block characters. In the preserved v1.0.0 binaries, Display and Everyday mapped 372 Unicode characters per font and Mono mapped 532. The preserved v1.0.0 release-verification evidence confirmed 32/32 version-1.000 compiled fonts. These were the original foundation, **not new additions introduced by v1.0.1**.

The v1.0.0 engineering record is historical context, not a separate public release or tag. [CHANGELOG.md](CHANGELOG.md) contains the detailed initial-family, character-repertoire, OpenType and verification history.

**v1.0.1** adds an independent Greek capital **Δ** (U+0394) to all seven masters, without replacing mathematical increment **∆** (U+2206) or white up-pointing triangle **△** (U+25B3). Delta and increment retain separate glyph identities and equal initial outlines and advance widths. Font version metadata is **1.001**.

This focused addition does **not** constitute full Greek alphabet or language support.

## Build and quality evidence

The reorganized release sources were compiled in a successful, manual GitHub Actions production build:

- **Repository:** `RedSigilDelta/RS-Type-System`
- **Source commit:** `c956f7fc483a8a2d5bf6af8b35a643e8d3147a24`
- **Workflow run:** [42104786087](https://github.com/RedSigilDelta/RS-Type-System/actions/runs/42104786087)
- **Validated results:** all 32 outputs, version/name data, Unicode mapping and TTF/WOFF2 equivalence.
- **Independent downloaded-artifact checks:** 32/32 compiled fonts passed; the saved SHA-256 inventory passed 32/32 rechecks.

See [Provenance](docs/PROVENANCE.md) and [Verification](docs/VERIFICATION.md). The release packaging adds independent archive-level checksums; older builds are not claimed to be byte-for-byte identical.

## Get the files

Download the four numbered archives and SHA-256 sidecar from the [v1.0.1 GitHub release](https://github.com/RedSigilDelta/RS-Type-System/releases/tag/v1.0.1), or browse the editable source tree in the repository.

## Licensing

Font Software and UFO/Designspace sources: **SIL OFL 1.1**, Reserved Font Name **RedSigil**. Original project build/verification/release scripts and manual workflow: **MIT**. Original documentation: **MIT**. The finished decorative specimen artwork and original textured sigil are **All Rights Reserved**; no artwork reuse rights are granted by the MIT documentation license. Third-party dependencies retain their own licenses. Refer to [LICENSES.md](LICENSES.md).
