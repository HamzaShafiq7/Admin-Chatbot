"""SQLite persistence layer for the WPBrigade admin chatbot."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "chatbot.db"

SEED_USERS = [
    ("admin@wpbrigade.com", "Admin", "+92000", "Head Office"),
    ("samantha@xyz.com", "Samantha", "+92300", "Lahore"),
    ("john.smith@xyz.com", "John Smith", "+92332", "Karachi"),
]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create schema and seed demo users (idempotent)."""
    conn = get_conn()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(email TEXT PRIMARY KEY, name TEXT, phone TEXT, city TEXT)"
    )
    conn.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", SEED_USERS)
    conn.commit()
    conn.close()


def email_exists(email: str) -> bool:
    conn = get_conn()
    row = conn.execute("SELECT 1 FROM users WHERE lower(email) = lower(?)", (email,)).fetchone()
    conn.close()
    return row is not None


def find_user(ident: str):
    """Resolve by email, exact name, possessive name ('samanthas'), or partial name."""
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM users WHERE lower(email) = lower(?) OR lower(name) = lower(?)",
        (ident, ident),
    ).fetchone()
    if row is None and ident.endswith("s"):
        row = conn.execute(
            "SELECT * FROM users WHERE lower(name) = lower(?)", (ident[:-1],)
        ).fetchone()
    if row is None:
        row = conn.execute(
            "SELECT * FROM users WHERE lower(name) LIKE ?", (f"%{ident.lower()}%",)
        ).fetchone()
    conn.close()
    return row


def all_users():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM users ORDER BY email").fetchall()
    conn.close()
    return rows


def add_user(email: str, name: str, phone: str) -> bool:
    conn = get_conn()
    try:
        conn.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (email, name, phone, ""))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def remove_user(email: str) -> bool:
    conn = get_conn()
    cur = conn.execute("DELETE FROM users WHERE lower(email) = lower(?)", (email,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted


def update_user(email: str, field: str, value: str) -> None:
    assert field in ("name", "phone", "city")  
    conn = get_conn()
    conn.execute(f"UPDATE users SET {field} = ? WHERE email = ?", (value, email))
    conn.commit()
    conn.close()