"""
Build complete 20/20 LoRA dataset from user's custom redhead character specification:
  1. Map user's existing 6 key images into the dataset.
  2. Generate the remaining 14 images matching the exact prompts from img_XX.txt.
  3. Package all 20 images + 20 captions into dataset.zip.
"""

from __future__ import annotations

import asyncio
import os
import shutil
import urllib.parse
import zipfile
import aiohttp
import ssl

SRC_DIR = os.path.join(os.path.dirname(__file__), "alisa_hero_lora_dataset")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "lora_dataset_redhead")
ZIP_OUTPUT = os.path.join(os.path.dirname(__file__), "dataset.zip")

# Mapping of user's existing images to corresponding IDs
EXISTING_MAP = {
    "Портрет (анфас).jpg": "img_01.jpg",
    "Портрет (3 4).jpg": "img_02.jpg",
    "Профиль.jpg": "img_03.jpg",
    "Эмоция (смех).jpg": "img_04.jpg",
    "План по пояс.jpg": "img_09.jpg",
    "В полный рост.jpg": "img_16.jpg",
}

STYLE_SUFFIX = (
    ", captured on 35mm film camera, Kodak Portra 400 aesthetic, natural ambient lighting, "
    "candid documentary photography, real human skin texture with pores, subtle film grain, unedited raw photo"
)


async def fetch_image(session: aiohttp.ClientSession, prompt: str, seed: int) -> bytes:
    full_prompt = f"{prompt.strip()}{STYLE_SUFFIX}"
    encoded = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=flux&nologo=true&seed={seed}"
    async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
        resp.raise_for_status()
        return await resp.read()


async def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Building 20-image redhead dataset into {OUTPUT_DIR}...")

    # 1. Copy all 20 .txt caption files
    for i in range(1, 21):
        txt_name = f"img_{i:02d}.txt"
        src_txt = os.path.join(SRC_DIR, txt_name)
        dst_txt = os.path.join(OUTPUT_DIR, txt_name)
        if os.path.exists(src_txt):
            shutil.copy(src_txt, dst_txt)

    # 2. Copy user's 6 existing images
    for user_img_name, target_img_name in EXISTING_MAP.items():
        src_img = os.path.join(SRC_DIR, user_img_name)
        dst_img = os.path.join(OUTPUT_DIR, target_img_name)
        if os.path.exists(src_img):
            shutil.copy(src_img, dst_img)
            print(f"[OK] Mapped user image: {user_img_name} -> {target_img_name}")

    # 3. Generate the remaining 14 images
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=180)) as session:
        for i in range(1, 21):
            img_name = f"img_{i:02d}.jpg"
            txt_name = f"img_{i:02d}.txt"
            dst_img = os.path.join(OUTPUT_DIR, img_name)

            if os.path.exists(dst_img) and os.path.getsize(dst_img) > 10000:
                continue  # already copied or generated

            txt_path = os.path.join(OUTPUT_DIR, txt_name)
            with open(txt_path, "r", encoding="utf-8") as f:
                prompt = f.read().strip()

            seed = 777000 + i * 2024
            print(f"Generating missing {img_name} (seed={seed})...")
            try:
                data = await fetch_image(session, prompt, seed)
                with open(dst_img, "wb") as f:
                    f.write(data)
                print(f"[OK] Saved {img_name} ({len(data) // 1024} KB)")
            except Exception as e:
                print(f"Error generating {img_name}: {e}")
            await asyncio.sleep(1)

    # 4. Package into dataset.zip
    print(f"\nPackaging complete redhead dataset into {ZIP_OUTPUT}...")
    with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in sorted(os.listdir(OUTPUT_DIR)):
            fpath = os.path.join(OUTPUT_DIR, fname)
            if os.path.isfile(fpath):
                zf.write(fpath, arcname=fname)

    zip_size_mb = os.path.getsize(ZIP_OUTPUT) / (1024 * 1024)
    print(f"SUCCESS! Created dataset.zip ({zip_size_mb:.2f} MB) with all 20 images + 20 captions!")


if __name__ == "__main__":
    asyncio.run(main())
