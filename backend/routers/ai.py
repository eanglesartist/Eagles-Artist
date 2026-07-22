from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from ..services.ai_service import enqueue_generation
import threading

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/generate")
def generate(request: schemas.JobCreate, user_id: str, db: Session = Depends(get_db)):
    # 1. Check credits
    credits = crud.get_credits(db, user_id)
    if credits < 50:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    # 2. Deduct credits
    success, new_balance = crud.deduct_credits(db, user_id, 50)
    if not success:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    # 3. Create job
    job_id = crud.create_job(db, user_id, request.prompt, request.model)
    
    # 4. Enqueue background task (Phase 4 will replace this with Celery)
    # For Phase 1/2, we use a simple thread (non-blocking)
    def process():
        # Simulate AI work
        import time
        time.sleep(5)
        # Update job with video URL (placeholder)
        video_url = "https://www.w3schools.com/html/mov_bbb.mp4"
        crud.update_job_status(db, job_id, "completed", video_url)
    
    threading.Thread(target=process).start()
    
    return {"job_id": job_id, "status": "queued", "message": "Job accepted"}

@router.get("/job/{job_id}", response_model=schemas.Job)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
