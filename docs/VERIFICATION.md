# Source and compiled-font verification

The included standalone verifiers test version 1.001 source metadata, the independently mapped Delta/increment glyphs, expected output counts, compiled version/name tables, and TTF/WOFF2 table content parity.

Run source inspection:

```bash
python tools/stable_font_verify.py --sources
```

Run focused Greek Delta tests:

```bash
python -m unittest tools/test_greek_delta_check.py
```

After a production build, run compiled verification:

```bash
python tools/stable_font_verify.py --compiled ./build-output --report ./build-output/QA_REPORT.json
```

Release-package checksums will be generated anew in the **04 — Release Verification** archive. Do not substitute v1.0.0 hashes or treat v1.0.0 provenance as evidence that v1.0.1 binaries were built from the curated source layout.

**Recorded production history:** 32/32 v1.0.1 fonts passed a feature-branch production build and independent checks (Actions run 42083737306). The merge revision is a36f1dfcf8579a235a467d235cbd1104e0d1a5ad. The current *publicly curated* copy has not yet undergone its own complete production rebuild.
