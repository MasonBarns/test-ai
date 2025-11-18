import sqlite3
from pathlib import Path

DB_PATH = Path("nova.db")

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            email TEXT,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    con.close()

def save_chat(user_id: str, email: str, prompt: str, response: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO chats (user_id, email, prompt, response)
        VALUES (?, ?, ?, ?)
    """, (user_id, email, prompt, response))
    con.commit()
    con.close()

def list_chats(user_id: str, limit: int = 25):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        SELECT id, prompt, response, created_at
        FROM chats
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cur.fetchall()
    con.close()
    return [
        {"id": r[0], "prompt": r[1], "response": r[2], "created_at": r[3]}
        for r in rows
    ]
