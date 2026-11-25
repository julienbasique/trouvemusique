"""Sessions mémorisées : réponses du quiz, styles, retours j'aime/j'aime pas."""

import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "trouvemusique.db"


def _connexion():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db() -> None:
    with _connexion() as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS sessions (
                id          TEXT PRIMARY KEY,
                created_at  TEXT NOT NULL,
                reponses    TEXT NOT NULL,
                gains       TEXT NOT NULL DEFAULT '{}',
                scores      TEXT NOT NULL,
                retours     TEXT NOT NULL DEFAULT '[]',
                vus         TEXT NOT NULL DEFAULT '[]'
            )"""
        )


def nouvelle_session(reponses: dict, gains: dict, scores: dict, vus: list) -> str:
    sid = uuid.uuid4().hex[:12]
    with _connexion() as con:
        con.execute(
            "INSERT INTO sessions (id, created_at, reponses, gains, scores, vus) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (sid, datetime.now().isoformat(timespec="seconds"),
             json.dumps(reponses, ensure_ascii=False),
             json.dumps(gains, ensure_ascii=False),
             json.dumps(scores, ensure_ascii=False),
             json.dumps(vus, ensure_ascii=False)),
        )
    return sid


def lire(sid: str) -> dict | None:
    with _connexion() as con:
        r = con.execute("SELECT * FROM sessions WHERE id = ?", (sid,)).fetchone()
        if not r:
            return None
        return {
            "id": r["id"],
            "reponses": json.loads(r["reponses"]),
            "gains": json.loads(r["gains"]),
            "scores": json.loads(r["scores"]),
            "retours": json.loads(r["retours"]),
            "vus": json.loads(r["vus"]),
        }


def maj_retours(sid: str, retours: list, vus: list) -> None:
    with _connexion() as con:
        con.execute(
            "UPDATE sessions SET retours = ?, vus = ? WHERE id = ?",
            (json.dumps(retours, ensure_ascii=False),
             json.dumps(vus, ensure_ascii=False), sid),
        )
