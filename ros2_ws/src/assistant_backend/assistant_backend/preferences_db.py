"""Reine Python-Logik ohne ROS: Präferenzen in SQLite (einzeln testbar)."""
import os
import sqlite3

DB_PATH = os.environ.get("ASSISTANT_DB", os.path.expanduser("~/.assistant/assistant.db"))
LANGUAGES = {"de", "en"}   # mit Conversational abstimmen
DEFAULT_LANGUAGE = "de"


def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS preferences ("
                 "user_id INTEGER PRIMARY KEY, language TEXT NOT NULL)")
    return conn


def get_language(user_id):
    with _connect() as c:
        row = c.execute("SELECT language FROM preferences WHERE user_id=?", (user_id,)).fetchone()
    return row[0] if row else DEFAULT_LANGUAGE


def set_language(user_id, language):
    if language not in LANGUAGES:
        raise ValueError(f"Unbekannte Sprache: {language!r}")
    with _connect() as c:
        c.execute("INSERT INTO preferences(user_id, language) VALUES(?, ?) "
                  "ON CONFLICT(user_id) DO UPDATE SET language=excluded.language",
                  (user_id, language))
