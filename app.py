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
    conn.commit()
    conn.close()

init_db()

class GenerateRequest(BaseModel):
    prompt: str
    user_id: str
    model: str = "veo"

class CreditDeductRequest(BaseModel):
    user_id: str
    amount: int = 50

def get_user_credits(user_id: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row["credits"] if row else 1250

def deduct_credits(user_id: str, amount: int) -> tuple[bool, int]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if not row:
        conn.execute("INSERT INTO users (user_id, credits) VALUES (?, ?)", (user_id, 1250))
        conn.commit()
        credits = 1250
    else:
        credits = row["credits"]
    
    if credits < amount:
        conn.close()
        return False, credits
    
    new_balance = credits - amount
    conn.execute("UPDATE users SET credits = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()
    return True, new_balance

@app.get("/credits/{user_id}")
def get_credits(user_id: str):
    return {"user_id": user_id, "credits": get_user_credits(user_id)}

@app.post("/credits/deduct")
def deduct(request: CreditDeductRequest):
    success, new_balance = deduct_credits(request.user_id, request.amount)
    if not success:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    return {"user_id": request.user_id, "credits": new_balance}

@app.post("/generate")
def generate_video(request: GenerateRequest):
    success, new_balance = deduct_credits(request.user_id, 50)
    if not success:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    job_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
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

@app.get("/job/{job_id}")
def get_job_status(job_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Job not found")
    return dict(row)
