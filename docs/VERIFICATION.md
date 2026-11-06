# Verification — RedSigilΔ Type System v1.0.1

## Source and font checks

The included verifiers check source version **1.001**, independently encoded Delta/increment mappings, expected compiled file counts, version/name tables and TTF/WOFF2 parity.

```bash
python tools/stable_font_verify.py --sources
```

```bash
python tools/greek_delta_check.py
```

```bash
python -m unittest tools/test_greek_delta_check.py
```

```bash
python tools/stable_font_verify.py --compiled ./build-output --report ./build-output/QA_REPORT.json
```

## Published build provenance

- Source: `c956f7fc483a8a2d5bf6af8b35a643e8d3147a24`.
- Successful run: [42104786087](https://github.com/RedSigilDelta/RS-Type-System/actions/runs/42104786087).
- Artifact: `redsigil-v1.0.1-stable-fonts-42104786087`.
- Outputs: 13 static TTF + 3 variable TTF + 16 WOFF2 = **32**.
- Downloaded compiled verifier: **PASS**, 32/32.
- Independent saved font SHA-256 rechecks: **PASS**, 32/32.

The workflow artifact download includes an outer artifact-named folder. Pass the folder containing the `display/`, `everyday/` and `mono/` children as the compiled-verifier root.

## Release ZIP integrity

Package **04 — Release Verification** carries build QA data, file checksums for the 32 font binaries and SHA-256 hashes for Packages 01–03. The separately published `SHA256SUMS_v1.0.1.txt` covers all four numbered ZIPs.

From a directory containing the five release assets:

```bash
sha256sum -c SHA256SUMS_v1.0.1.txt
```

Do not substitute v1.0.0 checksums for v1.0.1 files. The published v1.0.1 binaries derive from the source commit above; later documentation-only commits do not alter the compiled fonts.
