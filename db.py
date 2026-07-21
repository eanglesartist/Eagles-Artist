"""
db.py
------------------
Lightweight SQLite persistence for users / projects / credits.
Creates the three .db files declared in the folder structure
(users.db, projects.db, credits.db) on first run.
"""
import sqlite3
import os

DB_DIR = os.path.dirname(__file__)

USERS_DB = os.path.join(DB_DIR, "users.db")
PROJECTS_DB = os.path.join(DB_DIR, "projects.db")
CREDITS_DB = os.path.join(DB_DIR, "credits.db")


def init_databases():
    with sqlite3.connect(USERS_DB) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password_hash TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )"""
        )

    with sqlite3.connect(PROJECTS_DB) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                owner_email TEXT,
                title TEXT,
                scene_count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )"""
        )

    with sqlite3.connect(CREDITS_DB) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS credits (
                email TEXT PRIMARY KEY,
                balance INTEGER DEFAULT 1000
            )"""
        )


def get_credits(email: str) -> int:
    with sqlite3.connect(CREDITS_DB) as conn:
        row = conn.execute("SELECT balance FROM credits WHERE email = ?", (email,)).fetchone()
        if row is None:
            conn.execute("INSERT INTO credits (email, balance) VALUES (?, 1000)", (email,))
            return 1000
        return row[0]


def spend_credits(email: str, amount: int) -> int:
    balance = get_credits(email)
    new_balance = max(0, balance - amount)
    with sqlite3.connect(CREDITS_DB) as conn:
        conn.execute("UPDATE credits SET balance = ? WHERE email = ?", (new_balance, email))
    return new_balance


def save_project(project) -> None:
    with sqlite3.connect(PROJECTS_DB) as conn:
        conn.execute(
            """INSERT INTO projects (id, owner_email, title, scene_count)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET title=excluded.title, scene_count=excluded.scene_count""",
            (project.id, project.owner_email, project.title, len(project.scenes)),
        )
