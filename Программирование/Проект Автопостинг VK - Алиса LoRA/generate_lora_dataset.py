"""
Generate complete 20-image LoRA training dataset for ALISA_HERO persona:
  - 8 Headshots & Close-ups (front, 3/4, profile, expressions)
  - 7 Medium Shots (poses, hands, angles, waist-up)
  - 5 Full Body Shots (posture, proportions, sitting, standing)
Generates matching .txt caption files with trigger word ALISA_HERO and packages into dataset.zip.
"""

from __future__ import annotations

import asyncio
import io
import os
import random
import urllib.parse
import zipfile
import aiohttp
import ssl

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "lora_dataset")
ZIP_OUTPUT = os.path.join(os.path.dirname(__file__), "dataset.zip")
TRIGGER_WORD = "ALISA_HERO"

BASE_DNA = (
    "Authentic raw candid 35mm film photograph of the exact same 24yo slavic woman ALISA_HERO, "
    "distinctive shaggy layered wolf-cut messy black hair with textured curtain bangs reaching collarbone, "
    "striking large emerald green eyes, subtle winged eyeliner, pale porcelain skin with light freckles, "
    "plump natural lips, authentic real human skin texture with pores, realistic curvy feminine proportions, "
    "completely NO tattoos, NO body ink, NO piercings, NO nose ring, "
)

STYLE_SUFFIX = (
    ", captured on 35mm film camera, Kodak Portra 400 aesthetic, natural ambient lighting, "
    "candid documentary photography, subtle film grain, real lens bokeh, unedited raw photo"
)

DATASET_SPECS = [
    # --- 8 Headshots / Close-ups ---
    {
        "id": "01",
        "prompt": f"{BASE_DNA}close-up headshot portrait, looking directly at camera with a calm neutral expression, plain neutral background{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, close up headshot portrait, front view, looking at camera, neutral calm expression, black wolf cut hair with bangs, green eyes, natural freckles",
    },
    {
        "id": "02",
        "prompt": f"{BASE_DNA}close-up portrait, three-quarter view angle turned slightly to the left, gentle warm smile, eyes looking at camera, soft studio light{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, close up portrait, three quarter view left, gentle smile, looking at camera, black wolf cut hair, green eyes",
    },
    {
        "id": "03",
        "prompt": f"{BASE_DNA}close-up portrait, three-quarter view angle turned slightly to the right, slight head tilt, natural window daylight{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, close up portrait, three quarter view right, slight head tilt, soft window lighting, black wolf cut hair, green eyes",
    },
    {
        "id": "04",
        "prompt": f"{BASE_DNA}clean side profile shot from the side, showing jawline, ear, shaggy wolf-cut layers and neck, looking to the side{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, side profile shot, looking to the side, showing jawline and shaggy black wolf cut hair",
    },
    {
        "id": "05",
        "prompt": f"{BASE_DNA}close-up portrait, expressive wide green eyes, subtle surprised curious expression, soft ambient light{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, close up portrait, expressive wide green eyes, surprised curious expression, black wolf cut hair",
    },
    {
        "id": "06",
        "prompt": f"{BASE_DNA}close-up portrait, bright natural morning sunlight casting soft shadows, showing detailed skin texture and delicate freckles{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, close up portrait, natural morning sunlight, detailed skin texture, light freckles, black wolf cut hair, green eyes",
    },
    {
        "id": "07",
        "prompt": f"{BASE_DNA}close-up portrait, thoughtful calm gaze looking slightly off-camera, soft moody indoor light{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, close up portrait, thoughtful gaze looking away from camera, soft lighting, black wolf cut hair, green eyes",
    },
    {
        "id": "08",
        "prompt": f"{BASE_DNA}slightly high angle close-up portrait, looking up towards the camera lens, soft ambient daylight{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, high angle close up portrait, looking up at camera, black wolf cut hair with bangs, green eyes",
    },

    # --- 7 Medium Shots (Waist-Up) ---
    {
        "id": "09",
        "prompt": f"{BASE_DNA}medium waist-up shot, front facing, standing with arms relaxed, wearing a simple casual red ribbed tank dress, neutral interior{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, medium shot, waist up, standing front facing, wearing a red tank dress, black wolf cut hair, green eyes",
    },
    {
        "id": "10",
        "prompt": f"{BASE_DNA}medium shot, sitting at a wooden cafe table, resting chin gently on one hand, looking at camera, wearing a casual dark t-shirt{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, medium shot, sitting at a wooden table, resting chin on hand, wearing a dark tshirt, black wolf cut hair",
    },
    {
        "id": "11",
        "prompt": f"{BASE_DNA}medium shot, three-quarter pose, standing with arms crossed, wearing a casual beige linen button-up shirt, clean background{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, medium shot, standing three quarter angle, arms crossed, wearing a beige linen shirt, black wolf cut hair",
    },
    {
        "id": "12",
        "prompt": f"{BASE_DNA}medium shot, turning back and looking over her shoulder towards the camera, wearing a casual dark summer top, outdoor park background{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, medium shot, looking over shoulder at camera, wearing casual summer top, black wolf cut hair",
    },
    {
        "id": "13",
        "prompt": f"{BASE_DNA}medium shot, candid natural outdoor daylight, standing against a rustic brick wall, wearing an olive green sleeveless top{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, medium shot, outdoor daylight, brick wall background, wearing an olive green top, black wolf cut hair",
    },
    {
        "id": "14",
        "prompt": f"{BASE_DNA}medium shot, holding an antique hardcover book in her hands, indoor warm library room, looking at camera with a gentle expression{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, medium shot, holding a book, library background, black wolf cut hair, green eyes",
    },
    {
        "id": "15",
        "prompt": f"{BASE_DNA}medium shot, dynamic candid talking pose with natural hand gesture, wearing a simple navy blue casual shirt, blurred room background{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, medium shot, talking with hand gesture, wearing a navy blue shirt, black wolf cut hair",
    },

    # --- 5 Full Body Shots ---
    {
        "id": "16",
        "prompt": f"{BASE_DNA}full length body shot, standing upright front facing with natural posture, wearing a red ribbed sundress and casual sneakers, clean minimalist room{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, full body shot, standing front view, natural posture, wearing a red sundress and sneakers, full length",
    },
    {
        "id": "17",
        "prompt": f"{BASE_DNA}full length body shot, three-quarter walking pose, wearing a casual olive linen dress, natural daylight, full body visible from head to shoes{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, full body shot, three quarter walking pose, wearing an olive linen dress, full length",
    },
    {
        "id": "18",
        "prompt": f"{BASE_DNA}full length body shot, sitting comfortably on a vintage wooden armchair, relaxed natural pose, wearing casual jeans and a simple fitted top{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, full body shot, sitting in an armchair, relaxed posture, wearing jeans and fitted top, full length",
    },
    {
        "id": "19",
        "prompt": f"{BASE_DNA}full length shot, leaning relaxed against a plain neutral studio wall, casual posture, wearing a khaki jumpsuit, full body framing{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, full body shot, leaning against wall, wearing a khaki jumpsuit, full length",
    },
    {
        "id": "20",
        "prompt": f"{BASE_DNA}full length candid shot, looking through an antique globe in a library, standing pose showing full body and posture, soft ambient lighting{STYLE_SUFFIX}",
        "caption": f"photo of {TRIGGER_WORD} woman, full body shot, standing next to a globe in library, full length, black wolf cut hair",
    },
]


