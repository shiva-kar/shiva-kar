#!/usr/bin/env python3
"""Validates the generated SVGs and README.md for quality, correctness, and layout standards.

Run: python scripts/validate.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "svg")
README_FILE = os.path.join(ROOT, "README.md")

ERRORS = []


def check(condition, message):
    if not condition:
        ERRORS.append(message)
        print(f"FAIL: {message}")
    else:
        print(f"PASS: {message}")


def main():
    print("--- 1. Root Neofetch Card Check ---")
    for name in ("dark_mode.svg", "light_mode.svg"):
        p = os.path.join(ROOT, name)
        check(os.path.exists(p) and os.path.getsize(p) > 100, f"Root {name} exists and is non-empty")

    print("\n--- 2. README.md Local Image References ---")
    with open(README_FILE, encoding="utf-8") as f:
        readme_content = f.read()

    local_imgs = [m for m in re.findall(r'(?:src|srcset)="([^"]+)"', readme_content) if not m.startswith("http")]
    missing = [img for img in local_imgs if not os.path.exists(os.path.join(ROOT, img))]
    check(len(missing) == 0, f"All {len(local_imgs)} local image references exist on disk")
    if missing:
        print(f"  Missing files: {missing}")

    print("\n--- 3. Typography Floor (font-size >= 10.5px) ---")
    font_size_pattern = re.compile(r'font-size="([\d\.]+)"')
    small_fonts = []
    svg_files = [f for f in os.listdir(OUT) if f.endswith(".svg") and not f.startswith("banner-")]
    for svg_file in svg_files:
        with open(os.path.join(OUT, svg_file), encoding="utf-8") as f:
            content = f.read()
        for sz_str in font_size_pattern.findall(content):
            if float(sz_str) < 10.5:
                small_fonts.append((svg_file, float(sz_str)))

    check(len(small_fonts) == 0, f"Checked {len(svg_files)} SVGs: all text elements have font-size >= 10.5px")
    if small_fonts:
        print(f"  Found small fonts: {small_fonts[:5]}")

    print("\n--- 4. Zero AI Long Dashes Check ---")
    dash_issues = []
    for svg_file in svg_files + ["../../README.md"]:
        p = os.path.join(OUT, svg_file)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                c = f.read()
            if "\u2014" in c or "\u2013" in c:
                dash_issues.append(svg_file)
    check(len(dash_issues) == 0, "Zero em dashes or en dashes found in rendered output")

    print("\n--- 5. Unbranded Check ---")
    branded = []
    for svg_file in svg_files + ["../../README.md"]:
        p = os.path.join(OUT, svg_file)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                c = f.read()
            if "sagargupta" in c.lower():
                branded.append(svg_file)
    check(len(branded) == 0, "Zero external profile credits or mentions found")

    print("\n" + "=" * 40)
    if ERRORS:
        print(f"Validation FAILED with {len(ERRORS)} error(s).")
        sys.exit(1)
    else:
        print(f"Validation PASSED! All {len(svg_files)} SVGs and README.md are verified.")
        sys.exit(0)


if __name__ == "__main__":
    main()
