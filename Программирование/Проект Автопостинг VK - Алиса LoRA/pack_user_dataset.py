"""
Package user's 18 real images into a clean, paired dataset.zip:
  - img_01.jpg .. img_04.jpg (User original portraits)
  - 10.jpg .. 23.jpg -> img_05.jpg .. img_18.jpg (User new generation shots)
  - Pair each with matching img_01.txt .. img_18.txt containing ALISA_HERO trigger word.
"""

from __future__ import annotations

import os
import shutil
import zipfile

SRC_DIR = os.path.join(os.path.dirname(__file__), "lora_dataset_redhead")
CLEAN_DIR = os.path.join(os.path.dirname(__file__), "clean_lora_dataset")
ZIP_OUTPUT = os.path.join(os.path.dirname(__file__), "dataset.zip")
ARTIFACT_ZIP = r"C:\Users\User\.gemini\antigravity\brain\e3a1221b-a9fa-4f1e-a397-89e7f7932519\dataset.zip"

# The 18 user-provided images in logical order:
USER_IMAGE_SEQUENCE = [
    "img_01.jpg",  # Front portrait
    "img_02.jpg",  # 3/4 portrait
    "img_03.jpg",  # Profile portrait
    "img_04.jpg",  # Laughing expression
    "10.jpg",      # Shot 5
    "11.jpg",      # Shot 6
    "12.jpg",      # Shot 7
    "13.jpg",      # Shot 8
    "14.jpg",      # Shot 9
    "15.jpg",      # Shot 10
    "16.jpg",      # Shot 11
    "17.jpg",      # Shot 12
    "18.jpg",      # Shot 13
    "19.jpg",      # Shot 14
    "20.jpg",      # Shot 15
    "21.jpg",      # Shot 16
    "22.jpg",      # Shot 17
    "23.jpg",      # Shot 18
]


def main() -> None:
    if os.path.exists(CLEAN_DIR):
        shutil.rmtree(CLEAN_DIR)
    os.makedirs(CLEAN_DIR, exist_ok=True)

    print("Assembling clean dataset from user's 18 custom photos...")

    for idx, src_filename in enumerate(USER_IMAGE_SEQUENCE, start=1):
        target_base = f"alisa_{idx:02d}"
        target_img_name = f"{target_base}.jpg"
        target_txt_name = f"{target_base}.txt"

        src_img_path = os.path.join(SRC_DIR, src_filename)
        src_txt_path = os.path.join(SRC_DIR, f"img_{idx:02d}.txt")

        dst_img_path = os.path.join(CLEAN_DIR, target_img_name)
        dst_txt_path = os.path.join(CLEAN_DIR, target_txt_name)

        if os.path.exists(src_img_path):
            shutil.copy(src_img_path, dst_img_path)

        if os.path.exists(src_txt_path):
            shutil.copy(src_txt_path, dst_txt_path)
        else:
            # Fallback caption
            with open(dst_txt_path, "w", encoding="utf-8") as f:
                f.write("photo of ALISA_HERO woman, vibrant red hair, warm amber eyes, clean skin, larger bust, confident expression")

        size_kb = os.path.getsize(dst_img_path) // 1024
        print(f"[{idx:02d}/18] Paired: {src_filename} -> {target_img_name} ({size_kb} KB) + {target_txt_name}")

    # Build dataset.zip
    print(f"\nCreating {ZIP_OUTPUT}...")
    with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in sorted(os.listdir(CLEAN_DIR)):
            fpath = os.path.join(CLEAN_DIR, fname)
            if os.path.isfile(fpath):
                zf.write(fpath, arcname=fname)

    # Copy to artifacts directory
    os.makedirs(os.path.dirname(ARTIFACT_ZIP), exist_ok=True)
    shutil.copy(ZIP_OUTPUT, ARTIFACT_ZIP)

    zip_size_mb = os.path.getsize(ZIP_OUTPUT) / (1024 * 1024)
    print(f"SUCCESS! Created dataset.zip ({zip_size_mb:.2f} MB) with 18 user photos + 18 captions.")


if __name__ == "__main__":
    main()
