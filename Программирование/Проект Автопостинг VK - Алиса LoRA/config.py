"""
Configuration module — loads settings from .env via pydantic-settings.
"""

from __future__ import annotations

import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Application settings, loaded from .env file at the project root."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── VK API ──────────────────────────────────────────────
    vk_access_token: str
    vk_group_id: int
    vk_api_version: str = "5.199"

    # ── LLM API ─────────────────────────────────────────────
    llm_api_key: str
    llm_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    llm_model: str = "gemini-3.6-flash"

    # ── Image Generation API ────────────────────────────────
    image_api_key: str
    image_api_url: str = "https://api.fal.ai/v1"
    image_model: str = "fal-ai/flux/schnell"

    # ── Scheduler ───────────────────────────────────────────
    post_interval_hours: int = 3

    # ── Rendering ───────────────────────────────────────────
    card_width: int = 1080
    card_height: int = 1350

    # ── Logging ─────────────────────────────────────────────
    log_level: str = "INFO"

    # ── Derived paths ───────────────────────────────────────
    @property
    def fonts_dir(self) -> Path:
        return BASE_DIR / "fonts"

    @property
    def assets_dir(self) -> Path:
        return BASE_DIR / "assets"

    @property
    def db_path(self) -> Path:
        return BASE_DIR / "posts.db"

    @property
    def default_font_path(self) -> Path:
        return self.fonts_dir / "Montserrat-Bold.ttf"


def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()  # type: ignore[call-arg]


def setup_logging(level: str = "INFO") -> None:
    """Configure root logger with a human-friendly format."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
