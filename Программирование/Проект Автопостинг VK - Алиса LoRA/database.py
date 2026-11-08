"""
Database module — async SQLite via aiosqlite.
Stores post history, prevents topic duplication.
"""

from __future__ import annotations

import logging
from typing import Optional

import aiosqlite

from config import get_settings

logger = logging.getLogger(__name__)

_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS posts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    topic       TEXT    NOT NULL,
    title       TEXT    NOT NULL,
    fact_text   TEXT    NOT NULL,
    image_url   TEXT,
    vk_post_id  INTEGER,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

_CREATE_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_posts_topic ON posts (topic);
"""


async def _get_connection() -> aiosqlite.Connection:
    """Open (or create) the SQLite database."""
    settings = get_settings()
    conn = await aiosqlite.connect(str(settings.db_path))
    conn.row_factory = aiosqlite.Row
    return conn


async def init_db() -> None:
    """Initialize the database schema."""
    conn = await _get_connection()
    try:
        await conn.execute(_CREATE_TABLE_SQL)
        await conn.execute(_CREATE_INDEX_SQL)
        await conn.commit()
        logger.info("Database initialized at %s", get_settings().db_path)
    finally:
        await conn.close()


async def is_topic_exists(topic: str) -> bool:
    """Check whether a topic has already been used."""
    conn = await _get_connection()
    try:
        cursor = await conn.execute(
            "SELECT 1 FROM posts WHERE LOWER(topic) = LOWER(?) LIMIT 1",
            (topic,),
        )
        row = await cursor.fetchone()
        return row is not None
    finally:
        await conn.close()


async def get_recent_topics(limit: int = 50) -> list[str]:
    """Return the most recent *limit* topics ordered newest-first."""
    conn = await _get_connection()
    try:
        cursor = await conn.execute(
            "SELECT topic FROM posts ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        return [row[0] for row in rows]
    finally:
        await conn.close()


async def save_post(
    topic: str,
    title: str,
    fact_text: str,
    image_url: Optional[str] = None,
    vk_post_id: Optional[int] = None,
) -> int:
    """Persist a published post and return its row id."""
    conn = await _get_connection()
    try:
        cursor = await conn.execute(
            """
            INSERT INTO posts (topic, title, fact_text, image_url, vk_post_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (topic, title, fact_text, image_url, vk_post_id),
        )
        await conn.commit()
        row_id = cursor.lastrowid or 0
        logger.info("Post saved — id=%d, topic=%r", row_id, topic)
        return row_id
    finally:
        await conn.close()
