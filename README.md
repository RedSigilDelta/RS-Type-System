# RedSigilΔ Type System

**Version 1.0.1 — first planned public release (draft; not published).**

RedSigilΔ Type System provides three related font families—**RedSigil Display**, **RedSigil Everyday**, and **RedSigil Mono**—in editable UFO/Designspace source form and as 32 compiled TTF/WOFF2 font files in the separate Stable Fonts package.

## Font families and formats

| Family | UFO masters | Static TTF | Variable TTF | WOFF2 |
|---|---:|---:|---:|---:|
| RedSigil Display | 3 | 5 | 1 | 6 |
| RedSigil Everyday | 2 | 4 | 1 | 5 |
| RedSigil Mono | 2 | 4 | 1 | 5 |
| **Total** | **7** | **13** | **3** | **16** |

See [Font Families](docs/FONT_FAMILIES.md) for styles and source locations.

## Release history

**v1.0.0 — original stable foundation (private engineering release, October 2026).** Established the three-family stable baseline, seven editable masters, three Designspace documents, and the 32-font production distribution. The v1.0.0 GitHub release history is preserved; it was *not* the first public distribution.

**v1.0.1 — first planned public release.** Introduces independent Greek capital Delta **Δ** (U+0394) in every master. Mathematical increment **∆** (U+2206) and white up-pointing triangle **△** (U+25B3) remain. Delta and increment have distinct glyph identities but matching initial outlines and advance widths. No claim of full Greek-alphabet or language coverage is made. Source and font version metadata are updated to 1.001.

For details see [CHANGELOG](CHANGELOG.md) and [RELEASE_NOTES](RELEASE_NOTES.md).

## Editable sources

The public source layout is:

- `sources/display/`: three Display UFO masters and `RedSigilDisplay.designspace`
- `sources/everyday/`: two Everyday UFO masters and `RedSigilEveryday.designspace`
- `sources/mono/`: two Mono UFO masters and `RedSigilMono.designspace`
- `build/`: pinned production dependencies and standalone build scripts
- `tools/`: source/compiled font verification and Greek Delta regression tests

Source glyph filenames are **case-sensitive**; extract and develop on a case-sensitive filesystem. Some internal UFO glyph identifiers retain legacy numeric prefixes because they are functional references; those are not version or release names.

See [Building](docs/BUILDING.md), [Verification](docs/VERIFICATION.md) and [Source Structure](docs/SOURCE_STRUCTURE.md).

## Licensing

The RedSigil **Font Software** is licensed under SIL Open Font License 1.1, including Reserved Font Name **RedSigil**, with the existing copyright notice retained. The seven original standalone build and verification scripts in this source package use MIT. Third-party dependencies keep their own licenses. See [LICENSES](LICENSES.md) and `licenses/` for scope and full notices. The OFL remains the governing license for the fonts, not MIT.

## Release provenance

The proposed v1.0.1 source release is derived from private `master` merge revision `a36f1dfcf8579a235a467d235cbd1104e0d1a5ad`. The 32-font production check was performed with GitHub Actions run `42083737306` **before the merge**, and compiled output was independently verified 32/32. Public source path cleanup and comments/notes cleanup were performed in a separate working copy; a direct rebuild from that curated copy has **not yet been completed**. These records are not a claim of binary-for-binary equivalence.

## Distribution status

This working copy is a **review draft** and is not a published public repository, a public GitHub release, or an approval to publish.
