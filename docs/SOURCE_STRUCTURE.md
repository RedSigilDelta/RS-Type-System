# Editable source layout

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

Public family directories are named by family rather than development milestone. All Designspace `source filename` links remain relative and point to the same UFO names.

GLIF component references, glyph names and the UFO `public.glyphOrder` are *not* renamed. Some glyph identifiers retain numeric prefixes because they are functional source identifiers. Changing them requires a coordinated glyph-renaming migration and additional checks. Nonfunctional historical phase notes in GLIF metadata and obsolete source-status notes have been removed from this review copy; the corresponding unmodified originals remain in the private engineering revision.

**Filesystem requirement:** Glyph files include filenames whose casing matters. Do not unpack or develop on a case-insensitive filesystem that merges names differing only by case. A private, case-sensitive working filesystem is suitable.
