#!/usr/bin/env python3
"""Owner-only launcher for v1.0.1 specimens; MIT-licensed launcher code.

Decorative artwork assets and the original sigil are separately reserved and
are intentionally not stored in the public source repository.
"""
from pathlib import Path
import argparse
import subprocess
import sys

DEFAULT_KIT = Path.home() / "RedSigil-Type-System-v1.0.1-Integrated-Naming-Correction" / "specimen-workspace"
DEFAULT_OUTPUT = Path.home() / "redsigil-v1.0.1-specimen-renders-r1"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", nargs="?", choices=["preflight", "render", "validate", "artwork-proof", "check-kit"], default="render")
    parser.add_argument("--kit", type=Path, default=DEFAULT_KIT)
    parser.add_argument("--fonts", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--only", choices=["hero", "display", "everyday", "mono", "symbols"])
    parser.add_argument("--scale", type=int, choices=[1, 2], default=1)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    if not (repo / ".git").is_dir():
        parser.error("Expected existing RS-Type-System repository with .git")
    kit = args.kit.expanduser().resolve()
    target = kit / "render.py"
    if not target.is_file() or not (kit / "MANIFEST.json").is_file():
        parser.error("Missing private artwork kit. Pass --kit /path/to/specimen-workspace; not distributed in the public repo")
    cmd = [sys.executable, str(target), args.action, "--repo", str(repo), "--output", str(args.output.expanduser()), "--scale", str(args.scale)]
    if args.fonts: cmd += ["--fonts", str(args.fonts.expanduser())]
    if args.only: cmd += ["--only", args.only]
    return subprocess.run(cmd, check=False).returncode

if __name__ == "__main__":
    sys.exit(main())
