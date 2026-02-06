from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

# 프로젝트 루트 기준 data/app.db 사용 (news랑 같은 DB)
DB_PATH = Path("data/app.db")


def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_emoji_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS emoji_items (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              prompt TEXT NOT NULL,
              model TEXT NOT NULL,
              filename_png TEXT NOT NULL,
              filename_webp TEXT,
              size INTEGER DEFAULT 512,
              transparent INTEGER DEFAULT 1,
              created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def insert_emoji_item(
    prompt: str,
    model: str,
    filename_png: str,
    filename_webp: Optional[str] = None,
    size: int = 512,
    transparent: int = 1,
) -> int:
    now = datetime.now(timezone.utc).isoformat()
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO emoji_items (prompt, model, filename_png, filename_webp, size, transparent, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (prompt, model, filename_png, filename_webp, size, transparent, now),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_recent_emoji_items(limit: int = 50) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, prompt, model, filename_png, filename_webp, size, transparent, created_at
            FROM emoji_items
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]




def update_emoji_filename_png(item_id: int, filename_png: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE emoji_items SET filename_png=? WHERE id=?",
            (filename_png, item_id),
        )
        conn.commit()


def get_emoji_item(item_id: int):
    with get_conn() as conn:
        row = conn.execute(
            """
            SELECT id, prompt, model, filename_png, filename_webp, size, transparent, created_at
            FROM emoji_items
            WHERE id = ?
            """,
            (item_id,),
        ).fetchone()
        return dict(row) if row else None


def delete_emoji_item(item_id: int) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM emoji_items WHERE id = ?", (item_id,))
        conn.commit()