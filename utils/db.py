import sqlite3
import uuid

DB_PATH = "users.db"

def init_db():
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (user_id TEXT PRIMARY KEY, credits INTEGER DEFAULT 1250)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (session_id TEXT PRIMARY KEY, user_id TEXT, amount INTEGER, status TEXT)''')
    conn.commit()
    conn.close()

def get_or_create_user(user_id):
    """Get a user, create with default credits if new."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT credits FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    if result is None:
        c.execute("INSERT INTO users (user_id, credits) VALUES (?, ?)", (user_id, 1250))
        conn.commit()
        credits = 1250
    else:
        credits = result[0]
    conn.close()
    return credits

def get_user_credits(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT credits FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 1250

def deduct_credits(user_id, amount):
    """Deduct credits if sufficient. Returns (success, new_balance)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT credits FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    if result is None or result[0] < amount:
        conn.close()
        return False, 0
    new_balance = result[0] - amount
    c.execute("UPDATE users SET credits = ? WHERE user_id=?", (new_balance, user_id))
    conn.commit()
    conn.close()
    return True, new_balance

def add_credits(user_id, amount, session_id=None):
    """Add credits and log transaction."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, credits) VALUES (?, ?)", (user_id, 1250))
    c.execute("UPDATE users SET credits = credits + ? WHERE user_id=?", (amount, user_id))
    if session_id:
        c.execute("INSERT OR REPLACE INTO transactions (session_id, user_id, amount, status) VALUES (?, ?, ?, ?)",
                  (session_id, user_id, amount, "processed"))
    conn.commit()
    conn.close()
    return get_user_credits(user_id)

def transaction_exists(session_id):
    """Check if a Stripe session was already processed (idempotency)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM transactions WHERE session_id=?", (session_id,))
    exists = c.fetchone() is not None
    conn.close()
    return exists
