from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import uuid
import threading
import time
from typing import Optional

app = FastAPI(title="AI Cinematic Studio API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "https://your-streamlit-app.streamlit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            credits INTEGER DEFAULT 1250
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            user_id TEXT,
            prompt TEXT,
            model TEXT,
            status TEXT DEFAULT 'queued',
            video_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT,
            amount INTEGER,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

class GenerateRequest(BaseModel):
    prompt: str
    user_id: str
    model: str = "veo"

class CreditAddRequest(BaseModel):
    user_id: str
    amount: int
    stripe_session_id: Optional[str] = None

def get_user_credits(user_id: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row["credits"] if row else 1250

@app.get("/credits/{user_id}")
def get_credits(user_id: str):
    return {"user_id": user_id, "credits": get_user_credits(user_id)}

@app.post("/credits/add")
def add_credits(request: CreditAddRequest):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Ensure user exists
    cur = conn.execute("SELECT credits FROM users WHERE user_id = ?", (request.user_id,))
    row = cur.fetchone()
    if not row:
        conn.execute("INSERT INTO users (user_id, credits) VALUES (?, ?)", (request.user_id, 1250))
        current_credits = 1250
    else:
        current_credits = row["credits"]
        
    new_balance = current_credits + request.amount
    conn.execute("UPDATE users SET credits = ? WHERE user_id = ?", (new_balance, request.user_id))
    
    if request.stripe_session_id:
        conn.execute(
            "INSERT OR REPLACE INTO transactions (session_id, user_id, amount, status) VALUES (?, ?, ?, ?)",
            (request.stripe_session_id, request.user_id, request.amount, "completed")
        )
        
    conn.commit()
    conn.close()
    return {"user_id": request.user_id, "credits": new_balance}

@app.post("/ai/generate")
def generate_video(request: GenerateRequest):
    credits = get_user_credits(request.user_id)
    if credits < 50:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    # Deduct 50 credits automatically
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET credits = credits - 50 WHERE user_id = ?", (request.user_id,))
    
    job_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO jobs (job_id, user_id, prompt, model, status) VALUES (?, ?, ?, ?, ?)",
        (job_id, request.user_id, request.prompt, request.model, "queued")
    )
    conn.commit()
    conn.close()

    def process():
        time.sleep(5)
        c = sqlite3.connect(DB_PATH)
        c.execute("UPDATE jobs SET status = ?, video_url = ? WHERE job_id = ?", 
                  ("completed", "https://www.w3schools.com/html/mov_bbb.mp4", job_id))
        c.commit()
        c.close()

    threading.Thread(target=process).start()
    return {"job_id": job_id, "status": "queued"}

@app.get("/ai/job/{job_id}")
def get_job_status(job_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Job not found")
    return dict(row)
