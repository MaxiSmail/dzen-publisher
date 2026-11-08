"""
Download and extract the trained LoRA weights.
"""

from __future__ import annotations

import io
import os
import re
import zipfile
import requests

URL = "https://tmpfiles.org/wawrhW6rXUUi/alisa_lora_bundle.zip"
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")


def main() -> None:
    os.makedirs(ASSETS_DIR, exist_ok=True)
    print("Connecting to tmpfiles.org...")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    r = requests.get(URL, headers=headers, timeout=60)
    print("Page status:", r.status_code)

    match = re.search(r'href=[\'"](https://tmpfiles\.org/dl/[^\'"]+)[\'"]', r.text)
    if not match:
        dl_url = "https://tmpfiles.org/dl/wawrhW6rXUUi/alisa_lora_bundle.zip"
    else:
        dl_url = match.group(1)

    print("Downloading file from:", dl_url)
    resp = requests.get(dl_url, headers=headers, timeout=300)
    size_mb = len(resp.content) / (1024 * 1024)
    print(f"Downloaded {size_mb:.2f} MB")

    zip_file = os.path.join(ASSETS_DIR, "alisa_lora_bundle.zip")
    with open(zip_file, "wb") as f:
        f.write(resp.content)

    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        print("\nFiles inside archive:")
        for info in zf.infolist():
            print(f"  - {info.filename} ({info.file_size / (1024 * 1024):.2f} MB)")
        zf.extractall(ASSETS_DIR)

    print("\n[OK] All LoRA files successfully extracted to assets/!")


if __name__ == "__main__":
    main()
