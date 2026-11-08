import os
from pathlib import Path

# Базовые директории
BASE_DIR = Path(__file__).resolve().parent
BROWSER_DATA_DIR = BASE_DIR / "browser_data"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Файлы вывода
JSON_OUTPUT_FILE = OUTPUT_DIR / "materials.json"
MARKDOWN_OUTPUT_FILE = OUTPUT_DIR / "materials.md"

# Настройки по умолчанию
DEFAULT_CONFIG_FILE = BASE_DIR / "settings.json"
