"""
Download Montserrat-Bold.ttf from Google Fonts into the fonts/ directory.

Usage:
    python download_font.py
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

FONT_URL = (
    "https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Bold.ttf"
)
TARGET_DIR = Path(__file__).resolve().parent / "fonts"
TARGET_FILE = TARGET_DIR / "Montserrat-Bold.ttf"


def main() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    if TARGET_FILE.exists():
        print(f"[OK] Font already exists: {TARGET_FILE}")
        return

    print("Downloading Montserrat-Bold.ttf from GitHub...")
    try:
        urllib.request.urlretrieve(FONT_URL, TARGET_FILE)
        size_kb = TARGET_FILE.stat().st_size // 1024
        print(f"[OK] Downloaded successfully: {TARGET_FILE} ({size_kb} KB)")
    except Exception as exc:
        print(f"[FAIL] Download failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