async def fetch_image(session: aiohttp.ClientSession, prompt: str, seed: int) -> bytes:
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=flux&nologo=true&seed={seed}"
    async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
        resp.raise_for_status()
        return await resp.read()


async def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Generating 20 LoRA dataset images into {OUTPUT_DIR}...")

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=180)) as session:
        for idx, item in enumerate(DATASET_SPECS, start=1):
            file_base = f"alisa_{item['id']}"
            jpg_path = os.path.join(OUTPUT_DIR, f"{file_base}.jpg")
            txt_path = os.path.join(OUTPUT_DIR, f"{file_base}.txt")

            # Write caption .txt
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(item["caption"])

            if os.path.exists(jpg_path) and os.path.getsize(jpg_path) > 10000:
                print(f"[{idx}/20] Exists: {file_base}.jpg")
                continue

            seed = 100000 + idx * 1337 + random.randint(1, 999)
            print(f"[{idx}/20] Downloading {file_base}.jpg (seed={seed})...")
            try:
                img_data = await fetch_image(session, item["prompt"], seed)
                with open(jpg_path, "wb") as f:
                    f.write(img_data)
                print(f"[{idx}/20] Saved {file_base}.jpg ({len(img_data) // 1024} KB)")
            except Exception as e:
                print(f"[{idx}/20] Error fetching {file_base}: {e}")
            await asyncio.sleep(1)

    # Package into dataset.zip
    print(f"\nPackaging dataset into {ZIP_OUTPUT}...")
    with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in os.listdir(OUTPUT_DIR):
            fpath = os.path.join(OUTPUT_DIR, fname)
            if os.path.isfile(fpath):
                zf.write(fpath, arcname=fname)

    zip_size_mb = os.path.getsize(ZIP_OUTPUT) / (1024 * 1024)
    print(f"SUCCESS! Created dataset.zip ({zip_size_mb:.2f} MB) with 20 images + 20 caption files.")


if __name__ == "__main__":
    asyncio.run(main())
