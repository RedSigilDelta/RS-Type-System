# Editable source structure

```text
sources/
  display/
    RedSigilDisplay.designspace
    RedSigilDisplay-Regular.ufo/
    RedSigilDisplay-Semibold.ufo/
    RedSigilDisplay-ExtraBold.ufo/
  everyday/
    RedSigilEveryday.designspace
    RedSigilEveryday-Regular.ufo/
    RedSigilEveryday-Bold.ufo/
  mono/
    RedSigilMono.designspace
    RedSigilMono-Regular.ufo/
    RedSigilMono-Bold.ufo/
```

This repository organizes the seven UFO masters and three Designspaces by family rather than the engineering phase in which they originated. Designspace source links are relative to their corresponding family directory.

Functional glyph names and GLIF component references—including some older numeric prefixes—are preserved. Removing or renaming them without a coordinated migration could break glyph composition. Obsolete nonfunctional notes were removed without changing glyph outlines, widths or Unicode assignments; the reorganized sources successfully built all 32 release fonts.

**Case-sensitive filenames are required.** Some GLIF filenames differ only in letter case. Extract editable source ZIP files onto a case-sensitive filesystem; otherwise two distinct glyph files may collide.
