#!/usr/bin/env python3
"""Check a PDF for page count, file size, and possible identity keywords."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_IDENTITY_KEYWORDS = [
    "学校",
    "学院",
    "大学",
    "参赛队员",
    "队员",
    "姓名",
    "学号",
    "指导教师",
    "导师",
    "赛区",
    "省赛区",
    "University",
    "College",
    "School",
    "Student ID",
    "Advisor",
    "Supervisor",
    "Instructor",
    "Region",
    "Province",
    "Email",
    "Phone",
]


def page_count_with_python(pdf_path: Path) -> int | None:
    for module_name in ("pypdf", "PyPDF2"):
        try:
            module = __import__(module_name)
            reader = module.PdfReader(str(pdf_path))
            return len(reader.pages)
        except Exception:
            continue
    return None


def page_count_with_pdfinfo(pdf_path: Path) -> int | None:
    if shutil.which("pdfinfo") is None:
        return None
    result = subprocess.run(
        ["pdfinfo", str(pdf_path)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="ignore",
    )
    if result.returncode != 0:
        return None
    match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, re.MULTILINE)
    return int(match.group(1)) if match else None


def page_count_with_regex(pdf_path: Path) -> int | None:
    data = pdf_path.read_bytes()
    matches = re.findall(rb"/Type\s*/Page\b", data)
    return len(matches) if matches else None


def extract_text_with_python(pdf_path: Path) -> str:
    chunks: list[str] = []
    for module_name in ("pypdf", "PyPDF2"):
        try:
            module = __import__(module_name)
            reader = module.PdfReader(str(pdf_path))
            for page in reader.pages:
                chunks.append(page.extract_text() or "")
            text = "\n".join(chunks)
            if text.strip():
                return text
        except Exception:
            chunks.clear()
            continue
    return ""


def extract_text_with_pdftotext(pdf_path: Path) -> str:
    if shutil.which("pdftotext") is None:
        return ""
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="ignore",
    )
    return result.stdout if result.returncode == 0 else ""


def extract_text_fallback(pdf_path: Path, limit: int) -> str:
    data = pdf_path.read_bytes()[:limit]
    return data.decode("utf-8", errors="ignore") + "\n" + data.decode("latin-1", errors="ignore")


def get_page_count(pdf_path: Path) -> int | None:
    return (
        page_count_with_python(pdf_path)
        or page_count_with_pdfinfo(pdf_path)
        or page_count_with_regex(pdf_path)
    )


def get_text(pdf_path: Path, fallback_bytes: int) -> str:
    return (
        extract_text_with_python(pdf_path)
        or extract_text_with_pdftotext(pdf_path)
        or extract_text_fallback(pdf_path, fallback_bytes)
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="PDF file to check")
    parser.add_argument("--max-pages", type=int, help="Official page limit to enforce")
    parser.add_argument("--max-size-mb", type=float, help="Official file size limit to enforce")
    parser.add_argument(
        "--keyword",
        action="append",
        default=[],
        help="Additional identity keyword to flag; can be repeated",
    )
    parser.add_argument(
        "--ignore-keyword",
        action="append",
        default=[],
        help="Identity keyword to ignore for this PDF; can be repeated",
    )
    parser.add_argument(
        "--identity-mode",
        choices=("warn", "strict"),
        default="warn",
        help="How to handle identity keyword matches. Default: warn without failing.",
    )
    parser.add_argument(
        "--fallback-text-bytes",
        type=int,
        default=2_000_000,
        help="Bytes to scan if no PDF text extractor is available",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf_path = args.pdf
    failures: list[str] = []
    warnings: list[str] = []

    if not pdf_path.is_file():
        print(f"ERROR: PDF not found: {pdf_path}")
        return 2

    size_bytes = os.path.getsize(pdf_path)
    size_mb = size_bytes / (1024 * 1024)
    print(f"File: {pdf_path}")
    print(f"Size: {size_mb:.2f} MB")

    if args.max_size_mb is not None and size_mb > args.max_size_mb:
        failures.append(f"file size {size_mb:.2f} MB exceeds limit {args.max_size_mb:.2f} MB")

    pages = get_page_count(pdf_path)
    if pages is None:
        failures.append("could not determine page count")
        print("Pages: unknown")
    else:
        print(f"Pages: {pages}")
        if args.max_pages is not None and pages > args.max_pages:
            failures.append(f"page count {pages} exceeds limit {args.max_pages}")

    text = get_text(pdf_path, args.fallback_text_bytes)
    ignored_keywords = {keyword.lower() for keyword in args.ignore_keyword if keyword}
    keywords = [
        keyword
        for keyword in DEFAULT_IDENTITY_KEYWORDS + args.keyword
        if keyword and keyword.lower() not in ignored_keywords
    ]
    found = sorted(
        {keyword for keyword in keywords if keyword.lower() in text.lower()},
        key=str.lower,
    )
    if found:
        message = "possible identity keywords found: " + ", ".join(found)
        if args.identity_mode == "strict":
            failures.append(message)
        else:
            warnings.append(message)
        print("Identity keywords: " + ", ".join(found))
        if ignored_keywords:
            print("Ignored identity keywords: " + ", ".join(args.ignore_keyword))
    else:
        print("Identity keywords: none found")

    if failures:
        print("\nFAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    if warnings:
        print("\nPASSED WITH WARNINGS")
        for warning in warnings:
            print(f"- {warning}")
        print("Rerun with `--identity-mode strict` to fail on identity keyword matches before final submission.")
        return 0

    print("\nPASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
