# Font specimens and real glyph coverage

The README showcases **five raster images rendered using the actual RedSigil Type System v1.0.1 static TTF files**. These are not AI-simulated letterforms and are not substitute fonts. Text shown in each family panel uses that family's compiled styles. Brand headings and supporting labels also use actual compiled RedSigil font files. Decorative lines, backgrounds, panels, and the genuine textured sigil are artwork—not glyph coverage claims. These illustrative assets are All Rights Reserved.

## Images

| Image | Description |
|---|---|
| [`hero.png`](../assets/specimens/hero.png) | Display, Everyday, and Mono at a glance |
| [`display.png`](../assets/specimens/display.png) | Display in use, five genuine static weights and verified characters |
| [`everyday.png`](../assets/specimens/everyday.png) | Everyday paragraph, four genuine static weights and verified characters |
| [`mono.png`](../assets/specimens/mono.png) | Mono code/terminal text, four genuine static weights and verified characters |
| [`symbols.png`](../assets/specimens/symbols.png) | Representative math, arrows, currency, publishing, punctuation, and accented Latin glyphs |

## Actual styles

| Family | Static weights by OS/2 `usWeightClass` | Variable `wght` range |
|---|---|---|
| RedSigil Display | Regular 400; Medium 500; Semibold 600; Bold 700; ExtraBold 800 | 400–800 |
| RedSigil Everyday | Regular 400; Medium 500; Semibold 600; Bold 700 | 400–700 |
| RedSigil Mono | Regular 400; Medium 500; Semibold 600; Bold 700 | 400–700 |

These values are checked from the actual compiled static files during specimen generation; the script refuses mismatches.

## Original 1.0.0 foundation, retained in v1.0.1

The original archived v1.0.0 fonts already contained **372 mapped code points** in Display and Everyday and **532** in Mono, with static/variable support and real OpenType positioning and substitutions. The repertoire included extended Latin accents, numerals, punctuation, selected mathematics, arrows, publishing/currency marks and Mono's additional box/block symbols. **Greek capital Delta U+0394 is the v1.0.1 addition**, not a retroactive v1.0.0 feature.

OpenType features verified in all v1.0.0 TTFs: `ccmp`, `locl`, `mark`, `mkmk`; Display/Everyday additionally have `kern`, and Mono additionally has `ss01` and `zero`. The current renderer checks characters and weights from **actual v1.0.1 binaries**, not these historical counts, before drawing specimen images.

## Selected supported glyph groups

- **Delta and triangle:** Δ (U+0394), ∆ (U+2206), △ (U+25B3), each with a distinct compiled glyph identity.
- **Mathematics:** ± × ÷ ≠ ≤ ≥ ≈ ∞ √ ∑ ∏ ∂ ∫ µ.
- **Arrows:** ← → ↑ ↓ ↔ ↗ ↘.
- **Currency:** € £ ¥ ¢ $.
- **Publishing:** © ® ™ § ¶ † ‡ • · ‰.
- **Punctuation:** “ ” ‘ ’ — – … « ».
- **Accented and extended Latin:** Á É Ñ Ç ß Æ Œ ø Ł.

The renderer computes support from the compiled font `cmap` rather than assuming the above characters are universally available. Symbols not present in a family are omitted from that family's image. The combined symbols image uses glyphs shared by all three families. This is a **selection**, not an exhaustive character-coverage manifest; broad Greek, emoji, and comprehensive math or music-script support are **not** claimed for v1.0.1.

## Crimson Mirage colors

These are the typography palette values. The approved ornate background images contain additional rasterized nebula colors:

| Theme token | Value |
|---|---|
| Midnight Crimson background | `#18091D` |
| Warm Ivory foreground | `#FFF3E9` |
| Royal Lavender | `#D9ADFF` |
| Champagne Gold | `#FFE09A` |
| Arcane Blue | `#AABFFF` |
| Warm Amber | `#FFB47B` |

## Specimen generation and verification

The five published PNGs and `assets/specimens/SPECIMENS.json` are generated using genuine v1.0.1 static TTF files from the verified GitHub Actions build [42104786087](https://github.com/RedSigilDelta/RS-Type-System/actions/runs/42104786087). Every specimen character is checked against the applicable font's `cmap`, and each static style and weight is verified before rendering. Decorative borders, nebula artwork, and the original textured sigil are separate reserved visual assets, not font glyphs.

The public repository distributes the approved final PNGs and their verification metadata, **not** the editable decorative plates, layered compositions, or original sigil source image. A public checkout therefore cannot reproduce the exact ornamental backgrounds from the Font Software alone. This does not affect independent rebuilding or verification of the fonts themselves. `tools/render_specimens.py` is an optional maintainer launcher that requires separately held artwork assets; it does not download those assets or substitute system fonts.

`SPECIMENS.json` records the public build identity, verified font-input hashes and weights, character coverage, and final PNG SHA-256 checksums. Optional characters absent from a family's `cmap` are omitted and recorded; required text is rendered only when verified and fitted without fallback. The published image checksums can be checked independently without access to the editable background artwork.

## Artwork and tool licensing

The rendered decorative compositions and original textured sigil are **All Rights Reserved**. The RedSigil Font Software is SIL OFL 1.1, with Reserved Font Name **RedSigil**. The public launcher, original scripts and project prose are MIT-licensed. The private layered art templates and bitmap assets are not offered for public reuse. No licensing notice is embedded into the face of any image. See [LICENSES.md](../LICENSES.md).
