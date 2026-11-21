import sqlite3
from pathlib import Path
from contextlib import contextmanager
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sufyan_hub.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        username = "sufyan"
        password = __import__("os").environ.get("HUB_PASSWORD", "MSufyan141R")
        existing = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if not existing:
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )

def verify_user(username, password):
    with get_db() as db:
        user = db.execute("SELECT password_hash FROM users WHERE username = ?", (username,)).fetchone()
    return bool(user and check_password_hash(user["password_hash"], password))

def get_tasks():
    with get_db() as db:
        return db.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()

def add_task(title):
    with get_db() as db:
        db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))

def toggle_task(task_id):
    with get_db() as db:
        db.execute("""
            UPDATE tasks SET completed = CASE completed WHEN 0 THEN 1 ELSE 0 END
            WHERE id = ?
        """, (task_id,))

def delete_task(task_id):
    with get_db() as db:
        db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
