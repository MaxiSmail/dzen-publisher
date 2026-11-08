# -*- coding: utf-8 -*-
from __future__ import annotations
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
Automated LoRA training pipeline via HuggingFace:
  1. Upload dataset images to HF Dataset repo (via commit API)
  2. Create HF Space with Gradio training app (runs on HF's free T4 GPU)
  3. Print Space URL for user to click Start
"""


import base64
import json
import os
import time
import zipfile
from pathlib import Path

import requests

HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_USERNAME = "MaxiSmail"
DATASET_REPO = f"{HF_USERNAME}/alisa-hero-dataset"
SPACE_REPO = f"{HF_USERNAME}/alisa-lora-trainer"
MODEL_REPO = f"{HF_USERNAME}/alisa-lora-v1"
DATASET_ZIP = str(Path(__file__).parent / "dataset.zip")

AUTH_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}


def create_repo(repo_id: str, repo_type: str, space_sdk: str = None) -> None:
    name = repo_id.split("/")[1]
    payload = {"name": name, "type": repo_type, "private": False}
    if space_sdk:
        payload["sdk"] = space_sdk
    r = requests.post(
        "https://huggingface.co/api/repos/create",
        headers={**AUTH_HEADERS, "Content-Type": "application/json"},
        json=payload,
    )
    if r.status_code in (200, 409):
        print(f"  [OK] {repo_type} repo: {repo_id}")
    else:
        print(f"  [ERR] Create {repo_type} repo: {r.status_code} {r.text[:200]}")


def commit_files(repo_id: str, files: dict, repo_type: str, message: str = "Upload") -> None:
    """Commit multiple files using HF commit API."""
    type_map = {"dataset": "datasets", "model": "models", "space": "spaces"}
    type_url = type_map.get(repo_type, repo_type)

    operations = []
    for path, content in files.items():
        if isinstance(content, str):
            content = content.encode()
        content_b64 = base64.b64encode(content).decode()
        operations.append({
            "op": "addOrUpdate",
            "path": path,
            "content": content_b64,
            "encoding": "base64",
        })

    payload = {"message": message, "operations": operations}
    url = f"https://huggingface.co/api/{type_url}/{repo_id}/commit/main"
    r = requests.post(
        url,
        headers={**AUTH_HEADERS, "Content-Type": "application/json"},
        json=payload,
    )
    if r.status_code in (200, 201):
        paths = [op["path"] for op in operations]
        print(f"  [OK] Committed {len(operations)} files: {paths}")
    else:
        print(f"  [FAIL] Commit: {r.status_code} {r.text[:200]}")


def upload_dataset() -> None:
    print("\n=== Step 1: Uploading dataset to HF ===")
    create_repo(DATASET_REPO, "dataset")

    with zipfile.ZipFile(DATASET_ZIP, "r") as zf:
        all_files = {
            name: zf.read(name)
            for name in zf.namelist()
            if not name.endswith("/")
        }

    print(f"  Total files in zip: {len(all_files)}")
    items = list(all_files.items())

    # Commit in batches of 5 files
    BATCH = 5
    for i in range(0, len(items), BATCH):
        batch = dict(items[i:i+BATCH])
        commit_files(DATASET_REPO, batch, "dataset", f"Upload batch {i//BATCH+1}")
        time.sleep(1)

    print(f"  Dataset uploaded: https://huggingface.co/datasets/{DATASET_REPO}")


APP_PY = '''import os
import sys
import subprocess
import shutil
import requests
import gradio as gr
from pathlib import Path

HF_TOKEN = os.getenv("HF_TOKEN", "")
DATASET_REPO = "MaxiSmail/alisa-hero-dataset"
MODEL_REPO   = "MaxiSmail/alisa-lora-v1"
OUTPUT_DIR   = "/tmp/lora_out"
DATA_DIR     = "/tmp/dataset"

def run_training():
    lines = []
    def log(msg):
        lines.append(msg)
        print(msg)

    try:
        log("=== Installing packages ===")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q",
            "diffusers==0.30.3", "transformers==4.44.2",
            "peft==0.13.2", "accelerate==0.34.2",
            "safetensors", "bitsandbytes", "huggingface_hub"],
            check=True, capture_output=True)
        log("Packages installed OK")

        log("=== Downloading dataset ===")
        from huggingface_hub import snapshot_download
        ds_path = snapshot_download(
            repo_id=DATASET_REPO, repo_type="dataset",
            token=HF_TOKEN, local_dir="/tmp/hf_ds")
        shutil.rmtree(DATA_DIR, ignore_errors=True)
        os.makedirs(DATA_DIR)
        copied = 0
        for f in Path(ds_path).rglob("*"):
            if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".txt"):
                shutil.copy(f, DATA_DIR)
                copied += 1
        log(f"Dataset ready: {copied} files in {DATA_DIR}")

        log("=== Downloading training script v0.30.3 ===")
        url = "https://raw.githubusercontent.com/huggingface/diffusers/v0.30.3/examples/dreambooth/train_dreambooth_lora.py"
        r = requests.get(url, timeout=60)
        with open("/tmp/train.py", "w") as f:
            f.write(r.text)
        log("Script downloaded OK")

        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
        os.makedirs(OUTPUT_DIR)

        log("=== Starting LoRA training (500 steps) ===")
        cmd = [
            sys.executable, "/tmp/train.py",
            "--pretrained_model_name_or_path", "runwayml/stable-diffusion-v1-5",
            "--instance_data_dir", DATA_DIR,
            "--output_dir", OUTPUT_DIR,
            "--instance_prompt", "a photo of ALISA_HERO woman, vibrant red hair, warm amber eyes",
            "--resolution", "512",
            "--train_batch_size", "1",
            "--gradient_accumulation_steps", "1",
            "--learning_rate", "1e-4",
            "--lr_scheduler", "constant",
            "--lr_warmup_steps", "0",
            "--max_train_steps", "500",
            "--mixed_precision", "fp16",
            "--seed", "42",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        log(result.stdout[-3000:] if result.stdout else "(no stdout)")
        if result.returncode != 0:
            log("!!! TRAINING FAILED !!!")
            log(result.stderr[-2000:])
            return "\\n".join(lines)

        log("=== Uploading weights to HF Model Repo ===")
        from huggingface_hub import HfApi
        api = HfApi(token=HF_TOKEN)
        for fpath in Path(OUTPUT_DIR).rglob("*"):
            if fpath.is_file():
                size = fpath.stat().st_size // 1024
                api.upload_file(
                    path_or_fileobj=str(fpath),
                    path_in_repo=fpath.name,
                    repo_id=MODEL_REPO, repo_type="model")
                log(f"  Uploaded: {fpath.name} ({size} KB)")

        log("")
        log("=" * 50)
        log("TRAINING COMPLETE!")
        log(f"Model saved: https://huggingface.co/{MODEL_REPO}")
        log("=" * 50)

    except Exception as exc:
        import traceback
        log(f"ERROR: {exc}")
        log(traceback.format_exc())

    return "\\n".join(lines)


with gr.Blocks(title="ALISA_HERO LoRA Trainer") as demo:
    gr.Markdown("# ALISA_HERO LoRA Trainer\\nClick the button to start training on HF GPU.")
    btn = gr.Button("Start Training", variant="primary", size="lg")
    out = gr.Textbox(label="Training Log", lines=40, max_lines=80)
    btn.click(fn=run_training, outputs=out)

demo.launch()
'''

REQUIREMENTS_TXT = """gradio>=4.0
diffusers==0.30.3
transformers==4.44.2
peft==0.13.2
accelerate==0.34.2
safetensors
bitsandbytes
huggingface_hub
requests
torch
torchvision
"""

README_MD = """---
title: Alisa Lora Trainer
emoji: 🎨
colorFrom: red
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
hardware: t4-small
---
# ALISA_HERO LoRA Trainer
Click **Start Training** to begin. Weights auto-uploaded to model repo when done.
"""


def create_space() -> None:
    print("\n=== Step 2: Creating HF Training Space ===")
    create_repo(SPACE_REPO, "space", space_sdk="gradio")
    time.sleep(2)

    space_files = {
        "app.py": APP_PY.encode(),
        "requirements.txt": REQUIREMENTS_TXT.encode(),
        "README.md": README_MD.encode(),
    }
    commit_files(SPACE_REPO, space_files, "space", "Initialize LoRA trainer app")

    print(f"\n  Space URL: https://huggingface.co/spaces/{SPACE_REPO}")


def main() -> None:
    upload_dataset()
    create_space()

    print("\n" + "="*60)
    print("PIPELINE READY!")
    print(f"1. Dataset:  https://huggingface.co/datasets/{DATASET_REPO}")
    print(f"2. Space:    https://huggingface.co/spaces/{SPACE_REPO}")
    print(f"3. Model:    https://huggingface.co/{MODEL_REPO}")
    print()
    print("Space запустится автоматически на GPU T4 через ~2-3 мин.")
    print("Или откройте ссылку выше и нажмите 'Start Training'.")
    print("="*60)


if __name__ == "__main__":
    main()
