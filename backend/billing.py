import sqlite3

DATABASE_URL = "database/studio.db"

def add_credits_to_database(customer_email: str, credits_to_add: int):
    """
    Connects to the database and adds credits to the specified user account.
    """
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Ensure table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            credits INTEGER DEFAULT 0
        )
    """)
    
    # Check if user exists
    cursor.execute("SELECT credits FROM users WHERE email = ?", (customer_email,))
    row = cursor.fetchone()
    
    if row:
        new_balance = row[0] + credits_to_add
        cursor.execute("UPDATE users SET credits = ? WHERE email = ?", (new_balance, customer_email))
    else:
        # If user record doesn't exist yet, create it with baseline + purchased credits
        cursor.execute("INSERT INTO users (email, credits) VALUES (?, ?)", (customer_email, credits_to_add))
        
    conn.commit()
    conn.close()
