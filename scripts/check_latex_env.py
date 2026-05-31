#!/usr/bin/env python3
"""Check local LaTeX class availability for modeling contest templates."""

from __future__ import annotations

import shutil
import subprocess
import sys
import argparse


def kpsewhich(filename: str) -> str | None:
    if shutil.which("kpsewhich") is None:
        return None
    result = subprocess.run(
        ["kpsewhich", filename],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    path = result.stdout.strip()
    return path if result.returncode == 0 and path else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--use-ref-bib",
        action="store_true",
        help="Also verify that BibTeX is available for ref.bib workflows.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if shutil.which("kpsewhich") is None:
        print("ERROR: kpsewhich not found. Install TeX Live or MiKTeX and ensure it is on PATH.")
        return 1

    checks = {
        "mcmthesis.cls": kpsewhich("mcmthesis.cls"),
        "cumcmthesis.cls": kpsewhich("cumcmthesis.cls"),
    }

    missing = []
    for cls_name, path in checks.items():
        if path:
            print(f"OK: {cls_name} found at {path}")
        else:
            missing.append(cls_name)
            print(f"MISSING: {cls_name}")

    if "mcmthesis.cls" in missing:
        print("Hint for MCM/ICM: install the package with `tlmgr install mcmthesis` or the MiKTeX package manager.")

    if "cumcmthesis.cls" in missing:
        print(
            "Hint for CUMCM: cumcmthesis is a common template class and may not be available through tlmgr. "
            "Download/provide the CUMCMThesis template locally, install it in your TeX tree, or use "
            "`templates/cumcm/main-ctexart-fallback.tex`."
        )

    if args.use_ref_bib:
        if shutil.which("bibtex") is None:
            missing.append("bibtex")
            print("MISSING: bibtex")
            print("Hint for ref.bib: install BibTeX through TeX Live, MiKTeX, or your TeX package manager.")
        else:
            print(f"OK: bibtex found at {shutil.which('bibtex')}")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
