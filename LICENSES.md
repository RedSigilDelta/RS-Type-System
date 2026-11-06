# License scopes — RedSigil Type System v1.0.1

**Copyright © 2026 Gerald A Folsom Jr.** Different components have different licenses; a license for one component does not silently relicense other content.

## Font Software: SIL Open Font License 1.1

All original **RedSigil Display, Everyday, and Mono** binaries, seven UFO masters, and three Designspace files use **SIL OFL 1.1**, with sole Reserved Font Name **RedSigil** and the original font copyright notice. Complete license text and Reserved Font Name notice: [`licenses/OFL-1.1.txt`](licenses/OFL-1.1.txt).

## Original scripts and workflow: MIT

The following original build, verification and distribution automation uses **MIT**; full text: [`licenses/MIT-TOOLS.txt`](licenses/MIT-TOOLS.txt).

- `build/build_family_with_fontmake.sh`
- `build/scripts/guarded_fix_nonhinting.py`
- `build/scripts/make_woff2.py`
- `build/scripts/repair_bold_ribbi.py`
- `tools/greek_delta_check.py`
- `tools/stable_font_verify.py`
- `tools/test_greek_delta_check.py`
- `release/make_release.py`
- `tools/render_specimens.py` (public launcher for the owner’s local specimen workspace)
- `.github/workflows/stable-font-build.yml`

## Original project documentation: MIT

For **this Type System project**, the original prose in `README.md`, `CHANGELOG.md`, `RELEASE_NOTES.md`, `LICENSES.md`, `docs/*.md`, and the original explanatory readmes and verification instructions in distribution packages is licensed under **MIT**. The same existing full MIT license text and copyright notice at [`licenses/MIT-TOOLS.txt`](licenses/MIT-TOOLS.txt) covers both this original documentation and the original scripts/workflow listed above. This permission applies only to original documentation owned by the project author. Third-party material and Font Software keep their respective licenses.

## External dependencies

`build/requirements-direct.txt` records build dependencies. Their authors retain their own rights and license terms. The project does not own or relicense these dependencies. License texts are distributed for project components, not as a claim of ownership over upstream packages.

## Specimen artwork and renderer

Original decorative artwork, nebula/background designs, ornamental compositions, textured sigil, and the finished visual specimen PNGs in `assets/specimens/` are **All Rights Reserved**. They are not licensed under the documentation or tools MIT license. Copyright © 2026 Gerald A Folsom Jr. No public redistribution or reuse license for these decorative assets is granted by MIT. The owner may distribute the approved specimen images with this release; that distribution does not grant recipients a separate artwork reuse license.

The specimen rendering program, verification scripts, and original project documentation use **MIT**, under `licenses/MIT-TOOLS.txt`. This permission excludes decorative bitmap assets and artistic visual compositions, including artwork-specific layered template designs. The MIT license on the renderer does not license the artwork it loads or its artistic layout.

Released font binaries and editable font sources remain **SIL OFL 1.1**, with Reserved Font Name **RedSigil**. Displayed glyphs are rendered from that Font Software; their appearance in an image does not relicense the font binaries or sources. Third-party dependencies retain their licenses.

License and copyright notices belong in documentation and asset notices, not on the specimen image face.
