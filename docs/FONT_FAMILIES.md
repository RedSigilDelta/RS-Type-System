# Font families and styles

| Family | Source masters | Static styles | Variable font |
|---|---:|---|---|
| **RedSigil Display** | 3 | Regular, Medium, Semibold, Bold, ExtraBold | Weight axis, 400–800 |
| **RedSigil Everyday** | 2 | Regular, Medium, Semibold, Bold | Weight axis, 400–700 |
| **RedSigil Mono** | 2 | Regular, Medium, Semibold, Bold | Weight axis, 400–700 |

The three families have separate source files and distinct family naming. The Mono source is designed for a fixed-width text cell.

Each family includes one Designspace document and one or more UFO masters. Source files retain exact case-sensitive glyph filenames. The source folder layout does not use internal development-phase names.

In v1.0.1, U+0394 (Greek capital Delta) is encoded independently of U+2206 (mathematical increment); the initial outlines and advance widths match. U+25B3 (white up-pointing triangle) remains separate. These additions are **not** full Greek-language support.
